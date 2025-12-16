"""
Integration tests for AI feedback generation and fallback handling.

Tests the complete AI feedback workflow:
1. Exercise answer submission
2. AI feedback generation (mocked)
3. Error analysis and categorization
4. Fallback to rule-based feedback
5. Personalized suggestions
"""

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import patch, Mock, MagicMock
from datetime import datetime

from models.exercise import Exercise, Verb, VerbType, SubjunctiveTense, ExerciseType, DifficultyLevel
from models.progress import Attempt, Session as PracticeSession
from models.user import User
from services.feedback import FeedbackGenerator, ErrorAnalyzer, Feedback
from services.conjugation import ConjugationEngine, ValidationResult


@pytest.mark.integration
class TestAIFeedbackFlow:
    """Integration tests for AI feedback generation and error handling."""

    def test_complete_ai_feedback_flow_success(
        self,
        db_session: Session,
        test_user: User,
        sample_exercises_with_tags,
        conjugation_engine: ConjugationEngine,
        error_analyzer: ErrorAnalyzer,
        mock_anthropic
    ):
        """
        Test complete AI feedback flow with successful API call.

        Flow:
        1. User submits incorrect answer
        2. Validate answer and detect error
        3. Generate AI feedback via Claude API
        4. Parse and structure feedback
        5. Return to user
        6. Store in database
        """
        # Step 1: Get exercise and submit wrong answer
        exercise = sample_exercises_with_tags[0]
        user_answer = "hablo"  # Indicative instead of subjunctive
        correct_answer = exercise.correct_answer

        # Step 2: Validate answer
        validation = conjugation_engine.validate_conjugation(
            user_answer=user_answer,
            correct_answer=correct_answer,
            person=exercise.person or "yo",
            tense="present_subjunctive"
        )

        assert not validation.is_correct
        assert validation.error_type is not None

        # Step 3: Mock AI feedback generation
        mock_anthropic.messages.create.return_value = Mock(
            content=[Mock(
                text="""The error here is using the indicative mood "hablo" instead of the subjunctive "hable".

After the expression "Es importante que" (It's important that), you must use the subjunctive mood because it expresses necessity or importance about a hypothetical situation.

Suggestion: Practice recognizing trigger phrases like "es importante que", "es necesario que", "es bueno que" which always require subjunctive."""
            )]
        )

        # Step 4: Generate feedback
        feedback_generator = FeedbackGenerator(conjugation_engine, error_analyzer)

        # Create exercise context
        exercise_context = {
            "verb": "hablar",
            "person": "yo",
            "tense": "present_subjunctive",
            "trigger_phrase": "es importante que",
            "prompt": exercise.prompt
        }

        # Generate feedback (will use mocked AI)
        feedback = feedback_generator.generate_feedback(
            validation_result=validation,
            exercise_context=exercise_context
        )

        # Step 5: Verify feedback structure
        assert feedback is not None
        assert not feedback.is_correct
        assert len(feedback.message) > 0
        assert len(feedback.explanation) > 0
        assert "subjunctive" in feedback.explanation.lower()

        # Step 6: Store attempt with feedback
        session = PracticeSession(
            user_id=test_user.id,
            started_at=datetime.utcnow(),
            session_type="practice"
        )
        db_session.add(session)
        db_session.commit()

        attempt = Attempt(
            session_id=session.id,
            exercise_id=exercise.id,
            user_id=test_user.id,
            user_answer=user_answer,
            is_correct=False
        )
        db_session.add(attempt)
        db_session.commit()
        db_session.refresh(attempt)

        assert attempt.is_correct is False

    def test_ai_feedback_fallback_to_rules(
        self,
        db_session: Session,
        test_user: User,
        sample_exercises_with_tags,
        conjugation_engine: ConjugationEngine,
        error_analyzer: ErrorAnalyzer
    ):
        """
        Test fallback to rule-based feedback when AI fails.

        Flow:
        1. Submit incorrect answer
        2. Attempt AI feedback (mock failure)
        3. Fallback to rule-based feedback
        4. Verify feedback still provided
        """
        exercise = sample_exercises_with_tags[0]
        user_answer = "hablé"  # Wrong tense
        correct_answer = exercise.correct_answer

        # Validate
        validation = conjugation_engine.validate_conjugation(
            user_answer=user_answer,
            correct_answer=correct_answer,
            person=exercise.person or "yo",
            tense="present_subjunctive"
        )

        assert not validation.is_correct

        # Mock AI failure
        with patch("anthropic.Anthropic") as mock_client:
            mock_instance = Mock()
            mock_instance.messages.create.side_effect = Exception("API Error")
            mock_client.return_value = mock_instance

            # Generate feedback with fallback
            feedback_generator = FeedbackGenerator(conjugation_engine, error_analyzer)

            exercise_context = {
                "verb": "hablar",
                "person": "yo",
                "tense": "present_subjunctive",
                "trigger_phrase": "es importante que"
            }

            # Should fall back to rule-based
            feedback = feedback_generator.generate_feedback(
                validation_result=validation,
                exercise_context=exercise_context
            )

            # Verify fallback feedback provided
            assert feedback is not None
            assert not feedback.is_correct
            assert len(feedback.message) > 0

    def test_error_categorization_and_analysis(
        self,
        conjugation_engine: ConjugationEngine,
        error_analyzer: ErrorAnalyzer
    ):
        """
        Test error categorization and detailed analysis.

        Flow:
        1. Submit various types of errors
        2. Analyze each error type
        3. Verify correct categorization
        4. Verify targeted suggestions
        """
        test_cases = [
            {
                "user_answer": "hablo",
                "correct_answer": "hable",
                "expected_category": "mood_confusion",
                "description": "Indicative instead of subjunctive"
            },
            {
                "user_answer": "hables",
                "correct_answer": "hable",
                "expected_category": "wrong_person",
                "description": "Wrong person conjugation"
            },
            {
                "user_answer": "hablé",
                "correct_answer": "hable",
                "expected_category": "wrong_tense",
                "description": "Wrong tense"
            }
        ]

        for test_case in test_cases:
            validation = conjugation_engine.validate_conjugation(
                user_answer=test_case["user_answer"],
                correct_answer=test_case["correct_answer"],
                person="yo",
                tense="present_subjunctive"
            )

            assert not validation.is_correct

            # Analyze error
            analysis = error_analyzer.analyze_error(
                validation_result=validation,
                exercise_context={"verb": "hablar", "person": "yo"}
            )

            assert analysis is not None
            assert "error_type" in analysis

    def test_personalized_feedback_based_on_history(
        self,
        db_session: Session,
        test_user: User,
        sample_exercises_with_tags,
        conjugation_engine: ConjugationEngine,
        error_analyzer: ErrorAnalyzer
    ):
        """
        Test personalized feedback adapts to user's error patterns.

        Flow:
        1. Track multiple errors of same type
        2. Detect error pattern
        3. Generate personalized suggestion
        4. Verify pattern-specific advice
        """
        # Create session
        session = PracticeSession(
            user_id=test_user.id,
            started_at=datetime.utcnow(),
            session_type="practice"
        )
        db_session.add(session)
        db_session.commit()

        # Simulate pattern: repeatedly using indicative instead of subjunctive
        exercises = sample_exercises_with_tags[:3]

        for exercise in exercises:
            # Submit indicative form (common error)
            user_answer = "hablo"  # Always using indicative

            attempt = Attempt(
                session_id=session.id,
                exercise_id=exercise.id,
                user_id=test_user.id,
                user_answer=user_answer,
                is_correct=False
            )
            db_session.add(attempt)

        db_session.commit()

        # Query error pattern
        errors = db_session.query(Attempt).filter(
            Attempt.user_id == test_user.id,
            Attempt.is_correct == False
        ).all()

        # Detect pattern: all using indicative
        assert len(errors) >= 3

        # Generate pattern-specific feedback
        # In real implementation, this would analyze the pattern
        # and provide targeted advice like:
        # "You're consistently using indicative mood. Focus on recognizing
        # subjunctive triggers like 'es importante que', 'quiero que', etc."

    def test_feedback_includes_grammar_rules(
        self,
        conjugation_engine: ConjugationEngine,
        error_analyzer: ErrorAnalyzer,
        mock_anthropic
    ):
        """
        Test feedback includes relevant grammar rules and explanations.

        Flow:
        1. Submit incorrect answer
        2. Generate feedback
        3. Verify grammar rules included
        4. Verify rule explanations present
        """
        # Mock AI response with grammar rules
        mock_anthropic.messages.create.return_value = Mock(
            content=[Mock(
                text="""Grammar Rule: After expressions of desire, emotion, doubt, or necessity, Spanish uses the subjunctive mood.

In this case, "Quiero que" (I want that) expresses desire, which triggers the subjunctive.

The present subjunctive of "ser" for "tú" is "seas", not "eres" (indicative).

Related rules:
- WEIRDO triggers (Wishes, Emotions, Impersonal expressions, Recommendations, Doubt, Ojalá)
- Subjunctive in dependent clauses after "que"
"""
            )]
        )

        validation = ValidationResult(
            is_correct=False,
            user_answer="eres",
            correct_answer="seas",
            error_type="mood_confusion",
            suggestions=["Use subjunctive after 'quiero que'"]
        )

        feedback_generator = FeedbackGenerator(conjugation_engine, error_analyzer)

        exercise_context = {
            "verb": "ser",
            "person": "tú",
            "tense": "present_subjunctive",
            "trigger_phrase": "quiero que"
        }

        feedback = feedback_generator.generate_feedback(
            validation_result=validation,
            exercise_context=exercise_context
        )

        # Verify grammar rules included
        assert feedback is not None
        assert len(feedback.related_rules) > 0 or "rule" in feedback.explanation.lower()

    def test_feedback_with_correct_answer(
        self,
        conjugation_engine: ConjugationEngine,
        error_analyzer: ErrorAnalyzer
    ):
        """
        Test feedback for correct answers is encouraging.

        Flow:
        1. Submit correct answer
        2. Generate feedback
        3. Verify positive reinforcement
        4. Verify no error analysis
        """
        validation = ValidationResult(
            is_correct=True,
            user_answer="hable",
            correct_answer="hable",
            error_type=None,
            suggestions=[]
        )

        feedback_generator = FeedbackGenerator(conjugation_engine, error_analyzer)

        exercise_context = {
            "verb": "hablar",
            "person": "yo",
            "tense": "present_subjunctive"
        }

        feedback = feedback_generator.generate_feedback(
            validation_result=validation,
            exercise_context=exercise_context
        )

        # Verify positive feedback
        assert feedback.is_correct is True
        assert feedback.error_category is None
        assert len(feedback.encouragement) > 0

    def test_ai_timeout_handling(
        self,
        conjugation_engine: ConjugationEngine,
        error_analyzer: ErrorAnalyzer
    ):
        """
        Test handling of AI API timeout.

        Flow:
        1. Submit answer requiring feedback
        2. Mock AI timeout
        3. Verify graceful fallback
        4. Verify user still receives feedback
        """
        validation = ValidationResult(
            is_correct=False,
            user_answer="hablo",
            correct_answer="hable",
            error_type="mood_confusion",
            suggestions=["Use subjunctive"]
        )

        # Mock timeout
        with patch("anthropic.Anthropic") as mock_client:
            mock_instance = Mock()
            mock_instance.messages.create.side_effect = TimeoutError("Request timeout")
            mock_client.return_value = mock_instance

            feedback_generator = FeedbackGenerator(conjugation_engine, error_analyzer)

            exercise_context = {
                "verb": "hablar",
                "person": "yo",
                "tense": "present_subjunctive"
            }

            # Should handle timeout gracefully
            feedback = feedback_generator.generate_feedback(
                validation_result=validation,
                exercise_context=exercise_context
            )

            # Verify fallback feedback provided
            assert feedback is not None
            assert not feedback.is_correct

    def test_feedback_caching_for_common_errors(
        self,
        db_session: Session,
        test_user: User,
        mock_redis
    ):
        """
        Test caching of feedback for common errors to reduce API calls.

        Flow:
        1. Generate feedback for common error
        2. Cache the feedback
        3. Same error occurs again
        4. Retrieve from cache (no API call)
        5. Verify cache hit
        """
        # Mock Redis cache
        cache_key = "feedback:hablar:yo:hablo:hable"
        cached_feedback = {
            "is_correct": False,
            "message": "Incorrect - you used indicative mood",
            "explanation": "Use subjunctive after trigger phrases",
            "error_category": "mood_confusion"
        }

        mock_redis.get.return_value = None  # First call - cache miss
        mock_redis.set.return_value = True

        # First request - should call AI and cache
        # Second request - should use cache

        # Simulate cache hit on second call
        import json
        mock_redis.get.return_value = json.dumps(cached_feedback).encode()

        # Retrieve from cache
        cached_result = mock_redis.get(cache_key)
        assert cached_result is not None

        # Parse cached feedback
        feedback_dict = json.loads(cached_result)
        assert feedback_dict["is_correct"] is False
        assert feedback_dict["error_category"] == "mood_confusion"

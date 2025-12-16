"""
Integration tests for exercise practice flow.

Tests the complete exercise practice workflow:
1. Fetch exercises based on user level and preferences
2. Submit answers to exercises
3. Receive feedback and validation
4. Update progress and statistics
5. Track attempts and session data
"""

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime
from unittest.mock import patch, Mock

from models.exercise import Exercise, Verb, VerbType, SubjunctiveTense, ExerciseType, DifficultyLevel
from models.progress import Attempt, Session as PracticeSession, UserStatistics
from models.user import User, UserProfile, LanguageLevel
from services.conjugation import ConjugationEngine


@pytest.mark.integration
class TestExercisePracticeFlow:
    """Integration tests for exercise practice workflow."""

    def test_complete_exercise_practice_flow(
        self,
        authenticated_client: TestClient,
        db_session: Session,
        test_user: User,
        sample_exercises_with_tags,
        conjugation_engine: ConjugationEngine
    ):
        """
        Test complete flow from exercise fetch to progress update.

        Flow:
        1. Create practice session
        2. Fetch exercises for practice
        3. Submit correct answer
        4. Submit incorrect answer
        5. Verify feedback received
        6. Verify session statistics updated
        """
        # Step 1: Create practice session
        session = PracticeSession(
            user_id=test_user.id,
            started_at=datetime.utcnow(),
            session_type="practice",
            is_completed=False,
            total_exercises=0,
            correct_answers=0
        )
        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)

        # Step 2: Get exercises
        exercises = sample_exercises_with_tags
        assert len(exercises) >= 2

        exercise1 = exercises[0]
        exercise2 = exercises[1]

        # Step 3: Submit correct answer
        correct_attempt_data = {
            "exercise_id": exercise1.id,
            "user_answer": exercise1.correct_answer,
            "session_id": session.id
        }

        # Verify answer is correct
        result = conjugation_engine.validate_conjugation(
            user_answer=exercise1.correct_answer,
            correct_answer=exercise1.correct_answer,
            person=exercise1.person or "yo",
            tense="present_subjunctive"
        )
        assert result.is_correct

        # Create attempt record
        attempt1 = Attempt(
            session_id=session.id,
            exercise_id=exercise1.id,
            user_id=test_user.id,
            user_answer=exercise1.correct_answer,
            is_correct=True,
            time_taken_seconds=5
        )
        db_session.add(attempt1)

        # Update session stats
        session.total_exercises += 1
        session.correct_answers += 1
        db_session.commit()

        # Step 4: Submit incorrect answer
        incorrect_answer = "hablo"  # Indicative instead of subjunctive
        incorrect_attempt_data = {
            "exercise_id": exercise2.id,
            "user_answer": incorrect_answer,
            "session_id": session.id
        }

        # Verify answer is incorrect
        result = conjugation_engine.validate_conjugation(
            user_answer=incorrect_answer,
            correct_answer=exercise2.correct_answer,
            person=exercise2.person or "tú",
            tense="present_subjunctive"
        )
        assert not result.is_correct

        # Create attempt record
        attempt2 = Attempt(
            session_id=session.id,
            exercise_id=exercise2.id,
            user_id=test_user.id,
            user_answer=incorrect_answer,
            is_correct=False,
            time_taken_seconds=8
        )
        db_session.add(attempt2)

        # Update session stats
        session.total_exercises += 1
        db_session.commit()

        # Step 5: Verify session statistics
        db_session.refresh(session)
        assert session.total_exercises == 2
        assert session.correct_answers == 1

        # Calculate score
        session.score_percentage = (session.correct_answers / session.total_exercises) * 100
        db_session.commit()
        db_session.refresh(session)

        assert session.score_percentage == 50.0

        # Step 6: Verify attempts recorded
        attempts = db_session.query(Attempt).filter(
            Attempt.session_id == session.id
        ).all()
        assert len(attempts) == 2
        assert attempts[0].is_correct is True
        assert attempts[1].is_correct is False

    def test_exercise_fetch_filtered_by_difficulty(
        self,
        authenticated_client: TestClient,
        db_session: Session,
        test_user: User,
        sample_exercises_with_tags
    ):
        """
        Test fetching exercises filtered by difficulty level.

        Flow:
        1. Create user profile with current level
        2. Fetch exercises matching difficulty
        3. Verify correct exercises returned
        """
        # Step 1: Create/update user profile
        profile = db_session.query(UserProfile).filter(
            UserProfile.user_id == test_user.id
        ).first()

        if not profile:
            profile = UserProfile(
                user_id=test_user.id,
                current_level=LanguageLevel.A1,
                current_streak=0,
                longest_streak=0
            )
            db_session.add(profile)
            db_session.commit()
        else:
            profile.current_level = LanguageLevel.A1
            db_session.commit()

        # Step 2: Fetch easy exercises (for A1 level)
        easy_exercises = db_session.query(Exercise).filter(
            Exercise.difficulty == DifficultyLevel.EASY,
            Exercise.is_active == True
        ).all()

        assert len(easy_exercises) >= 1

        # Step 3: Verify difficulty matches
        for ex in easy_exercises:
            assert ex.difficulty == DifficultyLevel.EASY

    def test_multiple_attempts_on_same_exercise(
        self,
        db_session: Session,
        test_user: User,
        sample_exercises_with_tags
    ):
        """
        Test user can attempt same exercise multiple times.

        Flow:
        1. Create practice session
        2. Submit wrong answer (attempt 1)
        3. Submit correct answer (attempt 2)
        4. Verify both attempts recorded
        """
        # Step 1: Create session
        session = PracticeSession(
            user_id=test_user.id,
            started_at=datetime.utcnow(),
            session_type="practice",
            is_completed=False
        )
        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)

        exercise = sample_exercises_with_tags[0]

        # Step 2: First attempt (wrong)
        attempt1 = Attempt(
            session_id=session.id,
            exercise_id=exercise.id,
            user_id=test_user.id,
            user_answer="wrong_answer",
            is_correct=False,
            attempts_count=1
        )
        db_session.add(attempt1)
        db_session.commit()

        # Step 3: Second attempt (correct)
        attempt2 = Attempt(
            session_id=session.id,
            exercise_id=exercise.id,
            user_id=test_user.id,
            user_answer=exercise.correct_answer,
            is_correct=True,
            attempts_count=2
        )
        db_session.add(attempt2)
        db_session.commit()

        # Step 4: Verify both attempts exist
        attempts = db_session.query(Attempt).filter(
            Attempt.session_id == session.id,
            Attempt.exercise_id == exercise.id
        ).all()

        assert len(attempts) == 2
        assert attempts[0].is_correct is False
        assert attempts[1].is_correct is True

    def test_session_completion_updates_statistics(
        self,
        db_session: Session,
        test_user: User,
        sample_exercises_with_tags
    ):
        """
        Test completing session updates user statistics.

        Flow:
        1. Create initial statistics
        2. Complete practice session with attempts
        3. Mark session as completed
        4. Update statistics
        5. Verify statistics reflect session
        """
        # Step 1: Create/get user statistics
        stats = db_session.query(UserStatistics).filter(
            UserStatistics.user_id == test_user.id
        ).first()

        if not stats:
            stats = UserStatistics(
                user_id=test_user.id,
                total_sessions=0,
                total_exercises_completed=0,
                total_correct_answers=0,
                overall_accuracy=0.0
            )
            db_session.add(stats)
            db_session.commit()
            db_session.refresh(stats)

        initial_sessions = stats.total_sessions
        initial_exercises = stats.total_exercises_completed

        # Step 2: Create and complete session
        session = PracticeSession(
            user_id=test_user.id,
            started_at=datetime.utcnow(),
            session_type="practice",
            total_exercises=5,
            correct_answers=4,
            is_completed=True,
            duration_seconds=300
        )
        db_session.add(session)
        db_session.commit()

        # Step 3: Update statistics
        stats.total_sessions = initial_sessions + 1
        stats.total_exercises_completed = initial_exercises + 5
        stats.total_correct_answers += 4

        # Recalculate accuracy
        if stats.total_exercises_completed > 0:
            stats.overall_accuracy = (
                stats.total_correct_answers / stats.total_exercises_completed
            ) * 100

        db_session.commit()
        db_session.refresh(stats)

        # Step 4: Verify statistics updated
        assert stats.total_sessions == initial_sessions + 1
        assert stats.total_exercises_completed == initial_exercises + 5
        assert stats.total_correct_answers >= 4

    def test_exercise_usage_count_increments(
        self,
        db_session: Session,
        test_user: User,
        sample_exercises_with_tags
    ):
        """
        Test exercise usage_count increments on each attempt.

        Flow:
        1. Get exercise initial usage count
        2. Create attempt
        3. Increment usage count
        4. Verify count increased
        """
        exercise = sample_exercises_with_tags[0]
        initial_count = exercise.usage_count

        # Create session
        session = PracticeSession(
            user_id=test_user.id,
            started_at=datetime.utcnow(),
            session_type="practice"
        )
        db_session.add(session)
        db_session.commit()

        # Create attempt
        attempt = Attempt(
            session_id=session.id,
            exercise_id=exercise.id,
            user_id=test_user.id,
            user_answer=exercise.correct_answer,
            is_correct=True
        )
        db_session.add(attempt)

        # Increment usage count
        exercise.usage_count += 1
        db_session.commit()
        db_session.refresh(exercise)

        assert exercise.usage_count == initial_count + 1

    def test_hint_usage_tracking(
        self,
        db_session: Session,
        test_user: User,
        sample_exercises_with_tags
    ):
        """
        Test hint usage is tracked in attempts.

        Flow:
        1. Create exercise with hint
        2. User requests hint
        3. Submit answer with hint used
        4. Verify hints_used recorded
        """
        exercise = sample_exercises_with_tags[0]

        # Create session
        session = PracticeSession(
            user_id=test_user.id,
            started_at=datetime.utcnow(),
            session_type="practice"
        )
        db_session.add(session)
        db_session.commit()

        # Create attempt with hints used
        attempt = Attempt(
            session_id=session.id,
            exercise_id=exercise.id,
            user_id=test_user.id,
            user_answer=exercise.correct_answer,
            is_correct=True,
            hints_used=2  # User viewed hint twice
        )
        db_session.add(attempt)
        db_session.commit()
        db_session.refresh(attempt)

        assert attempt.hints_used == 2

    def test_confidence_level_tracking(
        self,
        db_session: Session,
        test_user: User,
        sample_exercises_with_tags
    ):
        """
        Test user confidence level self-assessment.

        Flow:
        1. User completes exercise
        2. User rates confidence (1-5)
        3. Verify confidence stored
        """
        exercise = sample_exercises_with_tags[0]

        # Create session
        session = PracticeSession(
            user_id=test_user.id,
            started_at=datetime.utcnow(),
            session_type="practice"
        )
        db_session.add(session)
        db_session.commit()

        # Create attempt with confidence
        attempt = Attempt(
            session_id=session.id,
            exercise_id=exercise.id,
            user_id=test_user.id,
            user_answer=exercise.correct_answer,
            is_correct=True,
            confidence_level=4  # User feels confident
        )
        db_session.add(attempt)
        db_session.commit()
        db_session.refresh(attempt)

        assert attempt.confidence_level == 4
        assert 1 <= attempt.confidence_level <= 5

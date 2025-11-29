"""
Custom exercise validation logic.

Handles validation of dynamically generated exercises (IDs starting with "gen_")
using ConjugationEngine, FeedbackGenerator, and LearningAlgorithm.
"""

from typing import Dict, Any
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import logging

from schemas.exercise import AnswerSubmit, AnswerValidation
from services.conjugation import ConjugationEngine
from services.feedback import FeedbackGenerator
from services.learning_algorithm import LearningAlgorithm

logger = logging.getLogger(__name__)


def extract_trigger_category(trigger_phrase: str) -> str:
    """Extract WEIRDO category from trigger phrase."""
    if not trigger_phrase:
        return None

    from utils.spanish_grammar import WEIRDO_TRIGGERS

    trigger_lower = trigger_phrase.lower()

    for category, data in WEIRDO_TRIGGERS.items():
        for trigger in data.get("triggers", []):
            if trigger.lower() in trigger_lower:
                return category

    return None


def validate_custom_exercise(
    submission: AnswerSubmit,
    current_user: Dict[str, Any],
    db: Session,
    conjugation_engine: ConjugationEngine,
    feedback_generator: FeedbackGenerator,
    learning_algorithm: LearningAlgorithm,
    save_attempt_func
) -> AnswerValidation:
    """
    Validate a custom generated exercise using ConjugationEngine.

    Custom exercises have IDs starting with "gen_" and include metadata
    in the submission (verb, tense, person, etc.).

    Args:
        submission: Answer submission with custom exercise metadata
        current_user: Current authenticated user
        db: Database session
        conjugation_engine: Conjugation validation engine
        feedback_generator: Feedback generation service
        learning_algorithm: Spaced repetition algorithm
        save_attempt_func: Function to save attempt to database

    Returns:
        AnswerValidation response with results and feedback
    """
    # Extract metadata from submission
    # Custom exercise ID format: gen_{id}_{verb}_{person}
    if not submission.verb or not submission.tense or not submission.person:
        # Try to parse from ID
        parts = submission.exercise_id.split('_')
        if len(parts) >= 4:
            # Format: gen_{id}_{verb}_{person}
            verb = parts[2] if not submission.verb else submission.verb
            person = '_'.join(parts[3:]) if not submission.person else submission.person
            tense = submission.tense or "present_subjunctive"
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Custom exercise missing required metadata (verb, tense, person)"
            )
    else:
        verb = submission.verb
        tense = submission.tense
        person = submission.person

    logger.info(f"Validating custom exercise: verb={verb}, tense={tense}, person={person}")

    # Use ConjugationEngine for validation
    try:
        validation_result = conjugation_engine.validate_answer(
            verb=verb,
            tense=tense,
            person=person,
            user_answer=submission.user_answer
        )
        is_correct = validation_result.is_correct
        correct_answer = validation_result.correct_answer

        # Generate rich feedback
        exercise_context = {
            "trigger_phrase": submission.trigger_phrase,
            "trigger_category": extract_trigger_category(submission.trigger_phrase) if submission.trigger_phrase else None,
            "explanation": submission.explanation
        }

        rich_feedback = feedback_generator.generate_feedback(
            validation_result=validation_result,
            exercise_context=exercise_context,
            user_level="intermediate"
        )

    except Exception as e:
        logger.error(f"ConjugationEngine validation failed for custom exercise: {e}")
        # Fallback to simple string comparison if provided
        if submission.correct_answer:
            user_normalized = submission.user_answer.strip().lower()
            correct_normalized = submission.correct_answer.strip().lower()
            alternative_normalized = [a.strip().lower() for a in (submission.alternative_answers or [])]

            is_correct = user_normalized == correct_normalized or user_normalized in alternative_normalized
            correct_answer = submission.correct_answer

            # Simple feedback
            class SimpleFeedback:
                message = "Excellent! Your answer is correct." if is_correct else f"Not quite. The correct answer is '{correct_answer}'."
                explanation = submission.explanation or ("Great job!" if is_correct else "Review the conjugation rules.")
                error_category = None if is_correct else "unknown_error"
                suggestions = [] if is_correct else ["Review the correct answer and try again"]
                related_rules = []
                encouragement = "Keep up the good work!" if is_correct else "Don't worry, mistakes help you learn!"
                next_steps = ["Continue practicing"] if is_correct else ["Try similar exercises"]

            rich_feedback = SimpleFeedback()
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Validation failed and no fallback answer provided: {str(e)}"
            )

    # Calculate score
    base_score = 100 if is_correct else 0

    # Time bonus
    if is_correct and submission.time_taken:
        if submission.time_taken < 10:
            base_score = min(100, base_score + 10)
        elif submission.time_taken < 20:
            base_score = min(100, base_score + 5)

    # Get alternative answers
    alternative_answers = submission.alternative_answers or []

    # Process with learning algorithm for spaced repetition
    learning_result = None
    try:
        response_time_ms = (submission.time_taken * 1000) if submission.time_taken else 5000
        learning_result = learning_algorithm.process_exercise_result(
            verb=verb,
            tense=tense,
            person=person,
            correct=is_correct,
            response_time_ms=response_time_ms,
            difficulty_felt=None
        )
        logger.info(f"Learning algorithm updated for custom exercise: next review in {learning_result['interval_days']} days")
    except Exception as e:
        logger.warning(f"Learning algorithm processing failed for custom exercise: {e}")

    # Save attempt to database (with exercise_id=None for custom exercises)
    save_attempt_func(
        db=db,
        user_id=current_user["sub"],
        exercise_id=None,  # Custom exercises don't have DB exercise_id
        user_answer=submission.user_answer,
        is_correct=is_correct,
        score=base_score,
        session_id=submission.session_id,
        time_taken_seconds=submission.time_taken
    )

    logger.info(f"User {current_user.get('sub')} submitted custom exercise answer: correct={is_correct}")

    # Build comprehensive response
    return AnswerValidation(
        is_correct=is_correct,
        correct_answer=correct_answer,
        user_answer=submission.user_answer,
        feedback=rich_feedback.message,
        explanation=rich_feedback.explanation,
        score=base_score,
        alternative_answers=alternative_answers,
        # Enhanced feedback
        error_type=rich_feedback.error_category,
        suggestions=rich_feedback.suggestions,
        related_rules=rich_feedback.related_rules,
        encouragement=rich_feedback.encouragement,
        next_steps=rich_feedback.next_steps,
        # Spaced repetition
        next_review_date=learning_result["next_review"] if learning_result else None,
        interval_days=learning_result["interval_days"] if learning_result else None,
        difficulty_level=learning_result["new_difficulty"] if learning_result else None
    )

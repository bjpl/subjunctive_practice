"""
Exercise routes: get exercises, submit answers, validation.

INTEGRATED VERSION with ConjugationEngine, FeedbackGenerator, and LearningAlgorithm.
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
import json
import random
from pathlib import Path
from datetime import datetime
import logging

from core.security import get_current_active_user
from core.database import get_db_session
from models.exercise import Exercise, ExerciseType, SubjunctiveTense, DifficultyLevel
from models.progress import Attempt
from schemas.exercise import (
    ExerciseResponse,
    AnswerSubmit,
    AnswerValidation,
    ExerciseListResponse
)

# Learning services
from services.conjugation import ConjugationEngine
from services.feedback import FeedbackGenerator, Feedback
from services.learning_algorithm import LearningAlgorithm

# Custom exercise validation
from api.custom_exercise_validation import validate_custom_exercise

# Configure logging
logger = logging.getLogger(__name__)


router = APIRouter(prefix="/exercises", tags=["Exercises"])


# Learning services singleton instances
_conjugation_engine: Optional[ConjugationEngine] = None
_feedback_generator: Optional[FeedbackGenerator] = None
_learning_algorithm: Optional[LearningAlgorithm] = None


def get_learning_services() -> tuple[ConjugationEngine, FeedbackGenerator, LearningAlgorithm]:
    """
    Get or create learning service instances (singleton pattern).

    Returns:
        Tuple of (ConjugationEngine, FeedbackGenerator, LearningAlgorithm)
    """
    global _conjugation_engine, _feedback_generator, _learning_algorithm

    if _conjugation_engine is None:
        logger.info("Initializing learning services...")
        _conjugation_engine = ConjugationEngine()
        _feedback_generator = FeedbackGenerator(_conjugation_engine)
        _learning_algorithm = LearningAlgorithm()
        logger.info("Learning services initialized successfully")

    return _conjugation_engine, _feedback_generator, _learning_algorithm


# Exercise data file (fallback only - deprecated)
EXERCISE_DATA_FILE = Path("user_data/fallback_exercises.json")


def load_exercises_from_db(
    db: Session,
    difficulty: Optional[int] = None,
    exercise_type: Optional[str] = None,
    limit: int = 50,
    random_order: bool = True
) -> List[Exercise]:
    """
    Load exercises from database with optional filtering.

    Args:
        db: Database session
        difficulty: Filter by difficulty level (1-5)
        exercise_type: Filter by subjunctive type
        limit: Maximum number of exercises to return
        random_order: Randomize exercise order

    Returns:
        List of Exercise objects from database
    """
    logger.info(f"Querying database for exercises (difficulty={difficulty}, type={exercise_type}, limit={limit})")

    query = db.query(Exercise).filter(Exercise.is_active == True)

    # Apply filters
    if difficulty is not None:
        # Convert difficulty int to DifficultyLevel enum
        try:
            diff_level = DifficultyLevel(difficulty)
            query = query.filter(Exercise.difficulty == diff_level)
        except ValueError:
            logger.warning(f"Invalid difficulty level: {difficulty}")

    if exercise_type:
        # Try to match SubjunctiveTense enum
        try:
            tense = SubjunctiveTense(exercise_type)
            query = query.filter(Exercise.tense == tense)
        except ValueError:
            logger.warning(f"Invalid exercise type: {exercise_type}")

    # Execute query
    exercises = query.all()

    logger.info(f"Found {len(exercises)} exercises in database")

    # Randomize if requested
    if random_order:
        random.shuffle(exercises)

    # Apply limit
    return exercises[:limit]


def load_exercises_from_json() -> List[Dict[str, Any]]:
    """
    Load exercises from JSON file (DEPRECATED - fallback only).
    This is kept for backward compatibility but should not be used.
    """
    logger.warning("Using deprecated JSON fallback for exercises - database should be seeded")
    if EXERCISE_DATA_FILE.exists():
        with open(EXERCISE_DATA_FILE, "r") as f:
            data = json.load(f)
            return data.get("subjunctive_exercises", [])
    return []


def normalize_answer(answer: str) -> str:
    """Normalize answer for comparison."""
    return answer.strip().lower()


def validate_answer(user_answer: str, correct_answer: str) -> bool:
    """
    Validate if user answer matches correct answer.
    Handles multiple acceptable answers separated by '/'.
    """
    user_normalized = normalize_answer(user_answer)

    # Split correct answer by '/' for alternatives
    correct_alternatives = [normalize_answer(ans) for ans in correct_answer.split('/')]

    return user_normalized in correct_alternatives


@router.get("", response_model=ExerciseListResponse)
async def get_exercises(
    difficulty: Optional[int] = Query(None, ge=1, le=5, description="Filter by difficulty"),
    exercise_type: Optional[str] = Query(None, description="Filter by subjunctive type"),
    tags: Optional[str] = Query(None, description="Filter by tags (comma-separated)"),
    limit: int = Query(10, ge=1, le=50, description="Number of exercises to return"),
    random_order: bool = Query(True, description="Randomize exercise order"),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: Session = Depends(get_db_session)
):
    """
    Get practice exercises with optional filtering.

    - **difficulty**: Filter by difficulty level (1-5)
    - **exercise_type**: Filter by subjunctive type (present_subjunctive, imperfect_subjunctive, etc.)
    - **tags**: Filter by tags (comma-separated, e.g., "trigger-phrases,common-verbs")
    - **limit**: Number of exercises to return (default: 10)
    - **random_order**: Randomize exercise order (default: true)

    Requires authentication.
    """
    # Load exercises from database
    exercises = load_exercises_from_db(
        db=db,
        difficulty=difficulty,
        exercise_type=exercise_type,
        limit=limit,
        random_order=random_order
    )

    # Apply tag filtering if specified
    if tags:
        tag_list = [tag.strip() for tag in tags.split(',')]
        exercises = [
            ex for ex in exercises
            if ex.tags and any(tag in ex.tags for tag in tag_list)
        ]

    if not exercises:
        logger.warning("No exercises found in database")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No exercises available"
        )

    logger.info(f"Returning {len(exercises)} exercises to user {current_user.get('sub')}")

    # Convert to response models using from_attributes (Pydantic v2)
    exercise_responses = [
        ExerciseResponse.model_validate(ex)
        for ex in exercises
    ]

    # Get total count for pagination
    total_query = db.query(Exercise).filter(Exercise.is_active == True)
    if difficulty is not None:
        try:
            diff_level = DifficultyLevel(difficulty)
            total_query = total_query.filter(Exercise.difficulty == diff_level)
        except ValueError:
            pass
    if exercise_type:
        try:
            tense = SubjunctiveTense(exercise_type)
            total_query = total_query.filter(Exercise.tense == tense)
        except ValueError:
            pass

    total_count = total_query.count()

    return ExerciseListResponse(
        exercises=exercise_responses,
        total=len(exercise_responses),
        page=1,
        page_size=limit,
        has_more=total_count > limit
    )


@router.get("/{exercise_id}", response_model=ExerciseResponse)
async def get_exercise_by_id(
    exercise_id: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: Session = Depends(get_db_session)
):
    """
    Get a specific exercise by ID.

    - **exercise_id**: Unique exercise identifier

    Requires authentication.
    """
    # Convert exercise_id to int
    try:
        ex_id = int(exercise_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid exercise ID format: {exercise_id}"
        )

    # Query database
    exercise = db.query(Exercise).filter(
        Exercise.id == ex_id,
        Exercise.is_active == True
    ).first()

    if not exercise:
        logger.warning(f"Exercise {exercise_id} not found in database")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise {exercise_id} not found"
        )

    logger.info(f"Returning exercise {exercise_id} to user {current_user.get('sub')}")

    return ExerciseResponse.model_validate(exercise)


@router.post("/submit", response_model=AnswerValidation)
async def submit_answer(
    submission: AnswerSubmit,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: Session = Depends(get_db_session)
):
    """
    Submit an answer for validation with intelligent feedback.

    Uses ConjugationEngine for validation, FeedbackGenerator for rich feedback,
    and LearningAlgorithm for spaced repetition scheduling.

    Handles both database exercises and custom generated exercises (IDs starting with "gen_").

    - **exercise_id**: Exercise identifier (or "gen_" for custom exercises)
    - **user_answer**: User's submitted answer
    - **time_taken**: Optional time taken in seconds
    - **verb/tense/person**: Required for custom exercises

    Returns validation result with feedback and score.
    Requires authentication.
    """
    # Get learning services
    conjugation_engine, feedback_generator, learning_algorithm = get_learning_services()

    # Check if this is a custom generated exercise
    is_custom_exercise = submission.exercise_id.startswith("gen_")

    if is_custom_exercise:
        # Handle custom exercise validation
        return validate_custom_exercise(
            submission=submission,
            current_user=current_user,
            db=db,
            conjugation_engine=conjugation_engine,
            feedback_generator=feedback_generator,
            learning_algorithm=learning_algorithm,
            save_attempt_func=save_user_attempt_to_db
        )

    # Standard database exercise validation
    # Convert exercise_id to int
    try:
        ex_id = int(submission.exercise_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid exercise ID format: {submission.exercise_id}"
        )

    # Query database for exercise
    exercise = db.query(Exercise).filter(
        Exercise.id == ex_id,
        Exercise.is_active == True
    ).first()

    if not exercise:
        logger.warning(f"Exercise {submission.exercise_id} not found for answer submission")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise {submission.exercise_id} not found"
        )

    correct_answer = exercise.correct_answer
    is_correct = validate_answer(submission.user_answer, correct_answer)

    # Calculate score based on correctness and time
    base_score = 100 if is_correct else 0

    # Time bonus (if answer is correct and quick)
    if is_correct and submission.time_taken:
        if submission.time_taken < 10:
            base_score = min(100, base_score + 10)
        elif submission.time_taken < 20:
            base_score = min(100, base_score + 5)

    # Generate feedback
    if is_correct:
        feedback = "Excellent! Your answer is correct."
    else:
        feedback = f"Not quite. The correct answer is '{correct_answer}'."

    # Get alternative answers
    alternative_answers = []
    if exercise.alternative_answers:
        alternative_answers = exercise.alternative_answers
    elif '/' in correct_answer:
        alternative_answers = correct_answer.split('/')

    # Save user's attempt to database
    save_user_attempt_to_db(
        db=db,
        user_id=current_user["sub"],
        exercise_id=ex_id,
        user_answer=submission.user_answer,
        is_correct=is_correct,
        score=base_score
    )

    logger.info(f"User {current_user.get('sub')} submitted answer for exercise {ex_id}: correct={is_correct}")

    return AnswerValidation(
        is_correct=is_correct,
        correct_answer=correct_answer,
        user_answer=submission.user_answer,
        feedback=feedback,
        explanation=exercise.explanation or "",
        score=base_score,
        alternative_answers=alternative_answers
    )


def save_user_attempt_to_db(
    db: Session,
    user_id: str,
    exercise_id: Optional[int],
    user_answer: str,
    is_correct: bool,
    score: int,
    session_id: Optional[int] = None,
    time_taken_seconds: Optional[int] = None
):
    """
    Save user attempt to database.

    If session_id is provided, appends attempt to existing session and updates stats.
    Otherwise, creates a standalone session (legacy behavior for backwards compatibility).

    Args:
        db: Database session
        user_id: User ID (string like "user_7" or numeric)
        exercise_id: Exercise ID (None for custom exercises)
        user_answer: User's submitted answer
        is_correct: Whether answer was correct
        score: Score achieved (0-100)
        session_id: Optional session ID to append attempt to
        time_taken_seconds: Optional time taken to complete
    """
    # Convert user_id string to int (assuming format like "user_7")
    try:
        if isinstance(user_id, str):
            # Extract numeric part if user_id is like "user_7"
            user_id_int = int(user_id.split('_')[-1]) if '_' in user_id else int(user_id)
        else:
            user_id_int = int(user_id)
    except (ValueError, IndexError):
        logger.error(f"Invalid user_id format: {user_id}")
        # For now, skip saving if we can't parse user_id
        # In production, we'd want better user ID handling
        return

    from models.progress import Session as PracticeSession

    # If session_id provided, append to existing session
    if session_id:
        practice_session = db.query(PracticeSession).filter(
            PracticeSession.id == session_id,
            PracticeSession.user_id == user_id_int
        ).first()

        if practice_session:
            # Update session stats
            practice_session.total_exercises = (practice_session.total_exercises or 0) + 1
            practice_session.correct_answers = (practice_session.correct_answers or 0) + (1 if is_correct else 0)
            practice_session.score_percentage = (
                (practice_session.correct_answers / practice_session.total_exercises) * 100
            ) if practice_session.total_exercises > 0 else 0
        else:
            logger.warning(f"Session {session_id} not found for user {user_id}, creating new session")
            session_id = None  # Fall through to create new session

    # Create a new session if no session_id provided or session not found
    if not session_id:
        practice_session = PracticeSession(
            user_id=user_id_int,
            started_at=datetime.utcnow(),
            ended_at=datetime.utcnow(),
            total_exercises=1,
            correct_answers=1 if is_correct else 0,
            score_percentage=score,
            session_type="practice",
            is_completed=True
        )
        db.add(practice_session)
        db.flush()  # Get the session ID

    attempt = Attempt(
        session_id=practice_session.id,
        user_id=user_id_int,
        exercise_id=exercise_id,  # Can be None for custom exercises
        user_answer=user_answer,
        is_correct=is_correct,
        time_taken_seconds=time_taken_seconds
    )
    db.add(attempt)
    db.commit()
    logger.info(f"Saved attempt for user {user_id} on exercise {exercise_id}")


def save_user_attempt_to_json(
    user_id: str,
    exercise_id: str,
    user_answer: str,
    is_correct: bool,
    score: int
):
    """Save user attempt to file (DEPRECATED - fallback only)."""
    logger.warning("Using deprecated JSON fallback for saving attempts")
    attempts_file = Path(f"user_data/attempts_{user_id}.json")
    attempts_file.parent.mkdir(exist_ok=True)

    attempts = []
    if attempts_file.exists():
        with open(attempts_file, "r") as f:
            attempts = json.load(f)

    attempts.append({
        "exercise_id": exercise_id,
        "user_answer": user_answer,
        "is_correct": is_correct,
        "score": score,
        "timestamp": datetime.utcnow().isoformat()
    })

    with open(attempts_file, "w") as f:
        json.dump(attempts, f, indent=2)


@router.get("/types/available", response_model=List[str])
async def get_available_exercise_types(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: Session = Depends(get_db_session)
):
    """
    Get list of available exercise types.

    Requires authentication.
    """
    # Query distinct exercise types from database
    types = db.query(Exercise.tense).filter(Exercise.is_active == True).distinct().all()
    type_values = sorted([t[0].value for t in types if t[0] is not None])

    logger.info(f"Available exercise types: {type_values}")

    return type_values


def parse_user_id(user_id_str: str) -> int:
    """Parse user ID from string format (e.g., 'user_7' or '7') to int."""
    if isinstance(user_id_str, int):
        return user_id_str
    if '_' in user_id_str:
        return int(user_id_str.split('_')[-1])
    return int(user_id_str)


# ============================================================================
# Spaced Repetition / Review Endpoints
# ============================================================================

from schemas.exercise import DueReviewResponse, DueReviewItem, ReviewStatsResponse


@router.get("/review/due", response_model=DueReviewResponse)
async def get_due_reviews(
    limit: int = Query(10, ge=1, le=50, description="Maximum number of due items to return"),
    tense: Optional[str] = Query(None, description="Filter by tense"),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: Session = Depends(get_db_session)
):
    """
    Get exercises that are due for review based on spaced repetition schedule.

    Returns items ordered by most overdue first, with metadata about difficulty
    level and review performance.
    """
    from models.progress import ReviewSchedule
    from models.exercise import Verb
    from datetime import timedelta

    # Parse user ID
    try:
        user_id_int = parse_user_id(current_user["sub"])
    except (ValueError, IndexError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    # Query for due reviews
    now = datetime.utcnow()
    query = db.query(ReviewSchedule).filter(
        ReviewSchedule.user_id == user_id_int,
        ReviewSchedule.next_review_date <= now
    ).join(Verb)

    # Order by most overdue first
    query = query.order_by(ReviewSchedule.next_review_date.asc())

    # Get all due items (we'll limit after processing)
    due_schedules = query.all()

    # Build response items
    items = []
    for schedule in due_schedules:
        # Calculate days overdue
        time_diff = now - schedule.next_review_date
        days_overdue = max(0, time_diff.days)

        # Calculate success rate
        success_rate = 0.0
        if schedule.total_attempts > 0:
            success_rate = (schedule.total_correct / schedule.total_attempts) * 100

        # Determine difficulty level based on SM-2 parameters
        difficulty_level = "new"
        if schedule.review_count == 0:
            difficulty_level = "new"
        elif schedule.easiness_factor < 2.0:
            difficulty_level = "learning"
        elif schedule.easiness_factor < 2.5:
            difficulty_level = "reviewing"
        else:
            difficulty_level = "mastered"

        # Create review item
        item = DueReviewItem(
            verb_id=schedule.verb_id,
            verb_infinitive=schedule.verb.infinitive,
            verb_translation=schedule.verb.english_translation,
            tense="present_subjunctive",  # Default, can be customized
            person=None,  # Will be determined during practice
            days_overdue=days_overdue,
            difficulty_level=difficulty_level,
            easiness_factor=schedule.easiness_factor,
            next_review_date=schedule.next_review_date,
            review_count=schedule.review_count,
            success_rate=success_rate
        )
        items.append(item)

        if len(items) >= limit:
            break

    # Get next upcoming review date (for items not yet due)
    next_review_query = db.query(ReviewSchedule).filter(
        ReviewSchedule.user_id == user_id_int,
        ReviewSchedule.next_review_date > now
    ).order_by(ReviewSchedule.next_review_date.asc()).first()

    next_review_date = next_review_query.next_review_date if next_review_query else None

    logger.info(f"User {user_id_int} has {len(items)} items due for review")

    return DueReviewResponse(
        items=items,
        total_due=len(items),
        next_review_date=next_review_date
    )


@router.get("/review/stats", response_model=ReviewStatsResponse)
async def get_review_stats(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: Session = Depends(get_db_session)
):
    """
    Get review statistics including:
    - Count of due cards
    - Distribution by difficulty level
    - Average retention rate
    - Review activity metrics
    """
    from models.progress import ReviewSchedule, Session as PracticeSession
    from datetime import timedelta

    # Parse user ID
    try:
        user_id_int = parse_user_id(current_user["sub"])
    except (ValueError, IndexError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    # Get all review schedules for user
    all_schedules = db.query(ReviewSchedule).filter(
        ReviewSchedule.user_id == user_id_int
    ).all()

    # Count due items
    total_due = 0
    due_by_difficulty = {
        "new": 0,
        "learning": 0,
        "reviewing": 0,
        "mastered": 0
    }

    total_correct = 0
    total_attempts = 0
    total_reviewed = 0

    for schedule in all_schedules:
        # Count reviewed items
        if schedule.review_count > 0:
            total_reviewed += 1

        # Accumulate performance metrics
        total_correct += schedule.total_correct
        total_attempts += schedule.total_attempts

        # Check if due
        if schedule.next_review_date <= now:
            total_due += 1

            # Categorize by difficulty
            if schedule.review_count == 0:
                due_by_difficulty["new"] += 1
            elif schedule.easiness_factor < 2.0:
                due_by_difficulty["learning"] += 1
            elif schedule.easiness_factor < 2.5:
                due_by_difficulty["reviewing"] += 1
            else:
                due_by_difficulty["mastered"] += 1

    # Calculate average retention rate
    average_retention = 0.0
    if total_attempts > 0:
        average_retention = (total_correct / total_attempts) * 100

    # Count reviews done today
    reviews_today = db.query(PracticeSession).filter(
        PracticeSession.user_id == user_id_int,
        PracticeSession.session_type == "review",
        PracticeSession.started_at >= today_start
    ).count()

    # Calculate streak days (simplified - count consecutive days with reviews)
    streak_days = 0
    check_date = today_start
    for _ in range(365):  # Check up to a year back
        day_sessions = db.query(PracticeSession).filter(
            PracticeSession.user_id == user_id_int,
            PracticeSession.started_at >= check_date,
            PracticeSession.started_at < check_date + timedelta(days=1),
            PracticeSession.is_completed == True
        ).count()

        if day_sessions > 0:
            streak_days += 1
            check_date -= timedelta(days=1)
        else:
            break

    logger.info(f"Review stats for user {user_id_int}: {total_due} due, {average_retention:.1f}% retention")

    return ReviewStatsResponse(
        total_due=total_due,
        due_by_difficulty=due_by_difficulty,
        average_retention=round(average_retention, 2),
        total_reviewed=total_reviewed,
        reviews_today=reviews_today,
        streak_days=streak_days
    )

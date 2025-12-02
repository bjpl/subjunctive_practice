"""
Progress tracking routes: user progress, statistics, analytics.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, status, Depends
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import logging

from core.security import get_current_active_user
from core.database import get_db_session
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from models.progress import Attempt, Session as PracticeSession
from models.user import UserProfile
from services.gamification import calculate_level_info
from utils.user_utils import parse_user_id, UserIdError

# Configure logging
logger = logging.getLogger(__name__)

# These schemas need to be properly defined - temporary inline versions
class ProgressResponse(BaseModel):
    """Schema for user progress data."""
    user_id: str
    total_exercises: int = 0
    correct_answers: int = 0
    incorrect_answers: int = 0
    accuracy_rate: float = Field(..., ge=0.0, le=100.0)
    current_streak: int = 0
    best_streak: int = 0
    last_practice: Optional[datetime] = None
    level: int = Field(..., ge=1, le=10)
    experience_points: int = 0

class StatisticsResponse(BaseModel):
    """Schema for detailed user statistics."""
    user_id: str
    overall_stats: Dict[str, Any]
    by_type: Dict[str, Dict[str, Any]]  # Stats by subjunctive type
    by_difficulty: Dict[int, Dict[str, Any]]  # Stats by difficulty level
    recent_performance: List[Dict[str, Any]]  # Last 10 exercises
    learning_insights: List[str]  # AI-generated insights
    practice_calendar: List[str]  # Dates of practice


router = APIRouter(prefix="/progress", tags=["Progress & Statistics"])


def load_user_attempts_from_db(db: Session, user_id: str) -> List[Dict[str, Any]]:
    """
    Load user's exercise attempts from database.

    Args:
        db: Database session
        user_id: User ID (e.g., "user_7" or "7")

    Returns:
        List of attempt dictionaries
    """
    try:
        user_id_int = parse_user_id(user_id)
    except UserIdError as e:
        logger.warning(f"Invalid user_id for attempts query: {user_id} - {e}")
        return []

    attempts = db.query(Attempt).filter(Attempt.user_id == user_id_int).all()
    logger.info(f"Loaded {len(attempts)} attempts for user {user_id} from database")

    return [
        {
            "exercise_id": str(a.exercise_id),
            "is_correct": a.is_correct,
            "score": 100 if a.is_correct else 0,
            "timestamp": a.created_at.isoformat(),
            "user_answer": a.user_answer
        }
        for a in attempts
    ]


def load_streak_data_from_db(db: Session, user_id: str) -> Dict[str, Any]:
    """
    Load user's streak data from UserProfile in database.

    Args:
        db: Database session
        user_id: User ID (e.g., "user_7" or "7")

    Returns:
        Dictionary with streak data
    """
    try:
        user_id_int = parse_user_id(user_id)
    except UserIdError as e:
        logger.warning(f"Invalid user_id for streak query: {user_id} - {e}")
        return {
            "current_streak": 0,
            "best_streak": 0,
            "last_practice": None,
            "total_days": 0,
            "practice_dates": []
        }

    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id_int).first()

    if not profile:
        logger.info(f"No profile found for user {user_id}, returning default streak data")
        return {
            "current_streak": 0,
            "best_streak": 0,
            "last_practice": None,
            "total_days": 0,
            "practice_dates": []
        }

    # Calculate practice dates from attempts
    attempts = db.query(Attempt).filter(Attempt.user_id == user_id_int).all()
    practice_dates = sorted(set(a.created_at.date().isoformat() for a in attempts))

    return {
        "current_streak": profile.current_streak,
        "best_streak": profile.longest_streak,
        "last_practice": profile.last_practice_date.isoformat() if profile.last_practice_date else None,
        "total_days": len(practice_dates),
        "practice_dates": practice_dates
    }


# DEPRECATED: JSON file functions kept for backward compatibility
# These should not be used in production - database functions above are preferred
def load_user_attempts(user_id: str) -> List[Dict[str, Any]]:
    """
    DEPRECATED: Load user's exercise attempts from file.
    Use load_user_attempts_from_db() instead.
    """
    logger.warning("Using deprecated JSON fallback for loading attempts - use database instead")
    attempts_file = Path(f"user_data/attempts_{user_id}.json")
    if attempts_file.exists():
        with open(attempts_file, "r") as f:
            return json.load(f)
    return []


def load_streak_data(user_id: str) -> Dict[str, Any]:
    """
    DEPRECATED: Load user's streak data from file.
    Use load_streak_data_from_db() instead.
    """
    logger.warning("Using deprecated JSON fallback for loading streak data - use database instead")
    streak_file = Path("user_data/streaks.json")
    if streak_file.exists():
        with open(streak_file, "r") as f:
            data = json.load(f)
            return data
    return {
        "current_streak": 0,
        "best_streak": 0,
        "last_practice": None,
        "total_days": 0,
        "practice_dates": []
    }


def calculate_level_and_xp(total_exercises: int, correct_answers: int) -> tuple:
    """
    DEPRECATED: Use calculate_level_info() from services.gamification instead.
    This function is kept for backwards compatibility only.

    Calculate user level and experience points.

    WARNING: This uses a legacy XP formula that does NOT match the frontend.
    The formula should be updated to use per-exercise XP tracking instead.
    """
    # Legacy XP formula - does not match frontend gamification
    # Frontend uses: per-exercise XP with difficulty, streak, and accuracy bonuses
    # Backend (this function) uses: simplified 10 per correct + 2 per attempt
    xp = (correct_answers * 10) + (total_exercises * 2)

    # Use unified gamification service for level calculation
    level_info = calculate_level_info(xp)
    level = level_info["current_level"]

    return level, xp


def update_streak_in_db(db: Session, user_id_int: int, practice_date: str) -> None:
    """
    Update streak data in database for user profile.

    Args:
        db: Database session
        user_id_int: Integer user ID
        practice_date: Practice date in ISO format (YYYY-MM-DD)
    """
    # Get or create user profile
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id_int).first()

    if not profile:
        logger.info(f"Creating new profile for user {user_id_int}")
        profile = UserProfile(user_id=user_id_int)
        db.add(profile)
        db.flush()

    # Get all practice dates from attempts
    attempts = db.query(Attempt).filter(Attempt.user_id == user_id_int).all()
    practice_dates = sorted(set(a.created_at.date() for a in attempts), reverse=True)

    if not practice_dates:
        logger.warning(f"No practice dates found for user {user_id_int}")
        return

    # Calculate current streak
    current_streak = 0
    today = datetime.utcnow().date()

    for i, date in enumerate(practice_dates):
        if i == 0:
            # First date must be today or yesterday to have an active streak
            if date == today or date == today - timedelta(days=1):
                current_streak = 1
            else:
                break
        else:
            # Check if dates are consecutive
            if date == practice_dates[i-1] - timedelta(days=1):
                current_streak += 1
            else:
                break

    # Update profile with new streak data
    profile.current_streak = current_streak
    profile.longest_streak = max(profile.longest_streak, current_streak)
    profile.last_practice_date = datetime.fromisoformat(practice_date) if isinstance(practice_date, str) else practice_date

    db.commit()
    logger.info(f"Updated streak for user {user_id_int}: current={current_streak}, best={profile.longest_streak}")


def update_streak_data(user_id: str, practice_date: str) -> Dict[str, Any]:
    """
    DEPRECATED: Update streak data with new practice session.
    Use update_streak_in_db() instead.
    """
    logger.warning("Using deprecated JSON fallback for updating streak data - use database instead")
    streak_file = Path("user_data/streaks.json")
    streak_data = load_streak_data(user_id)

    practice_dates = set(streak_data.get("practice_dates", []))
    practice_dates.add(practice_date)

    # Calculate current streak
    current_streak = 0
    best_streak = streak_data.get("best_streak", 0)
    today = datetime.utcnow().date()

    sorted_dates = sorted([datetime.fromisoformat(d).date() for d in practice_dates], reverse=True)

    for i, date in enumerate(sorted_dates):
        if i == 0:
            if date == today or date == today - timedelta(days=1):
                current_streak = 1
            else:
                break
        else:
            if date == sorted_dates[i-1] - timedelta(days=1):
                current_streak += 1
            else:
                break

    best_streak = max(best_streak, current_streak)

    updated_data = {
        "current_streak": current_streak,
        "best_streak": best_streak,
        "last_practice": practice_date,
        "total_days": len(practice_dates),
        "practice_dates": sorted(list(practice_dates))
    }

    # Save updated data
    with open(streak_file, "w") as f:
        json.dump(updated_data, f, indent=2)

    return updated_data


@router.get("", response_model=ProgressResponse)
async def get_user_progress(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: Session = Depends(get_db_session)
):
    """
    Get current user's learning progress.

    Returns:
    - Total exercises completed
    - Correct/incorrect answer counts
    - Accuracy rate
    - Current and best streak
    - Level and experience points

    Requires authentication.
    """
    user_id = current_user["sub"]

    # Load data from database
    attempts = load_user_attempts_from_db(db, user_id)
    streak_data = load_streak_data_from_db(db, user_id)

    total_exercises = len(attempts)
    correct_answers = sum(1 for a in attempts if a.get("is_correct", False))
    incorrect_answers = total_exercises - correct_answers

    accuracy_rate = (correct_answers / total_exercises * 100) if total_exercises > 0 else 0.0

    level, xp = calculate_level_and_xp(total_exercises, correct_answers)

    # Update streak in database if practiced today
    today = datetime.utcnow().date().isoformat()
    if attempts and attempts[-1].get("timestamp", "").startswith(today[:10]):
        try:
            user_id_int = parse_user_id(user_id)
            update_streak_in_db(db, user_id_int, today)
            # Reload streak data after update
            streak_data = load_streak_data_from_db(db, user_id)
        except UserIdError as e:
            logger.warning(f"Failed to update streak: {e}")

    last_practice = None
    if streak_data.get("last_practice"):
        last_practice = datetime.fromisoformat(streak_data["last_practice"])

    logger.info(f"Returning progress for user {user_id}: {total_exercises} exercises, {accuracy_rate:.1f}% accuracy")

    return ProgressResponse(
        user_id=user_id,
        total_exercises=total_exercises,
        correct_answers=correct_answers,
        incorrect_answers=incorrect_answers,
        accuracy_rate=round(accuracy_rate, 2),
        current_streak=streak_data.get("current_streak", 0),
        best_streak=streak_data.get("best_streak", 0),
        last_practice=last_practice,
        level=level,
        experience_points=xp
    )


@router.get("/statistics", response_model=StatisticsResponse)
async def get_user_statistics(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: Session = Depends(get_db_session)
):
    """
    Get detailed user learning statistics and analytics.

    Returns:
    - Overall performance stats
    - Performance by subjunctive type
    - Performance by difficulty level
    - Recent exercise history
    - AI-generated learning insights
    - Practice calendar

    Requires authentication.
    """
    user_id = current_user["sub"]

    # Load data from database
    attempts = load_user_attempts_from_db(db, user_id)
    streak_data = load_streak_data_from_db(db, user_id)

    if not attempts:
        # Return empty statistics for new users
        return StatisticsResponse(
            user_id=user_id,
            overall_stats={
                "total_exercises": 0,
                "correct_answers": 0,
                "accuracy_rate": 0.0,
                "average_score": 0.0
            },
            by_type={},
            by_difficulty={},
            recent_performance=[],
            learning_insights=["Complete your first exercise to see statistics!"],
            practice_calendar=[]
        )

    # Overall statistics
    total_exercises = len(attempts)
    correct_answers = sum(1 for a in attempts if a.get("is_correct", False))
    accuracy_rate = (correct_answers / total_exercises * 100) if total_exercises > 0 else 0.0
    average_score = sum(a.get("score", 0) for a in attempts) / total_exercises if total_exercises > 0 else 0.0

    overall_stats = {
        "total_exercises": total_exercises,
        "correct_answers": correct_answers,
        "accuracy_rate": round(accuracy_rate, 2),
        "average_score": round(average_score, 2)
    }

    # Load exercise data for type analysis
    from .exercises import load_exercises_from_db
    db_exercises = load_exercises_from_db(db, limit=1000)
    exercises = {str(ex.id): {
        "id": str(ex.id),
        "type": ex.tense.value if ex.tense else "unknown",
        "difficulty": ex.difficulty.value if ex.difficulty else 1
    } for ex in db_exercises}

    # Statistics by type
    by_type = defaultdict(lambda: {"total": 0, "correct": 0, "accuracy": 0.0})
    for attempt in attempts:
        exercise = exercises.get(attempt["exercise_id"])
        if exercise:
            ex_type = exercise["type"]
            by_type[ex_type]["total"] += 1
            if attempt.get("is_correct", False):
                by_type[ex_type]["correct"] += 1

    for ex_type in by_type:
        total = by_type[ex_type]["total"]
        correct = by_type[ex_type]["correct"]
        by_type[ex_type]["accuracy"] = round((correct / total * 100), 2) if total > 0 else 0.0

    # Statistics by difficulty
    by_difficulty = defaultdict(lambda: {"total": 0, "correct": 0, "accuracy": 0.0})
    for attempt in attempts:
        exercise = exercises.get(attempt["exercise_id"])
        if exercise:
            difficulty = exercise["difficulty"]
            by_difficulty[difficulty]["total"] += 1
            if attempt.get("is_correct", False):
                by_difficulty[difficulty]["correct"] += 1

    for difficulty in by_difficulty:
        total = by_difficulty[difficulty]["total"]
        correct = by_difficulty[difficulty]["correct"]
        by_difficulty[difficulty]["accuracy"] = round((correct / total * 100), 2) if total > 0 else 0.0

    # Recent performance (last 10 exercises)
    recent_performance = []
    for attempt in attempts[-10:]:
        exercise = exercises.get(attempt["exercise_id"])
        recent_performance.append({
            "exercise_id": attempt["exercise_id"],
            "exercise_type": exercise["type"] if exercise else "unknown",
            "is_correct": attempt.get("is_correct", False),
            "score": attempt.get("score", 0),
            "timestamp": attempt.get("timestamp", "")
        })

    # Generate learning insights (AI-powered if available)
    from services.ai_service import get_ai_service
    import logging
    logger = logging.getLogger(__name__)

    ai_service = get_ai_service()
    learning_insights = []

    if ai_service.is_enabled:
        # Try AI-powered insights
        try:
            # Identify weak areas for AI analysis
            weak_areas = [
                {"area": k, "accuracy": v["accuracy"] / 100}
                for k, v in by_type.items() if v["accuracy"] < 70
            ]

            # Build user stats for AI
            ai_user_stats = {
                "total_exercises": total_exercises,
                "accuracy": accuracy_rate / 100,
                "total_study_time_minutes": 0,  # Not tracked in current implementation
                "total_sessions": len(set(a.get("session_id", 0) for a in attempts))
            }

            learning_insights = await ai_service.generate_learning_insights(
                ai_user_stats,
                weak_areas
            )
            logger.info(f"Generated AI-powered insights for user {user_id}")
        except Exception as e:
            # Fallback to local insights if AI fails
            logger.warning(f"AI insights failed, using fallback: {str(e)}")
            learning_insights = generate_learning_insights(
                overall_stats,
                dict(by_type),
                dict(by_difficulty),
                recent_performance
            )
    else:
        # Use local insights generation
        learning_insights = generate_learning_insights(
            overall_stats,
            dict(by_type),
            dict(by_difficulty),
            recent_performance
        )

    return StatisticsResponse(
        user_id=user_id,
        overall_stats=overall_stats,
        by_type=dict(by_type),
        by_difficulty={str(k): v for k, v in by_difficulty.items()},
        recent_performance=recent_performance,
        learning_insights=learning_insights,
        practice_calendar=streak_data.get("practice_dates", [])
    )


def generate_learning_insights(
    overall_stats: Dict[str, Any],
    by_type: Dict[str, Dict[str, Any]],
    by_difficulty: Dict[int, Dict[str, Any]],
    recent_performance: List[Dict[str, Any]]
) -> List[str]:
    """Generate AI-powered learning insights based on user performance."""
    insights = []

    # Overall accuracy insights
    accuracy = overall_stats["accuracy_rate"]
    if accuracy >= 90:
        insights.append("Excellent work! You're mastering the subjunctive mood.")
    elif accuracy >= 75:
        insights.append("Great progress! Keep practicing to reach mastery.")
    elif accuracy >= 60:
        insights.append("Good effort! Focus on areas where you're struggling.")
    else:
        insights.append("Keep practicing! Review grammar rules and try easier exercises.")

    # Type-specific insights
    if by_type:
        weakest_type = min(by_type.items(), key=lambda x: x[1]["accuracy"])
        strongest_type = max(by_type.items(), key=lambda x: x[1]["accuracy"])

        if weakest_type[1]["total"] >= 3:
            insights.append(
                f"Focus on '{weakest_type[0].replace('_', ' ')}' - "
                f"your accuracy is {weakest_type[1]['accuracy']:.1f}%"
            )

        if strongest_type[1]["accuracy"] >= 85 and strongest_type[1]["total"] >= 5:
            insights.append(
                f"You excel at '{strongest_type[0].replace('_', ' ')}'! "
                f"Accuracy: {strongest_type[1]['accuracy']:.1f}%"
            )

    # Difficulty insights
    if by_difficulty:
        for level, stats in by_difficulty.items():
            if stats["total"] >= 5 and stats["accuracy"] >= 85:
                insights.append(
                    f"You've mastered difficulty level {level}! "
                    f"Try challenging yourself with harder exercises."
                )

    # Recent performance trends
    if len(recent_performance) >= 5:
        recent_correct = sum(1 for p in recent_performance[-5:] if p["is_correct"])
        if recent_correct >= 4:
            insights.append("You're on a roll! Your recent performance is excellent.")
        elif recent_correct <= 1:
            insights.append("Take a break and review the grammar rules before continuing.")

    # Encourage consistency
    insights.append("Daily practice is key to mastering the subjunctive mood!")

    return insights[:5]  # Return top 5 insights


@router.post("/reset")
async def reset_user_progress(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: Session = Depends(get_db_session)
):
    """
    Reset user's progress (for testing purposes).

    WARNING: This will delete all progress data from database.
    Requires authentication.
    """
    user_id = current_user["sub"]

    try:
        user_id_int = parse_user_id(user_id)

        # Delete all attempts from database
        attempts_deleted = db.query(Attempt).filter(Attempt.user_id == user_id_int).delete()

        # Delete all sessions from database
        sessions_deleted = db.query(PracticeSession).filter(PracticeSession.user_id == user_id_int).delete()

        # Reset user profile streaks
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id_int).first()
        if profile:
            profile.current_streak = 0
            profile.longest_streak = 0
            profile.last_practice_date = None

        db.commit()

        logger.info(f"Reset progress for user {user_id}: deleted {attempts_deleted} attempts, {sessions_deleted} sessions")

        return {
            "message": "Progress reset successfully",
            "user_id": user_id,
            "attempts_deleted": attempts_deleted,
            "sessions_deleted": sessions_deleted
        }

    except UserIdError as e:
        logger.error(f"Failed to reset progress: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid user ID format: {user_id}"
        )

    except Exception as e:
        logger.error(f"Error resetting progress: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reset progress"
        )

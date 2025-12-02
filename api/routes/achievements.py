"""
Achievement routes: get achievements, check unlocks, sync progress.
Provides comprehensive gamification features including achievement tracking,
progress calculation, and automatic unlocking based on user performance.
"""

from typing import List, Dict, Any, Optional, Tuple
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
import logging

from core.security import get_current_active_user
from core.database import get_db_session
from models.progress import Achievement, UserAchievement, Attempt, Session as PracticeSession
from models.user import UserProfile
from models.exercise import Exercise
from utils.user_utils import parse_user_id, UserIdError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/achievements", tags=["Achievements"])


# ============================================================================
# Response Models
# ============================================================================

class AchievementResponse(BaseModel):
    """Response model for achievement data with user progress."""
    id: int
    name: str
    description: str
    category: str
    icon_url: Optional[str] = None
    points: int
    unlocked: bool
    unlocked_at: Optional[datetime] = None
    progress: float = Field(..., ge=0, le=100, description="Progress percentage (0-100)")
    requirement: int = Field(..., description="Target value to unlock achievement")
    current_value: int = Field(..., description="User's current progress value")

    class Config:
        from_attributes = True


class NewlyUnlockedResponse(BaseModel):
    """Response for newly unlocked achievements."""
    achievements: List[AchievementResponse]
    total_points: int
    message: str


class UserStatsResponse(BaseModel):
    """User statistics relevant for achievements."""
    current_streak: int
    total_exercises: int
    correct_exercises: int
    consecutive_correct: int
    total_sessions: int
    perfect_sessions: int
    category_accuracy: Dict[str, float]


# ============================================================================
# Main Endpoints
# ============================================================================

@router.get("", response_model=List[AchievementResponse])
async def get_user_achievements(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: Session = Depends(get_db_session)
):
    """
    Get all achievements with user's progress and unlock status.

    Returns comprehensive achievement data including:
    - Locked and unlocked achievements
    - Progress towards each achievement
    - Current value and requirement for each achievement

    **Authentication required**
    """
    try:
        user_id = parse_user_id(current_user["sub"])
    except UserIdError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    # Get all achievements
    achievements = db.query(Achievement).all()

    if not achievements:
        logger.warning("No achievements found in database. Database may need seeding.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No achievements available. Please contact administrator."
        )

    # Get user's unlocked achievements
    user_achievements = db.query(UserAchievement).filter(
        UserAchievement.user_id == user_id
    ).all()
    unlocked_ids = {ua.achievement_id: ua for ua in user_achievements}

    # Get user stats for progress calculation
    stats = get_user_stats_for_achievements(db, user_id)

    result = []
    for ach in achievements:
        unlocked = ach.id in unlocked_ids
        ua = unlocked_ids.get(ach.id)

        current_value, requirement = calculate_achievement_progress(ach, stats)
        progress = min(100.0, (current_value / requirement * 100)) if requirement > 0 else 0.0

        result.append(AchievementResponse(
            id=ach.id,
            name=ach.name,
            description=ach.description,
            category=ach.category,
            icon_url=ach.icon_url,
            points=ach.points,
            unlocked=unlocked,
            unlocked_at=ua.unlocked_at if ua else None,
            progress=round(progress, 2),
            requirement=requirement,
            current_value=current_value
        ))

    logger.info(f"Returning {len(result)} achievements for user {user_id}")
    return result


@router.post("/check", response_model=NewlyUnlockedResponse)
async def check_new_achievements(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: Session = Depends(get_db_session)
):
    """
    Check for newly unlocked achievements based on current user progress.

    Should be called after exercises/sessions to detect new unlocks.
    Returns only newly unlocked achievements (not previously unlocked ones).

    **Authentication required**
    """
    try:
        user_id = parse_user_id(current_user["sub"])
    except UserIdError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )

    newly_unlocked = check_and_unlock_achievements(db, user_id)

    total_points = sum(ach.points for ach in newly_unlocked)

    # Convert to response models
    achievements_response = []
    stats = get_user_stats_for_achievements(db, user_id)

    for ach in newly_unlocked:
        current_value, requirement = calculate_achievement_progress(ach, stats)
        achievements_response.append(AchievementResponse(
            id=ach.id,
            name=ach.name,
            description=ach.description,
            category=ach.category,
            icon_url=ach.icon_url,
            points=ach.points,
            unlocked=True,
            unlocked_at=datetime.utcnow(),
            progress=100.0,
            requirement=requirement,
            current_value=current_value
        ))

    message = f"Unlocked {len(newly_unlocked)} new achievement(s)!" if newly_unlocked else "No new achievements unlocked"

    logger.info(f"User {user_id} unlocked {len(newly_unlocked)} achievements worth {total_points} points")

    return NewlyUnlockedResponse(
        achievements=achievements_response,
        total_points=total_points,
        message=message
    )


@router.get("/stats", response_model=UserStatsResponse)
async def get_achievement_stats(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: Session = Depends(get_db_session)
):
    """
    Get user statistics relevant for achievement calculation.

    Returns detailed stats used in achievement progress tracking:
    - Streak information
    - Exercise counts and accuracy
    - Session statistics
    - Category-specific accuracy

    **Authentication required**
    """
    try:
        user_id = parse_user_id(current_user["sub"])
    except UserIdError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )
    stats = get_user_stats_for_achievements(db, user_id)

    return UserStatsResponse(**stats)


# ============================================================================
# Helper Functions
# ============================================================================

def get_user_stats_for_achievements(db: Session, user_id: int) -> Dict[str, Any]:
    """
    Calculate comprehensive user statistics for achievement evaluation.

    Args:
        db: Database session
        user_id: User ID

    Returns:
        Dictionary containing:
        - current_streak: Current consecutive practice days
        - total_exercises: Total exercise attempts
        - correct_exercises: Total correct answers
        - consecutive_correct: Max consecutive correct answers
        - total_sessions: Total practice sessions
        - perfect_sessions: Sessions with 100% accuracy
        - category_accuracy: Accuracy per exercise category
    """
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

    # Total attempts and correct answers
    total_attempts = db.query(Attempt).filter(Attempt.user_id == user_id).count()
    correct_attempts = db.query(Attempt).filter(
        Attempt.user_id == user_id,
        Attempt.is_correct == True
    ).count()

    # Session statistics
    total_sessions = db.query(PracticeSession).filter(
        PracticeSession.user_id == user_id
    ).count()

    perfect_sessions = db.query(PracticeSession).filter(
        PracticeSession.user_id == user_id,
        PracticeSession.total_exercises > 0,
        PracticeSession.score_percentage >= 100
    ).count()

    # Calculate consecutive correct answers
    consecutive_correct = calculate_consecutive_correct(db, user_id)

    # Calculate category accuracy
    category_accuracy = calculate_category_accuracy(db, user_id)

    # Check for special achievements (time-based)
    has_night_owl = check_night_owl_session(db, user_id)
    has_early_bird = check_early_bird_session(db, user_id)
    has_speed_demon = check_speed_demon_session(db, user_id)

    return {
        "current_streak": profile.current_streak if profile else 0,
        "total_exercises": total_attempts,
        "correct_exercises": correct_attempts,
        "consecutive_correct": consecutive_correct,
        "total_sessions": total_sessions,
        "perfect_sessions": perfect_sessions,
        "category_accuracy": category_accuracy,
        "has_night_owl": has_night_owl,
        "has_early_bird": has_early_bird,
        "has_speed_demon": has_speed_demon
    }


def calculate_consecutive_correct(db: Session, user_id: int) -> int:
    """
    Calculate maximum consecutive correct answers.

    Looks at recent attempts and finds the longest streak of correct answers.

    Args:
        db: Database session
        user_id: User ID

    Returns:
        Maximum consecutive correct answer count
    """
    attempts = db.query(Attempt).filter(
        Attempt.user_id == user_id
    ).order_by(Attempt.created_at.desc()).limit(200).all()

    max_streak = current = 0
    for attempt in attempts:
        if attempt.is_correct:
            current += 1
            max_streak = max(max_streak, current)
        else:
            current = 0

    return max_streak


def calculate_category_accuracy(db: Session, user_id: int) -> Dict[str, float]:
    """
    Calculate accuracy percentage for each exercise category/tense.

    Args:
        db: Database session
        user_id: User ID

    Returns:
        Dictionary mapping category to accuracy percentage
    """
    # Query attempts with exercise information
    results = db.query(
        Exercise.tense,
        func.count(Attempt.id).label('total'),
        func.sum(func.cast(Attempt.is_correct, db.bind.dialect.NUMERIC)).label('correct')
    ).join(
        Attempt, Attempt.exercise_id == Exercise.id
    ).filter(
        Attempt.user_id == user_id
    ).group_by(
        Exercise.tense
    ).all()

    category_accuracy = {}
    for tense, total, correct in results:
        if total > 0 and tense:
            accuracy = (float(correct or 0) / float(total)) * 100
            category_accuracy[tense.value] = round(accuracy, 2)

    return category_accuracy


def check_night_owl_session(db: Session, user_id: int) -> bool:
    """Check if user has practiced between midnight and 4 AM."""
    sessions = db.query(PracticeSession).filter(
        PracticeSession.user_id == user_id
    ).all()

    for session in sessions:
        hour = session.started_at.hour
        if 0 <= hour < 4:
            return True
    return False


def check_early_bird_session(db: Session, user_id: int) -> bool:
    """Check if user has practiced between 5 AM and 7 AM."""
    sessions = db.query(PracticeSession).filter(
        PracticeSession.user_id == user_id
    ).all()

    for session in sessions:
        hour = session.started_at.hour
        if 5 <= hour < 7:
            return True
    return False


def check_speed_demon_session(db: Session, user_id: int) -> bool:
    """Check if user completed 20+ exercises in under 5 minutes."""
    sessions = db.query(PracticeSession).filter(
        PracticeSession.user_id == user_id,
        PracticeSession.total_exercises >= 20,
        PracticeSession.duration_seconds <= 300
    ).first()

    return sessions is not None


def calculate_achievement_progress(
    achievement: Achievement,
    stats: Dict[str, Any]
) -> Tuple[int, int]:
    """
    Calculate current progress value and requirement for an achievement.

    Args:
        achievement: Achievement object
        stats: User statistics dictionary

    Returns:
        Tuple of (current_value, requirement)
    """
    criteria = achievement.criteria or {}
    category = achievement.category.lower()

    # Streak achievements
    if category == "streak":
        return stats["current_streak"], criteria.get("streak_days", 3)

    # Volume achievements (total exercises)
    elif category == "volume":
        return stats["total_exercises"], criteria.get("exercises_completed", 50)

    # Accuracy achievements (consecutive correct)
    elif category == "accuracy":
        # Perfect session achievement
        if "perfect_session" in criteria or "session_accuracy" in criteria:
            return stats["perfect_sessions"], criteria.get("perfect_sessions", 1)
        # Consecutive correct achievements
        else:
            return stats["consecutive_correct"], criteria.get("correct_answers", 10)

    # Mastery achievements (category accuracy)
    elif category == "mastery":
        if "all_categories" in criteria:
            # All categories above threshold
            threshold = criteria.get("accuracy_threshold", 85)
            category_acc = stats.get("category_accuracy", {})
            if not category_acc:
                return 0, threshold
            all_above = all(acc >= threshold for acc in category_acc.values())
            return threshold if all_above else 0, threshold
        else:
            # Any category above threshold
            category_acc = stats.get("category_accuracy", {})
            max_accuracy = max(category_acc.values(), default=0)
            return int(max_accuracy), criteria.get("accuracy_threshold", 90)

    # Special achievements
    elif category == "special":
        achievement_id = criteria.get("type", "")
        if achievement_id == "night_owl":
            return 1 if stats.get("has_night_owl") else 0, 1
        elif achievement_id == "early_bird":
            return 1 if stats.get("has_early_bird") else 0, 1
        elif achievement_id == "speed_demon":
            return 1 if stats.get("has_speed_demon") else 0, 1

    # Default fallback
    return 0, 1


def check_and_unlock_achievements(db: Session, user_id: int) -> List[Achievement]:
    """
    Check if user has unlocked any new achievements and create records.

    This function:
    1. Retrieves user statistics
    2. Checks all achievements against current progress
    3. Unlocks achievements that meet criteria but aren't yet unlocked
    4. Commits new UserAchievement records to database

    Args:
        db: Database session
        user_id: User ID

    Returns:
        List of newly unlocked Achievement objects
    """
    stats = get_user_stats_for_achievements(db, user_id)
    achievements = db.query(Achievement).all()

    # Get already unlocked achievement IDs
    unlocked_ids = set(
        ua.achievement_id for ua in
        db.query(UserAchievement).filter(UserAchievement.user_id == user_id).all()
    )

    newly_unlocked = []
    for ach in achievements:
        if ach.id in unlocked_ids:
            continue

        current, requirement = calculate_achievement_progress(ach, stats)
        if current >= requirement:
            # Achievement unlocked!
            user_ach = UserAchievement(
                user_id=user_id,
                achievement_id=ach.id,
                unlocked_at=datetime.utcnow(),
                progress_data={
                    "current_value": current,
                    "requirement": requirement,
                    "unlocked_via": ach.category
                }
            )
            db.add(user_ach)
            newly_unlocked.append(ach)
            logger.info(f"User {user_id} unlocked achievement '{ach.name}' (ID: {ach.id})")

    if newly_unlocked:
        db.commit()

    return newly_unlocked

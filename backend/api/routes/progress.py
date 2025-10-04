"""
Progress tracking routes: user progress, statistics, analytics.
"""

from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, status, Depends
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

from core.security import get_current_active_user
from models.schemas import ProgressResponse, StatisticsResponse


router = APIRouter(prefix="/progress", tags=["Progress & Statistics"])


def load_user_attempts(user_id: str) -> List[Dict[str, Any]]:
    """Load user's exercise attempts from file."""
    attempts_file = Path(f"user_data/attempts_{user_id}.json")
    if attempts_file.exists():
        with open(attempts_file, "r") as f:
            return json.load(f)
    return []


def load_streak_data(user_id: str) -> Dict[str, Any]:
    """Load user's streak data."""
    streak_file = Path("user_data/streaks.json")
    if streak_file.exists():
        with open(streak_file, "r") as f:
            data = json.load(f)
            # In production, filter by user_id
            return data
    return {
        "current_streak": 0,
        "best_streak": 0,
        "last_practice": None,
        "total_days": 0,
        "practice_dates": []
    }


def calculate_level_and_xp(total_exercises: int, correct_answers: int) -> tuple:
    """Calculate user level and experience points."""
    # XP formula: 10 points per correct answer, 2 per attempt
    xp = (correct_answers * 10) + (total_exercises * 2)

    # Level formula: Level = floor(sqrt(xp / 100)) + 1
    level = min(10, int((xp / 100) ** 0.5) + 1)

    return level, xp


def update_streak_data(user_id: str, practice_date: str) -> Dict[str, Any]:
    """Update streak data with new practice session."""
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
    current_user: Dict[str, Any] = Depends(get_current_active_user)
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
    attempts = load_user_attempts(user_id)
    streak_data = load_streak_data(user_id)

    total_exercises = len(attempts)
    correct_answers = sum(1 for a in attempts if a.get("is_correct", False))
    incorrect_answers = total_exercises - correct_answers

    accuracy_rate = (correct_answers / total_exercises * 100) if total_exercises > 0 else 0.0

    level, xp = calculate_level_and_xp(total_exercises, correct_answers)

    # Update streak if practiced today
    today = datetime.utcnow().date().isoformat()
    if attempts and attempts[-1].get("timestamp", "").startswith(today[:10]):
        streak_data = update_streak_data(user_id, today)

    last_practice = None
    if streak_data.get("last_practice"):
        last_practice = datetime.fromisoformat(streak_data["last_practice"])

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
    current_user: Dict[str, Any] = Depends(get_current_active_user)
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
    attempts = load_user_attempts(user_id)
    streak_data = load_streak_data(user_id)

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
    from .exercises import load_exercises
    exercises = {ex["id"]: ex for ex in load_exercises()}

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

    # Generate learning insights
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
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """
    Reset user's progress (for testing purposes).

    WARNING: This will delete all progress data.
    Requires authentication.
    """
    user_id = current_user["sub"]

    # Delete attempts file
    attempts_file = Path(f"user_data/attempts_{user_id}.json")
    if attempts_file.exists():
        attempts_file.unlink()

    return {
        "message": "Progress reset successfully",
        "user_id": user_id
    }

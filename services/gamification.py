"""
Gamification service - XP and level calculations.
Must match frontend/lib/gamification.ts exactly.
"""

from typing import Dict
from enum import IntEnum


class Difficulty(IntEnum):
    """Difficulty levels for exercises."""
    EASY = 1
    MEDIUM = 2
    HARD = 3
    EXPERT = 4


# Base XP by difficulty (matches frontend)
BASE_XP = {
    Difficulty.EASY: 10,
    Difficulty.MEDIUM: 20,
    Difficulty.HARD: 30,
    Difficulty.EXPERT: 40,
}


def calculate_exercise_xp(
    is_correct: bool,
    difficulty: int = 2,
    streak: int = 0
) -> int:
    """
    Calculate XP earned for a single exercise.
    Must match frontend calculateExerciseXP().

    Args:
        is_correct: Whether the answer was correct
        difficulty: Difficulty level (1=easy, 2=medium, 3=hard, 4=expert)
        streak: Current streak count

    Returns:
        XP earned (integer)
    """
    base_xp = BASE_XP.get(difficulty, 20)
    xp = float(base_xp)

    if is_correct:
        xp *= 1.5  # Bonus for correct answer

    # Streak bonus (up to 2x)
    streak_multiplier = min(1 + streak * 0.1, 2.0)
    xp *= streak_multiplier

    return round(xp)


def calculate_session_xp(
    exercise_count: int,
    correct_count: int,
    session_time_seconds: int,
    streak: int = 0
) -> int:
    """
    Calculate XP earned for completing a session.
    Must match frontend calculateSessionXP().

    Args:
        exercise_count: Number of exercises completed
        correct_count: Number of correct answers
        session_time_seconds: Total session time in seconds
        streak: Current streak count

    Returns:
        XP earned (integer)
    """
    # Base XP for participation
    xp = 50

    # XP per exercise
    xp += exercise_count * 15

    # Accuracy bonus
    accuracy = correct_count / exercise_count if exercise_count > 0 else 0
    if accuracy >= 0.9:
        xp += 100
    elif accuracy >= 0.75:
        xp += 50
    elif accuracy >= 0.5:
        xp += 25

    # Time-based bonus (completing exercises efficiently)
    avg_time = session_time_seconds / exercise_count if exercise_count > 0 else 999
    if avg_time < 30:
        xp += 30  # Fast learner bonus

    # Streak bonus
    xp += min(streak * 10, 100)

    return round(xp)


def get_xp_for_level(level: int) -> int:
    """
    Calculate XP required to reach a level (cumulative).
    XP required for each level increases exponentially.
    Level 1: 0-100, Level 2: 100-300, Level 3: 300-600, etc.

    Args:
        level: The level number

    Returns:
        XP required for that level
    """
    return level * 100 + (level - 1) ** 2 * 50


def calculate_level_info(total_xp: int) -> Dict:
    """
    Calculate level from total XP.
    Must match frontend calculateLevel().

    Args:
        total_xp: Total XP earned by user

    Returns:
        Dictionary with level info:
        - current_level: Current level number
        - current_xp: XP earned toward next level
        - xp_for_next_level: XP needed for next level
        - total_xp: Total XP earned
        - progress_to_next_level: Progress percentage (0-100)
    """
    current_level = 1
    xp_for_current_level = 0
    xp_for_next_level = get_xp_for_level(1)

    # Find the current level
    while total_xp >= xp_for_next_level:
        current_level += 1
        xp_for_current_level = xp_for_next_level
        xp_for_next_level = xp_for_current_level + get_xp_for_level(current_level)

    # Calculate progress within current level
    current_xp = total_xp - xp_for_current_level
    xp_needed = xp_for_next_level - xp_for_current_level
    progress = round((current_xp / xp_needed) * 100) if xp_needed > 0 else 100

    return {
        "current_level": current_level,
        "current_xp": current_xp,
        "xp_for_next_level": xp_needed,
        "total_xp": total_xp,
        "progress_to_next_level": progress,
    }


def validate_level_calculation():
    """
    Validate that level calculations match expected values.
    Useful for testing consistency with frontend.

    Returns:
        Dictionary of test cases with expected results
    """
    test_cases = {
        0: {"level": 1, "progress": 0},
        50: {"level": 1, "progress": 50},
        100: {"level": 2, "progress": 0},
        300: {"level": 3, "progress": 0},
        600: {"level": 4, "progress": 0},
        1000: {"level": 5, "progress": 0},
    }

    results = {}
    for xp, expected in test_cases.items():
        info = calculate_level_info(xp)
        results[xp] = {
            "actual_level": info["current_level"],
            "expected_level": expected["level"],
            "match": info["current_level"] == expected["level"],
            "actual_progress": info["progress_to_next_level"],
            "expected_progress": expected["progress"],
        }

    return results

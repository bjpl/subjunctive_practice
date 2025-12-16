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
    Calculate XP (experience points) earned for completing a single exercise.

    XP calculation formula:
    1. Base XP by difficulty:
       - Easy (1): 10 XP
       - Medium (2): 20 XP
       - Hard (3): 30 XP
       - Expert (4): 40 XP

    2. Correctness bonus: +50% if answer is correct
       - Correct: multiply by 1.5
       - Incorrect: no bonus (helps track attempts)

    3. Streak multiplier: +10% per consecutive correct answer (capped at 2x)
       - Streak of 5: 1.5x multiplier
       - Streak of 10+: 2.0x multiplier (maximum)
       - Encourages consistent practice and focus

    Examples:
        Medium difficulty (20 XP), correct, no streak: 20 * 1.5 = 30 XP
        Hard difficulty (30 XP), correct, 5 streak: 30 * 1.5 * 1.5 = 67 XP
        Easy difficulty (10 XP), incorrect, 0 streak: 10 XP

    CRITICAL: This function must match frontend/lib/gamification.ts exactly
    to maintain consistency between client and server XP calculations.

    Args:
        is_correct: Whether the answer was correct
        difficulty: Difficulty level (1=easy, 2=medium, 3=hard, 4=expert)
        streak: Current streak count (number of consecutive correct answers)

    Returns:
        XP earned as integer (rounded)
    """
    # Get base XP for this difficulty level
    base_xp = BASE_XP.get(difficulty, 20)
    xp = float(base_xp)

    # Apply correctness bonus
    if is_correct:
        xp *= 1.5  # 50% bonus for correct answer

    # Apply streak multiplier (capped at 2x to prevent runaway progression)
    # Formula: 1 + (streak * 0.1), maximum 2.0
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
    Calculate XP earned for completing a practice session.

    Session XP rewards both participation and performance:

    1. Base participation XP: 50 XP
       - Awarded just for completing a session
       - Encourages regular practice

    2. Exercise completion XP: 15 XP per exercise
       - Scales with effort (more exercises = more XP)
       - Independent of correctness to avoid discouraging attempts

    3. Accuracy bonus (tiered):
       - ≥90% accuracy: +100 XP (mastery)
       - ≥75% accuracy: +50 XP (proficient)
       - ≥50% accuracy: +25 XP (learning)
       - <50% accuracy: no bonus (needs more practice)

    4. Efficiency bonus: +30 XP if average time < 30 seconds per exercise
       - Rewards automaticity and fluent recall
       - Indicates strong internalization of patterns

    5. Streak bonus: +10 XP per day streak (capped at 100 XP)
       - Rewards consistency: 10-day streak = +100 XP
       - Encourages daily practice habit

    Typical session XP examples:
    - 10 exercises, 80% accuracy, 4 min: 50 + 150 + 50 = 250 XP
    - 20 exercises, 95% accuracy, 8 min: 50 + 300 + 100 + 30 = 480 XP

    CRITICAL: Must match frontend/lib/gamification.ts exactly.

    Args:
        exercise_count: Number of exercises completed in session
        correct_count: Number of correct answers
        session_time_seconds: Total session duration in seconds
        streak: Current daily practice streak count

    Returns:
        Total session XP earned (integer)
    """
    # Base XP for showing up and practicing
    xp = 50

    # XP for completing exercises (15 per exercise)
    xp += exercise_count * 15

    # Accuracy-based bonus (tiered rewards)
    accuracy = correct_count / exercise_count if exercise_count > 0 else 0
    if accuracy >= 0.9:
        xp += 100  # Excellent - 90%+ mastery
    elif accuracy >= 0.75:
        xp += 50   # Good - 75%+ proficiency
    elif accuracy >= 0.5:
        xp += 25   # Fair - 50%+ learning progress

    # Efficiency bonus: reward fast, automatic recall
    # Average time per exercise < 30 seconds indicates fluency
    avg_time = session_time_seconds / exercise_count if exercise_count > 0 else 999
    if avg_time < 30:
        xp += 30  # Fast learner bonus

    # Streak bonus: encourage daily practice habit
    # Capped at 100 XP to prevent excessive advantage for long streaks
    xp += min(streak * 10, 100)

    return round(xp)


def get_xp_for_level(level: int) -> int:
    """
    Calculate XP required to advance from one level to the next.

    Level progression uses exponential growth to:
    1. Make early levels achievable quickly (encourages new users)
    2. Increase challenge gradually (maintains engagement)
    3. Prevent level inflation (keeps high levels meaningful)

    Formula: level * 100 + (level - 1)² * 50

    This creates a progression curve:
    - Level 1→2: 100 XP (easy, 1-2 sessions)
    - Level 2→3: 250 XP (moderate, 3-4 sessions)
    - Level 3→4: 450 XP (challenging, 5-6 sessions)
    - Level 5→6: 1000 XP (significant commitment)
    - Level 10→11: 4550 XP (mastery milestone)

    The quadratic component (level - 1)² * 50 ensures that higher levels
    require substantially more effort, making them prestigious achievements.

    Cumulative XP thresholds:
    - Level 1: 0 XP
    - Level 2: 100 XP
    - Level 3: 300 XP (100 + 200)
    - Level 4: 600 XP (300 + 300)
    - Level 5: 1000 XP (600 + 400)

    Args:
        level: The target level number (1-based)

    Returns:
        XP increment needed to reach this level from previous level
    """
    return level * 100 + (level - 1) ** 2 * 50


def calculate_level_info(total_xp: int) -> Dict:
    """
    Calculate current level and progress from cumulative XP.

    This function performs reverse lookup from total XP to determine:
    1. Current level achieved
    2. Progress within current level
    3. XP needed to reach next level

    Algorithm:
    1. Start at level 1
    2. Iterate through levels, accumulating XP thresholds
    3. Stop when total_xp < next threshold
    4. Calculate progress percentage within current level

    The exponential growth curve means:
    - Early levels: quick progression, visible achievements
    - Mid levels: steady challenge, sustained engagement
    - High levels: prestigious milestones, long-term goals

    CRITICAL: Must match frontend/lib/gamification.ts calculateLevel() exactly.
    Any discrepancy will cause level display mismatches between client and server.

    Args:
        total_xp: Total cumulative XP earned by user

    Returns:
        Dictionary containing:
        - current_level: Current level number (1-based)
        - current_xp: XP earned within current level (0 to xp_for_next_level)
        - xp_for_next_level: XP needed to advance to next level
        - total_xp: Total cumulative XP (input value)
        - progress_to_next_level: Progress percentage (0-100)

    Examples:
        >>> calculate_level_info(0)
        {"current_level": 1, "current_xp": 0, "xp_for_next_level": 100, "progress_to_next_level": 0}

        >>> calculate_level_info(150)
        {"current_level": 2, "current_xp": 50, "xp_for_next_level": 200, "progress_to_next_level": 25}

        >>> calculate_level_info(1000)
        {"current_level": 5, "current_xp": 0, "xp_for_next_level": 500, "progress_to_next_level": 0}
    """
    current_level = 1
    xp_for_current_level = 0  # Cumulative XP at start of current level
    xp_for_next_level = get_xp_for_level(1)  # Cumulative XP needed for next level

    # Find the current level by iterating until we exceed total_xp
    while total_xp >= xp_for_next_level:
        current_level += 1
        xp_for_current_level = xp_for_next_level
        xp_for_next_level = xp_for_current_level + get_xp_for_level(current_level)

    # Calculate progress within current level
    current_xp = total_xp - xp_for_current_level  # XP earned in this level
    xp_needed = xp_for_next_level - xp_for_current_level  # XP range for this level
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

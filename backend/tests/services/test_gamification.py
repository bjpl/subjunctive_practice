"""
Tests for gamification service.
Ensures backend calculations match frontend/lib/gamification.ts exactly.
"""

import pytest
from services.gamification import (
    calculate_exercise_xp,
    calculate_session_xp,
    calculate_level_info,
    get_xp_for_level,
    Difficulty,
)


class TestExerciseXP:
    """Test exercise XP calculations match frontend."""

    def test_basic_xp_easy(self):
        """Easy exercise, correct answer, no streak."""
        xp = calculate_exercise_xp(is_correct=True, difficulty=Difficulty.EASY, streak=0)
        assert xp == 15  # 10 * 1.5 = 15

    def test_basic_xp_medium(self):
        """Medium exercise, correct answer, no streak."""
        xp = calculate_exercise_xp(is_correct=True, difficulty=Difficulty.MEDIUM, streak=0)
        assert xp == 30  # 20 * 1.5 = 30

    def test_basic_xp_hard(self):
        """Hard exercise, correct answer, no streak."""
        xp = calculate_exercise_xp(is_correct=True, difficulty=Difficulty.HARD, streak=0)
        assert xp == 45  # 30 * 1.5 = 45

    def test_incorrect_answer(self):
        """Incorrect answer gets no bonus multiplier."""
        xp = calculate_exercise_xp(is_correct=False, difficulty=Difficulty.MEDIUM, streak=0)
        assert xp == 20  # 20 * 1.0 = 20

    def test_streak_bonus(self):
        """Streak provides up to 2x multiplier."""
        # 5-day streak = 1.5x
        xp = calculate_exercise_xp(is_correct=True, difficulty=Difficulty.MEDIUM, streak=5)
        assert xp == 45  # 20 * 1.5 * 1.5 = 45

    def test_streak_cap(self):
        """Streak bonus caps at 2x."""
        # 10-day streak = 2.0x (capped)
        xp = calculate_exercise_xp(is_correct=True, difficulty=Difficulty.MEDIUM, streak=10)
        assert xp == 60  # 20 * 1.5 * 2.0 = 60

        # 100-day streak = still 2.0x (capped)
        xp = calculate_exercise_xp(is_correct=True, difficulty=Difficulty.MEDIUM, streak=100)
        assert xp == 60  # 20 * 1.5 * 2.0 = 60

    def test_incorrect_with_streak(self):
        """Streak applies even on incorrect answers."""
        xp = calculate_exercise_xp(is_correct=False, difficulty=Difficulty.HARD, streak=5)
        assert xp == 45  # 30 * 1.0 * 1.5 = 45


class TestSessionXP:
    """Test session XP calculations match frontend."""

    def test_base_session_xp(self):
        """Base participation XP + per-exercise XP."""
        # 5 exercises, 0% accuracy (all wrong), slow
        xp = calculate_session_xp(
            exercise_count=5,
            correct_count=0,
            session_time_seconds=1000,
            streak=0
        )
        # 50 (base) + 75 (5 * 15) = 125
        assert xp == 125

    def test_accuracy_bonus_90(self):
        """90%+ accuracy bonus = 100 XP."""
        xp = calculate_session_xp(
            exercise_count=10,
            correct_count=9,
            session_time_seconds=1000,
            streak=0
        )
        # 50 (base) + 150 (10 * 15) + 100 (90% acc) = 300
        assert xp == 300

    def test_accuracy_bonus_75(self):
        """75%+ accuracy bonus = 50 XP."""
        xp = calculate_session_xp(
            exercise_count=10,
            correct_count=8,
            session_time_seconds=1000,
            streak=0
        )
        # 50 (base) + 150 (10 * 15) + 50 (80% acc) = 250
        assert xp == 250

    def test_accuracy_bonus_50(self):
        """50%+ accuracy bonus = 25 XP."""
        xp = calculate_session_xp(
            exercise_count=10,
            correct_count=5,
            session_time_seconds=1000,
            streak=0
        )
        # 50 (base) + 150 (10 * 15) + 25 (50% acc) = 225
        assert xp == 225

    def test_speed_bonus(self):
        """Fast learner bonus for <30s average."""
        # 10 exercises in 250 seconds = 25s average
        xp = calculate_session_xp(
            exercise_count=10,
            correct_count=5,
            session_time_seconds=250,
            streak=0
        )
        # 50 (base) + 150 (exercises) + 25 (50% acc) + 30 (speed) = 255
        assert xp == 255

    def test_streak_bonus(self):
        """Streak bonus up to 100 XP."""
        # 7-day streak = 70 XP
        xp = calculate_session_xp(
            exercise_count=10,
            correct_count=5,
            session_time_seconds=1000,
            streak=7
        )
        # 50 (base) + 150 (exercises) + 25 (50% acc) + 70 (streak) = 295
        assert xp == 295

    def test_streak_cap(self):
        """Streak bonus caps at 100 XP."""
        # 20-day streak should cap at 100 XP
        xp = calculate_session_xp(
            exercise_count=10,
            correct_count=5,
            session_time_seconds=1000,
            streak=20
        )
        # 50 (base) + 150 (exercises) + 25 (50% acc) + 100 (streak capped) = 325
        assert xp == 325

    def test_perfect_session(self):
        """Perfect session with all bonuses."""
        xp = calculate_session_xp(
            exercise_count=10,
            correct_count=10,
            session_time_seconds=200,  # 20s average
            streak=7
        )
        # 50 (base) + 150 (exercises) + 100 (100% acc) + 30 (speed) + 70 (streak) = 400
        assert xp == 400


class TestLevelCalculation:
    """Test level calculations match frontend."""

    def test_level_1_start(self):
        """Level 1 starts at 0 XP."""
        info = calculate_level_info(0)
        assert info["current_level"] == 1
        assert info["current_xp"] == 0
        assert info["total_xp"] == 0
        assert info["progress_to_next_level"] == 0

    def test_level_1_progress(self):
        """Progress within level 1."""
        info = calculate_level_info(50)
        assert info["current_level"] == 1
        assert info["current_xp"] == 50
        assert info["xp_for_next_level"] == 100  # 100 XP needed for L1->L2
        assert info["progress_to_next_level"] == 50

    def test_level_2_threshold(self):
        """Level 2 starts at 100 XP."""
        info = calculate_level_info(100)
        assert info["current_level"] == 2
        assert info["current_xp"] == 0
        assert info["total_xp"] == 100

    def test_level_3_threshold(self):
        """Level 3 starts at 350 XP."""
        info = calculate_level_info(350)
        assert info["current_level"] == 3
        assert info["current_xp"] == 0
        assert info["total_xp"] == 350

    def test_level_4_threshold(self):
        """Level 4 starts at 850 XP."""
        info = calculate_level_info(850)
        assert info["current_level"] == 4
        assert info["current_xp"] == 0

    def test_level_5_threshold(self):
        """Level 5 starts at 1700 XP."""
        info = calculate_level_info(1700)
        assert info["current_level"] == 5
        assert info["current_xp"] == 0

    def test_level_progression_exponential(self):
        """Verify exponential progression formula."""
        # Level 1: 0-100 (100 XP)
        assert get_xp_for_level(1) == 100

        # Level 2: 100-350 (250 XP)
        assert get_xp_for_level(2) == 250

        # Level 3: 350-850 (500 XP)
        assert get_xp_for_level(3) == 500

        # Level 4: 850-1700 (850 XP)
        assert get_xp_for_level(4) == 850

    def test_high_xp(self):
        """Test with high XP values."""
        info = calculate_level_info(10000)
        assert info["current_level"] == 8  # 10000 XP is level 8
        assert info["total_xp"] == 10000


class TestDifficultyEnum:
    """Test Difficulty enum values."""

    def test_difficulty_values(self):
        """Verify difficulty enum values."""
        assert Difficulty.EASY == 1
        assert Difficulty.MEDIUM == 2
        assert Difficulty.HARD == 3
        assert Difficulty.EXPERT == 4


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_zero_exercises(self):
        """Session with zero exercises."""
        xp = calculate_session_xp(
            exercise_count=0,
            correct_count=0,
            session_time_seconds=0,
            streak=0
        )
        # Should only get base participation XP
        assert xp == 50

    def test_negative_streak(self):
        """Negative streak creates negative multiplier (edge case)."""
        xp = calculate_exercise_xp(is_correct=True, difficulty=2, streak=-5)
        # 20 * 1.5 (correct) * 0.5 (1 + (-5)*0.1) = 15
        assert xp == 15

    def test_invalid_difficulty(self):
        """Invalid difficulty defaults to medium."""
        xp = calculate_exercise_xp(is_correct=True, difficulty=999, streak=0)
        # Should default to medium (20)
        assert xp == 30

    def test_perfect_accuracy_edge(self):
        """Perfect accuracy (100%) gets highest bonus."""
        xp = calculate_session_xp(
            exercise_count=1,
            correct_count=1,
            session_time_seconds=100,
            streak=0
        )
        # 50 (base) + 15 (1 exercise) + 100 (100% acc) = 165
        assert xp == 165


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

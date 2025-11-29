"""
Tests for achievements API endpoints.

Tests achievement retrieval, progress calculation, and automatic unlocking.
"""

import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from models.progress import Achievement, UserAchievement, Attempt, Session as PracticeSession
from models.user import User, UserProfile
from models.exercise import Exercise, SubjunctiveTense, DifficultyLevel
from api.routes.achievements import (
    get_user_stats_for_achievements,
    calculate_achievement_progress,
    calculate_consecutive_correct,
    check_and_unlock_achievements,
    parse_user_id
)


@pytest.fixture
def sample_user(db_session: Session):
    """Create a test user with profile."""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashed",
        is_active=True
    )
    db_session.add(user)
    db_session.flush()

    profile = UserProfile(
        user_id=user.id,
        current_streak=5,
        longest_streak=10,
        total_xp=500
    )
    db_session.add(profile)
    db_session.commit()

    return user


@pytest.fixture
def sample_achievements(db_session: Session):
    """Create sample achievements."""
    achievements = [
        Achievement(
            name="Getting Started",
            description="Practice for 3 days in a row",
            category="streak",
            icon_url="flame",
            points=10,
            criteria={"streak_days": 3}
        ),
        Achievement(
            name="Perfect Ten",
            description="Get 10 exercises correct in a row",
            category="accuracy",
            icon_url="target",
            points=15,
            criteria={"correct_answers": 10}
        ),
        Achievement(
            name="Dedicated Learner",
            description="Complete 50 exercises",
            category="volume",
            icon_url="book-open",
            points=20,
            criteria={"exercises_completed": 50}
        ),
    ]

    for ach in achievements:
        db_session.add(ach)

    db_session.commit()
    return achievements


@pytest.fixture
def sample_exercise(db_session: Session):
    """Create a sample exercise."""
    exercise = Exercise(
        spanish_sentence="Espero que tú _____ (hablar) español.",
        correct_answer="hables",
        tense=SubjunctiveTense.PRESENT_SUBJUNCTIVE,
        difficulty=DifficultyLevel.BEGINNER,
        explanation="Use present subjunctive after 'espero que'",
        is_active=True
    )
    db_session.add(exercise)
    db_session.commit()
    return exercise


class TestParseUserId:
    """Test user ID parsing from JWT subject."""

    def test_parse_numeric_string(self):
        """Should parse numeric string."""
        assert parse_user_id("7") == 7

    def test_parse_user_prefix(self):
        """Should parse 'user_7' format."""
        assert parse_user_id("user_7") == 7

    def test_parse_integer(self):
        """Should handle integer input."""
        assert parse_user_id(7) == 7

    def test_invalid_format(self):
        """Should raise HTTPException for invalid format."""
        with pytest.raises(Exception):
            parse_user_id("invalid")


class TestGetUserStats:
    """Test user statistics calculation."""

    def test_empty_stats(self, db_session, sample_user):
        """Should return zero stats for new user."""
        stats = get_user_stats_for_achievements(db_session, sample_user.id)

        assert stats["current_streak"] == 5  # From profile
        assert stats["total_exercises"] == 0
        assert stats["correct_exercises"] == 0
        assert stats["consecutive_correct"] == 0
        assert stats["total_sessions"] == 0
        assert stats["perfect_sessions"] == 0
        assert stats["category_accuracy"] == {}

    def test_with_attempts(self, db_session, sample_user, sample_exercise):
        """Should calculate stats correctly with attempts."""
        # Create a session
        session = PracticeSession(
            user_id=sample_user.id,
            started_at=datetime.utcnow(),
            total_exercises=5,
            correct_answers=5,
            score_percentage=100,
            is_completed=True
        )
        db_session.add(session)
        db_session.flush()

        # Create correct attempts
        for i in range(5):
            attempt = Attempt(
                session_id=session.id,
                user_id=sample_user.id,
                exercise_id=sample_exercise.id,
                user_answer="hables",
                is_correct=True
            )
            db_session.add(attempt)

        db_session.commit()

        stats = get_user_stats_for_achievements(db_session, sample_user.id)

        assert stats["total_exercises"] == 5
        assert stats["correct_exercises"] == 5
        assert stats["consecutive_correct"] == 5
        assert stats["total_sessions"] == 1
        assert stats["perfect_sessions"] == 1


class TestCalculateConsecutiveCorrect:
    """Test consecutive correct answer calculation."""

    def test_all_correct(self, db_session, sample_user, sample_exercise):
        """Should count all correct answers."""
        session = PracticeSession(
            user_id=sample_user.id,
            started_at=datetime.utcnow(),
            total_exercises=10,
            correct_answers=10,
            is_completed=True
        )
        db_session.add(session)
        db_session.flush()

        for i in range(10):
            attempt = Attempt(
                session_id=session.id,
                user_id=sample_user.id,
                exercise_id=sample_exercise.id,
                user_answer="hables",
                is_correct=True,
                created_at=datetime.utcnow() + timedelta(seconds=i)
            )
            db_session.add(attempt)

        db_session.commit()

        consecutive = calculate_consecutive_correct(db_session, sample_user.id)
        assert consecutive == 10

    def test_mixed_results(self, db_session, sample_user, sample_exercise):
        """Should find max streak in mixed results."""
        session = PracticeSession(
            user_id=sample_user.id,
            started_at=datetime.utcnow(),
            total_exercises=10,
            correct_answers=7,
            is_completed=True
        )
        db_session.add(session)
        db_session.flush()

        # Pattern: 3 correct, 1 wrong, 5 correct, 1 wrong
        pattern = [True, True, True, False, True, True, True, True, True, False]
        for i, is_correct in enumerate(pattern):
            attempt = Attempt(
                session_id=session.id,
                user_id=sample_user.id,
                exercise_id=sample_exercise.id,
                user_answer="hables" if is_correct else "wrong",
                is_correct=is_correct,
                created_at=datetime.utcnow() + timedelta(seconds=i)
            )
            db_session.add(attempt)

        db_session.commit()

        consecutive = calculate_consecutive_correct(db_session, sample_user.id)
        assert consecutive == 5  # Longest streak


class TestCalculateAchievementProgress:
    """Test achievement progress calculation."""

    def test_streak_achievement(self, sample_achievements):
        """Should calculate streak progress correctly."""
        streak_ach = sample_achievements[0]  # Getting Started (3 days)
        stats = {
            "current_streak": 5,
            "total_exercises": 0,
            "consecutive_correct": 0
        }

        current, requirement = calculate_achievement_progress(streak_ach, stats)
        assert current == 5
        assert requirement == 3

    def test_accuracy_achievement(self, sample_achievements):
        """Should calculate accuracy progress correctly."""
        accuracy_ach = sample_achievements[1]  # Perfect Ten (10 correct)
        stats = {
            "current_streak": 0,
            "total_exercises": 0,
            "consecutive_correct": 12
        }

        current, requirement = calculate_achievement_progress(accuracy_ach, stats)
        assert current == 12
        assert requirement == 10

    def test_volume_achievement(self, sample_achievements):
        """Should calculate volume progress correctly."""
        volume_ach = sample_achievements[2]  # Dedicated Learner (50 exercises)
        stats = {
            "current_streak": 0,
            "total_exercises": 30,
            "consecutive_correct": 0
        }

        current, requirement = calculate_achievement_progress(volume_ach, stats)
        assert current == 30
        assert requirement == 50


class TestCheckAndUnlockAchievements:
    """Test automatic achievement unlocking."""

    def test_unlock_streak_achievement(self, db_session, sample_user, sample_achievements):
        """Should unlock streak achievement when criteria met."""
        # User has 5-day streak, should unlock "Getting Started" (3 days)
        newly_unlocked = check_and_unlock_achievements(db_session, sample_user.id)

        assert len(newly_unlocked) == 1
        assert newly_unlocked[0].name == "Getting Started"

        # Verify database record
        user_ach = db_session.query(UserAchievement).filter(
            UserAchievement.user_id == sample_user.id,
            UserAchievement.achievement_id == newly_unlocked[0].id
        ).first()

        assert user_ach is not None
        assert user_ach.unlocked_at is not None

    def test_no_duplicate_unlocks(self, db_session, sample_user, sample_achievements):
        """Should not unlock same achievement twice."""
        # First unlock
        first_unlock = check_and_unlock_achievements(db_session, sample_user.id)
        assert len(first_unlock) >= 1

        # Second check should return empty
        second_unlock = check_and_unlock_achievements(db_session, sample_user.id)
        assert len(second_unlock) == 0

    def test_unlock_multiple_achievements(self, db_session, sample_user, sample_exercise, sample_achievements):
        """Should unlock multiple achievements at once."""
        # Create data that meets multiple criteria
        session = PracticeSession(
            user_id=sample_user.id,
            started_at=datetime.utcnow(),
            total_exercises=60,
            correct_answers=60,
            is_completed=True
        )
        db_session.add(session)
        db_session.flush()

        # Create 60 correct attempts
        for i in range(60):
            attempt = Attempt(
                session_id=session.id,
                user_id=sample_user.id,
                exercise_id=sample_exercise.id,
                user_answer="hables",
                is_correct=True,
                created_at=datetime.utcnow() + timedelta(seconds=i)
            )
            db_session.add(attempt)

        db_session.commit()

        newly_unlocked = check_and_unlock_achievements(db_session, sample_user.id)

        # Should unlock streak (5 days), volume (60 exercises), and accuracy (60 consecutive)
        assert len(newly_unlocked) >= 2
        achievement_names = [ach.name for ach in newly_unlocked]
        assert "Getting Started" in achievement_names
        assert "Dedicated Learner" in achievement_names


@pytest.fixture
def db_session():
    """Mock database session for testing."""
    from core.database import get_db
    db = next(get_db())
    yield db
    db.close()

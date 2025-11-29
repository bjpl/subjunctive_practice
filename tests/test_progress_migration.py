"""
Test progress tracking data layer migration.
Tests database functions for progress tracking.
"""

import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from backend.api.routes.progress import (
    parse_user_id,
    load_user_attempts_from_db,
    load_streak_data_from_db,
    update_streak_in_db
)
from backend.models.progress import Attempt, Session as PracticeSession
from backend.models.user import User, UserProfile


class TestUserIdParsing:
    """Test user ID parsing functionality."""

    def test_parse_user_id_with_prefix(self):
        """Test parsing user_7 format."""
        assert parse_user_id("user_7") == 7
        assert parse_user_id("user_123") == 123
        assert parse_user_id("user_1") == 1

    def test_parse_user_id_numeric(self):
        """Test parsing numeric string format."""
        assert parse_user_id("7") == 7
        assert parse_user_id("123") == 123
        assert parse_user_id("1") == 1

    def test_parse_user_id_integer(self):
        """Test parsing integer input."""
        assert parse_user_id(7) == 7
        assert parse_user_id(123) == 123

    def test_parse_user_id_invalid(self):
        """Test parsing invalid formats raises ValueError."""
        with pytest.raises(ValueError):
            parse_user_id("invalid")
        with pytest.raises(ValueError):
            parse_user_id("")
        with pytest.raises(ValueError):
            parse_user_id(None)


class TestDatabaseFunctions:
    """Test database query functions for progress tracking."""

    @pytest.fixture
    def db_session(self, db):
        """Provide clean database session."""
        return db

    @pytest.fixture
    def test_user(self, db_session):
        """Create test user."""
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password="dummy_hash"
        )
        db_session.add(user)
        db_session.commit()
        return user

    @pytest.fixture
    def test_profile(self, db_session, test_user):
        """Create test user profile."""
        profile = UserProfile(user_id=test_user.id)
        db_session.add(profile)
        db_session.commit()
        return profile

    def test_load_user_attempts_empty(self, db_session, test_user):
        """Test loading attempts when user has none."""
        attempts = load_user_attempts_from_db(db_session, f"user_{test_user.id}")
        assert attempts == []
        assert isinstance(attempts, list)

    def test_load_user_attempts_with_data(self, db_session, test_user):
        """Test loading attempts when user has attempts."""
        # Create test session
        session = PracticeSession(
            user_id=test_user.id,
            total_exercises=2,
            correct_answers=1,
            is_completed=True
        )
        db_session.add(session)
        db_session.flush()

        # Create test attempts
        attempt1 = Attempt(
            session_id=session.id,
            user_id=test_user.id,
            exercise_id=1,
            user_answer="test",
            is_correct=True
        )
        attempt2 = Attempt(
            session_id=session.id,
            user_id=test_user.id,
            exercise_id=2,
            user_answer="test2",
            is_correct=False
        )
        db_session.add_all([attempt1, attempt2])
        db_session.commit()

        # Load attempts
        attempts = load_user_attempts_from_db(db_session, f"user_{test_user.id}")

        assert len(attempts) == 2
        assert attempts[0]["exercise_id"] == "1"
        assert attempts[0]["is_correct"] is True
        assert attempts[0]["score"] == 100
        assert "timestamp" in attempts[0]

        assert attempts[1]["exercise_id"] == "2"
        assert attempts[1]["is_correct"] is False
        assert attempts[1]["score"] == 0

    def test_load_user_attempts_invalid_user(self, db_session):
        """Test loading attempts with invalid user ID."""
        attempts = load_user_attempts_from_db(db_session, "invalid_id")
        assert attempts == []

    def test_load_streak_data_no_profile(self, db_session, test_user):
        """Test loading streak when user has no profile."""
        streak_data = load_streak_data_from_db(db_session, f"user_{test_user.id}")

        assert streak_data["current_streak"] == 0
        assert streak_data["best_streak"] == 0
        assert streak_data["last_practice"] is None
        assert streak_data["total_days"] == 0
        assert streak_data["practice_dates"] == []

    def test_load_streak_data_with_profile(self, db_session, test_user, test_profile):
        """Test loading streak when user has profile."""
        # Set profile data
        test_profile.current_streak = 5
        test_profile.longest_streak = 10
        test_profile.last_practice_date = datetime.utcnow()
        db_session.commit()

        streak_data = load_streak_data_from_db(db_session, f"user_{test_user.id}")

        assert streak_data["current_streak"] == 5
        assert streak_data["best_streak"] == 10
        assert streak_data["last_practice"] is not None
        assert "practice_dates" in streak_data

    def test_update_streak_creates_profile(self, db_session, test_user):
        """Test that updating streak creates profile if none exists."""
        today = datetime.utcnow().date().isoformat()

        # Create an attempt so there's practice data
        session = PracticeSession(
            user_id=test_user.id,
            total_exercises=1,
            correct_answers=1,
            is_completed=True
        )
        db_session.add(session)
        db_session.flush()

        attempt = Attempt(
            session_id=session.id,
            user_id=test_user.id,
            exercise_id=1,
            user_answer="test",
            is_correct=True
        )
        db_session.add(attempt)
        db_session.commit()

        # Update streak
        update_streak_in_db(db_session, test_user.id, today)

        # Verify profile was created
        profile = db_session.query(UserProfile).filter(
            UserProfile.user_id == test_user.id
        ).first()

        assert profile is not None
        assert profile.current_streak > 0
        assert profile.last_practice_date is not None

    def test_update_streak_consecutive_days(self, db_session, test_user, test_profile):
        """Test streak calculation with consecutive practice days."""
        today = datetime.utcnow()
        yesterday = today - timedelta(days=1)

        # Create session for each day
        for practice_date in [yesterday, today]:
            session = PracticeSession(
                user_id=test_user.id,
                started_at=practice_date,
                total_exercises=1,
                correct_answers=1,
                is_completed=True
            )
            db_session.add(session)
            db_session.flush()

            attempt = Attempt(
                session_id=session.id,
                user_id=test_user.id,
                exercise_id=1,
                user_answer="test",
                is_correct=True,
                created_at=practice_date
            )
            db_session.add(attempt)

        db_session.commit()

        # Update streak
        update_streak_in_db(db_session, test_user.id, today.date().isoformat())

        # Verify streak
        profile = db_session.query(UserProfile).filter(
            UserProfile.user_id == test_user.id
        ).first()

        assert profile.current_streak == 2
        assert profile.longest_streak >= 2

    def test_update_streak_broken_streak(self, db_session, test_user, test_profile):
        """Test that non-consecutive days break the streak."""
        today = datetime.utcnow()
        three_days_ago = today - timedelta(days=3)

        # Create attempts with gap
        for practice_date in [three_days_ago, today]:
            session = PracticeSession(
                user_id=test_user.id,
                started_at=practice_date,
                total_exercises=1,
                correct_answers=1,
                is_completed=True
            )
            db_session.add(session)
            db_session.flush()

            attempt = Attempt(
                session_id=session.id,
                user_id=test_user.id,
                exercise_id=1,
                user_answer="test",
                is_correct=True,
                created_at=practice_date
            )
            db_session.add(attempt)

        db_session.commit()

        # Update streak
        update_streak_in_db(db_session, test_user.id, today.date().isoformat())

        # Verify streak was broken
        profile = db_session.query(UserProfile).filter(
            UserProfile.user_id == test_user.id
        ).first()

        # Should only count today (streak broken by gap)
        assert profile.current_streak == 1


class TestIntegration:
    """Integration tests for complete progress flow."""

    @pytest.fixture
    def db_session(self, db):
        """Provide clean database session."""
        return db

    @pytest.fixture
    def test_user(self, db_session):
        """Create test user."""
        user = User(
            username="integrationtest",
            email="integration@example.com",
            hashed_password="dummy_hash"
        )
        db_session.add(user)
        db_session.commit()
        return user

    def test_full_progress_flow(self, db_session, test_user):
        """Test complete flow: submit answer → update streak → query progress."""
        # Step 1: Create attempt (simulating submit answer)
        session = PracticeSession(
            user_id=test_user.id,
            total_exercises=1,
            correct_answers=1,
            is_completed=True
        )
        db_session.add(session)
        db_session.flush()

        attempt = Attempt(
            session_id=session.id,
            user_id=test_user.id,
            exercise_id=1,
            user_answer="hablar",
            is_correct=True
        )
        db_session.add(attempt)
        db_session.commit()

        # Step 2: Update streak
        today = datetime.utcnow().date().isoformat()
        update_streak_in_db(db_session, test_user.id, today)

        # Step 3: Query progress
        attempts = load_user_attempts_from_db(db_session, f"user_{test_user.id}")
        streak_data = load_streak_data_from_db(db_session, f"user_{test_user.id}")

        # Verify results
        assert len(attempts) == 1
        assert attempts[0]["is_correct"] is True
        assert streak_data["current_streak"] == 1
        assert streak_data["best_streak"] == 1
        assert len(streak_data["practice_dates"]) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

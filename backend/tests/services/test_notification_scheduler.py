"""
Integration tests for notification scheduler.
Tests scheduled jobs, reminder logic, and email coordination.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from services.notification_scheduler import NotificationScheduler, get_scheduler
from models.user import User, UserProfile, UserPreference
from models.progress import UserStatistics, Achievement, UserAchievement


@pytest.fixture
def mock_db_session():
    """Mock database session."""
    session = Mock(spec=Session)
    session.execute = Mock()
    session.get = Mock()
    session.query = Mock()
    session.close = Mock()
    return session


@pytest.fixture
def mock_email_service():
    """Mock email service."""
    service = Mock()
    service.send_streak_reminder = AsyncMock(return_value=True)
    service.send_weekly_progress_summary = AsyncMock(return_value=True)
    service.send_achievement_notification = AsyncMock(return_value=True)
    service.send_welcome_email = AsyncMock(return_value=True)
    return service


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    user = User(
        id=1,
        username="testuser",
        email="test@example.com",
        hashed_password="hashed",
        is_active=True
    )

    profile = UserProfile(
        user_id=1,
        full_name="Test User",
        current_streak=7,
        last_practice_date=datetime.now() - timedelta(days=1)
    )

    preference = UserPreference(
        user_id=1,
        email_notifications=True,
        reminder_enabled=True,
        reminder_time="19:00"
    )

    stats = UserStatistics(
        user_id=1,
        total_sessions=50,
        total_exercises_completed=500,
        total_correct_answers=425,
        overall_accuracy=85.0,
        weekly_exercises=50,
        weekly_accuracy=88.0,
        total_study_time_minutes=300,
        verbs_mastered=25,
        total_achievements=5
    )

    return user, profile, preference, stats


class TestSchedulerInitialization:
    """Test scheduler initialization and lifecycle."""

    @patch('services.notification_scheduler.get_email_service')
    def test_scheduler_initialization(self, mock_get_email):
        """Test scheduler initializes correctly."""
        scheduler = NotificationScheduler()

        assert scheduler.scheduler is not None
        assert scheduler.is_running is False
        mock_get_email.assert_called_once()

    @patch('services.notification_scheduler.get_email_service')
    def test_scheduler_start(self, mock_get_email):
        """Test starting the scheduler."""
        scheduler = NotificationScheduler()
        scheduler.start()

        assert scheduler.is_running is True
        assert len(scheduler.scheduler.get_jobs()) > 0

        scheduler.stop()

    @patch('services.notification_scheduler.get_email_service')
    def test_scheduler_stop(self, mock_get_email):
        """Test stopping the scheduler."""
        scheduler = NotificationScheduler()
        scheduler.start()
        scheduler.stop()

        assert scheduler.is_running is False

    @patch('services.notification_scheduler.get_email_service')
    def test_scheduler_start_already_running(self, mock_get_email, caplog):
        """Test starting scheduler when already running."""
        scheduler = NotificationScheduler()
        scheduler.start()
        scheduler.start()  # Try to start again

        assert "already running" in caplog.text.lower()
        scheduler.stop()


class TestStreakReminders:
    """Test streak reminder functionality."""

    @pytest.mark.asyncio
    @patch('services.notification_scheduler.get_db')
    @patch('services.notification_scheduler.get_email_service')
    async def test_check_streak_reminders(
        self,
        mock_get_email,
        mock_get_db,
        mock_db_session,
        mock_email_service,
        sample_user_data
    ):
        """Test checking and sending streak reminders."""
        user, profile, preference, stats = sample_user_data

        # Mock database query results
        mock_result = Mock()
        mock_result.all.return_value = [(user, profile, preference)]
        mock_db_session.execute.return_value = mock_result
        mock_get_db.return_value = iter([mock_db_session])
        mock_get_email.return_value = mock_email_service

        scheduler = NotificationScheduler()

        # Simulate current hour matching reminder time
        with patch('services.notification_scheduler.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime.strptime("19:00", "%H:%M")

            await scheduler._check_streak_reminders()

            mock_email_service.send_streak_reminder.assert_called_once_with(
                user_email=user.email,
                user_name=profile.full_name,
                current_streak=profile.current_streak
            )

    @pytest.mark.asyncio
    @patch('services.notification_scheduler.get_db')
    @patch('services.notification_scheduler.get_email_service')
    async def test_no_reminders_when_practiced_today(
        self,
        mock_get_email,
        mock_get_db,
        mock_db_session,
        mock_email_service,
        sample_user_data
    ):
        """Test no reminder sent if user already practiced today."""
        user, profile, preference, stats = sample_user_data

        # Set last practice to today
        profile.last_practice_date = datetime.now()

        mock_result = Mock()
        mock_result.all.return_value = [(user, profile, preference)]
        mock_db_session.execute.return_value = mock_result
        mock_get_db.return_value = iter([mock_db_session])
        mock_get_email.return_value = mock_email_service

        scheduler = NotificationScheduler()
        await scheduler._check_streak_reminders()

        # Should not send reminder
        mock_email_service.send_streak_reminder.assert_not_called()

    def test_needs_practice_reminder_logic(self, sample_user_data):
        """Test the logic for determining if reminder is needed."""
        user, profile, preference, stats = sample_user_data
        scheduler = NotificationScheduler()

        # Case 1: Never practiced before
        profile.last_practice_date = None
        assert scheduler._needs_practice_reminder(profile) is True

        # Case 2: Practiced yesterday
        profile.last_practice_date = datetime.now() - timedelta(days=1)
        assert scheduler._needs_practice_reminder(profile) is True

        # Case 3: Practiced today
        profile.last_practice_date = datetime.now()
        assert scheduler._needs_practice_reminder(profile) is False


class TestWeeklySummaries:
    """Test weekly summary functionality."""

    @pytest.mark.asyncio
    @patch('services.notification_scheduler.get_db')
    @patch('services.notification_scheduler.get_email_service')
    async def test_send_weekly_summaries(
        self,
        mock_get_email,
        mock_get_db,
        mock_db_session,
        mock_email_service,
        sample_user_data
    ):
        """Test sending weekly summaries."""
        user, profile, preference, stats = sample_user_data

        # Mock database query results
        mock_result = Mock()
        mock_result.all.return_value = [(user, profile, preference, stats)]
        mock_db_session.execute.return_value = mock_result

        # Mock achievements query
        achievements_result = Mock()
        achievements_result.all.return_value = [Mock(), Mock()]  # 2 achievements
        mock_db_session.execute.side_effect = [mock_result, achievements_result]

        mock_get_db.return_value = iter([mock_db_session])
        mock_get_email.return_value = mock_email_service

        scheduler = NotificationScheduler()
        await scheduler._send_weekly_summaries()

        # Verify email was sent
        mock_email_service.send_weekly_progress_summary.assert_called_once()

        # Verify stats content
        call_args = mock_email_service.send_weekly_progress_summary.call_args
        assert call_args[1]["user_email"] == user.email
        assert call_args[1]["user_name"] == profile.full_name
        assert call_args[1]["stats"]["total_exercises"] == 50
        assert call_args[1]["stats"]["accuracy"] == 88.0

    @pytest.mark.asyncio
    @patch('services.notification_scheduler.get_db')
    @patch('services.notification_scheduler.get_email_service')
    async def test_weekly_summary_date_calculation(
        self,
        mock_get_email,
        mock_get_db,
        mock_db_session,
        mock_email_service,
        sample_user_data
    ):
        """Test week date calculation in summaries."""
        user, profile, preference, stats = sample_user_data

        mock_result = Mock()
        mock_result.all.return_value = [(user, profile, preference, stats)]
        mock_db_session.execute.return_value = mock_result
        mock_get_db.return_value = iter([mock_db_session])
        mock_get_email.return_value = mock_email_service

        scheduler = NotificationScheduler()
        await scheduler._send_weekly_summaries()

        call_args = mock_email_service.send_weekly_progress_summary.call_args
        stats_data = call_args[1]["stats"]

        # Verify week_start and week_end are present
        assert "week_start" in stats_data
        assert "week_end" in stats_data


class TestAchievementNotifications:
    """Test achievement notification functionality."""

    @pytest.mark.asyncio
    @patch('services.notification_scheduler.get_db')
    @patch('services.notification_scheduler.get_email_service')
    async def test_send_achievement_notification(
        self,
        mock_get_email,
        mock_get_db,
        mock_db_session,
        mock_email_service
    ):
        """Test sending achievement notification."""
        user = User(
            id=1,
            username="testuser",
            email="test@example.com",
            is_active=True
        )

        profile = UserProfile(
            user_id=1,
            full_name="Test User"
        )

        preference = UserPreference(
            user_id=1,
            email_notifications=True
        )

        achievement = Achievement(
            id=1,
            name="First Steps",
            description="Complete your first exercise",
            icon_url="https://example.com/icon.png",
            points=10,
            category="milestone",
            criteria={"exercises_completed": 1}
        )

        # Mock database queries
        user_result = Mock()
        user_result.first.return_value = (user, profile, preference)
        mock_db_session.execute.return_value = user_result
        mock_db_session.get.return_value = achievement
        mock_get_db.return_value = iter([mock_db_session])
        mock_get_email.return_value = mock_email_service

        scheduler = NotificationScheduler()
        result = await scheduler.send_achievement_notification(
            user_id=1,
            achievement_id=1
        )

        assert result is True
        mock_email_service.send_achievement_notification.assert_called_once()

    @pytest.mark.asyncio
    @patch('services.notification_scheduler.get_db')
    @patch('services.notification_scheduler.get_email_service')
    async def test_achievement_notification_disabled(
        self,
        mock_get_email,
        mock_get_db,
        mock_db_session,
        mock_email_service
    ):
        """Test achievement notification respects user preferences."""
        user = User(id=1, username="testuser", email="test@example.com")
        profile = UserProfile(user_id=1, full_name="Test User")
        preference = UserPreference(user_id=1, email_notifications=False)

        user_result = Mock()
        user_result.first.return_value = (user, profile, preference)
        mock_db_session.execute.return_value = user_result
        mock_get_db.return_value = iter([mock_db_session])
        mock_get_email.return_value = mock_email_service

        scheduler = NotificationScheduler()
        result = await scheduler.send_achievement_notification(
            user_id=1,
            achievement_id=1
        )

        # Should return False because notifications are disabled
        assert result is False
        mock_email_service.send_achievement_notification.assert_not_called()


class TestWelcomeEmail:
    """Test welcome email functionality."""

    @pytest.mark.asyncio
    @patch('services.notification_scheduler.get_db')
    @patch('services.notification_scheduler.get_email_service')
    async def test_send_welcome_email(
        self,
        mock_get_email,
        mock_get_db,
        mock_db_session,
        mock_email_service
    ):
        """Test sending welcome email to new user."""
        user = User(id=1, username="newuser", email="new@example.com")
        profile = UserProfile(user_id=1, full_name="New User")

        mock_db_session.get.return_value = user
        mock_db_session.query.return_value.filter.return_value.first.return_value = profile
        mock_get_db.return_value = iter([mock_db_session])
        mock_get_email.return_value = mock_email_service

        scheduler = NotificationScheduler()
        result = await scheduler.send_welcome_email(user_id=1)

        assert result is True
        mock_email_service.send_welcome_email.assert_called_once_with(
            user_email=user.email,
            user_name=profile.full_name
        )


class TestSchedulerSingleton:
    """Test scheduler singleton pattern."""

    @patch('services.notification_scheduler.get_email_service')
    def test_get_scheduler_singleton(self, mock_get_email):
        """Test that get_scheduler returns the same instance."""
        scheduler1 = get_scheduler()
        scheduler2 = get_scheduler()

        assert scheduler1 is scheduler2

    @patch('services.notification_scheduler.get_email_service')
    def test_start_stop_scheduler_functions(self, mock_get_email):
        """Test global start and stop functions."""
        from services.notification_scheduler import start_scheduler, stop_scheduler

        start_scheduler()
        scheduler = get_scheduler()
        assert scheduler.is_running is True

        stop_scheduler()
        assert scheduler.is_running is False

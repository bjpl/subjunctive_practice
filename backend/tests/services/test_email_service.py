"""
Comprehensive tests for email service.
Tests both SendGrid and SMTP providers with retry logic.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from pathlib import Path

from services.email_service import EmailService, EmailRecipient, EmailTemplate
from core.config import Settings


@pytest.fixture
def mock_settings_smtp(monkeypatch):
    """Mock settings for SMTP provider."""
    settings = Settings(
        JWT_SECRET_KEY="test_secret",
        EMAIL_PROVIDER="smtp",
        EMAIL_FROM_ADDRESS="test@example.com",
        EMAIL_FROM_NAME="Test App",
        SMTP_HOST="smtp.test.com",
        SMTP_PORT=587,
        SMTP_USER="user@test.com",
        SMTP_PASSWORD="password123",
        FRONTEND_URL="http://localhost:3000",
        APP_NAME="Test App"
    )
    monkeypatch.setattr("services.email_service.settings", settings)
    return settings


@pytest.fixture
def mock_settings_sendgrid(monkeypatch):
    """Mock settings for SendGrid provider."""
    settings = Settings(
        JWT_SECRET_KEY="test_secret",
        EMAIL_PROVIDER="sendgrid",
        EMAIL_FROM_ADDRESS="test@example.com",
        EMAIL_FROM_NAME="Test App",
        SENDGRID_API_KEY="SG.test_api_key",
        FRONTEND_URL="http://localhost:3000",
        APP_NAME="Test App"
    )
    monkeypatch.setattr("services.email_service.settings", settings)
    return settings


@pytest.fixture
def email_recipient():
    """Sample email recipient."""
    return EmailRecipient(email="user@example.com", name="Test User")


@pytest.fixture
def email_template():
    """Sample email template."""
    return EmailTemplate(
        template_name="welcome",
        subject="Welcome to Test App",
        context={
            "user_name": "Test User",
            "app_name": "Test App",
            "year": 2025
        }
    )


class TestEmailServiceInitialization:
    """Test email service initialization with different providers."""

    def test_smtp_initialization(self, mock_settings_smtp):
        """Test SMTP provider initialization."""
        service = EmailService()
        assert service.provider == "smtp"
        assert service.from_address == "test@example.com"
        assert service.from_name == "Test App"
        assert service.max_retries == 3

    @patch('services.email_service.SendGridAPIClient')
    def test_sendgrid_initialization(self, mock_client, mock_settings_sendgrid):
        """Test SendGrid provider initialization."""
        service = EmailService()
        assert service.provider == "sendgrid"
        mock_client.assert_called_once()

    def test_template_environment_setup(self, mock_settings_smtp):
        """Test Jinja2 template environment is set up correctly."""
        service = EmailService()
        assert service.jinja_env is not None
        assert len(service.jinja_env.list_templates()) > 0


class TestEmailSending:
    """Test email sending functionality."""

    @pytest.mark.asyncio
    @patch('services.email_service.aiosmtplib.send')
    async def test_send_email_smtp_success(
        self,
        mock_smtp_send,
        mock_settings_smtp,
        email_recipient,
        email_template
    ):
        """Test successful email sending via SMTP."""
        mock_smtp_send.return_value = None

        service = EmailService()
        result = await service.send_email(email_recipient, email_template)

        assert result is True
        mock_smtp_send.assert_called_once()

    @pytest.mark.asyncio
    @patch('services.email_service.aiosmtplib.send')
    async def test_send_email_smtp_retry(
        self,
        mock_smtp_send,
        mock_settings_smtp,
        email_recipient,
        email_template
    ):
        """Test email retry logic on SMTP failure."""
        # Fail twice, succeed on third attempt
        mock_smtp_send.side_effect = [
            Exception("Connection failed"),
            Exception("Connection failed"),
            None
        ]

        service = EmailService()
        service.retry_delay = 0.1  # Speed up test
        result = await service.send_email(email_recipient, email_template)

        assert result is True
        assert mock_smtp_send.call_count == 3

    @pytest.mark.asyncio
    @patch('services.email_service.aiosmtplib.send')
    async def test_send_email_smtp_max_retries(
        self,
        mock_smtp_send,
        mock_settings_smtp,
        email_recipient,
        email_template
    ):
        """Test email fails after max retries."""
        mock_smtp_send.side_effect = Exception("Connection failed")

        service = EmailService()
        service.retry_delay = 0.1  # Speed up test
        result = await service.send_email(email_recipient, email_template)

        assert result is False
        assert mock_smtp_send.call_count == 4  # Initial + 3 retries

    @pytest.mark.asyncio
    @patch('services.email_service.SendGridAPIClient')
    async def test_send_email_sendgrid_success(
        self,
        mock_client_class,
        mock_settings_sendgrid,
        email_recipient,
        email_template
    ):
        """Test successful email sending via SendGrid."""
        mock_response = Mock()
        mock_response.status_code = 202
        mock_client = Mock()
        mock_client.send.return_value = mock_response
        mock_client_class.return_value = mock_client

        service = EmailService()
        result = await service.send_email(email_recipient, email_template)

        assert result is True
        mock_client.send.assert_called_once()


class TestHighLevelNotifications:
    """Test high-level notification methods."""

    @pytest.mark.asyncio
    @patch('services.email_service.aiosmtplib.send')
    async def test_send_streak_reminder(self, mock_smtp_send, mock_settings_smtp):
        """Test streak reminder notification."""
        mock_smtp_send.return_value = None

        service = EmailService()
        result = await service.send_streak_reminder(
            user_email="user@example.com",
            user_name="Test User",
            current_streak=7
        )

        assert result is True
        mock_smtp_send.assert_called_once()

        # Verify email content
        call_args = mock_smtp_send.call_args
        message = call_args[0][0]
        assert "7" in str(message)
        assert "streak" in str(message).lower()

    @pytest.mark.asyncio
    @patch('services.email_service.aiosmtplib.send')
    async def test_send_achievement_notification(self, mock_smtp_send, mock_settings_smtp):
        """Test achievement notification."""
        mock_smtp_send.return_value = None

        achievement = {
            "name": "First Steps",
            "description": "Complete your first exercise",
            "icon_url": "https://example.com/icon.png",
            "points": 10
        }

        service = EmailService()
        result = await service.send_achievement_notification(
            user_email="user@example.com",
            user_name="Test User",
            achievement=achievement
        )

        assert result is True
        mock_smtp_send.assert_called_once()

        # Verify email content
        call_args = mock_smtp_send.call_args
        message = call_args[0][0]
        assert "First Steps" in str(message)
        assert "10" in str(message)

    @pytest.mark.asyncio
    @patch('services.email_service.aiosmtplib.send')
    async def test_send_weekly_summary(self, mock_smtp_send, mock_settings_smtp):
        """Test weekly progress summary."""
        mock_smtp_send.return_value = None

        stats = {
            "week_start": "Dec 9",
            "week_end": "Dec 15, 2025",
            "total_exercises": 50,
            "accuracy": 85.5,
            "study_time_minutes": 120,
            "current_streak": 7,
            "verbs_mastered": 15,
            "achievements_earned": 3
        }

        service = EmailService()
        result = await service.send_weekly_progress_summary(
            user_email="user@example.com",
            user_name="Test User",
            stats=stats
        )

        assert result is True
        mock_smtp_send.assert_called_once()

        # Verify email content
        call_args = mock_smtp_send.call_args
        message = call_args[0][0]
        assert "50" in str(message)
        assert "85.5" in str(message)

    @pytest.mark.asyncio
    @patch('services.email_service.aiosmtplib.send')
    async def test_send_welcome_email(self, mock_smtp_send, mock_settings_smtp):
        """Test welcome email."""
        mock_smtp_send.return_value = None

        service = EmailService()
        result = await service.send_welcome_email(
            user_email="user@example.com",
            user_name="Test User"
        )

        assert result is True
        mock_smtp_send.assert_called_once()

        # Verify email content
        call_args = mock_smtp_send.call_args
        message = call_args[0][0]
        assert "Welcome" in str(message)

    @pytest.mark.asyncio
    @patch('services.email_service.aiosmtplib.send')
    async def test_send_password_reset(self, mock_smtp_send, mock_settings_smtp):
        """Test password reset email."""
        mock_smtp_send.return_value = None

        service = EmailService()
        result = await service.send_password_reset(
            user_email="user@example.com",
            user_name="Test User",
            reset_token="abc123xyz"
        )

        assert result is True
        mock_smtp_send.assert_called_once()

        # Verify email content
        call_args = mock_smtp_send.call_args
        message = call_args[0][0]
        assert "abc123xyz" in str(message)
        assert "reset" in str(message).lower()


class TestBulkEmails:
    """Test bulk email sending."""

    @pytest.mark.asyncio
    @patch('services.email_service.aiosmtplib.send')
    async def test_send_bulk_emails_success(self, mock_smtp_send, mock_settings_smtp):
        """Test sending bulk emails successfully."""
        mock_smtp_send.return_value = None

        recipients = [
            EmailRecipient(email=f"user{i}@example.com", name=f"User {i}")
            for i in range(5)
        ]

        template = EmailTemplate(
            template_name="welcome",
            subject="Welcome",
            context={"user_name": "User", "app_name": "Test", "year": 2025}
        )

        service = EmailService()
        results = await service.send_bulk_emails(recipients, template)

        assert results["total"] == 5
        assert results["sent"] == 5
        assert results["failed"] == 0
        assert mock_smtp_send.call_count == 5

    @pytest.mark.asyncio
    @patch('services.email_service.aiosmtplib.send')
    async def test_send_bulk_emails_partial_failure(
        self,
        mock_smtp_send,
        mock_settings_smtp
    ):
        """Test bulk emails with some failures."""
        # First 2 succeed, next 2 fail, last one succeeds
        mock_smtp_send.side_effect = [
            None,
            None,
            Exception("Failed"),
            Exception("Failed"),
            None
        ]

        recipients = [
            EmailRecipient(email=f"user{i}@example.com", name=f"User {i}")
            for i in range(5)
        ]

        template = EmailTemplate(
            template_name="welcome",
            subject="Welcome",
            context={"user_name": "User", "app_name": "Test", "year": 2025}
        )

        service = EmailService()
        service.max_retries = 0  # Disable retries for this test
        results = await service.send_bulk_emails(recipients, template)

        assert results["total"] == 5
        assert results["sent"] == 3
        assert results["failed"] == 2


class TestTemplateRendering:
    """Test email template rendering."""

    def test_render_html_template(self, mock_settings_smtp):
        """Test HTML template rendering."""
        service = EmailService()
        content = service._render_template(
            "welcome.html",
            {"user_name": "Test User", "app_name": "Test App", "year": 2025}
        )

        assert "Test User" in content
        assert "Test App" in content
        assert "2025" in content

    def test_render_text_template(self, mock_settings_smtp):
        """Test plain text template rendering."""
        service = EmailService()
        content = service._render_template(
            "welcome.txt",
            {"user_name": "Test User", "app_name": "Test App", "year": 2025}
        )

        assert "Test User" in content
        assert "Test App" in content

    def test_render_missing_template(self, mock_settings_smtp):
        """Test error handling for missing template."""
        service = EmailService()

        with pytest.raises(Exception):
            service._render_template(
                "nonexistent.html",
                {"user_name": "Test"}
            )


class TestEmailServiceSingleton:
    """Test email service singleton pattern."""

    def test_get_email_service_singleton(self, mock_settings_smtp):
        """Test that get_email_service returns the same instance."""
        from services.email_service import get_email_service

        service1 = get_email_service()
        service2 = get_email_service()

        assert service1 is service2

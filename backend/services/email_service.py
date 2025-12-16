"""
Email notification service with SendGrid and SMTP support.
Provides template-based async email sending with retry logic.
"""

from typing import Dict, Any, Optional, List
from pathlib import Path
import asyncio
import logging
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import aiosmtplib
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import BaseModel, EmailStr

from core.config import settings

logger = logging.getLogger(__name__)


class EmailRecipient(BaseModel):
    """Email recipient information."""
    email: EmailStr
    name: Optional[str] = None


class EmailTemplate(BaseModel):
    """Email template data."""
    template_name: str
    subject: str
    context: Dict[str, Any]


class EmailService:
    """
    Email notification service supporting SendGrid and SMTP.
    Features:
    - Template-based emails using Jinja2
    - Async sending with retry logic
    - Multiple provider support (SendGrid/SMTP)
    - HTML and plain text alternatives
    """

    def __init__(self):
        """Initialize email service with configuration."""
        self.provider = settings.EMAIL_PROVIDER
        self.from_address = settings.EMAIL_FROM_ADDRESS
        self.from_name = settings.EMAIL_FROM_NAME
        self.max_retries = 3
        self.retry_delay = 2  # seconds

        # Setup Jinja2 template environment
        template_dir = Path(__file__).parent.parent / "templates" / "emails"
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=select_autoescape(['html', 'xml'])
        )

        # Initialize provider-specific clients
        if self.provider == "sendgrid":
            try:
                from sendgrid import SendGridAPIClient
                from sendgrid.helpers.mail import Mail
                self.sendgrid_client = SendGridAPIClient(settings.SENDGRID_API_KEY)
                self.Mail = Mail
                logger.info("SendGrid client initialized")
            except ImportError:
                logger.error("SendGrid library not installed. Install with: pip install sendgrid")
                raise
        elif self.provider == "smtp":
            logger.info(f"SMTP client configured for {settings.SMTP_HOST}:{settings.SMTP_PORT}")
        else:
            logger.warning(f"Unknown email provider: {self.provider}")

    async def send_email(
        self,
        recipient: EmailRecipient,
        template: EmailTemplate,
        retry_count: int = 0
    ) -> bool:
        """
        Send an email using the configured provider with retry logic.

        Args:
            recipient: Email recipient information
            template: Email template data
            retry_count: Current retry attempt (internal use)

        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Render email template
            html_content = self._render_template(
                f"{template.template_name}.html",
                template.context
            )
            text_content = self._render_template(
                f"{template.template_name}.txt",
                template.context
            )

            # Send using configured provider
            if self.provider == "sendgrid":
                success = await self._send_via_sendgrid(
                    recipient=recipient,
                    subject=template.subject,
                    html_content=html_content,
                    text_content=text_content
                )
            elif self.provider == "smtp":
                success = await self._send_via_smtp(
                    recipient=recipient,
                    subject=template.subject,
                    html_content=html_content,
                    text_content=text_content
                )
            else:
                logger.error(f"Unsupported email provider: {self.provider}")
                return False

            if success:
                logger.info(f"Email sent successfully to {recipient.email}: {template.subject}")
                return True

            # Retry logic
            if retry_count < self.max_retries:
                await asyncio.sleep(self.retry_delay * (retry_count + 1))
                logger.warning(f"Retrying email send (attempt {retry_count + 1}/{self.max_retries})")
                return await self.send_email(recipient, template, retry_count + 1)

            logger.error(f"Failed to send email after {self.max_retries} attempts")
            return False

        except Exception as e:
            logger.error(f"Error sending email: {str(e)}", exc_info=True)

            # Retry on exception
            if retry_count < self.max_retries:
                await asyncio.sleep(self.retry_delay * (retry_count + 1))
                return await self.send_email(recipient, template, retry_count + 1)

            return False

    async def _send_via_sendgrid(
        self,
        recipient: EmailRecipient,
        subject: str,
        html_content: str,
        text_content: str
    ) -> bool:
        """Send email via SendGrid API."""
        try:
            message = self.Mail(
                from_email=(self.from_address, self.from_name),
                to_emails=recipient.email,
                subject=subject,
                html_content=html_content,
                plain_text_content=text_content
            )

            response = self.sendgrid_client.send(message)
            return response.status_code in [200, 201, 202]

        except Exception as e:
            logger.error(f"SendGrid error: {str(e)}", exc_info=True)
            return False

    async def _send_via_smtp(
        self,
        recipient: EmailRecipient,
        subject: str,
        html_content: str,
        text_content: str
    ) -> bool:
        """Send email via SMTP."""
        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = f"{self.from_name} <{self.from_address}>"
            message['To'] = recipient.email

            # Attach both plain text and HTML versions
            part1 = MIMEText(text_content, 'plain')
            part2 = MIMEText(html_content, 'html')
            message.attach(part1)
            message.attach(part2)

            # Send via SMTP
            await aiosmtplib.send(
                message,
                hostname=settings.SMTP_HOST,
                port=settings.SMTP_PORT,
                username=settings.SMTP_USER,
                password=settings.SMTP_PASSWORD,
                start_tls=True,
                timeout=30
            )

            return True

        except Exception as e:
            logger.error(f"SMTP error: {str(e)}", exc_info=True)
            return False

    def _render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """Render a Jinja2 template with the given context."""
        try:
            template = self.jinja_env.get_template(template_name)
            return template.render(**context)
        except Exception as e:
            logger.error(f"Template rendering error for {template_name}: {str(e)}")
            raise

    # ============================================================================
    # High-level notification methods
    # ============================================================================

    async def send_streak_reminder(
        self,
        user_email: str,
        user_name: str,
        current_streak: int
    ) -> bool:
        """
        Send streak reminder notification.

        Args:
            user_email: User's email address
            user_name: User's display name
            current_streak: Current streak count in days

        Returns:
            bool: True if sent successfully
        """
        recipient = EmailRecipient(email=user_email, name=user_name)
        template = EmailTemplate(
            template_name="streak_reminder",
            subject=f"Don't break your {current_streak}-day streak! 🔥",
            context={
                "user_name": user_name,
                "current_streak": current_streak,
                "app_name": settings.APP_NAME,
                "year": datetime.now().year
            }
        )

        return await self.send_email(recipient, template)

    async def send_achievement_notification(
        self,
        user_email: str,
        user_name: str,
        achievement: Dict[str, Any]
    ) -> bool:
        """
        Send achievement unlock notification.

        Args:
            user_email: User's email address
            user_name: User's display name
            achievement: Achievement data (name, description, icon, points)

        Returns:
            bool: True if sent successfully
        """
        recipient = EmailRecipient(email=user_email, name=user_name)
        template = EmailTemplate(
            template_name="achievement_unlocked",
            subject=f"Achievement Unlocked: {achievement['name']} 🏆",
            context={
                "user_name": user_name,
                "achievement_name": achievement["name"],
                "achievement_description": achievement["description"],
                "achievement_icon": achievement.get("icon_url", ""),
                "achievement_points": achievement.get("points", 0),
                "app_name": settings.APP_NAME,
                "year": datetime.now().year
            }
        )

        return await self.send_email(recipient, template)

    async def send_weekly_progress_summary(
        self,
        user_email: str,
        user_name: str,
        stats: Dict[str, Any]
    ) -> bool:
        """
        Send weekly progress summary.

        Args:
            user_email: User's email address
            user_name: User's display name
            stats: Weekly statistics data

        Returns:
            bool: True if sent successfully
        """
        recipient = EmailRecipient(email=user_email, name=user_name)
        template = EmailTemplate(
            template_name="weekly_summary",
            subject="Your Weekly Spanish Learning Progress 📊",
            context={
                "user_name": user_name,
                "week_start": stats.get("week_start", ""),
                "week_end": stats.get("week_end", ""),
                "total_exercises": stats.get("total_exercises", 0),
                "accuracy": stats.get("accuracy", 0),
                "study_time_minutes": stats.get("study_time_minutes", 0),
                "current_streak": stats.get("current_streak", 0),
                "verbs_mastered": stats.get("verbs_mastered", 0),
                "achievements_earned": stats.get("achievements_earned", 0),
                "app_name": settings.APP_NAME,
                "year": datetime.now().year
            }
        )

        return await self.send_email(recipient, template)

    async def send_welcome_email(
        self,
        user_email: str,
        user_name: str
    ) -> bool:
        """
        Send welcome email to new users.

        Args:
            user_email: User's email address
            user_name: User's display name

        Returns:
            bool: True if sent successfully
        """
        recipient = EmailRecipient(email=user_email, name=user_name)
        template = EmailTemplate(
            template_name="welcome",
            subject=f"Welcome to {settings.APP_NAME}! 🎉",
            context={
                "user_name": user_name,
                "app_name": settings.APP_NAME,
                "year": datetime.now().year
            }
        )

        return await self.send_email(recipient, template)

    async def send_password_reset(
        self,
        user_email: str,
        user_name: str,
        reset_token: str
    ) -> bool:
        """
        Send password reset email.

        Args:
            user_email: User's email address
            user_name: User's display name
            reset_token: Password reset token

        Returns:
            bool: True if sent successfully
        """
        # Build reset URL (adjust based on your frontend URL)
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"

        recipient = EmailRecipient(email=user_email, name=user_name)
        template = EmailTemplate(
            template_name="password_reset",
            subject="Password Reset Request 🔒",
            context={
                "user_name": user_name,
                "reset_url": reset_url,
                "reset_token": reset_token,
                "app_name": settings.APP_NAME,
                "year": datetime.now().year
            }
        )

        return await self.send_email(recipient, template)

    async def send_bulk_emails(
        self,
        recipients: List[EmailRecipient],
        template: EmailTemplate
    ) -> Dict[str, Any]:
        """
        Send emails to multiple recipients.

        Args:
            recipients: List of email recipients
            template: Email template to use

        Returns:
            Dict with success/failure counts and details
        """
        results = {
            "total": len(recipients),
            "sent": 0,
            "failed": 0,
            "errors": []
        }

        # Send emails concurrently with rate limiting
        tasks = []
        for recipient in recipients:
            tasks.append(self.send_email(recipient, template))

            # Rate limit: send in batches of 10 with delay
            if len(tasks) >= 10:
                batch_results = await asyncio.gather(*tasks, return_exceptions=True)
                for result in batch_results:
                    if isinstance(result, bool) and result:
                        results["sent"] += 1
                    else:
                        results["failed"] += 1
                        results["errors"].append(str(result))

                tasks = []
                await asyncio.sleep(1)  # 1 second delay between batches

        # Send remaining emails
        if tasks:
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in batch_results:
                if isinstance(result, bool) and result:
                    results["sent"] += 1
                else:
                    results["failed"] += 1
                    results["errors"].append(str(result))

        logger.info(f"Bulk email completed: {results['sent']}/{results['total']} sent")
        return results


# Global email service instance
_email_service: Optional[EmailService] = None


def get_email_service() -> EmailService:
    """Get or create the global email service instance."""
    global _email_service
    if _email_service is None:
        _email_service = EmailService()
    return _email_service

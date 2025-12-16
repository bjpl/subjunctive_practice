"""
Notification scheduler service using APScheduler.
Manages scheduled tasks for email notifications, reminders, and summaries.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta, time as datetime_time
import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session
from sqlalchemy import select

from core.database import get_db
from models.user import User, UserProfile, UserPreference
from models.progress import UserStatistics, UserAchievement, Achievement
from services.email_service import get_email_service

logger = logging.getLogger(__name__)


class NotificationScheduler:
    """
    Scheduled notification service for automated emails.

    Features:
    - Daily streak reminders based on user preferences
    - Weekly progress summaries
    - Achievement notifications
    - Configurable scheduling with APScheduler
    """

    def __init__(self):
        """Initialize the scheduler."""
        self.scheduler = AsyncIOScheduler()
        self.email_service = get_email_service()
        self.is_running = False

    def start(self):
        """Start the scheduler with all configured jobs."""
        if self.is_running:
            logger.warning("Scheduler is already running")
            return

        try:
            # Schedule daily streak reminders (runs hourly to check user reminder times)
            self.scheduler.add_job(
                self._check_streak_reminders,
                trigger=CronTrigger(minute=0),  # Every hour at :00
                id="streak_reminders",
                name="Check and send streak reminders",
                replace_existing=True
            )

            # Schedule weekly summaries (Sundays at 8 PM)
            self.scheduler.add_job(
                self._send_weekly_summaries,
                trigger=CronTrigger(day_of_week='sun', hour=20, minute=0),
                id="weekly_summaries",
                name="Send weekly progress summaries",
                replace_existing=True
            )

            # Schedule daily cleanup (daily at 3 AM)
            self.scheduler.add_job(
                self._cleanup_old_notifications,
                trigger=CronTrigger(hour=3, minute=0),
                id="cleanup",
                name="Clean up old notification records",
                replace_existing=True
            )

            self.scheduler.start()
            self.is_running = True
            logger.info("Notification scheduler started successfully")

        except Exception as e:
            logger.error(f"Failed to start scheduler: {str(e)}", exc_info=True)
            raise

    def stop(self):
        """Stop the scheduler."""
        if not self.is_running:
            logger.warning("Scheduler is not running")
            return

        try:
            self.scheduler.shutdown(wait=True)
            self.is_running = False
            logger.info("Notification scheduler stopped")
        except Exception as e:
            logger.error(f"Error stopping scheduler: {str(e)}", exc_info=True)

    async def _check_streak_reminders(self):
        """
        Check for users who need streak reminders and send them.
        Runs hourly and sends reminders based on user's preferred time.
        """
        logger.info("Checking for users needing streak reminders")

        try:
            # Get current hour
            current_hour = datetime.now().hour
            current_time = f"{current_hour:02d}:00"

            # Get database session
            db = next(get_db())

            try:
                # Find users with:
                # 1. Reminder enabled
                # 2. Email notifications enabled
                # 3. Reminder time matches current hour
                # 4. Haven't practiced today
                query = (
                    select(User, UserProfile, UserPreference)
                    .join(UserProfile, User.id == UserProfile.user_id)
                    .join(UserPreference, User.id == UserPreference.user_id)
                    .where(
                        User.is_active == True,
                        UserPreference.reminder_enabled == True,
                        UserPreference.email_notifications == True,
                        UserPreference.reminder_time.like(f"{current_hour:02d}:%")
                    )
                )

                results = db.execute(query).all()

                reminder_count = 0
                for user, profile, preference in results:
                    # Check if user hasn't practiced today
                    if self._needs_practice_reminder(profile):
                        success = await self.email_service.send_streak_reminder(
                            user_email=user.email,
                            user_name=profile.full_name or user.username,
                            current_streak=profile.current_streak
                        )

                        if success:
                            reminder_count += 1
                            logger.info(f"Sent streak reminder to {user.email}")

                logger.info(f"Sent {reminder_count} streak reminders")

            finally:
                db.close()

        except Exception as e:
            logger.error(f"Error checking streak reminders: {str(e)}", exc_info=True)

    async def _send_weekly_summaries(self):
        """
        Send weekly progress summaries to all active users.
        Runs on Sundays.
        """
        logger.info("Sending weekly progress summaries")

        try:
            db = next(get_db())

            try:
                # Find all active users with email notifications enabled
                query = (
                    select(User, UserProfile, UserPreference, UserStatistics)
                    .join(UserProfile, User.id == UserProfile.user_id)
                    .join(UserPreference, User.id == UserPreference.user_id)
                    .join(UserStatistics, User.id == UserStatistics.user_id)
                    .where(
                        User.is_active == True,
                        UserPreference.email_notifications == True
                    )
                )

                results = db.execute(query).all()

                summary_count = 0
                for user, profile, preference, stats in results:
                    # Calculate week dates
                    today = datetime.now()
                    week_start = (today - timedelta(days=today.weekday() + 1)).strftime("%B %d")
                    week_end = today.strftime("%B %d, %Y")

                    # Prepare stats data
                    weekly_stats = {
                        "week_start": week_start,
                        "week_end": week_end,
                        "total_exercises": stats.weekly_exercises,
                        "accuracy": round(stats.weekly_accuracy, 1),
                        "study_time_minutes": stats.total_study_time_minutes,
                        "current_streak": profile.current_streak,
                        "verbs_mastered": stats.verbs_mastered,
                        "achievements_earned": self._get_weekly_achievements_count(db, user.id)
                    }

                    success = await self.email_service.send_weekly_progress_summary(
                        user_email=user.email,
                        user_name=profile.full_name or user.username,
                        stats=weekly_stats
                    )

                    if success:
                        summary_count += 1
                        logger.info(f"Sent weekly summary to {user.email}")

                logger.info(f"Sent {summary_count} weekly summaries")

            finally:
                db.close()

        except Exception as e:
            logger.error(f"Error sending weekly summaries: {str(e)}", exc_info=True)

    async def send_achievement_notification(
        self,
        user_id: int,
        achievement_id: int
    ) -> bool:
        """
        Send achievement unlock notification immediately.
        This is called when an achievement is unlocked during gameplay.

        Args:
            user_id: User ID who unlocked the achievement
            achievement_id: Achievement ID that was unlocked

        Returns:
            bool: True if notification sent successfully
        """
        try:
            db = next(get_db())

            try:
                # Get user and achievement details
                user_query = (
                    select(User, UserProfile, UserPreference)
                    .join(UserProfile, User.id == UserProfile.user_id)
                    .join(UserPreference, User.id == UserPreference.user_id)
                    .where(User.id == user_id)
                )
                user_result = db.execute(user_query).first()

                if not user_result:
                    logger.warning(f"User {user_id} not found")
                    return False

                user, profile, preference = user_result

                # Check if email notifications are enabled
                if not preference.email_notifications:
                    logger.info(f"Email notifications disabled for user {user_id}")
                    return False

                # Get achievement details
                achievement = db.get(Achievement, achievement_id)
                if not achievement:
                    logger.warning(f"Achievement {achievement_id} not found")
                    return False

                # Send notification
                achievement_data = {
                    "name": achievement.name,
                    "description": achievement.description,
                    "icon_url": achievement.icon_url,
                    "points": achievement.points
                }

                success = await self.email_service.send_achievement_notification(
                    user_email=user.email,
                    user_name=profile.full_name or user.username,
                    achievement=achievement_data
                )

                if success:
                    logger.info(f"Sent achievement notification to user {user_id}")

                return success

            finally:
                db.close()

        except Exception as e:
            logger.error(f"Error sending achievement notification: {str(e)}", exc_info=True)
            return False

    async def send_welcome_email(self, user_id: int) -> bool:
        """
        Send welcome email to new user.

        Args:
            user_id: New user's ID

        Returns:
            bool: True if sent successfully
        """
        try:
            db = next(get_db())

            try:
                user = db.get(User, user_id)
                if not user:
                    logger.warning(f"User {user_id} not found")
                    return False

                profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

                success = await self.email_service.send_welcome_email(
                    user_email=user.email,
                    user_name=profile.full_name if profile else user.username
                )

                if success:
                    logger.info(f"Sent welcome email to user {user_id}")

                return success

            finally:
                db.close()

        except Exception as e:
            logger.error(f"Error sending welcome email: {str(e)}", exc_info=True)
            return False

    # ============================================================================
    # Helper methods
    # ============================================================================

    def _needs_practice_reminder(self, profile: UserProfile) -> bool:
        """Check if user needs a practice reminder today."""
        if not profile.last_practice_date:
            return True

        today = datetime.now().date()
        last_practice = profile.last_practice_date.date()

        # Need reminder if haven't practiced today
        return last_practice < today

    def _get_weekly_achievements_count(self, db: Session, user_id: int) -> int:
        """Get count of achievements earned in the last week."""
        try:
            week_ago = datetime.now() - timedelta(days=7)
            query = (
                select(UserAchievement)
                .where(
                    UserAchievement.user_id == user_id,
                    UserAchievement.unlocked_at >= week_ago
                )
            )
            results = db.execute(query).all()
            return len(results)
        except Exception:
            return 0

    async def _cleanup_old_notifications(self):
        """Clean up old notification records (placeholder for future implementation)."""
        logger.info("Running notification cleanup")
        # Future: Clean up any notification tracking tables
        pass


# Global scheduler instance
_scheduler: Optional[NotificationScheduler] = None


def get_scheduler() -> NotificationScheduler:
    """Get or create the global scheduler instance."""
    global _scheduler
    if _scheduler is None:
        _scheduler = NotificationScheduler()
    return _scheduler


def start_scheduler():
    """Start the global notification scheduler."""
    scheduler = get_scheduler()
    scheduler.start()


def stop_scheduler():
    """Stop the global notification scheduler."""
    scheduler = get_scheduler()
    scheduler.stop()

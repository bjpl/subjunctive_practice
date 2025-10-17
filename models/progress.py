"""
Progress tracking models: Sessions, Attempts, Achievements, and Statistics.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base


class Session(Base):
    """
    Practice session model.
    Tracks individual learning sessions.
    """
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Session metadata
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    ended_at = Column(DateTime, nullable=True)
    duration_seconds = Column(Integer, nullable=True)

    # Session stats
    total_exercises = Column(Integer, default=0, nullable=False)
    correct_answers = Column(Integer, default=0, nullable=False)
    score_percentage = Column(Float, nullable=True)

    # Session context
    session_type = Column(String(50), default="practice", nullable=False)  # practice, review, test
    is_completed = Column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="sessions")
    attempts = relationship("Attempt", back_populates="session", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Session(id={self.id}, user_id={self.user_id}, score={self.score_percentage}%)>"


class Attempt(Base):
    """
    Individual exercise attempt within a session.
    Tracks detailed performance data.
    """
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id", ondelete="SET NULL"), nullable=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Attempt data
    user_answer = Column(String(200), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    time_taken_seconds = Column(Integer, nullable=True)

    # Learning metadata
    hints_used = Column(Integer, default=0, nullable=False)
    attempts_count = Column(Integer, default=1, nullable=False)  # If user tried multiple times
    confidence_level = Column(Integer, nullable=True)  # 1-5 self-assessment

    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    session = relationship("Session", back_populates="attempts")
    exercise = relationship("Exercise", back_populates="attempts")

    def __repr__(self):
        return f"<Attempt(id={self.id}, exercise_id={self.exercise_id}, correct={self.is_correct})>"


class Achievement(Base):
    """
    Achievement/badge definitions.
    Gamification elements to encourage learning.
    """
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)

    # Achievement metadata
    category = Column(String(50), nullable=False)  # streak, mastery, practice, milestone
    icon_url = Column(String(500), nullable=True)
    points = Column(Integer, default=10, nullable=False)

    # Unlock criteria (stored as JSON)
    criteria = Column(JSON, nullable=False)  # {"streak_days": 7} or {"correct_answers": 100}

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user_achievements = relationship("UserAchievement", back_populates="achievement")

    def __repr__(self):
        return f"<Achievement(id={self.id}, name='{self.name}', points={self.points})>"


class UserAchievement(Base):
    """
    User's earned achievements.
    Many-to-many relationship with achievement unlock tracking.
    """
    __tablename__ = "user_achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    achievement_id = Column(Integer, ForeignKey("achievements.id", ondelete="CASCADE"), nullable=False, index=True)

    # Unlock data
    unlocked_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    progress_data = Column(JSON, nullable=True)  # Additional context about unlock

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="user_achievements")

    def __repr__(self):
        return f"<UserAchievement(user_id={self.user_id}, achievement_id={self.achievement_id})>"


class ReviewSchedule(Base):
    """
    Spaced repetition schedule for individual verbs/exercises.
    Implements SM-2 algorithm for optimal review timing.
    """
    __tablename__ = "review_schedules"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    verb_id = Column(Integer, ForeignKey("verbs.id", ondelete="CASCADE"), nullable=False, index=True)

    # SM-2 algorithm parameters
    easiness_factor = Column(Float, default=2.5, nullable=False)  # 1.3 - 2.5
    interval_days = Column(Integer, default=1, nullable=False)
    repetitions = Column(Integer, default=0, nullable=False)

    # Review tracking
    next_review_date = Column(DateTime, nullable=False)
    last_reviewed_at = Column(DateTime, nullable=True)
    review_count = Column(Integer, default=0, nullable=False)

    # Performance tracking
    total_correct = Column(Integer, default=0, nullable=False)
    total_attempts = Column(Integer, default=0, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="review_schedules")
    verb = relationship("Verb", back_populates="review_schedules")

    def __repr__(self):
        return f"<ReviewSchedule(user_id={self.user_id}, verb_id={self.verb_id}, next={self.next_review_date})>"


class UserStatistics(Base):
    """
    Aggregated user statistics for analytics and dashboards.
    One-to-one with User, updated periodically.
    """
    __tablename__ = "user_statistics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)

    # Overall statistics
    total_sessions = Column(Integer, default=0, nullable=False)
    total_exercises_completed = Column(Integer, default=0, nullable=False)
    total_correct_answers = Column(Integer, default=0, nullable=False)
    overall_accuracy = Column(Float, default=0.0, nullable=False)  # 0-100%

    # Time statistics
    total_study_time_minutes = Column(Integer, default=0, nullable=False)
    average_session_duration = Column(Integer, default=0, nullable=False)

    # Verb mastery
    verbs_mastered = Column(Integer, default=0, nullable=False)
    verbs_learning = Column(Integer, default=0, nullable=False)

    # Weekly statistics
    weekly_exercises = Column(Integer, default=0, nullable=False)
    weekly_accuracy = Column(Float, default=0.0, nullable=False)

    # Achievement stats
    total_achievements = Column(Integer, default=0, nullable=False)
    total_points = Column(Integer, default=0, nullable=False)

    # Last updated
    last_calculated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="statistics")

    def __repr__(self):
        return f"<UserStatistics(user_id={self.user_id}, accuracy={self.overall_accuracy}%)>"

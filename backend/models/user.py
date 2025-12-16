"""
User management models: User, Profile, and Preferences.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from core.database import Base


class UserRole(str, enum.Enum):
    """User role enumeration."""
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"


class LanguageLevel(str, enum.Enum):
    """CEFR language proficiency levels."""
    A1 = "A1"  # Beginner
    A2 = "A2"  # Elementary
    B1 = "B1"  # Intermediate
    B2 = "B2"  # Upper Intermediate
    C1 = "C1"  # Advanced
    C2 = "C2"  # Proficient


class User(Base):
    """
    User account model.
    Stores authentication and core user data.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.STUDENT, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)

    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    preferences = relationship("UserPreference", back_populates="user", uselist=False, cascade="all, delete-orphan")
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")
    achievements = relationship("UserAchievement", back_populates="user", cascade="all, delete-orphan")
    review_schedules = relationship("ReviewSchedule", back_populates="user", cascade="all, delete-orphan")
    statistics = relationship("UserStatistics", back_populates="user", uselist=False, cascade="all, delete-orphan")
    ai_usage_records = relationship("AIUsageRecord", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


class UserProfile(Base):
    """
    User profile with learning metadata.
    One-to-one relationship with User.
    """
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    # Profile information
    full_name = Column(String(100), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)

    # Learning metadata
    current_level = Column(SQLEnum(LanguageLevel), default=LanguageLevel.A1, nullable=False)
    target_level = Column(SQLEnum(LanguageLevel), default=LanguageLevel.B2, nullable=True)
    native_language = Column(String(50), default="English", nullable=True)

    # Streak and engagement
    current_streak = Column(Integer, default=0, nullable=False)
    longest_streak = Column(Integer, default=0, nullable=False)
    last_practice_date = Column(DateTime, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="profile")

    def __repr__(self):
        return f"<UserProfile(user_id={self.user_id}, level={self.current_level})>"


class UserPreference(Base):
    """
    User learning preferences and settings.
    One-to-one relationship with User.
    """
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    # Exercise preferences
    daily_goal = Column(Integer, default=10, nullable=False)  # exercises per day
    session_length = Column(Integer, default=15, nullable=False)  # minutes
    difficulty_preference = Column(Integer, default=2, nullable=False)  # 1=easy, 2=medium, 3=hard

    # Notification settings
    email_notifications = Column(Boolean, default=True, nullable=False)
    reminder_enabled = Column(Boolean, default=True, nullable=False)
    reminder_time = Column(String(5), default="19:00", nullable=True)  # HH:MM format

    # Learning preferences
    show_explanations = Column(Boolean, default=True, nullable=False)
    auto_advance = Column(Boolean, default=False, nullable=False)
    audio_enabled = Column(Boolean, default=True, nullable=False)

    # Spaced repetition settings
    enable_spaced_repetition = Column(Boolean, default=True, nullable=False)
    review_frequency = Column(Integer, default=3, nullable=False)  # days between reviews

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="preferences")

    def __repr__(self):
        return f"<UserPreference(user_id={self.user_id}, daily_goal={self.daily_goal})>"

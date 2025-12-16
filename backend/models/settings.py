"""
User settings database model.
Replaces file-based settings storage with database persistence.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base


class UserSettings(Base):
    """
    User settings model stored in database.
    Replaces file-based JSON storage for settings.
    """
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)

    # Notification settings
    notifications = Column(JSON, nullable=False, default={
        "email": True,
        "push": False,
        "streakReminders": True
    })

    # Practice settings
    practice = Column(JSON, nullable=False, default={
        "dailyGoal": 10,
        "autoAdvance": True,
        "showHints": True,
        "showExplanations": True
    })

    # Accessibility settings
    accessibility = Column(JSON, nullable=False, default={
        "fontSize": "medium",
        "highContrast": False,
        "reduceMotion": False
    })

    # Language settings
    language = Column(JSON, nullable=False, default={
        "interface": "en",
        "practice": "es"
    })

    # Metadata
    version = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="settings")

    def __repr__(self):
        return f"<UserSettings(user_id={self.user_id}, version={self.version})>"

    def to_dict(self):
        """Convert settings to dictionary format."""
        return {
            "notifications": self.notifications,
            "practice": self.practice,
            "accessibility": self.accessibility,
            "language": self.language
        }

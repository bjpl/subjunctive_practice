"""
SQLAlchemy ORM models for database tables.

This module exports all database models for easy importing.
Models are organized by domain:
- user.py: User, UserProfile, UserPreference
- exercise.py: Verb, Exercise, Scenario, ExerciseScenario
- progress.py: Session, Attempt, Achievement, UserAchievement, ReviewSchedule, UserStatistics

Usage:
    from models import User, Exercise, Session
    from models.user import UserRole, LanguageLevel
    from models.exercise import VerbType, SubjunctiveTense, ExerciseType, DifficultyLevel
"""

# Import all SQLAlchemy models
from .user import (
    User,
    UserProfile,
    UserPreference,
    UserRole,
    LanguageLevel,
)

from .exercise import (
    Verb,
    Exercise,
    Scenario,
    ExerciseScenario,
    VerbType,
    SubjunctiveTense,
    ExerciseType,
    DifficultyLevel,
)

from .progress import (
    Session,
    Attempt,
    Achievement,
    UserAchievement,
    ReviewSchedule,
    UserStatistics,
)

# Export all models
__all__ = [
    # User models
    "User",
    "UserProfile",
    "UserPreference",
    "UserRole",
    "LanguageLevel",
    # Exercise models
    "Verb",
    "Exercise",
    "Scenario",
    "ExerciseScenario",
    "VerbType",
    "SubjunctiveTense",
    "ExerciseType",
    "DifficultyLevel",
    # Progress models
    "Session",
    "Attempt",
    "Achievement",
    "UserAchievement",
    "ReviewSchedule",
    "UserStatistics",
]

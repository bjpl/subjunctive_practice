"""
Pydantic schemas for API request/response validation.
"""

from backend.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserProfileResponse,
    UserPreferenceUpdate,
)
from backend.schemas.exercise import (
    VerbResponse,
    ExerciseResponse,
    ExerciseWithAnswer,
    ScenarioResponse,
    ScenarioWithExercises,
    AnswerSubmit,
    AnswerValidation,
    ExerciseListResponse,
)
from backend.schemas.progress import (
    SessionCreate,
    SessionResponse,
    AttemptCreate,
    AttemptResponse,
    AchievementResponse,
    UserStatisticsResponse,
)

__all__ = [
    # User schemas
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserProfileResponse",
    "UserPreferenceUpdate",
    # Exercise schemas
    "VerbResponse",
    "ExerciseResponse",
    "ExerciseWithAnswer",
    "ScenarioResponse",
    "ScenarioWithExercises",
    "AnswerSubmit",
    "AnswerValidation",
    "ExerciseListResponse",
    # Progress schemas
    "SessionCreate",
    "SessionResponse",
    "AttemptCreate",
    "AttemptResponse",
    "AchievementResponse",
    "UserStatisticsResponse",
]

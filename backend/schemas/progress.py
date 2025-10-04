"""
Pydantic schemas for progress tracking models.
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List, Dict, Any


class SessionBase(BaseModel):
    """Base session schema."""
    session_type: str = "practice"


class SessionCreate(SessionBase):
    """Schema for creating a session."""
    pass


class SessionUpdate(BaseModel):
    """Schema for updating a session."""
    ended_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    total_exercises: Optional[int] = None
    correct_answers: Optional[int] = None
    score_percentage: Optional[float] = None
    is_completed: Optional[bool] = None


class SessionResponse(SessionBase):
    """Schema for session response."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    started_at: datetime
    ended_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    total_exercises: int
    correct_answers: int
    score_percentage: Optional[float] = None
    is_completed: bool
    created_at: datetime


class AttemptBase(BaseModel):
    """Base attempt schema."""
    user_answer: str
    time_taken_seconds: Optional[int] = None
    hints_used: int = 0
    confidence_level: Optional[int] = Field(None, ge=1, le=5)


class AttemptCreate(AttemptBase):
    """Schema for creating an attempt."""
    exercise_id: int


class AttemptResponse(AttemptBase):
    """Schema for attempt response."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    session_id: int
    exercise_id: Optional[int] = None
    user_id: int
    is_correct: bool
    attempts_count: int
    created_at: datetime


class AchievementBase(BaseModel):
    """Base achievement schema."""
    name: str = Field(..., max_length=100)
    description: str
    category: str = Field(..., max_length=50)
    points: int = Field(default=10, ge=0)


class AchievementCreate(AchievementBase):
    """Schema for creating an achievement."""
    icon_url: Optional[str] = None
    criteria: Dict[str, Any]


class AchievementResponse(AchievementBase):
    """Schema for achievement response."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    icon_url: Optional[str] = None
    created_at: datetime


class UserAchievementResponse(BaseModel):
    """Schema for user achievement response."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    achievement_id: int
    achievement: Optional[AchievementResponse] = None
    unlocked_at: datetime
    progress_data: Optional[Dict[str, Any]] = None


class ReviewScheduleResponse(BaseModel):
    """Schema for review schedule response."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    verb_id: int
    easiness_factor: float
    interval_days: int
    repetitions: int
    next_review_date: datetime
    last_reviewed_at: Optional[datetime] = None
    review_count: int
    total_correct: int
    total_attempts: int


class UserStatisticsResponse(BaseModel):
    """Schema for user statistics response."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    total_sessions: int
    total_exercises_completed: int
    total_correct_answers: int
    overall_accuracy: float
    total_study_time_minutes: int
    average_session_duration: int
    verbs_mastered: int
    verbs_learning: int
    weekly_exercises: int
    weekly_accuracy: float
    total_achievements: int
    total_points: int
    last_calculated_at: datetime

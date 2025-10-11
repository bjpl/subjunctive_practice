"""
Pydantic schemas for user-related models.
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional
from backend.models.user import UserRole, LanguageLevel


class UserBase(BaseModel):
    """Base user schema with common fields."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8, max_length=100)


class UserProfileResponse(BaseModel):
    """Schema for user profile response."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    current_level: LanguageLevel
    target_level: Optional[LanguageLevel] = None
    native_language: Optional[str] = None
    current_streak: int
    longest_streak: int
    last_practice_date: Optional[datetime] = None


class UserPreferenceResponse(BaseModel):
    """Schema for user preferences response."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    daily_goal: int
    session_length: int
    difficulty_preference: int
    email_notifications: bool
    reminder_enabled: bool
    reminder_time: Optional[str] = None
    show_explanations: bool
    auto_advance: bool
    audio_enabled: bool
    enable_spaced_repetition: bool
    review_frequency: int


class UserPreferenceUpdate(BaseModel):
    """Schema for updating user preferences."""
    daily_goal: Optional[int] = Field(None, ge=1, le=100)
    session_length: Optional[int] = Field(None, ge=5, le=120)
    difficulty_preference: Optional[int] = Field(None, ge=1, le=3)
    email_notifications: Optional[bool] = None
    reminder_enabled: Optional[bool] = None
    reminder_time: Optional[str] = Field(None, regex=r"^([01]\d|2[0-3]):([0-5]\d)$")
    show_explanations: Optional[bool] = None
    auto_advance: Optional[bool] = None
    audio_enabled: Optional[bool] = None
    enable_spaced_repetition: Optional[bool] = None
    review_frequency: Optional[int] = Field(None, ge=1, le=30)


class UserResponse(UserBase):
    """Schema for user response."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    profile: Optional[UserProfileResponse] = None
    preferences: Optional[UserPreferenceResponse] = None


class UserLogin(BaseModel):
    """Schema for user login."""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Schema for authentication token response."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

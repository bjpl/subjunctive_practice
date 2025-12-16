"""
Pydantic schemas for leaderboard-related models.
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List
from models.leaderboard import ScoreType, LeaderboardPeriod


class LeaderboardEntryBase(BaseModel):
    """Base leaderboard entry schema."""
    score_type: ScoreType
    score: float = Field(..., ge=0)
    period: LeaderboardPeriod


class LeaderboardEntryCreate(LeaderboardEntryBase):
    """Schema for creating a leaderboard entry."""
    user_id: int
    period_start: datetime
    period_end: datetime


class LeaderboardEntryUpdate(BaseModel):
    """Schema for updating a leaderboard entry."""
    score: Optional[float] = Field(None, ge=0)
    rank: Optional[int] = Field(None, ge=1)


class UserLeaderboardInfo(BaseModel):
    """Schema for user information in leaderboard display."""
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    username: str
    avatar_url: Optional[str] = None
    full_name: Optional[str] = None


class LeaderboardEntryResponse(BaseModel):
    """Schema for leaderboard entry response."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    username: str
    avatar_url: Optional[str] = None
    full_name: Optional[str] = None
    score_type: ScoreType
    score: float
    rank: int
    achieved_at: datetime
    period: LeaderboardPeriod
    is_current_user: bool = False


class LeaderboardResponse(BaseModel):
    """Schema for complete leaderboard response."""
    score_type: ScoreType
    period: LeaderboardPeriod
    entries: List[LeaderboardEntryResponse]
    total_participants: int
    last_updated: datetime
    period_start: datetime
    period_end: datetime


class UserRankResponse(BaseModel):
    """Schema for user's rank information."""
    user_id: int
    username: str
    score_type: ScoreType
    period: LeaderboardPeriod
    score: float
    rank: int
    total_participants: int
    percentile: float
    nearby_users: List[LeaderboardEntryResponse]


class LeaderboardStatsResponse(BaseModel):
    """Schema for leaderboard statistics."""
    score_type: ScoreType
    period: LeaderboardPeriod
    total_participants: int
    highest_score: float
    average_score: float
    median_score: float
    your_rank: Optional[int] = None
    your_score: Optional[float] = None
    your_percentile: Optional[float] = None


class LeaderboardSnapshotResponse(BaseModel):
    """Schema for historical leaderboard snapshot."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    score_type: ScoreType
    score: float
    rank: int
    period: LeaderboardPeriod
    period_start: datetime
    period_end: datetime
    snapshot_date: datetime
    total_participants: int
    percentile: Optional[float] = None
    score_change: Optional[float] = None
    rank_change: Optional[int] = None


class LeaderboardHistoryResponse(BaseModel):
    """Schema for user's leaderboard history."""
    user_id: int
    score_type: ScoreType
    snapshots: List[LeaderboardSnapshotResponse]
    best_rank: int
    best_score: float
    average_rank: float
    average_score: float

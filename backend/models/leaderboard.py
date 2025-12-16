"""
Leaderboard models for competitive learning features.
Tracks user rankings across multiple metrics and time periods.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Index, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base
import enum


class ScoreType(str, enum.Enum):
    """Types of scores tracked on the leaderboard."""
    XP = "xp"
    ACCURACY = "accuracy"
    STREAK = "streak"
    EXERCISES_COMPLETED = "exercises_completed"


class LeaderboardPeriod(str, enum.Enum):
    """Time periods for leaderboard rankings."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    ALL_TIME = "all_time"


class LeaderboardEntry(Base):
    """
    Current leaderboard entries for users across different metrics.
    This table is updated in real-time as users complete activities.
    """
    __tablename__ = "leaderboard_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Score details
    score_type = Column(SQLEnum(ScoreType), nullable=False, index=True)
    score = Column(Float, nullable=False, default=0.0)
    rank = Column(Integer, nullable=True, index=True)

    # Time period
    period = Column(SQLEnum(LeaderboardPeriod), nullable=False, index=True)
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)

    # Tie-breaking metadata
    achieved_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", backref="leaderboard_entries")

    # Composite indexes for efficient queries
    __table_args__ = (
        Index('idx_leaderboard_score_period', 'score_type', 'period', 'score', 'achieved_at'),
        Index('idx_leaderboard_user_period', 'user_id', 'score_type', 'period'),
    )

    def __repr__(self):
        return f"<LeaderboardEntry(user_id={self.user_id}, type={self.score_type}, period={self.period}, score={self.score}, rank={self.rank})>"


class LeaderboardSnapshot(Base):
    """
    Historical snapshots of leaderboard standings.
    Stores final rankings at the end of each period for archival and analytics.
    """
    __tablename__ = "leaderboard_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Snapshot details
    score_type = Column(SQLEnum(ScoreType), nullable=False, index=True)
    score = Column(Float, nullable=False)
    rank = Column(Integer, nullable=False, index=True)

    # Period information
    period = Column(SQLEnum(LeaderboardPeriod), nullable=False, index=True)
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)

    # Snapshot metadata
    snapshot_date = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    total_participants = Column(Integer, nullable=False)

    # Performance details
    percentile = Column(Float, nullable=True)  # Top X% of users
    score_change = Column(Float, nullable=True)  # Change from previous period
    rank_change = Column(Integer, nullable=True)  # Rank improvement/decline

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", backref="leaderboard_snapshots")

    # Composite indexes for historical queries
    __table_args__ = (
        Index('idx_snapshot_period_type', 'period', 'score_type', 'snapshot_date'),
        Index('idx_snapshot_user_history', 'user_id', 'score_type', 'period', 'snapshot_date'),
    )

    def __repr__(self):
        return f"<LeaderboardSnapshot(user_id={self.user_id}, period={self.period}, rank={self.rank}, date={self.snapshot_date})>"


class LeaderboardCache(Base):
    """
    Cache table for frequently accessed leaderboard queries.
    Reduces database load for popular leaderboard views.
    """
    __tablename__ = "leaderboard_cache"

    id = Column(Integer, primary_key=True, index=True)

    # Cache key components
    score_type = Column(SQLEnum(ScoreType), nullable=False, index=True)
    period = Column(SQLEnum(LeaderboardPeriod), nullable=False, index=True)
    cache_key = Column(String(255), unique=True, nullable=False, index=True)

    # Cached data (stored as JSON string)
    cached_data = Column(String, nullable=False)  # JSON string of leaderboard data

    # Cache metadata
    cache_hits = Column(Integer, default=0, nullable=False)
    expires_at = Column(DateTime, nullable=False, index=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<LeaderboardCache(key={self.cache_key}, expires={self.expires_at})>"

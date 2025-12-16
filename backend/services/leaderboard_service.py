"""
Leaderboard service for managing rankings, scores, and competitive features.
Implements efficient ranking algorithms with caching and tie-breaking logic.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, select
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Tuple
import json
from models.leaderboard import (
    LeaderboardEntry,
    LeaderboardSnapshot,
    LeaderboardCache,
    ScoreType,
    LeaderboardPeriod
)
from models.user import User, UserProfile
from models.progress import UserStatistics
from schemas.leaderboard import (
    LeaderboardEntryResponse,
    LeaderboardResponse,
    UserRankResponse,
    LeaderboardStatsResponse,
    LeaderboardSnapshotResponse,
    LeaderboardHistoryResponse
)


class LeaderboardService:
    """Service class for leaderboard operations with caching and ranking logic."""

    CACHE_TTL_SECONDS = 300  # 5 minutes
    DEFAULT_LIMIT = 10

    def __init__(self, db: Session):
        self.db = db

    def _get_period_bounds(self, period: LeaderboardPeriod) -> Tuple[datetime, datetime]:
        """Calculate start and end datetime for a given period."""
        now = datetime.utcnow()

        if period == LeaderboardPeriod.DAILY:
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=1)
        elif period == LeaderboardPeriod.WEEKLY:
            # Start from Monday
            days_since_monday = now.weekday()
            start = (now - timedelta(days=days_since_monday)).replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=7)
        elif period == LeaderboardPeriod.MONTHLY:
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            # Calculate next month's first day
            if now.month == 12:
                end = start.replace(year=start.year + 1, month=1)
            else:
                end = start.replace(month=start.month + 1)
        else:  # ALL_TIME
            start = datetime(2000, 1, 1)
            end = datetime(2099, 12, 31)

        return start, end

    def _get_score_from_statistics(self, user_id: int, score_type: ScoreType) -> float:
        """Extract score from UserStatistics based on score type."""
        stats = self.db.query(UserStatistics).filter(
            UserStatistics.user_id == user_id
        ).first()

        if not stats:
            return 0.0

        score_mapping = {
            ScoreType.XP: float(stats.total_points),
            ScoreType.ACCURACY: float(stats.overall_accuracy),
            ScoreType.EXERCISES_COMPLETED: float(stats.total_exercises_completed),
        }

        return score_mapping.get(score_type, 0.0)

    def _get_streak_score(self, user_id: int) -> float:
        """Get current streak from user profile."""
        profile = self.db.query(UserProfile).filter(
            UserProfile.user_id == user_id
        ).first()

        return float(profile.current_streak) if profile else 0.0

    def update_user_score(
        self,
        user_id: int,
        score_type: ScoreType,
        new_score: float,
        period: LeaderboardPeriod = LeaderboardPeriod.ALL_TIME
    ) -> LeaderboardEntry:
        """
        Update or create a user's leaderboard score.

        Args:
            user_id: User identifier
            score_type: Type of score being updated
            new_score: New score value
            period: Time period for the score

        Returns:
            Updated LeaderboardEntry
        """
        period_start, period_end = self._get_period_bounds(period)

        # Check if entry exists
        entry = self.db.query(LeaderboardEntry).filter(
            and_(
                LeaderboardEntry.user_id == user_id,
                LeaderboardEntry.score_type == score_type,
                LeaderboardEntry.period == period,
                LeaderboardEntry.period_start == period_start
            )
        ).first()

        if entry:
            # Update existing entry
            entry.score = new_score
            entry.updated_at = datetime.utcnow()
            # Only update achieved_at if score improved
            if new_score > entry.score:
                entry.achieved_at = datetime.utcnow()
        else:
            # Create new entry
            entry = LeaderboardEntry(
                user_id=user_id,
                score_type=score_type,
                score=new_score,
                period=period,
                period_start=period_start,
                period_end=period_end,
                achieved_at=datetime.utcnow()
            )
            self.db.add(entry)

        self.db.commit()
        self.db.refresh(entry)

        # Recalculate ranks for this score type and period
        self._recalculate_ranks(score_type, period)

        # Invalidate cache
        self._invalidate_cache(score_type, period)

        return entry

    def _recalculate_ranks(self, score_type: ScoreType, period: LeaderboardPeriod):
        """
        Recalculate ranks for all users in a specific leaderboard.
        Uses SQL window functions for efficient ranking with tie-breaking.
        """
        period_start, period_end = self._get_period_bounds(period)

        # Use window function to assign ranks
        # ORDER BY score DESC, achieved_at ASC (earlier achiever wins ties)
        rank_subquery = self.db.query(
            LeaderboardEntry.id,
            func.row_number().over(
                order_by=[
                    LeaderboardEntry.score.desc(),
                    LeaderboardEntry.achieved_at.asc()
                ]
            ).label('new_rank')
        ).filter(
            and_(
                LeaderboardEntry.score_type == score_type,
                LeaderboardEntry.period == period,
                LeaderboardEntry.period_start == period_start
            )
        ).subquery()

        # Update ranks in batch
        self.db.query(LeaderboardEntry).filter(
            LeaderboardEntry.id == rank_subquery.c.id
        ).update(
            {LeaderboardEntry.rank: rank_subquery.c.new_rank},
            synchronize_session=False
        )

        self.db.commit()

    def get_leaderboard(
        self,
        score_type: ScoreType,
        period: LeaderboardPeriod,
        limit: int = DEFAULT_LIMIT,
        offset: int = 0,
        current_user_id: Optional[int] = None
    ) -> LeaderboardResponse:
        """
        Get top users for a specific leaderboard.

        Args:
            score_type: Type of score to rank by
            period: Time period
            limit: Maximum number of entries to return
            offset: Number of entries to skip
            current_user_id: ID of requesting user (to mark their entry)

        Returns:
            LeaderboardResponse with top entries
        """
        # Check cache first
        cache_key = f"{score_type.value}_{period.value}_{limit}_{offset}"
        cached = self._get_from_cache(cache_key)

        if cached and not current_user_id:
            return cached

        period_start, period_end = self._get_period_bounds(period)

        # Query leaderboard entries with user info
        query = self.db.query(
            LeaderboardEntry,
            User.username,
            UserProfile.avatar_url,
            UserProfile.full_name
        ).join(
            User, LeaderboardEntry.user_id == User.id
        ).outerjoin(
            UserProfile, User.id == UserProfile.user_id
        ).filter(
            and_(
                LeaderboardEntry.score_type == score_type,
                LeaderboardEntry.period == period,
                LeaderboardEntry.period_start == period_start,
                LeaderboardEntry.rank.isnot(None)
            )
        ).order_by(
            LeaderboardEntry.rank.asc()
        ).limit(limit).offset(offset)

        results = query.all()

        # Get total participants
        total_participants = self.db.query(func.count(LeaderboardEntry.id)).filter(
            and_(
                LeaderboardEntry.score_type == score_type,
                LeaderboardEntry.period == period,
                LeaderboardEntry.period_start == period_start
            )
        ).scalar() or 0

        # Format response
        entries = [
            LeaderboardEntryResponse(
                id=entry.id,
                user_id=entry.user_id,
                username=username,
                avatar_url=avatar_url,
                full_name=full_name,
                score_type=entry.score_type,
                score=entry.score,
                rank=entry.rank,
                achieved_at=entry.achieved_at,
                period=entry.period,
                is_current_user=(entry.user_id == current_user_id) if current_user_id else False
            )
            for entry, username, avatar_url, full_name in results
        ]

        response = LeaderboardResponse(
            score_type=score_type,
            period=period,
            entries=entries,
            total_participants=total_participants,
            last_updated=datetime.utcnow(),
            period_start=period_start,
            period_end=period_end
        )

        # Cache the response (without current_user marking)
        if not current_user_id:
            self._save_to_cache(cache_key, response)

        return response

    def get_user_rank(
        self,
        user_id: int,
        score_type: ScoreType,
        period: LeaderboardPeriod
    ) -> Optional[UserRankResponse]:
        """
        Get a user's rank and nearby competitors.

        Args:
            user_id: User identifier
            score_type: Type of score
            period: Time period

        Returns:
            UserRankResponse with rank and nearby users
        """
        period_start, period_end = self._get_period_bounds(period)

        # Get user's entry
        user_entry = self.db.query(
            LeaderboardEntry,
            User.username
        ).join(
            User, LeaderboardEntry.user_id == User.id
        ).filter(
            and_(
                LeaderboardEntry.user_id == user_id,
                LeaderboardEntry.score_type == score_type,
                LeaderboardEntry.period == period,
                LeaderboardEntry.period_start == period_start
            )
        ).first()

        if not user_entry:
            return None

        entry, username = user_entry

        # Get total participants
        total_participants = self.db.query(func.count(LeaderboardEntry.id)).filter(
            and_(
                LeaderboardEntry.score_type == score_type,
                LeaderboardEntry.period == period,
                LeaderboardEntry.period_start == period_start
            )
        ).scalar() or 1

        # Calculate percentile
        percentile = ((total_participants - entry.rank) / total_participants) * 100

        # Get nearby users
        nearby_users = self.get_nearby_users(user_id, score_type, period, above=2, below=2)

        return UserRankResponse(
            user_id=user_id,
            username=username,
            score_type=score_type,
            period=period,
            score=entry.score,
            rank=entry.rank,
            total_participants=total_participants,
            percentile=round(percentile, 2),
            nearby_users=nearby_users
        )

    def get_nearby_users(
        self,
        user_id: int,
        score_type: ScoreType,
        period: LeaderboardPeriod,
        above: int = 2,
        below: int = 2
    ) -> List[LeaderboardEntryResponse]:
        """
        Get users ranked near the specified user.

        Args:
            user_id: User identifier
            score_type: Type of score
            period: Time period
            above: Number of higher-ranked users to include
            below: Number of lower-ranked users to include

        Returns:
            List of nearby LeaderboardEntryResponse
        """
        period_start, period_end = self._get_period_bounds(period)

        # Get user's rank
        user_entry = self.db.query(LeaderboardEntry).filter(
            and_(
                LeaderboardEntry.user_id == user_id,
                LeaderboardEntry.score_type == score_type,
                LeaderboardEntry.period == period,
                LeaderboardEntry.period_start == period_start
            )
        ).first()

        if not user_entry or not user_entry.rank:
            return []

        user_rank = user_entry.rank
        min_rank = max(1, user_rank - above)
        max_rank = user_rank + below

        # Query nearby entries
        query = self.db.query(
            LeaderboardEntry,
            User.username,
            UserProfile.avatar_url,
            UserProfile.full_name
        ).join(
            User, LeaderboardEntry.user_id == User.id
        ).outerjoin(
            UserProfile, User.id == UserProfile.user_id
        ).filter(
            and_(
                LeaderboardEntry.score_type == score_type,
                LeaderboardEntry.period == period,
                LeaderboardEntry.period_start == period_start,
                LeaderboardEntry.rank >= min_rank,
                LeaderboardEntry.rank <= max_rank
            )
        ).order_by(LeaderboardEntry.rank.asc())

        results = query.all()

        return [
            LeaderboardEntryResponse(
                id=entry.id,
                user_id=entry.user_id,
                username=username,
                avatar_url=avatar_url,
                full_name=full_name,
                score_type=entry.score_type,
                score=entry.score,
                rank=entry.rank,
                achieved_at=entry.achieved_at,
                period=entry.period,
                is_current_user=(entry.user_id == user_id)
            )
            for entry, username, avatar_url, full_name in results
        ]

    def get_leaderboard_stats(
        self,
        score_type: ScoreType,
        period: LeaderboardPeriod,
        user_id: Optional[int] = None
    ) -> LeaderboardStatsResponse:
        """Get statistical summary of a leaderboard."""
        period_start, period_end = self._get_period_bounds(period)

        # Aggregate statistics
        stats = self.db.query(
            func.count(LeaderboardEntry.id).label('total'),
            func.max(LeaderboardEntry.score).label('max_score'),
            func.avg(LeaderboardEntry.score).label('avg_score')
        ).filter(
            and_(
                LeaderboardEntry.score_type == score_type,
                LeaderboardEntry.period == period,
                LeaderboardEntry.period_start == period_start
            )
        ).first()

        # Calculate median (works in PostgreSQL and SQLite)
        scores = self.db.query(LeaderboardEntry.score).filter(
            and_(
                LeaderboardEntry.score_type == score_type,
                LeaderboardEntry.period == period,
                LeaderboardEntry.period_start == period_start
            )
        ).order_by(LeaderboardEntry.score.asc()).all()

        median_score = 0.0
        if scores:
            mid = len(scores) // 2
            median_score = float(scores[mid][0]) if len(scores) % 2 else float((scores[mid-1][0] + scores[mid][0]) / 2)

        # Get user's stats if provided
        your_rank = None
        your_score = None
        your_percentile = None

        if user_id:
            user_entry = self.db.query(LeaderboardEntry).filter(
                and_(
                    LeaderboardEntry.user_id == user_id,
                    LeaderboardEntry.score_type == score_type,
                    LeaderboardEntry.period == period,
                    LeaderboardEntry.period_start == period_start
                )
            ).first()

            if user_entry:
                your_rank = user_entry.rank
                your_score = user_entry.score
                if stats.total > 0:
                    your_percentile = ((stats.total - user_entry.rank) / stats.total) * 100

        return LeaderboardStatsResponse(
            score_type=score_type,
            period=period,
            total_participants=stats.total or 0,
            highest_score=float(stats.max_score) if stats.max_score else 0.0,
            average_score=float(stats.avg_score) if stats.avg_score else 0.0,
            median_score=median_score,
            your_rank=your_rank,
            your_score=your_score,
            your_percentile=round(your_percentile, 2) if your_percentile else None
        )

    def create_snapshot(
        self,
        score_type: ScoreType,
        period: LeaderboardPeriod
    ) -> int:
        """
        Create historical snapshot of current leaderboard standings.
        Called at the end of each period.

        Returns:
            Number of snapshots created
        """
        period_start, period_end = self._get_period_bounds(period)

        # Get all current entries
        entries = self.db.query(LeaderboardEntry).filter(
            and_(
                LeaderboardEntry.score_type == score_type,
                LeaderboardEntry.period == period,
                LeaderboardEntry.period_start == period_start
            )
        ).all()

        total_participants = len(entries)
        snapshot_count = 0

        for entry in entries:
            # Calculate percentile
            percentile = ((total_participants - entry.rank) / total_participants) * 100 if entry.rank else None

            # Check for previous snapshot to calculate changes
            prev_snapshot = self.db.query(LeaderboardSnapshot).filter(
                and_(
                    LeaderboardSnapshot.user_id == entry.user_id,
                    LeaderboardSnapshot.score_type == score_type,
                    LeaderboardSnapshot.period == period
                )
            ).order_by(LeaderboardSnapshot.snapshot_date.desc()).first()

            score_change = None
            rank_change = None

            if prev_snapshot:
                score_change = entry.score - prev_snapshot.score
                if entry.rank and prev_snapshot.rank:
                    rank_change = prev_snapshot.rank - entry.rank  # Positive = improvement

            # Create snapshot
            snapshot = LeaderboardSnapshot(
                user_id=entry.user_id,
                score_type=score_type,
                score=entry.score,
                rank=entry.rank or 0,
                period=period,
                period_start=period_start,
                period_end=period_end,
                total_participants=total_participants,
                percentile=percentile,
                score_change=score_change,
                rank_change=rank_change
            )

            self.db.add(snapshot)
            snapshot_count += 1

        self.db.commit()
        return snapshot_count

    def _get_from_cache(self, cache_key: str) -> Optional[LeaderboardResponse]:
        """Retrieve data from cache if valid."""
        cache_entry = self.db.query(LeaderboardCache).filter(
            and_(
                LeaderboardCache.cache_key == cache_key,
                LeaderboardCache.expires_at > datetime.utcnow()
            )
        ).first()

        if cache_entry:
            cache_entry.cache_hits += 1
            self.db.commit()

            # Deserialize cached data
            try:
                data = json.loads(cache_entry.cached_data)
                return LeaderboardResponse(**data)
            except Exception:
                return None

        return None

    def _save_to_cache(self, cache_key: str, data: LeaderboardResponse):
        """Save data to cache with TTL."""
        expires_at = datetime.utcnow() + timedelta(seconds=self.CACHE_TTL_SECONDS)

        # Serialize data
        cached_data = data.model_dump_json()

        # Check if cache entry exists
        cache_entry = self.db.query(LeaderboardCache).filter(
            LeaderboardCache.cache_key == cache_key
        ).first()

        if cache_entry:
            cache_entry.cached_data = cached_data
            cache_entry.expires_at = expires_at
            cache_entry.updated_at = datetime.utcnow()
        else:
            cache_entry = LeaderboardCache(
                score_type=data.score_type,
                period=data.period,
                cache_key=cache_key,
                cached_data=cached_data,
                expires_at=expires_at
            )
            self.db.add(cache_entry)

        self.db.commit()

    def _invalidate_cache(self, score_type: ScoreType, period: LeaderboardPeriod):
        """Invalidate all cache entries for a specific leaderboard."""
        self.db.query(LeaderboardCache).filter(
            and_(
                LeaderboardCache.score_type == score_type,
                LeaderboardCache.period == period
            )
        ).delete()

        self.db.commit()

    def refresh_all_scores(self, period: LeaderboardPeriod = LeaderboardPeriod.ALL_TIME):
        """
        Refresh leaderboard scores from user statistics.
        Useful for initial population or periodic recalculation.
        """
        # Get all users with statistics
        users = self.db.query(User, UserStatistics, UserProfile).join(
            UserStatistics, User.id == UserStatistics.user_id
        ).outerjoin(
            UserProfile, User.id == UserProfile.user_id
        ).all()

        for user, stats, profile in users:
            # Update XP leaderboard
            self.update_user_score(
                user.id,
                ScoreType.XP,
                float(stats.total_points),
                period
            )

            # Update accuracy leaderboard
            self.update_user_score(
                user.id,
                ScoreType.ACCURACY,
                float(stats.overall_accuracy),
                period
            )

            # Update exercises completed leaderboard
            self.update_user_score(
                user.id,
                ScoreType.EXERCISES_COMPLETED,
                float(stats.total_exercises_completed),
                period
            )

            # Update streak leaderboard
            if profile:
                self.update_user_score(
                    user.id,
                    ScoreType.STREAK,
                    float(profile.current_streak),
                    period
                )

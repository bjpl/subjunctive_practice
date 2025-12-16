"""
API routes for leaderboard functionality.
Provides endpoints for rankings, user positions, and competitive features.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from core.database import get_db_session
from core.security import get_current_user
from services.leaderboard_service import LeaderboardService
from models.leaderboard import ScoreType, LeaderboardPeriod
from models.user import User
from schemas.leaderboard import (
    LeaderboardResponse,
    UserRankResponse,
    LeaderboardStatsResponse,
    LeaderboardHistoryResponse
)

router = APIRouter(prefix="/api/leaderboard", tags=["leaderboard"])


@router.get("/{score_type}", response_model=LeaderboardResponse)
def get_leaderboard(
    score_type: ScoreType,
    period: LeaderboardPeriod = Query(default=LeaderboardPeriod.ALL_TIME),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db_session),
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    Get top users on the leaderboard for a specific score type and period.

    Args:
        score_type: Type of score (xp, accuracy, streak, exercises_completed)
        period: Time period (daily, weekly, monthly, all_time)
        limit: Maximum number of entries to return (1-100)
        offset: Number of entries to skip for pagination
        current_user: Currently authenticated user (optional)

    Returns:
        LeaderboardResponse with top entries and metadata
    """
    service = LeaderboardService(db)

    try:
        current_user_id = current_user.id if current_user else None
        leaderboard = service.get_leaderboard(
            score_type=score_type,
            period=period,
            limit=limit,
            offset=offset,
            current_user_id=current_user_id
        )

        return leaderboard

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve leaderboard: {str(e)}"
        )


@router.get("/{score_type}/me", response_model=UserRankResponse)
def get_my_rank(
    score_type: ScoreType,
    period: LeaderboardPeriod = Query(default=LeaderboardPeriod.ALL_TIME),
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get the current user's rank and nearby competitors.

    Args:
        score_type: Type of score
        period: Time period
        current_user: Authenticated user (required)

    Returns:
        UserRankResponse with rank, score, and nearby users
    """
    service = LeaderboardService(db)

    try:
        rank_info = service.get_user_rank(
            user_id=current_user.id,
            score_type=score_type,
            period=period
        )

        if not rank_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User rank not found. Complete some activities to appear on the leaderboard."
            )

        return rank_info

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user rank: {str(e)}"
        )


@router.get("/{score_type}/user/{user_id}", response_model=UserRankResponse)
def get_user_rank(
    score_type: ScoreType,
    user_id: int,
    period: LeaderboardPeriod = Query(default=LeaderboardPeriod.ALL_TIME),
    db: Session = Depends(get_db_session)
):
    """
    Get a specific user's rank and nearby competitors.

    Args:
        score_type: Type of score
        user_id: User identifier
        period: Time period

    Returns:
        UserRankResponse with rank, score, and nearby users
    """
    service = LeaderboardService(db)

    try:
        rank_info = service.get_user_rank(
            user_id=user_id,
            score_type=score_type,
            period=period
        )

        if not rank_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Rank not found for user {user_id}"
            )

        return rank_info

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user rank: {str(e)}"
        )


@router.get("/stats/{score_type}", response_model=LeaderboardStatsResponse)
def get_leaderboard_statistics(
    score_type: ScoreType,
    period: LeaderboardPeriod = Query(default=LeaderboardPeriod.ALL_TIME),
    db: Session = Depends(get_db_session),
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    Get statistical summary of a leaderboard.

    Args:
        score_type: Type of score
        period: Time period
        current_user: Authenticated user (optional, for personalized stats)

    Returns:
        LeaderboardStatsResponse with aggregate statistics
    """
    service = LeaderboardService(db)

    try:
        current_user_id = current_user.id if current_user else None
        stats = service.get_leaderboard_stats(
            score_type=score_type,
            period=period,
            user_id=current_user_id
        )

        return stats

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve leaderboard statistics: {str(e)}"
        )


@router.post("/{score_type}/refresh")
def refresh_leaderboard(
    score_type: ScoreType,
    period: LeaderboardPeriod = Query(default=LeaderboardPeriod.ALL_TIME),
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    """
    Refresh leaderboard scores from current user statistics.
    Typically called by admin users or scheduled tasks.

    Args:
        score_type: Type of score to refresh
        period: Time period
        current_user: Authenticated user (must be admin)

    Returns:
        Success message
    """
    # Check if user is admin (add role check if needed)
    # if current_user.role != UserRole.ADMIN:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Admin access required"
    #     )

    service = LeaderboardService(db)

    try:
        service.refresh_all_scores(period=period)

        return {
            "message": f"Leaderboard refreshed successfully for {score_type.value} ({period.value})",
            "score_type": score_type.value,
            "period": period.value
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to refresh leaderboard: {str(e)}"
        )


@router.post("/{score_type}/snapshot")
def create_leaderboard_snapshot(
    score_type: ScoreType,
    period: LeaderboardPeriod,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    """
    Create a historical snapshot of current leaderboard standings.
    Called at the end of each period (typically automated).

    Args:
        score_type: Type of score
        period: Time period
        current_user: Authenticated user (must be admin)

    Returns:
        Snapshot creation summary
    """
    # Check if user is admin
    # if current_user.role != UserRole.ADMIN:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Admin access required"
    #     )

    service = LeaderboardService(db)

    try:
        snapshot_count = service.create_snapshot(
            score_type=score_type,
            period=period
        )

        return {
            "message": "Snapshot created successfully",
            "score_type": score_type.value,
            "period": period.value,
            "entries_saved": snapshot_count
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create snapshot: {str(e)}"
        )


@router.get("/nearby/{score_type}/me")
def get_my_nearby_users(
    score_type: ScoreType,
    period: LeaderboardPeriod = Query(default=LeaderboardPeriod.ALL_TIME),
    above: int = Query(default=2, ge=0, le=10),
    below: int = Query(default=2, ge=0, le=10),
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get users ranked near the current user.

    Args:
        score_type: Type of score
        period: Time period
        above: Number of higher-ranked users to include
        below: Number of lower-ranked users to include
        current_user: Authenticated user

    Returns:
        List of nearby users with their ranks
    """
    service = LeaderboardService(db)

    try:
        nearby = service.get_nearby_users(
            user_id=current_user.id,
            score_type=score_type,
            period=period,
            above=above,
            below=below
        )

        return {
            "score_type": score_type.value,
            "period": period.value,
            "nearby_users": nearby
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve nearby users: {str(e)}"
        )


@router.get("/all-types/summary")
def get_all_leaderboards_summary(
    period: LeaderboardPeriod = Query(default=LeaderboardPeriod.ALL_TIME),
    db: Session = Depends(get_db_session),
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    Get summary of all leaderboard types for quick overview.

    Args:
        period: Time period
        current_user: Authenticated user (optional)

    Returns:
        Summary of all leaderboard types
    """
    service = LeaderboardService(db)
    current_user_id = current_user.id if current_user else None

    try:
        summaries = {}

        for score_type in ScoreType:
            if current_user_id:
                rank_info = service.get_user_rank(
                    user_id=current_user_id,
                    score_type=score_type,
                    period=period
                )
                summaries[score_type.value] = {
                    "your_rank": rank_info.rank if rank_info else None,
                    "your_score": rank_info.score if rank_info else None,
                    "total_participants": rank_info.total_participants if rank_info else 0,
                    "percentile": rank_info.percentile if rank_info else None
                }
            else:
                stats = service.get_leaderboard_stats(
                    score_type=score_type,
                    period=period
                )
                summaries[score_type.value] = {
                    "total_participants": stats.total_participants,
                    "highest_score": stats.highest_score,
                    "average_score": stats.average_score
                }

        return {
            "period": period.value,
            "leaderboards": summaries
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve leaderboard summary: {str(e)}"
        )

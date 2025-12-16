"""
Admin API routes for system management and monitoring.

Endpoints:
- AI usage tracking and analytics
- System health monitoring
- User management (admin only)
"""

from typing import Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from pathlib import Path

from core.database import get_db
from services.ai_usage_tracker import get_usage_tracker, AIUsageTracker
from models.user import User, UserRole
from api.dependencies.auth import get_current_active_user

router = APIRouter(prefix="/admin", tags=["admin"])


def require_admin(current_user: User = Depends(get_current_active_user)) -> User:
    """
    Dependency to ensure user has admin role.

    Args:
        current_user: Currently authenticated user

    Returns:
        User if admin role

    Raises:
        HTTPException: If user is not admin
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


@router.get("/ai-usage/summary")
async def get_ai_usage_summary(
    start_date: Optional[datetime] = Query(None, description="Start date for usage period"),
    end_date: Optional[datetime] = Query(None, description="End date for usage period"),
    period: Optional[str] = Query("monthly", description="Predefined period: daily, weekly, monthly"),
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin)
):
    """
    Get AI usage summary with cost breakdown.

    Returns aggregated usage statistics including:
    - Total requests and tokens
    - Estimated costs
    - Breakdown by request type
    - User-level statistics

    **Admin only**
    """
    tracker = get_usage_tracker(db)

    # Use predefined period if no dates provided
    if not start_date and not end_date:
        if period == "daily":
            summary = tracker.get_daily_usage()
        elif period == "weekly":
            summary = tracker.get_weekly_usage()
        else:  # monthly (default)
            summary = tracker.get_monthly_usage()
    else:
        summary = tracker.get_usage_summary(start_date=start_date, end_date=end_date)

    return summary.to_dict()


@router.get("/ai-usage/by-user/{user_id}")
async def get_user_ai_usage(
    user_id: int,
    start_date: Optional[datetime] = Query(None, description="Start date for usage period"),
    end_date: Optional[datetime] = Query(None, description="End date for usage period"),
    days: int = Query(30, description="Number of days to look back (default: 30)"),
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin)
):
    """
    Get AI usage statistics for a specific user.

    Returns detailed usage for the specified user including:
    - Total requests and costs
    - Token consumption
    - Request type breakdown
    - Time-based trends

    **Admin only**
    """
    tracker = get_usage_tracker(db)

    # Default to last N days if no dates provided
    if not start_date and not end_date:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

    summary = tracker.get_user_usage(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date
    )

    return summary.to_dict()


@router.get("/ai-usage/budget-alerts")
async def get_budget_alerts(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin)
):
    """
    Get current budget status and alerts.

    Returns:
    - Daily and monthly budget status
    - Current spending
    - Remaining budget
    - Warning flags for approaching limits

    **Admin only**
    """
    tracker = get_usage_tracker(db)
    alerts = tracker.check_budget_alerts()

    return {
        "alerts": alerts,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/ai-usage/projection")
async def get_cost_projection(
    days_ahead: int = Query(30, description="Number of days to project", ge=1, le=365),
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin)
):
    """
    Get projected AI costs based on recent usage patterns.

    Projects future costs using 7-day rolling average.
    Includes confidence level based on data volume.

    **Admin only**
    """
    tracker = get_usage_tracker(db)
    projection = tracker.get_cost_projection(days_ahead=days_ahead)

    return projection


@router.post("/ai-usage/export/json")
async def export_usage_json(
    start_date: Optional[datetime] = Query(None, description="Start date for export"),
    end_date: Optional[datetime] = Query(None, description="End date for export"),
    days: int = Query(30, description="Number of days to export (default: 30)"),
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin)
):
    """
    Export AI usage data to JSON format.

    Downloads aggregated usage summary as JSON file.
    Useful for external analysis and reporting.

    **Admin only**
    """
    from fastapi.responses import FileResponse
    import tempfile

    tracker = get_usage_tracker(db)

    # Default to last N days if no dates provided
    if not start_date and not end_date:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.json',
        delete=False
    )
    temp_path = Path(temp_file.name)
    temp_file.close()

    # Export to file
    tracker.export_to_json(temp_path, start_date=start_date, end_date=end_date)

    # Return as downloadable file
    filename = f"ai_usage_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.json"

    return FileResponse(
        path=str(temp_path),
        media_type='application/json',
        filename=filename
    )


@router.post("/ai-usage/export/csv")
async def export_usage_csv(
    start_date: Optional[datetime] = Query(None, description="Start date for export"),
    end_date: Optional[datetime] = Query(None, description="End date for export"),
    days: int = Query(30, description="Number of days to export (default: 30)"),
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin)
):
    """
    Export AI usage data to CSV format.

    Downloads detailed usage records as CSV file.
    Includes all individual API calls with timestamps.

    **Admin only**
    """
    from fastapi.responses import FileResponse
    import tempfile

    tracker = get_usage_tracker(db)

    # Default to last N days if no dates provided
    if not start_date and not end_date:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.csv',
        delete=False
    )
    temp_path = Path(temp_file.name)
    temp_file.close()

    # Export to file
    tracker.export_to_csv(temp_path, start_date=start_date, end_date=end_date)

    # Return as downloadable file
    filename = f"ai_usage_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv"

    return FileResponse(
        path=str(temp_path),
        media_type='text/csv',
        filename=filename
    )


@router.get("/ai-usage/statistics")
async def get_usage_statistics(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin)
):
    """
    Get comprehensive AI usage statistics.

    Returns:
    - Current day, week, and month summaries
    - Budget status
    - Cost projection
    - Top users by usage

    **Admin only**
    """
    tracker = get_usage_tracker(db)

    # Get multiple time periods
    daily = tracker.get_daily_usage()
    weekly = tracker.get_weekly_usage()
    monthly = tracker.get_monthly_usage()

    # Get budget alerts
    budget = tracker.check_budget_alerts()

    # Get projection
    projection = tracker.get_cost_projection(days_ahead=30)

    return {
        "daily": daily.to_dict(),
        "weekly": weekly.to_dict(),
        "monthly": monthly.to_dict(),
        "budget_alerts": budget,
        "projection_30_days": projection,
        "timestamp": datetime.utcnow().isoformat()
    }

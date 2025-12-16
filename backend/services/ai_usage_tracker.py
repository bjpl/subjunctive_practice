"""
AI Usage Tracker for monitoring token consumption and costs.

This module provides comprehensive tracking of Claude API usage:
- Token consumption (input/output) per request
- Cost estimation based on current pricing
- Usage aggregation by user, time period, and request type
- Budget alerts and thresholds
- Export capabilities for analysis

Pricing (as of 2025):
- Claude 3.5 Sonnet: $3/M input tokens, $15/M output tokens
"""

from typing import Dict, List, Optional, Any, Literal
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import json
import csv
from pathlib import Path
import structlog
from sqlalchemy.orm import Session
from sqlalchemy import func

logger = structlog.get_logger(__name__)


class RequestType(str, Enum):
    """Types of AI requests for categorization."""
    FEEDBACK = "feedback"
    INSIGHTS = "insights"
    HINT = "hint"
    HEALTH_CHECK = "health_check"
    OTHER = "other"


@dataclass
class UsageRecord:
    """Individual usage record for a single API call."""
    request_type: str
    input_tokens: int
    output_tokens: int
    estimated_cost: float
    user_id: Optional[int] = None
    timestamp: datetime = None
    model: str = "claude-3-5-sonnet-20241022"

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()

    @property
    def total_tokens(self) -> int:
        """Total tokens (input + output)."""
        return self.input_tokens + self.output_tokens


@dataclass
class UsageSummary:
    """Aggregated usage statistics."""
    total_requests: int
    total_input_tokens: int
    total_output_tokens: int
    total_cost: float
    period_start: datetime
    period_end: datetime
    by_request_type: Dict[str, Dict[str, Any]]
    by_user: Optional[Dict[int, Dict[str, Any]]] = None

    @property
    def total_tokens(self) -> int:
        """Total tokens across all requests."""
        return self.total_input_tokens + self.total_output_tokens

    @property
    def average_cost_per_request(self) -> float:
        """Average cost per request."""
        return self.total_cost / self.total_requests if self.total_requests > 0 else 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "total_requests": self.total_requests,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_tokens,
            "total_cost": round(self.total_cost, 4),
            "average_cost_per_request": round(self.average_cost_per_request, 4),
            "period_start": self.period_start.isoformat(),
            "period_end": self.period_end.isoformat(),
            "by_request_type": self.by_request_type,
            "by_user": self.by_user
        }


class AIUsageTracker:
    """
    Tracks and analyzes AI API usage with cost estimation.

    Features:
    - Token counting and cost estimation
    - Usage aggregation by time period, user, request type
    - Budget alerts and thresholds
    - Export to JSON/CSV for analysis
    - Database persistence via SQLAlchemy

    Pricing Model (Claude 3.5 Sonnet):
    - Input: $3 per million tokens
    - Output: $15 per million tokens
    """

    # Pricing per million tokens (in USD)
    INPUT_PRICE_PER_MILLION = 3.0
    OUTPUT_PRICE_PER_MILLION = 15.0

    # Budget thresholds (in USD)
    DEFAULT_DAILY_BUDGET = 10.0
    DEFAULT_MONTHLY_BUDGET = 200.0

    def __init__(
        self,
        db_session: Optional[Session] = None,
        daily_budget: float = DEFAULT_DAILY_BUDGET,
        monthly_budget: float = DEFAULT_MONTHLY_BUDGET
    ):
        """
        Initialize the usage tracker.

        Args:
            db_session: SQLAlchemy database session for persistence
            daily_budget: Daily spending limit in USD
            monthly_budget: Monthly spending limit in USD
        """
        self.db = db_session
        self.daily_budget = daily_budget
        self.monthly_budget = monthly_budget

    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Calculate the cost for a given number of tokens.

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens

        Returns:
            Estimated cost in USD
        """
        input_cost = (input_tokens / 1_000_000) * self.INPUT_PRICE_PER_MILLION
        output_cost = (output_tokens / 1_000_000) * self.OUTPUT_PRICE_PER_MILLION
        return input_cost + output_cost

    def track_usage(
        self,
        request_type: RequestType,
        input_tokens: int,
        output_tokens: int,
        user_id: Optional[int] = None,
        model: str = "claude-3-5-sonnet-20241022"
    ) -> UsageRecord:
        """
        Track a single API usage event.

        Args:
            request_type: Type of request (feedback, insights, hint, etc.)
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            user_id: Optional user ID for user-specific tracking
            model: Model identifier

        Returns:
            UsageRecord with calculated cost
        """
        cost = self.calculate_cost(input_tokens, output_tokens)

        record = UsageRecord(
            request_type=request_type.value,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            estimated_cost=cost,
            user_id=user_id,
            model=model
        )

        # Persist to database if session available
        if self.db:
            self._save_to_db(record)

        logger.info(
            "ai_usage_tracked",
            request_type=request_type.value,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost=round(cost, 4),
            user_id=user_id
        )

        return record

    def _save_to_db(self, record: UsageRecord) -> None:
        """Save usage record to database."""
        from models.ai_usage import AIUsageRecord

        db_record = AIUsageRecord(
            user_id=record.user_id,
            request_type=record.request_type,
            input_tokens=record.input_tokens,
            output_tokens=record.output_tokens,
            estimated_cost=record.estimated_cost,
            model=record.model,
            created_at=record.timestamp
        )

        self.db.add(db_record)
        self.db.commit()

    def get_usage_summary(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        user_id: Optional[int] = None,
        request_type: Optional[RequestType] = None
    ) -> UsageSummary:
        """
        Get aggregated usage summary for a time period.

        Args:
            start_date: Start of period (defaults to 30 days ago)
            end_date: End of period (defaults to now)
            user_id: Filter by specific user
            request_type: Filter by request type

        Returns:
            UsageSummary with aggregated statistics
        """
        if not self.db:
            raise ValueError("Database session required for usage summary")

        from models.ai_usage import AIUsageRecord

        # Default to last 30 days
        if end_date is None:
            end_date = datetime.utcnow()
        if start_date is None:
            start_date = end_date - timedelta(days=30)

        # Build query
        query = self.db.query(AIUsageRecord).filter(
            AIUsageRecord.created_at >= start_date,
            AIUsageRecord.created_at <= end_date
        )

        if user_id:
            query = query.filter(AIUsageRecord.user_id == user_id)
        if request_type:
            query = query.filter(AIUsageRecord.request_type == request_type.value)

        records = query.all()

        # Aggregate data
        total_requests = len(records)
        total_input_tokens = sum(r.input_tokens for r in records)
        total_output_tokens = sum(r.output_tokens for r in records)
        total_cost = sum(r.estimated_cost for r in records)

        # Group by request type
        by_request_type = {}
        for record in records:
            rt = record.request_type
            if rt not in by_request_type:
                by_request_type[rt] = {
                    "count": 0,
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "cost": 0.0
                }

            by_request_type[rt]["count"] += 1
            by_request_type[rt]["input_tokens"] += record.input_tokens
            by_request_type[rt]["output_tokens"] += record.output_tokens
            by_request_type[rt]["cost"] += record.estimated_cost

        # Round costs
        for rt in by_request_type:
            by_request_type[rt]["cost"] = round(by_request_type[rt]["cost"], 4)

        # Group by user if not filtering by user
        by_user = None
        if not user_id:
            by_user = {}
            for record in records:
                uid = record.user_id or 0  # 0 for anonymous
                if uid not in by_user:
                    by_user[uid] = {
                        "count": 0,
                        "input_tokens": 0,
                        "output_tokens": 0,
                        "cost": 0.0
                    }

                by_user[uid]["count"] += 1
                by_user[uid]["input_tokens"] += record.input_tokens
                by_user[uid]["output_tokens"] += record.output_tokens
                by_user[uid]["cost"] += record.estimated_cost

            # Round costs
            for uid in by_user:
                by_user[uid]["cost"] = round(by_user[uid]["cost"], 4)

        return UsageSummary(
            total_requests=total_requests,
            total_input_tokens=total_input_tokens,
            total_output_tokens=total_output_tokens,
            total_cost=total_cost,
            period_start=start_date,
            period_end=end_date,
            by_request_type=by_request_type,
            by_user=by_user
        )

    def get_daily_usage(self, date: Optional[datetime] = None) -> UsageSummary:
        """Get usage summary for a specific day."""
        if date is None:
            date = datetime.utcnow()

        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        return self.get_usage_summary(start_date=start_of_day, end_date=end_of_day)

    def get_weekly_usage(self, date: Optional[datetime] = None) -> UsageSummary:
        """Get usage summary for a week (last 7 days)."""
        if date is None:
            date = datetime.utcnow()

        end_date = date
        start_date = date - timedelta(days=7)

        return self.get_usage_summary(start_date=start_date, end_date=end_date)

    def get_monthly_usage(self, date: Optional[datetime] = None) -> UsageSummary:
        """Get usage summary for a month (last 30 days)."""
        if date is None:
            date = datetime.utcnow()

        end_date = date
        start_date = date - timedelta(days=30)

        return self.get_usage_summary(start_date=start_date, end_date=end_date)

    def get_user_usage(
        self,
        user_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> UsageSummary:
        """Get usage summary for a specific user."""
        return self.get_usage_summary(
            start_date=start_date,
            end_date=end_date,
            user_id=user_id
        )

    def check_budget_alerts(self) -> Dict[str, Any]:
        """
        Check if usage is approaching or exceeding budget limits.

        Returns:
            Dictionary with alert status and details
        """
        daily_usage = self.get_daily_usage()
        monthly_usage = self.get_monthly_usage()

        alerts = {
            "daily": {
                "budget": self.daily_budget,
                "spent": round(daily_usage.total_cost, 2),
                "remaining": round(self.daily_budget - daily_usage.total_cost, 2),
                "percentage": round((daily_usage.total_cost / self.daily_budget) * 100, 1) if self.daily_budget > 0 else 0,
                "exceeded": daily_usage.total_cost > self.daily_budget,
                "warning": daily_usage.total_cost > (self.daily_budget * 0.8)
            },
            "monthly": {
                "budget": self.monthly_budget,
                "spent": round(monthly_usage.total_cost, 2),
                "remaining": round(self.monthly_budget - monthly_usage.total_cost, 2),
                "percentage": round((monthly_usage.total_cost / self.monthly_budget) * 100, 1) if self.monthly_budget > 0 else 0,
                "exceeded": monthly_usage.total_cost > self.monthly_budget,
                "warning": monthly_usage.total_cost > (self.monthly_budget * 0.8)
            }
        }

        # Log warnings
        if alerts["daily"]["exceeded"]:
            logger.warning("daily_budget_exceeded", spent=alerts["daily"]["spent"], budget=self.daily_budget)
        elif alerts["daily"]["warning"]:
            logger.warning("daily_budget_warning", spent=alerts["daily"]["spent"], budget=self.daily_budget)

        if alerts["monthly"]["exceeded"]:
            logger.warning("monthly_budget_exceeded", spent=alerts["monthly"]["spent"], budget=self.monthly_budget)
        elif alerts["monthly"]["warning"]:
            logger.warning("monthly_budget_warning", spent=alerts["monthly"]["spent"], budget=self.monthly_budget)

        return alerts

    def export_to_json(
        self,
        filepath: Path,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> None:
        """
        Export usage data to JSON file.

        Args:
            filepath: Path to output JSON file
            start_date: Start of period
            end_date: End of period
        """
        summary = self.get_usage_summary(start_date=start_date, end_date=end_date)

        with open(filepath, 'w') as f:
            json.dump(summary.to_dict(), f, indent=2)

        logger.info("usage_exported_json", filepath=str(filepath))

    def export_to_csv(
        self,
        filepath: Path,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> None:
        """
        Export detailed usage records to CSV file.

        Args:
            filepath: Path to output CSV file
            start_date: Start of period
            end_date: End of period
        """
        if not self.db:
            raise ValueError("Database session required for CSV export")

        from models.ai_usage import AIUsageRecord

        # Default to last 30 days
        if end_date is None:
            end_date = datetime.utcnow()
        if start_date is None:
            start_date = end_date - timedelta(days=30)

        records = self.db.query(AIUsageRecord).filter(
            AIUsageRecord.created_at >= start_date,
            AIUsageRecord.created_at <= end_date
        ).order_by(AIUsageRecord.created_at).all()

        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'id', 'user_id', 'request_type', 'input_tokens', 'output_tokens',
                'total_tokens', 'estimated_cost', 'model', 'created_at'
            ])

            for record in records:
                writer.writerow([
                    record.id,
                    record.user_id or '',
                    record.request_type,
                    record.input_tokens,
                    record.output_tokens,
                    record.input_tokens + record.output_tokens,
                    round(record.estimated_cost, 4),
                    record.model,
                    record.created_at.isoformat()
                ])

        logger.info("usage_exported_csv", filepath=str(filepath), records=len(records))

    def get_cost_projection(self, days_ahead: int = 30) -> Dict[str, Any]:
        """
        Project future costs based on recent usage patterns.

        Args:
            days_ahead: Number of days to project forward

        Returns:
            Dictionary with projected costs
        """
        # Get last 7 days of usage
        weekly_usage = self.get_weekly_usage()

        if weekly_usage.total_requests == 0:
            return {
                "projection_days": days_ahead,
                "projected_cost": 0.0,
                "daily_average": 0.0,
                "confidence": "low"
            }

        # Calculate daily average
        daily_average = weekly_usage.total_cost / 7
        projected_cost = daily_average * days_ahead

        # Determine confidence based on request consistency
        confidence = "high" if weekly_usage.total_requests > 50 else "medium" if weekly_usage.total_requests > 20 else "low"

        return {
            "projection_days": days_ahead,
            "projected_cost": round(projected_cost, 2),
            "daily_average": round(daily_average, 2),
            "confidence": confidence,
            "based_on_requests": weekly_usage.total_requests
        }


# Global tracker instance
_usage_tracker: Optional[AIUsageTracker] = None


def get_usage_tracker(db: Session) -> AIUsageTracker:
    """
    Get or create the global usage tracker instance.

    Args:
        db: Database session

    Returns:
        AIUsageTracker instance
    """
    global _usage_tracker
    if _usage_tracker is None or _usage_tracker.db != db:
        _usage_tracker = AIUsageTracker(db_session=db)
    return _usage_tracker

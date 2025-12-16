"""
Tests for AI Usage Tracker functionality.

Tests include:
- Token counting and cost calculation
- Usage tracking and persistence
- Aggregation by time period, user, request type
- Budget alerts and thresholds
- Export to JSON/CSV
- Cost projections
"""

import pytest
from datetime import datetime, timedelta
from pathlib import Path
import json
import csv
from sqlalchemy.orm import Session

from services.ai_usage_tracker import AIUsageTracker, RequestType, UsageRecord, UsageSummary
from models.ai_usage import AIUsageRecord
from models.user import User, UserRole


class TestUsageTracking:
    """Test basic usage tracking functionality."""

    def test_calculate_cost(self, db: Session):
        """Test cost calculation for different token amounts."""
        tracker = AIUsageTracker(db_session=db)

        # Claude 3.5 Sonnet pricing: $3/M input, $15/M output
        # Test 1000 input tokens, 500 output tokens
        cost = tracker.calculate_cost(1000, 500)
        expected = (1000 / 1_000_000 * 3.0) + (500 / 1_000_000 * 15.0)
        assert abs(cost - expected) < 0.0001

        # Test larger amounts
        cost = tracker.calculate_cost(10000, 5000)
        expected = (10000 / 1_000_000 * 3.0) + (5000 / 1_000_000 * 15.0)
        assert abs(cost - expected) < 0.0001

    def test_track_usage_without_user(self, db: Session):
        """Test tracking usage without user association."""
        tracker = AIUsageTracker(db_session=db)

        record = tracker.track_usage(
            request_type=RequestType.FEEDBACK,
            input_tokens=500,
            output_tokens=200,
            user_id=None
        )

        assert record.request_type == RequestType.FEEDBACK.value
        assert record.input_tokens == 500
        assert record.output_tokens == 200
        assert record.total_tokens == 700
        assert record.user_id is None
        assert record.estimated_cost > 0

        # Verify it was saved to database
        db_record = db.query(AIUsageRecord).filter(
            AIUsageRecord.request_type == RequestType.FEEDBACK.value
        ).first()
        assert db_record is not None
        assert db_record.input_tokens == 500

    def test_track_usage_with_user(self, db: Session, test_user: User):
        """Test tracking usage with user association."""
        tracker = AIUsageTracker(db_session=db)

        record = tracker.track_usage(
            request_type=RequestType.HINT,
            input_tokens=300,
            output_tokens=150,
            user_id=test_user.id
        )

        assert record.user_id == test_user.id

        # Verify database record
        db_record = db.query(AIUsageRecord).filter(
            AIUsageRecord.user_id == test_user.id
        ).first()
        assert db_record is not None
        assert db_record.user_id == test_user.id


class TestUsageSummary:
    """Test usage summary and aggregation."""

    @pytest.fixture
    def usage_data(self, db: Session, test_user: User):
        """Create test usage data."""
        tracker = AIUsageTracker(db_session=db)

        # Create multiple usage records
        tracker.track_usage(RequestType.FEEDBACK, 1000, 500, test_user.id)
        tracker.track_usage(RequestType.FEEDBACK, 800, 400, test_user.id)
        tracker.track_usage(RequestType.HINT, 300, 150, test_user.id)
        tracker.track_usage(RequestType.INSIGHTS, 2000, 1000, test_user.id)

        return tracker

    def test_get_usage_summary(self, db: Session, usage_data: AIUsageTracker):
        """Test getting usage summary."""
        summary = usage_data.get_usage_summary()

        assert summary.total_requests == 4
        assert summary.total_input_tokens == 4100
        assert summary.total_output_tokens == 2050
        assert summary.total_tokens == 6150
        assert summary.total_cost > 0

        # Check request type breakdown
        assert "feedback" in summary.by_request_type
        assert summary.by_request_type["feedback"]["count"] == 2
        assert "hint" in summary.by_request_type
        assert summary.by_request_type["hint"]["count"] == 1

    def test_get_daily_usage(self, db: Session, usage_data: AIUsageTracker):
        """Test daily usage summary."""
        daily = usage_data.get_daily_usage()

        assert daily.total_requests == 4
        assert (daily.period_end - daily.period_start).days == 1

    def test_get_weekly_usage(self, db: Session, usage_data: AIUsageTracker):
        """Test weekly usage summary."""
        weekly = usage_data.get_weekly_usage()

        assert weekly.total_requests == 4
        assert (weekly.period_end - weekly.period_start).days == 7

    def test_get_monthly_usage(self, db: Session, usage_data: AIUsageTracker):
        """Test monthly usage summary."""
        monthly = usage_data.get_monthly_usage()

        assert monthly.total_requests == 4
        assert (monthly.period_end - monthly.period_start).days == 30

    def test_get_user_usage(self, db: Session, test_user: User, usage_data: AIUsageTracker):
        """Test user-specific usage summary."""
        user_summary = usage_data.get_user_usage(test_user.id)

        assert user_summary.total_requests == 4
        assert user_summary.total_cost > 0


class TestBudgetAlerts:
    """Test budget monitoring and alerts."""

    def test_budget_alerts_under_limit(self, db: Session):
        """Test budget alerts when under limit."""
        tracker = AIUsageTracker(db_session=db, daily_budget=10.0, monthly_budget=200.0)

        # Add minimal usage
        tracker.track_usage(RequestType.FEEDBACK, 100, 50, user_id=None)

        alerts = tracker.check_budget_alerts()

        assert not alerts["daily"]["exceeded"]
        assert not alerts["daily"]["warning"]
        assert alerts["daily"]["remaining"] > 0

    def test_budget_alerts_warning(self, db: Session):
        """Test budget warning at 80% threshold."""
        tracker = AIUsageTracker(db_session=db, daily_budget=0.01, monthly_budget=0.1)

        # Add usage to trigger warning (80% of daily budget)
        # Need approximately $0.008 worth of tokens
        # $3/M input + $15/M output
        # Use ~2000 output tokens to get close to $0.008
        tracker.track_usage(RequestType.FEEDBACK, 500, 2000, user_id=None)

        alerts = tracker.check_budget_alerts()

        assert alerts["daily"]["warning"] or alerts["daily"]["exceeded"]

    def test_budget_alerts_exceeded(self, db: Session):
        """Test budget exceeded alert."""
        tracker = AIUsageTracker(db_session=db, daily_budget=0.001, monthly_budget=0.01)

        # Add usage to exceed budget
        tracker.track_usage(RequestType.INSIGHTS, 1000, 5000, user_id=None)

        alerts = tracker.check_budget_alerts()

        assert alerts["daily"]["exceeded"]
        assert alerts["daily"]["spent"] > alerts["daily"]["budget"]


class TestExportFunctionality:
    """Test data export features."""

    def test_export_to_json(self, db: Session, test_user: User, tmp_path: Path):
        """Test JSON export."""
        tracker = AIUsageTracker(db_session=db)

        # Create test data
        tracker.track_usage(RequestType.FEEDBACK, 1000, 500, test_user.id)
        tracker.track_usage(RequestType.HINT, 300, 150, test_user.id)

        # Export to JSON
        json_file = tmp_path / "usage.json"
        tracker.export_to_json(json_file)

        # Verify file exists and contains valid JSON
        assert json_file.exists()

        with open(json_file) as f:
            data = json.load(f)

        assert "total_requests" in data
        assert data["total_requests"] == 2
        assert "by_request_type" in data

    def test_export_to_csv(self, db: Session, test_user: User, tmp_path: Path):
        """Test CSV export."""
        tracker = AIUsageTracker(db_session=db)

        # Create test data
        tracker.track_usage(RequestType.FEEDBACK, 1000, 500, test_user.id)
        tracker.track_usage(RequestType.HINT, 300, 150, test_user.id)

        # Export to CSV
        csv_file = tmp_path / "usage.csv"
        tracker.export_to_csv(csv_file)

        # Verify file exists and contains valid CSV
        assert csv_file.exists()

        with open(csv_file, newline='') as f:
            reader = csv.reader(f)
            rows = list(reader)

        # Should have header + 2 data rows
        assert len(rows) == 3
        assert rows[0][0] == 'id'  # Header row


class TestCostProjection:
    """Test cost projection functionality."""

    def test_cost_projection_with_data(self, db: Session):
        """Test cost projection based on recent usage."""
        tracker = AIUsageTracker(db_session=db)

        # Create consistent usage pattern
        for _ in range(10):
            tracker.track_usage(RequestType.FEEDBACK, 1000, 500, user_id=None)

        projection = tracker.get_cost_projection(days_ahead=30)

        assert projection["projection_days"] == 30
        assert projection["projected_cost"] > 0
        assert projection["daily_average"] > 0
        assert projection["confidence"] in ["low", "medium", "high"]

    def test_cost_projection_no_data(self, db: Session):
        """Test cost projection with no usage data."""
        tracker = AIUsageTracker(db_session=db)

        projection = tracker.get_cost_projection(days_ahead=30)

        assert projection["projected_cost"] == 0.0
        assert projection["confidence"] == "low"


@pytest.fixture
def test_user(db: Session) -> User:
    """Create a test user."""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed",
        role=UserRole.STUDENT
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def db() -> Session:
    """Database session fixture (placeholder)."""
    # In actual tests, this would provide a test database session
    # For now, this is a placeholder
    pass

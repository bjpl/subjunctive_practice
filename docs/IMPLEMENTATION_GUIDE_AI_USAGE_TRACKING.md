# AI Usage Tracking Implementation Guide

Complete implementation guide for adding token counting and cost tracking to the AI service.

## Overview

This implementation adds comprehensive AI usage tracking including:
- Token consumption monitoring (input/output)
- Real-time cost estimation (Claude 3.5 Sonnet pricing)
- Usage aggregation (daily/weekly/monthly)
- Budget alerts and thresholds
- User-level analytics
- Export capabilities (JSON/CSV)
- Admin API endpoints

## Files Created

### 1. Core Tracking Module
**Location:** `backend/services/ai_usage_tracker.py`

Complete usage tracking system with:
- `AIUsageTracker` class for tracking and analytics
- Token counting and cost calculation
- Aggregation methods (daily, weekly, monthly)
- Budget alert system
- Export to JSON/CSV

### 2. Database Model
**Location:** `backend/models/ai_usage.py`

SQLAlchemy model for persisting usage records:
- `AIUsageRecord` model with all fields
- Relationship to User model
- Optimized indexes for queries

### 3. Database Migration
**Location:** `backend/alembic/versions/add_ai_usage_tracking.py`

Alembic migration to create:
- `ai_usage_records` table
- All necessary indexes
- Foreign key constraints

### 4. Admin API Routes
**Location:** `backend/api/routes/admin.py`

RESTful API endpoints for:
- Usage summaries (`GET /admin/ai-usage/summary`)
- User-specific usage (`GET /admin/ai-usage/by-user/{user_id}`)
- Budget alerts (`GET /admin/ai-usage/budget-alerts`)
- Cost projection (`GET /admin/ai-usage/projection`)
- JSON export (`POST /admin/ai-usage/export/json`)
- CSV export (`POST /admin/ai-usage/export/csv`)

### 5. Updated AI Service
**Location:** `backend/services/ai_service_updated.py`

Enhanced AI service with:
- Integrated usage tracking on all API calls
- Automatic token extraction
- User ID tracking for analytics

### 6. Authentication Dependencies
**Location:** `backend/api/dependencies/auth.py`

Authentication utilities for admin routes:
- `get_current_user`
- `get_current_active_user`
- `get_current_admin_user`

### 7. Tests
**Location:** `backend/tests/test_ai_usage_tracker.py`

Comprehensive test suite covering:
- Cost calculation
- Usage tracking and persistence
- Aggregation methods
- Budget alerts
- Export functionality
- Cost projections

### 8. Documentation
**Location:** `docs/AI_USAGE_TRACKING.md`

Complete documentation including:
- Architecture overview
- Usage examples
- API reference
- Database schema
- Best practices

## Installation Steps

### Step 1: Apply Updated AI Service

The updated AI service integrates usage tracking. Replace the current file:

```bash
# Backup current ai_service.py
cp backend/services/ai_service.py backend/services/ai_service.py.backup

# Apply updated version
mv backend/services/ai_service_updated.py backend/services/ai_service.py
```

**IMPORTANT:** The updated service integrates with your existing cache service. Review the changes:

```python
# New imports added
from sqlalchemy.orm import Session
from services.ai_usage_tracker import AIUsageTracker, RequestType

# Modified __init__ to accept db session
def __init__(self, cache_service: Optional[RedisCache] = None, db: Optional[Session] = None):
    # ... existing code ...
    self._usage_tracker = AIUsageTracker(db_session=db) if db else None

# Modified _create_message to track usage
async def _create_message(
    self,
    prompt: str,
    # ... existing params ...
    request_type: RequestType = RequestType.OTHER,
    user_id: Optional[int] = None
) -> str:
    # ... API call code ...

    # NEW: Track usage if tracker available
    if self._usage_tracker and response.usage:
        self._usage_tracker.track_usage(
            request_type=request_type,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            user_id=user_id,
            model=params["model"]
        )
```

### Step 2: Update Models

The User model needs a new relationship. Update `backend/models/user.py`:

```python
# Add this to the User model's relationships section:
ai_usage_records = relationship("AIUsageRecord", back_populates="user", cascade="all, delete-orphan")
```

Update `backend/models/__init__.py`:

```python
from .ai_usage import (
    AIUsageRecord,
)

# Add to __all__:
"AIUsageRecord",
```

### Step 3: Run Database Migration

```bash
# Run the migration to create ai_usage_records table
cd backend
alembic upgrade head
```

This creates:
- `ai_usage_records` table
- All indexes for efficient querying
- Foreign key to users table

### Step 4: Register Admin Routes

Add the admin routes to your FastAPI application:

```python
# In backend/main.py or wherever you register routes
from api.routes import admin

app.include_router(
    admin.router,
    prefix="/api",
    tags=["admin"]
)
```

### Step 5: Update Service Initialization

Update how you initialize the AI service to pass the database session:

```python
# In your FastAPI dependency or startup
from core.database import get_db

def get_ai_service_with_tracking(db: Session = Depends(get_db)):
    return get_ai_service(db=db)
```

### Step 6: Configure Budget Thresholds (Optional)

Default budgets are:
- Daily: $10.00
- Monthly: $200.00

To customize, modify `backend/services/ai_usage_tracker.py`:

```python
DEFAULT_DAILY_BUDGET = 10.0  # Your daily budget
DEFAULT_MONTHLY_BUDGET = 200.0  # Your monthly budget
```

## Usage Examples

### Basic Usage in Routes

```python
from fastapi import APIRouter, Depends
from services.ai_service import get_ai_service
from core.database import get_db

router = APIRouter()

@router.post("/feedback")
async def generate_feedback(
    user_answer: str,
    correct_answer: str,
    exercise_context: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # AI service now has usage tracking enabled
    ai_service = get_ai_service(db=db)

    # Usage is tracked automatically with user_id
    feedback = await ai_service.generate_feedback(
        user_answer=user_answer,
        correct_answer=correct_answer,
        exercise_context=exercise_context,
        user_id=current_user.id  # Track usage for this user
    )

    return {"feedback": feedback}
```

### Check Budget Status

```python
from services.ai_usage_tracker import get_usage_tracker

@router.get("/admin/budget-status")
async def get_budget_status(db: Session = Depends(get_db)):
    tracker = get_usage_tracker(db)
    alerts = tracker.check_budget_alerts()

    return {
        "daily_spent": alerts["daily"]["spent"],
        "daily_budget": alerts["daily"]["budget"],
        "daily_remaining": alerts["daily"]["remaining"],
        "daily_exceeded": alerts["daily"]["exceeded"],
        "daily_warning": alerts["daily"]["warning"]
    }
```

### Get Usage Summary

```python
@router.get("/admin/usage-summary")
async def get_usage_summary(
    period: str = "monthly",
    db: Session = Depends(get_db)
):
    tracker = get_usage_tracker(db)

    if period == "daily":
        summary = tracker.get_daily_usage()
    elif period == "weekly":
        summary = tracker.get_weekly_usage()
    else:
        summary = tracker.get_monthly_usage()

    return summary.to_dict()
```

## Testing

Run the test suite:

```bash
# Run AI usage tracking tests
pytest backend/tests/test_ai_usage_tracker.py -v

# Run with coverage
pytest backend/tests/test_ai_usage_tracker.py --cov=services.ai_usage_tracker --cov-report=html
```

## Monitoring

### Daily Monitoring Script

Create a simple monitoring script:

```python
# scripts/check_ai_usage.py
import asyncio
from sqlalchemy.orm import Session
from core.database import SessionLocal
from services.ai_usage_tracker import get_usage_tracker

async def main():
    db = SessionLocal()
    try:
        tracker = get_usage_tracker(db)

        # Get daily summary
        daily = tracker.get_daily_usage()
        print(f"Today's Usage:")
        print(f"  Requests: {daily.total_requests}")
        print(f"  Tokens: {daily.total_tokens:,}")
        print(f"  Cost: ${daily.total_cost:.2f}")

        # Check budgets
        alerts = tracker.check_budget_alerts()
        if alerts["daily"]["exceeded"]:
            print("\n⚠️  ALERT: Daily budget exceeded!")
        elif alerts["daily"]["warning"]:
            print("\n⚠️  WARNING: 80% of daily budget used")

        print(f"\nDaily Budget: ${alerts['daily']['spent']:.2f} / ${alerts['daily']['budget']:.2f}")
        print(f"Monthly Budget: ${alerts['monthly']['spent']:.2f} / ${alerts['monthly']['budget']:.2f}")

    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
python scripts/check_ai_usage.py
```

## API Examples

### Get Usage Summary

```bash
curl -X GET "http://localhost:8000/api/admin/ai-usage/summary?period=daily" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

### Get User Usage

```bash
curl -X GET "http://localhost:8000/api/admin/ai-usage/by-user/123?days=30" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

### Check Budget Alerts

```bash
curl -X GET "http://localhost:8000/api/admin/ai-usage/budget-alerts" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

### Export to CSV

```bash
curl -X POST "http://localhost:8000/api/admin/ai-usage/export/csv?days=30" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -O "usage_export.csv"
```

## Troubleshooting

### Issue: Usage not being tracked

**Solution:**
1. Verify database session is passed to AI service
2. Check that migration ran successfully: `alembic current`
3. Verify usage_tracker is initialized: Check logs for "usage_tracking_enabled"

### Issue: Budget alerts not working

**Solution:**
1. Ensure budget thresholds are set appropriately
2. Check that usage is being recorded in database
3. Review alert calculation logic in logs

### Issue: Export fails

**Solution:**
1. Verify write permissions for export directory
2. Check database connection is active
3. Ensure sufficient disk space

### Issue: High costs

**Solution:**
1. Review usage by request type: Identify expensive operations
2. Check token counts: May need to optimize prompts
3. Implement caching: Reduce duplicate requests
4. Set max_tokens limits: Prevent runaway generations

## Performance Considerations

### Database Indexes

The migration creates optimized indexes:
- `idx_user_date`: User + date queries
- `idx_type_date`: Request type + date queries
- `idx_date_cost`: Date + cost queries

These indexes support efficient:
- User usage summaries
- Request type analysis
- Time-based aggregations
- Budget calculations

### Query Optimization

For large datasets:

```python
# Use date ranges to limit query scope
summary = tracker.get_usage_summary(
    start_date=datetime.now() - timedelta(days=7),
    end_date=datetime.now()
)

# Filter by user to reduce result set
user_summary = tracker.get_user_usage(
    user_id=123,
    start_date=recent_date
)
```

## Security Considerations

1. **Admin-Only Access**: All usage endpoints require admin role
2. **User Privacy**: Individual user data only accessible to admins
3. **Cost Data**: Sensitive financial information protected
4. **Export Safety**: Temporary files cleaned up after download

## Next Steps

1. Set up automated budget alerts (email/Slack)
2. Create usage dashboard visualization
3. Implement per-user budget limits
4. Add cost optimization recommendations
5. Integrate with billing system

## Support

For questions or issues:
1. Check documentation: `docs/AI_USAGE_TRACKING.md`
2. Review test examples: `backend/tests/test_ai_usage_tracker.py`
3. Check logs for tracking errors
4. Review database records directly

## Summary

This implementation provides comprehensive AI usage tracking with:
- ✅ Token counting and cost estimation
- ✅ Real-time budget monitoring
- ✅ User-level analytics
- ✅ Export capabilities
- ✅ Admin API endpoints
- ✅ Database persistence
- ✅ Comprehensive tests
- ✅ Full documentation

The system automatically tracks all Claude API calls and provides detailed analytics for cost optimization and budgeting.

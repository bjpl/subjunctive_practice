# AI Usage Tracking & Cost Monitoring

Comprehensive token counting and cost tracking system for Claude API usage.

## Overview

The AI usage tracking system monitors and analyzes all Claude API calls, providing:

- **Token Consumption Tracking**: Input and output tokens per request
- **Cost Estimation**: Real-time cost calculation based on Claude 3.5 Sonnet pricing
- **Usage Aggregation**: Daily, weekly, and monthly summaries
- **Budget Alerts**: Configurable thresholds with warning system
- **User-Level Analytics**: Track usage per user
- **Export Capabilities**: JSON and CSV export for external analysis
- **Cost Projections**: Forecast future spending based on usage patterns

## Architecture

### Components

1. **AIUsageTracker** (`backend/services/ai_usage_tracker.py`)
   - Core tracking and analytics engine
   - Cost calculation and aggregation
   - Budget monitoring

2. **AIUsageRecord** (`backend/models/ai_usage.py`)
   - SQLAlchemy model for database persistence
   - Indexed for efficient querying

3. **Admin API** (`backend/api/routes/admin.py`)
   - REST endpoints for usage analytics
   - Export functionality
   - Budget status monitoring

4. **Enhanced AI Service** (`backend/services/ai_service.py`)
   - Integrated usage tracking on all API calls
   - Automatic token extraction from responses

## Pricing Model

**Claude 3.5 Sonnet (as of 2025):**
- Input tokens: $3.00 per million tokens
- Output tokens: $15.00 per million tokens

### Cost Calculation Formula

```python
input_cost = (input_tokens / 1_000_000) * 3.0
output_cost = (output_tokens / 1_000_000) * 15.0
total_cost = input_cost + output_cost
```

## Usage

### Basic Tracking

```python
from services.ai_usage_tracker import AIUsageTracker, RequestType
from core.database import get_db

# Initialize tracker
tracker = AIUsageTracker(db_session=get_db())

# Track a usage event
record = tracker.track_usage(
    request_type=RequestType.FEEDBACK,
    input_tokens=500,
    output_tokens=200,
    user_id=123  # Optional
)

print(f"Cost: ${record.estimated_cost:.4f}")
```

### Get Usage Summary

```python
# Get daily summary
daily = tracker.get_daily_usage()
print(f"Today: {daily.total_requests} requests, ${daily.total_cost:.2f}")

# Get weekly summary
weekly = tracker.get_weekly_usage()

# Get monthly summary
monthly = tracker.get_monthly_usage()

# Get user-specific summary
user_usage = tracker.get_user_usage(user_id=123)
```

### Budget Monitoring

```python
# Check budget status
alerts = tracker.check_budget_alerts()

if alerts["daily"]["exceeded"]:
    print("Daily budget exceeded!")
elif alerts["daily"]["warning"]:
    print("Warning: 80% of daily budget used")

print(f"Daily: ${alerts['daily']['spent']:.2f} / ${alerts['daily']['budget']:.2f}")
print(f"Monthly: ${alerts['monthly']['spent']:.2f} / ${alerts['monthly']['budget']:.2f}")
```

### Cost Projection

```python
# Project costs for next 30 days
projection = tracker.get_cost_projection(days_ahead=30)

print(f"Projected cost: ${projection['projected_cost']:.2f}")
print(f"Daily average: ${projection['daily_average']:.2f}")
print(f"Confidence: {projection['confidence']}")
```

### Export Data

```python
from pathlib import Path
from datetime import datetime, timedelta

# Export to JSON
tracker.export_to_json(
    Path("usage_summary.json"),
    start_date=datetime.now() - timedelta(days=30)
)

# Export to CSV
tracker.export_to_csv(
    Path("usage_details.csv"),
    start_date=datetime.now() - timedelta(days=30)
)
```

## API Endpoints (Admin Only)

### GET `/admin/ai-usage/summary`

Get aggregated usage summary.

**Query Parameters:**
- `start_date` (optional): Start of period
- `end_date` (optional): End of period
- `period` (optional): Predefined period (`daily`, `weekly`, `monthly`)

**Response:**
```json
{
  "total_requests": 1250,
  "total_input_tokens": 125000,
  "total_output_tokens": 62500,
  "total_tokens": 187500,
  "total_cost": 1.3125,
  "average_cost_per_request": 0.00105,
  "period_start": "2025-01-01T00:00:00",
  "period_end": "2025-01-31T23:59:59",
  "by_request_type": {
    "feedback": {
      "count": 800,
      "input_tokens": 80000,
      "output_tokens": 40000,
      "cost": 0.84
    },
    "hint": {
      "count": 300,
      "input_tokens": 30000,
      "output_tokens": 15000,
      "cost": 0.315
    },
    "insights": {
      "count": 150,
      "input_tokens": 15000,
      "output_tokens": 7500,
      "cost": 0.1575
    }
  }
}
```

### GET `/admin/ai-usage/by-user/{user_id}`

Get usage for specific user.

**Query Parameters:**
- `start_date` (optional): Start of period
- `end_date` (optional): End of period
- `days` (optional): Number of days to look back (default: 30)

### GET `/admin/ai-usage/budget-alerts`

Get current budget status and alerts.

**Response:**
```json
{
  "alerts": {
    "daily": {
      "budget": 10.0,
      "spent": 3.45,
      "remaining": 6.55,
      "percentage": 34.5,
      "exceeded": false,
      "warning": false
    },
    "monthly": {
      "budget": 200.0,
      "spent": 87.32,
      "remaining": 112.68,
      "percentage": 43.7,
      "exceeded": false,
      "warning": false
    }
  },
  "timestamp": "2025-01-16T12:00:00"
}
```

### GET `/admin/ai-usage/projection`

Get cost projection based on recent usage.

**Query Parameters:**
- `days_ahead` (optional): Number of days to project (default: 30)

**Response:**
```json
{
  "projection_days": 30,
  "projected_cost": 104.25,
  "daily_average": 3.475,
  "confidence": "high",
  "based_on_requests": 875
}
```

### POST `/admin/ai-usage/export/json`

Export usage data to JSON file.

**Query Parameters:**
- `start_date` (optional): Start of export period
- `end_date` (optional): End of export period
- `days` (optional): Number of days to export (default: 30)

**Response:** Downloads JSON file

### POST `/admin/ai-usage/export/csv`

Export usage data to CSV file.

**Query Parameters:**
- `start_date` (optional): Start of export period
- `end_date` (optional): End of export period
- `days` (optional): Number of days to export (default: 30)

**Response:** Downloads CSV file

## Database Schema

### `ai_usage_records` Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer | Primary key |
| `user_id` | Integer | User ID (nullable, FK to users) |
| `request_type` | String(50) | Type of request (feedback, hint, insights, etc.) |
| `model` | String(100) | Claude model used |
| `input_tokens` | Integer | Number of input tokens |
| `output_tokens` | Integer | Number of output tokens |
| `estimated_cost` | Float | Estimated cost in USD |
| `created_at` | DateTime | Timestamp |

**Indexes:**
- `ix_ai_usage_records_id`: Primary key index
- `ix_ai_usage_records_user_id`: User lookup
- `ix_ai_usage_records_request_type`: Type filtering
- `ix_ai_usage_records_created_at`: Time-based queries
- `idx_user_date`: Composite index for user + date queries
- `idx_type_date`: Composite index for type + date queries
- `idx_date_cost`: Composite index for date + cost queries

## Configuration

### Budget Thresholds

Default values (can be customized):

```python
# In ai_usage_tracker.py
DEFAULT_DAILY_BUDGET = 10.0  # USD per day
DEFAULT_MONTHLY_BUDGET = 200.0  # USD per month
```

### Alert Thresholds

- **Warning:** 80% of budget
- **Exceeded:** 100% of budget

## Integration with AI Service

The AI service automatically tracks all API calls:

```python
# In ai_service.py
async def _create_message(
    self,
    prompt: str,
    request_type: RequestType = RequestType.OTHER,
    user_id: Optional[int] = None
    # ...
) -> str:
    # Make API call
    response = await self._client.messages.create(...)

    # Track usage automatically
    if self._usage_tracker and response.usage:
        self._usage_tracker.track_usage(
            request_type=request_type,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            user_id=user_id,
            model=params["model"]
        )

    return content
```

## Request Types

```python
class RequestType(str, Enum):
    FEEDBACK = "feedback"       # Exercise feedback
    INSIGHTS = "insights"       # Learning insights
    HINT = "hint"              # Exercise hints
    HEALTH_CHECK = "health_check"  # Service health checks
    OTHER = "other"            # Other requests
```

## Monitoring Best Practices

1. **Set Appropriate Budgets**
   - Start conservatively
   - Adjust based on actual usage patterns
   - Monitor alerts regularly

2. **Review Usage Patterns**
   - Check daily/weekly summaries
   - Identify high-cost operations
   - Optimize expensive queries

3. **Track by User**
   - Identify power users
   - Detect anomalous usage
   - Allocate costs appropriately

4. **Export for Analysis**
   - Regular CSV exports for detailed analysis
   - JSON exports for integration with BI tools
   - Historical trend analysis

5. **Cost Optimization**
   - Cache frequently requested content
   - Use shorter prompts where possible
   - Batch similar requests
   - Set appropriate max_tokens limits

## Migration

To add the AI usage tracking table to your database:

```bash
# Run the migration
alembic upgrade head
```

The migration file creates:
- `ai_usage_records` table
- All necessary indexes
- Foreign key to `users` table

## Troubleshooting

### High Costs

1. Check request distribution: `GET /admin/ai-usage/summary?period=daily`
2. Identify top users: Review `by_user` breakdown
3. Examine request types: Check `by_request_type` breakdown
4. Review token counts: High token usage may indicate verbose prompts

### Budget Exceeded

1. Check alerts: `GET /admin/ai-usage/budget-alerts`
2. Review recent usage: Export CSV for last 7 days
3. Adjust budgets if needed
4. Implement rate limiting for high-usage endpoints

### Missing Data

1. Verify database session is passed to AI service
2. Check that usage tracker is initialized
3. Confirm API responses include usage data
4. Review logs for tracking errors

## Future Enhancements

- Real-time usage dashboard
- Per-user budget limits
- Cost attribution by feature
- Advanced anomaly detection
- Integration with billing systems
- Historical trend visualization
- Automated cost optimization recommendations

## See Also

- [AI Service Documentation](./AI_SERVICE.md)
- [Admin API Documentation](./API_ADMIN.md)
- [Database Schema](./DATABASE_SCHEMA.md)

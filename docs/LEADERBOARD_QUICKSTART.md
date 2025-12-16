# Leaderboard System - Quick Start Guide

## Installation & Setup

### 1. Run Database Migration

```bash
cd backend
alembic upgrade head
```

This creates three new tables:
- `leaderboard_entries` - Current rankings
- `leaderboard_snapshots` - Historical data
- `leaderboard_cache` - Query cache

### 2. Verify Migration

```bash
alembic current
# Should show: a9b4c5d6e7f8 (head)
```

### 3. Initial Data Population

```python
from core.database import get_db
from services.leaderboard_service import LeaderboardService
from models.leaderboard import LeaderboardPeriod

with get_db() as db:
    service = LeaderboardService(db)

    # Populate all-time leaderboard from existing user data
    service.refresh_all_scores(LeaderboardPeriod.ALL_TIME)

    print("Leaderboard initialized successfully!")
```

## Quick Usage Examples

### Backend - Update Scores

```python
# After user completes an exercise
from services.leaderboard_service import LeaderboardService
from models.leaderboard import ScoreType, LeaderboardPeriod

service = LeaderboardService(db)

# Update XP
service.update_user_score(
    user_id=user.id,
    score_type=ScoreType.XP,
    new_score=user.statistics.total_points,
    period=LeaderboardPeriod.ALL_TIME
)

# Update accuracy
service.update_user_score(
    user_id=user.id,
    score_type=ScoreType.ACCURACY,
    new_score=user.statistics.overall_accuracy,
    period=LeaderboardPeriod.WEEKLY
)
```

### Backend - Query Rankings

```python
# Get top 10 users
leaderboard = service.get_leaderboard(
    score_type=ScoreType.XP,
    period=LeaderboardPeriod.ALL_TIME,
    limit=10
)

print(f"Total participants: {leaderboard.total_participants}")
for entry in leaderboard.entries:
    print(f"#{entry.rank} {entry.username}: {entry.score} XP")

# Get user's rank
rank_info = service.get_user_rank(
    user_id=123,
    score_type=ScoreType.STREAK,
    period=LeaderboardPeriod.MONTHLY
)

print(f"Your rank: #{rank_info.rank}")
print(f"Your score: {rank_info.score}")
print(f"You're in the top {rank_info.percentile}%")
```

### Frontend - Display Component

```tsx
import { Leaderboard } from '@/components/dashboard';

function DashboardPage() {
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>

      {/* Add leaderboard component */}
      <Leaderboard />
    </div>
  );
}

export default DashboardPage;
```

### API Endpoints

#### Get Top Users
```bash
# Get top 10 XP leaders (all-time)
curl http://localhost:8000/api/leaderboard/xp

# Get top 20 weekly accuracy leaders
curl "http://localhost:8000/api/leaderboard/accuracy?period=weekly&limit=20"

# Response:
{
  "score_type": "xp",
  "period": "all_time",
  "entries": [
    {
      "id": 1,
      "user_id": 42,
      "username": "maria_learn",
      "rank": 1,
      "score": 15000.0,
      "achieved_at": "2025-12-15T10:30:00"
    },
    ...
  ],
  "total_participants": 150,
  "last_updated": "2025-12-16T11:45:00"
}
```

#### Get My Rank
```bash
# Get your rank (requires authentication)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/leaderboard/xp/me?period=weekly"

# Response:
{
  "user_id": 123,
  "username": "you",
  "score_type": "xp",
  "period": "weekly",
  "score": 2500.0,
  "rank": 15,
  "total_participants": 200,
  "percentile": 92.5,
  "nearby_users": [
    {"rank": 13, "username": "user13", "score": 2700},
    {"rank": 14, "username": "user14", "score": 2600},
    {"rank": 15, "username": "you", "score": 2500, "is_current_user": true},
    {"rank": 16, "username": "user16", "score": 2400},
    {"rank": 17, "username": "user17", "score": 2300}
  ]
}
```

#### Get Statistics
```bash
curl "http://localhost:8000/api/leaderboard/stats/accuracy?period=monthly"

# Response:
{
  "score_type": "accuracy",
  "period": "monthly",
  "total_participants": 180,
  "highest_score": 98.5,
  "average_score": 75.3,
  "median_score": 78.0
}
```

## Score Types

| Type | Description | Source |
|------|-------------|--------|
| `xp` | Experience points | `user_statistics.total_points` |
| `accuracy` | Overall accuracy % | `user_statistics.overall_accuracy` |
| `streak` | Current streak days | `user_profile.current_streak` |
| `exercises_completed` | Total exercises | `user_statistics.total_exercises_completed` |

## Time Periods

| Period | Description | Reset Time |
|--------|-------------|------------|
| `daily` | Today only | 00:00 UTC |
| `weekly` | Monday-Sunday | Monday 00:00 UTC |
| `monthly` | Calendar month | 1st of month 00:00 UTC |
| `all_time` | Since account creation | Never |

## Integration Points

### After Exercise Completion

```python
# In your exercise completion handler
def complete_exercise(user_id: int, exercise_id: int, is_correct: bool, db: Session):
    # ... existing logic ...

    # Update statistics
    stats = user.statistics
    stats.total_exercises_completed += 1
    if is_correct:
        stats.total_correct_answers += 1
        stats.total_points += 10

    stats.overall_accuracy = (stats.total_correct_answers / stats.total_exercises_completed) * 100
    db.commit()

    # Update leaderboards
    leaderboard_service = LeaderboardService(db)

    # Update all relevant periods
    for period in [LeaderboardPeriod.DAILY, LeaderboardPeriod.WEEKLY,
                   LeaderboardPeriod.MONTHLY, LeaderboardPeriod.ALL_TIME]:
        leaderboard_service.update_user_score(
            user_id=user_id,
            score_type=ScoreType.XP,
            new_score=float(stats.total_points),
            period=period
        )
        leaderboard_service.update_user_score(
            user_id=user_id,
            score_type=ScoreType.ACCURACY,
            new_score=float(stats.overall_accuracy),
            period=period
        )
        leaderboard_service.update_user_score(
            user_id=user_id,
            score_type=ScoreType.EXERCISES_COMPLETED,
            new_score=float(stats.total_exercises_completed),
            period=period
        )
```

### Daily Streak Update

```python
def update_streak(user_id: int, db: Session):
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

    # ... streak calculation logic ...

    profile.current_streak = new_streak
    db.commit()

    # Update streak leaderboard
    leaderboard_service = LeaderboardService(db)
    for period in [LeaderboardPeriod.DAILY, LeaderboardPeriod.WEEKLY,
                   LeaderboardPeriod.MONTHLY, LeaderboardPeriod.ALL_TIME]:
        leaderboard_service.update_user_score(
            user_id=user_id,
            score_type=ScoreType.STREAK,
            new_score=float(profile.current_streak),
            period=period
        )
```

## Scheduled Tasks

### Daily Snapshot (Recommended)

Create snapshots at end of each period for historical analysis:

```python
# scheduled_tasks.py
from services.leaderboard_service import LeaderboardService
from models.leaderboard import ScoreType, LeaderboardPeriod

def create_daily_snapshots(db: Session):
    """Run this at 23:59 UTC daily"""
    service = LeaderboardService(db)

    for score_type in ScoreType:
        service.create_snapshot(score_type, LeaderboardPeriod.DAILY)
        print(f"Created daily snapshot for {score_type.value}")

def create_weekly_snapshots(db: Session):
    """Run this at 23:59 UTC on Sundays"""
    service = LeaderboardService(db)

    for score_type in ScoreType:
        service.create_snapshot(score_type, LeaderboardPeriod.WEEKLY)
        print(f"Created weekly snapshot for {score_type.value}")

def create_monthly_snapshots(db: Session):
    """Run this at 23:59 UTC on last day of month"""
    service = LeaderboardService(db)

    for score_type in ScoreType:
        service.create_snapshot(score_type, LeaderboardPeriod.MONTHLY)
        print(f"Created monthly snapshot for {score_type.value}")
```

### Cron Jobs (Linux/Mac)

```bash
# crontab -e

# Daily snapshots at 23:59 UTC
59 23 * * * curl -X POST http://localhost:8000/api/leaderboard/xp/snapshot?period=daily

# Weekly snapshots on Sunday at 23:59 UTC
59 23 * * 0 curl -X POST http://localhost:8000/api/leaderboard/xp/snapshot?period=weekly

# Monthly snapshots on last day of month at 23:59 UTC
59 23 28-31 * * [ $(date -d tomorrow +\%d) -eq 1 ] && curl -X POST http://localhost:8000/api/leaderboard/xp/snapshot?period=monthly
```

## Testing

### Manual Testing

```bash
# 1. Run migration
cd backend
alembic upgrade head

# 2. Start server
python main.py

# 3. Create test user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass123"}'

# 4. Login
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}' | jq -r '.access_token')

# 5. Check leaderboard
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/leaderboard/xp

# 6. Check your rank
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/leaderboard/xp/me
```

### Automated Tests

```python
import pytest
from services.leaderboard_service import LeaderboardService
from models.leaderboard import ScoreType, LeaderboardPeriod

def test_leaderboard_ranking(db_session):
    service = LeaderboardService(db_session)

    # Create test users with scores
    service.update_user_score(1, ScoreType.XP, 1000, LeaderboardPeriod.ALL_TIME)
    service.update_user_score(2, ScoreType.XP, 2000, LeaderboardPeriod.ALL_TIME)
    service.update_user_score(3, ScoreType.XP, 1500, LeaderboardPeriod.ALL_TIME)

    # Get leaderboard
    leaderboard = service.get_leaderboard(ScoreType.XP, LeaderboardPeriod.ALL_TIME)

    # Verify ranking
    assert leaderboard.entries[0].user_id == 2  # Highest score
    assert leaderboard.entries[0].rank == 1
    assert leaderboard.entries[1].user_id == 3  # Second highest
    assert leaderboard.entries[1].rank == 2
    assert leaderboard.entries[2].user_id == 1  # Lowest
    assert leaderboard.entries[2].rank == 3

def test_tie_breaking(db_session):
    service = LeaderboardService(db_session)

    # Same scores, different times
    service.update_user_score(1, ScoreType.XP, 1000, LeaderboardPeriod.ALL_TIME)
    # Sleep 1 second
    time.sleep(1)
    service.update_user_score(2, ScoreType.XP, 1000, LeaderboardPeriod.ALL_TIME)

    leaderboard = service.get_leaderboard(ScoreType.XP, LeaderboardPeriod.ALL_TIME)

    # Earlier achiever should rank higher
    assert leaderboard.entries[0].user_id == 1
    assert leaderboard.entries[1].user_id == 2
```

## Troubleshooting

### Problem: User not appearing on leaderboard

**Solution:**
```python
# 1. Check if user has statistics
user_stats = db.query(UserStatistics).filter(UserStatistics.user_id == user_id).first()
print(f"User stats: {user_stats}")

# 2. Manually update scores
service = LeaderboardService(db)
service.update_user_score(user_id, ScoreType.XP, float(user_stats.total_points))

# 3. Refresh all scores
service.refresh_all_scores()
```

### Problem: Ranks not updating

**Solution:**
```python
# Force rank recalculation
service._recalculate_ranks(ScoreType.XP, LeaderboardPeriod.ALL_TIME)
```

### Problem: Stale cache data

**Solution:**
```python
# Clear cache for specific leaderboard
service._invalidate_cache(ScoreType.XP, LeaderboardPeriod.WEEKLY)

# Or clear all expired cache entries
from datetime import datetime
db.query(LeaderboardCache).filter(
    LeaderboardCache.expires_at < datetime.utcnow()
).delete()
db.commit()
```

## Next Steps

1. **Customize UI**: Modify `Leaderboard.css` to match your brand colors
2. **Add Notifications**: Alert users when they climb ranks
3. **Create Badges**: Award achievements for leaderboard milestones
4. **Analytics Dashboard**: Admin panel to view leaderboard trends
5. **Social Features**: Share leaderboard position on social media

## Support

For issues or questions:
- Check logs: `backend/backend.log`
- Review documentation: `docs/LEADERBOARD_IMPLEMENTATION.md`
- Database inspection: Use Alembic or SQL client to inspect tables

## Performance Tips

1. **Index Usage**: Verify indexes are being used in queries
   ```sql
   EXPLAIN ANALYZE SELECT * FROM leaderboard_entries
   WHERE score_type = 'xp' AND period = 'all_time'
   ORDER BY score DESC LIMIT 10;
   ```

2. **Cache Monitoring**: Track cache hit rate
   ```python
   total_queries = db.query(func.count(LeaderboardCache.id)).scalar()
   total_hits = db.query(func.sum(LeaderboardCache.cache_hits)).scalar()
   hit_rate = (total_hits / total_queries) * 100
   print(f"Cache hit rate: {hit_rate}%")
   ```

3. **Query Optimization**: Use pagination for large leaderboards
   ```python
   # Get next page
   leaderboard = service.get_leaderboard(
       score_type=ScoreType.XP,
       period=LeaderboardPeriod.ALL_TIME,
       limit=10,
       offset=10  # Skip first 10 entries
   )
   ```

Happy ranking!

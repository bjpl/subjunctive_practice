# Achievements System Implementation

## Overview

Complete achievement system implementation for the Spanish Subjunctive Practice application. This system provides comprehensive gamification features including:

- 17 unique achievements across 5 categories
- Automatic progress tracking and unlocking
- Real-time achievement checking after exercise submission
- Detailed statistics for achievement progress
- Full REST API integration

## Implementation Summary

### Files Created/Modified

#### New Files

1. **`backend/api/routes/achievements.py`** (450+ lines)
   - Main achievements API endpoint
   - 3 REST endpoints: GET, POST /check, GET /stats
   - Helper functions for stats calculation
   - Progress calculation logic
   - Automatic achievement unlocking

2. **`backend/scripts/seed_achievements.py`** (200+ lines)
   - Database seeding script
   - 17 achievement definitions matching frontend
   - Safe seeding (skips duplicates)
   - Logging and error handling

3. **`backend/docs/achievements_api.md`** (400+ lines)
   - Comprehensive API documentation
   - All endpoints documented with examples
   - Response models and error handling
   - Integration guide
   - Example code in TypeScript and Python

4. **`backend/tests/test_achievements_api.py`** (350+ lines)
   - Comprehensive unit tests
   - Tests for all helper functions
   - Integration tests for unlocking logic
   - Edge case testing

#### Modified Files

1. **`backend/main.py`**
   - Added achievements router import
   - Registered `/api/achievements` routes

2. **`backend/api/routes/exercises.py`**
   - Integrated automatic achievement checking
   - Calls `check_and_unlock_achievements()` after answer submission
   - Graceful error handling (non-blocking)

## API Endpoints

### 1. GET `/api/achievements`

**Purpose**: Get all achievements with user progress

**Response**: List of achievements with:
- Unlock status
- Progress percentage (0-100)
- Current value vs requirement
- Points and metadata

**Use Case**: Display achievements page, show progress bars

### 2. POST `/api/achievements/check`

**Purpose**: Check for newly unlocked achievements

**Response**: List of newly unlocked achievements with total points

**Use Case**:
- Called after completing exercises/sessions
- Display achievement unlock notifications
- Award points to user

### 3. GET `/api/achievements/stats`

**Purpose**: Get detailed user statistics

**Response**: Comprehensive stats including:
- Streak information
- Exercise counts
- Accuracy metrics
- Category-specific data

**Use Case**: Analytics, progress tracking, debugging

## Achievement Categories

### Streak Achievements (4)
- Getting Started: 3 days (10 pts)
- Week Warrior: 7 days (25 pts)
- Month Master: 30 days (100 pts)
- Century Champion: 100 days (500 pts)

### Volume Achievements (4)
- Dedicated Learner: 50 exercises (20 pts)
- Practice Makes Perfect: 250 exercises (75 pts)
- Master Student: 1,000 exercises (250 pts)
- Grammar Guru: 5,000 exercises (1,000 pts)

### Accuracy Achievements (4)
- Perfect Ten: 10 consecutive correct (15 pts)
- Sharpshooter: 25 consecutive correct (50 pts)
- Perfectionist: 50 consecutive correct (150 pts)
- Flawless Victory: 100% session accuracy (30 pts)

### Mastery Achievements (2)
- Topic Master: 90% in any category (100 pts)
- Complete Mastery: 85% in all categories (500 pts)

### Special Achievements (3)
- Speed Demon: 20 exercises in <5 minutes (75 pts)
- Night Owl: Practice midnight-4 AM (10 pts)
- Early Bird: Practice 5-7 AM (10 pts)

**Total Points Available**: 3,035 points

## Database Schema

### Achievement Table
```sql
CREATE TABLE achievements (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    icon_url VARCHAR(500),
    points INTEGER DEFAULT 10,
    criteria JSON NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### UserAchievement Table
```sql
CREATE TABLE user_achievements (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    achievement_id INTEGER NOT NULL,
    unlocked_at TIMESTAMP NOT NULL,
    progress_data JSON,
    created_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (achievement_id) REFERENCES achievements(id)
);
```

## Setup Instructions

### 1. Database Migration

The achievement tables are already defined in `models/progress.py`:
- `Achievement` model
- `UserAchievement` model

Run Alembic migration to create tables:
```bash
cd backend
alembic upgrade head
```

### 2. Seed Achievements

Populate the database with achievement definitions:

```bash
cd backend
python -m scripts.seed_achievements
```

**Output**:
```
Starting achievement seeding...
Created achievement: Getting Started (streak, 10 pts)
Created achievement: Week Warrior (streak, 25 pts)
...
Achievement seeding complete!
  Created: 17
  Skipped: 0
  Total: 17
✓ Achievement seeding successful!
```

### 3. Verify API

Start the server and test endpoints:

```bash
# Start server
uvicorn main:app --reload

# In another terminal, test (requires authentication)
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/api/achievements
```

## Integration Guide

### Frontend Integration

#### 1. Display Achievements Page

```typescript
import { useEffect, useState } from 'react';

interface Achievement {
  id: number;
  name: string;
  description: string;
  category: string;
  points: number;
  unlocked: boolean;
  progress: number;
  requirement: number;
  current_value: number;
}

export function AchievementsPage() {
  const [achievements, setAchievements] = useState<Achievement[]>([]);

  useEffect(() => {
    const fetchAchievements = async () => {
      const response = await fetch('/api/achievements', {
        headers: {
          'Authorization': `Bearer ${getToken()}`
        }
      });
      const data = await response.json();
      setAchievements(data);
    };

    fetchAchievements();
  }, []);

  return (
    <div>
      {achievements.map(ach => (
        <AchievementCard key={ach.id} achievement={ach} />
      ))}
    </div>
  );
}
```

#### 2. Check After Exercise Submission

```typescript
async function submitExercise(exerciseId: string, answer: string) {
  // Submit answer
  const response = await fetch('/api/exercises/submit', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ exercise_id: exerciseId, user_answer: answer })
  });

  const result = await response.json();

  // Check for new achievements
  const achResponse = await fetch('/api/achievements/check', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` }
  });

  const newAchievements = await achResponse.json();

  // Display notifications
  if (newAchievements.achievements.length > 0) {
    newAchievements.achievements.forEach(ach => {
      showNotification(`🏆 Achievement Unlocked: ${ach.name}!`, {
        description: ach.description,
        points: ach.points
      });
    });
  }

  return result;
}
```

#### 3. Display Progress Bars

```typescript
function AchievementCard({ achievement }: { achievement: Achievement }) {
  return (
    <div className="achievement-card">
      <h3>{achievement.name}</h3>
      <p>{achievement.description}</p>

      {/* Progress bar */}
      <div className="progress-bar">
        <div
          className="progress-fill"
          style={{ width: `${achievement.progress}%` }}
        />
      </div>

      <p className="progress-text">
        {achievement.current_value} / {achievement.requirement}
      </p>

      {achievement.unlocked ? (
        <span className="badge unlocked">✓ Unlocked</span>
      ) : (
        <span className="badge locked">🔒 Locked</span>
      )}

      <p className="points">{achievement.points} points</p>
    </div>
  );
}
```

### Automatic Checking

Achievement checking is **automatically triggered** when users submit exercises via `POST /api/exercises/submit`.

The exercise submission endpoint now:
1. Validates and saves the answer
2. Checks for newly unlocked achievements
3. Logs achievement unlocks
4. Returns answer validation (achievement check is non-blocking)

**No additional frontend code required** for basic functionality.

## Testing

### Unit Tests

Run all achievement tests:

```bash
cd backend
pytest tests/test_achievements_api.py -v
```

**Test Coverage**:
- User ID parsing
- Statistics calculation
- Consecutive correct tracking
- Progress calculation for each category
- Achievement unlocking logic
- Duplicate prevention
- Multiple concurrent unlocks

### Manual Testing

1. **Create Test User**
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "username": "testuser", "password": "testpass123"}'
```

2. **Get Achievements**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/achievements
```

3. **Submit Exercises**
```bash
# Submit 10 correct answers to unlock "Perfect Ten"
for i in {1..10}; do
  curl -X POST http://localhost:8000/api/exercises/submit \
    -H "Authorization: Bearer YOUR_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"exercise_id": "1", "user_answer": "correct_answer"}'
done
```

4. **Check New Achievements**
```bash
curl -X POST http://localhost:8000/api/achievements/check \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Performance Considerations

### Database Queries

- **Indexed Fields**: `user_id`, `achievement_id` for fast lookups
- **Batch Operations**: All achievements checked in single database transaction
- **Efficient Joins**: Uses SQLAlchemy ORM efficiently

### Caching Opportunities

1. **Achievement Definitions**: Static data, cache client-side
2. **User Stats**: Recalculated on-demand, could be cached with TTL
3. **Unlocked Achievements**: Cached until new unlock occurs

### Optimization

- Non-blocking achievement checking in exercise submission
- Graceful error handling (doesn't fail main request)
- Lazy calculation (stats computed only when needed)
- Limited query scope (e.g., last 200 attempts for consecutive check)

## Error Handling

### API Level

All endpoints return standard error format:

```json
{
  "error": "Error Type",
  "message": "Detailed message",
  "path": "/api/achievements",
  "timestamp": "2025-11-28T14:25:30Z"
}
```

### Integration Level

Exercise submission includes try-catch for achievement checking:

```python
try:
    newly_unlocked = check_and_unlock_achievements(db, user_id)
    if newly_unlocked:
        logger.info(f"Unlocked {len(newly_unlocked)} achievements")
except Exception as e:
    # Log error but don't fail the request
    logger.error(f"Achievement check failed: {e}", exc_info=True)
```

This ensures achievement failures don't break core functionality.

## Monitoring and Logging

### Log Messages

The system logs:
- Achievement unlocks: `User X unlocked achievement 'Y' (ID: Z)`
- API calls: `Returning N achievements for user X`
- Errors: Full stack traces for debugging

### Metrics to Track

- Achievement unlock rate
- Most/least unlocked achievements
- Average time to unlock each achievement
- User engagement with achievements feature

## Future Enhancements

### Planned Features

1. **Achievement Tiers**
   - Visual distinction (Bronze, Silver, Gold, Platinum)
   - Upgrade system (unlock higher tiers)

2. **Leaderboards**
   - Rank users by total achievement points
   - Category-specific leaderboards

3. **Social Features**
   - Share achievement unlocks
   - Compare with friends
   - Team achievements

4. **Custom Achievements**
   - User-defined goals
   - Personal milestones

5. **Reward Integration**
   - Link to app features
   - Unlock themes/avatars
   - Discount codes

### Technical Improvements

1. **Caching Layer**
   - Redis cache for stats
   - Reduce database queries

2. **Real-time Notifications**
   - WebSocket for instant unlock notifications
   - Push notifications

3. **Analytics Dashboard**
   - Admin view of achievement statistics
   - Engagement metrics

4. **A/B Testing**
   - Test different point values
   - Optimize unlock criteria

## Troubleshooting

### Issue: No achievements returned

**Solution**: Seed the database
```bash
python -m scripts.seed_achievements
```

### Issue: Achievements not unlocking

**Checks**:
1. Verify user has required progress: `GET /api/achievements/stats`
2. Check criteria in database matches expectations
3. Review logs for errors during `check_and_unlock_achievements()`

### Issue: Duplicate achievements

**Prevention**: The system checks for existing unlocks before creating new ones.

**Manual fix** (if needed):
```sql
DELETE FROM user_achievements
WHERE id NOT IN (
  SELECT MIN(id)
  FROM user_achievements
  GROUP BY user_id, achievement_id
);
```

## Contributing

When adding new achievements:

1. Add definition to `ACHIEVEMENT_DEFINITIONS` in `seed_achievements.py`
2. Update criteria handling in `calculate_achievement_progress()`
3. Add stats calculation if needed in `get_user_stats_for_achievements()`
4. Update documentation
5. Add tests for new achievement type
6. Run migration and seeding

## License

Part of Spanish Subjunctive Practice application.

---

**Implementation Date**: November 28, 2025
**Version**: 1.0.0
**Status**: Production Ready

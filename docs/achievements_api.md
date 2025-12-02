# Achievements API Documentation

## Overview

The Achievements API provides gamification features for tracking user progress and unlocking achievements based on learning milestones.

**Base URL**: `/api/achievements`

**Authentication**: All endpoints require JWT authentication via Bearer token.

---

## Endpoints

### GET `/api/achievements`

Get all achievements with user's progress and unlock status.

**Response**: `List[AchievementResponse]`

```json
[
  {
    "id": 1,
    "name": "Getting Started",
    "description": "Practice for 3 days in a row",
    "category": "streak",
    "icon_url": "flame",
    "points": 10,
    "unlocked": true,
    "unlocked_at": "2025-11-20T10:30:00Z",
    "progress": 100.0,
    "requirement": 3,
    "current_value": 5
  },
  {
    "id": 2,
    "name": "Week Warrior",
    "description": "Practice for 7 days in a row",
    "category": "streak",
    "icon_url": "flame",
    "points": 25,
    "unlocked": false,
    "unlocked_at": null,
    "progress": 71.43,
    "requirement": 7,
    "current_value": 5
  }
]
```

**Status Codes**:
- `200 OK`: Success
- `401 Unauthorized`: Invalid or missing authentication
- `404 Not Found`: No achievements available (database not seeded)

---

### POST `/api/achievements/check`

Check for newly unlocked achievements based on current user progress.

Should be called after completing exercises or sessions to detect new achievement unlocks.

**Response**: `NewlyUnlockedResponse`

```json
{
  "achievements": [
    {
      "id": 5,
      "name": "Perfect Ten",
      "description": "Get 10 exercises correct in a row",
      "category": "accuracy",
      "icon_url": "target",
      "points": 15,
      "unlocked": true,
      "unlocked_at": "2025-11-28T14:25:30Z",
      "progress": 100.0,
      "requirement": 10,
      "current_value": 12
    }
  ],
  "total_points": 15,
  "message": "Unlocked 1 new achievement(s)!"
}
```

**Status Codes**:
- `200 OK`: Success (empty array if no new achievements)
- `401 Unauthorized`: Invalid or missing authentication

---

### GET `/api/achievements/stats`

Get user statistics relevant for achievement calculation.

**Response**: `UserStatsResponse`

```json
{
  "current_streak": 5,
  "total_exercises": 127,
  "correct_exercises": 98,
  "consecutive_correct": 12,
  "total_sessions": 18,
  "perfect_sessions": 3,
  "category_accuracy": {
    "present_subjunctive": 85.5,
    "imperfect_subjunctive": 72.3,
    "present_perfect_subjunctive": 90.1
  }
}
```

**Status Codes**:
- `200 OK`: Success
- `401 Unauthorized`: Invalid or missing authentication

---

## Achievement Categories

### Streak Achievements
Track consecutive days of practice.

| Achievement | Requirement | Points |
|------------|-------------|--------|
| Getting Started | 3 days | 10 |
| Week Warrior | 7 days | 25 |
| Month Master | 30 days | 100 |
| Century Champion | 100 days | 500 |

### Volume Achievements
Track total exercises completed.

| Achievement | Requirement | Points |
|------------|-------------|--------|
| Dedicated Learner | 50 exercises | 20 |
| Practice Makes Perfect | 250 exercises | 75 |
| Master Student | 1,000 exercises | 250 |
| Grammar Guru | 5,000 exercises | 1,000 |

### Accuracy Achievements
Track consecutive correct answers and perfect sessions.

| Achievement | Requirement | Points |
|------------|-------------|--------|
| Perfect Ten | 10 correct in a row | 15 |
| Sharpshooter | 25 correct in a row | 50 |
| Perfectionist | 50 correct in a row | 150 |
| Flawless Victory | 100% accuracy in a session | 30 |

### Mastery Achievements
Track category-specific accuracy.

| Achievement | Requirement | Points |
|------------|-------------|--------|
| Topic Master | 90% accuracy in any category | 100 |
| Complete Mastery | 85% accuracy in all categories | 500 |

### Special Achievements
Unique achievements for special accomplishments.

| Achievement | Requirement | Points |
|------------|-------------|--------|
| Speed Demon | 20 exercises in under 5 minutes | 75 |
| Night Owl | Practice between midnight and 4 AM | 10 |
| Early Bird | Practice between 5 AM and 7 AM | 10 |

---

## Integration

### Automatic Achievement Checking

Achievement checking is automatically triggered when:

1. **Exercise Submission** (`POST /api/exercises/submit`)
   - Checks for volume, accuracy, and mastery achievements
   - Runs asynchronously to not block response

2. **Manual Check** (`POST /api/achievements/check`)
   - Useful for checking after session completion
   - Returns only newly unlocked achievements

### Database Seeding

Before using the achievements API, seed the database:

```bash
cd backend
python -m scripts.seed_achievements
```

This creates all 16 achievement definitions matching the frontend.

---

## Response Models

### AchievementResponse

```typescript
{
  id: number;
  name: string;
  description: string;
  category: "streak" | "volume" | "accuracy" | "mastery" | "special";
  icon_url: string | null;
  points: number;
  unlocked: boolean;
  unlocked_at: datetime | null;
  progress: number; // 0-100
  requirement: number;
  current_value: number;
}
```

### NewlyUnlockedResponse

```typescript
{
  achievements: AchievementResponse[];
  total_points: number;
  message: string;
}
```

### UserStatsResponse

```typescript
{
  current_streak: number;
  total_exercises: number;
  correct_exercises: number;
  consecutive_correct: number;
  total_sessions: number;
  perfect_sessions: number;
  category_accuracy: { [category: string]: number };
}
```

---

## Error Handling

All endpoints follow standard error response format:

```json
{
  "error": "Error type",
  "message": "Detailed error message",
  "path": "/api/achievements",
  "timestamp": "2025-11-28T14:25:30Z"
}
```

Common errors:

- **401 Unauthorized**: Missing or invalid JWT token
- **404 Not Found**: Achievements not seeded in database
- **500 Internal Server Error**: Unexpected server error

---

## Best Practices

1. **Seed Database First**: Run `seed_achievements.py` before using the API
2. **Check After Actions**: Call `/check` endpoint after completing exercises or sessions
3. **Handle Empty Results**: No new achievements is a valid successful response
4. **Display Progress**: Use `progress` field to show progress bars
5. **Cache Results**: Achievement list changes infrequently, cache for better UX
6. **Error Tolerance**: Achievement failures shouldn't block main functionality

---

## Example Usage

### JavaScript/TypeScript

```typescript
// Get all achievements with progress
const getAchievements = async () => {
  const response = await fetch('/api/achievements', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  return await response.json();
};

// Check for new achievements after exercise
const checkNewAchievements = async () => {
  const response = await fetch('/api/achievements/check', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });
  const result = await response.json();

  if (result.achievements.length > 0) {
    // Show achievement unlock notification
    showNotification(`Unlocked: ${result.achievements[0].name}!`);
  }
};

// Get user stats
const getStats = async () => {
  const response = await fetch('/api/achievements/stats', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  return await response.json();
};
```

### Python

```python
import requests

# Get achievements
def get_achievements(token):
    response = requests.get(
        'http://localhost:8000/api/achievements',
        headers={'Authorization': f'Bearer {token}'}
    )
    return response.json()

# Check for new achievements
def check_new_achievements(token):
    response = requests.post(
        'http://localhost:8000/api/achievements/check',
        headers={'Authorization': f'Bearer {token}'}
    )
    result = response.json()

    if result['achievements']:
        for ach in result['achievements']:
            print(f"🏆 Unlocked: {ach['name']} (+{ach['points']} pts)")

    return result
```

---

## Performance Considerations

- **Caching**: Achievement definitions are static, cache them client-side
- **Batch Operations**: Achievement checking is batched for efficiency
- **Async Processing**: Achievement unlocking doesn't block main operations
- **Database Indexes**: User_id and achievement_id are indexed for fast queries
- **Lazy Loading**: Stats are calculated on-demand, not pre-computed

---

## Future Enhancements

Planned features for future releases:

1. **Achievement Tiers**: Bronze, Silver, Gold, Platinum visual indicators
2. **Leaderboards**: Compare achievement points with other users
3. **Custom Achievements**: User-defined achievement goals
4. **Achievement Sharing**: Share unlocks on social media
5. **Reward Integration**: Link achievements to app features/discounts

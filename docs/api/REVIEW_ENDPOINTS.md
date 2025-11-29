# Spaced Repetition Review Endpoints

This document describes the spaced repetition review endpoints for the Subjunctive Practice API.

## Overview

The review system implements a spaced repetition algorithm (SM-2) to optimize learning retention. It tracks individual verbs/exercises and schedules them for review based on user performance.

## Endpoints

### GET /api/exercises/review/due

Get exercises that are due for review based on spaced repetition schedule.

**Authentication:** Required (Bearer token)

**Query Parameters:**
- `limit` (optional, default: 10): Maximum number of due items to return (1-50)
- `tense` (optional): Filter by specific tense (future enhancement)

**Response:**
```json
{
  "items": [
    {
      "verb_id": 1,
      "verb_infinitive": "hablar",
      "verb_translation": "to speak",
      "tense": "present_subjunctive",
      "person": null,
      "days_overdue": 2,
      "difficulty_level": "learning",
      "easiness_factor": 2.3,
      "next_review_date": "2025-11-26T10:30:00Z",
      "review_count": 3,
      "success_rate": 75.5
    }
  ],
  "total_due": 15,
  "next_review_date": "2025-11-29T14:00:00Z"
}
```

**Difficulty Levels:**
- `new`: Never reviewed (review_count = 0)
- `learning`: Struggling (easiness_factor < 2.0)
- `reviewing`: Making progress (easiness_factor 2.0-2.5)
- `mastered`: Well learned (easiness_factor > 2.5)

**Ordering:**
Items are returned ordered by most overdue first (earliest next_review_date).

---

### GET /api/exercises/review/stats

Get comprehensive review statistics for the current user.

**Authentication:** Required (Bearer token)

**Response:**
```json
{
  "total_due": 15,
  "due_by_difficulty": {
    "new": 5,
    "learning": 6,
    "reviewing": 3,
    "mastered": 1
  },
  "average_retention": 78.5,
  "total_reviewed": 25,
  "reviews_today": 3,
  "streak_days": 7
}
```

**Field Descriptions:**
- `total_due`: Total number of items currently due for review
- `due_by_difficulty`: Breakdown of due items by difficulty level
- `average_retention`: Overall success rate across all attempts (0-100%)
- `total_reviewed`: Total number of items that have been reviewed at least once
- `reviews_today`: Number of review sessions completed today
- `streak_days`: Consecutive days with at least one completed session

---

## Usage Examples

### Python (requests library)

```python
import requests

# Get authentication token
token = "your_jwt_token_here"
headers = {"Authorization": f"Bearer {token}"}
base_url = "http://localhost:8000/api"

# Get due reviews
response = requests.get(f"{base_url}/exercises/review/due", headers=headers)
due_items = response.json()

print(f"You have {due_items['total_due']} items to review")
for item in due_items['items'][:5]:
    print(f"- {item['verb_infinitive']} ({item['verb_translation']})")
    print(f"  Difficulty: {item['difficulty_level']}, {item['days_overdue']} days overdue")

# Get review statistics
response = requests.get(f"{base_url}/exercises/review/stats", headers=headers)
stats = response.json()

print(f"\nReview Statistics:")
print(f"Total due: {stats['total_due']}")
print(f"Average retention: {stats['average_retention']}%")
print(f"Streak: {stats['streak_days']} days")
```

### JavaScript (fetch API)

```javascript
const baseUrl = 'http://localhost:8000/api';
const token = 'your_jwt_token_here';
const headers = {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json'
};

// Get due reviews
async function getDueReviews(limit = 10) {
  const response = await fetch(
    `${baseUrl}/exercises/review/due?limit=${limit}`,
    { headers }
  );
  const data = await response.json();

  console.log(`${data.total_due} items due for review`);
  data.items.forEach(item => {
    console.log(`${item.verb_infinitive}: ${item.difficulty_level}`);
  });

  return data;
}

// Get review stats
async function getReviewStats() {
  const response = await fetch(
    `${baseUrl}/exercises/review/stats`,
    { headers }
  );
  const stats = await response.json();

  console.log('Review Statistics:', stats);
  return stats;
}

// Use the functions
getDueReviews(20);
getReviewStats();
```

### cURL

```bash
# Get due reviews
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/exercises/review/due?limit=10"

# Get review statistics
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/exercises/review/stats"
```

---

## Integration with Learning Workflow

### Typical Usage Flow

1. **Check what needs review:**
   ```
   GET /exercises/review/stats
   ```
   - See how many items are due
   - Check your retention rate
   - Monitor your streak

2. **Fetch due items:**
   ```
   GET /exercises/review/due?limit=20
   ```
   - Get items that need practice
   - Items ordered by urgency (most overdue first)

3. **Practice the exercises:**
   - For each due item, generate or fetch an exercise for that verb
   - User practices the conjugation
   - Submit answers via existing `POST /exercises/submit` endpoint

4. **Review updates automatically:**
   - The learning algorithm updates ReviewSchedule when answers are submitted
   - `next_review_date` is recalculated based on performance
   - `easiness_factor` adjusts based on correctness

### Dashboard Integration

Create a dashboard showing:
- Number of items due today
- Success rate trend
- Streak counter (gamification)
- Difficulty distribution chart

```javascript
// Example dashboard data fetch
async function getDashboardData() {
  const stats = await fetch('/api/exercises/review/stats', { headers });
  const dueItems = await fetch('/api/exercises/review/due?limit=5', { headers });

  return {
    stats: await stats.json(),
    upcomingReviews: await dueItems.json()
  };
}
```

---

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```
User must provide valid authentication token.

### 400 Bad Request
```json
{
  "detail": "Invalid user ID format"
}
```
Issue with user ID parsing from token.

---

## Notes

- All dates are in UTC timezone (ISO 8601 format)
- The spaced repetition algorithm (SM-2) automatically adjusts review intervals
- Reviews are verb-specific, not exercise-specific
- The system tracks overall performance across all attempts for each verb

## Related Documentation

- [Exercise Endpoints](./API_PARAMETERS_REFERENCE.md)
- [Answer Submission](./API_PARAMETERS_REFERENCE.md#answer-submission)
- [Learning Algorithm](../architecture/LEARNING_ALGORITHM.md)

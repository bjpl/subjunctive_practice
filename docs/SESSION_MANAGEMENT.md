# Session Management API

## Overview

The session management system properly tracks practice sessions with incremental statistics updates. This fixes the issue where each answer submission created a new session record with `total_exercises=1`.

## Architecture Changes

### Problem Fixed
**Before**: Each answer submission created a new `Session` record with `total_exercises=1`, breaking session aggregation and streak calculations.

**After**: Sessions are created explicitly via `/exercises/session/start`, and all attempts within that session update the same Session record incrementally.

## API Endpoints

### 1. Start Practice Session

**Endpoint**: `POST /exercises/session/start`

**Request Body**:
```json
{
  "session_type": "practice"  // Options: "practice", "review", "test"
}
```

**Response**:
```json
{
  "session_id": 42,
  "started_at": "2025-11-28T10:30:00.000Z"
}
```

**Usage**:
```javascript
// Start a new practice session
const response = await fetch('/api/exercises/session/start', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_TOKEN'
  },
  body: JSON.stringify({
    session_type: 'practice'
  })
});

const { session_id, started_at } = await response.json();
// Store session_id for use in answer submissions
```

### 2. Submit Answers with Session ID

**Endpoint**: `POST /exercises/submit`

**Request Body**:
```json
{
  "exercise_id": "123",
  "user_answer": "hable",
  "time_taken": 8,
  "session_id": 42  // IMPORTANT: Include session_id from start endpoint
}
```

**Response**: Same as before (AnswerValidation schema)

**Usage**:
```javascript
// Submit answer with session_id
const response = await fetch('/api/exercises/submit', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_TOKEN'
  },
  body: JSON.stringify({
    exercise_id: exerciseId,
    user_answer: userAnswer,
    time_taken: timeTaken,
    session_id: sessionId  // Use session_id from /session/start
  })
});
```

**How it Works**:
- When `session_id` is provided, the attempt is appended to the existing session
- Session's `total_exercises` increments by 1
- Session's `correct_answers` increments if answer is correct
- Session's `score_percentage` is recalculated: `(correct_answers / total_exercises) * 100`

### 3. End Practice Session

**Endpoint**: `POST /exercises/session/end`

**Request Body**:
```json
{
  "session_id": 42
}
```

**Response**:
```json
{
  "session_id": 42,
  "started_at": "2025-11-28T10:30:00.000Z",
  "ended_at": "2025-11-28T10:45:30.000Z",
  "duration_seconds": 930,
  "total_exercises": 15,
  "correct_answers": 12,
  "score_percentage": 80.0,
  "session_type": "practice"
}
```

**Usage**:
```javascript
// End the session when user is done
const response = await fetch('/api/exercises/session/end', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_TOKEN'
  },
  body: JSON.stringify({
    session_id: sessionId
  })
});

const summary = await response.json();
console.log(`Session completed: ${summary.correct_answers}/${summary.total_exercises} correct`);
```

## Complete Frontend Workflow

```javascript
class PracticeSessionManager {
  constructor() {
    this.sessionId = null;
    this.startedAt = null;
  }

  async startSession(sessionType = 'practice') {
    const response = await fetch('/api/exercises/session/start', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.getToken()}`
      },
      body: JSON.stringify({ session_type: sessionType })
    });

    if (!response.ok) {
      throw new Error('Failed to start session');
    }

    const data = await response.json();
    this.sessionId = data.session_id;
    this.startedAt = data.started_at;

    console.log(`Session ${this.sessionId} started at ${this.startedAt}`);
    return data;
  }

  async submitAnswer(exerciseId, userAnswer, timeTaken) {
    if (!this.sessionId) {
      throw new Error('No active session. Call startSession() first.');
    }

    const response = await fetch('/api/exercises/submit', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.getToken()}`
      },
      body: JSON.stringify({
        exercise_id: exerciseId,
        user_answer: userAnswer,
        time_taken: timeTaken,
        session_id: this.sessionId
      })
    });

    if (!response.ok) {
      throw new Error('Failed to submit answer');
    }

    return await response.json();
  }

  async endSession() {
    if (!this.sessionId) {
      throw new Error('No active session to end');
    }

    const response = await fetch('/api/exercises/session/end', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.getToken()}`
      },
      body: JSON.stringify({
        session_id: this.sessionId
      })
    });

    if (!response.ok) {
      throw new Error('Failed to end session');
    }

    const summary = await response.json();

    // Clear session state
    this.sessionId = null;
    this.startedAt = null;

    return summary;
  }

  getToken() {
    // Your authentication token retrieval logic
    return localStorage.getItem('authToken');
  }
}

// Example usage
const practiceSession = new PracticeSessionManager();

// Start session
await practiceSession.startSession('practice');

// Submit answers
for (const exercise of exercises) {
  const result = await practiceSession.submitAnswer(
    exercise.id,
    userAnswer,
    timeTaken
  );

  console.log(`Answer ${result.is_correct ? 'correct' : 'incorrect'}`);
}

// End session and get summary
const summary = await practiceSession.endSession();
console.log(`Final score: ${summary.score_percentage}%`);
console.log(`Duration: ${summary.duration_seconds}s`);
```

## Backward Compatibility

The system maintains backward compatibility:

- **Without session_id**: If no `session_id` is provided in answer submission, the system creates a standalone session (legacy behavior) with `total_exercises=1` and `is_completed=true`.

- **With session_id**: When `session_id` is provided, attempts are appended to the existing session with incremental updates.

## Database Schema

### Session Model (`sessions` table)

```python
class Session(Base):
    id: int                      # Primary key
    user_id: int                 # Foreign key to users
    started_at: datetime         # Session start time
    ended_at: datetime           # Session end time (null until ended)
    duration_seconds: int        # Calculated when session ends
    total_exercises: int         # Increments with each attempt
    correct_answers: int         # Increments when answer is correct
    score_percentage: float      # Recalculated after each attempt
    session_type: str            # "practice", "review", or "test"
    is_completed: bool           # False until session/end is called
```

### Attempt Model (`attempts` table)

```python
class Attempt(Base):
    id: int                      # Primary key
    session_id: int              # Foreign key to sessions
    user_id: int                 # Foreign key to users
    exercise_id: int             # Foreign key to exercises
    user_answer: str             # User's submitted answer
    is_correct: bool             # Whether answer was correct
    time_taken_seconds: int      # Time spent on this exercise
```

## Error Handling

### Session Not Found
```json
// Status: 404 Not Found
{
  "detail": "Session not found or does not belong to user"
}
```

### Session Already Completed
```json
// Status: 400 Bad Request
{
  "detail": "Session is already completed"
}
```

### Invalid Session Type
```json
// Status: 400 Bad Request
{
  "detail": "Invalid session_type. Must be one of: practice, review, test"
}
```

## Benefits

1. **Accurate Statistics**: Sessions now correctly track total exercises and score across multiple attempts
2. **Streak Calculations**: Session aggregation works properly for calculating learning streaks
3. **Performance Tracking**: Duration and completion metrics are accurate
4. **Analytics**: Better data for user progress reports and dashboards
5. **Backward Compatible**: Existing clients without session management still work (creates standalone sessions)

## Migration Notes

- Existing sessions in the database remain unchanged
- New frontend should adopt session management flow for proper tracking
- Legacy API calls (without session_id) continue to work but create individual sessions
- No database migration required; changes are additive

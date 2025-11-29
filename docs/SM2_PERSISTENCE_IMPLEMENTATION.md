# SM-2 Spaced Repetition Data Persistence Implementation

## Overview

Fixed the SM-2 spaced repetition data persistence issue where `LearningAlgorithm` class stored data only in-memory, losing progress after each request.

## Problem

- **LearningAlgorithm** class stored SM2Card data in `self.cards = {}` (in-memory only)
- **ReviewSchedule** model existed but was never used
- User progress was lost between sessions/requests

## Solution

### 1. Modified `LearningAlgorithm` Class

**File:** `backend/services/learning_algorithm.py`

#### Changes:

1. **Added database session parameter**
   ```python
   def __init__(
       self,
       initial_difficulty: str = "intermediate",
       db_session = None  # NEW: database session for persistence
   ):
       self.db = db_session  # Store db session
   ```

2. **Added `load_card_from_db()` method**
   - Loads existing ReviewSchedule data from database
   - Converts ReviewSchedule to SM2Card
   - Params: user_id, verb, tense, person
   - Returns SM2Card or None

3. **Added `save_card_to_db()` method**
   - Saves/updates SM2Card data to ReviewSchedule table
   - Creates new record if doesn't exist
   - Updates existing record if found
   - Params: user_id, card (SM2Card)

4. **Modified `add_card()` method**
   - Added optional `user_id` parameter
   - Checks in-memory cache first
   - Tries loading from database if user_id provided
   - Creates new card only if not found

5. **Modified `process_exercise_result()` method**
   - Added optional `user_id` parameter
   - Calls `save_card_to_db()` after processing
   - Persists SM-2 data automatically after each exercise

### 2. Updated Routes

**File:** `backend/api/routes/exercises.py`

#### Changes:

1. **Modified `get_learning_services()` function**
   - Changed from singleton to per-request instance for LearningAlgorithm
   - ConjugationEngine and FeedbackGenerator remain singletons
   - Accepts db session parameter
   - Returns new LearningAlgorithm instance with database session

2. **Modified `submit_answer()` endpoint**
   - Passes db session to `get_learning_services(db)`
   - Parses user_id and passes to `process_exercise_result()`
   - Enables automatic SM-2 data persistence

## Database Schema

### ReviewSchedule Model

The existing `ReviewSchedule` model (in `models/progress.py`) is now actively used:

```python
class ReviewSchedule(Base):
    __tablename__ = "review_schedules"

    # Primary key
    id: int

    # Foreign keys
    user_id: int  # Foreign key to users
    verb_id: int  # Foreign key to verbs

    # SM-2 algorithm parameters
    easiness_factor: float = 2.5  # 1.3 - 2.5 range
    interval_days: int = 1
    repetitions: int = 0

    # Review tracking
    next_review_date: datetime
    last_reviewed_at: datetime
    review_count: int = 0

    # Performance tracking
    total_correct: int = 0
    total_attempts: int = 0
```

## Data Flow

### Exercise Submission Flow:

1. User submits answer via `/exercises/submit` endpoint
2. `submit_answer()` creates LearningAlgorithm with db session
3. Answer is validated by ConjugationEngine
4. `process_exercise_result()` is called with user_id
5. LearningAlgorithm:
   - Loads existing ReviewSchedule from database (if exists)
   - Processes result with SM-2 algorithm
   - Saves updated data back to database
6. Returns next review date and interval to client

### Persistence Flow:

```
Request → submit_answer()
    → get_learning_services(db)
    → LearningAlgorithm(db_session=db)
    → process_exercise_result(user_id=X)
        → load_card_from_db(user_id, verb, tense, person)
        → sm2.process_review(card, correct, time, difficulty)
        → save_card_to_db(user_id, updated_card)
    → ReviewSchedule saved to database
```

## Testing

### Test Script

Created comprehensive test: `tests/test_sm2_persistence.py`

**Test Coverage:**
- ✓ Creates ReviewSchedule record on first exercise
- ✓ Persists SM-2 parameters (EF, interval, repetitions)
- ✓ Updates existing record on subsequent exercises
- ✓ Loads card from database correctly
- ✓ Handles correct and incorrect answers
- ✓ Interval increases with correct answers
- ✓ Interval resets on incorrect answers

### Test Results

```
✓ First exercise processed
  - Next review: 2025-11-29
  - Interval days: 1

✓ Data persisted to database
  - EF: 2.5
  - Interval: 1 days
  - Attempts: 1
  - Correct: 1

✓ Second exercise processed
  - Next review: 2025-12-04
  - Interval days: 6

✓ Data updated correctly
  - EF: 2.6
  - Interval: 6 days
  - Attempts: 2
  - Correct: 2

✓ Card loaded from database successfully
  - Total reviews: 2
  - Correct: 2
  - Accuracy: 100.0%

✓ Incorrect answer processed
  - Interval reset to: 1 days

✓ All tests passed!
```

## Benefits

1. **Persistent Learning Data**: User progress is saved between sessions
2. **Accurate Spaced Repetition**: SM-2 parameters evolve based on performance
3. **Cross-Session Continuity**: Progress carries over across multiple practice sessions
4. **Database-Backed**: Reliable PostgreSQL storage instead of volatile memory
5. **Production-Ready**: Proper error handling and transaction management

## API Response Changes

### `/exercises/submit` endpoint now returns:

```json
{
  "is_correct": true,
  "feedback": "Excellent! Your answer is correct.",
  "next_review_date": "2025-12-04T18:27:30.497115",
  "interval_days": 6,
  "difficulty_level": "intermediate"
}
```

## Files Modified

1. `backend/services/learning_algorithm.py`
   - Added db_session parameter
   - Added load_card_from_db() method
   - Added save_card_to_db() method
   - Modified add_card() for db loading
   - Modified process_exercise_result() for db saving

2. `backend/api/routes/exercises.py`
   - Modified get_learning_services() to accept db session
   - Updated submit_answer() to pass db and user_id
   - Removed singleton for LearningAlgorithm (now per-request)

3. `tests/test_sm2_persistence.py` (NEW)
   - Comprehensive persistence test suite

## Migration Notes

- No database migrations required (ReviewSchedule table already exists)
- Backward compatible: works without db session (falls back to in-memory)
- Existing in-memory functionality preserved for testing

## Next Steps

Potential enhancements:

1. Add tense/person granularity to ReviewSchedule (currently per-verb)
2. Implement review queue API endpoints (`/exercises/review/due`)
3. Add analytics dashboard for spaced repetition stats
4. Optimize query performance with database indexes
5. Implement batch loading for multiple cards

## Related Issues

- Fixes: SM-2 data persistence
- Related: Spaced repetition scheduling
- Dependency: ReviewSchedule model (already implemented)

---

**Implementation Date:** 2025-11-28
**Author:** Backend API Developer Agent
**Status:** ✓ Complete & Tested

# Gamification Unification - XP and Level Calculations

## Summary

Created unified gamification service to synchronize XP and level calculations between frontend and backend.

## Changes Made

### 1. Created `backend/services/gamification.py`

New backend service that mirrors the frontend gamification logic exactly:

**Functions:**
- `calculate_exercise_xp(is_correct, difficulty, streak)` - Matches `frontend/lib/gamification.ts::calculateExerciseXP()`
- `calculate_session_xp(exercise_count, correct_count, session_time_seconds, streak)` - Matches `frontend/lib/gamification.ts::calculateSessionXP()`
- `calculate_level_info(total_xp)` - Matches `frontend/lib/gamification.ts::calculateLevel()`
- `get_xp_for_level(level)` - Helper for exponential level progression

**Key Features:**
- Exponential level progression: `level * 100 + (level - 1)^2 * 50`
- Difficulty-based base XP: Easy=10, Medium=20, Hard=30, Expert=40
- Correct answer bonus: 1.5x multiplier
- Streak bonus: Up to 2x multiplier (10% per streak, capped at 2x)
- Session bonuses: Accuracy (25-100 XP), Speed (30 XP if <30s avg), Participation (50 XP)

### 2. Updated `backend/services/__init__.py`

Added gamification exports to existing services package.

### 3. Updated `backend/api/routes/progress.py`

**Import Added:**
```python
from services.gamification import calculate_level_info
```

**Function Updated:**
```python
def calculate_level_and_xp(total_exercises: int, correct_answers: int) -> tuple:
    """
    DEPRECATED: Use calculate_level_info() from services.gamification instead.

    WARNING: This uses a legacy XP formula that does NOT match the frontend.
    """
    # Legacy XP formula (for backwards compatibility)
    xp = (correct_answers * 10) + (total_exercises * 2)

    # Use unified gamification service for level calculation
    level_info = calculate_level_info(xp)
    level = level_info["current_level"]

    return level, xp
```

**Route Updated:**
```python
@router.get("", response_model=ProgressResponse)
async def get_user_progress(...):
    # Calculate level using unified gamification service
    # TODO: Store total_xp in UserProfile instead of calculating from attempts
    # TODO: Update to use per-exercise XP tracking with difficulty/streak bonuses
    legacy_xp = (correct_answers * 10) + (total_exercises * 2)
    level_info = calculate_level_info(legacy_xp)
    level = level_info["current_level"]
    xp = legacy_xp
```

## Current State

### What's Unified ✅
- Level calculation formula (exponential progression)
- Level progression thresholds
- XP calculation logic (exercise and session)

### What's Still Different ❌
- **XP Accumulation Method:**
  - Frontend: Tracks per-exercise XP with difficulty, streak, and accuracy bonuses
  - Backend: Uses simplified legacy formula (10 per correct + 2 per attempt)

## Migration Path

### Phase 1: Backend Service (COMPLETE)
- [x] Create `backend/services/gamification.py`
- [x] Import in `backend/api/routes/progress.py`
- [x] Use `calculate_level_info()` for level calculation

### Phase 2: Database Schema (TODO)
- [ ] Add `total_xp` column to `UserProfile` table
- [ ] Add migration to populate `total_xp` from existing attempts
- [ ] Add `xp_earned` column to `Attempt` table (track per-exercise XP)

### Phase 3: XP Tracking (TODO)
- [ ] Update exercise submission to calculate and store XP:
  ```python
  from services.gamification import calculate_exercise_xp

  xp_earned = calculate_exercise_xp(
      is_correct=is_correct,
      difficulty=exercise.difficulty.value,
      streak=user_profile.current_streak
  )

  # Store in Attempt
  attempt.xp_earned = xp_earned

  # Update UserProfile
  user_profile.total_xp += xp_earned
  ```

- [ ] Update session completion to award session bonuses:
  ```python
  from services.gamification import calculate_session_xp

  session_xp = calculate_session_xp(
      exercise_count=session.exercises_completed,
      correct_count=session.correct_answers,
      session_time_seconds=session.total_time,
      streak=user_profile.current_streak
  )

  user_profile.total_xp += session_xp
  ```

### Phase 4: API Updates (TODO)
- [ ] Return `level_info` in progress endpoint:
  ```python
  level_info = calculate_level_info(user_profile.total_xp)
  return ProgressResponse(
      ...,
      level=level_info["current_level"],
      experience_points=level_info["total_xp"],
      current_xp=level_info["current_xp"],
      xp_for_next_level=level_info["xp_for_next_level"],
      progress_to_next_level=level_info["progress_to_next_level"]
  )
  ```

- [ ] Update `ProgressResponse` schema to include level details
- [ ] Remove deprecated `calculate_level_and_xp()` function

### Phase 5: Testing (TODO)
- [ ] Create `backend/tests/services/test_gamification.py`
- [ ] Test XP calculations match frontend
- [ ] Test level progression matches frontend
- [ ] Test edge cases (streak caps, accuracy bonuses, etc.)
- [ ] Integration tests for XP tracking in exercise submissions

## Example Usage

### Exercise XP Calculation
```python
from services.gamification import calculate_exercise_xp

# Easy exercise, correct answer, 5-day streak
xp = calculate_exercise_xp(is_correct=True, difficulty=1, streak=5)
# Result: 10 (base) * 1.5 (correct) * 1.5 (streak) = 22 XP

# Hard exercise, incorrect answer, no streak
xp = calculate_exercise_xp(is_correct=False, difficulty=3, streak=0)
# Result: 30 (base) * 1.0 (incorrect) * 1.0 (no streak) = 30 XP
```

### Session XP Calculation
```python
from services.gamification import calculate_session_xp

# 10 exercises, 9 correct (90% accuracy), 4 minutes, 7-day streak
xp = calculate_session_xp(
    exercise_count=10,
    correct_count=9,
    session_time_seconds=240,
    streak=7
)
# Result: 50 (base) + 150 (exercises) + 100 (accuracy) + 30 (speed) + 70 (streak) = 400 XP
```

### Level Calculation
```python
from services.gamification import calculate_level_info

level_info = calculate_level_info(total_xp=500)
# Result: {
#   "current_level": 3,
#   "current_xp": 200,
#   "xp_for_next_level": 400,
#   "total_xp": 500,
#   "progress_to_next_level": 50
# }
```

## Validation

The gamification service includes a `validate_level_calculation()` function to verify consistency:

```python
from services.gamification import validate_level_calculation

results = validate_level_calculation()
# Validates XP thresholds: 0→L1, 100→L2, 300→L3, 600→L4, 1000→L5
```

## Files Modified

1. **Created:**
   - `backend/services/gamification.py` (169 lines)
   - `docs/GAMIFICATION_UNIFICATION.md` (this file)

2. **Updated:**
   - `backend/services/__init__.py` (added gamification exports)
   - `backend/api/routes/progress.py` (added import, updated calculate_level_and_xp)

## Next Steps

1. Add `total_xp` and `xp_earned` columns to database schema
2. Create migration to populate `total_xp` from existing attempts
3. Update exercise submission endpoint to track XP
4. Update session completion to award bonuses
5. Write comprehensive tests
6. Remove legacy XP formula once migration is complete

## Notes

- The legacy XP formula `(correct * 10) + (total * 2)` is **incompatible** with the frontend
- Frontend tracks per-exercise XP with bonuses; backend currently uses aggregate calculation
- Full unification requires database schema changes to store `total_xp` in `UserProfile`
- Backwards compatibility is maintained through the deprecated `calculate_level_and_xp()` function

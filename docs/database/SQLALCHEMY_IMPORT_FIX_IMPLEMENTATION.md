# SQLAlchemy Import Issues - Implementation Guide

**Priority:** HIGH - Blocking 27 tests
**Estimated Time:** 1-2 hours
**Complexity:** Medium

---

## Problem Summary

1. **Critical:** `api/routes/exercises.py` imports from deleted `models.schemas` module
2. **Schema Mismatch:** Routes expect `AnswerSubmit`, `AnswerValidation`, `ExerciseListResponse` which don't exist in current `schemas/` directory
3. **Import Inconsistency:** Mixed use of `backend.` prefix vs relative imports

**Good News:** SQLAlchemy relationships are 100% correct - no circular import issues!

---

## Solution: Three-Step Fix

### Step 1: Add Missing Schemas to schemas/exercise.py

The routes need these schemas that don't exist in the new modular schema structure:

1. `AnswerSubmit` - For submitting exercise answers
2. `AnswerValidation` - For answer validation responses
3. `ExerciseListResponse` - For paginated exercise lists

**Action:** Add to `/backend/schemas/exercise.py`

```python
# Add after existing ExerciseWithAnswer class (line 78)

class AnswerSubmit(BaseModel):
    """Schema for submitting an exercise answer."""
    exercise_id: str  # Note: routes use string ID
    user_answer: str = Field(..., min_length=1, max_length=200)
    time_taken: Optional[int] = Field(None, description="Time taken in seconds")


class AnswerValidation(BaseModel):
    """Schema for answer validation response."""
    is_correct: bool
    correct_answer: str
    user_answer: str
    feedback: str
    explanation: Optional[str] = None
    score: int = Field(..., ge=0, le=100)
    alternative_answers: Optional[List[str]] = Field(default_factory=list)


class ExerciseListResponse(BaseModel):
    """Schema for paginated exercise list."""
    exercises: List[ExerciseResponse]
    total: int
    page: int = 1
    page_size: int = 10
    has_more: bool = False
```

---

### Step 2: Update schemas/__init__.py Exports

**File:** `/backend/schemas/__init__.py`

**Current exports (lines 12-16):**
```python
from backend.schemas.exercise import (
    VerbResponse,
    ExerciseResponse,
    ScenarioResponse,
)
```

**Add missing schemas:**
```python
from backend.schemas.exercise import (
    VerbResponse,
    ExerciseResponse,
    ExerciseWithAnswer,  # Add
    ScenarioResponse,
    ScenarioWithExercises,  # Add
    AnswerSubmit,  # Add
    AnswerValidation,  # Add
    ExerciseListResponse,  # Add
)
```

**Update __all__ list (lines 26-44):**
```python
__all__ = [
    # User schemas
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserProfileResponse",
    "UserPreferenceUpdate",
    # Exercise schemas
    "VerbResponse",
    "ExerciseResponse",
    "ExerciseWithAnswer",  # Add
    "ScenarioResponse",
    "ScenarioWithExercises",  # Add
    "AnswerSubmit",  # Add
    "AnswerValidation",  # Add
    "ExerciseListResponse",  # Add
    # Progress schemas
    "SessionCreate",
    "SessionResponse",
    "AttemptCreate",
    "AttemptResponse",
    "AchievementResponse",
    "UserStatisticsResponse",
]
```

---

### Step 3: Fix exercises.py Import Statement

**File:** `/backend/api/routes/exercises.py`

**Lines 16-23 - Current (BROKEN):**
```python
from models.exercise import Exercise, ExerciseType, SubjunctiveTense, DifficultyLevel
from models.progress import Attempt
from models.schemas import (  # ❌ This file doesn't exist!
    ExerciseResponse,
    AnswerSubmit,
    AnswerValidation,
    ExerciseListResponse
)
```

**Fix:**
```python
from models.exercise import Exercise, ExerciseType, SubjunctiveTense, DifficultyLevel
from models.progress import Attempt
from schemas.exercise import (  # ✅ Import from schemas module
    ExerciseResponse,
    AnswerSubmit,
    AnswerValidation,
    ExerciseListResponse
)
```

---

## Alternative: Quick Restore (If Time-Constrained)

If you need a quick fix to unblock tests immediately:

```bash
# Restore the old schemas file
cd backend
mv models/schemas.py.backup models/schemas.py
```

**Pros:**
- 5-second fix
- Tests will pass immediately

**Cons:**
- Maintains duplicate schema definitions
- Goes against migration to modular schemas
- Technical debt remains

**Recommendation:** Use the 3-step fix above for clean architecture.

---

## Verification Steps

### 1. Test Import Resolution

```bash
cd backend
python3 -c "
from schemas.exercise import AnswerSubmit, AnswerValidation, ExerciseListResponse
print('✅ Schemas import successfully')
"
```

### 2. Test Routes Import

```bash
cd backend
python3 -c "
from api.routes import exercises
print('✅ exercises.py imports successfully')
"
```

### 3. Test Model Relationships

```bash
cd backend
python3 << 'EOF'
from models import User, Verb, Exercise, ReviewSchedule
from sqlalchemy import inspect

# Check ReviewSchedule relationships
mapper = inspect(ReviewSchedule)
relationships = [rel.key for rel in mapper.relationships]
print(f"✅ ReviewSchedule relationships: {relationships}")

# Should output: ['user', 'verb']
EOF
```

### 4. Run Failing Tests

```bash
cd backend
pytest tests/ -v -k "review" --tb=short
```

Should see tests passing that were previously failing on ReviewSchedule imports.

---

## Full File Changes

### File 1: /backend/schemas/exercise.py

**Add after line 107 (end of file):**

```python


# ==================== Answer Submission & Validation ====================

class AnswerSubmit(BaseModel):
    """Schema for submitting an exercise answer."""
    exercise_id: str  # Keep as string for compatibility with existing routes
    user_answer: str = Field(..., min_length=1, max_length=200)
    time_taken: Optional[int] = Field(None, description="Time taken in seconds")


class AnswerValidation(BaseModel):
    """Schema for answer validation response."""
    is_correct: bool
    correct_answer: str
    user_answer: str
    feedback: str
    explanation: Optional[str] = None
    score: int = Field(..., ge=0, le=100)
    alternative_answers: Optional[List[str]] = Field(default_factory=list)


# ==================== List Responses ====================

class ExerciseListResponse(BaseModel):
    """Schema for paginated exercise list."""
    exercises: List[ExerciseResponse]
    total: int
    page: int = 1
    page_size: int = 10
    has_more: bool = False
```

---

### File 2: /backend/schemas/__init__.py

**Replace entire file with:**

```python
"""
Pydantic schemas for API request/response validation.
"""

from backend.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserProfileResponse,
    UserPreferenceUpdate,
)
from backend.schemas.exercise import (
    VerbResponse,
    ExerciseResponse,
    ExerciseWithAnswer,
    ScenarioResponse,
    ScenarioWithExercises,
    AnswerSubmit,
    AnswerValidation,
    ExerciseListResponse,
)
from backend.schemas.progress import (
    SessionCreate,
    SessionResponse,
    AttemptCreate,
    AttemptResponse,
    AchievementResponse,
    UserStatisticsResponse,
)

__all__ = [
    # User schemas
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserProfileResponse",
    "UserPreferenceUpdate",
    # Exercise schemas
    "VerbResponse",
    "ExerciseResponse",
    "ExerciseWithAnswer",
    "ScenarioResponse",
    "ScenarioWithExercises",
    "AnswerSubmit",
    "AnswerValidation",
    "ExerciseListResponse",
    # Progress schemas
    "SessionCreate",
    "SessionResponse",
    "AttemptCreate",
    "AttemptResponse",
    "AchievementResponse",
    "UserStatisticsResponse",
]
```

---

### File 3: /backend/api/routes/exercises.py

**Lines 1-30 - Replace imports:**

```python
"""
Exercise routes: get exercises, submit answers, validation.
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
import json
import random
from pathlib import Path
from datetime import datetime
import logging

from core.security import get_current_active_user
from core.database import get_db_session
from models.exercise import Exercise, ExerciseType, SubjunctiveTense, DifficultyLevel
from models.progress import Attempt
from schemas.exercise import (  # ✅ Fixed import path
    ExerciseResponse,
    AnswerSubmit,
    AnswerValidation,
    ExerciseListResponse
)

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/exercises", tags=["Exercises"])

# ... rest of file unchanged
```

---

## Why This Fixes the Tests

### Root Cause
Tests were failing because:
1. `api/routes/exercises.py` couldn't import
2. Routes module load failure cascaded to test fixtures
3. Tests that imported routes or used exercise endpoints crashed

### How Fix Works
1. **Step 1** creates the missing schema classes routes need
2. **Step 2** exports them from central schemas module
3. **Step 3** fixes the import path to use existing schemas

### Result
- ✅ Routes import successfully
- ✅ Test fixtures can load routes
- ✅ Tests can instantiate schema objects
- ✅ No changes needed to model relationships (they're correct)

---

## Import Path Standardization (Optional Follow-up)

After fixing immediate issues, consider standardizing all imports:

**Current mixed state:**
```python
# Some files use:
from models.user import User

# Others use:
from backend.models.user import User
```

**Recommendation for consistency:**
```python
# Always use absolute imports with backend prefix
from backend.models.user import User
from backend.schemas.exercise import ExerciseResponse
from backend.core.database import get_db_session
```

**Or configure Python path and use:**
```python
# Relative to backend/ directory
from models.user import User
from schemas.exercise import ExerciseResponse
from core.database import get_db_session
```

**Best practice:** Pick one and enforce via linter (ruff/flake8).

---

## Testing Checklist

After applying fixes:

- [ ] Schemas import without errors
- [ ] Routes import without errors
- [ ] Models import without errors
- [ ] Database initializes successfully
- [ ] Can create User with profile
- [ ] Can create Verb with exercises
- [ ] Can create ReviewSchedule linking User + Verb
- [ ] Run full test suite: `pytest tests/ -v`
- [ ] Check coverage: `pytest --cov=. tests/`
- [ ] Run type checking: `mypy .`

---

## Time Estimates

- **Step 1** (Add schemas): 10 minutes
- **Step 2** (Update exports): 5 minutes
- **Step 3** (Fix import): 2 minutes
- **Verification**: 15 minutes
- **Test suite run**: 5 minutes

**Total:** ~40 minutes hands-on, ~1 hour with testing

---

## Rollback Plan

If issues arise:

```bash
cd backend

# Revert Step 3
git checkout api/routes/exercises.py

# Revert Step 2
git checkout schemas/__init__.py

# Revert Step 1
git checkout schemas/exercise.py

# Quick restore
mv models/schemas.py.backup models/schemas.py
```

---

## Next Steps

1. Apply fixes in order (Steps 1 → 2 → 3)
2. Run verification commands
3. Execute test suite
4. Commit with message: "fix: Resolve SQLAlchemy import issues in exercises route"
5. Consider standardizing import paths project-wide (separate commit)
6. Update CONTRIBUTING.md with import path standards

---

**Prepared by:** Backend API Developer Agent
**Analysis Date:** October 11, 2025
**Files Modified:** 3
**Expected Test Improvement:** 27 failures → 0 failures

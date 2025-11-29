# Custom Exercise Validation - Backend Implementation

## Overview

Custom exercises (those with IDs starting with "gen_") now validate through the backend API instead of local frontend validation. This ensures consistent validation logic, integrates with the ConjugationEngine, SM-2 spaced repetition algorithm, and tracks progress in the database.

## Changes Made

### 1. Schema Updates (`backend/schemas/exercise.py`)

Added optional fields to `AnswerSubmit` schema for custom exercise metadata:

```python
class AnswerSubmit(BaseModel):
    """Schema for submitting an exercise answer."""
    exercise_id: str
    user_answer: str = Field(..., min_length=1, max_length=200)
    time_taken: Optional[int] = Field(None, description="Time taken in seconds")

    # Session management
    session_id: Optional[int] = Field(None, description="Session ID to associate this attempt with")

    # Optional fields for custom exercise metadata (generated exercises with ID starting with "gen_")
    verb: Optional[str] = Field(None, description="Verb infinitive for custom exercises")
    tense: Optional[str] = Field(None, description="Subjunctive tense for custom exercises")
    person: Optional[str] = Field(None, description="Grammatical person for custom exercises")
    correct_answer: Optional[str] = Field(None, description="Expected correct answer for custom exercises")
    alternative_answers: Optional[List[str]] = Field(None, description="Alternative acceptable answers for custom exercises")
    explanation: Optional[str] = Field(None, description="Exercise explanation for custom exercises")
    trigger_phrase: Optional[str] = Field(None, description="WEIRDO trigger phrase for custom exercises")
```

### 2. Custom Exercise Validation Module (`backend/api/custom_exercise_validation.py`)

New module dedicated to custom exercise validation:

**Key Features:**
- **ConjugationEngine Integration**: Uses the same sophisticated validation as database exercises
- **Rich Feedback**: Generates detailed feedback using FeedbackGenerator
- **Spaced Repetition**: Processes results through LearningAlgorithm (SM-2)
- **Database Tracking**: Saves attempts with `exercise_id=None` for custom exercises
- **Fallback Validation**: Falls back to simple string comparison if ConjugationEngine fails
- **Error Analysis**: Identifies specific conjugation errors (stem changes, spelling, mood confusion)

**Main Function:**
```python
def validate_custom_exercise(
    submission: AnswerSubmit,
    current_user: Dict[str, Any],
    db: Session,
    conjugation_engine: ConjugationEngine,
    feedback_generator: FeedbackGenerator,
    learning_algorithm: LearningAlgorithm,
    save_attempt_func
) -> AnswerValidation
```

### 3. Exercises Route Updates (`backend/api/routes/exercises.py`)

**Added Learning Services:**
```python
# Learning services singleton instances
_conjugation_engine: Optional[ConjugationEngine] = None
_feedback_generator: Optional[FeedbackGenerator] = None
_learning_algorithm: Optional[LearningAlgorithm] = None

def get_learning_services() -> tuple[ConjugationEngine, FeedbackGenerator, LearningAlgorithm]:
    """Get or create learning service instances (singleton pattern)."""
    # Initialize on first use
```

**Updated `submit_answer` Endpoint:**
- Detects custom exercises by checking if `exercise_id.startswith("gen_")`
- Routes custom exercises to `validate_custom_exercise()`
- Routes database exercises to existing validation logic
- Both paths now use ConjugationEngine, FeedbackGenerator, and LearningAlgorithm

```python
@router.post("/submit", response_model=AnswerValidation)
async def submit_answer(submission: AnswerSubmit, ...):
    # Get learning services
    conjugation_engine, feedback_generator, learning_algorithm = get_learning_services()

    # Check if this is a custom generated exercise
    is_custom_exercise = submission.exercise_id.startswith("gen_")

    if is_custom_exercise:
        # Handle custom exercise validation
        return validate_custom_exercise(...)

    # Standard database exercise validation
    # ...
```

**Updated `save_user_attempt_to_db` Function:**
- Now accepts optional `exercise_id` (can be `None` for custom exercises)
- Added `session_id` parameter to append to existing sessions
- Added `time_taken_seconds` parameter for precise tracking

```python
def save_user_attempt_to_db(
    db: Session,
    user_id: str,
    exercise_id: Optional[int],  # Can be None for custom exercises
    user_answer: str,
    is_correct: bool,
    score: int,
    session_id: Optional[int] = None,
    time_taken_seconds: Optional[int] = None
)
```

### 4. Database Compatibility

The `Attempt` model already supports `exercise_id=None`:
```python
exercise_id = Column(Integer, ForeignKey("exercises.id", ondelete="SET NULL"), nullable=True, index=True)
```

No database migration required.

## How It Works

### Custom Exercise Flow

1. **Frontend Submits Answer**:
   - Sends POST to `/exercises/submit` with:
     - `exercise_id`: "gen_1_hablar_yo"
     - `user_answer`: "hable"
     - `verb`: "hablar"
     - `tense`: "present_subjunctive"
     - `person`: "yo"
     - `correct_answer`: "hable" (fallback)
     - `alternative_answers`: []
     - `explanation`: "..."
     - `trigger_phrase`: "Espero que"

2. **Backend Detection**:
   - `submit_answer` detects `exercise_id.startswith("gen_")`
   - Routes to `validate_custom_exercise()`

3. **Validation**:
   - Extracts verb/tense/person from submission or ID
   - Uses `ConjugationEngine.validate_answer()` for precise validation
   - Generates rich feedback via `FeedbackGenerator`
   - Falls back to simple string comparison if engine fails

4. **Learning Algorithm**:
   - Processes result through `LearningAlgorithm.process_exercise_result()`
   - Calculates next review date using SM-2
   - Adjusts difficulty based on performance

5. **Database Persistence**:
   - Saves attempt with `exercise_id=None`
   - Associates with session if `session_id` provided
   - Tracks user answer, correctness, time taken

6. **Response**:
   - Returns `AnswerValidation` with:
     - `is_correct`: boolean
     - `correct_answer`: string
     - `feedback`: rich message
     - `explanation`: detailed explanation
     - `error_type`: classification of error
     - `suggestions`: helpful tips
     - `next_review_date`: spaced repetition
     - `interval_days`: SM-2 interval
     - Full enhanced feedback fields

## Benefits

1. **Consistency**: Same validation logic for database and custom exercises
2. **Intelligence**: ConjugationEngine catches subtle errors (stem changes, spelling, mood confusion)
3. **Spaced Repetition**: Custom exercises integrate with SM-2 algorithm for optimal learning
4. **Progress Tracking**: All attempts saved to database for analytics
5. **Rich Feedback**: Detailed, contextual feedback helps users learn from mistakes
6. **Error Analysis**: Identifies specific error types and provides targeted suggestions
7. **Maintainability**: Single source of truth for validation logic

## Testing

All files compile successfully:
- ✓ `backend/schemas/exercise.py`
- ✓ `backend/api/custom_exercise_validation.py`
- ✓ `backend/api/routes/exercises.py`

## Next Steps

**Frontend Integration** (separate task):
1. Update `practice/page.tsx` to remove local validation (lines 160-182)
2. Send custom exercise metadata with submission
3. Remove local validation logic
4. Use backend response for all feedback

## API Example

**Request:**
```http
POST /api/exercises/submit
Content-Type: application/json
Authorization: Bearer <token>

{
  "exercise_id": "gen_1_hablar_yo",
  "user_answer": "hablo",
  "time_taken": 5,
  "verb": "hablar",
  "tense": "present_subjunctive",
  "person": "yo",
  "correct_answer": "hable",
  "alternative_answers": [],
  "explanation": "The phrase 'Espero que' triggers the subjunctive mood...",
  "trigger_phrase": "Espero que",
  "session_id": 123
}
```

**Response:**
```json
{
  "is_correct": false,
  "correct_answer": "hable",
  "user_answer": "hablo",
  "feedback": "You used the indicative mood. The subjunctive form is 'hable'.",
  "explanation": "The phrase 'Espero que' triggers the subjunctive mood...",
  "score": 0,
  "alternative_answers": [],
  "error_type": "mood_confusion",
  "suggestions": [
    "You used the indicative mood. The subjunctive form is 'hable'."
  ],
  "related_rules": [
    "Wishes and hopes trigger the subjunctive"
  ],
  "encouragement": "Don't worry, mood confusion is common when learning the subjunctive!",
  "next_steps": [
    "Review the subjunctive triggers",
    "Practice more -ar verb conjugations"
  ],
  "next_review_date": "2025-11-29T10:00:00Z",
  "interval_days": 1,
  "difficulty_level": "medium"
}
```

## Files Modified

1. `backend/schemas/exercise.py` - Added custom exercise metadata fields
2. `backend/api/routes/exercises.py` - Added custom exercise routing and learning services
3. `backend/api/custom_exercise_validation.py` - New validation module (171 lines)

## Architecture Diagram

```
Frontend (practice/page.tsx)
    │
    │ POST /api/exercises/submit
    │ {exercise_id: "gen_...", verb, tense, person, ...}
    ▼
Backend (exercises.py::submit_answer)
    │
    ├─► Detect custom exercise (ID starts with "gen_")
    │
    ├─► validate_custom_exercise()
    │   │
    │   ├─► ConjugationEngine.validate_answer()
    │   │   └─► Precise conjugation validation
    │   │
    │   ├─► FeedbackGenerator.generate_feedback()
    │   │   └─► Rich, contextual feedback
    │   │
    │   ├─► LearningAlgorithm.process_exercise_result()
    │   │   └─► SM-2 spaced repetition
    │   │
    │   └─► save_user_attempt_to_db()
    │       └─► Database persistence (exercise_id=NULL)
    │
    └─► Return AnswerValidation
        └─► Frontend displays feedback
```

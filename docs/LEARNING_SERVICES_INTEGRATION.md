# Learning Services Integration

## Overview

The exercise submission endpoint (`POST /exercises/submit`) has been enhanced to integrate three core learning services:

1. **ConjugationEngine** - Advanced Spanish subjunctive conjugation validation
2. **FeedbackGenerator** - Intelligent, context-aware feedback with error analysis
3. **LearningAlgorithm** - SM-2 spaced repetition scheduling and adaptive difficulty

## Integration Architecture

### File Structure

- **Main Implementation**: `backend/api/routes/exercises_integrated.py`
- **Current File**: `backend/api/routes/exercises.py` (to be replaced)
- **Services**:
  - `backend/services/conjugation.py`
  - `backend/services/feedback.py`
  - `backend/services/learning_algorithm.py`

### Service Initialization

Services are initialized using a singleton pattern to avoid redundant loading:

```python
def get_learning_services() -> tuple[ConjugationEngine, FeedbackGenerator, LearningAlgorithm]:
    """Get or create learning service instances (singleton pattern)."""
    global _conjugation_engine, _feedback_generator, _learning_algorithm

    if _conjugation_engine is None:
        _conjugation_engine = ConjugationEngine()
        _feedback_generator = FeedbackGenerator(_conjugation_engine)
        _learning_algorithm = LearningAlgorithm()

    return _conjugation_engine, _feedback_generator, _learning_algorithm
```

## Key Features

### 1. Intelligent Validation

**Fallback Strategy**:
- **Primary**: ConjugationEngine validation when verb information is available
- **Fallback**: Simple string comparison when verb data is missing

**Person Extraction**:
```python
def extract_person_from_prompt(prompt: str) -> Optional[str]:
    """Extract grammatical person from exercise prompt."""
    # Looks for indicators like "yo", "tú", "él/ella", etc.
    # Returns "yo" as default if unclear
```

**Tense Mapping**:
```python
tense_map = {
    SubjunctiveTense.PRESENT: "present_subjunctive",
    SubjunctiveTense.IMPERFECT: "imperfect_subjunctive_ra",
    SubjunctiveTense.PRESENT_PERFECT: "present_subjunctive",
    SubjunctiveTense.PLUPERFECT: "imperfect_subjunctive_ra"
}
```

### 2. Rich Feedback Generation

**Context Building**:
```python
exercise_context = {
    "trigger_phrase": exercise.trigger_phrase,
    "trigger_category": extract_trigger_category(exercise.trigger_phrase),
    "explanation": exercise.explanation
}

rich_feedback = feedback_generator.generate_feedback(
    validation_result=validation_result,
    exercise_context=exercise_context,
    user_level="intermediate"
)
```

**Feedback Components**:
- `message`: Primary feedback message ("Excellent!" or "Not quite...")
- `explanation`: Detailed explanation of the error or success
- `error_category`: Type of error (mood_confusion, stem_change_error, etc.)
- `suggestions`: Targeted improvement suggestions
- `related_rules`: Grammar rules applicable to this exercise
- `encouragement`: Motivational message
- `next_steps`: Recommended follow-up actions

### 3. Spaced Repetition Integration

**SM-2 Algorithm Processing**:
```python
learning_result = learning_algorithm.process_exercise_result(
    verb=verb_infinitive,
    tense=tense,
    person=person,
    correct=is_correct,
    response_time_ms=response_time_ms,
    difficulty_felt=None  # Optional user input
)
```

**Returned Data**:
- `next_review_date`: ISO timestamp for next review
- `interval_days`: Days until next review (SM-2 interval)
- `difficulty_level`: Current adaptive difficulty level
- `card_updated`: Complete SM-2Card state

## Response Schema

### Enhanced AnswerValidation

**Base Fields** (existing):
- `is_correct: bool`
- `correct_answer: str`
- `user_answer: str`
- `feedback: str`
- `explanation: Optional[str]`
- `score: int` (0-100)
- `alternative_answers: List[str]`

**Enhanced Feedback** (NEW):
- `error_type: Optional[str]` - Error classification
- `suggestions: List[str]` - Targeted suggestions
- `related_rules: List[str]` - Grammar rules
- `encouragement: Optional[str]` - Motivational message
- `next_steps: List[str]` - Recommended actions

**Spaced Repetition** (NEW):
- `next_review_date: Optional[str]` - ISO timestamp
- `interval_days: Optional[int]` - Days until review
- `difficulty_level: Optional[str]` - Current difficulty

## Error Categories

The ConjugationEngine can detect and categorize the following error types:

1. **mood_confusion**: Used indicative instead of subjunctive
2. **wrong_person**: Correct conjugation but wrong grammatical person
3. **wrong_tense**: Correct mood but wrong tense
4. **stem_change_error**: Failed to apply stem change (e→ie, o→ue, etc.)
5. **spelling_change_error**: Failed to apply orthographic spelling change (c→qu, g→gu, etc.)
6. **wrong_ending**: Incorrect ending for verb type
7. **spelling_error**: Close match with minor spelling mistake
8. **unknown_error**: Unclassified error

## Trigger Category Detection

Automatically detects WEIRDO categories from trigger phrases:

```python
def extract_trigger_category(trigger_phrase: Optional[str]) -> Optional[str]:
    """Extract WEIRDO category from trigger phrase."""
    # Checks against WEIRDO_TRIGGERS data
    # Returns: Wishes, Emotions, Impersonal_Expressions,
    #          Recommendations, Doubt, Ojalá, etc.
```

## Usage Example

### Request

```json
POST /exercises/submit
{
  "exercise_id": "123",
  "user_answer": "hable",
  "time_taken": 8
}
```

### Response (Correct Answer)

```json
{
  "is_correct": true,
  "correct_answer": "hable",
  "user_answer": "hable",
  "feedback": "Excellent!",
  "explanation": "You correctly conjugated 'hablar' in the present subjunctive.",
  "score": 105,
  "alternative_answers": [],
  "error_type": null,
  "suggestions": [],
  "related_rules": [
    "'hablar' is a regular -ar verb",
    "Regular -ar verbs use -e ending for 'yo'"
  ],
  "encouragement": "Keep up the excellent work!",
  "next_steps": [
    "Continue practicing to reinforce this pattern",
    "Try more complex verbs to challenge yourself"
  ],
  "next_review_date": "2025-11-29T10:30:00Z",
  "interval_days": 1,
  "difficulty_level": "intermediate"
}
```

### Response (Incorrect Answer with Error Analysis)

```json
{
  "is_correct": false,
  "correct_answer": "sea",
  "user_answer": "es",
  "feedback": "Not quite. The correct answer is 'sea'.",
  "explanation": "You used the indicative mood, but this sentence requires the subjunctive. The trigger phrase 'espero que' signals hope/desire, which requires subjunctive.",
  "score": 0,
  "alternative_answers": [],
  "error_type": "mood_confusion",
  "suggestions": [
    "Review WEIRDO triggers that require subjunctive",
    "Practice recognizing 'Wishes' patterns",
    "Remember: subjunctive expresses doubt, emotion, or influence over others"
  ],
  "related_rules": [
    "Wishes: espero que",
    "'ser' is an irregular verb"
  ],
  "encouragement": "Don't worry, mistakes are part of learning!",
  "next_steps": [
    "Review WEIRDO trigger phrases",
    "Practice identifying subjunctive triggers in sentences",
    "Do 5 more exercises focusing on mood recognition"
  ],
  "next_review_date": "2025-11-28T12:00:00Z",
  "interval_days": 0,
  "difficulty_level": "intermediate"
}
```

## Deployment Steps

### 1. Test the Integration

```bash
# Run backend tests
cd backend
pytest tests/api/test_exercises.py -v

# Test the services independently
pytest tests/services/test_conjugation.py -v
pytest tests/services/test_feedback.py -v
pytest tests/services/test_learning_algorithm.py -v
```

### 2. Replace Current File

```bash
# Backup current file
cp backend/api/routes/exercises.py backend/api/routes/exercises.backup.py

# Deploy integrated version
cp backend/api/routes/exercises_integrated.py backend/api/routes/exercises.py
```

### 3. Restart Backend

```bash
# If using uvicorn directly
uvicorn main:app --reload

# If using npm scripts
npm run dev
```

### 4. Test API Endpoint

```bash
# Get auth token first
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass"}'

# Submit answer
curl -X POST http://localhost:8000/exercises/submit \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "exercise_id": "1",
    "user_answer": "hable",
    "time_taken": 5
  }'
```

## Performance Considerations

### Singleton Services

Services are initialized once and reused:
- **Memory**: ~5-10 MB for loaded grammar data
- **Init Time**: ~100-200ms on first call
- **Subsequent Calls**: <1ms overhead

### Fallback Strategy

If verb data is missing or validation fails:
- Automatically falls back to simple string comparison
- No user-facing errors
- Logs warning for debugging

### Graceful Degradation

Each service layer has independent error handling:
1. ConjugationEngine fails → Simple validation
2. FeedbackGenerator fails → Basic feedback
3. LearningAlgorithm fails → Skip spaced repetition

## Future Enhancements

### 1. User Difficulty Level

Currently hardcoded to "intermediate". Should be retrieved from user profile:

```python
user_level = current_user.get("proficiency_level", "intermediate")
rich_feedback = feedback_generator.generate_feedback(
    validation_result, exercise_context, user_level=user_level
)
```

### 2. Difficulty Felt Input

Add optional field to AnswerSubmit schema:

```python
class AnswerSubmit(BaseModel):
    exercise_id: str
    user_answer: str
    time_taken: Optional[int] = None
    difficulty_felt: Optional[int] = Field(None, ge=1, le=5)  # NEW
```

### 3. Person from Exercise Model

Add `person` field to Exercise model instead of extracting from prompt:

```python
class Exercise(Base):
    # ... existing fields ...
    person: Optional[String] = Column(String(50), nullable=True)
```

### 4. Persistent Learning State

Store learning algorithm state in database:
- Create `LearningCard` model
- Persist SM-2 cards across sessions
- Link to ReviewSchedule model

### 5. Batch Processing

Support submitting multiple exercises at once:

```python
@router.post("/submit-batch", response_model=List[AnswerValidation])
async def submit_answers_batch(submissions: List[AnswerSubmit], ...):
    # Process multiple submissions efficiently
    pass
```

## Troubleshooting

### Issue: Intelligent validation not working

**Symptoms**: Always falls back to simple validation

**Checks**:
1. Verify exercise has `verb_id` relationship: `exercise.verb is not None`
2. Check verb table is seeded: `SELECT COUNT(*) FROM verbs;`
3. Ensure prompt contains person indicator: "yo", "tú", etc.
4. Check logs for extraction failures

### Issue: Learning algorithm not updating

**Symptoms**: `next_review_date` is always null

**Checks**:
1. Verify `use_intelligent_validation = True`
2. Check `verb_infinitive` and `person` are not None
3. Review logs for learning algorithm exceptions
4. Ensure time_taken is provided or defaults to 5000ms

### Issue: Error type always "unknown_error"

**Symptoms**: No specific error categorization

**Checks**:
1. Verify ConjugationEngine is being used (not simple fallback)
2. Check verb is in conjugation data
3. Ensure tense mapping is correct
4. Review ValidationResult.error_type in logs

## Testing Checklist

- [ ] Correct answer generates positive feedback
- [ ] Incorrect answer generates error-specific feedback
- [ ] Mood confusion detected correctly
- [ ] Stem-change errors detected
- [ ] Spelling-change errors detected
- [ ] Spaced repetition date calculated
- [ ] Fallback works when verb data missing
- [ ] Services initialize only once
- [ ] Database saves attempt correctly
- [ ] Response schema matches expectations

## Related Documentation

- `backend/services/conjugation.py` - ConjugationEngine implementation
- `backend/services/feedback.py` - FeedbackGenerator implementation
- `backend/services/learning_algorithm.py` - SM-2 algorithm implementation
- `backend/utils/spanish_grammar.py` - Grammar rules and verb data
- `backend/schemas/exercise.py` - Updated AnswerValidation schema

---

**Last Updated**: 2025-11-28
**Status**: Ready for deployment
**Breaking Changes**: None (backward compatible response schema)

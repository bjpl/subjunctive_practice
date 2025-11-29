# Person Extraction Logic Improvements

## Problem Statement

The current `extract_person_from_prompt()` function (found in `exercises_integrated.py`) uses fragile regex patterns that often fail to extract the grammatical person, defaulting to "yo" when uncertain. This causes wrong conjugations to be marked as correct.

## Changes Implemented

### 1. Database Schema Changes

**File**: `backend/models/exercise.py`
- **Added**: `person` field to Exercise model (line 95)
  ```python
  person = Column(String(50), nullable=True)  # "yo", "tú", "él/ella/usted", etc.
  ```

**File**: `backend/schemas/exercise.py`
- **Added**: `person` field to ExerciseBase schema (line 48)
  ```python
  person: Optional[str] = None  # Grammatical person: "yo", "tú", "él/ella/usted", etc.
  ```

**Migration Needed**: Run `alembic revision -m "Add person field to exercises"`

### 2. Person Extraction Function Improvements

**Location**: Should be added to `backend/api/routes/exercises.py` or extracted to a utility module

**Improved Function**:
```python
def extract_person_from_prompt(prompt: str, exercise_person: Optional[str] = None) -> Optional[str]:
    """
    Extract grammatical person from exercise prompt.

    Args:
        prompt: The exercise prompt text
        exercise_person: Explicit person field from exercise (if available)

    Returns:
        Grammatical person string or None if cannot be determined reliably.
        Returns None instead of defaulting to "yo" when uncertain.
    """
    # First priority: use explicit person field if available
    if exercise_person:
        logger.debug(f"Using explicit person field: {exercise_person}")
        return exercise_person

    prompt_lower = prompt.lower()

    # Person indicators - improved patterns with word boundaries
    person_patterns = {
        "yo": [" yo ", "^yo "],
        "tú": [" tú ", "^tú "],
        "él/ella/usted": [" él ", " ella ", " usted ", "^él ", "^ella ", "^usted "],
        "nosotros/nosotras": [" nosotros ", " nosotras ", "^nosotros ", "^nosotras "],
        "vosotros/vosotras": [" vosotros ", " vosotras ", "^vosotros ", "^vosotras "],
        "ellos/ellas/ustedes": [" ellos ", " ellas ", " ustedes ", "^ellos ", "^ellas ", "^ustedes "]
    }

    for person, patterns in person_patterns.items():
        for pattern in patterns:
            # Handle start of string patterns
            if pattern.startswith("^"):
                if prompt_lower.startswith(pattern[1:]):
                    logger.debug(f"Extracted person from prompt: {person}")
                    return person
            else:
                if pattern in prompt_lower:
                    logger.debug(f"Extracted person from prompt: {person}")
                    return person

    # Return None if person cannot be determined reliably
    logger.warning(f"Could not reliably extract person from prompt: {prompt[:50]}...")
    return None
```

**Key Improvements**:
1. **Explicit person field priority**: Check `exercise.person` first before parsing prompt
2. **Better word boundaries**: Use patterns like `" yo "` and `"^yo "` to avoid false matches
3. **Return None on failure**: Instead of defaulting to "yo", return None to trigger simple validation fallback
4. **Debug logging**: Log when person is extracted vs when it fails

### 3. Validation Logic Updates

**File**: `backend/api/routes/exercises.py` (submit_answer function, around line 338-395)

**Current State**: Uses simple string comparison for all database exercises

**Proposed Changes**:
```python
# After querying exercise from database (around line 336)

# Try to use intelligent validation if exercise has verb
verb_infinitive = None
person = None
use_intelligent_validation = False

if hasattr(exercise, 'verb') and exercise.verb:
    verb_infinitive = exercise.verb.infinitive
    # Pass exercise.person field to extract_person_from_prompt
    person = extract_person_from_prompt(exercise.prompt, getattr(exercise, 'person', None))

    if person:
        use_intelligent_validation = True
        logger.info(f"Using intelligent validation for {verb_infinitive} ({person})")
    else:
        logger.warning(f"Cannot use intelligent validation: person extraction failed for exercise {ex_id}")

# Perform validation
if use_intelligent_validation:
    # Use ConjugationEngine for sophisticated validation
    tense_map = {
        SubjunctiveTense.PRESENT: "present_subjunctive",
        SubjunctiveTense.IMPERFECT: "imperfect_subjunctive_ra",
        SubjunctiveTense.PRESENT_PERFECT: "present_subjunctive",
        SubjunctiveTense.PLUPERFECT: "imperfect_subjunctive_ra"
    }
    tense = tense_map.get(exercise.tense, "present_subjunctive")

    try:
        validation_result = conjugation_engine.validate_answer(
            verb=verb_infinitive,
            tense=tense,
            person=person,
            user_answer=submission.user_answer
        )
        is_correct = validation_result.is_correct
        correct_answer = validation_result.correct_answer

        # Generate rich feedback (similar to custom_exercise_validation.py)
        exercise_context = {
            "trigger_phrase": exercise.trigger_phrase,
            "trigger_category": extract_trigger_category(exercise.trigger_phrase) if exercise.trigger_phrase else None,
            "explanation": exercise.explanation
        }

        rich_feedback = feedback_generator.generate_feedback(
            validation_result=validation_result,
            exercise_context=exercise_context,
            user_level="intermediate"
        )

    except Exception as e:
        logger.warning(f"Intelligent validation failed: {e}, falling back to simple validation")
        use_intelligent_validation = False

if not use_intelligent_validation:
    # Fallback to simple string comparison
    logger.info(f"Using simple validation for exercise {ex_id} (reason: {'no verb' if not exercise.verb else 'person extraction failed'})")
    correct_answer = exercise.correct_answer
    is_correct = validate_answer(submission.user_answer, correct_answer)

    # Create simple feedback object
    # ... (existing code)
```

### 4. Exercise Generation Updates

**File**: `backend/api/routes/exercises.py` (generate_custom_exercises function)

**Change**: The `GeneratedExercise` class already includes `person` field (line 539 in current file). Ensure this is always populated when generating exercises.

```python
exercise = GeneratedExercise(
    id=f"gen_{exercise_id}_{verb}_{person}",
    verb=verb,
    verb_translation=get_verb_translation(verb),
    tense=config.tense,
    person=person,  # ✓ Already included
    prompt=generate_exercise_prompt(...),
    correct_answer=correct_answer,
    # ...
)
```

## Testing Strategy

1. **Unit Tests**: Test `extract_person_from_prompt()` with various prompts
   - With explicit person field
   - With clear person in prompt ("yo hable", "tú hables")
   - With ambiguous prompts (should return None)
   - Edge cases (empty string, person at start of prompt)

2. **Integration Tests**: Test submit_answer endpoint
   - Exercise with explicit person field → should use intelligent validation
   - Exercise without person field but clear prompt → should extract and use intelligent validation
   - Exercise with ambiguous prompt → should fall back to simple validation
   - Verify logging messages for each case

3. **Database Migration Test**: Ensure existing exercises work after adding nullable person column

## Implementation Checklist

- [x] Add `person` field to Exercise model
- [x] Add `person` field to ExerciseBase schema
- [ ] Create database migration
- [ ] Add `extract_person_from_prompt()` function to exercises.py
- [ ] Update submit_answer() to use intelligent validation for database exercises
- [ ] Add extract_trigger_category() helper function (if not already present)
- [ ] Update seed data to include person field for new exercises
- [ ] Write unit tests for extract_person_from_prompt()
- [ ] Write integration tests for validation with/without person field
- [ ] Update documentation

## Affected Files

1. `backend/models/exercise.py` - Add person column (DONE)
2. `backend/schemas/exercise.py` - Add person field (DONE)
3. `backend/api/routes/exercises.py` - Add person extraction and intelligent validation
4. `backend/core/seed_data.py` - Include person in SEED_EXERCISES
5. `alembic/versions/` - New migration file
6. `tests/` - New test files

## Notes

- The `custom_exercise_validation.py` module already implements intelligent validation correctly for custom exercises
- Custom exercises always have explicit `person` field from the submission
- Database exercises need similar logic but must extract person from exercise.prompt or exercise.person
- Simple validation remains as fallback for exercises where person cannot be determined

# Documentation Index - Spanish Subjunctive Practice App

## Overview Documents
- **README.md** - Main project documentation (if exists)
- **EXPANSION_SUMMARY.md** - Complete summary of subjunctive expansion

## Technical Documentation

### Expansion Details
1. **SUBJUNCTIVE_EXPANSION.md** - Full technical documentation of the expansion
   - Backend service updates
   - Database model changes
   - Seed data structure
   - Exercise breakdown (35 total exercises)
   - Integration points

2. **QUICK_REFERENCE_NEW_TENSES.md** - Quick reference for developers
   - Present perfect subjunctive conjugation
   - Pluperfect subjunctive conjugation
   - Relative clause subjunctive usage
   - Irregular past participles
   - Code examples
   - Trigger phrases
   - Common mistakes

## Implementation Files

### Core Services
- **`backend/services/conjugation.py`**
  - ConjugationEngine class
  - PAST_PARTICIPLES dictionary (60+ verbs)
  - Perfect/pluperfect conjugation methods
  - Past participle generation

### Data Models
- **`backend/models/exercise.py`**
  - SubjunctiveTense enum (includes new tenses)
  - ExerciseType enum
  - DifficultyLevel enum
  - Database models

### Seed Data
- **`backend/core/seed_data.py`**
  - SEED_VERBS (52 verbs with conjugations)
  - SEED_EXERCISES (35 new exercises)
    - perfect_subjunctive: 15 exercises
    - relative_clause_subjunctive: 10 exercises
    - pluperfect_subjunctive: 10 exercises
  - SEED_ACHIEVEMENTS

## Verification & Testing

### Scripts
- **`scripts/verify_expansion.py`** - Comprehensive verification script
  - Tests perfect subjunctive conjugation
  - Tests pluperfect subjunctive conjugation
  - Tests past participle dictionary
  - Tests relative clause subjunctive
  - Verifies seed data structure

## Exercise Content

### A. Perfect Subjunctive (15 exercises)
**Format**: haya/hayas/haya/hayamos/hayáis/hayan + past participle

**Difficulty**: Medium (11), Hard (4)

**Covered Verbs**:
- Regular: hablar, comer, vivir, estudiar, trabajar, cantar, llegar, terminar
- Irregular: hacer→hecho, decir→dicho, escribir→escrito, ver→visto, poner→puesto, volver→vuelto, abrir→abierto

### B. Relative Clause Subjunctive (10 exercises)
**Format**: Present subjunctive in relative clauses with indefinite antecedent

**Difficulty**: Medium (2), Hard (8)

**Covered Verbs**: tener, saber, poder, ser, hablar, entender, querer, vivir, hacer, conocer

### C. Pluperfect Subjunctive (10 exercises)
**Format**: hubiera/hubieras/hubiera/hubiéramos/hubierais/hubieran + past participle

**Difficulty**: Expert (10)

**Covered Verbs**:
- Regular: saber, estudiar, trabajar, llegar
- Irregular: hacer→hecho, decir→dicho, venir→venido, escribir→escrito, ver→visto, poner→puesto

## Quick Start

### For Developers
```python
from backend.services.conjugation import ConjugationEngine

engine = ConjugationEngine()

# Perfect subjunctive
result = engine.conjugate('hacer', 'present_perfect_subjunctive', 'yo')
print(result.conjugation)  # "haya hecho"

# Pluperfect subjunctive
result = engine.conjugate('decir', 'pluperfect_subjunctive', 'ellos/ellas/ustedes')
print(result.conjugation)  # "hubieran dicho"
```

### For Content Creators
See **SEED_EXERCISES** in `backend/core/seed_data.py` for exercise structure:
```python
{
    "verb": "hablar",
    "exercise_type": ExerciseType.FILL_BLANK,
    "tense": SubjunctiveTense.PRESENT_PERFECT,
    "difficulty": DifficultyLevel.MEDIUM,
    "prompt": "Es posible que él ya _____ con el profesor. (hablar)",
    "correct_answer": "haya hablado",
    "person": "él/ella/usted",
    "trigger_phrase": "Es posible que",
    "explanation": "Present perfect subjunctive: haya + past participle",
    "tags": ["perfect-subjunctive", "regular-participle"]
}
```

## Statistics

- **Total Verbs**: 52 (in SEED_VERBS)
- **New Exercises**: 35
- **Past Participles**: 60+ (regular and irregular)
- **Irregular Participles**: 15+
- **Trigger Phrases**: 12+
- **Exercise Tags**: 20+
- **Difficulty Levels**: 4 (Easy, Medium, Hard, Expert)

## Navigation

### By User Type

**Learners**:
- Use the application UI to practice exercises
- Reference QUICK_REFERENCE for grammar explanations

**Developers**:
- Start with EXPANSION_SUMMARY.md for overview
- Use QUICK_REFERENCE_NEW_TENSES.md for implementation
- Check conjugation.py for technical details
- Run verify_expansion.py for testing

**Content Creators**:
- Review seed_data.py for exercise structure
- Use SUBJUNCTIVE_EXPANSION.md for content guidelines
- Follow tag system for organization

### By Topic

**Conjugation**:
- `backend/services/conjugation.py`
- QUICK_REFERENCE_NEW_TENSES.md
- Perfect subjunctive: haya + participle
- Pluperfect subjunctive: hubiera + participle

**Exercises**:
- `backend/core/seed_data.py`
- SUBJUNCTIVE_EXPANSION.md
- 35 exercises across 3 categories

**Database**:
- `backend/models/exercise.py`
- SubjunctiveTense enum
- Exercise model structure

**Testing**:
- `scripts/verify_expansion.py`
- All tests passing ✓

## Recent Changes

**December 16, 2025** - Spanish Subjunctive Expansion
- Added 35 new exercises (perfect, relative clause, pluperfect subjunctive)
- Implemented compound tense conjugation (perfect/pluperfect)
- Added 60+ past participles with irregular forms
- Created comprehensive documentation
- All tests passing

---

*Last updated: December 16, 2025*

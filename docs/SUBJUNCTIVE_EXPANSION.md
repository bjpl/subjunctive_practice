# Spanish Subjunctive Content Expansion

## Overview
This document describes the expansion of Spanish subjunctive content for the language learning application, adding three new advanced subjunctive types with comprehensive exercise coverage.

## Changes Summary

### 1. Backend Service Updates

#### `/backend/services/conjugation.py`
**New Features:**
- Added `PAST_PARTICIPLES` dictionary with 50+ verbs (regular and irregular participles)
- Implemented `_conjugate_perfect_subjunctive()` method for present perfect subjunctive
- Implemented `_conjugate_pluperfect_subjunctive()` method for pluperfect subjunctive
- Added helper methods:
  - `_get_past_participle()` - Returns correct participle form
  - `_get_regular_participle()` - Generates regular participles
- Updated valid tenses list to include new compound tenses
- Enhanced error analysis to recognize new tenses

**Past Participle Coverage:**
- **Regular participles:** hablar→hablado, comer→comido, vivir→vivido, etc.
- **Irregular participles:** hacer→hecho, decir→dicho, escribir→escrito, ver→visto, poner→puesto, volver→vuelto, abrir→abierto, romper→roto, morir→muerto, and more

### 2. Database Model Updates

#### `/backend/models/exercise.py`
**Updated Enums:**
```python
class SubjunctiveTense(str, enum.Enum):
    PRESENT = "present_subjunctive"
    IMPERFECT = "imperfect_subjunctive"
    PRESENT_PERFECT = "present_perfect_subjunctive"  # NEW
    PLUPERFECT = "pluperfect_subjunctive"            # NEW
```

### 3. Seed Data Expansion

#### `/backend/core/seed_data.py`
**New Content:**
- Added `SEED_EXERCISES` dictionary with 35 new exercises across three categories
- Added 2 new verbs with irregular participles (romper, cubrir)

**Exercise Breakdown:**

##### A. Perfect Subjunctive (15 exercises)
Present Perfect Subjunctive: haya/hayas/haya/hayamos/hayáis/hayan + past participle

**Trigger Phrases:**
- "Es posible que" (possibility)
- "Dudo que" (doubt)
- "No creo que" (negation)
- "Es increíble que" (emotion)
- "Espero que" (hope)
- "Me alegra que" (emotion)
- "Es probable que" (probability)
- "Ojalá que" (wish)
- "Es extraño que" (strangeness)

**Verbs Covered:**
- Regular participles: hablar, comer, vivir, estudiar, trabajar, cantar, llegar, terminar
- Irregular participles: hacer→hecho, decir→dicho, escribir→escrito, ver→visto, poner→puesto, volver→vuelto, abrir→abierto

**Example:**
```
Prompt: Es posible que él ya _____ con el profesor. (hablar)
Answer: haya hablado
Explanation: Present perfect subjunctive: haya + past participle (hablado)
```

##### B. Relative Clause Subjunctive (10 exercises)
Subjunctive in relative clauses with indefinite or non-existent antecedents

**Patterns:**
- "Busco una casa que..." (indefinite antecedent)
- "Necesito alguien que..." (indefinite antecedent)
- "No hay nadie que..." (non-existent antecedent)
- "Quiero un/una... que..." (indefinite antecedent)

**Verbs Covered:**
tener, saber, poder, ser, hablar, entender, querer, vivir, hacer, conocer

**Key Concept:**
Uses subjunctive when the antecedent is indefinite (any house, anyone) or non-existent (nobody, nothing). Contrasts with indicative when the antecedent is specific and known.

**Example:**
```
Prompt: Busco una casa que _____ tres dormitorios. (tener)
Answer: tenga
Explanation: Subjunctive in relative clause with indefinite antecedent (any house, not a specific one)
```

##### C. Pluperfect Subjunctive (10 exercises)
Pluperfect Subjunctive: hubiera/hubieras/hubiera/hubiéramos/hubierais/hubieran + past participle

**Uses:**
- Hypothetical past situations (Si clauses)
- Regret about the past (Ojalá)
- Unreal past conditions

**Trigger Phrases:**
- "Si yo/tú/él..." (hypothetical past conditionals)
- "Ojalá..." (wishes about the past)

**Verbs Covered:**
- Regular participles: saber, estudiar, trabajar, llegar
- Irregular participles: hacer→hecho, decir→dicho, venir→venido, escribir→escrito, ver→visto, poner→puesto

**Example:**
```
Prompt: Si yo _____ la verdad, habría actuado diferente. (saber)
Answer: hubiera sabido
Explanation: Pluperfect subjunctive for hypothetical past: hubiera + past participle
```

## Difficulty Progression

### Medium (Exercises: 18)
- Perfect subjunctive with regular participles
- Relative clause with common verbs
- Basic trigger phrase recognition

### Hard (Exercises: 12)
- Perfect subjunctive with irregular participles
- Relative clause with negation (nadie, nada)
- Complex relative clause patterns

### Expert (Exercises: 10)
- Pluperfect subjunctive (all exercises)
- Hypothetical past conditionals
- Complex Si clauses

## Tag System

New tags added for organization and filtering:

**Perfect Subjunctive:**
- `perfect-subjunctive`
- `regular-participle`
- `irregular-participle`
- `doubt`, `hope`, `emotion`, `probability`, `impossibility`, `wish`

**Relative Clause:**
- `relative-clause`
- `indefinite-antecedent`
- `nonexistent-antecedent`
- `negation`

**Pluperfect Subjunctive:**
- `pluperfect-subjunctive`
- `hypothetical-past`
- `conditional`
- `regret`
- `wish`

## Integration Points

### 1. Conjugation Engine
```python
from backend.services.conjugation import ConjugationEngine

engine = ConjugationEngine()

# Present perfect subjunctive
result = engine.conjugate('hacer', 'present_perfect_subjunctive', 'nosotros/nosotras')
print(result.conjugation)  # "hayamos hecho"

# Pluperfect subjunctive
result = engine.conjugate('decir', 'pluperfect_subjunctive', 'tú')
print(result.conjugation)  # "hubieras dicho"
```

### 2. Exercise Creation
Exercises follow the existing structure and can be loaded via seed data:
```python
from backend.core.seed_data import SEED_EXERCISES

perfect_exercises = SEED_EXERCISES['perfect_subjunctive']
relative_exercises = SEED_EXERCISES['relative_clause_subjunctive']
pluperfect_exercises = SEED_EXERCISES['pluperfect_subjunctive']
```

## Testing

All conjugations have been verified:
- ✅ Present perfect subjunctive: Regular and irregular participles
- ✅ Pluperfect subjunctive: Regular and irregular participles
- ✅ All grammatical persons (yo, tú, él/ella/usted, nosotros, vosotros, ellos/ellas/ustedes)
- ✅ Error analysis updated for new tenses

## Database Migration

To apply these changes to the database:

1. Update the database schema to support new tenses (if needed)
2. Run seed data import to add new exercises:
   ```bash
   python backend/scripts/seed_database.py
   ```

## Future Enhancements

Potential additions for further expansion:

1. **Future Subjunctive** (archaic but educational)
2. **More relative clause exercises** with indicative/subjunctive contrast
3. **Perfect vs. Pluperfect drills** to distinguish usage
4. **Sequence of tenses exercises** combining multiple subjunctive forms
5. **Multiple choice exercises** for all new tense types

## Summary Statistics

- **Total new exercises:** 35
- **New tenses supported:** 2 (present perfect, pluperfect)
- **Verbs with participle data:** 50+
- **Irregular participles covered:** 15+
- **New trigger phrases:** 12+
- **Difficulty levels:** Medium (18), Hard (12), Expert (10)

## References

- Present Perfect Subjunctive: Used for completed actions in the recent past where subjunctive is triggered
- Pluperfect Subjunctive: Used for hypothetical or contrary-to-fact situations in the past
- Relative Clauses: Subjunctive required when antecedent is indefinite, non-existent, or negated

---

*Last updated: December 16, 2025*

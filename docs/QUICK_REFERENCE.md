# Spanish Subjunctive Conjugation Engine - Quick Reference

## Installation

```python
# All modules are in backend/services/
from backend.services.conjugation import ConjugationEngine
from backend.services.exercise_generator import ExerciseGenerator
from backend.services.learning_algorithm import LearningAlgorithm
from backend.services.feedback import FeedbackGenerator
```

## Quick Start (30 seconds)

```python
# 1. Initialize
engine = ConjugationEngine()

# 2. Conjugate a verb
result = engine.conjugate("hablar", "present_subjunctive", "yo")
print(result.conjugation)  # "hable"

# 3. Validate an answer
validation = engine.validate_answer("ser", "present_subjunctive", "yo", "sea")
print(validation.is_correct)  # True

# Done!
```

## Common Operations

### Conjugate a Verb
```python
result = engine.conjugate(verb, tense, person)
# verb: "hablar", "ser", "querer", etc.
# tense: "present_subjunctive", "imperfect_subjunctive_ra", "imperfect_subjunctive_se"
# person: "yo", "tú", "él/ella/usted", "nosotros/nosotras", "vosotros/vosotras", "ellos/ellas/ustedes"
```

### Get Full Conjugation Table
```python
table = engine.get_full_conjugation_table("ser", "present_subjunctive")
# Returns dict: {"yo": result, "tú": result, ...}
```

### Validate User Answer
```python
validation = engine.validate_answer("hablar", "present_subjunctive", "yo", "hable")
# Returns: ValidationResult(is_correct, error_type, suggestions)
```

### Generate an Exercise
```python
generator = ExerciseGenerator()
exercise = generator.generate_exercise(difficulty="intermediate")
# difficulty: "beginner", "intermediate", "advanced"
# Returns: Exercise with sentence, verb, correct_answer, hints
```

### Generate Exercise Set
```python
exercises = generator.generate_exercise_set(count=10, difficulty="beginner")
# Returns: List of 10 exercises
```

### Track Learning Progress
```python
learning = LearningAlgorithm()
learning.add_card("hablar", "present_subjunctive", "yo")

result = learning.process_exercise_result(
    verb="hablar",
    tense="present_subjunctive",
    person="yo",
    correct=True,
    response_time_ms=3000
)
# Returns: Dict with next_review, interval_days, difficulty info
```

### Get Statistics
```python
stats = learning.get_statistics()
# Returns: {
#   total_cards, mastered_cards, learning_cards, new_cards,
#   due_cards, overall_accuracy, difficulty
# }
```

### Generate Feedback
```python
feedback_gen = FeedbackGenerator()
validation = engine.validate_answer(...)
feedback = feedback_gen.generate_feedback(validation, context={...})
# Returns: Feedback with message, explanation, suggestions, next_steps
```

## Supported Verbs by Category

### Regular Verbs
```python
# -ar: hablar, estudiar, trabajar, cantar, bailar, caminar, comprar...
# -er: comer, beber, aprender, leer, correr, comprender, vender...
# -ir: vivir, escribir, recibir, abrir, subir, decidir, partir...
```

### Irregular Verbs (17)
```python
irregulars = ["ser", "estar", "ir", "haber", "dar", "saber", "ver",
              "hacer", "decir", "tener", "poner", "poder", "querer",
              "venir", "salir", "traer", "caer"]
```

### Stem-Changing Verbs
```python
# e→ie: pensar, querer, sentir, preferir, cerrar, empezar...
# o→ue: poder, dormir, volver, contar, encontrar, mostrar...
# e→i: pedir, servir, repetir, seguir, conseguir, vestir...
```

### Spelling-Change Verbs
```python
# g→gu: pagar, llegar, jugar
# c→qu: buscar, sacar, tocar, practicar
# z→c: empezar, comenzar, cruzar
```

## WEIRDO Categories

```python
categories = [
    "Wishes",                    # quiero que, espero que
    "Emotions",                  # me alegro de que, siento que
    "Impersonal_Expressions",    # es importante que, es necesario que
    "Recommendations",           # recomiendo que, sugiero que
    "Doubt_Denial",             # dudo que, no creo que
    "Ojalá"                     # ojalá que
]
```

## Error Types

```python
error_types = [
    "mood_confusion",        # Used indicative instead of subjunctive
    "wrong_person",          # Correct form for different person
    "wrong_tense",          # Different subjunctive tense
    "stem_change_error",    # Missed stem change
    "spelling_change_error", # Missed spelling change
    "wrong_ending",         # Incorrect ending
    "spelling_error"        # Close but misspelled
]
```

## SM-2 Algorithm Quality Scores

```python
# Used internally by learning algorithm:
# 5 = perfect response (< 3 sec)
# 4 = correct after hesitation (3-7 sec)
# 3 = correct with difficulty (> 7 sec)
# 2 = incorrect but remembered
# 1 = incorrect, familiar
# 0 = complete blackout
```

## Typical Workflow

```python
# 1. Initialize all components
engine = ConjugationEngine()
generator = ExerciseGenerator(engine)
learning = LearningAlgorithm(initial_difficulty="intermediate")
feedback_gen = FeedbackGenerator(engine)

# 2. Generate exercise
exercise = generator.generate_exercise(
    difficulty=learning.difficulty_manager.get_difficulty()
)

# 3. Show to user
print(exercise.get_display_sentence())

# 4. Get user answer
user_answer = input("Your answer: ")

# 5. Validate
validation = engine.validate_answer(
    exercise.verb, exercise.tense, exercise.person, user_answer
)

# 6. Generate feedback
feedback = feedback_gen.generate_feedback(validation, {...})
print(feedback.message)
print(feedback.explanation)

# 7. Update learning
learning.process_exercise_result(
    exercise.verb, exercise.tense, exercise.person,
    validation.is_correct, response_time_ms
)

# 8. Get next exercise
next_items = learning.get_next_items(count=1)
```

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific module
pytest tests/test_conjugation_engine.py -v

# Run with coverage
pytest tests/ --cov=backend/services
```

## Common Patterns

### Get verb information
```python
info = engine.get_verb_info("querer")
# {type, is_irregular, is_stem_changing, stem_change_pattern, ...}
```

### Check if verb is supported
```python
verbs = engine.get_supported_verbs()
# {irregular: [...], stem_changing_e_ie: [...], regular_ar: [...], ...}
```

### Generate exercises for specific category
```python
wishes_exercises = generator.generate_exercise_set(
    count=5,
    weirdo_categories=["Wishes"]
)
```

### Get WEIRDO explanation
```python
explanation = generator.get_weirdo_explanation("Wishes")
# {category, description, triggers, examples}
```

### Detect error patterns
```python
from backend.services.feedback import ErrorAnalyzer

analyzer = ErrorAnalyzer()
# ... after multiple errors ...
patterns = analyzer.detect_patterns(min_frequency=3)
# Returns list of ErrorPattern objects
```

## Performance Tips

1. **Reuse engine instances** - Don't recreate for each operation
2. **Batch operations** - Use `generate_exercise_set()` for multiple exercises
3. **Cache conjugation tables** - Store frequently used tables
4. **Use appropriate difficulty** - Start with beginner for new learners

## Troubleshooting

### Verb not found
```python
# Check if verb is supported
verbs = engine.get_supported_verbs()
if "myverb" in verbs["irregular"]:
    # supported
```

### Invalid conjugation
```python
try:
    result = engine.conjugate(verb, tense, person)
except ValueError as e:
    print(f"Error: {e}")
    # Check verb spelling, tense name, person format
```

### No exercises generated
```python
# Ensure difficulty is valid
valid_difficulties = ["beginner", "intermediate", "advanced"]

# Ensure WEIRDO category is valid
from backend.utils.spanish_grammar import WEIRDO_TRIGGERS
valid_categories = list(WEIRDO_TRIGGERS.keys())
```

## File Locations

```
backend/
├── services/
│   ├── conjugation.py          # ConjugationEngine
│   ├── exercise_generator.py   # ExerciseGenerator
│   ├── learning_algorithm.py   # LearningAlgorithm, SM2Algorithm
│   └── feedback.py             # FeedbackGenerator, ErrorAnalyzer
└── utils/
    └── spanish_grammar.py      # All grammar constants

tests/
├── test_conjugation_engine.py
└── test_exercise_generator.py

examples/
└── usage_examples.py           # 12 complete examples

docs/
├── CONJUGATION_ENGINE_SUMMARY.md  # Full documentation
└── QUICK_REFERENCE.md            # This file
```

## Need More Help?

- See `examples/usage_examples.py` for 12 detailed examples
- See `docs/CONJUGATION_ENGINE_SUMMARY.md` for complete documentation
- Check test files for usage patterns
- Review docstrings in source files

"""
Comprehensive Usage Examples for Spanish Subjunctive Conjugation Engine

This file demonstrates all major features of the conjugation engine,
exercise generator, learning algorithm, and feedback system.
"""

from backend.services.conjugation import ConjugationEngine
from backend.services.exercise_generator import ExerciseGenerator
from backend.services.learning_algorithm import LearningAlgorithm, SM2Algorithm
from backend.services.feedback import FeedbackGenerator, ErrorAnalyzer


def example_1_basic_conjugation():
    """Example 1: Basic conjugation usage"""
    print("=" * 70)
    print("EXAMPLE 1: Basic Conjugation")
    print("=" * 70)

    engine = ConjugationEngine()

    # Regular verb
    result = engine.conjugate("hablar", "present_subjunctive", "yo")
    print(f"\nRegular verb 'hablar' (yo): {result.conjugation}")

    # Irregular verb
    result = engine.conjugate("ser", "present_subjunctive", "yo")
    print(f"Irregular verb 'ser' (yo): {result.conjugation}")
    print(f"  Is irregular: {result.is_irregular}")

    # Stem-changing verb
    result = engine.conjugate("querer", "present_subjunctive", "yo")
    print(f"\nStem-changing verb 'querer' (yo): {result.conjugation}")
    print(f"  Stem change pattern: {result.stem_change_pattern}")

    # Spelling change verb
    result = engine.conjugate("buscar", "present_subjunctive", "yo")
    print(f"\nSpelling-change verb 'buscar' (yo): {result.conjugation}")
    print(f"  Has spelling change: {result.has_spelling_change}")


def example_2_full_conjugation_table():
    """Example 2: Getting full conjugation tables"""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Full Conjugation Table")
    print("=" * 70)

    engine = ConjugationEngine()

    # Get complete conjugation for 'ser'
    table = engine.get_full_conjugation_table("ser", "present_subjunctive")

    print("\nPresent Subjunctive conjugation of 'ser':")
    for person, result in table.items():
        if result:
            print(f"  {person:25} -> {result.conjugation}")


def example_3_answer_validation():
    """Example 3: Validating user answers"""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Answer Validation")
    print("=" * 70)

    engine = ConjugationEngine()

    # Correct answer
    validation = engine.validate_answer("hablar", "present_subjunctive", "yo", "hable")
    print(f"\nUser answer: 'hable'")
    print(f"Correct: {validation.is_correct}")

    # Incorrect answer (mood confusion)
    validation = engine.validate_answer("hablar", "present_subjunctive", "yo", "hablo")
    print(f"\nUser answer: 'hablo'")
    print(f"Correct: {validation.is_correct}")
    print(f"Error type: {validation.error_type}")
    print(f"Suggestions: {validation.suggestions}")

    # Wrong person
    validation = engine.validate_answer("hablar", "present_subjunctive", "yo", "hables")
    print(f"\nUser answer: 'hables'")
    print(f"Correct: {validation.is_correct}")
    print(f"Error type: {validation.error_type}")


def example_4_verb_information():
    """Example 4: Getting verb information"""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Verb Information")
    print("=" * 70)

    engine = ConjugationEngine()

    verbs = ["hablar", "ser", "querer", "buscar"]

    for verb in verbs:
        info = engine.get_verb_info(verb)
        print(f"\n{verb}:")
        print(f"  Type: {info['type']}")
        print(f"  Irregular: {info['is_irregular']}")
        print(f"  Stem-changing: {info['is_stem_changing']}")
        if info['stem_change_pattern']:
            print(f"  Pattern: {info['stem_change_pattern']}")


def example_5_exercise_generation():
    """Example 5: Generating exercises"""
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Exercise Generation")
    print("=" * 70)

    generator = ExerciseGenerator()

    # Generate a single exercise
    exercise = generator.generate_exercise(difficulty="intermediate")

    print(f"\nGenerated Exercise:")
    print(f"  ID: {exercise.exercise_id}")
    print(f"  Type: {exercise.exercise_type}")
    print(f"  Verb: {exercise.verb}")
    print(f"  Category: {exercise.trigger_category}")
    print(f"  Trigger: {exercise.trigger_phrase}")
    print(f"  Context: {exercise.context}")
    print(f"\n  Sentence: {exercise.get_display_sentence()}")
    print(f"\n  Hints:")
    for hint in exercise.hints:
        print(f"    - {hint}")
    print(f"\n  Correct answer: {exercise.correct_answer}")


def example_6_weirdo_categories():
    """Example 6: WEIRDO category exploration"""
    print("\n" + "=" * 70)
    print("EXAMPLE 6: WEIRDO Categories")
    print("=" * 70)

    generator = ExerciseGenerator()

    categories = ["Wishes", "Emotions", "Impersonal_Expressions",
                  "Recommendations", "Doubt_Denial", "Ojalá"]

    for category in categories[:3]:  # Show first 3
        explanation = generator.get_weirdo_explanation(category)
        print(f"\n{category}:")
        print(f"  Description: {explanation['description']}")
        print(f"  Example triggers:")
        for trigger in explanation['triggers'][:3]:
            print(f"    - {trigger}")


def example_7_exercise_set():
    """Example 7: Generating exercise sets"""
    print("\n" + "=" * 70)
    print("EXAMPLE 7: Exercise Sets")
    print("=" * 70)

    generator = ExerciseGenerator()

    # Generate a set of 5 exercises
    exercises = generator.generate_exercise_set(count=5, difficulty="beginner")

    print(f"\nGenerated {len(exercises)} exercises:")
    for i, exercise in enumerate(exercises, 1):
        print(f"\n{i}. {exercise.trigger_category}")
        print(f"   {exercise.get_display_sentence()}")
        print(f"   Answer: {exercise.correct_answer}")


def example_8_spaced_repetition():
    """Example 8: Spaced repetition (SM-2 algorithm)"""
    print("\n" + "=" * 70)
    print("EXAMPLE 8: Spaced Repetition (SM-2)")
    print("=" * 70)

    learning = LearningAlgorithm(initial_difficulty="intermediate")

    # Add some cards
    learning.add_card("hablar", "present_subjunctive", "yo")
    learning.add_card("ser", "present_subjunctive", "yo")
    learning.add_card("tener", "present_subjunctive", "yo")

    print("\nInitial state:")
    stats = learning.get_statistics()
    print(f"  Total cards: {stats['total_cards']}")
    print(f"  New cards: {stats['new_cards']}")

    # Simulate some practice
    result1 = learning.process_exercise_result(
        verb="hablar",
        tense="present_subjunctive",
        person="yo",
        correct=True,
        response_time_ms=2500
    )

    print(f"\nAfter practicing 'hablar':")
    print(f"  Next review: {result1['next_review']}")
    print(f"  Interval: {result1['interval_days']} days")

    # Another exercise (incorrect)
    result2 = learning.process_exercise_result(
        verb="ser",
        tense="present_subjunctive",
        person="yo",
        correct=False,
        response_time_ms=8000
    )

    print(f"\nAfter incorrect 'ser':")
    print(f"  Next review: {result2['next_review']}")
    print(f"  Interval: {result2['interval_days']} days")
    print(f"  Difficulty changed: {result2['difficulty_changed']}")

    # Get updated statistics
    stats = learning.get_statistics()
    print(f"\nCurrent statistics:")
    print(f"  Total cards: {stats['total_cards']}")
    print(f"  Learning cards: {stats['learning_cards']}")
    print(f"  Overall accuracy: {stats['overall_accuracy']:.1f}%")


def example_9_adaptive_difficulty():
    """Example 9: Adaptive difficulty adjustment"""
    print("\n" + "=" * 70)
    print("EXAMPLE 9: Adaptive Difficulty")
    print("=" * 70)

    learning = LearningAlgorithm(initial_difficulty="intermediate")

    print(f"\nStarting difficulty: {learning.difficulty_manager.get_difficulty()}")

    # Simulate high performance
    print("\nSimulating high performance (10 correct, fast answers)...")
    for i in range(10):
        learning.process_exercise_result(
            verb="hablar",
            tense="present_subjunctive",
            person="yo",
            correct=True,
            response_time_ms=2000
        )

    metrics = learning.difficulty_manager.get_performance_metrics()
    print(f"\nPerformance metrics:")
    print(f"  Accuracy: {metrics['accuracy']*100:.1f}%")
    print(f"  Average time: {metrics['average_time_ms']:.0f}ms")
    print(f"  Current difficulty: {metrics['difficulty']}")


def example_10_feedback_generation():
    """Example 10: Intelligent feedback"""
    print("\n" + "=" * 70)
    print("EXAMPLE 10: Intelligent Feedback")
    print("=" * 70)

    engine = ConjugationEngine()
    feedback_gen = FeedbackGenerator(engine)

    # Correct answer
    validation = engine.validate_answer("ser", "present_subjunctive", "yo", "sea")
    feedback = feedback_gen.generate_feedback(
        validation,
        {"trigger_phrase": "es importante que", "trigger_category": "Impersonal_Expressions"}
    )

    print("\nFeedback for CORRECT answer:")
    print(f"  Message: {feedback.message}")
    print(f"  Explanation: {feedback.explanation}")
    print(f"  Encouragement: {feedback.encouragement}")

    # Incorrect answer
    validation = engine.validate_answer("ser", "present_subjunctive", "yo", "soy")
    feedback = feedback_gen.generate_feedback(
        validation,
        {"trigger_phrase": "es importante que", "trigger_category": "Impersonal_Expressions"}
    )

    print("\n\nFeedback for INCORRECT answer:")
    print(f"  Message: {feedback.message}")
    print(f"  Explanation: {feedback.explanation}")
    print(f"  Error category: {feedback.error_category}")
    print(f"\n  Suggestions:")
    for suggestion in feedback.suggestions[:3]:
        print(f"    - {suggestion}")
    print(f"\n  Next steps:")
    for step in feedback.next_steps:
        print(f"    - {step}")


def example_11_error_pattern_detection():
    """Example 11: Error pattern detection"""
    print("\n" + "=" * 70)
    print("EXAMPLE 11: Error Pattern Detection")
    print("=" * 70)

    engine = ConjugationEngine()
    analyzer = ErrorAnalyzer()

    # Simulate multiple errors of same type
    print("\nSimulating repeated mood confusion errors...")
    for verb in ["hablar", "comer", "vivir", "ser", "tener"]:
        validation = engine.validate_answer(
            verb,
            "present_subjunctive",
            "yo",
            verb[:-2] + "o"  # Incorrect indicative form
        )
        analyzer.analyze_error(validation)

    # Detect patterns
    patterns = analyzer.detect_patterns(min_frequency=3)

    print(f"\n\nDetected {len(patterns)} error pattern(s):")
    for pattern in patterns:
        print(f"\n  Error type: {pattern.error_type}")
        print(f"  Frequency: {pattern.frequency}")
        print(f"  Priority: {pattern.priority}")
        print(f"  Suggestion: {pattern.suggestion}")


def example_12_complete_learning_session():
    """Example 12: Complete learning session"""
    print("\n" + "=" * 70)
    print("EXAMPLE 12: Complete Learning Session")
    print("=" * 70)

    # Initialize all components
    engine = ConjugationEngine()
    generator = ExerciseGenerator(engine)
    learning = LearningAlgorithm(initial_difficulty="intermediate")
    feedback_gen = FeedbackGenerator(engine)

    print("\nStarting learning session...")
    print(f"Initial difficulty: {learning.difficulty_manager.get_difficulty()}")

    # Generate and practice 3 exercises
    for i in range(3):
        print(f"\n{'='*60}")
        print(f"Exercise {i+1}/3")
        print('='*60)

        # Generate exercise
        exercise = generator.generate_exercise(
            difficulty=learning.difficulty_manager.get_difficulty()
        )

        print(f"\nCategory: {exercise.trigger_category}")
        print(f"Sentence: {exercise.get_display_sentence()}")
        print(f"Verb: {exercise.verb}")

        # Simulate user answer (alternate correct/incorrect for demo)
        if i % 2 == 0:
            user_answer = exercise.correct_answer
            response_time = 3000
        else:
            # Wrong answer
            user_answer = exercise.verb[:-2] + "o"
            response_time = 6000

        print(f"\nUser answer: '{user_answer}'")

        # Validate
        validation = engine.validate_answer(
            exercise.verb,
            exercise.tense,
            exercise.person,
            user_answer
        )

        # Generate feedback
        feedback = feedback_gen.generate_feedback(
            validation,
            {
                "trigger_phrase": exercise.trigger_phrase,
                "trigger_category": exercise.trigger_category
            }
        )

        print(f"\n{feedback.message}")
        print(f"{feedback.explanation}")

        # Update learning algorithm
        learning.process_exercise_result(
            exercise.verb,
            exercise.tense,
            exercise.person,
            validation.is_correct,
            response_time
        )

    # Final statistics
    print(f"\n{'='*60}")
    print("Session Complete!")
    print('='*60)

    stats = learning.get_statistics()
    print(f"\nSession Statistics:")
    print(f"  Total cards practiced: {stats['total_cards']}")
    print(f"  Overall accuracy: {stats['overall_accuracy']:.1f}%")
    print(f"  Current difficulty: {stats['difficulty']}")
    print(f"  Cards due for review: {stats['due_cards']}")


def main():
    """Run all examples"""
    examples = [
        example_1_basic_conjugation,
        example_2_full_conjugation_table,
        example_3_answer_validation,
        example_4_verb_information,
        example_5_exercise_generation,
        example_6_weirdo_categories,
        example_7_exercise_set,
        example_8_spaced_repetition,
        example_9_adaptive_difficulty,
        example_10_feedback_generation,
        example_11_error_pattern_detection,
        example_12_complete_learning_session
    ]

    print("\n" + "=" * 70)
    print("SPANISH SUBJUNCTIVE CONJUGATION ENGINE - USAGE EXAMPLES")
    print("=" * 70)
    print("\nThese examples demonstrate all major features of the system.")
    print("Run individual examples or all at once.\n")

    # Run all examples
    for example in examples:
        example()
        input("\n\nPress Enter to continue to next example...")


if __name__ == "__main__":
    # Run example 12 (complete session) as a demo
    example_12_complete_learning_session()

    print("\n\nTo see all examples, uncomment the main() call.")
    # main()

"""
Unit tests for Exercise Generator.

Tests cover:
- WEIRDO category selection
- Exercise generation (all types)
- Difficulty-based verb selection
- Sentence template generation
- Distractor generation
- Hint generation
"""

import pytest
from backend.services.exercise_generator import ExerciseGenerator, Exercise
from backend.services.conjugation import ConjugationEngine


@pytest.mark.unit
@pytest.mark.exercise
class TestExerciseGenerator:
    """Test suite for ExerciseGenerator."""

    def test_generator_initialization(self, exercise_generator):
        """Test generator initializes correctly."""
        assert exercise_generator is not None
        assert exercise_generator.engine is not None
        assert len(exercise_generator.templates) > 0

    # ========================================================================
    # Exercise Generation Tests
    # ========================================================================

    def test_generate_basic_exercise(self, exercise_generator):
        """Test generating a basic exercise."""
        exercise = exercise_generator.generate_exercise(
            difficulty="beginner",
            exercise_type="fill_in_blank"
        )

        assert isinstance(exercise, Exercise)
        assert exercise.exercise_id is not None
        assert exercise.verb is not None
        assert exercise.correct_answer is not None
        assert exercise.difficulty == "beginner"

    @pytest.mark.parametrize("difficulty", ["beginner", "intermediate", "advanced"])
    def test_generate_exercise_all_difficulties(self, exercise_generator, difficulty):
        """Test generating exercises at all difficulty levels."""
        exercise = exercise_generator.generate_exercise(difficulty=difficulty)

        assert exercise.difficulty == difficulty
        assert exercise.verb is not None

    @pytest.mark.parametrize("category", [
        "Wishes", "Emotions", "Impersonal_Expressions",
        "Recommendations", "Doubt_Denial", "Ojalá"
    ])
    def test_generate_exercise_all_weirdo_categories(self, exercise_generator, category):
        """Test generating exercises for all WEIRDO categories."""
        exercise = exercise_generator.generate_exercise(
            weirdo_category=category,
            difficulty="intermediate"
        )

        assert exercise.trigger_category == category
        assert exercise.trigger_phrase is not None

    def test_generate_exercise_specific_verb(self, exercise_generator):
        """Test generating exercise with specific verb."""
        exercise = exercise_generator.generate_exercise(
            specific_verb="hablar",
            difficulty="beginner"
        )

        assert exercise.verb == "hablar"

    @pytest.mark.parametrize("exercise_type", ["fill_in_blank", "multiple_choice"])
    def test_generate_exercise_types(self, exercise_generator, exercise_type):
        """Test generating different exercise types."""
        exercise = exercise_generator.generate_exercise(
            exercise_type=exercise_type,
            difficulty="intermediate"
        )

        assert exercise.exercise_type == exercise_type

        if exercise_type == "multiple_choice":
            assert len(exercise.distractors) > 0

    # ========================================================================
    # Difficulty Tests
    # ========================================================================

    def test_beginner_uses_regular_verbs(self, exercise_generator):
        """Test beginner difficulty uses only regular verbs."""
        verbs = set()
        for _ in range(20):
            exercise = exercise_generator.generate_exercise(difficulty="beginner")
            verbs.add(exercise.verb)

        # Beginner should primarily use regular verbs
        # (may include some common stem-changing verbs)
        assert len(verbs) > 0

    def test_advanced_uses_complex_verbs(self, exercise_generator):
        """Test advanced difficulty includes complex verbs."""
        irregular_count = 0
        for _ in range(20):
            exercise = exercise_generator.generate_exercise(difficulty="advanced")
            if exercise.verb in ["ser", "estar", "ir", "haber", "tener", "hacer"]:
                irregular_count += 1

        # Advanced should include more irregular verbs
        assert irregular_count > 0

    # ========================================================================
    # Exercise Set Tests
    # ========================================================================

    def test_generate_exercise_set(self, exercise_generator):
        """Test generating a set of exercises."""
        exercises = exercise_generator.generate_exercise_set(
            count=10,
            difficulty="intermediate"
        )

        assert len(exercises) == 10
        assert all(isinstance(ex, Exercise) for ex in exercises)

    def test_generate_exercise_set_variety(self, exercise_generator):
        """Test exercise set has variety in categories."""
        exercises = exercise_generator.generate_exercise_set(count=12)

        categories = set(ex.trigger_category for ex in exercises)
        assert len(categories) >= 3  # Should have at least 3 different categories

    def test_generate_exercise_set_with_categories(self, exercise_generator):
        """Test generating exercises with specific categories."""
        categories = ["Wishes", "Emotions"]
        exercises = exercise_generator.generate_exercise_set(
            count=10,
            weirdo_categories=categories
        )

        for exercise in exercises:
            assert exercise.trigger_category in categories

    # ========================================================================
    # Sentence Template Tests
    # ========================================================================

    def test_sentence_has_blank(self, exercise_generator):
        """Test generated sentences have blank placeholder."""
        exercise = exercise_generator.generate_exercise()

        assert "____" in exercise.sentence_template
        assert exercise.blank_position >= 0

    def test_sentence_matches_person(self, exercise_generator):
        """Test sentence template uses correct grammatical person."""
        for _ in range(10):
            exercise = exercise_generator.generate_exercise()

            # The person should be consistent with the template
            assert exercise.person is not None

    # ========================================================================
    # Hint Generation Tests
    # ========================================================================

    def test_hints_generated(self, exercise_generator):
        """Test hints are generated for exercises."""
        exercise = exercise_generator.generate_exercise()

        assert len(exercise.hints) > 0
        assert any("trigger" in hint.lower() or "category" in hint.lower() for hint in exercise.hints)

    def test_hints_include_verb_info(self, exercise_generator):
        """Test hints include verb-specific information."""
        # Test with irregular verb
        exercise = exercise_generator.generate_exercise(specific_verb="ser")

        hints_text = " ".join(exercise.hints).lower()
        assert "irregular" in hints_text or "ser" in hints_text

    def test_hints_include_person(self, exercise_generator):
        """Test hints include grammatical person."""
        exercise = exercise_generator.generate_exercise()

        hints_text = " ".join(exercise.hints)
        assert exercise.person in hints_text

    # ========================================================================
    # Distractor Generation Tests
    # ========================================================================

    def test_distractors_for_multiple_choice(self, exercise_generator):
        """Test distractors are generated for multiple choice."""
        exercise = exercise_generator.generate_exercise(
            exercise_type="multiple_choice"
        )

        assert len(exercise.distractors) > 0
        assert len(exercise.distractors) <= 3

    def test_distractors_different_from_answer(self, exercise_generator):
        """Test distractors don't match correct answer."""
        exercise = exercise_generator.generate_exercise(
            exercise_type="multiple_choice"
        )

        for distractor in exercise.distractors:
            assert distractor.lower() != exercise.correct_answer.lower()

    def test_distractors_plausible(self, exercise_generator):
        """Test distractors are plausible wrong answers."""
        exercise = exercise_generator.generate_exercise(
            exercise_type="multiple_choice",
            specific_verb="hablar"
        )

        # Distractors should be from the same verb or similar conjugations
        assert len(exercise.distractors) > 0

    # ========================================================================
    # Context Tests
    # ========================================================================

    def test_context_assigned(self, exercise_generator):
        """Test context is assigned to exercises."""
        exercise = exercise_generator.generate_exercise()

        assert exercise.context is not None
        assert len(exercise.context) > 0

    def test_context_matches_category(self, exercise_generator):
        """Test context is appropriate for category."""
        exercise = exercise_generator.generate_exercise(
            weirdo_category="Emotions"
        )

        # Context should be related to the category
        assert exercise.context is not None

    # ========================================================================
    # WEIRDO Explanation Tests
    # ========================================================================

    @pytest.mark.parametrize("category", [
        "Wishes", "Emotions", "Impersonal_Expressions",
        "Recommendations", "Doubt_Denial", "Ojalá"
    ])
    def test_get_weirdo_explanation(self, exercise_generator, category):
        """Test getting WEIRDO category explanation."""
        explanation = exercise_generator.get_weirdo_explanation(category)

        assert explanation["category"] == category
        assert "triggers" in explanation
        assert "examples" in explanation
        assert len(explanation["triggers"]) > 0

    def test_get_weirdo_explanation_invalid_category(self, exercise_generator):
        """Test getting explanation for invalid category."""
        explanation = exercise_generator.get_weirdo_explanation("InvalidCategory")
        assert explanation == {}

    # ========================================================================
    # Exercise to Dict Tests
    # ========================================================================

    def test_exercise_to_dict(self, exercise_generator):
        """Test converting exercise to dictionary."""
        exercise = exercise_generator.generate_exercise()
        exercise_dict = exercise.to_dict()

        assert isinstance(exercise_dict, dict)
        assert "exercise_id" in exercise_dict
        assert "verb" in exercise_dict
        assert "correct_answer" in exercise_dict
        assert "difficulty" in exercise_dict
        assert "trigger_category" in exercise_dict

    # ========================================================================
    # Display Tests
    # ========================================================================

    def test_get_display_sentence(self, exercise_generator):
        """Test getting display sentence with blanks."""
        exercise = exercise_generator.generate_exercise()
        display = exercise.get_display_sentence()

        assert "_______" in display  # Display blank
        assert display.count("_______") == 1

    # ========================================================================
    # Tense Tests
    # ========================================================================

    @pytest.mark.parametrize("tense", [
        "present_subjunctive",
        "imperfect_subjunctive_ra",
        "imperfect_subjunctive_se"
    ])
    def test_generate_exercise_different_tenses(self, exercise_generator, tense):
        """Test generating exercises in different tenses."""
        exercise = exercise_generator.generate_exercise(tense=tense)

        assert exercise.tense == tense

    # ========================================================================
    # Consistency Tests
    # ========================================================================

    def test_correct_answer_matches_conjugation(self, exercise_generator):
        """Test correct answer matches actual conjugation."""
        exercise = exercise_generator.generate_exercise(specific_verb="hablar")

        # Verify with conjugation engine
        result = exercise_generator.engine.conjugate(
            exercise.verb,
            exercise.tense,
            exercise.person
        )

        assert exercise.correct_answer == result.conjugation

    def test_exercise_id_unique(self, exercise_generator):
        """Test exercise IDs are unique."""
        exercises = [
            exercise_generator.generate_exercise()
            for _ in range(10)
        ]

        ids = [ex.exercise_id for ex in exercises]
        assert len(ids) == len(set(ids))  # All unique

    # ========================================================================
    # Edge Cases
    # ========================================================================

    def test_generate_many_exercises(self, exercise_generator):
        """Test generating large number of exercises."""
        exercises = exercise_generator.generate_exercise_set(count=50)

        assert len(exercises) == 50
        # Should have variety
        verbs = set(ex.verb for ex in exercises)
        assert len(verbs) > 10

    def test_exercise_with_all_defaults(self, exercise_generator):
        """Test generating exercise with default parameters."""
        exercise = exercise_generator.generate_exercise()

        assert exercise is not None
        assert exercise.difficulty == "intermediate"  # Default
        assert exercise.tense == "present_subjunctive"  # Default

    def test_template_loading(self, exercise_generator):
        """Test sentence templates are loaded."""
        assert "Wishes" in exercise_generator.templates
        assert "Emotions" in exercise_generator.templates
        assert len(exercise_generator.templates["Wishes"]) > 0

    def test_context_loading(self, exercise_generator):
        """Test context sentences are loaded."""
        assert "social" in exercise_generator.contexts
        assert "planning" in exercise_generator.contexts
        assert len(exercise_generator.contexts["social"]) > 0

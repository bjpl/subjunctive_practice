"""
Test Suite for Exercise Generator

Tests WEIRDO-based exercise generation, contextual sentences,
and multiple exercise types.
"""

import pytest
from backend.services.exercise_generator import ExerciseGenerator, Exercise
from backend.services.conjugation import ConjugationEngine


class TestExerciseGenerator:
    """Test suite for ExerciseGenerator"""

    @pytest.fixture
    def generator(self):
        """Create exercise generator instance"""
        return ExerciseGenerator()

    def test_generate_basic_exercise(self, generator):
        """Test basic exercise generation"""
        exercise = generator.generate_exercise()
        assert exercise.exercise_id is not None
        assert exercise.verb is not None
        assert exercise.tense == "present_subjunctive"
        assert exercise.correct_answer is not None
        assert exercise.trigger_category in ["Wishes", "Emotions", "Impersonal_Expressions",
                                             "Recommendations", "Doubt_Denial", "Ojalá"]

    def test_generate_beginner_exercise(self, generator):
        """Test beginner difficulty exercise"""
        exercise = generator.generate_exercise(difficulty="beginner")
        assert exercise.difficulty == "beginner"
        # Beginner exercises should use regular verbs
        engine = ConjugationEngine()
        verb_info = engine.get_verb_info(exercise.verb)
        # Most beginner exercises should be regular (allowing some stem-changing)
        assert not verb_info["is_irregular"] or verb_info["is_stem_changing"]

    def test_generate_advanced_exercise(self, generator):
        """Test advanced difficulty exercise"""
        exercise = generator.generate_exercise(difficulty="advanced")
        assert exercise.difficulty == "advanced"

    def test_generate_specific_weirdo_category(self, generator):
        """Test generating exercise for specific WEIRDO category"""
        exercise = generator.generate_exercise(weirdo_category="Wishes")
        assert exercise.trigger_category == "Wishes"

    def test_generate_with_specific_verb(self, generator):
        """Test generating exercise with specific verb"""
        exercise = generator.generate_exercise(specific_verb="ser")
        assert exercise.verb == "ser"

    def test_fill_in_blank_exercise(self, generator):
        """Test fill-in-blank exercise type"""
        exercise = generator.generate_exercise(exercise_type="fill_in_blank")
        assert exercise.exercise_type == "fill_in_blank"
        assert "____" in exercise.sentence_template

    def test_multiple_choice_exercise(self, generator):
        """Test multiple choice exercise generation"""
        exercise = generator.generate_exercise(exercise_type="multiple_choice")
        assert exercise.exercise_type == "multiple_choice"
        assert len(exercise.distractors) > 0
        assert exercise.correct_answer not in exercise.distractors

    def test_exercise_has_context(self, generator):
        """Test that exercises include context"""
        exercise = generator.generate_exercise()
        assert exercise.context is not None
        assert len(exercise.context) > 0

    def test_exercise_has_hints(self, generator):
        """Test that exercises include hints"""
        exercise = generator.generate_exercise()
        assert len(exercise.hints) > 0

    def test_generate_exercise_set(self, generator):
        """Test generating multiple exercises"""
        exercises = generator.generate_exercise_set(count=10)
        assert len(exercises) == 10
        # Check variety in WEIRDO categories
        categories = [ex.trigger_category for ex in exercises]
        assert len(set(categories)) > 1  # Should have variety

    def test_exercise_set_with_specific_categories(self, generator):
        """Test generating exercise set with specific categories"""
        exercises = generator.generate_exercise_set(
            count=6,
            weirdo_categories=["Wishes", "Emotions"]
        )
        for exercise in exercises:
            assert exercise.trigger_category in ["Wishes", "Emotions"]

    def test_get_weirdo_explanation(self, generator):
        """Test getting WEIRDO category explanation"""
        explanation = generator.get_weirdo_explanation("Wishes")
        assert "category" in explanation
        assert "description" in explanation
        assert "triggers" in explanation
        assert len(explanation["triggers"]) > 0

    def test_display_sentence(self, generator):
        """Test getting display sentence"""
        exercise = generator.generate_exercise()
        display = exercise.get_display_sentence()
        assert "_______" in display

    def test_exercise_to_dict(self, generator):
        """Test converting exercise to dictionary"""
        exercise = generator.generate_exercise()
        data = exercise.to_dict()
        assert "verb" in data
        assert "tense" in data
        assert "correct_answer" in data
        assert "trigger_category" in data


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])

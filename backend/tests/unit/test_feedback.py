"""
Unit tests for Feedback Generator and Error Analyzer.

Tests cover:
- Error analysis and categorization
- Pattern detection
- Feedback generation
- Encouragement messages
- Suggestions
"""

import pytest
from backend.services.feedback import (
    FeedbackGenerator,
    ErrorAnalyzer,
    Feedback,
    ErrorPattern
)
from backend.services.conjugation import ConjugationEngine, ValidationResult


@pytest.mark.unit
@pytest.mark.feedback
class TestErrorAnalyzer:
    """Test suite for ErrorAnalyzer."""

    def test_analyzer_initialization(self, error_analyzer):
        """Test analyzer initializes correctly."""
        assert error_analyzer is not None
        assert len(error_analyzer.error_history) == 0

    # ========================================================================
    # Error Analysis Tests
    # ========================================================================

    def test_analyze_correct_answer(self, error_analyzer):
        """Test analyzing correct answer."""
        validation = ValidationResult(
            is_correct=True,
            user_answer="hable",
            correct_answer="hable",
            verb="hablar",
            tense="present_subjunctive",
            person="yo"
        )

        analysis = error_analyzer.analyze_error(validation)

        assert analysis["error_type"] is None
        assert analysis["severity"] == "none"

    def test_analyze_incorrect_answer(self, error_analyzer):
        """Test analyzing incorrect answer."""
        validation = ValidationResult(
            is_correct=False,
            user_answer="hablo",
            correct_answer="hable",
            verb="hablar",
            tense="present_subjunctive",
            person="yo",
            error_type="mood_confusion"
        )

        analysis = error_analyzer.analyze_error(validation)

        assert analysis["error_type"] == "mood_confusion"
        assert analysis["severity"] in ["high", "medium", "low"]
        assert len(analysis["suggestions"]) > 0

    # ========================================================================
    # Error Severity Tests
    # ========================================================================

    @pytest.mark.parametrize("error_type,expected_severity", [
        ("mood_confusion", "high"),
        ("stem_change_error", "high"),
        ("wrong_person", "medium"),
        ("wrong_tense", "medium"),
        ("spelling_change_error", "medium"),
        ("spelling_error", "low"),
        ("wrong_ending", "low"),
    ])
    def test_error_severity_classification(self, error_analyzer, error_type, expected_severity):
        """Test error severity classification."""
        severity = error_analyzer._determine_severity(error_type)
        assert severity == expected_severity

    # ========================================================================
    # Error Pattern Detection Tests
    # ========================================================================

    def test_detect_patterns_empty(self, error_analyzer):
        """Test pattern detection with no errors."""
        patterns = error_analyzer.detect_patterns()

        assert len(patterns) == 0

    def test_detect_patterns_insufficient_data(self, error_analyzer):
        """Test pattern detection with insufficient data."""
        # Add only 2 errors (below threshold of 3)
        for i in range(2):
            validation = ValidationResult(
                is_correct=False,
                user_answer="hablo",
                correct_answer="hable",
                verb="hablar",
                tense="present_subjunctive",
                person="yo",
                error_type="mood_confusion"
            )
            error_analyzer.analyze_error(validation)

        patterns = error_analyzer.detect_patterns(min_frequency=3)

        assert len(patterns) == 0

    def test_detect_patterns_with_data(self, error_analyzer):
        """Test pattern detection with sufficient data."""
        # Add 5 mood confusion errors
        for i in range(5):
            validation = ValidationResult(
                is_correct=False,
                user_answer="hablo",
                correct_answer="hable",
                verb="hablar",
                tense="present_subjunctive",
                person="yo",
                error_type="mood_confusion"
            )
            error_analyzer.analyze_error(validation)

        patterns = error_analyzer.detect_patterns(min_frequency=3)

        assert len(patterns) > 0
        assert patterns[0].error_type == "mood_confusion"
        assert patterns[0].frequency == 5

    def test_patterns_sorted_by_frequency(self, error_analyzer):
        """Test patterns are sorted by frequency."""
        # Add different error types with different frequencies
        error_types = [
            ("mood_confusion", 5),
            ("wrong_person", 3),
            ("spelling_error", 4)
        ]

        for error_type, count in error_types:
            for i in range(count):
                validation = ValidationResult(
                    is_correct=False,
                    user_answer="wrong",
                    correct_answer="right",
                    verb="hablar",
                    tense="present_subjunctive",
                    person="yo",
                    error_type=error_type
                )
                error_analyzer.analyze_error(validation)

        patterns = error_analyzer.detect_patterns(min_frequency=3)

        # Should be sorted by frequency descending
        assert patterns[0].frequency >= patterns[-1].frequency

    # ========================================================================
    # Error Summary Tests
    # ========================================================================

    def test_error_summary_empty(self, error_analyzer):
        """Test error summary with no errors."""
        summary = error_analyzer.get_error_summary()

        assert summary["total_errors"] == 0
        assert summary["most_common_error"] is None

    def test_error_summary_with_errors(self, error_analyzer):
        """Test error summary with errors."""
        # Add various errors
        for i in range(5):
            validation = ValidationResult(
                is_correct=False,
                user_answer="wrong",
                correct_answer="right",
                verb="hablar",
                tense="present_subjunctive",
                person="yo",
                error_type="mood_confusion"
            )
            error_analyzer.analyze_error(validation)

        summary = error_analyzer.get_error_summary()

        assert summary["total_errors"] == 5
        assert summary["most_common_error"] == "mood_confusion"
        assert "error_types" in summary


@pytest.mark.unit
@pytest.mark.feedback
class TestFeedbackGenerator:
    """Test suite for FeedbackGenerator."""

    def test_generator_initialization(self, feedback_generator):
        """Test generator initializes correctly."""
        assert feedback_generator is not None
        assert feedback_generator.engine is not None
        assert feedback_generator.error_analyzer is not None

    # ========================================================================
    # Positive Feedback Tests
    # ========================================================================

    def test_generate_positive_feedback(self, feedback_generator, conjugation_engine):
        """Test generating positive feedback for correct answer."""
        validation = conjugation_engine.validate_answer(
            "hablar",
            "present_subjunctive",
            "yo",
            "hable"
        )

        feedback = feedback_generator.generate_feedback(validation)

        assert isinstance(feedback, Feedback)
        assert feedback.is_correct
        assert len(feedback.message) > 0
        assert len(feedback.explanation) > 0
        assert len(feedback.encouragement) > 0

    def test_positive_feedback_irregular_verb(self, feedback_generator, conjugation_engine):
        """Test positive feedback mentions irregular verb."""
        validation = conjugation_engine.validate_answer(
            "ser",
            "present_subjunctive",
            "yo",
            "sea"
        )

        feedback = feedback_generator.generate_feedback(validation)

        assert feedback.is_correct
        assert "irregular" in feedback.explanation.lower()

    def test_positive_feedback_stem_changing(self, feedback_generator, conjugation_engine):
        """Test positive feedback mentions stem change."""
        validation = conjugation_engine.validate_answer(
            "pensar",
            "present_subjunctive",
            "yo",
            "piense"
        )

        feedback = feedback_generator.generate_feedback(validation)

        assert feedback.is_correct
        # Should mention stem change
        explanation_lower = feedback.explanation.lower()
        assert "stem" in explanation_lower or "change" in explanation_lower

    # ========================================================================
    # Corrective Feedback Tests
    # ========================================================================

    def test_generate_corrective_feedback(self, feedback_generator, conjugation_engine):
        """Test generating corrective feedback for incorrect answer."""
        validation = conjugation_engine.validate_answer(
            "hablar",
            "present_subjunctive",
            "yo",
            "hablo"
        )

        feedback = feedback_generator.generate_feedback(validation)

        assert not feedback.is_correct
        assert feedback.error_category is not None
        assert len(feedback.suggestions) > 0
        assert "hable" in feedback.message  # Should show correct answer

    def test_corrective_feedback_includes_explanation(self, feedback_generator, conjugation_engine):
        """Test corrective feedback includes explanation."""
        validation = conjugation_engine.validate_answer(
            "ser",
            "present_subjunctive",
            "yo",
            "soy"
        )

        feedback = feedback_generator.generate_feedback(validation)

        assert len(feedback.explanation) > 0
        assert len(feedback.suggestions) > 0

    # ========================================================================
    # Context-Aware Feedback Tests
    # ========================================================================

    def test_feedback_with_context(self, feedback_generator, conjugation_engine):
        """Test feedback includes context information."""
        validation = conjugation_engine.validate_answer(
            "hablar",
            "present_subjunctive",
            "yo",
            "hable"
        )

        context = {
            "trigger_phrase": "quiero que",
            "trigger_category": "Wishes"
        }

        feedback = feedback_generator.generate_feedback(validation, context)

        # Should mention trigger in explanation
        assert "quiero que" in feedback.explanation.lower() or "wish" in feedback.explanation.lower()

    # ========================================================================
    # Encouragement Tests
    # ========================================================================

    def test_positive_encouragement(self, feedback_generator, conjugation_engine):
        """Test encouragement for correct answers."""
        validation = conjugation_engine.validate_answer(
            "hablar",
            "present_subjunctive",
            "yo",
            "hable"
        )

        feedback = feedback_generator.generate_feedback(validation)

        assert len(feedback.encouragement) > 0
        # Should be positive
        encouragement_lower = feedback.encouragement.lower()
        positive_words = ["great", "excellent", "good", "keep", "progress"]
        assert any(word in encouragement_lower for word in positive_words)

    def test_supportive_encouragement(self, feedback_generator, conjugation_engine):
        """Test encouragement for incorrect answers is supportive."""
        validation = conjugation_engine.validate_answer(
            "hablar",
            "present_subjunctive",
            "yo",
            "hablo"
        )

        feedback = feedback_generator.generate_feedback(validation)

        assert len(feedback.encouragement) > 0
        # Should be supportive
        encouragement_lower = feedback.encouragement.lower()
        supportive_words = ["practice", "learning", "try", "improve", "opportunity"]
        assert any(word in encouragement_lower for word in supportive_words)

    # ========================================================================
    # Suggestions Tests
    # ========================================================================

    def test_suggestions_for_mood_confusion(self, feedback_generator, conjugation_engine):
        """Test suggestions for mood confusion errors."""
        validation = conjugation_engine.validate_answer(
            "hablar",
            "present_subjunctive",
            "yo",
            "hablo"
        )

        feedback = feedback_generator.generate_feedback(validation)

        suggestions_text = " ".join(feedback.suggestions).lower()
        assert "weirdo" in suggestions_text or "trigger" in suggestions_text or "subjunctive" in suggestions_text

    def test_suggestions_specific_to_error(self, feedback_generator, conjugation_engine):
        """Test suggestions are specific to error type."""
        validation = conjugation_engine.validate_answer(
            "hablar",
            "present_subjunctive",
            "yo",
            "hables"  # Wrong person
        )

        feedback = feedback_generator.generate_feedback(validation)

        suggestions_text = " ".join(feedback.suggestions).lower()
        assert "person" in suggestions_text or "subject" in suggestions_text

    # ========================================================================
    # Next Steps Tests
    # ========================================================================

    def test_next_steps_provided(self, feedback_generator, conjugation_engine):
        """Test next steps are provided."""
        validation = conjugation_engine.validate_answer(
            "hablar",
            "present_subjunctive",
            "yo",
            "hablo"
        )

        feedback = feedback_generator.generate_feedback(validation)

        assert len(feedback.next_steps) > 0
        assert all(isinstance(step, str) for step in feedback.next_steps)

    def test_next_steps_for_correct_answer(self, feedback_generator, conjugation_engine):
        """Test next steps for correct answer."""
        validation = conjugation_engine.validate_answer(
            "hablar",
            "present_subjunctive",
            "yo",
            "hable"
        )

        feedback = feedback_generator.generate_feedback(validation)

        assert len(feedback.next_steps) > 0
        # Should encourage continued practice
        steps_text = " ".join(feedback.next_steps).lower()
        assert "practice" in steps_text or "continue" in steps_text or "try" in steps_text

    # ========================================================================
    # Related Rules Tests
    # ========================================================================

    def test_related_rules_included(self, feedback_generator, conjugation_engine):
        """Test related grammar rules are included."""
        validation = conjugation_engine.validate_answer(
            "ser",
            "present_subjunctive",
            "yo",
            "sea"
        )

        context = {
            "trigger_category": "Wishes",
            "trigger_phrase": "quiero que"
        }

        feedback = feedback_generator.generate_feedback(validation, context)

        assert len(feedback.related_rules) > 0

    def test_related_rules_for_irregular_verb(self, feedback_generator, conjugation_engine):
        """Test related rules for irregular verb."""
        validation = conjugation_engine.validate_answer(
            "ser",
            "present_subjunctive",
            "yo",
            "sea"
        )

        feedback = feedback_generator.generate_feedback(validation)

        rules_text = " ".join(feedback.related_rules).lower()
        assert "irregular" in rules_text or "ser" in rules_text

    # ========================================================================
    # Feedback to Dict Tests
    # ========================================================================

    def test_feedback_to_dict(self, feedback_generator, conjugation_engine):
        """Test converting feedback to dictionary."""
        validation = conjugation_engine.validate_answer(
            "hablar",
            "present_subjunctive",
            "yo",
            "hable"
        )

        feedback = feedback_generator.generate_feedback(validation)
        feedback_dict = feedback.to_dict()

        assert isinstance(feedback_dict, dict)
        assert "is_correct" in feedback_dict
        assert "message" in feedback_dict
        assert "explanation" in feedback_dict
        assert "suggestions" in feedback_dict

    # ========================================================================
    # User Level Tests
    # ========================================================================

    @pytest.mark.parametrize("user_level", ["beginner", "intermediate", "advanced"])
    def test_feedback_for_different_levels(self, feedback_generator, conjugation_engine, user_level):
        """Test feedback adapts to user level."""
        validation = conjugation_engine.validate_answer(
            "hablar",
            "present_subjunctive",
            "yo",
            "hable"
        )

        feedback = feedback_generator.generate_feedback(validation, user_level=user_level)

        assert feedback is not None
        assert len(feedback.message) > 0

    # ========================================================================
    # Edge Cases
    # ========================================================================

    def test_feedback_without_context(self, feedback_generator, conjugation_engine):
        """Test feedback generation without context."""
        validation = conjugation_engine.validate_answer(
            "hablar",
            "present_subjunctive",
            "yo",
            "hable"
        )

        feedback = feedback_generator.generate_feedback(validation, exercise_context=None)

        assert feedback is not None
        assert len(feedback.message) > 0

    def test_feedback_multiple_suggestions(self, feedback_generator, conjugation_engine):
        """Test feedback includes multiple suggestions."""
        validation = conjugation_engine.validate_answer(
            "ser",
            "present_subjunctive",
            "yo",
            "soy"
        )

        feedback = feedback_generator.generate_feedback(validation)

        assert len(feedback.suggestions) >= 1

    def test_no_duplicate_suggestions(self, feedback_generator, conjugation_engine):
        """Test feedback doesn't have duplicate suggestions."""
        validation = conjugation_engine.validate_answer(
            "hablar",
            "present_subjunctive",
            "yo",
            "hablo"
        )

        feedback = feedback_generator.generate_feedback(validation)

        # Check for duplicates
        assert len(feedback.suggestions) == len(set(feedback.suggestions))

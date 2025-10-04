"""
Unit tests for Spanish Conjugation Engine.

Tests cover:
- Regular verb conjugations (all types)
- Irregular verb conjugations
- Stem-changing verb conjugations
- Spelling changes
- Answer validation
- Error analysis
"""

import pytest
from backend.services.conjugation import (
    ConjugationEngine,
    ConjugationResult,
    ValidationResult
)


@pytest.mark.unit
@pytest.mark.conjugation
class TestConjugationEngine:
    """Test suite for ConjugationEngine."""

    def test_engine_initialization(self, conjugation_engine):
        """Test engine initializes correctly."""
        assert conjugation_engine is not None
        assert conjugation_engine.regular_endings is not None
        assert conjugation_engine.irregular_verbs is not None

    # ========================================================================
    # Regular Verb Tests
    # ========================================================================

    @pytest.mark.parametrize("verb,person,expected", [
        ("hablar", "yo", "hable"),
        ("hablar", "tú", "hables"),
        ("hablar", "él/ella/usted", "hable"),
        ("hablar", "nosotros/nosotras", "hablemos"),
        ("hablar", "vosotros/vosotras", "habléis"),
        ("hablar", "ellos/ellas/ustedes", "hablen"),
    ])
    def test_conjugate_regular_ar_verb(self, conjugation_engine, verb, person, expected):
        """Test regular -ar verb conjugations."""
        result = conjugation_engine.conjugate(verb, "present_subjunctive", person)

        assert isinstance(result, ConjugationResult)
        assert result.conjugation == expected
        assert result.verb == verb
        assert result.tense == "present_subjunctive"
        assert result.person == person
        assert not result.is_irregular
        assert not result.is_stem_changing

    @pytest.mark.parametrize("verb,person,expected", [
        ("comer", "yo", "coma"),
        ("comer", "tú", "comas"),
        ("comer", "él/ella/usted", "coma"),
        ("comer", "nosotros/nosotras", "comamos"),
        ("comer", "vosotros/vosotras", "comáis"),
        ("comer", "ellos/ellas/ustedes", "coman"),
    ])
    def test_conjugate_regular_er_verb(self, conjugation_engine, verb, person, expected):
        """Test regular -er verb conjugations."""
        result = conjugation_engine.conjugate(verb, "present_subjunctive", person)
        assert result.conjugation == expected

    @pytest.mark.parametrize("verb,person,expected", [
        ("vivir", "yo", "viva"),
        ("vivir", "tú", "vivas"),
        ("vivir", "él/ella/usted", "viva"),
        ("vivir", "nosotros/nosotras", "vivamos"),
        ("vivir", "vosotros/vosotras", "viváis"),
        ("vivir", "ellos/ellas/ustedes", "vivan"),
    ])
    def test_conjugate_regular_ir_verb(self, conjugation_engine, verb, person, expected):
        """Test regular -ir verb conjugations."""
        result = conjugation_engine.conjugate(verb, "present_subjunctive", person)
        assert result.conjugation == expected

    # ========================================================================
    # Irregular Verb Tests
    # ========================================================================

    @pytest.mark.parametrize("verb,person,expected", [
        ("ser", "yo", "sea"),
        ("ser", "tú", "seas"),
        ("ser", "él/ella/usted", "sea"),
        ("estar", "yo", "esté"),
        ("estar", "tú", "estés"),
        ("ir", "yo", "vaya"),
        ("ir", "tú", "vayas"),
        ("haber", "yo", "haya"),
        ("haber", "él/ella/usted", "haya"),
        ("tener", "yo", "tenga"),
        ("tener", "tú", "tengas"),
        ("hacer", "yo", "haga"),
        ("hacer", "tú", "hagas"),
        ("poder", "yo", "pueda"),
        ("poder", "tú", "puedas"),
        ("saber", "yo", "sepa"),
        ("saber", "tú", "sepas"),
        ("dar", "yo", "dé"),
        ("dar", "tú", "des"),
    ])
    def test_conjugate_irregular_verbs(self, conjugation_engine, verb, person, expected):
        """Test common irregular verb conjugations."""
        result = conjugation_engine.conjugate(verb, "present_subjunctive", person)

        assert result.conjugation == expected
        assert result.is_irregular
        assert not result.is_stem_changing

    # ========================================================================
    # Stem-Changing Verb Tests
    # ========================================================================

    @pytest.mark.parametrize("verb,person,expected,pattern", [
        ("pensar", "yo", "piense", "e→ie"),
        ("pensar", "tú", "pienses", "e→ie"),
        ("pensar", "él/ella/usted", "piense", "e→ie"),
        ("querer", "yo", "quiera", "e→ie"),
        ("querer", "tú", "quieras", "e→ie"),
        ("sentir", "yo", "sienta", "e→ie"),
        ("sentir", "tú", "sientas", "e→ie"),
    ])
    def test_conjugate_stem_changing_e_ie(self, conjugation_engine, verb, person, expected, pattern):
        """Test e→ie stem-changing verbs."""
        result = conjugation_engine.conjugate(verb, "present_subjunctive", person)

        assert result.conjugation == expected
        assert result.is_stem_changing or result.stem_change_pattern == pattern

    @pytest.mark.parametrize("verb,person,expected", [
        ("poder", "yo", "pueda"),
        ("poder", "tú", "puedas"),
        ("volver", "yo", "vuelva"),
        ("volver", "tú", "vuelvas"),
        ("dormir", "yo", "duerma"),
        ("dormir", "tú", "duermas"),
    ])
    def test_conjugate_stem_changing_o_ue(self, conjugation_engine, verb, person, expected):
        """Test o→ue stem-changing verbs."""
        result = conjugation_engine.conjugate(verb, "present_subjunctive", person)
        assert result.conjugation == expected

    @pytest.mark.parametrize("verb,person,expected", [
        ("pedir", "yo", "pida"),
        ("pedir", "tú", "pidas"),
        ("servir", "yo", "sirva"),
        ("servir", "tú", "sirvas"),
        ("repetir", "yo", "repita"),
        ("repetir", "tú", "repitas"),
    ])
    def test_conjugate_stem_changing_e_i(self, conjugation_engine, verb, person, expected):
        """Test e→i stem-changing verbs."""
        result = conjugation_engine.conjugate(verb, "present_subjunctive", person)
        assert result.conjugation == expected

    # ========================================================================
    # Spelling Change Tests
    # ========================================================================

    @pytest.mark.parametrize("verb,person,expected", [
        ("buscar", "yo", "busque"),
        ("buscar", "tú", "busques"),
        ("pagar", "yo", "pague"),
        ("pagar", "tú", "pagues"),
        ("empezar", "yo", "empiece"),
        ("empezar", "tú", "empieces"),
    ])
    def test_conjugate_spelling_changes(self, conjugation_engine, verb, person, expected):
        """Test verbs with orthographic spelling changes."""
        result = conjugation_engine.conjugate(verb, "present_subjunctive", person)
        assert result.conjugation == expected

    # ========================================================================
    # Imperfect Subjunctive Tests
    # ========================================================================

    @pytest.mark.parametrize("verb,tense,person,expected", [
        ("hablar", "imperfect_subjunctive_ra", "yo", "hablara"),
        ("hablar", "imperfect_subjunctive_ra", "tú", "hablaras"),
        ("hablar", "imperfect_subjunctive_se", "yo", "hablase"),
        ("hablar", "imperfect_subjunctive_se", "tú", "hablases"),
        ("comer", "imperfect_subjunctive_ra", "yo", "comiera"),
        ("vivir", "imperfect_subjunctive_ra", "yo", "viviera"),
    ])
    def test_conjugate_imperfect_subjunctive(self, conjugation_engine, verb, tense, person, expected):
        """Test imperfect subjunctive conjugations."""
        result = conjugation_engine.conjugate(verb, tense, person)
        assert result.conjugation == expected

    # ========================================================================
    # Full Conjugation Table Tests
    # ========================================================================

    def test_get_full_conjugation_table(self, conjugation_engine):
        """Test getting complete conjugation table."""
        table = conjugation_engine.get_full_conjugation_table("hablar", "present_subjunctive")

        assert len(table) == 6
        assert "yo" in table
        assert "tú" in table
        assert table["yo"].conjugation == "hable"
        assert table["tú"].conjugation == "hables"
        assert table["él/ella/usted"].conjugation == "hable"

    def test_get_full_conjugation_table_irregular(self, conjugation_engine):
        """Test full conjugation table for irregular verb."""
        table = conjugation_engine.get_full_conjugation_table("ser", "present_subjunctive")

        assert table["yo"].conjugation == "sea"
        assert table["tú"].conjugation == "seas"
        assert all(result.is_irregular for result in table.values() if result)

    # ========================================================================
    # Validation Tests
    # ========================================================================

    def test_validate_correct_answer(self, conjugation_engine):
        """Test validation of correct answer."""
        validation = conjugation_engine.validate_answer(
            "hablar", "present_subjunctive", "yo", "hable"
        )

        assert isinstance(validation, ValidationResult)
        assert validation.is_correct
        assert validation.user_answer == "hable"
        assert validation.correct_answer == "hable"
        assert validation.error_type is None

    def test_validate_incorrect_answer(self, conjugation_engine):
        """Test validation of incorrect answer."""
        validation = conjugation_engine.validate_answer(
            "hablar", "present_subjunctive", "yo", "hablo"
        )

        assert not validation.is_correct
        assert validation.user_answer == "hablo"
        assert validation.correct_answer == "hable"
        assert validation.error_type is not None
        assert len(validation.suggestions) > 0

    def test_validate_case_insensitive(self, conjugation_engine):
        """Test validation is case insensitive."""
        validation = conjugation_engine.validate_answer(
            "hablar", "present_subjunctive", "yo", "HABLE"
        )
        assert validation.is_correct

    def test_validate_with_whitespace(self, conjugation_engine):
        """Test validation handles whitespace."""
        validation = conjugation_engine.validate_answer(
            "hablar", "present_subjunctive", "yo", "  hable  "
        )
        assert validation.is_correct

    # ========================================================================
    # Error Analysis Tests
    # ========================================================================

    def test_error_type_mood_confusion(self, conjugation_engine):
        """Test detection of mood confusion error."""
        validation = conjugation_engine.validate_answer(
            "hablar", "present_subjunctive", "yo", "hablo"
        )

        assert validation.error_type == "mood_confusion"
        assert any("indicative" in s.lower() for s in validation.suggestions)

    def test_error_type_wrong_person(self, conjugation_engine):
        """Test detection of wrong person error."""
        validation = conjugation_engine.validate_answer(
            "hablar", "present_subjunctive", "yo", "hables"
        )

        assert validation.error_type == "wrong_person"
        assert "tú" in str(validation.suggestions)

    # ========================================================================
    # Verb Info Tests
    # ========================================================================

    def test_get_verb_info_regular(self, conjugation_engine):
        """Test getting info for regular verb."""
        info = conjugation_engine.get_verb_info("hablar")

        assert info["verb"] == "hablar"
        assert info["type"] == "-ar"
        assert not info["is_irregular"]
        assert not info["is_stem_changing"]

    def test_get_verb_info_irregular(self, conjugation_engine):
        """Test getting info for irregular verb."""
        info = conjugation_engine.get_verb_info("ser")

        assert info["verb"] == "ser"
        assert info["is_irregular"]

    def test_get_verb_info_stem_changing(self, conjugation_engine):
        """Test getting info for stem-changing verb."""
        info = conjugation_engine.get_verb_info("pensar")

        assert info["verb"] == "pensar"
        assert info["is_stem_changing"]
        assert info["stem_change_pattern"] == "e→ie"

    def test_get_supported_verbs(self, conjugation_engine):
        """Test getting list of supported verbs."""
        verbs = conjugation_engine.get_supported_verbs()

        assert "irregular" in verbs
        assert "regular_ar" in verbs
        assert "stem_changing_e_ie" in verbs
        assert len(verbs["irregular"]) > 0
        assert "ser" in verbs["irregular"]

    # ========================================================================
    # Error Handling Tests
    # ========================================================================

    def test_conjugate_empty_verb_raises_error(self, conjugation_engine):
        """Test conjugating empty verb raises error."""
        with pytest.raises(ValueError, match="cannot be empty"):
            conjugation_engine.conjugate("", "present_subjunctive", "yo")

    def test_conjugate_invalid_verb_raises_error(self, conjugation_engine):
        """Test conjugating invalid verb raises error."""
        with pytest.raises(ValueError, match="Invalid verb"):
            conjugation_engine.conjugate("invalid", "present_subjunctive", "yo")

    def test_conjugate_invalid_tense_raises_error(self, conjugation_engine):
        """Test conjugating with invalid tense raises error."""
        with pytest.raises(ValueError, match="Invalid tense"):
            conjugation_engine.conjugate("hablar", "invalid_tense", "yo")

    # ========================================================================
    # ConjugationResult Tests
    # ========================================================================

    def test_conjugation_result_to_dict(self, conjugation_engine):
        """Test converting ConjugationResult to dictionary."""
        result = conjugation_engine.conjugate("hablar", "present_subjunctive", "yo")
        result_dict = result.to_dict()

        assert isinstance(result_dict, dict)
        assert result_dict["verb"] == "hablar"
        assert result_dict["conjugation"] == "hable"
        assert result_dict["tense"] == "present_subjunctive"
        assert result_dict["person"] == "yo"

    # ========================================================================
    # Edge Cases
    # ========================================================================

    def test_conjugate_with_accents(self, conjugation_engine):
        """Test conjugating verbs with accents."""
        result = conjugation_engine.conjugate("estudiar", "present_subjunctive", "vosotros/vosotras")
        assert "é" in result.conjugation  # Should have accent

    def test_conjugate_all_persons_consistency(self, conjugation_engine):
        """Test all persons produce valid conjugations."""
        persons = [
            "yo", "tú", "él/ella/usted",
            "nosotros/nosotras", "vosotros/vosotras", "ellos/ellas/ustedes"
        ]

        for person in persons:
            result = conjugation_engine.conjugate("hablar", "present_subjunctive", person)
            assert result.conjugation is not None
            assert len(result.conjugation) > 0

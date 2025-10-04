"""
Comprehensive Test Suite for Conjugation Engine

Tests regular verbs, irregular verbs, stem-changing verbs,
spelling changes, and validation functionality.
"""

import pytest
from backend.services.conjugation import ConjugationEngine, ConjugationResult, ValidationResult


class TestConjugationEngine:
    """Test suite for ConjugationEngine"""

    @pytest.fixture
    def engine(self):
        """Create conjugation engine instance"""
        return ConjugationEngine()

    # Regular Verb Tests
    def test_regular_ar_verb_present(self, engine):
        """Test regular -ar verb in present subjunctive"""
        result = engine.conjugate("hablar", "present_subjunctive", "yo")
        assert result.conjugation == "hable"
        assert not result.is_irregular
        assert not result.is_stem_changing

    def test_regular_er_verb_present(self, engine):
        """Test regular -er verb in present subjunctive"""
        result = engine.conjugate("comer", "present_subjunctive", "tú")
        assert result.conjugation == "comas"

    def test_regular_ir_verb_present(self, engine):
        """Test regular -ir verb in present subjunctive"""
        result = engine.conjugate("vivir", "present_subjunctive", "él/ella/usted")
        assert result.conjugation == "viva"

    def test_regular_verb_imperfect_ra(self, engine):
        """Test regular verb in imperfect subjunctive -ra form"""
        result = engine.conjugate("hablar", "imperfect_subjunctive_ra", "yo")
        assert result.conjugation == "hablara"

    def test_regular_verb_imperfect_se(self, engine):
        """Test regular verb in imperfect subjunctive -se form"""
        result = engine.conjugate("hablar", "imperfect_subjunctive_se", "yo")
        assert result.conjugation == "hablase"

    # Irregular Verb Tests
    def test_irregular_ser_present(self, engine):
        """Test irregular verb 'ser' in present subjunctive"""
        result = engine.conjugate("ser", "present_subjunctive", "yo")
        assert result.conjugation == "sea"
        assert result.is_irregular

    def test_irregular_estar_present(self, engine):
        """Test irregular verb 'estar'"""
        result = engine.conjugate("estar", "present_subjunctive", "tú")
        assert result.conjugation == "estés"

    def test_irregular_ir_present(self, engine):
        """Test irregular verb 'ir'"""
        result = engine.conjugate("ir", "present_subjunctive", "nosotros/nosotras")
        assert result.conjugation == "vayamos"

    def test_irregular_haber_present(self, engine):
        """Test irregular verb 'haber'"""
        result = engine.conjugate("haber", "present_subjunctive", "yo")
        assert result.conjugation == "haya"

    def test_irregular_saber_present(self, engine):
        """Test irregular verb 'saber'"""
        result = engine.conjugate("saber", "present_subjunctive", "yo")
        assert result.conjugation == "sepa"

    def test_irregular_dar_present(self, engine):
        """Test irregular verb 'dar'"""
        result = engine.conjugate("dar", "present_subjunctive", "yo")
        assert result.conjugation == "dé"

    def test_irregular_ver_present(self, engine):
        """Test irregular verb 'ver'"""
        result = engine.conjugate("ver", "present_subjunctive", "yo")
        assert result.conjugation == "vea"

    def test_irregular_hacer_imperfect(self, engine):
        """Test irregular verb 'hacer' in imperfect"""
        result = engine.conjugate("hacer", "imperfect_subjunctive_ra", "yo")
        assert result.conjugation == "hiciera"

    def test_irregular_tener_present(self, engine):
        """Test irregular verb 'tener'"""
        result = engine.conjugate("tener", "present_subjunctive", "yo")
        assert result.conjugation == "tenga"

    # Stem-Changing Verb Tests
    def test_stem_change_e_ie_querer(self, engine):
        """Test e→ie stem change: querer"""
        result = engine.conjugate("querer", "present_subjunctive", "yo")
        assert result.conjugation == "quiera"
        assert result.is_stem_changing
        assert result.stem_change_pattern == "e→ie"

    def test_stem_change_o_ue_poder(self, engine):
        """Test o→ue stem change: poder"""
        result = engine.conjugate("poder", "present_subjunctive", "yo")
        assert result.conjugation == "pueda"

    def test_stem_change_e_i_pedir(self, engine):
        """Test e→i stem change: pedir"""
        result = engine.conjugate("pedir", "present_subjunctive", "yo")
        assert result.conjugation == "pida"

    # Spelling Change Tests
    def test_spelling_change_car_buscar(self, engine):
        """Test c→qu spelling change"""
        result = engine.conjugate("buscar", "present_subjunctive", "yo")
        assert result.conjugation == "busque"
        assert result.has_spelling_change

    def test_spelling_change_gar_pagar(self, engine):
        """Test g→gu spelling change"""
        result = engine.conjugate("pagar", "present_subjunctive", "yo")
        assert result.conjugation == "pague"
        assert result.has_spelling_change

    def test_spelling_change_zar_empezar(self, engine):
        """Test z→c spelling change"""
        result = engine.conjugate("empezar", "present_subjunctive", "yo")
        # Note: empezar is also stem-changing
        assert result.conjugation == "empiece"

    # Full Conjugation Table Tests
    def test_full_conjugation_table_ser(self, engine):
        """Test full conjugation table for 'ser'"""
        table = engine.get_full_conjugation_table("ser", "present_subjunctive")
        assert table["yo"].conjugation == "sea"
        assert table["tú"].conjugation == "seas"
        assert table["él/ella/usted"].conjugation == "sea"
        assert table["nosotros/nosotras"].conjugation == "seamos"
        assert table["vosotros/vosotras"].conjugation == "seáis"
        assert table["ellos/ellas/ustedes"].conjugation == "sean"

    def test_full_conjugation_table_hablar(self, engine):
        """Test full conjugation table for regular verb"""
        table = engine.get_full_conjugation_table("hablar", "present_subjunctive")
        assert table["yo"].conjugation == "hable"
        assert table["tú"].conjugation == "hables"
        assert table["nosotros/nosotras"].conjugation == "hablemos"

    # Validation Tests
    def test_validate_correct_answer(self, engine):
        """Test validation with correct answer"""
        result = engine.validate_answer("hablar", "present_subjunctive", "yo", "hable")
        assert result.is_correct
        assert result.error_type is None

    def test_validate_incorrect_answer(self, engine):
        """Test validation with incorrect answer"""
        result = engine.validate_answer("hablar", "present_subjunctive", "yo", "hablo")
        assert not result.is_correct
        assert result.error_type == "mood_confusion"

    def test_validate_wrong_person(self, engine):
        """Test validation with wrong person"""
        result = engine.validate_answer("hablar", "present_subjunctive", "yo", "hables")
        assert not result.is_correct
        assert result.error_type == "wrong_person"

    def test_validate_spelling_error(self, engine):
        """Test validation with spelling error"""
        result = engine.validate_answer("hablar", "present_subjunctive", "yo", "habl")
        assert not result.is_correct
        assert len(result.suggestions) > 0

    # Edge Cases and Error Handling
    def test_invalid_verb_raises_error(self, engine):
        """Test that invalid verb raises error"""
        with pytest.raises(ValueError):
            engine.conjugate("invalid", "present_subjunctive", "yo")

    def test_invalid_tense_raises_error(self, engine):
        """Test that invalid tense raises error"""
        with pytest.raises(ValueError):
            engine.conjugate("hablar", "invalid_tense", "yo")

    def test_empty_verb_raises_error(self, engine):
        """Test that empty verb raises error"""
        with pytest.raises(ValueError):
            engine.conjugate("", "present_subjunctive", "yo")

    # Verb Info Tests
    def test_get_verb_info_regular(self, engine):
        """Test getting verb info for regular verb"""
        info = engine.get_verb_info("hablar")
        assert info["type"] == "-ar"
        assert not info["is_irregular"]
        assert not info["is_stem_changing"]

    def test_get_verb_info_irregular(self, engine):
        """Test getting verb info for irregular verb"""
        info = engine.get_verb_info("ser")
        assert info["is_irregular"]

    def test_get_verb_info_stem_changing(self, engine):
        """Test getting verb info for stem-changing verb"""
        info = engine.get_verb_info("querer")
        assert info["is_stem_changing"]
        assert info["stem_change_pattern"] == "e→ie"

    # Supported Verbs Tests
    def test_get_supported_verbs(self, engine):
        """Test getting supported verbs"""
        verbs = engine.get_supported_verbs()
        assert "irregular" in verbs
        assert "ser" in verbs["irregular"]
        assert len(verbs["regular_ar"]) > 0


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])

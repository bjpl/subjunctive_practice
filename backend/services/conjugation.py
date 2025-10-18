"""
Spanish Subjunctive Conjugation Engine

This module provides comprehensive Spanish subjunctive conjugation capabilities
including regular verbs, irregular verbs, stem-changing verbs, and orthographic
spelling changes.
"""

from typing import Dict, List, Optional, Tuple, Union
import logging

from utils.spanish_grammar import (
    REGULAR_ENDINGS,
    IRREGULAR_VERBS,
    STEM_CHANGING_VERBS,
    SPELLING_CHANGES,
    COMMON_REGULAR_VERBS,
    get_verb_type,
    get_verb_stem,
    apply_spelling_changes,
    is_stem_changing,
    Tense,
    Person
)


logger = logging.getLogger(__name__)


class ConjugationResult:
    """Result of a conjugation operation"""

    def __init__(
        self,
        verb: str,
        tense: str,
        person: str,
        conjugation: str,
        is_irregular: bool = False,
        is_stem_changing: bool = False,
        stem_change_pattern: Optional[str] = None,
        has_spelling_change: bool = False,
        spelling_change_rule: Optional[str] = None
    ):
        self.verb = verb
        self.tense = tense
        self.person = person
        self.conjugation = conjugation
        self.is_irregular = is_irregular
        self.is_stem_changing = is_stem_changing
        self.stem_change_pattern = stem_change_pattern
        self.has_spelling_change = has_spelling_change
        self.spelling_change_rule = spelling_change_rule

    def to_dict(self) -> Dict:
        """Convert to dictionary representation"""
        return {
            "verb": self.verb,
            "tense": self.tense,
            "person": self.person,
            "conjugation": self.conjugation,
            "is_irregular": self.is_irregular,
            "is_stem_changing": self.is_stem_changing,
            "stem_change_pattern": self.stem_change_pattern,
            "has_spelling_change": self.has_spelling_change,
            "spelling_change_rule": self.spelling_change_rule
        }


class ValidationResult:
    """Result of answer validation"""

    def __init__(
        self,
        is_correct: bool,
        user_answer: str,
        correct_answer: str,
        verb: str,
        tense: str,
        person: str,
        error_type: Optional[str] = None,
        suggestions: Optional[List[str]] = None
    ):
        self.is_correct = is_correct
        self.user_answer = user_answer
        self.correct_answer = correct_answer
        self.verb = verb
        self.tense = tense
        self.person = person
        self.error_type = error_type
        self.suggestions = suggestions or []

    def to_dict(self) -> Dict:
        """Convert to dictionary representation"""
        return {
            "is_correct": self.is_correct,
            "user_answer": self.user_answer,
            "correct_answer": self.correct_answer,
            "verb": self.verb,
            "tense": self.tense,
            "person": self.person,
            "error_type": self.error_type,
            "suggestions": self.suggestions
        }


class ConjugationEngine:
    """
    Comprehensive Spanish subjunctive conjugation engine.

    Handles:
    - Regular verb conjugations (all patterns)
    - Irregular verb conjugations (30+ verbs)
    - Stem-changing verbs (e→ie, o→ue, e→i)
    - Orthographic spelling changes (g→gu, c→qu, z→c, etc.)
    - Answer validation with error analysis
    """

    def __init__(self):
        """Initialize the conjugation engine"""
        self.logger = logging.getLogger(__name__)
        self._load_verb_data()

    def _load_verb_data(self):
        """Load and cache verb conjugation data"""
        self.regular_endings = REGULAR_ENDINGS
        self.irregular_verbs = IRREGULAR_VERBS
        self.stem_changing = STEM_CHANGING_VERBS
        self.spelling_changes = SPELLING_CHANGES
        self.common_verbs = COMMON_REGULAR_VERBS

    def conjugate(
        self,
        verb: str,
        tense: str = "present_subjunctive",
        person: str = "yo"
    ) -> ConjugationResult:
        """
        Conjugate a verb in the subjunctive mood.

        Args:
            verb: Infinitive form of verb (e.g., "hablar", "ser")
            tense: Subjunctive tense (present_subjunctive, imperfect_subjunctive_ra, etc.)
            person: Grammatical person (yo, tú, él/ella/usted, etc.)

        Returns:
            ConjugationResult object with conjugation and metadata

        Raises:
            ValueError: If verb, tense, or person is invalid
        """
        # Validate inputs
        if not verb:
            raise ValueError("Verb cannot be empty")

        verb = verb.lower().strip()
        verb_type = get_verb_type(verb)

        if not verb_type:
            raise ValueError(f"Invalid verb: {verb}. Must end in -ar, -er, or -ir")

        if tense not in ["present_subjunctive", "imperfect_subjunctive_ra", "imperfect_subjunctive_se"]:
            raise ValueError(f"Invalid tense: {tense}")

        # Check if irregular verb (takes precedence)
        # Irregular verbs are taught as irregular, not stem-changing
        # But only if this specific tense has an irregular conjugation
        if verb in self.irregular_verbs and tense in self.irregular_verbs[verb]:
            return self._conjugate_irregular(verb, tense, person)

        # Check if stem-changing verb
        is_stem, pattern, info = is_stem_changing(verb)
        if is_stem:
            return self._conjugate_stem_changing(verb, tense, person, pattern, info)

        # Regular conjugation
        return self._conjugate_regular(verb, tense, person, verb_type)

    def _conjugate_irregular(
        self,
        verb: str,
        tense: str,
        person: str
    ) -> ConjugationResult:
        """Conjugate an irregular verb"""
        try:
            conjugation = self.irregular_verbs[verb][tense][person]
            return ConjugationResult(
                verb=verb,
                tense=tense,
                person=person,
                conjugation=conjugation,
                is_irregular=True
            )
        except KeyError:
            raise ValueError(
                f"No conjugation found for irregular verb '{verb}' "
                f"in tense '{tense}' and person '{person}'"
            )

    def _conjugate_stem_changing(
        self,
        verb: str,
        tense: str,
        person: str,
        pattern: str,
        info: Dict
    ) -> ConjugationResult:
        """Conjugate a stem-changing verb"""
        verb_type = info["type"]
        changed_stem = info["stem"]

        # Stem changes typically don't apply in nosotros/vosotros or imperfect
        # Exception: -ir verbs with e→i or o→u change in all forms
        use_stem_change = True

        if tense in ["imperfect_subjunctive_ra", "imperfect_subjunctive_se"]:
            # In imperfect subjunctive, most stem changes don't apply
            # Exception: dormir/morir have o→u change
            if verb in ["dormir", "morir"]:
                # Special handling for dormir/morir in imperfect
                if verb == "dormir":
                    changed_stem = "durm" if person not in ["nosotros/nosotras", "vosotros/vosotras"] else "durm"
                elif verb == "morir":
                    changed_stem = "murm" if person not in ["nosotros/nosotras", "vosotros/vosotras"] else "murm"
            else:
                use_stem_change = False

        # In present subjunctive, nosotros/vosotros don't change for -ar/-er verbs
        # but -ir verbs with e→i still change
        if tense == "present_subjunctive":
            if person in ["nosotros/nosotras", "vosotros/vosotras"]:
                if verb_type in ["-ar", "-er"]:
                    use_stem_change = False
                elif verb_type == "-ir" and pattern == "e→i":
                    # Keep the stem change for e→i -ir verbs
                    use_stem_change = True

        # Get the ending
        try:
            ending = self.regular_endings[tense][verb_type][person]
        except KeyError:
            raise ValueError(f"No ending found for {verb_type} verb in {tense}, person {person}")

        # Build conjugation
        if use_stem_change:
            conjugation = changed_stem + ending
        else:
            regular_stem = get_verb_stem(verb)
            conjugation = regular_stem + ending

        # Apply spelling changes if needed (for both stem-changing and regular)
        has_spelling_change = False
        spelling_rule = None

        original_conjugation = conjugation
        if use_stem_change:
            # For stem-changing verbs, apply spelling changes to the changed stem
            conjugation = apply_spelling_changes(verb, changed_stem, ending)
        else:
            # For regular conjugation, apply spelling changes to the regular stem
            conjugation = apply_spelling_changes(verb, get_verb_stem(verb), ending)

        if conjugation != original_conjugation:
            has_spelling_change = True
            spelling_rule = self._identify_spelling_change(verb, conjugation)

        return ConjugationResult(
            verb=verb,
            tense=tense,
            person=person,
            conjugation=conjugation,
            is_stem_changing=use_stem_change,
            stem_change_pattern=pattern if use_stem_change else None,
            has_spelling_change=has_spelling_change,
            spelling_change_rule=spelling_rule
        )

    def _conjugate_regular(
        self,
        verb: str,
        tense: str,
        person: str,
        verb_type: str
    ) -> ConjugationResult:
        """Conjugate a regular verb"""
        stem = get_verb_stem(verb)

        try:
            ending = self.regular_endings[tense][verb_type][person]
        except KeyError:
            raise ValueError(f"No ending found for {verb_type} verb in {tense}, person {person}")

        # Apply spelling changes
        original_conjugation = stem + ending
        conjugation = apply_spelling_changes(verb, stem, ending)

        has_spelling_change = conjugation != original_conjugation
        spelling_rule = None

        if has_spelling_change:
            spelling_rule = self._identify_spelling_change(verb, conjugation)

        return ConjugationResult(
            verb=verb,
            tense=tense,
            person=person,
            conjugation=conjugation,
            has_spelling_change=has_spelling_change,
            spelling_change_rule=spelling_rule
        )

    def _identify_spelling_change(self, verb: str, conjugation: str) -> Optional[str]:
        """Identify which spelling change rule was applied"""
        for change_type, change_info in self.spelling_changes.items():
            if verb in change_info.get("examples", []):
                return change_info.get("rule")
        return None

    def get_full_conjugation_table(
        self,
        verb: str,
        tense: str = "present_subjunctive"
    ) -> Dict[str, ConjugationResult]:
        """
        Get complete conjugation table for a verb in a given tense.

        Args:
            verb: Infinitive form
            tense: Subjunctive tense

        Returns:
            Dictionary mapping persons to ConjugationResult objects
        """
        persons = [
            "yo",
            "tú",
            "él/ella/usted",
            "nosotros/nosotras",
            "vosotros/vosotras",
            "ellos/ellas/ustedes"
        ]

        table = {}
        for person in persons:
            try:
                table[person] = self.conjugate(verb, tense, person)
            except Exception as e:
                self.logger.error(f"Error conjugating {verb} for {person}: {e}")
                table[person] = None

        return table

    def validate_answer(
        self,
        verb: str,
        tense: str,
        person: str,
        user_answer: str
    ) -> ValidationResult:
        """
        Validate a user's conjugation answer.

        Args:
            verb: Infinitive form
            tense: Subjunctive tense
            person: Grammatical person
            user_answer: User's conjugation attempt

        Returns:
            ValidationResult with correctness and error analysis
        """
        # Get correct answer
        try:
            correct_result = self.conjugate(verb, tense, person)
            correct_answer = correct_result.conjugation
        except Exception as e:
            self.logger.error(f"Error getting correct answer: {e}")
            return ValidationResult(
                is_correct=False,
                user_answer=user_answer,
                correct_answer="ERROR",
                verb=verb,
                tense=tense,
                person=person,
                error_type="validation_error",
                suggestions=["Unable to validate answer"]
            )

        # Normalize answers
        user_normalized = user_answer.lower().strip()
        correct_normalized = correct_answer.lower().strip()

        # Check if correct
        is_correct = user_normalized == correct_normalized

        # Analyze error if incorrect
        error_type = None
        suggestions = []

        if not is_correct:
            error_type, suggestions = self._analyze_error(
                user_normalized,
                correct_normalized,
                verb,
                tense,
                person,
                correct_result
            )

        return ValidationResult(
            is_correct=is_correct,
            user_answer=user_answer,
            correct_answer=correct_answer,
            verb=verb,
            tense=tense,
            person=person,
            error_type=error_type,
            suggestions=suggestions
        )

    def _analyze_error(
        self,
        user_answer: str,
        correct_answer: str,
        verb: str,
        tense: str,
        person: str,
        correct_result: ConjugationResult
    ) -> Tuple[str, List[str]]:
        """
        Analyze what type of error the user made.

        Returns:
            Tuple of (error_type, suggestions)
        """
        suggestions = []
        error_type = "unknown_error"

        # Check if user used indicative instead of subjunctive
        indicative_forms = self._get_indicative_forms(verb, person)
        if user_answer in indicative_forms:
            error_type = "mood_confusion"
            suggestions.append(f"You used the indicative mood. The subjunctive form is '{correct_answer}'.")
            return error_type, suggestions

        # Check if wrong person
        all_persons = self.get_full_conjugation_table(verb, tense)
        for p, result in all_persons.items():
            if result and result.conjugation.lower() == user_answer:
                error_type = "wrong_person"
                suggestions.append(f"'{user_answer}' is the form for '{p}', not '{person}'.")
                return error_type, suggestions

        # Check if wrong tense
        for t in ["present_subjunctive", "imperfect_subjunctive_ra", "imperfect_subjunctive_se"]:
            if t != tense:
                try:
                    other_result = self.conjugate(verb, t, person)
                    if other_result.conjugation.lower() == user_answer:
                        error_type = "wrong_tense"
                        tense_name = t.replace("_", " ").title()
                        suggestions.append(f"'{user_answer}' is the {tense_name} form, not {tense.replace('_', ' ').title()}.")
                        return error_type, suggestions
                except:
                    pass

        # Check for spelling errors
        if self._is_close_match(user_answer, correct_answer):
            error_type = "spelling_error"
            suggestions.append(f"Close! Check your spelling. The correct form is '{correct_answer}'.")

            if correct_result.has_spelling_change:
                suggestions.append(f"Remember the spelling rule: {correct_result.spelling_change_rule}")

            return error_type, suggestions

        # Check for stem change errors
        if correct_result.is_stem_changing:
            error_type = "stem_change_error"
            suggestions.append(
                f"This verb has a stem change: {correct_result.stem_change_pattern}. "
                f"The correct form is '{correct_answer}'."
            )
            return error_type, suggestions

        # Check for ending errors
        if correct_result.has_spelling_change:
            error_type = "spelling_change_error"
            suggestions.append(f"Remember: {correct_result.spelling_change_rule}")
            suggestions.append(f"The correct form is '{correct_answer}'.")
            return error_type, suggestions

        # Generic wrong ending
        verb_type = get_verb_type(verb)
        error_type = "wrong_ending"
        suggestions.append(f"Check the subjunctive endings for {verb_type} verbs.")
        suggestions.append(f"The correct form is '{correct_answer}'.")

        return error_type, suggestions

    def _get_indicative_forms(self, verb: str, person: str) -> List[str]:
        """Get common indicative forms to check for mood confusion"""
        # This is a simplified version - in production would have full indicative conjugations
        stem = get_verb_stem(verb)
        verb_type = get_verb_type(verb)

        indicative_forms = []

        # Present indicative endings
        present_endings = {
            "-ar": {"yo": "o", "tú": "as", "él/ella/usted": "a"},
            "-er": {"yo": "o", "tú": "es", "él/ella/usted": "e"},
            "-ir": {"yo": "o", "tú": "es", "él/ella/usted": "e"}
        }

        if verb_type in present_endings and person in present_endings[verb_type]:
            indicative_forms.append(stem + present_endings[verb_type][person])

        return indicative_forms

    def _is_close_match(self, answer1: str, answer2: str) -> bool:
        """Check if two answers are close (for spelling error detection)"""
        # Simple Levenshtein-style check
        if len(answer1) != len(answer2):
            return abs(len(answer1) - len(answer2)) <= 2

        differences = sum(1 for a, b in zip(answer1, answer2) if a != b)
        return differences <= 2

    def get_supported_verbs(self) -> Dict[str, List[str]]:
        """
        Get all supported verbs categorized by type.

        Returns:
            Dictionary with categories and verb lists
        """
        return {
            "irregular": list(self.irregular_verbs.keys()),
            "stem_changing_e_ie": list(self.stem_changing["e→ie"].keys()),
            "stem_changing_o_ue": list(self.stem_changing["o→ue"].keys()),
            "stem_changing_e_i": list(self.stem_changing["e→i"].keys()),
            "regular_ar": self.common_verbs["-ar"],
            "regular_er": self.common_verbs["-er"],
            "regular_ir": self.common_verbs["-ir"]
        }

    def get_verb_info(self, verb: str) -> Dict:
        """
        Get detailed information about a verb.

        Args:
            verb: Infinitive form

        Returns:
            Dictionary with verb classification and patterns
        """
        verb = verb.lower().strip()
        verb_type = get_verb_type(verb)

        info = {
            "verb": verb,
            "type": verb_type,
            "is_irregular": verb in self.irregular_verbs,
            "is_stem_changing": False,
            "stem_change_pattern": None,
            "has_spelling_changes": False,
            "spelling_change_rules": []
        }

        # Check stem changing
        is_stem, pattern, stem_info = is_stem_changing(verb)
        if is_stem:
            info["is_stem_changing"] = True
            info["stem_change_pattern"] = pattern

        # Check spelling changes
        for change_type, change_info in self.spelling_changes.items():
            if verb in change_info.get("examples", []):
                info["has_spelling_changes"] = True
                info["spelling_change_rules"].append({
                    "type": change_type,
                    "rule": change_info["rule"]
                })

        return info


# Example usage
if __name__ == "__main__":
    engine = ConjugationEngine()

    # Test regular verb
    result = engine.conjugate("hablar", "present_subjunctive", "yo")
    print(f"hablar (yo): {result.conjugation}")

    # Test irregular verb
    result = engine.conjugate("ser", "present_subjunctive", "yo")
    print(f"ser (yo): {result.conjugation}")

    # Test stem-changing verb
    result = engine.conjugate("querer", "present_subjunctive", "yo")
    print(f"querer (yo): {result.conjugation}")

    # Test spelling change verb
    result = engine.conjugate("buscar", "present_subjunctive", "yo")
    print(f"buscar (yo): {result.conjugation}")

    # Validate answer
    validation = engine.validate_answer("hablar", "present_subjunctive", "yo", "hable")
    print(f"Validation: {validation.is_correct}")

    # Get full table
    table = engine.get_full_conjugation_table("ser", "present_subjunctive")
    print("\nConjugation table for 'ser':")
    for person, result in table.items():
        if result:
            print(f"  {person}: {result.conjugation}")

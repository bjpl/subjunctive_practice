"""
Intelligent Feedback and Error Analysis System

This module provides detailed, contextualized feedback for learner errors
with categorization, pattern detection, and personalized suggestions.
"""

from typing import Dict, List, Optional, Tuple
from collections import Counter, defaultdict
from dataclasses import dataclass
import logging

from backend.services.conjugation import ConjugationEngine, ValidationResult
from backend.utils.spanish_grammar import WEIRDO_TRIGGERS


logger = logging.getLogger(__name__)


@dataclass
class ErrorPattern:
    """Represents a detected error pattern"""
    error_type: str
    frequency: int
    verbs_affected: List[str]
    persons_affected: List[str]
    suggestion: str
    priority: str  # high, medium, low


@dataclass
class Feedback:
    """Comprehensive feedback for an exercise"""
    is_correct: bool
    message: str
    explanation: str
    error_category: Optional[str]
    suggestions: List[str]
    related_rules: List[str]
    encouragement: str
    next_steps: List[str]

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "is_correct": self.is_correct,
            "message": self.message,
            "explanation": self.explanation,
            "error_category": self.error_category,
            "suggestions": self.suggestions,
            "related_rules": self.related_rules,
            "encouragement": self.encouragement,
            "next_steps": self.next_steps
        }


class ErrorAnalyzer:
    """
    Analyzes learner errors and detects patterns.

    Error categories:
    - Mood confusion (indicative vs subjunctive)
    - Wrong person conjugation
    - Wrong tense
    - Stem change errors
    - Spelling change errors
    - Ending errors
    """

    def __init__(self):
        """Initialize error analyzer"""
        self.logger = logging.getLogger(__name__)
        self.error_history: List[Dict] = []
        self.error_counts: Counter = Counter()

    def analyze_error(
        self,
        validation_result: ValidationResult,
        exercise_context: Optional[Dict] = None
    ) -> Dict:
        """
        Analyze a specific error in detail.

        Args:
            validation_result: ValidationResult from conjugation engine
            exercise_context: Optional context (trigger, category, etc.)

        Returns:
            Detailed error analysis
        """
        if validation_result.is_correct:
            return {
                "error_type": None,
                "severity": "none",
                "explanation": "Correct!",
                "suggestions": []
            }

        error_type = validation_result.error_type or "unknown"

        # Record error
        error_record = {
            "error_type": error_type,
            "verb": validation_result.verb,
            "tense": validation_result.tense,
            "person": validation_result.person,
            "user_answer": validation_result.user_answer,
            "correct_answer": validation_result.correct_answer
        }
        self.error_history.append(error_record)
        self.error_counts[error_type] += 1

        # Determine severity
        severity = self._determine_severity(error_type)

        # Get detailed explanation
        explanation = self._get_error_explanation(
            error_type,
            validation_result,
            exercise_context
        )

        # Get targeted suggestions
        suggestions = self._get_targeted_suggestions(
            error_type,
            validation_result,
            exercise_context
        )

        return {
            "error_type": error_type,
            "severity": severity,
            "explanation": explanation,
            "suggestions": suggestions,
            "frequency": self.error_counts[error_type]
        }

    def _determine_severity(self, error_type: str) -> str:
        """Determine error severity"""
        high_severity = ["mood_confusion", "stem_change_error"]
        medium_severity = ["wrong_person", "wrong_tense", "spelling_change_error"]

        if error_type in high_severity:
            return "high"
        elif error_type in medium_severity:
            return "medium"
        else:
            return "low"

    def _get_error_explanation(
        self,
        error_type: str,
        validation_result: ValidationResult,
        context: Optional[Dict]
    ) -> str:
        """Get detailed explanation for error type"""
        explanations = {
            "mood_confusion": (
                f"You used the indicative mood, but this sentence requires the subjunctive. "
                f"The trigger phrase '{context.get('trigger_phrase', 'in this sentence')}' "
                f"signals uncertainty, emotion, or desire, which requires subjunctive."
            ),
            "wrong_person": (
                f"Your conjugation '{validation_result.user_answer}' is correct, but for a different "
                f"grammatical person. This sentence requires the form for '{validation_result.person}'."
            ),
            "wrong_tense": (
                f"Your answer uses a different subjunctive tense. "
                f"This exercise requires the {validation_result.tense.replace('_', ' ')}."
            ),
            "stem_change_error": (
                f"The verb '{validation_result.verb}' undergoes a stem change in the subjunctive. "
                f"Remember to apply the stem change pattern before adding the ending."
            ),
            "spelling_change_error": (
                f"The verb '{validation_result.verb}' requires an orthographic spelling change "
                f"to maintain pronunciation. Check the spelling rules for this verb type."
            ),
            "wrong_ending": (
                f"The ending is incorrect. Review the subjunctive endings for this verb type."
            ),
            "spelling_error": (
                f"You're very close! There's a small spelling error. "
                f"The correct form is '{validation_result.correct_answer}'."
            )
        }

        return explanations.get(
            error_type,
            f"The correct form is '{validation_result.correct_answer}'."
        )

    def _get_targeted_suggestions(
        self,
        error_type: str,
        validation_result: ValidationResult,
        context: Optional[Dict]
    ) -> List[str]:
        """Get specific suggestions based on error type"""
        suggestions = []

        if error_type == "mood_confusion":
            suggestions.extend([
                "Review WEIRDO triggers that require subjunctive",
                f"Practice recognizing '{context.get('trigger_category', 'trigger')}' patterns",
                "Remember: subjunctive expresses doubt, emotion, or influence over others"
            ])

        elif error_type == "stem_change_error":
            suggestions.extend([
                f"Study the stem-changing pattern for '{validation_result.verb}'",
                "Practice other verbs with the same stem change",
                "Note which persons undergo the stem change"
            ])

        elif error_type == "spelling_change_error":
            suggestions.extend([
                "Review orthographic spelling rules",
                "Remember: spelling changes maintain pronunciation",
                "Practice similar verbs with the same spelling change"
            ])

        elif error_type == "wrong_person":
            suggestions.extend([
                "Pay attention to the subject of the sentence",
                "Review all persons for this verb",
                "Practice person identification in context"
            ])

        elif error_type == "wrong_tense":
            suggestions.extend([
                "Review the difference between present and imperfect subjunctive",
                "Pay attention to the tense of the main clause",
                "Practice tense sequence rules"
            ])

        return suggestions

    def detect_patterns(self, min_frequency: int = 3) -> List[ErrorPattern]:
        """
        Detect recurring error patterns.

        Args:
            min_frequency: Minimum occurrences to consider a pattern

        Returns:
            List of ErrorPattern objects
        """
        if not self.error_history:
            return []

        patterns = []

        # Group errors by type
        errors_by_type = defaultdict(list)
        for error in self.error_history:
            errors_by_type[error["error_type"]].append(error)

        # Analyze each error type
        for error_type, errors in errors_by_type.items():
            if len(errors) >= min_frequency:
                # Get affected verbs and persons
                verbs = [e["verb"] for e in errors]
                persons = [e["person"] for e in errors]

                # Determine priority
                priority = "high" if len(errors) >= 5 else "medium"

                pattern = ErrorPattern(
                    error_type=error_type,
                    frequency=len(errors),
                    verbs_affected=list(set(verbs)),
                    persons_affected=list(set(persons)),
                    suggestion=self._get_pattern_suggestion(error_type, verbs, persons),
                    priority=priority
                )
                patterns.append(pattern)

        # Sort by frequency (descending)
        patterns.sort(key=lambda p: p.frequency, reverse=True)

        return patterns

    def _get_pattern_suggestion(
        self,
        error_type: str,
        verbs: List[str],
        persons: List[str]
    ) -> str:
        """Generate suggestion for detected pattern"""
        most_common_verb = Counter(verbs).most_common(1)[0][0] if verbs else "verbs"
        most_common_person = Counter(persons).most_common(1)[0][0] if persons else "persons"

        suggestions = {
            "mood_confusion": (
                "You frequently confuse indicative and subjunctive moods. "
                "Dedicate time to studying WEIRDO triggers."
            ),
            "stem_change_error": (
                f"You're having trouble with stem-changing verbs, especially '{most_common_verb}'. "
                "Review stem change patterns and practice regularly."
            ),
            "spelling_change_error": (
                "You often miss orthographic spelling changes. "
                "Create flashcards for spelling change rules."
            ),
            "wrong_person": (
                f"You frequently mix up conjugations, especially for '{most_common_person}'. "
                "Practice identifying the subject before conjugating."
            )
        }

        return suggestions.get(
            error_type,
            f"Review {error_type.replace('_', ' ')} systematically."
        )

    def get_error_summary(self) -> Dict:
        """Get summary of all errors"""
        if not self.error_history:
            return {
                "total_errors": 0,
                "error_types": {},
                "most_common_error": None,
                "patterns_detected": 0
            }

        patterns = self.detect_patterns(min_frequency=2)

        return {
            "total_errors": len(self.error_history),
            "error_types": dict(self.error_counts),
            "most_common_error": self.error_counts.most_common(1)[0][0] if self.error_counts else None,
            "patterns_detected": len(patterns),
            "patterns": [
                {
                    "type": p.error_type,
                    "frequency": p.frequency,
                    "priority": p.priority,
                    "suggestion": p.suggestion
                }
                for p in patterns
            ]
        }


class FeedbackGenerator:
    """
    Generates comprehensive, encouraging feedback for learners.

    Features:
    - Positive reinforcement
    - Detailed explanations
    - Personalized suggestions
    - Progress acknowledgment
    - Next steps guidance
    """

    def __init__(
        self,
        conjugation_engine: Optional[ConjugationEngine] = None,
        error_analyzer: Optional[ErrorAnalyzer] = None
    ):
        """Initialize feedback generator"""
        self.logger = logging.getLogger(__name__)
        self.engine = conjugation_engine or ConjugationEngine()
        self.error_analyzer = error_analyzer or ErrorAnalyzer()

    def generate_feedback(
        self,
        validation_result: ValidationResult,
        exercise_context: Optional[Dict] = None,
        user_level: str = "intermediate"
    ) -> Feedback:
        """
        Generate comprehensive feedback for an exercise attempt.

        Args:
            validation_result: Validation result from conjugation engine
            exercise_context: Optional context (trigger, category, etc.)
            user_level: User's proficiency level

        Returns:
            Feedback object with detailed information
        """
        if validation_result.is_correct:
            return self._generate_positive_feedback(
                validation_result,
                exercise_context,
                user_level
            )
        else:
            return self._generate_corrective_feedback(
                validation_result,
                exercise_context,
                user_level
            )

    def _generate_positive_feedback(
        self,
        validation_result: ValidationResult,
        context: Optional[Dict],
        level: str
    ) -> Feedback:
        """Generate positive feedback for correct answer"""
        messages = [
            "Excellent work!",
            "Perfect!",
            "Great job!",
            "Well done!",
            "Fantastic!",
            "You got it!",
            "Correct!"
        ]

        message = messages[hash(validation_result.correct_answer) % len(messages)]

        # Explanation based on verb complexity
        verb_info = self.engine.get_verb_info(validation_result.verb)

        if verb_info["is_irregular"]:
            explanation = (
                f"You correctly conjugated the irregular verb '{validation_result.verb}'. "
                "Irregular verbs can be challenging, so this shows good mastery!"
            )
        elif verb_info["is_stem_changing"]:
            explanation = (
                f"You correctly applied the stem change for '{validation_result.verb}'. "
                f"The pattern {verb_info['stem_change_pattern']} is now becoming automatic for you!"
            )
        elif verb_info["has_spelling_changes"]:
            explanation = (
                f"You correctly applied the spelling change for '{validation_result.verb}'. "
                "Orthographic rules are tricky, so great attention to detail!"
            )
        else:
            explanation = (
                f"You correctly conjugated '{validation_result.verb}' in the subjunctive. "
                "Your understanding of regular patterns is solid!"
            )

        # Add trigger context if available
        if context and "trigger_phrase" in context:
            explanation += (
                f"\n\nYou also correctly recognized that '{context['trigger_phrase']}' "
                f"requires the subjunctive mood."
            )

        encouragement = self._get_encouragement("correct", level)

        next_steps = [
            "Continue practicing to reinforce this pattern",
            "Try more complex verbs to challenge yourself",
            "Review similar constructions to build confidence"
        ]

        return Feedback(
            is_correct=True,
            message=message,
            explanation=explanation,
            error_category=None,
            suggestions=[],
            related_rules=self._get_related_rules(validation_result, context),
            encouragement=encouragement,
            next_steps=next_steps
        )

    def _generate_corrective_feedback(
        self,
        validation_result: ValidationResult,
        context: Optional[Dict],
        level: str
    ) -> Feedback:
        """Generate corrective feedback for incorrect answer"""
        # Analyze error
        error_analysis = self.error_analyzer.analyze_error(validation_result, context)

        message = f"Not quite. The correct answer is '{validation_result.correct_answer}'."

        explanation = error_analysis["explanation"]

        suggestions = error_analysis["suggestions"]
        if validation_result.suggestions:
            suggestions.extend(validation_result.suggestions)

        encouragement = self._get_encouragement("incorrect", level)

        next_steps = self._get_next_steps(
            error_analysis["error_type"],
            validation_result.verb,
            level
        )

        related_rules = self._get_related_rules(validation_result, context)

        return Feedback(
            is_correct=False,
            message=message,
            explanation=explanation,
            error_category=error_analysis["error_type"],
            suggestions=list(set(suggestions)),  # Remove duplicates
            related_rules=related_rules,
            encouragement=encouragement,
            next_steps=next_steps
        )

    def _get_encouragement(self, result: str, level: str) -> str:
        """Get encouraging message"""
        if result == "correct":
            messages = [
                "Keep up the excellent work!",
                "You're making great progress!",
                "Your hard work is paying off!",
                "You're mastering the subjunctive!",
                "Fantastic progress!"
            ]
        else:
            messages = [
                "Don't worry, mistakes are part of learning!",
                "This is a tricky pattern - you'll get it with practice!",
                "Every error is a learning opportunity!",
                "Stay positive - you're improving!",
                "Keep practicing - you're on the right track!"
            ]

        return messages[hash(level) % len(messages)]

    def _get_next_steps(
        self,
        error_type: str,
        verb: str,
        level: str
    ) -> List[str]:
        """Get recommended next steps"""
        steps = []

        if error_type == "mood_confusion":
            steps.extend([
                "Review WEIRDO trigger phrases",
                "Practice identifying subjunctive triggers in sentences",
                "Do 5 more exercises focusing on mood recognition"
            ])
        elif error_type == "stem_change_error":
            steps.extend([
                f"Review stem change patterns",
                f"Practice conjugating other verbs with the same pattern",
                "Create flashcards for stem-changing verbs"
            ])
        elif error_type == "spelling_change_error":
            steps.extend([
                "Review orthographic spelling rules",
                "Practice verbs with similar spelling changes",
                "Write out full conjugation tables"
            ])
        else:
            steps.extend([
                f"Review conjugation of '{verb}'",
                "Practice similar verb patterns",
                "Do more exercises at your current level"
            ])

        return steps

    def _get_related_rules(
        self,
        validation_result: ValidationResult,
        context: Optional[Dict]
    ) -> List[str]:
        """Get related grammar rules"""
        rules = []

        # Add WEIRDO rule if context available
        if context and "trigger_category" in context:
            category = context["trigger_category"]
            if category in WEIRDO_TRIGGERS:
                rules.append(
                    f"{category}: {WEIRDO_TRIGGERS[category]['triggers'][0]}"
                )

        # Add verb-specific rules
        verb_info = self.engine.get_verb_info(validation_result.verb)

        if verb_info["is_irregular"]:
            rules.append(f"'{validation_result.verb}' is an irregular verb")

        if verb_info["is_stem_changing"]:
            rules.append(
                f"Stem change: {verb_info['stem_change_pattern']}"
            )

        if verb_info["has_spelling_changes"]:
            for rule in verb_info["spelling_change_rules"]:
                rules.append(rule["rule"])

        return rules


# Example usage
if __name__ == "__main__":
    from backend.services.conjugation import ConjugationEngine

    engine = ConjugationEngine()
    analyzer = ErrorAnalyzer()
    feedback_gen = FeedbackGenerator(engine, analyzer)

    # Test with correct answer
    validation = engine.validate_answer("hablar", "present_subjunctive", "yo", "hable")
    feedback = feedback_gen.generate_feedback(
        validation,
        {"trigger_phrase": "quiero que", "trigger_category": "Wishes"}
    )
    print("Correct answer feedback:")
    print(f"Message: {feedback.message}")
    print(f"Explanation: {feedback.explanation}\n")

    # Test with incorrect answer
    validation = engine.validate_answer("ser", "present_subjunctive", "yo", "soy")
    feedback = feedback_gen.generate_feedback(
        validation,
        {"trigger_phrase": "es importante que", "trigger_category": "Impersonal_Expressions"}
    )
    print("Incorrect answer feedback:")
    print(f"Message: {feedback.message}")
    print(f"Explanation: {feedback.explanation}")
    print(f"Suggestions: {feedback.suggestions}")

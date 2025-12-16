"""
Exercise Generator with WEIRDO Triggers

This module generates contextual Spanish subjunctive exercises using
WEIRDO methodology (Wishes, Emotions, Impersonal expressions,
Recommendations, Doubt/Denial, Ojalá).
"""

from typing import Dict, List, Optional, Tuple
import random
import logging

from services.conjugation import ConjugationEngine
from utils.spanish_grammar import (
    WEIRDO_TRIGGERS,
    IRREGULAR_VERBS,
    STEM_CHANGING_VERBS,
    COMMON_REGULAR_VERBS
)


logger = logging.getLogger(__name__)


class Exercise:
    """Represents a single exercise"""

    def __init__(
        self,
        exercise_id: str,
        exercise_type: str,
        verb: str,
        tense: str,
        person: str,
        trigger_phrase: str,
        trigger_category: str,
        sentence_template: str,
        blank_position: int,
        correct_answer: str,
        difficulty: str,
        context: Optional[str] = None,
        hints: Optional[List[str]] = None,
        distractors: Optional[List[str]] = None
    ):
        self.exercise_id = exercise_id
        self.exercise_type = exercise_type
        self.verb = verb
        self.tense = tense
        self.person = person
        self.trigger_phrase = trigger_phrase
        self.trigger_category = trigger_category
        self.sentence_template = sentence_template
        self.blank_position = blank_position
        self.correct_answer = correct_answer
        self.difficulty = difficulty
        self.context = context
        self.hints = hints or []
        self.distractors = distractors or []

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "exercise_id": self.exercise_id,
            "exercise_type": self.exercise_type,
            "verb": self.verb,
            "tense": self.tense,
            "person": self.person,
            "trigger_phrase": self.trigger_phrase,
            "trigger_category": self.trigger_category,
            "sentence_template": self.sentence_template,
            "blank_position": self.blank_position,
            "correct_answer": self.correct_answer,
            "difficulty": self.difficulty,
            "context": self.context,
            "hints": self.hints,
            "distractors": self.distractors
        }

    def get_display_sentence(self) -> str:
        """Get sentence with blank for display"""
        return self.sentence_template.replace("____", "_______")


class ExerciseGenerator:
    """
    Generates contextual Spanish subjunctive exercises using WEIRDO triggers.

    Features:
    - WEIRDO-based trigger selection
    - Contextual sentence generation
    - Multiple exercise types (fill-in-blank, multiple choice, translation)
    - Difficulty-based verb selection
    - Distractor generation
    """

    def __init__(self, conjugation_engine: Optional[ConjugationEngine] = None):
        """Initialize the exercise generator"""
        self.logger = logging.getLogger(__name__)
        self.engine = conjugation_engine or ConjugationEngine()
        self._load_sentence_templates()
        self._exercise_counter = 0

    def _load_sentence_templates(self):
        """Load sentence templates for each WEIRDO category"""
        self.templates = {
            "Wishes": [
                ("Quiero que tú ____ a la fiesta conmigo.", "tú"),
                ("Espero que él ____ pronto.", "él/ella/usted"),
                ("Deseo que nosotros ____ éxito.", "nosotros/nosotras"),
                ("Prefiero que ustedes ____ temprano.", "ellos/ellas/ustedes"),
                ("Ojalá que yo ____ la lotería.", "yo"),
                ("Necesito que tú me ____ con esto.", "tú"),
                ("Queremos que ellos ____ felices.", "ellos/ellas/ustedes")
            ],
            "Emotions": [
                ("Me alegro de que tú ____ aquí.", "tú"),
                ("Siento que ella no ____ venir.", "él/ella/usted"),
                ("Temo que nosotros ____ tarde.", "nosotros/nosotras"),
                ("Me sorprende que ellos ____ español.", "ellos/ellas/ustedes"),
                ("Me molesta que yo ____ esperar.", "yo"),
                ("Estoy contento de que tú ____ bien.", "tú"),
                ("Me gusta que ustedes ____.", "ellos/ellas/ustedes")
            ],
            "Impersonal_Expressions": [
                ("Es importante que yo ____ todos los días.", "yo"),
                ("Es necesario que tú ____ la verdad.", "tú"),
                ("Es posible que ella ____ mañana.", "él/ella/usted"),
                ("Es probable que nosotros ____ tarde.", "nosotros/nosotras"),
                ("Es mejor que ustedes ____ ahora.", "ellos/ellas/ustedes"),
                ("Es raro que él ____ eso.", "él/ella/usted"),
                ("Es una lástima que yo no ____.", "yo")
            ],
            "Recommendations": [
                ("Recomiendo que tú ____ al médico.", "tú"),
                ("Te sugiero que ____ con él.", "tú"),
                ("Aconsejo que usted ____ cuidado.", "él/ella/usted"),
                ("Propongo que nosotros ____ un viaje.", "nosotros/nosotras"),
                ("Pido que ustedes ____ silencio.", "ellos/ellas/ustedes"),
                ("Exijo que tú me ____ la verdad.", "tú"),
                ("Insisto en que él ____.", "él/ella/usted")
            ],
            "Doubt_Denial": [
                ("Dudo que yo ____ hacerlo.", "yo"),
                ("No creo que tú ____ razón.", "tú"),
                ("No pienso que ella ____ hoy.", "él/ella/usted"),
                ("No estoy seguro de que nosotros ____.", "nosotros/nosotras"),
                ("Niego que ellos ____ eso.", "ellos/ellas/ustedes"),
                ("No es verdad que yo ____.", "yo"),
                ("No es cierto que tú ____.", "tú")
            ],
            "Ojalá": [
                ("Ojalá que yo ____ suerte.", "yo"),
                ("Ojalá que tú ____ bien.", "tú"),
                ("Ojalá que él ____ pronto.", "él/ella/usted"),
                ("Ojalá que nosotros ____ tiempo.", "nosotros/nosotras"),
                ("Ojalá que ustedes ____ éxito.", "ellos/ellas/ustedes"),
                ("Ojalá no ____ hoy.", "él/ella/usted"),
                ("Ojalá ____ venir.", "yo")
            ]
        }

        # Context sentences for better immersion
        self.contexts = {
            "social": [
                "En una conversación entre amigos...",
                "Durante una cena familiar...",
                "En una reunión de trabajo...",
                "Hablando con un compañero de clase..."
            ],
            "planning": [
                "Planificando las vacaciones...",
                "Organizando una fiesta...",
                "Discutiendo el fin de semana...",
                "Preparando un viaje..."
            ],
            "advice": [
                "Dando consejos a un amigo...",
                "Un médico habla con su paciente...",
                "Un profesor aconseja a su estudiante...",
                "Un padre habla con su hijo..."
            ],
            "emotions": [
                "Expresando sentimientos...",
                "Reaccionando a una noticia...",
                "Compartiendo preocupaciones...",
                "Celebrando un logro..."
            ]
        }

    def generate_exercise(
        self,
        difficulty: str = "intermediate",
        exercise_type: str = "fill_in_blank",
        weirdo_category: Optional[str] = None,
        specific_verb: Optional[str] = None,
        tense: str = "present_subjunctive"
    ) -> Exercise:
        """
        Generate a subjunctive exercise.

        Args:
            difficulty: beginner, intermediate, or advanced
            exercise_type: fill_in_blank, multiple_choice, or translation
            weirdo_category: Specific WEIRDO category (or random if None)
            specific_verb: Specific verb to practice (or random if None)
            tense: Subjunctive tense to practice

        Returns:
            Exercise object
        """
        # Select WEIRDO category
        if weirdo_category and weirdo_category in WEIRDO_TRIGGERS:
            category = weirdo_category
        else:
            category = random.choice(list(WEIRDO_TRIGGERS.keys()))

        # Select trigger phrase
        trigger_info = WEIRDO_TRIGGERS[category]
        trigger_phrase = random.choice(trigger_info["triggers"])

        # Select verb based on difficulty
        verb = specific_verb or self._select_verb_by_difficulty(difficulty)

        # Select sentence template
        template, person = random.choice(self.templates[category])

        # Get correct conjugation
        try:
            result = self.engine.conjugate(verb, tense, person)
            correct_answer = result.conjugation
        except Exception as e:
            self.logger.error(f"Error conjugating {verb}: {e}")
            # Fall back to a simple verb
            verb = "hablar"
            result = self.engine.conjugate(verb, tense, person)
            correct_answer = result.conjugation

        # Generate exercise ID
        self._exercise_counter += 1
        exercise_id = f"EX{self._exercise_counter:06d}"

        # Select context
        context_category = self._map_category_to_context(category)
        context = random.choice(self.contexts[context_category])

        # Generate hints
        hints = self._generate_hints(verb, tense, person, category, result)

        # Generate distractors for multiple choice
        distractors = []
        if exercise_type == "multiple_choice":
            distractors = self._generate_distractors(verb, tense, person, correct_answer)

        exercise = Exercise(
            exercise_id=exercise_id,
            exercise_type=exercise_type,
            verb=verb,
            tense=tense,
            person=person,
            trigger_phrase=trigger_phrase,
            trigger_category=category,
            sentence_template=template,
            blank_position=template.index("____"),
            correct_answer=correct_answer,
            difficulty=difficulty,
            context=context,
            hints=hints,
            distractors=distractors
        )

        return exercise

    def _select_verb_by_difficulty(self, difficulty: str) -> str:
        """
        Select an appropriate verb based on difficulty level.

        Difficulty-based verb selection strategy:

        BEGINNER (regular verbs only):
        - 100% regular verbs from most common 6 per type
        - Examples: hablar, comer, vivir, trabajar, aprender, escribir
        - Focus: Learning basic subjunctive endings without complications

        INTERMEDIATE (mixed complexity):
        - 40% regular verbs (full common list)
        - 30% stem-changing verbs (e→ie, o→ue, e→i)
        - 30% common irregular verbs (ser, estar, ir, haber, etc.)
        - Focus: Applying stem changes and learning high-frequency irregulars

        ADVANCED (complex patterns):
        - 20% regular verbs (for variety)
        - 20% stem-changing verbs
        - 60% irregular verbs (all irregulars, including less common)
        - Focus: Mastering all patterns, including rare irregulars

        The weighted random selection ensures appropriate challenge level
        while maintaining variety within each difficulty tier.

        Args:
            difficulty: "beginner", "intermediate", or "advanced"

        Returns:
            Selected verb infinitive form

        Examples:
            >>> # Beginner always returns regular verb
            >>> verb = generator._select_verb_by_difficulty("beginner")
            >>> verb in ["hablar", "comer", "vivir", "trabajar", "aprender", "escribir"]
            True
        """
        if difficulty == "beginner":
            # Regular verbs only - first 6 most common of each type
            verb_type = random.choice(["-ar", "-er", "-ir"])
            return random.choice(COMMON_REGULAR_VERBS[verb_type][:6])

        elif difficulty == "intermediate":
            # Mix of regular (40%), stem-changing (30%), and common irregulars (30%)
            choice = random.random()
            if choice < 0.4:
                # Regular verb - full common list
                verb_type = random.choice(["-ar", "-er", "-ir"])
                return random.choice(COMMON_REGULAR_VERBS[verb_type])
            elif choice < 0.7:
                # Stem-changing verb (any pattern: e→ie, o→ue, e→i)
                pattern = random.choice(list(STEM_CHANGING_VERBS.keys()))
                return random.choice(list(STEM_CHANGING_VERBS[pattern].keys()))
            else:
                # Common irregular - high frequency verbs
                common_irregulars = ["ser", "estar", "ir", "haber", "tener", "hacer", "poder", "querer"]
                return random.choice(common_irregulars)

        else:  # advanced
            # All verb types, heavily favor complex patterns (80% non-regular)
            choice = random.random()
            if choice < 0.2:
                # Regular verb (20% for variety)
                verb_type = random.choice(["-ar", "-er", "-ir"])
                return random.choice(COMMON_REGULAR_VERBS[verb_type])
            elif choice < 0.4:
                # Stem-changing verb (20%)
                pattern = random.choice(list(STEM_CHANGING_VERBS.keys()))
                return random.choice(list(STEM_CHANGING_VERBS[pattern].keys()))
            else:
                # Any irregular verb (60%) - including rare/difficult ones
                return random.choice(list(IRREGULAR_VERBS.keys()))

    def _map_category_to_context(self, category: str) -> str:
        """Map WEIRDO category to context category"""
        mapping = {
            "Wishes": "planning",
            "Emotions": "emotions",
            "Impersonal_Expressions": "advice",
            "Recommendations": "advice",
            "Doubt_Denial": "emotions",
            "Ojalá": "planning"
        }
        return mapping.get(category, "social")

    def _generate_hints(
        self,
        verb: str,
        tense: str,
        person: str,
        category: str,
        conjugation_result
    ) -> List[str]:
        """Generate helpful hints for the exercise"""
        hints = []

        # Hint about trigger
        hints.append(f"This sentence uses a {category} trigger, which requires the subjunctive.")

        # Hint about verb type
        verb_info = self.engine.get_verb_info(verb)
        if verb_info["is_irregular"]:
            hints.append(f"'{verb}' is an irregular verb in the subjunctive.")
        elif verb_info["is_stem_changing"]:
            hints.append(
                f"'{verb}' is a stem-changing verb: {verb_info['stem_change_pattern']}."
            )

        # Hint about person
        hints.append(f"Conjugate for: {person}")

        # Hint about spelling changes
        if conjugation_result.has_spelling_change:
            hints.append(f"Remember: {conjugation_result.spelling_change_rule}")

        return hints

    def _generate_distractors(
        self,
        verb: str,
        tense: str,
        person: str,
        correct_answer: str
    ) -> List[str]:
        """
        Generate plausible incorrect answers for multiple choice exercises.

        Distractor generation strategy creates pedagogically valuable wrong answers:

        1. Wrong person distractors (up to 2):
           - Uses correct subjunctive mood and tense but different person
           - Example: If answer is "hable" (yo), add "hables" (tú)
           - Tests: Ability to identify correct grammatical person

        2. Mood confusion distractor:
           - Uses indicative mood instead of subjunctive
           - Example: If answer is "hable" (subjunctive), add "hablo" (indicative)
           - Tests: Understanding when subjunctive is required
           - Most common learner error, makes for valuable distractor

        The distractors are:
        - Plausible (grammatically valid forms of the same verb)
        - Educational (test specific aspects of subjunctive knowledge)
        - Unique (no duplicates, none match correct answer)
        - Limited (3 distractors maximum for standard multiple choice)

        Args:
            verb: Infinitive form
            tense: Subjunctive tense
            person: Grammatical person for correct answer
            correct_answer: The correct conjugation (to exclude)

        Returns:
            List of 1-3 plausible distractor options

        Examples:
            >>> # For "hable" (hablar, present_subjunctive, yo)
            >>> distractors = generator._generate_distractors("hablar", "present_subjunctive", "yo", "hable")
            >>> # Might return: ["hables", "hable", "hablo"]
            >>> # (tú form, él form, indicative yo)
        """
        distractors = []

        # Strategy 1: Add conjugations for other persons (same mood/tense)
        # This tests whether user knows the correct person
        all_conjugations = self.engine.get_full_conjugation_table(verb, tense)
        for p, result in all_conjugations.items():
            if result and result.conjugation != correct_answer and p != person:
                distractors.append(result.conjugation)
                if len(distractors) >= 2:
                    break

        # Strategy 2: Add indicative form as distractor (tests mood confusion)
        # This is the most common error type for subjunctive learners
        try:
            # Simplified indicative conjugation (production would use full conjugation engine)
            verb_stem = verb[:-2]
            verb_type = verb[-2:]

            # Present indicative endings for common persons
            if verb_type == "ar":
                indicative_ending = {"yo": "o", "tú": "as", "él/ella/usted": "a"}.get(person, "a")
            else:  # -er or -ir
                indicative_ending = {"yo": "o", "tú": "es", "él/ella/usted": "e"}.get(person, "e")

            indicative_form = verb_stem + indicative_ending

            # Only add if unique and different from correct answer
            if indicative_form not in distractors and indicative_form != correct_answer:
                distractors.append(indicative_form)
        except:
            # If indicative generation fails, continue with existing distractors
            pass

        # Shuffle to randomize order (prevents pattern recognition)
        random.shuffle(distractors)

        # Return maximum 3 distractors for standard multiple choice format
        return distractors[:3]

    def generate_exercise_set(
        self,
        count: int = 10,
        difficulty: str = "intermediate",
        weirdo_categories: Optional[List[str]] = None
    ) -> List[Exercise]:
        """
        Generate a set of exercises.

        Args:
            count: Number of exercises to generate
            difficulty: Difficulty level
            weirdo_categories: List of WEIRDO categories to include (or all if None)

        Returns:
            List of Exercise objects
        """
        exercises = []

        # Ensure variety across WEIRDO categories
        categories_to_use = weirdo_categories or list(WEIRDO_TRIGGERS.keys())

        for i in range(count):
            # Rotate through categories for variety
            category = categories_to_use[i % len(categories_to_use)]

            # Vary exercise type
            exercise_type = "multiple_choice" if i % 3 == 0 else "fill_in_blank"

            exercise = self.generate_exercise(
                difficulty=difficulty,
                exercise_type=exercise_type,
                weirdo_category=category
            )
            exercises.append(exercise)

        return exercises

    def get_weirdo_explanation(self, category: str) -> Dict:
        """Get explanation of a WEIRDO category"""
        if category not in WEIRDO_TRIGGERS:
            return {}

        trigger_info = WEIRDO_TRIGGERS[category]
        return {
            "category": category,
            "description": self._get_category_description(category),
            "triggers": trigger_info["triggers"],
            "examples": trigger_info["examples"]
        }

    def _get_category_description(self, category: str) -> str:
        """Get description for WEIRDO category"""
        descriptions = {
            "Wishes": "Expressing desires, wants, and preferences for others",
            "Emotions": "Expressing feelings and emotional reactions",
            "Impersonal_Expressions": "Impersonal statements about necessity, possibility, or judgment",
            "Recommendations": "Giving advice, suggestions, or commands",
            "Doubt_Denial": "Expressing doubt, denial, or uncertainty",
            "Ojalá": "Expressing hopes and wishes with 'ojalá'"
        }
        return descriptions.get(category, "")


# Example usage
if __name__ == "__main__":
    generator = ExerciseGenerator()

    # Generate single exercise
    exercise = generator.generate_exercise(difficulty="intermediate")
    print(f"Exercise: {exercise.get_display_sentence()}")
    print(f"Verb: {exercise.verb}")
    print(f"Category: {exercise.trigger_category}")
    print(f"Correct answer: {exercise.correct_answer}")
    print(f"Hints: {exercise.hints}")

    # Generate exercise set
    exercises = generator.generate_exercise_set(count=5, difficulty="beginner")
    print(f"\nGenerated {len(exercises)} exercises")

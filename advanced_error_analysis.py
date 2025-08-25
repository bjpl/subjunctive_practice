"""
Advanced Error Analysis and Guidance System
==========================================

This module provides sophisticated error analysis and guidance for Spanish subjunctive practice:

1. Intelligent error classification
2. Specific guidance based on error type
3. Pattern recognition for common mistakes
4. Personalized improvement suggestions
5. Cognitive load-aware feedback
6. Error prediction and prevention

Based on Second Language Acquisition (SLA) research and educational psychology principles.
"""

import re
import json
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from collections import defaultdict, Counter


class ErrorType(Enum):
    """Classification of subjunctive errors"""
    MOOD_CONFUSION = "mood_confusion"  # Used indicative instead of subjunctive
    CONJUGATION_ERROR = "conjugation_error"  # Wrong verb form
    TRIGGER_MISIDENTIFICATION = "trigger_misidentification"  # Missed subjunctive trigger
    STEM_CHANGE_ERROR = "stem_change_error"  # Incorrect stem changes
    IRREGULAR_VERB_ERROR = "irregular_verb_error"  # Wrong irregular form
    PERSON_NUMBER_ERROR = "person_number_error"  # Wrong person/number
    TENSE_ERROR = "tense_error"  # Wrong subjunctive tense
    SPELLING_ERROR = "spelling_error"  # Close but with typos
    INCOMPLETE_ANSWER = "incomplete_answer"  # Partial or missing response


@dataclass
class ErrorAnalysis:
    """Detailed error analysis result"""
    error_type: ErrorType
    confidence: float  # 0-1 confidence in classification
    user_answer: str
    correct_answer: str
    specific_issue: str  # Detailed description
    guidance_message: str  # Specific guidance
    practice_suggestions: List[str]  # Targeted practice recommendations
    cognitive_load: int  # 1-5 scale of complexity
    similar_patterns: List[str]  # Similar correct patterns to study


@dataclass
class LearnerProfile:
    """Track individual learner patterns and progress"""
    error_frequency: Dict[ErrorType, int]
    mastered_patterns: Set[str]
    struggling_patterns: Set[str]
    learning_velocity: float
    confidence_level: float
    last_updated: datetime


class SpanishLinguisticAnalyzer:
    """Analyzes Spanish morphology and syntax for error detection"""
    
    def __init__(self):
        # Common verb patterns and their subjunctive forms
        self.verb_patterns = {
            'ar_verbs': {
                'pattern': r'.*ar$',
                'subjunctive_endings': ['e', 'es', 'e', 'emos', 'éis', 'en']
            },
            'er_verbs': {
                'pattern': r'.*er$',
                'subjunctive_endings': ['a', 'as', 'a', 'amos', 'áis', 'an']
            },
            'ir_verbs': {
                'pattern': r'.*ir$',
                'subjunctive_endings': ['a', 'as', 'a', 'amos', 'áis', 'an']
            }
        }
        
        # Common irregular verbs and their subjunctive forms
        self.irregular_verbs = {
            'ser': ['sea', 'seas', 'sea', 'seamos', 'seáis', 'sean'],
            'estar': ['esté', 'estés', 'esté', 'estemos', 'estéis', 'estén'],
            'haber': ['haya', 'hayas', 'haya', 'hayamos', 'hayáis', 'hayan'],
            'tener': ['tenga', 'tengas', 'tenga', 'tengamos', 'tengáis', 'tengan'],
            'hacer': ['haga', 'hagas', 'haga', 'hagamos', 'hagáis', 'hagan'],
            'ir': ['vaya', 'vayas', 'vaya', 'vayamos', 'vayáis', 'vayan'],
            'dar': ['dé', 'des', 'dé', 'demos', 'deis', 'den'],
            'saber': ['sepa', 'sepas', 'sepa', 'sepamos', 'sepáis', 'sepan'],
            'ver': ['vea', 'veas', 'vea', 'veamos', 'veáis', 'vean']
        }
        
        # Stem-changing verbs patterns
        self.stem_changes = {
            'e_ie': ['pensar', 'cerrar', 'empezar', 'entender', 'perder'],
            'o_ue': ['contar', 'encontrar', 'volver', 'poder', 'dormir'],
            'e_i': ['pedir', 'servir', 'repetir', 'seguir'],
            'u_ue': ['jugar']
        }
        
        # Common subjunctive triggers
        self.subjunctive_triggers = {
            'emotion': ['alegrarse', 'temer', 'sentir', 'lamentar', 'sorprender'],
            'doubt': ['dudar', 'no creer', 'no pensar', 'negar', 'no estar seguro'],
            'wish': ['querer', 'desear', 'esperar', 'ojalá', 'preferir'],
            'impersonal': ['es necesario', 'es importante', 'es posible', 'es mejor', 'es raro'],
            'request': ['pedir', 'rogar', 'exigir', 'mandar', 'ordenar']
        }
    
    def extract_verb_info(self, verb: str) -> Dict:
        """Extract morphological information about a verb"""
        verb = verb.lower().strip()
        
        info = {
            'base_verb': verb,
            'verb_type': None,
            'is_irregular': False,
            'stem_change_type': None,
            'expected_subjunctive_forms': []
        }
        
        # Check if irregular
        if verb in self.irregular_verbs:
            info['is_irregular'] = True
            info['expected_subjunctive_forms'] = self.irregular_verbs[verb]
            return info
        
        # Check stem changes
        for change_type, verbs in self.stem_changes.items():
            if verb in verbs:
                info['stem_change_type'] = change_type
                break
        
        # Determine verb type
        if verb.endswith('ar'):
            info['verb_type'] = 'ar'
            info['expected_subjunctive_forms'] = self._generate_regular_subjunctive(verb, 'ar')
        elif verb.endswith('er'):
            info['verb_type'] = 'er'
            info['expected_subjunctive_forms'] = self._generate_regular_subjunctive(verb, 'er')
        elif verb.endswith('ir'):
            info['verb_type'] = 'ir'
            info['expected_subjunctive_forms'] = self._generate_regular_subjunctive(verb, 'ir')
        
        return info
    
    def _generate_regular_subjunctive(self, verb: str, verb_type: str) -> List[str]:
        """Generate regular subjunctive forms"""
        stem = verb[:-2]  # Remove -ar, -er, -ir
        
        if verb_type == 'ar':
            endings = ['e', 'es', 'e', 'emos', 'éis', 'en']
        else:  # er/ir verbs
            endings = ['a', 'as', 'a', 'amos', 'áis', 'an']
        
        return [stem + ending for ending in endings]
    
    def calculate_edit_distance(self, s1: str, s2: str) -> int:
        """Calculate Levenshtein distance between two strings"""
        if len(s1) < len(s2):
            return self.calculate_edit_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]


class AdvancedErrorAnalyzer:
    """Advanced error analysis system with linguistic intelligence"""
    
    def __init__(self):
        self.linguistic_analyzer = SpanishLinguisticAnalyzer()
        self.error_patterns = self._load_error_patterns()
        self.learner_profiles = {}  # Store individual learner data
    
    def analyze_error(self, user_answer: str, correct_answer: str, 
                     exercise_context: Dict, learner_id: str = "default") -> ErrorAnalysis:
        """Perform comprehensive error analysis"""
        
        user_answer = user_answer.lower().strip()
        correct_answer = correct_answer.lower().strip()
        
        # Quick check for exact match
        if user_answer == correct_answer:
            # This shouldn't happen for errors, but handle gracefully
            return self._create_success_analysis(user_answer, correct_answer)
        
        # Analyze the type of error
        error_type, confidence = self._classify_error_type(
            user_answer, correct_answer, exercise_context
        )
        
        # Generate specific guidance
        guidance = self._generate_specific_guidance(
            error_type, user_answer, correct_answer, exercise_context
        )
        
        # Get practice suggestions
        practice_suggestions = self._get_practice_suggestions(
            error_type, exercise_context
        )
        
        # Assess cognitive load
        cognitive_load = self._assess_cognitive_load(error_type, exercise_context)
        
        # Find similar patterns
        similar_patterns = self._find_similar_patterns(correct_answer, exercise_context)
        
        # Update learner profile
        self._update_learner_profile(learner_id, error_type)
        
        return ErrorAnalysis(
            error_type=error_type,
            confidence=confidence,
            user_answer=user_answer,
            correct_answer=correct_answer,
            specific_issue=self._describe_specific_issue(error_type, user_answer, correct_answer),
            guidance_message=guidance,
            practice_suggestions=practice_suggestions,
            cognitive_load=cognitive_load,
            similar_patterns=similar_patterns
        )
    
    def _classify_error_type(self, user_answer: str, correct_answer: str, 
                           context: Dict) -> Tuple[ErrorType, float]:
        """Classify the type of error with confidence level"""
        
        # Check for empty or incomplete answers
        if not user_answer or len(user_answer) < 2:
            return ErrorType.INCOMPLETE_ANSWER, 0.95
        
        # Check for spelling errors (high similarity but not exact)
        edit_distance = self.linguistic_analyzer.calculate_edit_distance(user_answer, correct_answer)
        similarity = 1 - (edit_distance / max(len(user_answer), len(correct_answer)))
        
        if similarity > 0.8:
            return ErrorType.SPELLING_ERROR, similarity
        
        # Extract verb information
        base_verb = context.get('base_verb', '')
        if base_verb:
            verb_info = self.linguistic_analyzer.extract_verb_info(base_verb)
            
            # Check for mood confusion (indicative instead of subjunctive)
            if self._is_indicative_form(user_answer, base_verb, context):
                return ErrorType.MOOD_CONFUSION, 0.9
            
            # Check for irregular verb errors
            if verb_info['is_irregular'] and user_answer not in verb_info['expected_subjunctive_forms']:
                return ErrorType.IRREGULAR_VERB_ERROR, 0.85
            
            # Check for stem change errors
            if verb_info['stem_change_type'] and not self._has_correct_stem_change(user_answer, verb_info):
                return ErrorType.STEM_CHANGE_ERROR, 0.8
        
        # Check for person/number errors
        if self._is_person_number_error(user_answer, correct_answer):
            return ErrorType.PERSON_NUMBER_ERROR, 0.75
        
        # Check for tense errors
        if self._is_tense_error(user_answer, context):
            return ErrorType.TENSE_ERROR, 0.7
        
        # Check for trigger misidentification
        if context.get('trigger_type') and self._missed_trigger(user_answer, context):
            return ErrorType.TRIGGER_MISIDENTIFICATION, 0.8
        
        # Default to conjugation error
        return ErrorType.CONJUGATION_ERROR, 0.6
    
    def _is_indicative_form(self, user_answer: str, base_verb: str, context: Dict) -> bool:
        """Check if user provided indicative instead of subjunctive"""
        # This would check against indicative conjugation patterns
        # Simplified implementation
        indicative_endings = ['o', 'as', 'a', 'amos', 'áis', 'an']  # Present indicative
        return any(user_answer.endswith(ending) for ending in indicative_endings)
    
    def _has_correct_stem_change(self, user_answer: str, verb_info: Dict) -> bool:
        """Check if stem change is correctly applied"""
        # Simplified implementation - would need full stem change logic
        stem_change_type = verb_info.get('stem_change_type', '')
        if not stem_change_type:
            return True
        
        # Basic check for common stem changes
        if stem_change_type == 'e_ie' and 'ie' in user_answer:
            return True
        elif stem_change_type == 'o_ue' and 'ue' in user_answer:
            return True
        elif stem_change_type == 'e_i' and user_answer.count('i') > user_answer.count('e'):
            return True
        
        return False
    
    def _is_person_number_error(self, user_answer: str, correct_answer: str) -> bool:
        """Check if error is in person/number agreement"""
        # Compare endings to detect person/number issues
        user_ending = user_answer[-2:] if len(user_answer) > 2 else user_answer
        correct_ending = correct_answer[-2:] if len(correct_answer) > 2 else correct_answer
        
        # If the stems are similar but endings different, likely person/number error
        if user_answer[:-2] == correct_answer[:-2] and user_ending != correct_ending:
            return True
        
        return False
    
    def _is_tense_error(self, user_answer: str, context: Dict) -> bool:
        """Check if wrong subjunctive tense was used"""
        expected_tense = context.get('tense', 'present')
        
        # Simplified tense detection
        if expected_tense == 'present' and ('ra' in user_answer or 'se' in user_answer):
            return True  # Used imperfect instead of present
        elif expected_tense == 'imperfect' and not ('ra' in user_answer or 'se' in user_answer):
            return True  # Used present instead of imperfect
        
        return False
    
    def _missed_trigger(self, user_answer: str, context: Dict) -> bool:
        """Check if user missed the subjunctive trigger"""
        # This would analyze the context for subjunctive triggers
        trigger_type = context.get('trigger_type', '')
        
        # If trigger requires subjunctive but user didn't use it
        if trigger_type in ['emotion', 'doubt', 'wish', 'impersonal'] and \
           self._is_indicative_form(user_answer, context.get('base_verb', ''), context):
            return True
        
        return False
    
    def _generate_specific_guidance(self, error_type: ErrorType, user_answer: str, 
                                  correct_answer: str, context: Dict) -> str:
        """Generate specific guidance based on error type"""
        
        guidance_templates = {
            ErrorType.MOOD_CONFUSION: [
                "You used the indicative mood, but this context requires the subjunctive. "
                "Look for the trigger word '{trigger}' which expresses {trigger_type}.",
                "Remember: after expressions of {trigger_type}, we use subjunctive to show "
                "uncertainty or subjectivity.",
                "The key phrase '{trigger}' signals that what follows is not a fact, "
                "but a subjective view that needs subjunctive."
            ],
            
            ErrorType.CONJUGATION_ERROR: [
                "Check the conjugation pattern for {verb_type} verbs in subjunctive.",
                "Remember: for {verb_type} verbs, the subjunctive endings are {endings}.",
                "The correct form is '{correct}' - notice the {specific_part} part."
            ],
            
            ErrorType.STEM_CHANGE_ERROR: [
                "This verb has a stem change ({stem_change}) in the subjunctive.",
                "Remember: '{base_verb}' changes its stem in subjunctive forms.",
                "The pattern is {stem_change}: the root changes from '{old_stem}' to '{new_stem}'."
            ],
            
            ErrorType.IRREGULAR_VERB_ERROR: [
                "'{base_verb}' is an irregular verb with special subjunctive forms.",
                "Irregular verbs don't follow the standard pattern - they have unique forms.",
                "For '{base_verb}', the subjunctive forms are: {irregular_forms}."
            ],
            
            ErrorType.PERSON_NUMBER_ERROR: [
                "Check the subject - you need the {correct_person} form.",
                "The subject '{subject}' requires the {person_number} conjugation.",
                "Make sure the verb agrees with the subject: {subject} → {correct_form}."
            ],
            
            ErrorType.TENSE_ERROR: [
                "This context requires {correct_tense} subjunctive, not {used_tense}.",
                "The time reference indicates {correct_tense} subjunctive is needed.",
                "Look at the context clues that point to {correct_tense} subjunctive."
            ],
            
            ErrorType.SPELLING_ERROR: [
                "Very close! Check the spelling - you wrote '{user}' but it's '{correct}'.",
                "Just a small spelling error - the correct form is '{correct}'.",
                "Almost perfect! Remember the accent marks and spelling: '{correct}'."
            ],
            
            ErrorType.TRIGGER_MISIDENTIFICATION: [
                "The phrase '{trigger}' is a subjunctive trigger expressing {trigger_type}.",
                "Did you notice the trigger word? '{trigger}' requires subjunctive.",
                "Key insight: '{trigger}' creates uncertainty, so we need subjunctive."
            ],
            
            ErrorType.INCOMPLETE_ANSWER: [
                "Please provide a complete answer.",
                "Make sure to write the full conjugated verb form.",
                "Don't forget to include the complete subjunctive form."
            ]
        }
        
        templates = guidance_templates.get(error_type, ["General conjugation error."])
        template = templates[0]  # Use first template for now
        
        # Fill in template variables
        try:
            guidance = template.format(
                trigger=context.get('trigger', ''),
                trigger_type=context.get('trigger_type', 'subjectivity'),
                verb_type=context.get('verb_type', 'regular'),
                endings=context.get('expected_endings', ''),
                correct=correct_answer,
                specific_part=self._identify_specific_part(user_answer, correct_answer),
                base_verb=context.get('base_verb', ''),
                stem_change=context.get('stem_change_type', ''),
                old_stem=context.get('old_stem', ''),
                new_stem=context.get('new_stem', ''),
                irregular_forms=', '.join(context.get('irregular_forms', [])),
                correct_person=context.get('person', ''),
                subject=context.get('subject', ''),
                person_number=context.get('person_number', ''),
                correct_form=correct_answer,
                correct_tense=context.get('correct_tense', 'present'),
                used_tense=context.get('used_tense', 'unknown'),
                user=user_answer
            )
        except KeyError:
            # Fallback if template variables are missing
            guidance = f"The correct form is '{correct_answer}'. Review the subjunctive rules for this context."
        
        return guidance
    
    def _identify_specific_part(self, user_answer: str, correct_answer: str) -> str:
        """Identify the specific part that differs between answers"""
        # Simple implementation - could be more sophisticated
        if len(user_answer) != len(correct_answer):
            return "length"
        
        differences = []
        for i, (u, c) in enumerate(zip(user_answer, correct_answer)):
            if u != c:
                differences.append(f"position {i+1}")
        
        return differences[0] if differences else "ending"
    
    def _get_practice_suggestions(self, error_type: ErrorType, context: Dict) -> List[str]:
        """Get targeted practice suggestions"""
        
        suggestions = {
            ErrorType.MOOD_CONFUSION: [
                "Practice identifying subjunctive triggers",
                "Review the difference between indicative and subjunctive moods",
                "Focus on expressions of emotion, doubt, and wish"
            ],
            
            ErrorType.CONJUGATION_ERROR: [
                "Practice regular subjunctive conjugations",
                f"Focus on {context.get('verb_type', 'regular')} verb patterns",
                "Review subjunctive endings systematically"
            ],
            
            ErrorType.STEM_CHANGE_ERROR: [
                "Practice stem-changing verbs in subjunctive",
                f"Focus on {context.get('stem_change_type', '')} pattern verbs",
                "Review how stem changes apply in subjunctive mood"
            ],
            
            ErrorType.IRREGULAR_VERB_ERROR: [
                "Memorize common irregular subjunctive forms",
                f"Practice '{context.get('base_verb', '')}' conjugation specifically",
                "Review high-frequency irregular verbs"
            ],
            
            ErrorType.PERSON_NUMBER_ERROR: [
                "Practice subject-verb agreement in subjunctive",
                "Review personal pronouns and their verb forms",
                "Focus on distinguishing similar subjunctive forms"
            ],
            
            ErrorType.TENSE_ERROR: [
                "Review when to use different subjunctive tenses",
                "Practice sequence of tenses rules",
                "Focus on time expressions that indicate subjunctive tense"
            ]
        }
        
        return suggestions.get(error_type, ["General subjunctive practice"])
    
    def _assess_cognitive_load(self, error_type: ErrorType, context: Dict) -> int:
        """Assess cognitive complexity (1-5 scale)"""
        complexity_map = {
            ErrorType.SPELLING_ERROR: 1,
            ErrorType.PERSON_NUMBER_ERROR: 2,
            ErrorType.CONJUGATION_ERROR: 2,
            ErrorType.STEM_CHANGE_ERROR: 3,
            ErrorType.TENSE_ERROR: 3,
            ErrorType.IRREGULAR_VERB_ERROR: 4,
            ErrorType.MOOD_CONFUSION: 4,
            ErrorType.TRIGGER_MISIDENTIFICATION: 5
        }
        
        base_complexity = complexity_map.get(error_type, 3)
        
        # Adjust based on context
        if context.get('is_irregular', False):
            base_complexity += 1
        if context.get('has_stem_change', False):
            base_complexity += 1
        
        return min(5, base_complexity)
    
    def _find_similar_patterns(self, correct_answer: str, context: Dict) -> List[str]:
        """Find similar patterns for reinforcement learning"""
        patterns = []
        
        verb_type = context.get('verb_type', '')
        if verb_type:
            patterns.append(f"Other {verb_type} verbs follow the same pattern")
        
        stem_change = context.get('stem_change_type', '')
        if stem_change:
            patterns.append(f"All {stem_change} verbs have similar stem changes")
        
        trigger_type = context.get('trigger_type', '')
        if trigger_type:
            patterns.append(f"Expressions of {trigger_type} all require subjunctive")
        
        return patterns
    
    def _update_learner_profile(self, learner_id: str, error_type: ErrorType):
        """Update individual learner profile"""
        if learner_id not in self.learner_profiles:
            self.learner_profiles[learner_id] = LearnerProfile(
                error_frequency=defaultdict(int),
                mastered_patterns=set(),
                struggling_patterns=set(),
                learning_velocity=0.0,
                confidence_level=0.5,
                last_updated=datetime.now()
            )
        
        profile = self.learner_profiles[learner_id]
        profile.error_frequency[error_type] += 1
        profile.last_updated = datetime.now()
        
        # Update struggling patterns
        if profile.error_frequency[error_type] >= 3:
            profile.struggling_patterns.add(error_type.value)
    
    def _create_success_analysis(self, user_answer: str, correct_answer: str) -> ErrorAnalysis:
        """Create analysis for successful answers (shouldn't happen in error analysis)"""
        return ErrorAnalysis(
            error_type=ErrorType.SPELLING_ERROR,  # Placeholder
            confidence=0.0,
            user_answer=user_answer,
            correct_answer=correct_answer,
            specific_issue="No error detected",
            guidance_message="Excellent work!",
            practice_suggestions=["Keep practicing!"],
            cognitive_load=1,
            similar_patterns=[]
        )
    
    def _load_error_patterns(self) -> Dict:
        """Load common error patterns from data"""
        # In a full implementation, this would load from a file or database
        return {
            "common_mistakes": {
                "ser_estar_confusion": 0.3,
                "indicative_for_subjunctive": 0.4,
                "wrong_stem_change": 0.2,
                "incorrect_irregular": 0.25
            }
        }
    
    def get_learner_insights(self, learner_id: str) -> Dict:
        """Get insights about learner's progress and patterns"""
        if learner_id not in self.learner_profiles:
            return {"message": "No data available yet"}
        
        profile = self.learner_profiles[learner_id]
        
        # Find most common errors
        most_common_errors = Counter(profile.error_frequency).most_common(3)
        
        # Calculate improvement areas
        improvement_areas = []
        for error_type, frequency in most_common_errors:
            if frequency >= 2:
                improvement_areas.append(error_type.value)
        
        return {
            "most_common_errors": [error.value for error, _ in most_common_errors],
            "improvement_areas": improvement_areas,
            "struggling_patterns": list(profile.struggling_patterns),
            "confidence_level": profile.confidence_level,
            "total_errors": sum(profile.error_frequency.values()),
            "last_updated": profile.last_updated.isoformat()
        }


# Integration helper functions
def integrate_error_analysis_with_feedback(feedback_widget, exercise_context: Dict):
    """Helper function to integrate error analysis with feedback widget"""
    analyzer = AdvancedErrorAnalyzer()
    
    def enhanced_error_handler(user_answer: str, correct_answer: str, learner_id: str = "default"):
        # Perform advanced error analysis
        error_analysis = analyzer.analyze_error(
            user_answer, correct_answer, exercise_context, learner_id
        )
        
        # Create enhanced error message
        error_message = f"""
        <div style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 12px; border-radius: 6px;">
            <h4 style="color: #856404; margin-top: 0;">🔍 Error Analysis</h4>
            <p><strong>Issue:</strong> {error_analysis.specific_issue}</p>
            <p><strong>Guidance:</strong> {error_analysis.guidance_message}</p>
            
            <details style="margin-top: 10px;">
                <summary style="font-weight: bold; cursor: pointer;">💡 Practice Suggestions</summary>
                <ul style="margin: 8px 0;">
                    {"".join(f"<li>{suggestion}</li>" for suggestion in error_analysis.practice_suggestions)}
                </ul>
            </details>
            
            <div style="font-size: 0.9em; color: #6c757d; margin-top: 8px;">
                Complexity Level: {"⭐" * error_analysis.cognitive_load} 
                ({error_analysis.cognitive_load}/5)
            </div>
        </div>
        """
        
        # Display in feedback widget
        feedback_widget.feedback_content.setHtml(error_message)
        
        return error_analysis
    
    return enhanced_error_handler
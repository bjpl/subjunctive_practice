"""
Spanish Subjunctive Learning Services

This package contains the core services for the Spanish subjunctive learning application.
"""

from .conjugation import ConjugationEngine
from .exercise_generator import ExerciseGenerator
from .learning_algorithm import LearningAlgorithm, SM2Algorithm
from .feedback import FeedbackGenerator, ErrorAnalyzer
from .gamification import (
    calculate_exercise_xp,
    calculate_session_xp,
    calculate_level_info,
    Difficulty,
)

__all__ = [
    'ConjugationEngine',
    'ExerciseGenerator',
    'LearningAlgorithm',
    'SM2Algorithm',
    'FeedbackGenerator',
    'ErrorAnalyzer',
    'calculate_exercise_xp',
    'calculate_session_xp',
    'calculate_level_info',
    'Difficulty',
]

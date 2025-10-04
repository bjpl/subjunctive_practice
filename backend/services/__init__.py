"""
Spanish Subjunctive Learning Services

This package contains the core services for the Spanish subjunctive learning application.
"""

from .conjugation import ConjugationEngine
from .exercise_generator import ExerciseGenerator
from .learning_algorithm import LearningAlgorithm, SM2Algorithm
from .feedback import FeedbackGenerator, ErrorAnalyzer

__all__ = [
    'ConjugationEngine',
    'ExerciseGenerator',
    'LearningAlgorithm',
    'SM2Algorithm',
    'FeedbackGenerator',
    'ErrorAnalyzer'
]

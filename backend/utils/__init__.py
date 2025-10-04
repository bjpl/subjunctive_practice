"""
Utility modules for Spanish subjunctive learning
"""

from .spanish_grammar import (
    REGULAR_ENDINGS,
    IRREGULAR_VERBS,
    STEM_CHANGING_VERBS,
    SPELLING_CHANGES,
    WEIRDO_TRIGGERS,
    get_verb_type,
    apply_spelling_changes
)

__all__ = [
    'REGULAR_ENDINGS',
    'IRREGULAR_VERBS',
    'STEM_CHANGING_VERBS',
    'SPELLING_CHANGES',
    'WEIRDO_TRIGGERS',
    'get_verb_type',
    'apply_spelling_changes'
]

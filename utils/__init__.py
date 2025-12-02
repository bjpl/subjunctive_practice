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

from .user_utils import (
    UserIdError,
    parse_user_id,
    format_user_id,
    get_user_id_from_token,
    validate_user_id
)

__all__ = [
    'REGULAR_ENDINGS',
    'IRREGULAR_VERBS',
    'STEM_CHANGING_VERBS',
    'SPELLING_CHANGES',
    'WEIRDO_TRIGGERS',
    'get_verb_type',
    'apply_spelling_changes',
    'UserIdError',
    'parse_user_id',
    'format_user_id',
    'get_user_id_from_token',
    'validate_user_id'
]

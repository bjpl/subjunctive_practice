"""
User ID utility functions.
Provides consistent user ID parsing across the codebase.
"""

from typing import Union, Optional
import logging

logger = logging.getLogger(__name__)


class UserIdError(ValueError):
    """Raised when user ID parsing fails."""
    pass


def parse_user_id(user_id: Union[str, int]) -> int:
    """
    Parse user ID from various formats to integer.

    Handles formats:
    - Integer: 7 -> 7
    - String integer: "7" -> 7
    - Prefixed string: "user_7" -> 7
    - JWT sub claim: "user_123" -> 123

    Args:
        user_id: User ID in any supported format

    Returns:
        Integer user ID

    Raises:
        UserIdError: If user ID cannot be parsed
    """
    if user_id is None:
        raise UserIdError("User ID cannot be None")

    # Already an integer
    if isinstance(user_id, int):
        if user_id <= 0:
            raise UserIdError(f"User ID must be positive, got: {user_id}")
        return user_id

    # String format
    if isinstance(user_id, str):
        user_id = user_id.strip()

        if not user_id:
            raise UserIdError("User ID cannot be empty string")

        # Handle prefixed format (e.g., "user_7")
        if '_' in user_id:
            try:
                # Take the last part after underscore
                numeric_part = user_id.split('_')[-1]
                result = int(numeric_part)
                if result <= 0:
                    raise UserIdError(f"User ID must be positive, got: {result}")
                return result
            except ValueError:
                raise UserIdError(f"Cannot parse user ID from: {user_id}")

        # Handle plain string integer
        try:
            result = int(user_id)
            if result <= 0:
                raise UserIdError(f"User ID must be positive, got: {result}")
            return result
        except ValueError:
            raise UserIdError(f"Cannot parse user ID from: {user_id}")

    raise UserIdError(f"Unsupported user ID type: {type(user_id)}")


def format_user_id(user_id: int, prefix: str = "user") -> str:
    """
    Format user ID as prefixed string.

    Args:
        user_id: Integer user ID
        prefix: Prefix to use (default: "user")

    Returns:
        Formatted string like "user_7"
    """
    return f"{prefix}_{user_id}"


def get_user_id_from_token(token_payload: dict) -> int:
    """
    Extract and parse user ID from JWT token payload.

    Args:
        token_payload: Decoded JWT payload with 'sub' claim

    Returns:
        Integer user ID

    Raises:
        UserIdError: If 'sub' claim is missing or invalid
    """
    if "sub" not in token_payload:
        raise UserIdError("Token payload missing 'sub' claim")

    return parse_user_id(token_payload["sub"])


def validate_user_id(user_id: Union[str, int]) -> bool:
    """
    Validate if a user ID can be parsed successfully.

    Args:
        user_id: User ID to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        parse_user_id(user_id)
        return True
    except UserIdError:
        return False

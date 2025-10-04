"""
Utility Helper Functions
Common utilities for the backend application
"""
import hashlib
import secrets
import string
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union
from uuid import UUID, uuid4
import re
from pathlib import Path


# ================================
# String Utilities
# ================================

def generate_random_string(length: int = 32, include_punctuation: bool = False) -> str:
    """
    Generate a cryptographically secure random string.

    Args:
        length: Length of the string to generate
        include_punctuation: Whether to include special characters

    Returns:
        Random string
    """
    characters = string.ascii_letters + string.digits
    if include_punctuation:
        characters += string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))


def generate_uuid() -> str:
    """Generate a UUID4 string."""
    return str(uuid4())


def slugify(text: str) -> str:
    """
    Convert text to URL-friendly slug.

    Args:
        text: Text to slugify

    Returns:
        Slugified text
    """
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate string to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


# ================================
# Validation Utilities
# ================================

def is_valid_email(email: str) -> bool:
    """
    Validate email format.

    Args:
        email: Email address to validate

    Returns:
        True if valid email format
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_valid_uuid(uuid_string: str) -> bool:
    """
    Validate UUID format.

    Args:
        uuid_string: UUID string to validate

    Returns:
        True if valid UUID
    """
    try:
        UUID(uuid_string, version=4)
        return True
    except (ValueError, AttributeError):
        return False


def is_strong_password(password: str, min_length: int = 8) -> bool:
    """
    Check if password meets strength requirements.

    Args:
        password: Password to check
        min_length: Minimum password length

    Returns:
        True if password is strong enough
    """
    if len(password) < min_length:
        return False

    has_upper = bool(re.search(r'[A-Z]', password))
    has_lower = bool(re.search(r'[a-z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

    return sum([has_upper, has_lower, has_digit, has_special]) >= 3


# ================================
# DateTime Utilities
# ================================

def get_current_timestamp() -> datetime:
    """Get current UTC timestamp."""
    return datetime.utcnow()


def format_datetime(dt: datetime, format_string: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format datetime object to string.

    Args:
        dt: Datetime object
        format_string: Format string

    Returns:
        Formatted datetime string
    """
    return dt.strftime(format_string)


def parse_datetime(date_string: str, format_string: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """
    Parse datetime string to datetime object.

    Args:
        date_string: Datetime string
        format_string: Format string

    Returns:
        Datetime object
    """
    return datetime.strptime(date_string, format_string)


def add_days(dt: datetime, days: int) -> datetime:
    """
    Add days to datetime.

    Args:
        dt: Datetime object
        days: Number of days to add

    Returns:
        New datetime object
    """
    return dt + timedelta(days=days)


def is_expired(expiry_date: datetime) -> bool:
    """
    Check if datetime has passed.

    Args:
        expiry_date: Expiry datetime

    Returns:
        True if expired
    """
    return datetime.utcnow() > expiry_date


# ================================
# Dictionary Utilities
# ================================

def deep_merge(dict1: Dict, dict2: Dict) -> Dict:
    """
    Deep merge two dictionaries.

    Args:
        dict1: First dictionary
        dict2: Second dictionary (takes precedence)

    Returns:
        Merged dictionary
    """
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def remove_none_values(data: Dict) -> Dict:
    """
    Remove keys with None values from dictionary.

    Args:
        data: Dictionary to clean

    Returns:
        Dictionary without None values
    """
    return {k: v for k, v in data.items() if v is not None}


def flatten_dict(data: Dict, parent_key: str = '', sep: str = '.') -> Dict:
    """
    Flatten nested dictionary.

    Args:
        data: Dictionary to flatten
        parent_key: Parent key prefix
        sep: Separator between keys

    Returns:
        Flattened dictionary
    """
    items = []
    for k, v in data.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


# ================================
# File Utilities
# ================================

def get_file_hash(file_path: Path, algorithm: str = "sha256") -> str:
    """
    Calculate file hash.

    Args:
        file_path: Path to file
        algorithm: Hash algorithm (md5, sha1, sha256)

    Returns:
        File hash as hex string
    """
    hash_func = hashlib.new(algorithm)
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()


def get_file_extension(filename: str) -> str:
    """
    Get file extension.

    Args:
        filename: Filename

    Returns:
        File extension (including dot)
    """
    return Path(filename).suffix


def is_allowed_file(filename: str, allowed_extensions: List[str]) -> bool:
    """
    Check if file extension is allowed.

    Args:
        filename: Filename to check
        allowed_extensions: List of allowed extensions (with dots)

    Returns:
        True if allowed
    """
    return get_file_extension(filename).lower() in allowed_extensions


# ================================
# Pagination Utilities
# ================================

def paginate_list(items: List[Any], page: int = 1, page_size: int = 10) -> Dict[str, Any]:
    """
    Paginate a list of items.

    Args:
        items: List to paginate
        page: Page number (1-indexed)
        page_size: Items per page

    Returns:
        Dictionary with paginated results and metadata
    """
    total_items = len(items)
    total_pages = (total_items + page_size - 1) // page_size
    page = max(1, min(page, total_pages)) if total_pages > 0 else 1

    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_items = items[start_idx:end_idx]

    return {
        "items": paginated_items,
        "total_items": total_items,
        "total_pages": total_pages,
        "current_page": page,
        "page_size": page_size,
        "has_next": page < total_pages,
        "has_previous": page > 1,
    }


def calculate_offset(page: int, page_size: int) -> int:
    """
    Calculate database offset for pagination.

    Args:
        page: Page number (1-indexed)
        page_size: Items per page

    Returns:
        Offset value
    """
    return (page - 1) * page_size


# ================================
# Response Formatting
# ================================

def success_response(data: Any = None, message: str = "Success") -> Dict[str, Any]:
    """
    Create standardized success response.

    Args:
        data: Response data
        message: Success message

    Returns:
        Formatted success response
    """
    return {
        "success": True,
        "message": message,
        "data": data,
    }


def error_response(message: str, error_code: Optional[str] = None, details: Any = None) -> Dict[str, Any]:
    """
    Create standardized error response.

    Args:
        message: Error message
        error_code: Optional error code
        details: Additional error details

    Returns:
        Formatted error response
    """
    response = {
        "success": False,
        "message": message,
    }
    if error_code:
        response["error_code"] = error_code
    if details:
        response["details"] = details
    return response


# ================================
# Data Sanitization
# ================================

def sanitize_html(text: str) -> str:
    """
    Remove HTML tags from text.

    Args:
        text: Text with potential HTML

    Returns:
        Text without HTML tags
    """
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace in text.

    Args:
        text: Text to normalize

    Returns:
        Text with normalized whitespace
    """
    return ' '.join(text.split())


# ================================
# Number Utilities
# ================================

def clamp(value: Union[int, float], min_value: Union[int, float], max_value: Union[int, float]) -> Union[int, float]:
    """
    Clamp value between min and max.

    Args:
        value: Value to clamp
        min_value: Minimum value
        max_value: Maximum value

    Returns:
        Clamped value
    """
    return max(min_value, min(value, max_value))


def percentage(part: Union[int, float], whole: Union[int, float], decimal_places: int = 2) -> float:
    """
    Calculate percentage.

    Args:
        part: Part value
        whole: Whole value
        decimal_places: Number of decimal places

    Returns:
        Percentage value
    """
    if whole == 0:
        return 0.0
    return round((part / whole) * 100, decimal_places)

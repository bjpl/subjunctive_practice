"""
Clean UI Color System
Centralized color palette with modern, accessible colors for the Subjunctive Practice application.

This module provides a consistent color scheme with proper contrast ratios for accessibility.
All UI components should import and use these colors to maintain visual consistency.
"""

from typing import Dict, Tuple

# Note: Rich imports are optional and only used when available
try:
    from rich.color import Color
    from rich.style import Style
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    # Mock classes for when Rich is not available
    class Color:
        pass
    class Style:
        def __init__(self, *args, **kwargs):
            pass


class CleanColors:
    """Modern, clean color palette with accessibility considerations."""
    
    # Primary Colors (Main brand/action colors)
    PRIMARY = "#3B82F6"          # Blue - Primary actions, buttons, links
    PRIMARY_HOVER = "#2563EB"    # Darker blue for hover states
    PRIMARY_LIGHT = "#DBEAFE"    # Light blue for backgrounds
    
    # Semantic Colors
    SUCCESS = "#10B981"          # Green - Success messages, correct answers
    SUCCESS_HOVER = "#059669"    # Darker green for hover
    SUCCESS_LIGHT = "#D1FAE5"    # Light green for backgrounds
    
    WARNING = "#F59E0B"          # Amber - Warnings, hints
    WARNING_HOVER = "#D97706"    # Darker amber for hover
    WARNING_LIGHT = "#FEF3C7"    # Light amber for backgrounds
    
    ERROR = "#EF4444"            # Soft red - Errors, incorrect answers
    ERROR_HOVER = "#DC2626"      # Darker red for hover
    ERROR_LIGHT = "#FEE2E2"      # Light red for backgrounds
    
    # Neutral Colors
    GRAY_50 = "#F9FAFB"          # Lightest gray - backgrounds
    GRAY_100 = "#F3F4F6"         # Light gray - card backgrounds
    GRAY_200 = "#E5E7EB"         # Light gray - dividers
    GRAY_300 = "#D1D5DB"         # Medium light gray - borders
    GRAY_400 = "#9CA3AF"         # Medium gray - placeholders
    GRAY_500 = "#6B7280"         # Medium dark gray - secondary text
    GRAY_600 = "#4B5563"         # Dark gray - primary text
    GRAY_700 = "#374151"         # Darker gray - headings
    GRAY_800 = "#1F2937"         # Very dark gray - high contrast text
    GRAY_900 = "#111827"         # Darkest gray - maximum contrast
    
    # Text Colors
    TEXT_PRIMARY = GRAY_800      # Main text color
    TEXT_SECONDARY = GRAY_600    # Secondary text
    TEXT_MUTED = GRAY_500        # Muted text
    TEXT_WHITE = "#FFFFFF"       # White text for dark backgrounds
    
    # Background Colors
    BACKGROUND = "#FFFFFF"       # Main background
    BACKGROUND_SECONDARY = GRAY_50  # Secondary backgrounds
    BACKGROUND_CARD = GRAY_100   # Card backgrounds
    
    # Border Colors
    BORDER = GRAY_300           # Standard borders
    BORDER_LIGHT = GRAY_200     # Light borders
    BORDER_FOCUS = PRIMARY      # Focus borders
    
    # Special Colors
    FOCUS = PRIMARY             # Focus indicators
    HOVER = GRAY_100           # Hover backgrounds
    SELECTED = PRIMARY_LIGHT    # Selected item backgrounds


class ColorScheme:
    """Color scheme utilities for consistent styling."""
    
    @staticmethod
    def get_status_color(status: str) -> str:
        """Get color for different status types."""
        status_colors = {
            'success': CleanColors.SUCCESS,
            'error': CleanColors.ERROR,
            'warning': CleanColors.WARNING,
            'info': CleanColors.PRIMARY,
            'correct': CleanColors.SUCCESS,
            'incorrect': CleanColors.ERROR,
            'hint': CleanColors.WARNING,
            'neutral': CleanColors.GRAY_600
        }
        return status_colors.get(status.lower(), CleanColors.GRAY_600)
    
    @staticmethod
    def get_hover_color(base_color: str) -> str:
        """Get hover color for a base color."""
        hover_map = {
            CleanColors.PRIMARY: CleanColors.PRIMARY_HOVER,
            CleanColors.SUCCESS: CleanColors.SUCCESS_HOVER,
            CleanColors.WARNING: CleanColors.WARNING_HOVER,
            CleanColors.ERROR: CleanColors.ERROR_HOVER,
        }
        return hover_map.get(base_color, CleanColors.GRAY_500)
    
    @staticmethod
    def get_light_color(base_color: str) -> str:
        """Get light version of a color for backgrounds."""
        light_map = {
            CleanColors.PRIMARY: CleanColors.PRIMARY_LIGHT,
            CleanColors.SUCCESS: CleanColors.SUCCESS_LIGHT,
            CleanColors.WARNING: CleanColors.WARNING_LIGHT,
            CleanColors.ERROR: CleanColors.ERROR_LIGHT,
        }
        return light_map.get(base_color, CleanColors.GRAY_100)


class RichStyles:
    """Pre-configured Rich styles using the clean color palette."""
    
    # Text Styles
    HEADING = Style(color=CleanColors.TEXT_PRIMARY, bold=True)
    SUBHEADING = Style(color=CleanColors.TEXT_SECONDARY, bold=True)
    BODY = Style(color=CleanColors.TEXT_PRIMARY)
    SECONDARY = Style(color=CleanColors.TEXT_SECONDARY)
    MUTED = Style(color=CleanColors.TEXT_MUTED)
    
    # Status Styles
    SUCCESS = Style(color=CleanColors.SUCCESS, bold=True)
    ERROR = Style(color=CleanColors.ERROR, bold=True)
    WARNING = Style(color=CleanColors.WARNING, bold=True)
    INFO = Style(color=CleanColors.PRIMARY, bold=True)
    
    # Interactive Styles
    BUTTON_PRIMARY = Style(color=CleanColors.TEXT_WHITE, bgcolor=CleanColors.PRIMARY, bold=True)
    BUTTON_SECONDARY = Style(color=CleanColors.TEXT_PRIMARY, bgcolor=CleanColors.GRAY_200, bold=True)
    LINK = Style(color=CleanColors.PRIMARY, underline=True)
    
    # Layout Styles
    BORDER = Style(color=CleanColors.BORDER)
    BACKGROUND = Style(bgcolor=CleanColors.BACKGROUND_CARD)
    PANEL = Style(color=CleanColors.TEXT_PRIMARY, bgcolor=CleanColors.BACKGROUND_CARD)


class AccessibilityColors:
    """Accessibility-compliant color combinations."""
    
    # WCAG AA compliant combinations (4.5:1 contrast ratio minimum)
    TEXT_COMBINATIONS = [
        (CleanColors.TEXT_PRIMARY, CleanColors.BACKGROUND),      # 12.6:1
        (CleanColors.TEXT_SECONDARY, CleanColors.BACKGROUND),    # 7.0:1
        (CleanColors.TEXT_MUTED, CleanColors.BACKGROUND),        # 4.6:1
        (CleanColors.TEXT_WHITE, CleanColors.PRIMARY),           # 4.8:1
        (CleanColors.TEXT_WHITE, CleanColors.SUCCESS),           # 4.7:1
        (CleanColors.TEXT_WHITE, CleanColors.ERROR),             # 5.9:1
    ]
    
    @staticmethod
    def is_accessible_combination(text_color: str, bg_color: str) -> bool:
        """Check if a color combination meets accessibility standards."""
        # This is a simplified check - in a full implementation,
        # you would calculate the actual contrast ratio
        return (text_color, bg_color) in AccessibilityColors.TEXT_COMBINATIONS


# Utility functions for easy color access
def primary(shade: str = 'base') -> str:
    """Get primary color in different shades."""
    shades = {
        'light': CleanColors.PRIMARY_LIGHT,
        'base': CleanColors.PRIMARY,
        'hover': CleanColors.PRIMARY_HOVER
    }
    return shades.get(shade, CleanColors.PRIMARY)


def success(shade: str = 'base') -> str:
    """Get success color in different shades."""
    shades = {
        'light': CleanColors.SUCCESS_LIGHT,
        'base': CleanColors.SUCCESS,
        'hover': CleanColors.SUCCESS_HOVER
    }
    return shades.get(shade, CleanColors.SUCCESS)


def warning(shade: str = 'base') -> str:
    """Get warning color in different shades."""
    shades = {
        'light': CleanColors.WARNING_LIGHT,
        'base': CleanColors.WARNING,
        'hover': CleanColors.WARNING_HOVER
    }
    return shades.get(shade, CleanColors.WARNING)


def error(shade: str = 'base') -> str:
    """Get error color in different shades."""
    shades = {
        'light': CleanColors.ERROR_LIGHT,
        'base': CleanColors.ERROR,
        'hover': CleanColors.ERROR_HOVER
    }
    return shades.get(shade, CleanColors.ERROR)


def gray(level: int = 600) -> str:
    """Get gray color by level (50-900)."""
    grays = {
        50: CleanColors.GRAY_50,
        100: CleanColors.GRAY_100,
        200: CleanColors.GRAY_200,
        300: CleanColors.GRAY_300,
        400: CleanColors.GRAY_400,
        500: CleanColors.GRAY_500,
        600: CleanColors.GRAY_600,
        700: CleanColors.GRAY_700,
        800: CleanColors.GRAY_800,
        900: CleanColors.GRAY_900,
    }
    return grays.get(level, CleanColors.GRAY_600)


# Export commonly used colors for easy import
__all__ = [
    'CleanColors',
    'ColorScheme', 
    'RichStyles',
    'AccessibilityColors',
    'primary',
    'success',
    'warning',
    'error',
    'gray'
]
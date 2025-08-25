"""
Source package for Spanish Subjunctive Practice App
"""

# Export main accessibility functions for easy import
from .accessibility_integration import integrate_accessibility, add_accessibility_startup_check

__all__ = ['integrate_accessibility', 'add_accessibility_startup_check']
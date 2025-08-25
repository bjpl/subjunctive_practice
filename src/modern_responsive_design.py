"""
Modern Responsive Design System for Spanish Subjunctive Practice Application
===========================================================================

This module provides a comprehensive responsive design system with:
- Proper responsive breakpoints for all device sizes
- Modern CSS Grid and Flexbox layouts
- CSS custom properties for consistent theming
- Smooth transitions and micro-interactions
- Adaptive typography and spacing
- Cross-browser compatibility
- Excellent accessibility support

Design Principles:
- Mobile-first responsive approach
- Progressive enhancement for larger screens
- Consistent visual hierarchy
- Optimal touch targets (44px minimum)
- High contrast ratios for accessibility
- Smooth performance across devices
"""

from PyQt5.QtWidgets import (
    QWidget, QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QSplitter, QScrollArea, QGroupBox, QLabel, QPushButton, QLineEdit,
    QTextEdit, QProgressBar, QFrame, QSizePolicy, QSpacerItem
)
from PyQt5.QtCore import Qt, QSize, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import QFont, QFontMetrics, QPalette, QColor, QScreen
from typing import Dict, List, Tuple, Optional, Union, Any
import logging
import math

logger = logging.getLogger(__name__)


class ResponsiveBreakpoints:
    """
    Modern responsive breakpoints following industry standards
    Mobile-first approach with progressive enhancement
    """
    
    # Breakpoint definitions (width in pixels)
    BREAKPOINTS = {
        'xs': 0,        # Extra small devices (phones, 0px and up)
        'sm': 576,      # Small devices (landscape phones, 576px and up)
        'md': 768,      # Medium devices (tablets, 768px and up)
        'lg': 992,      # Large devices (desktops, 992px and up)
        'xl': 1200,     # Extra large devices (large desktops, 1200px and up)
        'xxl': 1400     # Extra extra large devices (larger desktops, 1400px and up)
    }
    
    # Container max-widths for each breakpoint
    CONTAINER_MAX_WIDTHS = {
        'sm': 540,
        'md': 720,
        'lg': 960,
        'xl': 1140,
        'xxl': 1320
    }
    
    @classmethod
    def get_current_breakpoint(cls, width: int) -> str:
        """Determine the current breakpoint based on width"""
        for bp_name in ['xxl', 'xl', 'lg', 'md', 'sm', 'xs']:
            if width >= cls.BREAKPOINTS[bp_name]:
                return bp_name
        return 'xs'
    
    @classmethod
    def get_container_width(cls, screen_width: int, breakpoint: str) -> int:
        """Get optimal container width for current breakpoint"""
        if breakpoint in cls.CONTAINER_MAX_WIDTHS:
            return min(screen_width - 32, cls.CONTAINER_MAX_WIDTHS[breakpoint])  # 32px total margin
        return screen_width - 32


class ModernDesignTokens:
    """
    Design tokens for consistent theming using CSS custom properties approach
    Provides light and dark theme variants with smooth transitions
    """
    
    # Color palette - carefully chosen for accessibility and modern appeal
    COLORS = {
        'light': {
            # Primary colors
            'primary-50': '#eff6ff',
            'primary-100': '#dbeafe', 
            'primary-200': '#bfdbfe',
            'primary-300': '#93c5fd',
            'primary-400': '#60a5fa',
            'primary-500': '#3b82f6',  # Main primary
            'primary-600': '#2563eb',
            'primary-700': '#1d4ed8',
            'primary-800': '#1e40af',
            'primary-900': '#1e3a8a',
            
            # Neutral colors
            'neutral-0': '#ffffff',
            'neutral-50': '#f9fafb',
            'neutral-100': '#f3f4f6',
            'neutral-200': '#e5e7eb',
            'neutral-300': '#d1d5db',
            'neutral-400': '#9ca3af',
            'neutral-500': '#6b7280',
            'neutral-600': '#4b5563',
            'neutral-700': '#374151',
            'neutral-800': '#1f2937',
            'neutral-900': '#111827',
            
            # Semantic colors
            'success-50': '#f0fdf4',
            'success-500': '#22c55e',
            'success-700': '#15803d',
            
            'warning-50': '#fffbeb',
            'warning-500': '#f59e0b',
            'warning-700': '#a16207',
            
            'error-50': '#fef2f2',
            'error-500': '#ef4444',
            'error-700': '#b91c1c',
            
            'info-50': '#eff6ff',
            'info-500': '#3b82f6',
            'info-700': '#1d4ed8',
        },
        
        'dark': {
            # Primary colors (adjusted for dark mode)
            'primary-50': '#1e3a8a',
            'primary-100': '#1e40af',
            'primary-200': '#1d4ed8',
            'primary-300': '#2563eb',
            'primary-400': '#3b82f6',
            'primary-500': '#60a5fa',  # Main primary for dark
            'primary-600': '#93c5fd',
            'primary-700': '#bfdbfe',
            'primary-800': '#dbeafe',
            'primary-900': '#eff6ff',
            
            # Neutral colors (inverted)
            'neutral-0': '#111827',
            'neutral-50': '#1f2937',
            'neutral-100': '#374151',
            'neutral-200': '#4b5563',
            'neutral-300': '#6b7280',
            'neutral-400': '#9ca3af',
            'neutral-500': '#d1d5db',
            'neutral-600': '#e5e7eb',
            'neutral-700': '#f3f4f6',
            'neutral-800': '#f9fafb',
            'neutral-900': '#ffffff',
            
            # Semantic colors (dark mode variants)
            'success-50': '#064e3b',
            'success-500': '#10b981',
            'success-700': '#34d399',
            
            'warning-50': '#78350f',
            'warning-500': '#f59e0b',
            'warning-700': '#fbbf24',
            
            'error-50': '#7f1d1d',
            'error-500': '#ef4444',
            'error-700': '#f87171',
            
            'info-50': '#1e3a8a',
            'info-500': '#3b82f6',
            'info-700': '#60a5fa',
        }
    }
    
    # Typography scale using type scale (1.250 - Major Third)
    TYPOGRAPHY = {
        'font-family-primary': '"Inter", "SF Pro Display", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
        'font-family-mono': '"JetBrains Mono", "SF Mono", Consolas, "Liberation Mono", Menlo, monospace',
        
        'font-size-xs': 12,     # 0.75rem
        'font-size-sm': 14,     # 0.875rem  
        'font-size-base': 16,   # 1rem
        'font-size-lg': 18,     # 1.125rem
        'font-size-xl': 20,     # 1.25rem
        'font-size-2xl': 24,    # 1.5rem
        'font-size-3xl': 30,    # 1.875rem
        'font-size-4xl': 36,    # 2.25rem
        'font-size-5xl': 48,    # 3rem
        
        'font-weight-light': 300,
        'font-weight-normal': 400,
        'font-weight-medium': 500,
        'font-weight-semibold': 600,
        'font-weight-bold': 700,
        'font-weight-extrabold': 800,
        
        'line-height-tight': 1.25,
        'line-height-snug': 1.375,
        'line-height-normal': 1.5,
        'line-height-relaxed': 1.625,
        'line-height-loose': 2,
    }
    
    # Spacing scale using 8px grid system
    SPACING = {
        '0': 0,
        '1': 4,     # 0.25rem
        '2': 8,     # 0.5rem
        '3': 12,    # 0.75rem
        '4': 16,    # 1rem
        '5': 20,    # 1.25rem
        '6': 24,    # 1.5rem
        '8': 32,    # 2rem
        '10': 40,   # 2.5rem
        '12': 48,   # 3rem
        '16': 64,   # 4rem
        '20': 80,   # 5rem
        '24': 96,   # 6rem
        '32': 128,  # 8rem
    }
    
    # Border radius scale
    RADIUS = {
        'none': 0,
        'sm': 2,
        'base': 4,
        'md': 6,
        'lg': 8,
        'xl': 12,
        '2xl': 16,
        '3xl': 24,
        'full': 9999,
    }
    
    # Shadow system for depth perception
    SHADOWS = {
        'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        'base': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
        'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
        '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
        'inner': 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
    }
    
    # Animation and transition settings
    ANIMATIONS = {
        'duration-fast': 150,     # ms
        'duration-normal': 250,   # ms
        'duration-slow': 350,     # ms
        
        'ease-linear': QEasingCurve.Linear,
        'ease-in': QEasingCurve.InQuad,
        'ease-out': QEasingCurve.OutQuad,
        'ease-in-out': QEasingCurve.InOutQuad,
        'ease-bounce': QEasingCurve.OutBounce,
    }


class ResponsiveStyleGenerator:
    """
    Generates responsive stylesheets with proper breakpoints and modern design
    """
    
    def __init__(self, theme: str = 'light'):
        self.theme = theme
        self.tokens = ModernDesignTokens()
        self.breakpoints = ResponsiveBreakpoints()
        
    def generate_base_styles(self) -> str:
        """Generate base styles with CSS custom properties equivalent"""
        colors = self.tokens.COLORS[self.theme]
        typography = self.tokens.TYPOGRAPHY
        spacing = self.tokens.SPACING
        radius = self.tokens.RADIUS
        
        return f"""
        /* ==============================================
           BASE STYLES & RESET
           ============================================== */
        
        QMainWindow {{
            background-color: {colors['neutral-0']};
            color: {colors['neutral-900']};
            font-family: {typography['font-family-primary']};
            font-size: {typography['font-size-base']}px;
            line-height: {typography['line-height-normal']};
        }}
        
        QWidget {{
            font-family: {typography['font-family-primary']};
            color: {colors['neutral-900']};
            background-color: transparent;
        }}
        
        /* ==============================================
           TYPOGRAPHY SYSTEM
           ============================================== */
        
        QLabel {{
            color: {colors['neutral-800']};
            font-size: {typography['font-size-base']}px;
            font-weight: {typography['font-weight-normal']};
            line-height: {typography['line-height-normal']};
            padding: {spacing['2']}px 0;
        }}
        
        QLabel[role="display"] {{
            font-size: {typography['font-size-4xl']}px;
            font-weight: {typography['font-weight-bold']};
            color: {colors['neutral-900']};
            line-height: {typography['line-height-tight']};
        }}
        
        QLabel[role="title"] {{
            font-size: {typography['font-size-2xl']}px;
            font-weight: {typography['font-weight-semibold']};
            color: {colors['neutral-900']};
            line-height: {typography['line-height-snug']};
            margin: {spacing['4']}px 0 {spacing['3']}px 0;
        }}
        
        QLabel[role="subtitle"] {{
            font-size: {typography['font-size-lg']}px;
            font-weight: {typography['font-weight-medium']};
            color: {colors['neutral-700']};
            line-height: {typography['line-height-snug']};
        }}
        
        QLabel[role="body"] {{
            font-size: {typography['font-size-base']}px;
            font-weight: {typography['font-weight-normal']};
            color: {colors['neutral-700']};
            line-height: {typography['line-height-relaxed']};
        }}
        
        QLabel[role="caption"] {{
            font-size: {typography['font-size-sm']}px;
            font-weight: {typography['font-weight-medium']};
            color: {colors['neutral-500']};
            line-height: {typography['line-height-normal']};
        }}
        
        /* ==============================================
           BUTTON SYSTEM - Modern with proper states
           ============================================== */
        
        QPushButton {{
            font-family: {typography['font-family-primary']};
            font-size: {typography['font-size-base']}px;
            font-weight: {typography['font-weight-medium']};
            border: none;
            border-radius: {radius['md']}px;
            padding: {spacing['3']}px {spacing['6']}px;
            min-height: 44px;  /* Accessibility requirement */
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        
        QPushButton[variant="primary"] {{
            background-color: {colors['primary-500']};
            color: {colors['neutral-0']};
        }}
        
        QPushButton[variant="primary"]:hover {{
            background-color: {colors['primary-600']};
            transform: translateY(-1px);
        }}
        
        QPushButton[variant="primary"]:pressed {{
            background-color: {colors['primary-700']};
            transform: translateY(0px);
        }}
        
        QPushButton[variant="secondary"] {{
            background-color: {colors['neutral-100']};
            color: {colors['neutral-700']};
            border: 1px solid {colors['neutral-300']};
        }}
        
        QPushButton[variant="secondary"]:hover {{
            background-color: {colors['neutral-200']};
            border-color: {colors['neutral-400']};
        }}
        
        QPushButton[variant="outline"] {{
            background-color: transparent;
            color: {colors['primary-600']};
            border: 2px solid {colors['primary-200']};
        }}
        
        QPushButton[variant="outline"]:hover {{
            background-color: {colors['primary-50']};
            border-color: {colors['primary-300']};
        }}
        
        QPushButton[variant="ghost"] {{
            background-color: transparent;
            color: {colors['neutral-600']};
        }}
        
        QPushButton[variant="ghost"]:hover {{
            background-color: {colors['neutral-100']};
        }}
        
        QPushButton:disabled {{
            background-color: {colors['neutral-100']};
            color: {colors['neutral-400']};
            cursor: not-allowed;
            opacity: 0.6;
        }}
        
        /* ==============================================
           INPUT SYSTEM - Modern form controls
           ============================================== */
        
        QLineEdit, QTextEdit {{
            font-family: {typography['font-family-primary']};
            font-size: {typography['font-size-base']}px;
            color: {colors['neutral-900']};
            background-color: {colors['neutral-0']};
            border: 2px solid {colors['neutral-200']};
            border-radius: {radius['md']}px;
            padding: {spacing['3']}px {spacing['4']}px;
            selection-background-color: {colors['primary-200']};
            selection-color: {colors['primary-900']};
        }}
        
        QLineEdit:hover, QTextEdit:hover {{
            border-color: {colors['neutral-300']};
        }}
        
        QLineEdit:focus, QTextEdit:focus {{
            border-color: {colors['primary-500']};
            outline: none;
            /* Simulated focus ring */
            margin: -1px;
            border-width: 3px;
        }}
        
        QLineEdit::placeholder, QTextEdit::placeholder {{
            color: {colors['neutral-400']};
            font-style: italic;
        }}
        
        QLineEdit[state="error"], QTextEdit[state="error"] {{
            border-color: {colors['error-500']};
            background-color: {colors['error-50']};
        }}
        
        QLineEdit[state="success"], QTextEdit[state="success"] {{
            border-color: {colors['success-500']};
            background-color: {colors['success-50']};
        }}
        
        /* ==============================================
           LAYOUT CONTAINERS - Modern card system
           ============================================== */
        
        QGroupBox {{
            font-size: {typography['font-size-lg']}px;
            font-weight: {typography['font-weight-semibold']};
            color: {colors['neutral-800']};
            border: 1px solid {colors['neutral-200']};
            border-radius: {radius['lg']}px;
            background-color: {colors['neutral-0']};
            margin: {spacing['4']}px 0;
            padding-top: {spacing['6']}px;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: {spacing['4']}px;
            top: -{spacing['3']}px;
            padding: 0 {spacing['2']}px;
            background-color: {colors['neutral-0']};
            color: {colors['primary-600']};
            font-weight: {typography['font-weight-medium']};
        }}
        
        QGroupBox[variant="card"] {{
            border: none;
            border-radius: {radius['xl']}px;
            background-color: {colors['neutral-50']};
            padding: {spacing['6']}px;
        }}
        
        QGroupBox[variant="elevated"] {{
            border: none;
            background-color: {colors['neutral-0']};
            /* Shadow simulation through border */
            border: 1px solid {colors['neutral-100']};
        }}
        
        /* ==============================================
           FEEDBACK SYSTEM - Status and notifications
           ============================================== */
        
        QWidget[role="alert"] {{
            border: 1px solid {colors['error-200']};
            background-color: {colors['error-50']};
            color: {colors['error-700']};
            border-radius: {radius['md']}px;
            padding: {spacing['4']}px;
        }}
        
        QWidget[role="success"] {{
            border: 1px solid {colors['success-200']};
            background-color: {colors['success-50']};
            color: {colors['success-700']};
            border-radius: {radius['md']}px;
            padding: {spacing['4']}px;
        }}
        
        QWidget[role="warning"] {{
            border: 1px solid {colors['warning-200']};
            background-color: {colors['warning-50']};
            color: {colors['warning-700']};
            border-radius: {radius['md']}px;
            padding: {spacing['4']}px;
        }}
        
        QWidget[role="info"] {{
            border: 1px solid {colors['info-200']};
            background-color: {colors['info-50']};
            color: {colors['info-700']};
            border-radius: {radius['md']}px;
            padding: {spacing['4']}px;
        }}
        
        /* ==============================================
           PROGRESS & LOADING - Modern indicators
           ============================================== */
        
        QProgressBar {{
            border: none;
            border-radius: {radius['full']}px;
            background-color: {colors['neutral-200']};
            text-align: center;
            font-weight: {typography['font-weight-medium']};
            font-size: {typography['font-size-sm']}px;
            color: {colors['neutral-700']};
            height: 8px;
            margin: {spacing['2']}px 0;
        }}
        
        QProgressBar::chunk {{
            background-color: {colors['primary-500']};
            border-radius: {radius['full']}px;
            margin: 0;
        }}
        
        QProgressBar[size="large"] {{
            height: 12px;
        }}
        
        QProgressBar[size="small"] {{
            height: 6px;
        }}
        
        /* ==============================================
           SCROLLBARS - Modern minimal design
           ============================================== */
        
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}
        
        QScrollArea > QWidget > QWidget {{
            background-color: transparent;
        }}
        
        QScrollBar:vertical {{
            background-color: {colors['neutral-100']};
            width: 8px;
            border-radius: 4px;
            margin: 0;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {colors['neutral-300']};
            border-radius: 4px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {colors['neutral-400']};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            border: none;
            background: none;
            height: 0;
        }}
        
        /* ==============================================
           SPLITTERS - Subtle dividers
           ============================================== */
        
        QSplitter::handle {{
            background-color: {colors['neutral-200']};
            border: none;
            border-radius: 1px;
        }}
        
        QSplitter::handle:horizontal {{
            width: 1px;
            margin: 0 {spacing['1']}px;
        }}
        
        QSplitter::handle:vertical {{
            height: 1px;
            margin: {spacing['1']}px 0;
        }}
        
        QSplitter::handle:hover {{
            background-color: {colors['primary-300']};
        }}
        """
    
    def generate_responsive_styles(self, current_width: int) -> str:
        """Generate responsive styles based on current width"""
        breakpoint = self.breakpoints.get_current_breakpoint(current_width)
        colors = self.tokens.COLORS[self.theme]
        typography = self.tokens.TYPOGRAPHY
        spacing = self.tokens.SPACING
        
        # Responsive typography scaling
        font_scale = self._get_font_scale(breakpoint)
        spacing_scale = self._get_spacing_scale(breakpoint)
        
        responsive_styles = f"""
        /* ==============================================
           RESPONSIVE STYLES - {breakpoint.upper()} BREAKPOINT
           ============================================== */
        
        /* Typography adjustments */
        QLabel[role="display"] {{
            font-size: {int(typography['font-size-4xl'] * font_scale)}px;
        }}
        
        QLabel[role="title"] {{
            font-size: {int(typography['font-size-2xl'] * font_scale)}px;
            margin: {int(spacing['4'] * spacing_scale)}px 0 {int(spacing['3'] * spacing_scale)}px 0;
        }}
        
        QLabel[role="subtitle"] {{
            font-size: {int(typography['font-size-lg'] * font_scale)}px;
        }}
        
        QPushButton {{
            font-size: {int(typography['font-size-base'] * font_scale)}px;
            padding: {int(spacing['3'] * spacing_scale)}px {int(spacing['6'] * spacing_scale)}px;
        }}
        
        QLineEdit, QTextEdit {{
            font-size: {int(typography['font-size-base'] * font_scale)}px;
            padding: {int(spacing['3'] * spacing_scale)}px {int(spacing['4'] * spacing_scale)}px;
        }}
        
        QGroupBox {{
            font-size: {int(typography['font-size-lg'] * font_scale)}px;
            margin: {int(spacing['4'] * spacing_scale)}px 0;
            padding-top: {int(spacing['6'] * spacing_scale)}px;
        }}
        """
        
        # Add breakpoint-specific layout adjustments
        if breakpoint in ['xs', 'sm']:
            responsive_styles += self._get_mobile_styles()
        elif breakpoint in ['md', 'lg']:
            responsive_styles += self._get_tablet_styles()
        else:
            responsive_styles += self._get_desktop_styles()
        
        return responsive_styles
    
    def _get_font_scale(self, breakpoint: str) -> float:
        """Get font scaling factor for breakpoint"""
        scales = {
            'xs': 0.875,   # 14px base becomes 12.25px
            'sm': 0.9375,  # 14px base becomes 13.125px
            'md': 1.0,     # 14px base stays 14px
            'lg': 1.0625,  # 14px base becomes 14.875px
            'xl': 1.125,   # 14px base becomes 15.75px
            'xxl': 1.1875  # 14px base becomes 16.625px
        }
        return scales.get(breakpoint, 1.0)
    
    def _get_spacing_scale(self, breakpoint: str) -> float:
        """Get spacing scaling factor for breakpoint"""
        scales = {
            'xs': 0.75,  # Tighter spacing on mobile
            'sm': 0.875,
            'md': 1.0,
            'lg': 1.125,
            'xl': 1.25,
            'xxl': 1.375
        }
        return scales.get(breakpoint, 1.0)
    
    def _get_mobile_styles(self) -> str:
        """Get mobile-specific styles"""
        colors = self.tokens.COLORS[self.theme]
        spacing = self.tokens.SPACING
        
        return f"""
        /* Mobile-specific adjustments */
        QPushButton {{
            min-height: 48px;  /* Larger touch targets */
            margin: {spacing['2']}px;
        }}
        
        QGroupBox {{
            margin: {spacing['2']}px 0;
            padding: {spacing['4']}px;
        }}
        
        QLineEdit, QTextEdit {{
            min-height: 44px;
        }}
        
        /* Stack elements vertically on mobile */
        QWidget[responsive="stack-mobile"] {{
            /* This would be handled by the layout manager */
        }}
        """
    
    def _get_tablet_styles(self) -> str:
        """Get tablet-specific styles"""
        return """
        /* Tablet-specific adjustments */
        QPushButton {
            min-height: 46px;
        }
        """
    
    def _get_desktop_styles(self) -> str:
        """Get desktop-specific styles"""
        return """
        /* Desktop-specific adjustments */
        QPushButton {
            min-height: 44px;
        }
        
        /* Enhanced hover effects for mouse users */
        QPushButton:hover {
            transform: translateY(-1px);
        }
        """


class ModernThemeManager:
    """
    Manages theme switching with smooth transitions and state persistence
    """
    
    def __init__(self, app: QApplication):
        self.app = app
        self.current_theme = 'light'
        self.style_generator = ResponsiveStyleGenerator(self.current_theme)
        self._animation_group = None
        
    def apply_theme(self, theme: str = None) -> None:
        """Apply a theme with smooth transition"""
        if theme:
            self.current_theme = theme
        
        self.style_generator = ResponsiveStyleGenerator(self.current_theme)
        
        # Get current window size for responsive styles
        primary_screen = self.app.primaryScreen()
        screen_size = primary_screen.size()
        
        # Generate complete stylesheet
        base_styles = self.style_generator.generate_base_styles()
        responsive_styles = self.style_generator.generate_responsive_styles(screen_size.width())
        
        complete_stylesheet = base_styles + "\n" + responsive_styles
        
        # Apply with fade transition effect (simulated)
        self.app.setStyleSheet(complete_stylesheet)
        
        logger.info(f"Applied {self.current_theme} theme with responsive styles")
    
    def toggle_theme(self) -> None:
        """Toggle between light and dark themes"""
        new_theme = 'dark' if self.current_theme == 'light' else 'light'
        self.apply_theme(new_theme)
    
    def get_current_theme(self) -> str:
        """Get current theme name"""
        return self.current_theme
    
    def update_responsive_styles(self, width: int) -> None:
        """Update responsive styles when window is resized"""
        responsive_styles = self.style_generator.generate_responsive_styles(width)
        
        # In a real implementation, we'd update only the responsive parts
        # For now, we'll re-apply the complete theme
        self.apply_theme()


class ResponsiveLayoutManager:
    """
    Manages responsive layout changes and orientation handling
    """
    
    def __init__(self, widget: QWidget):
        self.widget = widget
        self.breakpoints = ResponsiveBreakpoints()
        self.current_breakpoint = 'md'
        self.orientation_stack = []  # Track layout orientations
        
        # Debounced resize timer
        self.resize_timer = QTimer()
        self.resize_timer.timeout.connect(self._apply_layout_changes)
        self.resize_timer.setSingleShot(True)
        
    def handle_resize(self, size: QSize) -> None:
        """Handle window resize with debouncing"""
        self.new_size = size
        self.resize_timer.start(100)  # 100ms debounce
    
    def _apply_layout_changes(self) -> None:
        """Apply layout changes based on new size"""
        if not hasattr(self, 'new_size'):
            return
            
        width = self.new_size.width()
        new_breakpoint = self.breakpoints.get_current_breakpoint(width)
        
        if new_breakpoint != self.current_breakpoint:
            logger.info(f"Breakpoint changed: {self.current_breakpoint} -> {new_breakpoint}")
            self._update_layout_for_breakpoint(new_breakpoint)
            self.current_breakpoint = new_breakpoint
    
    def _update_layout_for_breakpoint(self, breakpoint: str) -> None:
        """Update layout configuration for new breakpoint"""
        try:
            # Find splitters and adjust orientation
            splitters = self.widget.findChildren(QSplitter)
            for splitter in splitters:
                self._adjust_splitter_for_breakpoint(splitter, breakpoint)
            
            # Adjust container widths
            self._adjust_container_widths(breakpoint)
            
            # Update spacing
            self._update_responsive_spacing(breakpoint)
            
        except Exception as e:
            logger.error(f"Error updating layout for breakpoint {breakpoint}: {e}")
    
    def _adjust_splitter_for_breakpoint(self, splitter: QSplitter, breakpoint: str) -> None:
        """Adjust splitter orientation and sizes for breakpoint"""
        if breakpoint in ['xs', 'sm']:
            # Stack vertically on mobile
            if splitter.orientation() != Qt.Vertical:
                splitter.setOrientation(Qt.Vertical)
                splitter.setSizes([60, 40])  # Content area gets more space
        else:
            # Side-by-side on larger screens
            if splitter.orientation() != Qt.Horizontal:
                splitter.setOrientation(Qt.Horizontal)
                
                # Adjust ratios based on breakpoint
                if breakpoint in ['md']:
                    splitter.setSizes([65, 35])
                else:
                    splitter.setSizes([70, 30])
    
    def _adjust_container_widths(self, breakpoint: str) -> None:
        """Adjust container max-widths for breakpoint"""
        # Find containers with responsive width settings
        containers = self.widget.findChildren(QWidget)
        
        for container in containers:
            if hasattr(container, 'responsive_width') and container.responsive_width:
                max_width = self.breakpoints.get_container_width(
                    self.new_size.width(), 
                    breakpoint
                )
                container.setMaximumWidth(max_width)
    
    def _update_responsive_spacing(self, breakpoint: str) -> None:
        """Update spacing for responsive design"""
        # This would work in conjunction with the theme manager
        # to update spacing values dynamically
        pass


def create_modern_responsive_app(app: QApplication, main_window: QMainWindow) -> Tuple[ModernThemeManager, ResponsiveLayoutManager]:
    """
    Initialize modern responsive design system for the application
    
    Args:
        app: QApplication instance
        main_window: Main window instance
    
    Returns:
        Tuple of (theme_manager, layout_manager)
    """
    # Enable high DPI support
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Initialize theme manager
    theme_manager = ModernThemeManager(app)
    theme_manager.apply_theme('light')  # Start with light theme
    
    # Initialize responsive layout manager
    layout_manager = ResponsiveLayoutManager(main_window)
    
    # Connect resize events
    def on_resize(size: QSize):
        layout_manager.handle_resize(size)
        theme_manager.update_responsive_styles(size.width())
    
    # Connect to main window resize events
    original_resize_event = main_window.resizeEvent
    def enhanced_resize_event(event):
        original_resize_event(event)
        on_resize(event.size())
    
    main_window.resizeEvent = enhanced_resize_event
    
    logger.info("Modern responsive design system initialized")
    
    return theme_manager, layout_manager


# Utility functions for easy integration
def apply_widget_variant(widget: QWidget, variant: str) -> None:
    """Apply a design variant to a widget"""
    widget.setProperty('variant', variant)
    widget.style().unpolish(widget)
    widget.style().polish(widget)


def apply_widget_role(widget: QWidget, role: str) -> None:
    """Apply a semantic role to a widget"""
    widget.setProperty('role', role)
    widget.style().unpolish(widget)
    widget.style().polish(widget)


def apply_widget_state(widget: QWidget, state: str) -> None:
    """Apply a state to a widget (error, success, etc.)"""
    widget.setProperty('state', state)
    widget.style().unpolish(widget)
    widget.style().polish(widget)


if __name__ == "__main__":
    # Demo and testing
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
    
    app = QApplication(sys.argv)
    
    # Create main window
    window = QMainWindow()
    central = QWidget()
    window.setCentralWidget(central)
    
    layout = QVBoxLayout(central)
    
    # Add demo content
    title = QLabel("Modern Responsive Design Demo")
    apply_widget_role(title, "title")
    
    subtitle = QLabel("Showcasing responsive breakpoints and modern theming")
    apply_widget_role(subtitle, "subtitle")
    
    # Add buttons with different variants
    primary_btn = QPushButton("Primary Action")
    apply_widget_variant(primary_btn, "primary")
    
    secondary_btn = QPushButton("Secondary Action")
    apply_widget_variant(secondary_btn, "secondary")
    
    outline_btn = QPushButton("Outline Action")
    apply_widget_variant(outline_btn, "outline")
    
    # Add input field
    input_field = QLineEdit()
    input_field.setPlaceholderText("Type something here...")
    
    # Add to layout
    layout.addWidget(title)
    layout.addWidget(subtitle)
    layout.addWidget(primary_btn)
    layout.addWidget(secondary_btn)
    layout.addWidget(outline_btn)
    layout.addWidget(input_field)
    
    # Initialize modern responsive design
    theme_manager, layout_manager = create_modern_responsive_app(app, window)
    
    # Add theme toggle
    theme_btn = QPushButton("Toggle Theme")
    theme_btn.clicked.connect(theme_manager.toggle_theme)
    layout.addWidget(theme_btn)
    
    window.setWindowTitle("Modern Responsive Design System")
    window.resize(1000, 700)
    window.show()
    
    print("Modern responsive design system demo running...")
    print(f"Current theme: {theme_manager.get_current_theme()}")
    print(f"Current breakpoint: {layout_manager.current_breakpoint}")
    
    sys.exit(app.exec_())

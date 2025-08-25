"""
Enhanced Typography and Sizing System for Spanish Subjunctive Practice App

This module provides a comprehensive solution to fix small text and element sizing issues
by implementing a proper typographic scale, ensuring minimum readable font sizes,
creating proper touch/click targets, and adding responsive font sizing.

Key Features:
- Minimum 16px base font size for optimal readability
- Proper touch target sizes (44x44px minimum) for all interactive elements
- Responsive font scaling using CSS calc() and viewport units
- Enhanced line height (1.5-1.6) for better readability
- Consistent typographic hierarchy with proper size ratios
- Accessibility-compliant sizing at all zoom levels
- High DPI and multi-monitor support

Author: Enhanced Typography System v2.0
"""

import sys
import logging
from typing import Dict, Tuple, Optional, Union, List
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit, 
    QTextEdit, QGroupBox, QScrollArea, QComboBox, QCheckBox,
    QRadioButton, QProgressBar, QSlider, QSpinBox
)
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QFontMetrics, QFontInfo, QScreen, QPalette

logger = logging.getLogger(__name__)


class AccessibleTypographyConfig:
    """
    Typography configuration specifically optimized for accessibility and readability.
    Focuses on minimum sizes, optimal ratios, and clear visual hierarchy.
    """
    
    # Base font sizes (in pixels) - Accessibility-compliant minimums
    BASE_SIZES = {
        'caption': 14,      # Small text - minimum readable size
        'body': 16,         # Primary text - recommended accessibility baseline
        'body_large': 18,   # Comfortable reading size
        'subtitle': 20,     # Secondary headings
        'title': 24,        # Primary headings
        'display': 28,      # Large display text
        'hero': 32          # Extra large text
    }
    
    # Touch target sizes (minimum 44x44px for accessibility)
    TOUCH_TARGETS = {
        'minimum': 44,      # Absolute minimum for touch
        'comfortable': 48,  # More comfortable touch target
        'large': 56,        # Large touch target for important actions
        'extra_large': 64   # Extra large for primary actions
    }
    
    # Line height ratios optimized for Spanish text with accents
    LINE_HEIGHTS = {
        'tight': 1.3,       # For headings and titles
        'normal': 1.5,      # Standard body text
        'comfortable': 1.6, # Extended reading
        'loose': 1.8        # Maximum comfort for learning
    }
    
    # Letter spacing for improved readability
    LETTER_SPACING = {
        'tight': -0.025,    # Slight tightening for large text
        'normal': 0,        # Default spacing
        'comfortable': 0.025, # Slight opening for better reading
        'loose': 0.05       # Open spacing for emphasis
    }
    
    # Font weights for clear hierarchy
    FONT_WEIGHTS = {
        'light': 300,
        'regular': 400,
        'medium': 500,
        'semibold': 600,
        'bold': 700
    }
    
    # Spacing scale based on 8px grid system
    SPACING_SCALE = {
        'xs': 4,
        'sm': 8,
        'md': 16,
        'lg': 24,
        'xl': 32,
        'xxl': 40,
        'xxxl': 48
    }
    
    # High contrast color pairs for accessibility
    ACCESSIBLE_COLORS = {
        # Light theme colors with WCAG AA+ compliance
        'light_primary_text': '#1a1a1a',      # 4.5:1 contrast minimum
        'light_secondary_text': '#4a4a4a',    # 3:1 contrast for large text
        'light_background': '#ffffff',
        'light_surface': '#f8f9fa',
        'light_border': '#d1d5db',
        'light_focus': '#2563eb',
        
        # Dark theme colors
        'dark_primary_text': '#f9fafb',
        'dark_secondary_text': '#d1d5db',
        'dark_background': '#111827',
        'dark_surface': '#1f2937',
        'dark_border': '#374151',
        'dark_focus': '#60a5fa'
    }


class ResponsiveFontScaler:
    """
    Handles responsive font scaling based on screen size, DPI, and user preferences.
    Uses viewport-relative units and CSS calc() functions where possible.
    """
    
    def __init__(self):
        self.app = QApplication.instance()
        self.primary_screen = self.app.primaryScreen() if self.app else None
        self.base_dpi = 96
        self.user_scale_factor = 1.0
        
    def get_screen_metrics(self) -> Dict[str, Union[int, float]]:
        """Get comprehensive screen metrics for responsive calculations."""
        if not self.primary_screen:
            return {
                'width': 1920, 'height': 1080, 'dpi': 96,
                'diagonal_inches': 24.0, 'pixel_density': 'standard'
            }
        
        geometry = self.primary_screen.geometry()
        dpi = self.primary_screen.logicalDotsPerInch()
        
        # Calculate screen diagonal
        width_inches = geometry.width() / dpi
        height_inches = geometry.height() / dpi
        diagonal_inches = (width_inches**2 + height_inches**2)**0.5
        
        # Determine pixel density category
        if dpi >= 192:
            pixel_density = 'very_high'
        elif dpi >= 144:
            pixel_density = 'high'
        elif dpi >= 120:
            pixel_density = 'medium_high'
        else:
            pixel_density = 'standard'
        
        return {
            'width': geometry.width(),
            'height': geometry.height(),
            'dpi': dpi,
            'diagonal_inches': diagonal_inches,
            'pixel_density': pixel_density,
            'scale_factor': dpi / self.base_dpi
        }
    
    def calculate_responsive_scale_factor(self) -> float:
        """
        Calculate optimal scale factor considering:
        - Screen size and resolution
        - System DPI scaling
        - User accessibility preferences
        """
        metrics = self.get_screen_metrics()
        
        # Base DPI scaling
        dpi_scale = max(1.0, metrics['scale_factor'])
        
        # Screen size adjustment
        diagonal = metrics['diagonal_inches']
        if diagonal < 13:  # Small screens (tablets, small laptops)
            size_scale = 1.1
        elif diagonal > 27:  # Large screens (desktop monitors)
            size_scale = 1.05
        else:  # Standard screens (13-27 inches)
            size_scale = 1.0
        
        # Resolution density adjustment
        if metrics['pixel_density'] == 'very_high':
            density_scale = 1.0  # Already high resolution
        elif metrics['pixel_density'] == 'high':
            density_scale = 1.0
        elif metrics['pixel_density'] == 'medium_high':
            density_scale = 1.02
        else:  # standard
            density_scale = 1.05
        
        # Combine all scaling factors
        total_scale = dpi_scale * size_scale * density_scale * self.user_scale_factor
        
        # Clamp to reasonable limits
        return max(0.8, min(3.0, total_scale))
    
    def get_scaled_font_size(self, base_size: int) -> int:
        """Get DPI and preference-scaled font size."""
        scale_factor = self.calculate_responsive_scale_factor()
        scaled_size = int(base_size * scale_factor)
        
        # Ensure minimum sizes for accessibility
        if base_size <= 14:  # Caption/small text
            scaled_size = max(14, scaled_size)
        elif base_size <= 16:  # Body text
            scaled_size = max(16, scaled_size)
        else:  # Headings and larger text
            scaled_size = max(18, scaled_size)
        
        return scaled_size
    
    def set_user_scale_factor(self, factor: float):
        """Set user preference scale factor (0.5 to 2.0)."""
        self.user_scale_factor = max(0.5, min(2.0, factor))
        logger.info(f"User scale factor set to {self.user_scale_factor}")


class AccessibleTypography:
    """
    Main typography system focused on accessibility, readability, and proper sizing.
    Ensures all text meets WCAG guidelines and provides comfortable reading experience.
    """
    
    def __init__(self):
        self.config = AccessibleTypographyConfig()
        self.scaler = ResponsiveFontScaler()
        self.current_theme = 'light'
        self._font_cache: Dict[str, QFont] = {}
        
    def create_accessible_font(
        self,
        size_key: str = 'body',
        weight: str = 'regular',
        line_height: str = 'normal'
    ) -> QFont:
        """
        Create a font optimized for accessibility and Spanish text.
        
        Args:
            size_key: Size key from BASE_SIZES
            weight: Weight key from FONT_WEIGHTS  
            line_height: Line height key from LINE_HEIGHTS
            
        Returns:
            Properly configured QFont object
        """
        cache_key = f"{size_key}_{weight}_{line_height}"
        
        if cache_key in self._font_cache:
            return self._font_cache[cache_key]
        
        # Get base size and scale it properly
        base_size = self.config.BASE_SIZES.get(size_key, self.config.BASE_SIZES['body'])
        scaled_size = self.scaler.get_scaled_font_size(base_size)
        
        # Font family selection optimized for Spanish and accessibility
        font_families = [
            'Segoe UI',      # Windows 10/11 - excellent readability
            'San Francisco',  # macOS - highly readable
            'Ubuntu',        # Linux - designed for clarity
            'Roboto',        # Android/Google - optimized for screens
            'Arial',         # Universal fallback
            'Helvetica',     # Alternative fallback
            'sans-serif'     # System fallback
        ]
        
        # Create font with proper settings
        font = QFont()
        
        # Try font families in order of preference
        for family in font_families:
            font.setFamily(family)
            if QFontInfo(font).family() == family:
                break
        
        # Configure font properties
        font.setPixelSize(scaled_size)  # Use pixel size for consistency
        font.setWeight(self.config.FONT_WEIGHTS.get(weight, self.config.FONT_WEIGHTS['regular']))
        
        # Optimize for screen rendering
        font.setHintingPreference(QFont.PreferDefaultHinting)
        font.setStyleStrategy(QFont.PreferAntialias | QFont.PreferQuality)
        
        # Cache and return
        self._font_cache[cache_key] = font
        return font
    
    def get_line_height_pixels(self, size_key: str, line_height_key: str = 'normal') -> int:
        """Calculate line height in pixels for given font size."""
        base_size = self.config.BASE_SIZES.get(size_key, self.config.BASE_SIZES['body'])
        scaled_size = self.scaler.get_scaled_font_size(base_size)
        line_height_ratio = self.config.LINE_HEIGHTS.get(line_height_key, self.config.LINE_HEIGHTS['normal'])
        
        return int(scaled_size * line_height_ratio)
    
    def create_accessible_stylesheet(self, theme: str = 'light') -> str:
        """
        Create comprehensive stylesheet with accessibility-compliant sizing.
        
        Args:
            theme: 'light' or 'dark' theme
            
        Returns:
            Complete CSS stylesheet string
        """
        colors = self._get_theme_colors(theme)
        
        # Calculate responsive font sizes
        caption_size = self.scaler.get_scaled_font_size(self.config.BASE_SIZES['caption'])
        body_size = self.scaler.get_scaled_font_size(self.config.BASE_SIZES['body'])
        body_large_size = self.scaler.get_scaled_font_size(self.config.BASE_SIZES['body_large'])
        subtitle_size = self.scaler.get_scaled_font_size(self.config.BASE_SIZES['subtitle'])
        title_size = self.scaler.get_scaled_font_size(self.config.BASE_SIZES['title'])
        
        # Calculate touch target sizes
        min_touch = self.config.TOUCH_TARGETS['minimum']
        comfortable_touch = self.config.TOUCH_TARGETS['comfortable']
        large_touch = self.config.TOUCH_TARGETS['large']
        
        return f"""
        /* ========================================
           ACCESSIBLE TYPOGRAPHY SYSTEM v2.0
           Base font sizes optimized for readability
           Touch targets meet WCAG guidelines
           ======================================== */
        
        * {{
            box-sizing: border-box;
        }}
        
        /* Base application styles */
        QMainWindow, QWidget {{
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            font-size: {body_size}px;
            line-height: {self.get_line_height_pixels('body', 'normal')}px;
            color: {colors['primary_text']};
            background-color: {colors['background']};
        }}
        
        /* ========================================
           TEXT ELEMENTS - Proper sizing hierarchy
           ======================================== */
        
        /* Primary content text - Spanish sentences */
        QLabel[role="exercise"], QLabel[role="sentence"] {{
            font-size: {body_large_size}px;
            line-height: {self.get_line_height_pixels('body_large', 'comfortable')}px;
            font-weight: {self.config.FONT_WEIGHTS['regular']};
            color: {colors['primary_text']};
            padding: {self.config.SPACING_SCALE['md']}px;
            margin: {self.config.SPACING_SCALE['sm']}px 0;
            letter-spacing: {self.config.LETTER_SPACING['comfortable']}em;
        }}
        
        /* Translation text - clear but secondary */
        QLabel[role="translation"] {{
            font-size: {body_size}px;
            line-height: {self.get_line_height_pixels('body', 'normal')}px;
            font-weight: {self.config.FONT_WEIGHTS['regular']};
            color: {colors['secondary_text']};
            font-style: italic;
            padding: {self.config.SPACING_SCALE['sm']}px;
            margin: {self.config.SPACING_SCALE['xs']}px 0;
        }}
        
        /* Body text - comfortable reading */
        QLabel {{
            font-size: {body_size}px;
            line-height: {self.get_line_height_pixels('body', 'normal')}px;
            font-weight: {self.config.FONT_WEIGHTS['regular']};
            color: {colors['primary_text']};
            padding: {self.config.SPACING_SCALE['xs']}px 0;
        }}
        
        /* Headings with proper hierarchy */
        QLabel[role="title"], QGroupBox::title {{
            font-size: {title_size}px;
            line-height: {self.get_line_height_pixels('title', 'tight')}px;
            font-weight: {self.config.FONT_WEIGHTS['semibold']};
            color: {colors['primary_text']};
            margin: {self.config.SPACING_SCALE['lg']}px 0 {self.config.SPACING_SCALE['md']}px 0;
        }}
        
        QLabel[role="subtitle"] {{
            font-size: {subtitle_size}px;
            line-height: {self.get_line_height_pixels('subtitle', 'normal')}px;
            font-weight: {self.config.FONT_WEIGHTS['medium']};
            color: {colors['primary_text']};
            margin: {self.config.SPACING_SCALE['md']}px 0 {self.config.SPACING_SCALE['sm']}px 0;
        }}
        
        /* Caption and small text - minimum readable size */
        QLabel[role="caption"], QLabel[role="hint"] {{
            font-size: {caption_size}px;
            line-height: {self.get_line_height_pixels('caption', 'normal')}px;
            font-weight: {self.config.FONT_WEIGHTS['regular']};
            color: {colors['secondary_text']};
        }}
        
        /* ========================================
           INTERACTIVE ELEMENTS - Proper touch targets
           ======================================== */
        
        /* Primary buttons - large touch targets */
        QPushButton {{
            font-size: {body_size}px;
            font-weight: {self.config.FONT_WEIGHTS['medium']};
            color: white;
            background-color: {colors['focus']};
            border: none;
            border-radius: 6px;
            padding: {self.config.SPACING_SCALE['md']}px {self.config.SPACING_SCALE['lg']}px;
            margin: {self.config.SPACING_SCALE['xs']}px;
            min-height: {min_touch}px;
            min-width: {comfortable_touch * 2}px;
        }}
        
        QPushButton[role="primary"] {{
            min-height: {comfortable_touch}px;
            font-size: {body_size + 1}px;
            font-weight: {self.config.FONT_WEIGHTS['semibold']};
            padding: {self.config.SPACING_SCALE['lg']}px {self.config.SPACING_SCALE['xl']}px;
        }}
        
        QPushButton[role="large"] {{
            min-height: {large_touch}px;
            font-size: {body_large_size}px;
            padding: {self.config.SPACING_SCALE['xl']}px {self.config.SPACING_SCALE['xxl']}px;
        }}
        
        QPushButton:hover {{
            background-color: {colors['focus']}dd;
            transform: translateY(-1px);
        }}
        
        QPushButton:pressed {{
            background-color: {colors['focus']}bb;
            transform: translateY(0);
        }}
        
        QPushButton:disabled {{
            background-color: {colors['border']};
            color: {colors['secondary_text']};
        }}
        
        /* Input fields - comfortable sizing */
        QLineEdit, QTextEdit {{
            font-size: {body_size}px;
            line-height: {self.get_line_height_pixels('body', 'normal')}px;
            color: {colors['primary_text']};
            background-color: {colors['surface']};
            border: 2px solid {colors['border']};
            border-radius: 4px;
            padding: {self.config.SPACING_SCALE['md']}px;
            margin: {self.config.SPACING_SCALE['xs']}px 0;
            min-height: {min_touch}px;
        }}
        
        QLineEdit:focus, QTextEdit:focus {{
            border-color: {colors['focus']};
            outline: 2px solid {colors['focus']}33;
        }}
        
        /* Dropdown menus - accessible sizing */
        QComboBox {{
            font-size: {body_size}px;
            color: {colors['primary_text']};
            background-color: {colors['surface']};
            border: 2px solid {colors['border']};
            border-radius: 4px;
            padding: {self.config.SPACING_SCALE['md']}px;
            min-height: {min_touch}px;
            min-width: {comfortable_touch * 3}px;
        }}
        
        QComboBox:focus {{
            border-color: {colors['focus']};
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: {min_touch}px;
        }}
        
        /* Checkboxes and radio buttons - large touch targets */
        QCheckBox, QRadioButton {{
            font-size: {body_size}px;
            color: {colors['primary_text']};
            spacing: {self.config.SPACING_SCALE['md']}px;
            margin: {self.config.SPACING_SCALE['sm']}px;
        }}
        
        QCheckBox::indicator, QRadioButton::indicator {{
            width: 20px;
            height: 20px;
            border: 2px solid {colors['border']};
            background-color: {colors['surface']};
        }}
        
        QCheckBox::indicator:checked, QRadioButton::indicator:checked {{
            background-color: {colors['focus']};
            border-color: {colors['focus']};
        }}
        
        /* ========================================
           CONTAINERS - Proper spacing and grouping
           ======================================== */
        
        QGroupBox {{
            font-size: {body_size}px;
            font-weight: {self.config.FONT_WEIGHTS['medium']};
            color: {colors['primary_text']};
            background-color: {colors['surface']};
            border: 2px solid {colors['border']};
            border-radius: 8px;
            margin: {self.config.SPACING_SCALE['lg']}px {self.config.SPACING_SCALE['sm']}px;
            padding-top: {self.config.SPACING_SCALE['xl']}px;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: {self.config.SPACING_SCALE['md']}px;
            padding: 0 {self.config.SPACING_SCALE['sm']}px;
            color: {colors['focus']};
            background-color: {colors['surface']};
        }}
        
        /* Scroll areas */
        QScrollArea {{
            border: 1px solid {colors['border']};
            background-color: {colors['surface']};
            padding: {self.config.SPACING_SCALE['sm']}px;
        }}
        
        /* Progress bars */
        QProgressBar {{
            font-size: {body_size}px;
            font-weight: {self.config.FONT_WEIGHTS['medium']};
            color: {colors['primary_text']};
            background-color: {colors['surface']};
            border: 2px solid {colors['border']};
            border-radius: 4px;
            text-align: center;
            min-height: {self.config.SPACING_SCALE['lg']}px;
        }}
        
        QProgressBar::chunk {{
            background-color: {colors['focus']};
            border-radius: 2px;
        }}
        
        /* ========================================
           ACCESSIBILITY ENHANCEMENTS
           ======================================== */
        
        /* Focus indicators - high contrast */
        *:focus {{
            outline: 2px solid {colors['focus']};
            outline-offset: 2px;
        }}
        
        /* High contrast mode support */
        @media (prefers-contrast: high) {{
            * {{
                border-width: 3px !important;
            }}
            
            QPushButton {{
                border: 2px solid {colors['primary_text']} !important;
            }}
        }}
        
        /* Large text mode support */
        @media (min-resolution: 192dpi) {{
            * {{
                font-size: calc(var(--font-size) * 1.1);
            }}
        }}
        """
    
    def _get_theme_colors(self, theme: str) -> Dict[str, str]:
        """Get color palette for specified theme."""
        if theme == 'dark':
            return {
                'primary_text': self.config.ACCESSIBLE_COLORS['dark_primary_text'],
                'secondary_text': self.config.ACCESSIBLE_COLORS['dark_secondary_text'],
                'background': self.config.ACCESSIBLE_COLORS['dark_background'],
                'surface': self.config.ACCESSIBLE_COLORS['dark_surface'],
                'border': self.config.ACCESSIBLE_COLORS['dark_border'],
                'focus': self.config.ACCESSIBLE_COLORS['dark_focus']
            }
        else:  # light theme
            return {
                'primary_text': self.config.ACCESSIBLE_COLORS['light_primary_text'],
                'secondary_text': self.config.ACCESSIBLE_COLORS['light_secondary_text'],
                'background': self.config.ACCESSIBLE_COLORS['light_background'],
                'surface': self.config.ACCESSIBLE_COLORS['light_surface'],
                'border': self.config.ACCESSIBLE_COLORS['light_border'],
                'focus': self.config.ACCESSIBLE_COLORS['light_focus']
            }
    
    def set_user_font_scale(self, scale: float):
        """Set user font scale preference (0.5 to 2.0)."""
        self.scaler.set_user_scale_factor(scale)
        self._font_cache.clear()  # Clear cache to force recalculation


class AccessibleElementEnhancer:
    """
    Enhances individual UI elements for better accessibility and sizing.
    """
    
    def __init__(self, typography: AccessibleTypography):
        self.typography = typography
    
    def enhance_button(self, button: QPushButton, size: str = 'normal') -> None:
        """
        Enhance button with proper sizing and accessibility features.
        
        Args:
            button: QPushButton to enhance
            size: 'small', 'normal', 'large', or 'primary'
        """
        # Set minimum touch target size
        if size == 'large' or size == 'primary':
            button.setMinimumSize(
                self.typography.config.TOUCH_TARGETS['large'],
                self.typography.config.TOUCH_TARGETS['comfortable']
            )
            button.setProperty('role', 'large')
        else:
            button.setMinimumSize(
                self.typography.config.TOUCH_TARGETS['comfortable'],
                self.typography.config.TOUCH_TARGETS['minimum']
            )
        
        # Apply appropriate font
        if size == 'primary':
            font = self.typography.create_accessible_font('body_large', 'semibold')
            button.setProperty('role', 'primary')
        else:
            font = self.typography.create_accessible_font('body', 'medium')
        
        button.setFont(font)
        
        # Ensure text is not clipped
        button.adjustSize()
        
    def enhance_text_element(self, element: Union[QLabel, QTextEdit], role: str = 'body') -> None:
        """
        Enhance text element with proper typography and spacing.
        
        Args:
            element: QLabel or QTextEdit to enhance
            role: 'exercise', 'translation', 'body', 'title', 'subtitle', 'caption'
        """
        # Set semantic role for CSS targeting
        element.setProperty('role', role)
        
        # Apply appropriate font based on role
        if role == 'exercise' or role == 'sentence':
            font = self.typography.create_accessible_font('body_large', 'regular', 'comfortable')
        elif role == 'translation':
            font = self.typography.create_accessible_font('body', 'regular', 'normal')
        elif role == 'title':
            font = self.typography.create_accessible_font('title', 'semibold', 'tight')
        elif role == 'subtitle':
            font = self.typography.create_accessible_font('subtitle', 'medium', 'normal')
        elif role == 'caption' or role == 'hint':
            font = self.typography.create_accessible_font('caption', 'regular', 'normal')
        else:  # body
            font = self.typography.create_accessible_font('body', 'regular', 'normal')
        
        element.setFont(font)
        
        # Enable word wrap for labels
        if isinstance(element, QLabel):
            element.setWordWrap(True)
            element.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        # Adjust size to content
        element.adjustSize()
    
    def enhance_input_element(self, element: Union[QLineEdit, QTextEdit, QComboBox]) -> None:
        """
        Enhance input element with proper sizing and accessibility.
        
        Args:
            element: Input element to enhance
        """
        # Set minimum size for touch accessibility
        element.setMinimumHeight(self.typography.config.TOUCH_TARGETS['minimum'])
        
        # Apply appropriate font
        font = self.typography.create_accessible_font('body', 'regular')
        element.setFont(font)
        
        # Ensure adequate width for comfortable typing
        if isinstance(element, QLineEdit):
            element.setMinimumWidth(200)
        elif isinstance(element, QComboBox):
            element.setMinimumWidth(150)


class AccessibleThemeManager(QObject):
    """
    Manages theme switching and applies accessible typography throughout the application.
    """
    
    theme_changed = pyqtSignal(str)  # Emitted when theme changes
    
    def __init__(self, app: QApplication):
        super().__init__()
        self.app = app
        self.typography = AccessibleTypography()
        self.enhancer = AccessibleElementEnhancer(self.typography)
        self.current_theme = 'light'
        
    def apply_accessible_theme(self, theme: str = 'light') -> None:
        """
        Apply accessible theme to the entire application.
        
        Args:
            theme: 'light' or 'dark'
        """
        stylesheet = self.typography.create_accessible_stylesheet(theme)
        self.app.setStyleSheet(stylesheet)
        self.current_theme = theme
        self.theme_changed.emit(theme)
        
        logger.info(f"Applied accessible {theme} theme with enhanced typography")
    
    def toggle_theme(self) -> str:
        """Toggle between light and dark themes."""
        new_theme = 'dark' if self.current_theme == 'light' else 'light'
        self.apply_accessible_theme(new_theme)
        return new_theme
    
    def set_user_font_scale(self, scale: float) -> None:
        """
        Set user font scale and refresh the theme.
        
        Args:
            scale: Scale factor (0.5 to 2.0)
        """
        self.typography.set_user_font_scale(scale)
        self.apply_accessible_theme(self.current_theme)
        logger.info(f"Font scale set to {scale}")
    
    def enhance_widget(self, widget: QWidget) -> None:
        """
        Enhance a specific widget with accessible typography and sizing.
        
        Args:
            widget: Widget to enhance
        """
        if isinstance(widget, QPushButton):
            self.enhancer.enhance_button(widget)
        elif isinstance(widget, (QLabel, QTextEdit)):
            self.enhancer.enhance_text_element(widget)
        elif isinstance(widget, (QLineEdit, QComboBox)):
            self.enhancer.enhance_input_element(widget)
        
        logger.debug(f"Enhanced {widget.__class__.__name__} with accessible styling")
    
    def enhance_application_window(self, window: QWidget) -> None:
        """
        Comprehensively enhance an application window.
        
        Args:
            window: Main application window
        """
        # Enhance all child widgets
        for child in window.findChildren(QWidget):
            if isinstance(child, (QPushButton, QLabel, QTextEdit, QLineEdit, QComboBox)):
                self.enhance_widget(child)
        
        logger.info("Enhanced entire application window with accessible typography")


# Convenience functions for easy integration
def create_accessible_typography_system(app: QApplication) -> AccessibleThemeManager:
    """
    Create and initialize the accessible typography system.
    
    Args:
        app: QApplication instance
        
    Returns:
        AccessibleThemeManager instance
    """
    return AccessibleThemeManager(app)


def apply_accessibility_fixes_to_spanish_app(main_window) -> AccessibleThemeManager:
    """
    Apply comprehensive accessibility and typography fixes to the Spanish app.
    
    Args:
        main_window: Main application window instance
        
    Returns:
        AccessibleThemeManager for further customization
    """
    app = QApplication.instance()
    theme_manager = create_accessible_typography_system(app)
    
    # Apply accessible theme
    theme_manager.apply_accessible_theme('light')
    
    # Enhance the main window
    theme_manager.enhance_application_window(main_window)
    
    # Set specific roles for Spanish app elements
    if hasattr(main_window, 'sentence_label'):
        main_window.sentence_label.setProperty('role', 'exercise')
        theme_manager.enhancer.enhance_text_element(main_window.sentence_label, 'exercise')
    
    if hasattr(main_window, 'translation_label'):
        main_window.translation_label.setProperty('role', 'translation')
        theme_manager.enhancer.enhance_text_element(main_window.translation_label, 'translation')
    
    if hasattr(main_window, 'submit_button'):
        main_window.submit_button.setProperty('role', 'primary')
        theme_manager.enhancer.enhance_button(main_window.submit_button, 'primary')
    
    logger.info("Applied comprehensive accessibility fixes to Spanish Subjunctive Practice App")
    return theme_manager


if __name__ == "__main__":
    """Demo and testing for the accessible typography system."""
    from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout
    
    app = QApplication(sys.argv)
    
    # Create demo window
    window = QMainWindow()
    window.setWindowTitle("Accessible Typography System Demo")
    window.setGeometry(100, 100, 800, 600)
    
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    layout = QVBoxLayout(central_widget)
    
    # Create typography system
    theme_manager = create_accessible_typography_system(app)
    theme_manager.apply_accessible_theme('light')
    
    # Demo content with different roles
    title = QLabel("Spanish Subjunctive Practice - Accessible Typography")
    title.setProperty('role', 'title')
    layout.addWidget(title)
    
    exercise = QLabel("Es importante que tengas una buena experiencia de lectura.")
    exercise.setProperty('role', 'exercise')
    layout.addWidget(exercise)
    
    translation = QLabel("It's important that you have a good reading experience.")
    translation.setProperty('role', 'translation')
    layout.addWidget(translation)
    
    # Interactive elements
    button_layout = QHBoxLayout()
    
    primary_btn = QPushButton("Primary Action")
    primary_btn.setProperty('role', 'primary')
    
    normal_btn = QPushButton("Normal Action")
    
    large_btn = QPushButton("Large Button")
    large_btn.setProperty('role', 'large')
    
    button_layout.addWidget(primary_btn)
    button_layout.addWidget(normal_btn)
    button_layout.addWidget(large_btn)
    layout.addLayout(button_layout)
    
    # Input elements
    input_field = QLineEdit()
    input_field.setPlaceholderText("Type your Spanish answer here...")
    layout.addWidget(input_field)
    
    # Theme toggle
    theme_btn = QPushButton("Toggle Dark Theme")
    theme_btn.clicked.connect(lambda: theme_manager.toggle_theme())
    layout.addWidget(theme_btn)
    
    # Font scale controls
    scale_layout = QHBoxLayout()
    scale_layout.addWidget(QLabel("Font Scale:"))
    
    for scale, label in [(0.8, "Small"), (1.0, "Normal"), (1.2, "Large"), (1.5, "Extra Large")]:
        scale_btn = QPushButton(label)
        scale_btn.clicked.connect(lambda checked, s=scale: theme_manager.set_user_font_scale(s))
        scale_layout.addWidget(scale_btn)
    
    layout.addLayout(scale_layout)
    
    # Enhance all elements
    theme_manager.enhance_application_window(window)
    
    window.show()
    
    print("Accessible Typography System Demo")
    print("Features demonstrated:")
    print("- Minimum 16px base font size")
    print("- 44px minimum touch targets")
    print("- Proper line height (1.5-1.6)")
    print("- WCAG-compliant color contrast")
    print("- Responsive font scaling")
    print("- Semantic role-based styling")
    
    sys.exit(app.exec_())
"""
Typography System for Spanish Subjunctive Practice App

This module provides a comprehensive typography system optimized for:
- Spanish text with accents and special characters
- Optimal readability at different screen resolutions
- Clear visual hierarchy with proper font weights
- System fonts that work well on Windows
- Responsive font sizing based on display characteristics
- Enhanced text rendering for learning applications

Key Features:
- 14-16px base font sizes for optimal reading
- System font stack prioritizing Windows-native fonts
- Proper line height (1.4-1.6) for Spanish text with accents
- Letter spacing optimization for Spanish characters
- Font weight variations for clear hierarchy
- High DPI and resolution-aware font scaling
- Accessibility-compliant contrast and sizing

Author: Typography System for Enhanced Spanish Learning Experience
Version: 1.0.0
"""

import sys
from typing import Dict, Tuple, Optional, Union
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QFont, QFontMetrics, QFontInfo, QScreen


class SpanishTypographyConfig:
    """
    Configuration class for Spanish-optimized typography settings.
    
    This class contains all typography specifications optimized for Spanish text,
    including proper handling of accented characters and improved readability.
    """
    
    # Font families optimized for Windows and Spanish text
    FONT_FAMILIES = {
        'primary': [
            'Segoe UI',           # Windows 10/11 default - excellent Spanish support
            'Calibri',            # Microsoft Office standard - clean and readable
            'Tahoma',             # Windows classic - great for accents
            'Verdana',            # Web-safe fallback - designed for screen reading
            'Arial',              # Universal fallback
            'sans-serif'          # System fallback
        ],
        'monospace': [
            'Consolas',           # Windows developer font - excellent for code
            'Courier New',        # Classic monospace
            'monospace'           # System fallback
        ],
        'display': [
            'Segoe UI Light',     # For headings and titles
            'Segoe UI Semilight', # Alternative heading font
            'Segoe UI',           # Fallback to primary
            'sans-serif'
        ]
    }
    
    # Base font sizes (in pixels) - optimized for Spanish text readability
    BASE_SIZES = {
        'xs': 11,      # Small annotations, footnotes
        'sm': 12,      # Secondary text, captions
        'base': 14,    # Primary body text - optimal for sustained reading
        'md': 15,      # Comfortable body text
        'lg': 16,      # Large body text - good for accessibility
        'xl': 18,      # Small headings, emphasis
        'xxl': 20,     # Medium headings
        'title': 22,   # Large headings
        'display': 24, # Hero text, main titles
        'hero': 28     # Extra large display text
    }
    
    # Font weights - carefully chosen for hierarchy and readability
    WEIGHTS = {
        'light': 300,      # Light text for large sizes
        'normal': 400,     # Regular body text
        'medium': 500,     # Slightly emphasized text
        'semibold': 600,   # Strong emphasis, headings
        'bold': 700,       # Bold emphasis, important text
        'extrabold': 800   # Extra emphasis (use sparingly)
    }
    
    # Line heights optimized for Spanish text with accents and tildes
    LINE_HEIGHTS = {
        'tight': 1.2,     # Compact text (headings)
        'snug': 1.3,      # Slightly compact
        'normal': 1.4,    # Default - good for Spanish accents
        'relaxed': 1.5,   # Comfortable reading
        'loose': 1.6,     # Very comfortable, good for learning
        'extra_loose': 1.8 # Maximum comfort for extended reading
    }
    
    # Letter spacing (tracking) for Spanish characters
    LETTER_SPACING = {
        'tighter': -0.5,   # Tight spacing
        'tight': -0.25,    # Slightly tight
        'normal': 0,       # Default spacing
        'wide': 0.25,      # Slightly wide - good for learning
        'wider': 0.5,      # Wide spacing for emphasis
        'widest': 1.0      # Maximum spacing for headers
    }
    
    # Color values for text (hex format)
    TEXT_COLORS = {
        # Light theme colors
        'primary_light': '#1a202c',        # Dark gray-blue for primary text
        'secondary_light': '#4a5568',      # Medium gray for secondary text  
        'muted_light': '#718096',          # Light gray for muted text
        'accent_light': '#2b6cb0',         # Blue for accent text
        'success_light': '#2f855a',        # Green for success messages
        'warning_light': '#d69e2e',        # Orange for warnings
        'error_light': '#e53e3e',          # Red for errors
        
        # Dark theme colors
        'primary_dark': '#f7fafc',         # Off-white for primary text
        'secondary_dark': '#e2e8f0',       # Light gray for secondary text
        'muted_dark': '#a0aec0',           # Medium gray for muted text
        'accent_dark': '#63b3ed',          # Light blue for accent text
        'success_dark': '#68d391',         # Light green for success
        'warning_dark': '#fbb000',         # Light orange for warnings
        'error_dark': '#fc8181',           # Light red for errors
    }


class TypographyScaler:
    """
    Handles responsive typography scaling based on screen characteristics.
    
    This class analyzes the display properties and provides appropriate
    scaling factors for optimal typography at different resolutions.
    """
    
    def __init__(self):
        self.app = QApplication.instance()
        self.primary_screen = self.app.primaryScreen() if self.app else None
        self.base_dpi = 96  # Standard DPI baseline
        
    def get_screen_info(self) -> Dict[str, Union[int, float]]:
        """
        Get comprehensive screen information for typography scaling.
        
        Returns:
            Dictionary containing screen metrics
        """
        if not self.primary_screen:
            return {
                'dpi': 96,
                'scale_factor': 1.0,
                'width': 1920,
                'height': 1080,
                'diagonal_inches': 24.0
            }
        
        geometry = self.primary_screen.geometry()
        dpi = self.primary_screen.logicalDotsPerInch()
        
        # Calculate diagonal size in inches
        width_inches = geometry.width() / dpi
        height_inches = geometry.height() / dpi
        diagonal_inches = (width_inches**2 + height_inches**2)**0.5
        
        return {
            'dpi': dpi,
            'scale_factor': dpi / self.base_dpi,
            'width': geometry.width(),
            'height': geometry.height(),
            'diagonal_inches': diagonal_inches
        }
    
    def calculate_font_scale_factor(self) -> float:
        """
        Calculate optimal font scaling factor based on screen characteristics.
        
        Returns:
            Scaling factor for fonts (1.0 = no scaling)
        """
        screen_info = self.get_screen_info()
        
        # Base scaling from DPI
        dpi_scale = max(1.0, screen_info['scale_factor'])
        
        # Additional scaling for very high resolution displays
        if screen_info['width'] >= 2560:  # 4K+ displays
            resolution_scale = 1.1
        elif screen_info['width'] >= 1920:  # Full HD displays
            resolution_scale = 1.0
        else:  # Lower resolution displays
            resolution_scale = 0.95
        
        # Screen size consideration
        diagonal = screen_info['diagonal_inches']
        if diagonal < 13:  # Small screens (laptops)
            size_scale = 1.05
        elif diagonal > 27:  # Large screens
            size_scale = 1.1
        else:  # Standard screens
            size_scale = 1.0
        
        # Combine all scaling factors with reasonable limits
        total_scale = dpi_scale * resolution_scale * size_scale
        return max(0.8, min(2.0, total_scale))  # Clamp between 0.8x and 2.0x
    
    def get_scaled_size(self, base_size: int) -> int:
        """
        Get scaled font size based on screen characteristics.
        
        Args:
            base_size: Base font size in pixels
            
        Returns:
            Scaled font size in pixels
        """
        scale_factor = self.calculate_font_scale_factor()
        return max(8, round(base_size * scale_factor))  # Minimum 8px


class SpanishTypography:
    """
    Main typography system for Spanish text optimization.
    
    This class provides methods to create properly configured fonts
    for Spanish text with optimal readability and accessibility.
    """
    
    def __init__(self):
        self.config = SpanishTypographyConfig()
        self.scaler = TypographyScaler()
        self._font_cache: Dict[str, QFont] = {}
    
    def create_font(
        self, 
        size: str = 'base', 
        weight: str = 'normal',
        family: str = 'primary',
        line_height: str = 'normal',
        letter_spacing: str = 'normal'
    ) -> QFont:
        """
        Create an optimized QFont for Spanish text.
        
        Args:
            size: Size key from BASE_SIZES
            weight: Weight key from WEIGHTS  
            family: Font family key from FONT_FAMILIES
            line_height: Line height key (for reference, not applied to QFont)
            letter_spacing: Letter spacing key (for reference, not applied to QFont)
            
        Returns:
            Configured QFont object
        """
        cache_key = f"{size}_{weight}_{family}_{line_height}_{letter_spacing}"
        
        if cache_key in self._font_cache:
            return self._font_cache[cache_key]
        
        # Get base size and scale it
        base_size = self.config.BASE_SIZES.get(size, self.config.BASE_SIZES['base'])
        scaled_size = self.scaler.get_scaled_size(base_size)
        
        # Get font families
        font_families = self.config.FONT_FAMILIES.get(family, self.config.FONT_FAMILIES['primary'])
        
        # Create font with first available family
        font = QFont()
        for family_name in font_families:
            font.setFamily(family_name)
            if QFontInfo(font).family() == family_name:
                break
        
        # Set font properties
        font.setPointSize(scaled_size)
        font.setWeight(self.config.WEIGHTS.get(weight, self.config.WEIGHTS['normal']))
        
        # Optimize for screen rendering
        font.setHintingPreference(QFont.PreferDefaultHinting)
        font.setStyleStrategy(QFont.PreferAntialias | QFont.PreferQuality)
        
        # Cache the font
        self._font_cache[cache_key] = font
        
        return font
    
    def get_line_height_px(self, size: str = 'base', line_height: str = 'normal') -> int:
        """
        Calculate line height in pixels for a given font size.
        
        Args:
            size: Size key from BASE_SIZES
            line_height: Line height key from LINE_HEIGHTS
            
        Returns:
            Line height in pixels
        """
        base_size = self.config.BASE_SIZES.get(size, self.config.BASE_SIZES['base'])
        scaled_size = self.scaler.get_scaled_size(base_size)
        line_height_multiplier = self.config.LINE_HEIGHTS.get(line_height, self.config.LINE_HEIGHTS['normal'])
        
        return round(scaled_size * line_height_multiplier)
    
    def get_letter_spacing_px(self, letter_spacing: str = 'normal') -> float:
        """
        Get letter spacing value in pixels.
        
        Args:
            letter_spacing: Letter spacing key from LETTER_SPACING
            
        Returns:
            Letter spacing in pixels
        """
        base_spacing = self.config.LETTER_SPACING.get(letter_spacing, self.config.LETTER_SPACING['normal'])
        scale_factor = self.scaler.calculate_font_scale_factor()
        
        return base_spacing * scale_factor
    
    def create_text_style_dict(
        self,
        size: str = 'base',
        weight: str = 'normal', 
        family: str = 'primary',
        line_height: str = 'normal',
        letter_spacing: str = 'normal',
        color: str = 'primary_light'
    ) -> Dict[str, Union[str, int, float]]:
        """
        Create a complete text style dictionary for CSS or styling.
        
        Args:
            size: Size key from BASE_SIZES
            weight: Weight key from WEIGHTS
            family: Font family key from FONT_FAMILIES
            line_height: Line height key from LINE_HEIGHTS
            letter_spacing: Letter spacing key from LETTER_SPACING
            color: Color key from TEXT_COLORS
            
        Returns:
            Dictionary containing all style properties
        """
        font_families = self.config.FONT_FAMILIES.get(family, self.config.FONT_FAMILIES['primary'])
        font_family_str = ', '.join([f'"{f}"' if ' ' in f else f for f in font_families])
        
        base_size = self.config.BASE_SIZES.get(size, self.config.BASE_SIZES['base'])
        scaled_size = self.scaler.get_scaled_size(base_size)
        
        return {
            'font_family': font_family_str,
            'font_size': f'{scaled_size}px',
            'font_weight': self.config.WEIGHTS.get(weight, self.config.WEIGHTS['normal']),
            'line_height': self.config.LINE_HEIGHTS.get(line_height, self.config.LINE_HEIGHTS['normal']),
            'letter_spacing': f"{self.get_letter_spacing_px(letter_spacing)}px",
            'color': self.config.TEXT_COLORS.get(color, self.config.TEXT_COLORS['primary_light']),
            'text_rendering': 'optimizeLegibility',
            '-webkit-font-smoothing': 'antialiased',
            '-moz-osx-font-smoothing': 'grayscale'
        }
    
    def get_qt_stylesheet_rules(
        self,
        selector: str = 'QLabel',
        size: str = 'base',
        weight: str = 'normal',
        family: str = 'primary', 
        line_height: str = 'normal',
        letter_spacing: str = 'normal',
        color: str = 'primary_light'
    ) -> str:
        """
        Generate Qt stylesheet rules for the given typography settings.
        
        Args:
            selector: CSS selector (e.g., 'QLabel', 'QPushButton')
            size: Size key from BASE_SIZES
            weight: Weight key from WEIGHTS
            family: Font family key from FONT_FAMILIES
            line_height: Line height key from LINE_HEIGHTS
            letter_spacing: Letter spacing key from LETTER_SPACING
            color: Color key from TEXT_COLORS
            
        Returns:
            Qt stylesheet string
        """
        style_dict = self.create_text_style_dict(size, weight, family, line_height, letter_spacing, color)
        
        rules = [
            f"font-family: {style_dict['font_family']};",
            f"font-size: {style_dict['font_size']};",
            f"font-weight: {style_dict['font_weight']};",
            f"color: {style_dict['color']};",
        ]
        
        # Add letter-spacing if not normal
        if letter_spacing != 'normal':
            rules.append(f"letter-spacing: {style_dict['letter_spacing']};")
        
        return f"{selector} {{\n    " + "\n    ".join(rules) + "\n}"


class SpanishTextMetrics:
    """
    Utility class for measuring Spanish text dimensions and characteristics.
    
    Provides methods to measure text with proper consideration for
    Spanish accents, tildes, and special characters.
    """
    
    def __init__(self, typography: SpanishTypography):
        self.typography = typography
    
    def measure_text(
        self, 
        text: str, 
        font_size: str = 'base',
        font_weight: str = 'normal',
        max_width: Optional[int] = None
    ) -> Dict[str, int]:
        """
        Measure Spanish text dimensions with proper accent handling.
        
        Args:
            text: Text to measure
            font_size: Size key from BASE_SIZES
            font_weight: Weight key from WEIGHTS
            max_width: Optional maximum width for wrapping
            
        Returns:
            Dictionary with width, height, and line count
        """
        font = self.typography.create_font(font_size, font_weight)
        metrics = QFontMetrics(font)
        
        if max_width:
            # Calculate wrapped text dimensions
            rect = metrics.boundingRect(
                QRect(0, 0, max_width, 0),
                Qt.TextWordWrap,
                text
            )
            line_count = len(text.split('\n')) if '\n' in text else rect.height() // metrics.height()
        else:
            # Single line dimensions
            rect = metrics.boundingRect(text)
            line_count = 1
        
        return {
            'width': rect.width(),
            'height': rect.height(), 
            'line_height': metrics.height(),
            'line_count': line_count,
            'ascent': metrics.ascent(),
            'descent': metrics.descent()
        }
    
    def get_optimal_width(self, text: str, font_size: str = 'base') -> int:
        """
        Calculate optimal width for Spanish text readability.
        
        Spanish text with accents benefits from slightly wider line lengths
        to accommodate the vertical space needed for accent marks.
        
        Args:
            text: Sample text to analyze
            font_size: Font size key
            
        Returns:
            Optimal width in pixels
        """
        font = self.typography.create_font(font_size)
        metrics = QFontMetrics(font)
        
        # Target 50-75 characters per line for optimal readability
        average_char_width = metrics.averageCharWidth()
        optimal_chars = 65  # Sweet spot for Spanish text
        
        return round(average_char_width * optimal_chars)


class TypographyPresets:
    """
    Pre-defined typography presets for common UI elements in the Spanish app.
    
    These presets provide consistent typography for different parts of the
    application interface, optimized for Spanish learning contexts.
    """
    
    def __init__(self, typography: SpanishTypography):
        self.typography = typography
    
    def get_presets(self) -> Dict[str, Dict[str, str]]:
        """
        Get all typography presets for the application.
        
        Returns:
            Dictionary of preset configurations
        """
        return {
            # Main content text
            'body_text': {
                'size': 'base',
                'weight': 'normal',
                'family': 'primary',
                'line_height': 'relaxed',
                'letter_spacing': 'normal'
            },
            
            # Spanish exercise sentences (main content)
            'exercise_text': {
                'size': 'lg',
                'weight': 'normal', 
                'family': 'primary',
                'line_height': 'loose',
                'letter_spacing': 'wide'
            },
            
            # English translations
            'translation_text': {
                'size': 'sm',
                'weight': 'normal',
                'family': 'primary', 
                'line_height': 'normal',
                'letter_spacing': 'normal'
            },
            
            # Headings and section titles
            'heading_large': {
                'size': 'title',
                'weight': 'semibold',
                'family': 'display',
                'line_height': 'tight',
                'letter_spacing': 'normal'
            },
            
            'heading_medium': {
                'size': 'xl',
                'weight': 'semibold',
                'family': 'primary',
                'line_height': 'snug',
                'letter_spacing': 'normal'
            },
            
            'heading_small': {
                'size': 'lg',
                'weight': 'medium',
                'family': 'primary',
                'line_height': 'normal',
                'letter_spacing': 'normal'
            },
            
            # UI labels and secondary text
            'label_text': {
                'size': 'sm',
                'weight': 'medium',
                'family': 'primary',
                'line_height': 'normal',
                'letter_spacing': 'normal'
            },
            
            # Small text (hints, captions)
            'caption_text': {
                'size': 'xs',
                'weight': 'normal',
                'family': 'primary',
                'line_height': 'normal',
                'letter_spacing': 'normal'
            },
            
            # Button text
            'button_text': {
                'size': 'base',
                'weight': 'medium',
                'family': 'primary',
                'line_height': 'tight',
                'letter_spacing': 'wide'
            },
            
            # Input placeholder text
            'placeholder_text': {
                'size': 'base',
                'weight': 'normal',
                'family': 'primary',
                'line_height': 'normal',
                'letter_spacing': 'normal'
            },
            
            # Feedback and explanation text
            'feedback_text': {
                'size': 'base',
                'weight': 'normal',
                'family': 'primary',
                'line_height': 'loose',
                'letter_spacing': 'normal'
            },
            
            # Status and statistics text
            'stats_text': {
                'size': 'sm',
                'weight': 'medium',
                'family': 'monospace',
                'line_height': 'normal',
                'letter_spacing': 'normal'
            },
            
            # Code or conjugation examples
            'code_text': {
                'size': 'sm',
                'weight': 'normal',
                'family': 'monospace',
                'line_height': 'relaxed',
                'letter_spacing': 'normal'
            }
        }
    
    def create_preset_font(self, preset_name: str) -> QFont:
        """
        Create a QFont based on a preset configuration.
        
        Args:
            preset_name: Name of the preset
            
        Returns:
            Configured QFont object
        """
        presets = self.get_presets()
        if preset_name not in presets:
            preset_name = 'body_text'  # Fallback
        
        preset = presets[preset_name]
        return self.typography.create_font(**preset)
    
    def get_preset_stylesheet(self, selector: str, preset_name: str, color: str = 'primary_light') -> str:
        """
        Get Qt stylesheet for a preset.
        
        Args:
            selector: CSS selector
            preset_name: Name of the preset
            color: Color key for text
            
        Returns:
            Qt stylesheet string
        """
        presets = self.get_presets()
        if preset_name not in presets:
            preset_name = 'body_text'  # Fallback
        
        preset = presets[preset_name]
        return self.typography.get_qt_stylesheet_rules(selector, color=color, **preset)


# Convenience functions for easy integration
def create_spanish_typography() -> SpanishTypography:
    """
    Create a Spanish typography instance with optimal defaults.
    
    Returns:
        Configured SpanishTypography instance
    """
    return SpanishTypography()


def get_typography_info() -> Dict[str, Union[str, int, float, Dict]]:
    """
    Get comprehensive typography system information.
    
    Returns:
        Dictionary containing typography system details
    """
    typography = create_spanish_typography()
    scaler = typography.scaler
    screen_info = scaler.get_screen_info()
    scale_factor = scaler.calculate_font_scale_factor()
    
    return {
        'version': '1.0.0',
        'optimized_for': 'Spanish text with accents and special characters',
        'base_font_size': '14-16px for optimal readability',
        'recommended_line_height': '1.4-1.6 for Spanish text',
        'primary_fonts': typography.config.FONT_FAMILIES['primary'],
        'screen_info': screen_info,
        'current_scale_factor': scale_factor,
        'available_sizes': list(typography.config.BASE_SIZES.keys()),
        'available_weights': list(typography.config.WEIGHTS.keys()),
        'available_line_heights': list(typography.config.LINE_HEIGHTS.keys()),
        'available_letter_spacings': list(typography.config.LETTER_SPACING.keys())
    }


def apply_spanish_typography_to_app(app: QApplication) -> SpanishTypography:
    """
    Apply Spanish typography optimizations to the entire application.
    
    Args:
        app: QApplication instance
        
    Returns:
        SpanishTypography instance for further customization
    """
    typography = create_spanish_typography()
    presets = TypographyPresets(typography)
    
    # Create comprehensive stylesheet with Spanish-optimized typography
    base_stylesheet = f"""
        /* Spanish Typography System - Base Styles */
        
        QWidget {{
            {typography.get_qt_stylesheet_rules('', 'base', 'normal', 'primary', 'normal', 'normal', 'primary_light').split('{')[1].split('}')[0]}
        }}
        
        /* Main text elements */
        QLabel {{
            {typography.get_qt_stylesheet_rules('', 'base', 'normal', 'primary', 'relaxed', 'normal', 'primary_light').split('{')[1].split('}')[0]}
        }}
        
        /* Exercise text - large and comfortable for Spanish learning */
        QLabel[role="exercise"] {{
            {typography.get_qt_stylesheet_rules('', 'lg', 'normal', 'primary', 'loose', 'wide', 'primary_light').split('{')[1].split('}')[0]}
            padding: 12px;
        }}
        
        /* Translation text - smaller secondary text */
        QLabel[role="translation"] {{
            {typography.get_qt_stylesheet_rules('', 'sm', 'normal', 'primary', 'normal', 'normal', 'secondary_light').split('{')[1].split('}')[0]}
            font-style: italic;
        }}
        
        /* Headings with proper hierarchy */
        QLabel[role="heading-large"] {{
            {typography.get_qt_stylesheet_rules('', 'title', 'semibold', 'display', 'tight', 'normal', 'primary_light').split('{')[1].split('}')[0]}
        }}
        
        QLabel[role="heading-medium"] {{
            {typography.get_qt_stylesheet_rules('', 'xl', 'semibold', 'primary', 'snug', 'normal', 'primary_light').split('{')[1].split('}')[0]}
        }}
        
        /* Input elements with comfortable sizing */
        QLineEdit, QTextEdit {{
            {typography.get_qt_stylesheet_rules('', 'base', 'normal', 'primary', 'normal', 'normal', 'primary_light').split('{')[1].split('}')[0]}
            padding: 8px 12px;
        }}
        
        /* Button text */
        QPushButton {{
            {typography.get_qt_stylesheet_rules('', 'base', 'medium', 'primary', 'tight', 'wide', 'primary_light').split('{')[1].split('}')[0]}
        }}
        
        /* Group box titles */
        QGroupBox::title {{
            {typography.get_qt_stylesheet_rules('', 'lg', 'semibold', 'primary', 'normal', 'normal', 'accent_light').split('{')[1].split('}')[0]}
        }}
        
        /* Status and stats text */
        QStatusBar {{
            {typography.get_qt_stylesheet_rules('', 'sm', 'normal', 'primary', 'normal', 'normal', 'secondary_light').split('{')[1].split('}')[0]}
        }}
        
        /* Feedback text area */
        QTextEdit[role="feedback"] {{
            {typography.get_qt_stylesheet_rules('', 'base', 'normal', 'primary', 'loose', 'normal', 'primary_light').split('{')[1].split('}')[0]}
            line-height: 1.6;
        }}
    """
    
    # Apply the stylesheet
    app.setStyleSheet(base_stylesheet)
    
    return typography


if __name__ == "__main__":
    """
    Demo and testing script for the Spanish typography system.
    """
    import sys
    from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QGroupBox
    
    app = QApplication(sys.argv)
    
    # Create typography system
    typography = apply_spanish_typography_to_app(app)
    
    # Create demo window
    demo = QWidget()
    demo.setWindowTitle("Spanish Typography System Demo")
    demo.setMinimumSize(800, 600)
    
    layout = QVBoxLayout(demo)
    
    # Demo Spanish text with accents
    spanish_samples = [
        "El español tiene muchos acentos: ñ, á, é, í, ó, ú",
        "Ojalá que tengas un buen día estudiando el subjuntivo",
        "Es importante que practiques todos los días",
        "No creo que sea difícil aprender con esta tipografía",
        "Espero que esta fuente sea perfecta para el aprendizaje"
    ]
    
    title = QLabel("Sistema de Tipografía para Español")
    title.setProperty('role', 'heading-large')
    layout.addWidget(title)
    
    # Sample text with different styles
    for i, text in enumerate(spanish_samples):
        sample_group = QGroupBox(f"Muestra {i + 1}")
        sample_layout = QVBoxLayout(sample_group)
        
        # Exercise text
        exercise_label = QLabel(text)
        exercise_label.setProperty('role', 'exercise')
        sample_layout.addWidget(exercise_label)
        
        # Translation
        translation = QLabel("(Translation would appear here in smaller text)")
        translation.setProperty('role', 'translation')
        sample_layout.addWidget(translation)
        
        layout.addWidget(sample_group)
    
    # Typography info
    info = get_typography_info()
    info_group = QGroupBox("Typography System Information")
    info_layout = QVBoxLayout(info_group)
    
    info_text = f"""
    Scale Factor: {info['current_scale_factor']:.2f}
    Screen DPI: {info['screen_info']['dpi']}
    Screen Size: {info['screen_info']['width']}x{info['screen_info']['height']}
    Primary Fonts: {', '.join(info['primary_fonts'][:3])}
    """
    
    info_label = QLabel(info_text.strip())
    info_layout.addWidget(info_label)
    layout.addWidget(info_group)
    
    demo.show()
    sys.exit(app.exec_())
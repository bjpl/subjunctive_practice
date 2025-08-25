"""
Font Management System for Spanish Subjunctive Practice App

This module provides comprehensive font loading and management capabilities specifically
optimized for Windows systems and Spanish character rendering.

Key Features:
- System font detection with intelligent fallbacks
- Web-safe font stack for cross-platform consistency
- Special handling for Spanish characters (ñ, á, é, í, ó, ú)
- Dynamic font sizing based on DPI/screen resolution
- Font smoothing and rendering optimizations for Windows
- Performance optimizations and caching
"""

import sys
import os
import logging
import json
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import platform

# PyQt5 imports for font handling
from PyQt5.QtCore import QObject, pyqtSignal, QSettings, QStandardPaths
from PyQt5.QtGui import QFont, QFontDatabase, QFontMetrics, QApplication, QPixmap, QPainter
from PyQt5.QtWidgets import QWidget

# Windows-specific imports for DPI awareness
if platform.system() == "Windows":
    try:
        import ctypes
        from ctypes import wintypes, windll
        WINDOWS_AVAILABLE = True
    except ImportError:
        WINDOWS_AVAILABLE = False
else:
    WINDOWS_AVAILABLE = False


logger = logging.getLogger(__name__)


@dataclass
class FontConfig:
    """Configuration for font settings"""
    family: str
    size: int
    weight: int = QFont.Normal
    italic: bool = False
    stretch: int = QFont.Unstretched
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FontConfig':
        """Create from dictionary"""
        return cls(**data)


@dataclass
class SpanishFontSupport:
    """Information about Spanish character support in fonts"""
    supports_spanish: bool
    missing_chars: List[str]
    quality_score: float  # 0.0 to 1.0
    
    
class WindowsDPIManager:
    """Windows-specific DPI handling for proper font scaling"""
    
    def __init__(self):
        self.dpi_scale = 1.0
        self.system_dpi = 96
        self._initialize_dpi()
    
    def _initialize_dpi(self):
        """Initialize DPI settings on Windows"""
        if not WINDOWS_AVAILABLE:
            return
            
        try:
            # Set DPI awareness
            windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
            
            # Get system DPI
            hdc = windll.user32.GetDC(0)
            self.system_dpi = windll.gdi32.GetDeviceCaps(hdc, 88)  # LOGPIXELSX
            windll.user32.ReleaseDC(0, hdc)
            
            self.dpi_scale = self.system_dpi / 96.0
            
            logger.info(f"Windows DPI initialized: {self.system_dpi} DPI, scale: {self.dpi_scale:.2f}")
            
        except Exception as e:
            logger.warning(f"Failed to initialize Windows DPI settings: {e}")
            self.dpi_scale = 1.0
            self.system_dpi = 96
    
    def get_scaled_size(self, base_size: int) -> int:
        """Get DPI-scaled font size"""
        return max(8, int(base_size * self.dpi_scale))
    
    def get_dpi_scale(self) -> float:
        """Get current DPI scaling factor"""
        return self.dpi_scale


class SpanishCharacterValidator:
    """Validates and tests Spanish character support in fonts"""
    
    # Essential Spanish characters
    SPANISH_CHARS = [
        'ñ', 'Ñ',  # eñe
        'á', 'é', 'í', 'ó', 'ú',  # vowels with acute accent
        'Á', 'É', 'Í', 'Ó', 'Ú',  # capital vowels with acute accent
        'ü', 'Ü',  # u with diaeresis (used in güe, güi)
        '¿', '¡',  # inverted punctuation
    ]
    
    # Additional useful characters for Spanish
    EXTENDED_SPANISH_CHARS = [
        'ç', 'Ç',  # cedilla (rare in Spanish but used in some words)
        '€',  # Euro symbol (useful for Spanish content)
        '«', '»',  # Spanish quotation marks
    ]
    
    def __init__(self):
        self.test_pixmap = QPixmap(100, 50)
        self.test_painter = QPainter()
    
    def validate_spanish_support(self, font: QFont) -> SpanishFontSupport:
        """
        Validate Spanish character support in a font
        
        Returns:
            SpanishFontSupport object with detailed information
        """
        missing_chars = []
        total_chars = len(self.SPANISH_CHARS)
        
        try:
            # Test rendering of each Spanish character
            self.test_pixmap.fill()
            self.test_painter.begin(self.test_pixmap)
            self.test_painter.setFont(font)
            
            font_metrics = QFontMetrics(font)
            
            for char in self.SPANISH_CHARS:
                # Check if font has the character
                if not font_metrics.inFontUcs4(ord(char)):
                    missing_chars.append(char)
                    continue
                    
                # Additional rendering test
                try:
                    width = font_metrics.horizontalAdvance(char)
                    if width <= 0:
                        missing_chars.append(char)
                except:
                    missing_chars.append(char)
            
            self.test_painter.end()
            
        except Exception as e:
            logger.warning(f"Error validating Spanish support for font {font.family()}: {e}")
            # Assume worst case
            missing_chars = self.SPANISH_CHARS.copy()
        
        # Calculate quality score
        supported_chars = total_chars - len(missing_chars)
        quality_score = supported_chars / total_chars if total_chars > 0 else 0.0
        
        return SpanishFontSupport(
            supports_spanish=len(missing_chars) == 0,
            missing_chars=missing_chars,
            quality_score=quality_score
        )
    
    def get_best_spanish_fonts(self, available_fonts: List[str]) -> List[Tuple[str, float]]:
        """
        Get list of fonts ranked by Spanish character support quality
        
        Returns:
            List of (font_name, quality_score) tuples, sorted by quality
        """
        font_scores = []
        
        for font_name in available_fonts:
            font = QFont(font_name)
            support = self.validate_spanish_support(font)
            font_scores.append((font_name, support.quality_score))
        
        # Sort by quality score (descending)
        font_scores.sort(key=lambda x: x[1], reverse=True)
        
        return font_scores


class FontManager(QObject):
    """
    Comprehensive font management system for the Spanish Subjunctive Practice app
    """
    
    # Signals for font changes
    fontChanged = pyqtSignal(QFont)
    sizeChanged = pyqtSignal(int)
    
    # Web-safe font stack optimized for Spanish content
    WEB_SAFE_FONTS = [
        # System fonts (highest priority)
        "Segoe UI",           # Windows default, excellent Spanish support
        "SF Pro Display",     # macOS
        "-apple-system",      # macOS system font
        "system-ui",          # Generic system font
        
        # Fallback fonts with good Spanish support
        "Helvetica Neue",     # macOS, clean and readable
        "Arial",              # Universal fallback
        "Liberation Sans",    # Linux equivalent to Arial
        "DejaVu Sans",        # Linux, excellent Unicode support
        "Noto Sans",          # Google font, comprehensive Unicode
        
        # Generic fallbacks
        "sans-serif",         # Generic sans-serif
        "serif",              # Generic serif fallback
    ]
    
    # Windows-specific font preferences
    WINDOWS_PREFERRED_FONTS = [
        "Segoe UI",
        "Segoe UI Historic",  # Better Unicode support
        "Calibri",
        "Tahoma",
        "Verdana",
        "Arial Unicode MS",   # Excellent Unicode support
    ]
    
    # Font sizes for different UI elements
    DEFAULT_FONT_SIZES = {
        'tiny': 10,
        'small': 12,
        'normal': 14,
        'medium': 16,
        'large': 18,
        'extra_large': 22,
        'huge': 28,
    }
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        
        # Core components
        self.dpi_manager = WindowsDPIManager()
        self.spanish_validator = SpanishCharacterValidator()
        self.font_database = QFontDatabase()
        
        # Font configuration
        self.current_config: Optional[FontConfig] = None
        self.available_fonts: List[str] = []
        self.spanish_fonts: List[Tuple[str, float]] = []
        
        # Settings storage
        self.settings = QSettings("SpanishSubjunctive", "FontManager")
        
        # Cache for performance
        self._font_cache: Dict[str, QFont] = {}
        self._metrics_cache: Dict[str, QFontMetrics] = {}
        
        # Initialize the font system
        self._initialize()
    
    def _initialize(self):
        """Initialize the font management system"""
        try:
            logger.info("Initializing Font Manager...")
            
            # Detect available system fonts
            self._detect_system_fonts()
            
            # Validate Spanish character support
            self._validate_spanish_fonts()
            
            # Load saved configuration or set defaults
            self._load_configuration()
            
            # Apply Windows-specific optimizations
            if platform.system() == "Windows":
                self._apply_windows_optimizations()
            
            logger.info(f"Font Manager initialized with {len(self.available_fonts)} fonts")
            logger.info(f"Found {len(self.spanish_fonts)} fonts with Spanish support")
            
        except Exception as e:
            logger.error(f"Failed to initialize Font Manager: {e}")
            self._set_fallback_configuration()
    
    def _detect_system_fonts(self):
        """Detect available system fonts"""
        try:
            # Get all available font families
            all_families = self.font_database.families()
            
            # Filter out bitmap fonts and prefer scalable fonts
            scalable_families = []
            for family in all_families:
                if self.font_database.isSmoothlyScalable(family):
                    scalable_families.append(family)
            
            self.available_fonts = scalable_families
            logger.info(f"Detected {len(self.available_fonts)} scalable fonts")
            
        except Exception as e:
            logger.error(f"Error detecting system fonts: {e}")
            # Fallback to basic font list
            self.available_fonts = ["Arial", "Times New Roman", "Courier New"]
    
    def _validate_spanish_fonts(self):
        """Validate Spanish character support in available fonts"""
        try:
            # Get fonts ranked by Spanish support quality
            self.spanish_fonts = self.spanish_validator.get_best_spanish_fonts(
                self.available_fonts
            )
            
            # Log top Spanish-supporting fonts
            top_5 = self.spanish_fonts[:5]
            logger.info("Top 5 fonts for Spanish characters:")
            for font_name, quality in top_5:
                logger.info(f"  {font_name}: {quality:.1%} support")
                
        except Exception as e:
            logger.error(f"Error validating Spanish fonts: {e}")
            # Create fallback list
            self.spanish_fonts = [(font, 0.5) for font in self.WEB_SAFE_FONTS[:3]]
    
    def _load_configuration(self):
        """Load font configuration from settings"""
        try:
            saved_config = self.settings.value("font_config", None)
            
            if saved_config and isinstance(saved_config, dict):
                self.current_config = FontConfig.from_dict(saved_config)
                logger.info(f"Loaded font configuration: {self.current_config.family} {self.current_config.size}pt")
            else:
                self._set_default_configuration()
                
        except Exception as e:
            logger.warning(f"Error loading font configuration: {e}")
            self._set_default_configuration()
    
    def _set_default_configuration(self):
        """Set default font configuration based on system and Spanish support"""
        try:
            # Find the best available font for Spanish
            best_font = self._get_best_spanish_font()
            base_size = self.DEFAULT_FONT_SIZES['normal']
            
            # Apply DPI scaling
            scaled_size = self.dpi_manager.get_scaled_size(base_size)
            
            self.current_config = FontConfig(
                family=best_font,
                size=scaled_size,
                weight=QFont.Normal,
                italic=False
            )
            
            logger.info(f"Set default font configuration: {best_font} {scaled_size}pt")
            
        except Exception as e:
            logger.error(f"Error setting default font configuration: {e}")
            self._set_fallback_configuration()
    
    def _set_fallback_configuration(self):
        """Set absolute fallback configuration"""
        self.current_config = FontConfig(
            family="Arial",
            size=14,
            weight=QFont.Normal,
            italic=False
        )
        logger.info("Set fallback font configuration: Arial 14pt")
    
    def _get_best_spanish_font(self) -> str:
        """Get the best available font for Spanish characters"""
        if not self.spanish_fonts:
            # Fallback to web-safe fonts in order of preference
            for font_name in self.WEB_SAFE_FONTS:
                if font_name in self.available_fonts:
                    return font_name
            return "Arial"  # Ultimate fallback
        
        # Return the highest-quality Spanish font
        return self.spanish_fonts[0][0]
    
    def _apply_windows_optimizations(self):
        """Apply Windows-specific font rendering optimizations"""
        if not WINDOWS_AVAILABLE:
            return
            
        try:
            # Enable font smoothing (ClearType)
            windll.user32.SystemParametersInfoW(0x1015, 0, None, 0)  # SPI_SETFONTSMOOTHING
            windll.user32.SystemParametersInfoW(0x200B, 0, 2, 0)     # SPI_SETFONTSMOOTHINGTYPE (ClearType)
            
            logger.info("Applied Windows font rendering optimizations")
            
        except Exception as e:
            logger.warning(f"Failed to apply Windows optimizations: {e}")
    
    def get_font(self, size_key: str = 'normal', weight: int = QFont.Normal, italic: bool = False) -> QFont:
        """
        Get a configured font for the application
        
        Args:
            size_key: Font size key from DEFAULT_FONT_SIZES
            weight: Font weight (QFont.Normal, QFont.Bold, etc.)
            italic: Whether the font should be italic
            
        Returns:
            Configured QFont object
        """
        if not self.current_config:
            self._set_default_configuration()
        
        # Create cache key
        cache_key = f"{self.current_config.family}_{size_key}_{weight}_{italic}"
        
        # Return cached font if available
        if cache_key in self._font_cache:
            return self._font_cache[cache_key]
        
        # Get base size and apply DPI scaling
        base_size = self.DEFAULT_FONT_SIZES.get(size_key, self.DEFAULT_FONT_SIZES['normal'])
        scaled_size = self.dpi_manager.get_scaled_size(base_size)
        
        # Create font
        font = QFont(self.current_config.family)
        font.setPointSize(scaled_size)
        font.setWeight(weight)
        font.setItalic(italic)
        
        # Apply font hinting for better rendering on Windows
        if platform.system() == "Windows":
            font.setHintingPreference(QFont.PreferFullHinting)
            font.setStyleStrategy(QFont.PreferAntialias)
        
        # Cache the font
        self._font_cache[cache_key] = font
        
        return font
    
    def get_font_metrics(self, font: QFont) -> QFontMetrics:
        """Get font metrics with caching"""
        font_key = f"{font.family()}_{font.pointSize()}_{font.weight()}_{font.italic()}"
        
        if font_key not in self._metrics_cache:
            self._metrics_cache[font_key] = QFontMetrics(font)
        
        return self._metrics_cache[font_key]
    
    def set_base_font_size(self, size: int):
        """Set the base font size and update configuration"""
        if not self.current_config:
            self._set_default_configuration()
        
        # Apply DPI scaling
        scaled_size = self.dpi_manager.get_scaled_size(size)
        
        self.current_config.size = scaled_size
        self._clear_caches()
        self._save_configuration()
        
        logger.info(f"Set base font size to {size}pt (scaled: {scaled_size}pt)")
        self.sizeChanged.emit(scaled_size)
    
    def set_font_family(self, family: str):
        """Set the font family and update configuration"""
        if family not in self.available_fonts:
            logger.warning(f"Font family '{family}' not available")
            return
        
        if not self.current_config:
            self._set_default_configuration()
        
        self.current_config.family = family
        self._clear_caches()
        self._save_configuration()
        
        logger.info(f"Set font family to {family}")
        self.fontChanged.emit(self.get_font())
    
    def get_spanish_character_support(self, font_name: str) -> Optional[SpanishFontSupport]:
        """Get Spanish character support information for a font"""
        font = QFont(font_name)
        return self.spanish_validator.validate_spanish_support(font)
    
    def get_recommended_fonts(self) -> List[str]:
        """Get list of recommended fonts for Spanish content"""
        # Return fonts with >90% Spanish character support
        recommended = []
        for font_name, quality in self.spanish_fonts:
            if quality >= 0.9:
                recommended.append(font_name)
        
        # Ensure we have at least some recommendations
        if len(recommended) < 3:
            recommended.extend(self.WEB_SAFE_FONTS[:3])
        
        return list(dict.fromkeys(recommended))  # Remove duplicates, preserve order
    
    def get_available_fonts(self) -> List[str]:
        """Get list of all available fonts"""
        return self.available_fonts.copy()
    
    def get_current_configuration(self) -> Optional[FontConfig]:
        """Get current font configuration"""
        return self.current_config
    
    def apply_font_to_widget(self, widget: QWidget, size_key: str = 'normal', 
                           weight: int = QFont.Normal, italic: bool = False):
        """Apply font configuration to a widget"""
        font = self.get_font(size_key, weight, italic)
        widget.setFont(font)
    
    def create_stylesheet_font_rules(self, size_key: str = 'normal') -> str:
        """Create CSS font rules for Qt stylesheets"""
        if not self.current_config:
            self._set_default_configuration()
        
        base_size = self.DEFAULT_FONT_SIZES.get(size_key, self.DEFAULT_FONT_SIZES['normal'])
        scaled_size = self.dpi_manager.get_scaled_size(base_size)
        
        return f"""
            font-family: "{self.current_config.family}", {', '.join(f'"{f}"' for f in self.WEB_SAFE_FONTS[1:])};
            font-size: {scaled_size}pt;
        """
    
    def _save_configuration(self):
        """Save current font configuration to settings"""
        if self.current_config:
            try:
                self.settings.setValue("font_config", self.current_config.to_dict())
                self.settings.sync()
            except Exception as e:
                logger.error(f"Error saving font configuration: {e}")
    
    def _clear_caches(self):
        """Clear font and metrics caches"""
        self._font_cache.clear()
        self._metrics_cache.clear()
    
    def get_debug_info(self) -> Dict[str, Any]:
        """Get debug information about the font system"""
        return {
            "current_config": self.current_config.to_dict() if self.current_config else None,
            "system_dpi": self.dpi_manager.system_dpi,
            "dpi_scale": self.dpi_manager.dpi_scale,
            "available_fonts_count": len(self.available_fonts),
            "spanish_fonts_count": len(self.spanish_fonts),
            "platform": platform.system(),
            "windows_available": WINDOWS_AVAILABLE,
            "font_cache_size": len(self._font_cache),
            "metrics_cache_size": len(self._metrics_cache),
            "top_spanish_fonts": self.spanish_fonts[:5] if self.spanish_fonts else [],
            "recommended_fonts": self.get_recommended_fonts()[:5]
        }


# Convenience functions for easy integration
def create_font_manager(parent: Optional[QWidget] = None) -> FontManager:
    """Create and initialize a font manager instance"""
    return FontManager(parent)


def get_spanish_optimized_font(size: int = 14) -> QFont:
    """Get a font optimized for Spanish characters with specified size"""
    manager = FontManager()
    manager.set_base_font_size(size)
    return manager.get_font('normal')


def validate_spanish_font_support(font_name: str) -> SpanishFontSupport:
    """Validate Spanish character support for a specific font"""
    validator = SpanishCharacterValidator()
    font = QFont(font_name)
    return validator.validate_spanish_support(font)


# Example usage and testing
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
    
    class FontTestWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Font Manager Test")
            self.setGeometry(100, 100, 800, 600)
            
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            layout = QVBoxLayout(central_widget)
            
            # Create font manager
            self.font_manager = FontManager(self)
            
            # Test Spanish text
            spanish_text = "¡Hola! ¿Cómo estás? Mañana será un día fantástico. ñoño güeña"
            
            # Create labels with different font sizes
            for size_key in ['small', 'normal', 'medium', 'large', 'extra_large']:
                label = QLabel(f"{size_key.title()}: {spanish_text}")
                self.font_manager.apply_font_to_widget(label, size_key)
                layout.addWidget(label)
            
            # Debug info
            debug_info = self.font_manager.get_debug_info()
            debug_label = QLabel(f"Debug: {debug_info}")
            debug_label.setWordWrap(True)
            layout.addWidget(debug_label)
    
    app = QApplication(sys.argv)
    
    # Test the font manager
    window = FontTestWindow()
    window.show()
    
    sys.exit(app.exec_())
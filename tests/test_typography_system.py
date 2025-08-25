"""
Test Suite for Spanish Typography System

This module provides comprehensive tests for the Spanish typography system
to ensure proper functionality, responsiveness, and Spanish text optimization.

Tests cover:
- Font creation and scaling
- Spanish character rendering
- Responsive scaling logic
- Preset application
- Integration with PyQt5
- Performance characteristics

Usage:
    python -m pytest tests/test_typography_system.py
    or
    python tests/test_typography_system.py
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

try:
    from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton
    from PyQt5.QtGui import QFont, QFontMetrics
    from PyQt5.QtCore import Qt
    PYQT5_AVAILABLE = True
except ImportError:
    PYQT5_AVAILABLE = False

if PYQT5_AVAILABLE:
    from typography_system import (
        SpanishTypography,
        SpanishTypographyConfig,
        TypographyScaler,
        SpanishTextMetrics,
        TypographyPresets,
        create_spanish_typography,
        apply_spanish_typography_to_app,
        get_typography_info
    )


@unittest.skipUnless(PYQT5_AVAILABLE, "PyQt5 not available")
class TestSpanishTypographyConfig(unittest.TestCase):
    """Test the typography configuration class."""
    
    def setUp(self):
        self.config = SpanishTypographyConfig()
    
    def test_font_families(self):
        """Test font family configurations."""
        # Primary fonts should prioritize Windows fonts
        primary_fonts = self.config.FONT_FAMILIES['primary']
        self.assertIn('Segoe UI', primary_fonts)
        self.assertIn('Calibri', primary_fonts)
        self.assertIn('Tahoma', primary_fonts)
        self.assertIn('sans-serif', primary_fonts)
        
        # Should have monospace fonts
        mono_fonts = self.config.FONT_FAMILIES['monospace']
        self.assertIn('Consolas', mono_fonts)
        self.assertIn('monospace', mono_fonts)
        
        # Should have display fonts
        display_fonts = self.config.FONT_FAMILIES['display']
        self.assertIn('Segoe UI Light', display_fonts)
    
    def test_base_sizes(self):
        """Test font size configurations."""
        sizes = self.config.BASE_SIZES
        
        # Should have proper size progression
        self.assertLess(sizes['xs'], sizes['sm'])
        self.assertLess(sizes['sm'], sizes['base'])
        self.assertLess(sizes['base'], sizes['lg'])
        
        # Base size should be in optimal range for Spanish text
        self.assertGreaterEqual(sizes['base'], 14)
        self.assertLessEqual(sizes['base'], 16)
        
        # Should have all expected sizes
        expected_sizes = ['xs', 'sm', 'base', 'md', 'lg', 'xl', 'xxl', 'title', 'display', 'hero']
        for size in expected_sizes:
            self.assertIn(size, sizes)
            self.assertIsInstance(sizes[size], int)
    
    def test_line_heights(self):
        """Test line height configurations for Spanish text."""
        line_heights = self.config.LINE_HEIGHTS
        
        # Should have proper progression
        self.assertLess(line_heights['tight'], line_heights['normal'])
        self.assertLess(line_heights['normal'], line_heights['relaxed'])
        
        # Normal line height should be good for Spanish accents
        self.assertGreaterEqual(line_heights['normal'], 1.4)
        self.assertLessEqual(line_heights['normal'], 1.6)
    
    def test_text_colors(self):
        """Test text color configurations."""
        colors = self.config.TEXT_COLORS
        
        # Should have both light and dark theme colors
        self.assertIn('primary_light', colors)
        self.assertIn('primary_dark', colors)
        
        # Colors should be valid hex format
        for color in colors.values():
            self.assertTrue(color.startswith('#'))
            self.assertEqual(len(color), 7)  # #RRGGBB format


@unittest.skipUnless(PYQT5_AVAILABLE, "PyQt5 not available")
class TestTypographyScaler(unittest.TestCase):
    """Test the responsive typography scaling system."""
    
    def setUp(self):
        if not QApplication.instance():
            self.app = QApplication([])
        else:
            self.app = QApplication.instance()
        self.scaler = TypographyScaler()
    
    def test_screen_info_retrieval(self):
        """Test screen information gathering."""
        screen_info = self.scaler.get_screen_info()
        
        # Should have all expected fields
        expected_fields = ['dpi', 'scale_factor', 'width', 'height', 'diagonal_inches']
        for field in expected_fields:
            self.assertIn(field, screen_info)
        
        # Values should be reasonable
        self.assertGreater(screen_info['dpi'], 50)
        self.assertLess(screen_info['dpi'], 300)
        self.assertGreater(screen_info['width'], 800)
        self.assertGreater(screen_info['height'], 600)
    
    def test_scale_factor_calculation(self):
        """Test font scaling factor calculation."""
        scale_factor = self.scaler.calculate_font_scale_factor()
        
        # Should be within reasonable bounds
        self.assertGreaterEqual(scale_factor, 0.8)
        self.assertLessEqual(scale_factor, 2.0)
        self.assertIsInstance(scale_factor, float)
    
    def test_scaled_size_calculation(self):
        """Test scaled font size calculation."""
        base_size = 14
        scaled_size = self.scaler.get_scaled_size(base_size)
        
        # Should return integer
        self.assertIsInstance(scaled_size, int)
        
        # Should be at least minimum size
        self.assertGreaterEqual(scaled_size, 8)
        
        # Should scale proportionally
        scale_factor = self.scaler.calculate_font_scale_factor()
        expected_size = max(8, round(base_size * scale_factor))
        self.assertEqual(scaled_size, expected_size)
    
    @patch('typography_system.QApplication')
    def test_no_application_fallback(self, mock_app):
        """Test behavior when no QApplication is available."""
        mock_app.instance.return_value = None
        scaler = TypographyScaler()
        
        screen_info = scaler.get_screen_info()
        # Should return default values
        self.assertEqual(screen_info['dpi'], 96)
        self.assertEqual(screen_info['scale_factor'], 1.0)


@unittest.skipUnless(PYQT5_AVAILABLE, "PyQt5 not available")
class TestSpanishTypography(unittest.TestCase):
    """Test the main Spanish typography class."""
    
    def setUp(self):
        if not QApplication.instance():
            self.app = QApplication([])
        self.typography = SpanishTypography()
    
    def test_font_creation(self):
        """Test font creation with different parameters."""
        # Test basic font creation
        font = self.typography.create_font()
        self.assertIsInstance(font, QFont)
        
        # Test with specific parameters
        font = self.typography.create_font(
            size='lg',
            weight='semibold',
            family='primary'
        )
        self.assertIsInstance(font, QFont)
        
        # Font should have expected characteristics
        self.assertGreater(font.pointSize(), 10)
        
        # Should handle invalid parameters gracefully
        font = self.typography.create_font(size='invalid_size')
        self.assertIsInstance(font, QFont)
    
    def test_font_caching(self):
        """Test that fonts are properly cached."""
        # Create same font twice
        font1 = self.typography.create_font('base', 'normal', 'primary')
        font2 = self.typography.create_font('base', 'normal', 'primary')
        
        # Should be same object (cached)
        self.assertIs(font1, font2)
        
        # Different parameters should create different fonts
        font3 = self.typography.create_font('lg', 'normal', 'primary')
        self.assertIsNot(font1, font3)
    
    def test_line_height_calculation(self):
        """Test line height pixel calculation."""
        line_height_px = self.typography.get_line_height_px('base', 'normal')
        
        self.assertIsInstance(line_height_px, int)
        self.assertGreater(line_height_px, 10)
        
        # Loose line height should be larger
        loose_height = self.typography.get_line_height_px('base', 'loose')
        normal_height = self.typography.get_line_height_px('base', 'normal')
        self.assertGreater(loose_height, normal_height)
    
    def test_letter_spacing_calculation(self):
        """Test letter spacing calculation."""
        spacing = self.typography.get_letter_spacing_px('normal')
        self.assertEqual(spacing, 0.0)
        
        wide_spacing = self.typography.get_letter_spacing_px('wide')
        self.assertGreater(wide_spacing, 0)
        
        tight_spacing = self.typography.get_letter_spacing_px('tight')
        self.assertLess(tight_spacing, 0)
    
    def test_style_dictionary_creation(self):
        """Test creation of complete style dictionaries."""
        style_dict = self.typography.create_text_style_dict()
        
        # Should have all expected keys
        expected_keys = [
            'font_family', 'font_size', 'font_weight', 'line_height',
            'letter_spacing', 'color', 'text_rendering'
        ]
        for key in expected_keys:
            self.assertIn(key, style_dict)
        
        # Font family should be properly formatted
        self.assertIn('Segoe UI', style_dict['font_family'])
        
        # Font size should have 'px' suffix
        self.assertTrue(style_dict['font_size'].endswith('px'))
        
        # Color should be hex format
        self.assertTrue(style_dict['color'].startswith('#'))
    
    def test_qt_stylesheet_generation(self):
        """Test Qt stylesheet rule generation."""
        stylesheet = self.typography.get_qt_stylesheet_rules(
            selector='QLabel',
            size='base',
            weight='normal'
        )
        
        # Should be valid CSS-like syntax
        self.assertIn('QLabel {', stylesheet)
        self.assertIn('font-family:', stylesheet)
        self.assertIn('font-size:', stylesheet)
        self.assertIn('font-weight:', stylesheet)
        self.assertIn('color:', stylesheet)
        self.assertTrue(stylesheet.endswith('}'))


@unittest.skipUnless(PYQT5_AVAILABLE, "PyQt5 not available")
class TestSpanishTextMetrics(unittest.TestCase):
    """Test Spanish text measurement functionality."""
    
    def setUp(self):
        if not QApplication.instance():
            self.app = QApplication([])
        self.typography = SpanishTypography()
        self.metrics = SpanishTextMetrics(self.typography)
    
    def test_text_measurement(self):
        """Test measurement of Spanish text with accents."""
        spanish_text = "Espero que tengas éxito en el aprendizaje"
        
        dimensions = self.metrics.measure_text(spanish_text, 'base', 'normal')
        
        # Should return valid dimensions
        self.assertIsInstance(dimensions, dict)
        expected_keys = ['width', 'height', 'line_height', 'line_count', 'ascent', 'descent']
        for key in expected_keys:
            self.assertIn(key, dimensions)
            self.assertIsInstance(dimensions[key], int)
        
        # Dimensions should be reasonable
        self.assertGreater(dimensions['width'], 100)
        self.assertGreater(dimensions['height'], 10)
        self.assertEqual(dimensions['line_count'], 1)
    
    def test_wrapped_text_measurement(self):
        """Test measurement of wrapped text."""
        long_text = "Este es un texto muy largo que debería dividirse en múltiples líneas cuando se especifica un ancho máximo"
        
        dimensions = self.metrics.measure_text(
            text=long_text,
            font_size='base',
            max_width=200
        )
        
        # Should have multiple lines when wrapped
        self.assertGreaterEqual(dimensions['line_count'], 2)
        self.assertLessEqual(dimensions['width'], 200)
    
    def test_optimal_width_calculation(self):
        """Test optimal width calculation for Spanish text."""
        text = "Texto de ejemplo en español"
        optimal_width = self.metrics.get_optimal_width(text, 'base')
        
        self.assertIsInstance(optimal_width, int)
        self.assertGreater(optimal_width, 300)  # Should be reasonable for 65 characters
        self.assertLess(optimal_width, 1000)


@unittest.skipUnless(PYQT5_AVAILABLE, "PyQt5 not available")
class TestTypographyPresets(unittest.TestCase):
    """Test typography presets functionality."""
    
    def setUp(self):
        if not QApplication.instance():
            self.app = QApplication([])
        self.typography = SpanishTypography()
        self.presets = TypographyPresets(self.typography)
    
    def test_preset_configuration(self):
        """Test preset configurations."""
        presets = self.presets.get_presets()
        
        # Should have expected presets
        expected_presets = [
            'body_text', 'exercise_text', 'translation_text',
            'heading_large', 'heading_medium', 'heading_small',
            'label_text', 'button_text', 'feedback_text',
            'stats_text', 'code_text'
        ]
        
        for preset in expected_presets:
            self.assertIn(preset, presets)
            
            # Each preset should have required keys
            preset_config = presets[preset]
            required_keys = ['size', 'weight', 'family', 'line_height', 'letter_spacing']
            for key in required_keys:
                self.assertIn(key, preset_config)
    
    def test_preset_font_creation(self):
        """Test font creation from presets."""
        # Test valid preset
        font = self.presets.create_preset_font('exercise_text')
        self.assertIsInstance(font, QFont)
        
        # Test invalid preset (should fallback to body_text)
        font = self.presets.create_preset_font('invalid_preset')
        self.assertIsInstance(font, QFont)
    
    def test_preset_stylesheet_generation(self):
        """Test stylesheet generation from presets."""
        stylesheet = self.presets.get_preset_stylesheet(
            'QLabel[role="exercise"]', 
            'exercise_text'
        )
        
        self.assertIsInstance(stylesheet, str)
        self.assertIn('QLabel[role="exercise"]', stylesheet)
        self.assertIn('font-family:', stylesheet)
        self.assertIn('font-size:', stylesheet)
    
    def test_exercise_text_preset(self):
        """Test specific preset for Spanish exercise text."""
        presets = self.presets.get_presets()
        exercise_preset = presets['exercise_text']
        
        # Exercise text should be larger and comfortable for reading
        self.assertIn(exercise_preset['size'], ['lg', 'xl'])
        self.assertIn(exercise_preset['line_height'], ['relaxed', 'loose'])
        self.assertIn(exercise_preset['letter_spacing'], ['normal', 'wide'])


@unittest.skipUnless(PYQT5_AVAILABLE, "PyQt5 not available")
class TestIntegrationFunctions(unittest.TestCase):
    """Test integration and utility functions."""
    
    def setUp(self):
        if not QApplication.instance():
            self.app = QApplication([])
        else:
            self.app = QApplication.instance()
    
    def test_create_spanish_typography(self):
        """Test typography instance creation."""
        typography = create_spanish_typography()
        self.assertIsInstance(typography, SpanishTypography)
    
    def test_apply_spanish_typography_to_app(self):
        """Test application-wide typography application."""
        typography = apply_spanish_typography_to_app(self.app)
        
        self.assertIsInstance(typography, SpanishTypography)
        
        # Should have applied stylesheet to app
        stylesheet = self.app.styleSheet()
        self.assertIsInstance(stylesheet, str)
        self.assertIn('font-family:', stylesheet)
    
    def test_get_typography_info(self):
        """Test typography system information retrieval."""
        info = get_typography_info()
        
        self.assertIsInstance(info, dict)
        
        # Should have expected information fields
        expected_fields = [
            'version', 'optimized_for', 'base_font_size',
            'primary_fonts', 'screen_info', 'current_scale_factor'
        ]
        
        for field in expected_fields:
            self.assertIn(field, info)
    
    @patch('sys.platform', 'win32')
    def test_windows_optimization(self):
        """Test that system is optimized for Windows."""
        typography = create_spanish_typography()
        config = typography.config
        
        # Should prioritize Windows fonts
        primary_fonts = config.FONT_FAMILIES['primary']
        self.assertEqual(primary_fonts[0], 'Segoe UI')  # Windows 10/11 default
        self.assertIn('Calibri', primary_fonts)  # Office standard
        self.assertIn('Tahoma', primary_fonts)  # Windows classic


class TestSpanishCharacterHandling(unittest.TestCase):
    """Test handling of Spanish-specific characters."""
    
    def setUp(self):
        if PYQT5_AVAILABLE and not QApplication.instance():
            self.app = QApplication([])
    
    @unittest.skipUnless(PYQT5_AVAILABLE, "PyQt5 not available")
    def test_spanish_accent_characters(self):
        """Test that Spanish accented characters are handled properly."""
        typography = SpanishTypography()
        
        # Test text with various Spanish characters
        spanish_chars = "áéíóúüñÁÉÍÓÚÜÑ¿¡"
        
        # Should be able to create fonts and measure text
        font = typography.create_font('base', 'normal', 'primary')
        self.assertIsInstance(font, QFont)
        
        # Text metrics should work with Spanish characters
        metrics = SpanishTextMetrics(typography)
        dimensions = metrics.measure_text(spanish_chars, 'base', 'normal')
        self.assertGreater(dimensions['width'], 0)
        self.assertGreater(dimensions['height'], 0)
    
    @unittest.skipUnless(PYQT5_AVAILABLE, "PyQt5 not available")
    def test_common_spanish_phrases(self):
        """Test common Spanish phrases that students encounter."""
        typography = SpanishTypography()
        metrics = SpanishTextMetrics(typography)
        
        common_phrases = [
            "Espero que tengas un buen día",
            "Es importante que estudies español", 
            "No creo que sea difícil",
            "Ojalá que llueva mañana",
            "Dudo que venga a la fiesta"
        ]
        
        for phrase in common_phrases:
            dimensions = metrics.measure_text(phrase, 'lg', 'normal')
            # Should successfully measure all phrases
            self.assertGreater(dimensions['width'], 0)
            self.assertGreater(dimensions['height'], 0)
            
            # Should have reasonable dimensions for display
            self.assertLess(dimensions['width'], 1000)  # Not too wide
            self.assertGreater(dimensions['width'], 100)  # Not too narrow


class TestPerformance(unittest.TestCase):
    """Test performance characteristics of the typography system."""
    
    def setUp(self):
        if PYQT5_AVAILABLE and not QApplication.instance():
            self.app = QApplication([])
    
    @unittest.skipUnless(PYQT5_AVAILABLE, "PyQt5 not available")
    def test_font_creation_performance(self):
        """Test that font creation is reasonably fast."""
        import time
        
        typography = SpanishTypography()
        
        # Time font creation
        start_time = time.time()
        for i in range(100):
            font = typography.create_font('base', 'normal', 'primary')
        end_time = time.time()
        
        # Should complete quickly (most should be cached after first)
        total_time = end_time - start_time
        self.assertLess(total_time, 1.0)  # Should take less than 1 second
    
    @unittest.skipUnless(PYQT5_AVAILABLE, "PyQt5 not available")
    def test_caching_effectiveness(self):
        """Test that font caching reduces creation time."""
        import time
        
        typography = SpanishTypography()
        
        # Time first creation (not cached)
        start_time = time.time()
        font1 = typography.create_font('base', 'normal', 'primary')
        first_time = time.time() - start_time
        
        # Time second creation (should be cached)
        start_time = time.time()
        font2 = typography.create_font('base', 'normal', 'primary')
        second_time = time.time() - start_time
        
        # Second call should be much faster (cached)
        self.assertLess(second_time, first_time * 0.1)  # At least 10x faster
        
        # Should be same object
        self.assertIs(font1, font2)


def run_typography_tests():
    """Run all typography system tests and return results."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestSpanishTypographyConfig,
        TestTypographyScaler,
        TestSpanishTypography,
        TestSpanishTextMetrics,
        TestTypographyPresets,
        TestIntegrationFunctions,
        TestSpanishCharacterHandling,
        TestPerformance
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


def main():
    """Main test runner."""
    print("=== Spanish Typography System Test Suite ===\n")
    
    if not PYQT5_AVAILABLE:
        print("❌ PyQt5 not available. Cannot run typography tests.")
        print("Install PyQt5: pip install PyQt5")
        return False
    
    print("✅ PyQt5 available. Running typography tests...\n")
    
    # Run all tests
    result = run_typography_tests()
    
    # Summary
    print(f"\n=== Test Summary ===")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print(f"\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print(f"\n❌ Errors:")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    
    if success:
        print(f"\n✅ All tests passed! Typography system is working correctly.")
    else:
        print(f"\n❌ Some tests failed. Please check the implementation.")
    
    return success


if __name__ == "__main__":
    main()
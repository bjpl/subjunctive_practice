"""
Test Suite for Font Manager

This module contains comprehensive tests for the FontManager system,
including system font detection, Spanish character validation, DPI scaling,
and performance testing.
"""

import sys
import unittest
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import QSettings

from font_manager import (
    FontManager, FontConfig, SpanishCharacterValidator, 
    WindowsDPIManager, SpanishFontSupport,
    create_font_manager, get_spanish_optimized_font, validate_spanish_font_support
)

# Ensure QApplication exists for font testing
app = None
def setUpModule():
    global app
    if not QApplication.instance():
        app = QApplication([])

def tearDownModule():
    global app
    if app:
        app.quit()


class TestFontConfig(unittest.TestCase):
    """Test FontConfig dataclass"""
    
    def test_font_config_creation(self):
        """Test FontConfig creation and basic functionality"""
        config = FontConfig(family="Arial", size=14)
        
        self.assertEqual(config.family, "Arial")
        self.assertEqual(config.size, 14)
        self.assertEqual(config.weight, QFont.Normal)
        self.assertFalse(config.italic)
        self.assertEqual(config.stretch, QFont.Unstretched)
    
    def test_font_config_serialization(self):
        """Test FontConfig to/from dict conversion"""
        config = FontConfig(
            family="Segoe UI",
            size=16,
            weight=QFont.Bold,
            italic=True
        )
        
        # Test to_dict
        config_dict = config.to_dict()
        expected_dict = {
            'family': 'Segoe UI',
            'size': 16,
            'weight': QFont.Bold,
            'italic': True,
            'stretch': QFont.Unstretched
        }
        self.assertEqual(config_dict, expected_dict)
        
        # Test from_dict
        recreated_config = FontConfig.from_dict(config_dict)
        self.assertEqual(recreated_config.family, config.family)
        self.assertEqual(recreated_config.size, config.size)
        self.assertEqual(recreated_config.weight, config.weight)
        self.assertEqual(recreated_config.italic, config.italic)


class TestSpanishFontSupport(unittest.TestCase):
    """Test SpanishFontSupport dataclass"""
    
    def test_spanish_font_support_creation(self):
        """Test SpanishFontSupport creation"""
        support = SpanishFontSupport(
            supports_spanish=True,
            missing_chars=[],
            quality_score=1.0
        )
        
        self.assertTrue(support.supports_spanish)
        self.assertEqual(support.missing_chars, [])
        self.assertEqual(support.quality_score, 1.0)
    
    def test_spanish_font_support_partial(self):
        """Test SpanishFontSupport with partial support"""
        support = SpanishFontSupport(
            supports_spanish=False,
            missing_chars=['ñ', 'Ñ'],
            quality_score=0.8
        )
        
        self.assertFalse(support.supports_spanish)
        self.assertEqual(support.missing_chars, ['ñ', 'Ñ'])
        self.assertEqual(support.quality_score, 0.8)


class TestWindowsDPIManager(unittest.TestCase):
    """Test Windows DPI Manager"""
    
    def setUp(self):
        self.dpi_manager = WindowsDPIManager()
    
    def test_dpi_manager_initialization(self):
        """Test DPI manager initialization"""
        self.assertIsInstance(self.dpi_manager.dpi_scale, float)
        self.assertGreater(self.dpi_manager.dpi_scale, 0.0)
        self.assertIsInstance(self.dpi_manager.system_dpi, int)
        self.assertGreaterEqual(self.dpi_manager.system_dpi, 96)  # Minimum expected DPI
    
    def test_get_scaled_size(self):
        """Test DPI-scaled size calculation"""
        base_size = 14
        scaled_size = self.dpi_manager.get_scaled_size(base_size)
        
        self.assertIsInstance(scaled_size, int)
        self.assertGreaterEqual(scaled_size, 8)  # Minimum size enforced
        
        # Test minimum size enforcement
        tiny_size = self.dpi_manager.get_scaled_size(4)
        self.assertEqual(tiny_size, 8)
    
    def test_get_dpi_scale(self):
        """Test DPI scale retrieval"""
        scale = self.dpi_manager.get_dpi_scale()
        
        self.assertIsInstance(scale, float)
        self.assertGreater(scale, 0.0)
        self.assertEqual(scale, self.dpi_manager.dpi_scale)


class TestSpanishCharacterValidator(unittest.TestCase):
    """Test Spanish Character Validator"""
    
    def setUp(self):
        self.validator = SpanishCharacterValidator()
    
    def test_validator_initialization(self):
        """Test validator initialization"""
        self.assertIsNotNone(self.validator.test_pixmap)
        self.assertIsNotNone(self.validator.test_painter)
        
        # Check Spanish character sets
        self.assertIn('ñ', self.validator.SPANISH_CHARS)
        self.assertIn('Ñ', self.validator.SPANISH_CHARS)
        self.assertIn('á', self.validator.SPANISH_CHARS)
        self.assertIn('¿', self.validator.SPANISH_CHARS)
        self.assertIn('¡', self.validator.SPANISH_CHARS)
    
    def test_validate_spanish_support_arial(self):
        """Test Spanish support validation with Arial (should support most characters)"""
        arial_font = QFont("Arial", 14)
        support = self.validator.validate_spanish_support(arial_font)
        
        self.assertIsInstance(support, SpanishFontSupport)
        self.assertGreaterEqual(support.quality_score, 0.8)  # Arial should have good Spanish support
        self.assertIsInstance(support.missing_chars, list)
    
    def test_get_best_spanish_fonts(self):
        """Test getting best Spanish fonts from available fonts"""
        # Use a small set of common fonts for testing
        test_fonts = ["Arial", "Times New Roman", "Courier New"]
        
        best_fonts = self.validator.get_best_spanish_fonts(test_fonts)
        
        self.assertIsInstance(best_fonts, list)
        self.assertGreater(len(best_fonts), 0)
        
        # Check that results are tuples of (font_name, quality_score)
        for font_name, quality_score in best_fonts:
            self.assertIsInstance(font_name, str)
            self.assertIsInstance(quality_score, float)
            self.assertGreaterEqual(quality_score, 0.0)
            self.assertLessEqual(quality_score, 1.0)
        
        # Check that results are sorted by quality (descending)
        scores = [score for _, score in best_fonts]
        self.assertEqual(scores, sorted(scores, reverse=True))


class TestFontManager(unittest.TestCase):
    """Test FontManager main class"""
    
    def setUp(self):
        # Create FontManager with temporary settings
        self.temp_dir = tempfile.mkdtemp()
        
        # Mock QSettings to use temporary location
        with patch('font_manager.QSettings') as mock_settings:
            mock_settings.return_value = self.create_temp_settings()
            self.font_manager = FontManager()
    
    def tearDown(self):
        # Clean up temporary directory
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def create_temp_settings(self):
        """Create temporary settings for testing"""
        settings = Mock()
        settings.value.return_value = None
        settings.setValue = Mock()
        settings.sync = Mock()
        return settings
    
    def test_font_manager_initialization(self):
        """Test FontManager initialization"""
        self.assertIsInstance(self.font_manager.dpi_manager, WindowsDPIManager)
        self.assertIsInstance(self.font_manager.spanish_validator, SpanishCharacterValidator)
        self.assertIsInstance(self.font_manager.available_fonts, list)
        self.assertIsInstance(self.font_manager.spanish_fonts, list)
        self.assertIsNotNone(self.font_manager.current_config)
    
    def test_get_font_basic(self):
        """Test basic font retrieval"""
        font = self.font_manager.get_font()
        
        self.assertIsInstance(font, QFont)
        self.assertGreater(font.pointSize(), 0)
        self.assertIsInstance(font.family(), str)
    
    def test_get_font_different_sizes(self):
        """Test getting fonts with different sizes"""
        sizes = ['tiny', 'small', 'normal', 'medium', 'large', 'extra_large', 'huge']
        
        fonts = {}
        for size_key in sizes:
            font = self.font_manager.get_font(size_key)
            fonts[size_key] = font.pointSize()
        
        # Check that sizes are generally increasing
        self.assertLess(fonts['tiny'], fonts['small'])
        self.assertLess(fonts['small'], fonts['normal'])
        self.assertLess(fonts['normal'], fonts['medium'])
        self.assertLess(fonts['medium'], fonts['large'])
    
    def test_get_font_weights_and_styles(self):
        """Test getting fonts with different weights and styles"""
        normal_font = self.font_manager.get_font(weight=QFont.Normal)
        bold_font = self.font_manager.get_font(weight=QFont.Bold)
        italic_font = self.font_manager.get_font(italic=True)
        
        self.assertEqual(normal_font.weight(), QFont.Normal)
        self.assertEqual(bold_font.weight(), QFont.Bold)
        self.assertTrue(italic_font.italic())
    
    def test_font_caching(self):
        """Test font caching functionality"""
        # Get the same font twice
        font1 = self.font_manager.get_font('normal')
        font2 = self.font_manager.get_font('normal')
        
        # Should return the same cached instance
        self.assertIs(font1, font2)
        
        # Check cache size
        self.assertGreater(len(self.font_manager._font_cache), 0)
    
    def test_set_base_font_size(self):
        """Test setting base font size"""
        original_size = self.font_manager.current_config.size
        new_size = 18
        
        self.font_manager.set_base_font_size(new_size)
        
        # Check that size was updated (accounting for DPI scaling)
        updated_size = self.font_manager.current_config.size
        expected_size = self.font_manager.dpi_manager.get_scaled_size(new_size)
        self.assertEqual(updated_size, expected_size)
    
    def test_get_recommended_fonts(self):
        """Test getting recommended fonts for Spanish"""
        recommended = self.font_manager.get_recommended_fonts()
        
        self.assertIsInstance(recommended, list)
        self.assertGreater(len(recommended), 0)
        
        # All recommended fonts should be strings
        for font_name in recommended:
            self.assertIsInstance(font_name, str)
    
    def test_get_available_fonts(self):
        """Test getting available fonts"""
        available = self.font_manager.get_available_fonts()
        
        self.assertIsInstance(available, list)
        self.assertGreater(len(available), 0)
        
        # Should contain common system fonts
        font_names = [name.lower() for name in available]
        self.assertTrue(any('arial' in name for name in font_names))
    
    def test_create_stylesheet_font_rules(self):
        """Test creating CSS font rules"""
        css_rules = self.font_manager.create_stylesheet_font_rules('medium')
        
        self.assertIsInstance(css_rules, str)
        self.assertIn('font-family:', css_rules)
        self.assertIn('font-size:', css_rules)
        self.assertIn('pt;', css_rules)
    
    def test_get_debug_info(self):
        """Test getting debug information"""
        debug_info = self.font_manager.get_debug_info()
        
        self.assertIsInstance(debug_info, dict)
        
        # Check required keys
        required_keys = [
            'current_config', 'system_dpi', 'dpi_scale', 
            'available_fonts_count', 'spanish_fonts_count',
            'platform', 'font_cache_size', 'metrics_cache_size'
        ]
        
        for key in required_keys:
            self.assertIn(key, debug_info)


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions"""
    
    def test_create_font_manager(self):
        """Test create_font_manager function"""
        with patch('font_manager.QSettings'):
            manager = create_font_manager()
            self.assertIsInstance(manager, FontManager)
    
    def test_get_spanish_optimized_font(self):
        """Test get_spanish_optimized_font function"""
        with patch('font_manager.QSettings'):
            font = get_spanish_optimized_font(16)
            
            self.assertIsInstance(font, QFont)
            # Size might be DPI-scaled, so just check it's reasonable
            self.assertGreaterEqual(font.pointSize(), 8)
            self.assertLessEqual(font.pointSize(), 50)
    
    def test_validate_spanish_font_support(self):
        """Test validate_spanish_font_support function"""
        support = validate_spanish_font_support("Arial")
        
        self.assertIsInstance(support, SpanishFontSupport)
        self.assertIsInstance(support.supports_spanish, bool)
        self.assertIsInstance(support.missing_chars, list)
        self.assertIsInstance(support.quality_score, float)


class TestFontManagerPerformance(unittest.TestCase):
    """Performance tests for FontManager"""
    
    def setUp(self):
        with patch('font_manager.QSettings'):
            self.font_manager = FontManager()
    
    def test_font_creation_performance(self):
        """Test performance of font creation"""
        import time
        
        start_time = time.time()
        
        # Create 100 fonts
        fonts = []
        for i in range(100):
            font = self.font_manager.get_font('normal')
            fonts.append(font)
        
        elapsed_time = time.time() - start_time
        
        # Should complete in reasonable time (less than 1 second)
        self.assertLess(elapsed_time, 1.0)
        
        # Check that caching is working (should have fewer unique fonts than requests)
        unique_fonts = set(id(font) for font in fonts)
        self.assertLessEqual(len(unique_fonts), 10)  # Caching should reduce unique instances
    
    def test_spanish_validation_performance(self):
        """Test performance of Spanish character validation"""
        import time
        
        validator = SpanishCharacterValidator()
        available_fonts = self.font_manager.get_available_fonts()
        test_fonts = available_fonts[:10]  # Test first 10 fonts
        
        start_time = time.time()
        
        results = []
        for font_name in test_fonts:
            font = QFont(font_name)
            result = validator.validate_spanish_support(font)
            results.append(result)
        
        elapsed_time = time.time() - start_time
        
        # Should complete validation of 10 fonts in reasonable time
        self.assertLess(elapsed_time, 5.0)
        
        # All results should be valid
        for result in results:
            self.assertIsInstance(result, SpanishFontSupport)


class TestFontManagerIntegration(unittest.TestCase):
    """Integration tests for FontManager with Qt widgets"""
    
    def setUp(self):
        with patch('font_manager.QSettings'):
            self.font_manager = FontManager()
        self.test_widget = QWidget()
    
    def test_apply_font_to_widget(self):
        """Test applying font to a Qt widget"""
        original_font = self.test_widget.font()
        
        # Apply font from manager
        self.font_manager.apply_font_to_widget(self.test_widget, 'large', QFont.Bold)
        
        new_font = self.test_widget.font()
        
        # Font should have changed
        self.assertNotEqual(original_font.family(), new_font.family())
        self.assertEqual(new_font.weight(), QFont.Bold)
    
    def test_get_font_metrics(self):
        """Test getting font metrics"""
        font = self.font_manager.get_font('normal')
        metrics = self.font_manager.get_font_metrics(font)
        
        from PyQt5.QtGui import QFontMetrics
        self.assertIsInstance(metrics, QFontMetrics)
        
        # Test metrics caching
        metrics2 = self.font_manager.get_font_metrics(font)
        self.assertIs(metrics, metrics2)  # Should be same cached instance


if __name__ == '__main__':
    # Set up logging for tests
    import logging
    logging.basicConfig(level=logging.WARNING)  # Reduce noise during tests
    
    # Run all tests
    unittest.main(verbosity=2)
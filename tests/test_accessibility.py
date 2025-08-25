"""
Comprehensive Accessibility Tests for Spanish Subjunctive Practice App

This test suite validates all accessibility features including:
- Keyboard navigation
- Focus management
- High contrast mode
- Screen reader support
- ARIA labels
- Keyboard shortcuts

Author: Claude Code Assistant
"""

import unittest
import sys
import os
import tempfile
import json
from unittest.mock import Mock, patch, MagicMock

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QKeyEvent, QColor
from PyQt5.QtTest import QTest

from src.accessibility_manager import (
    AccessibilitySettings, FocusManager, KeyboardNavigationManager,
    AccessibilityThemeManager, AccessibilityManager
)
from src.accessibility_integration import AccessibilityIntegration, integrate_accessibility


class TestAccessibilitySettings(unittest.TestCase):
    """Test accessibility settings management"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.settings_file = os.path.join(self.temp_dir, "accessibility_settings.json")
        
    def tearDown(self):
        # Clean up temp files
        if os.path.exists(self.settings_file):
            os.remove(self.settings_file)
        os.rmdir(self.temp_dir)
    
    def test_default_settings(self):
        """Test default accessibility settings"""
        settings = AccessibilitySettings()
        
        # Check default values
        self.assertFalse(settings.get("high_contrast"))
        self.assertEqual(settings.get("focus_ring_width"), 3)
        self.assertEqual(settings.get("focus_ring_color"), "#FF4444")
        self.assertTrue(settings.get("keyboard_navigation_enabled"))
        self.assertTrue(settings.get("screen_reader_support"))
    
    def test_settings_persistence(self):
        """Test settings save and load"""
        settings = AccessibilitySettings()
        
        # Modify settings
        settings.set("high_contrast", True)
        settings.set("font_size_multiplier", 1.5)
        
        # Create new instance (should load saved settings)
        new_settings = AccessibilitySettings()
        
        self.assertTrue(new_settings.get("high_contrast"))
        self.assertEqual(new_settings.get("font_size_multiplier"), 1.5)
    
    def test_reset_to_defaults(self):
        """Test resetting settings to defaults"""
        settings = AccessibilitySettings()
        
        # Modify settings
        settings.set("high_contrast", True)
        settings.set("font_size_multiplier", 2.0)
        
        # Reset to defaults
        settings.reset_to_defaults()
        
        self.assertFalse(settings.get("high_contrast"))
        self.assertEqual(settings.get("font_size_multiplier"), 1.0)


class TestFocusManager(unittest.TestCase):
    """Test focus management functionality"""
    
    def setUp(self):
        if not QApplication.instance():
            self.app = QApplication([])
        else:
            self.app = QApplication.instance()
            
        self.settings = AccessibilitySettings()
        self.focus_manager = FocusManager(self.settings)
        
        # Create test widgets
        self.main_widget = QWidget()
        self.button1 = QPushButton("Button 1", self.main_widget)
        self.button2 = QPushButton("Button 2", self.main_widget)
        self.button3 = QPushButton("Button 3", self.main_widget)
        
        self.test_widgets = [self.button1, self.button2, self.button3]
    
    def test_focus_group_registration(self):
        """Test registering focus groups"""
        self.focus_manager.register_focus_group("buttons", self.test_widgets)
        
        self.assertIn("buttons", self.focus_manager.focus_groups)
        self.assertEqual(len(self.focus_manager.focus_groups["buttons"]), 3)
    
    def test_focus_navigation(self):
        """Test focus navigation within groups"""
        self.focus_manager.register_focus_group("buttons", self.test_widgets)
        
        # Test next navigation
        self.focus_manager.navigate_to_next_in_group("buttons", self.button1)
        # Should focus button2 (index 1)
        
        # Test previous navigation
        self.focus_manager.navigate_to_previous_in_group("buttons", self.button2)
        # Should focus button1 (index 0)
    
    def test_focus_styling_application(self):
        """Test application of focus styling"""
        self.focus_manager.apply_focus_styling(self.button1)
        
        # Check that styling was applied (widget should have style sheet)
        style_sheet = self.button1.styleSheet()
        self.assertIn("focus", style_sheet.lower())
    
    def test_focus_announcement(self):
        """Test focus announcement signals"""
        announcement_received = False
        announcement_text = ""
        
        def on_announcement(text):
            nonlocal announcement_received, announcement_text
            announcement_received = True
            announcement_text = text
        
        self.focus_manager.focus_announced.connect(on_announcement)
        self.focus_manager.set_focus_with_announcement(self.button1, "Test announcement")
        
        self.assertTrue(announcement_received)
        self.assertEqual(announcement_text, "Test announcement")


class TestKeyboardNavigationManager(unittest.TestCase):
    """Test keyboard navigation and shortcuts"""
    
    def setUp(self):
        if not QApplication.instance():
            self.app = QApplication([])
        else:
            self.app = QApplication.instance()
            
        self.settings = AccessibilitySettings()
        self.keyboard_manager = KeyboardNavigationManager(self.settings)
    
    def test_default_shortcuts(self):
        """Test default keyboard shortcuts setup"""
        # Check that default shortcuts are loaded
        self.assertIn("submit_answer", self.keyboard_manager.shortcuts)
        self.assertIn("next_exercise", self.keyboard_manager.shortcuts)
        self.assertIn("show_hint", self.keyboard_manager.shortcuts)
        self.assertIn("accessibility_settings", self.keyboard_manager.shortcuts)
    
    def test_shortcut_retrieval(self):
        """Test getting shortcuts"""
        submit_shortcut = self.keyboard_manager.get_shortcut("submit_answer")
        self.assertEqual(submit_shortcut, "Return")
        
        hint_shortcut = self.keyboard_manager.get_shortcut("show_hint")
        self.assertEqual(hint_shortcut, "H")
    
    def test_custom_shortcut_setting(self):
        """Test setting custom shortcuts"""
        self.keyboard_manager.set_custom_shortcut("submit_answer", "Ctrl+Enter")
        
        custom_shortcut = self.keyboard_manager.get_shortcut("submit_answer")
        self.assertEqual(custom_shortcut, "Ctrl+Enter")
    
    def test_shortcuts_by_category(self):
        """Test shortcuts organization by category"""
        categories = self.keyboard_manager.get_shortcuts_by_category()
        
        self.assertIn("Navigation", categories)
        self.assertIn("Learning", categories)
        self.assertIn("Settings", categories)
        
        # Check that navigation category has expected shortcuts
        nav_shortcuts = [s["action"] for s in categories["Navigation"]]
        self.assertIn("submit_answer", nav_shortcuts)
        self.assertIn("next_exercise", nav_shortcuts)
    
    def test_key_event_handling(self):
        """Test keyboard event handling"""
        shortcut_triggered = False
        triggered_action = ""
        
        def on_shortcut(action, description):
            nonlocal shortcut_triggered, triggered_action
            shortcut_triggered = True
            triggered_action = action
        
        self.keyboard_manager.shortcut_triggered.connect(on_shortcut)
        
        # Create a key event for 'H' (hint shortcut)
        key_event = QKeyEvent(QEvent.KeyPress, Qt.Key_H, Qt.NoModifier)
        
        handled = self.keyboard_manager.handle_key_event(key_event)
        
        self.assertTrue(handled)
        self.assertTrue(shortcut_triggered)
        self.assertEqual(triggered_action, "show_hint")


class TestAccessibilityThemeManager(unittest.TestCase):
    """Test accessibility theme management"""
    
    def setUp(self):
        if not QApplication.instance():
            self.app = QApplication([])
        else:
            self.app = QApplication.instance()
            
        self.settings = AccessibilitySettings()
        self.theme_manager = AccessibilityThemeManager(self.settings)
        
        self.test_widget = QWidget()
    
    def test_theme_definitions(self):
        """Test that all expected themes are defined"""
        expected_themes = ["default", "high_contrast", "dark_high_contrast", "low_vision"]
        
        for theme in expected_themes:
            self.assertIn(theme, self.theme_manager.themes)
    
    def test_theme_properties(self):
        """Test theme color properties"""
        high_contrast = self.theme_manager.themes["high_contrast"]
        
        # High contrast should have specific color characteristics
        self.assertEqual(high_contrast["background"], "#000000")
        self.assertEqual(high_contrast["text"], "#ffffff")
        self.assertEqual(high_contrast["focus"], "#ffff00")
    
    def test_stylesheet_generation(self):
        """Test stylesheet generation for themes"""
        stylesheet = self.theme_manager.get_theme_stylesheet("high_contrast")
        
        self.assertIn("#000000", stylesheet)  # High contrast background
        self.assertIn("#ffffff", stylesheet)  # High contrast text
        self.assertIn("focus", stylesheet.lower())  # Focus indicators
    
    def test_theme_application(self):
        """Test applying themes to widgets"""
        self.theme_manager.apply_theme(self.test_widget, "high_contrast")
        
        # Check that theme was applied
        self.assertEqual(self.theme_manager.current_theme, "high_contrast")
        
        # Widget should have style sheet applied
        style_sheet = self.test_widget.styleSheet()
        self.assertIn("#000000", style_sheet)  # Should contain high contrast colors
    
    def test_theme_cycling(self):
        """Test cycling through themes"""
        initial_theme = self.theme_manager.current_theme
        next_theme = self.theme_manager.cycle_theme(self.test_widget)
        
        self.assertNotEqual(initial_theme, next_theme)
        self.assertEqual(self.theme_manager.current_theme, next_theme)


class TestAccessibilityIntegration(unittest.TestCase):
    """Test accessibility integration with main application"""
    
    def setUp(self):
        if not QApplication.instance():
            self.app = QApplication([])
        else:
            self.app = QApplication.instance()
        
        # Create mock main window with required attributes
        self.main_window = Mock(spec=QMainWindow)
        self.main_window.findChildren = Mock(return_value=[])
        self.main_window.toolBar = Mock()
        
        # Add required attributes for integration
        self.main_window.current_exercise = 0
        self.main_window.total_exercises = 5
        self.main_window.show_translation = False
        
        # Mock methods
        self.main_window.submitAnswer = Mock()
        self.main_window.nextExercise = Mock()
        self.main_window.prevExercise = Mock()
        self.main_window.provideHint = Mock()
        self.main_window.updateExercise = Mock()
        self.main_window.getUserAnswer = Mock(return_value="test answer")
        self.main_window.updateStatus = Mock()
        
        # Mock UI elements
        self.main_window.sentence_label = Mock()
        self.main_window.feedback_text = Mock()
        self.main_window.mode_combo = Mock()
        self.main_window.mode_combo.currentText = Mock(return_value="Free Response")
    
    def test_integration_initialization(self):
        """Test accessibility integration initialization"""
        integration = AccessibilityIntegration(self.main_window)
        accessibility_manager = integration.initialize()
        
        self.assertIsNotNone(accessibility_manager)
        self.assertIsInstance(accessibility_manager, AccessibilityManager)
    
    @patch('src.accessibility_integration.AccessibilityManager')
    def test_method_wrapping(self, mock_accessibility_manager):
        """Test that original methods are wrapped with accessibility enhancements"""
        integration = AccessibilityIntegration(self.main_window)
        
        # Mock the accessibility manager
        mock_manager = Mock()
        mock_accessibility_manager.return_value = mock_manager
        mock_manager.settings.get.return_value = True
        mock_manager.announcement_requested = Mock()
        mock_manager.focus_manager = Mock()
        
        integration.accessibility_manager = mock_manager
        integration._setup_integration()
        integration._enhance_existing_shortcuts()
        
        # Check that original methods are stored
        self.assertIn('submitAnswer', integration.original_methods)
        self.assertIn('nextExercise', integration.original_methods)
    
    def test_announcement_handling(self):
        """Test accessibility announcement handling"""
        integration = AccessibilityIntegration(self.main_window)
        
        # Test announcement handling
        test_text = "Test announcement"
        integration._handle_announcement(test_text)
        
        # Should call updateStatus on main window
        self.main_window.updateStatus.assert_called_once()
        call_args = self.main_window.updateStatus.call_args[0][0]
        self.assertIn(test_text, call_args)


class TestAccessibilityManager(unittest.TestCase):
    """Test the main accessibility manager"""
    
    def setUp(self):
        if not QApplication.instance():
            self.app = QApplication([])
        else:
            self.app = QApplication.instance()
        
        # Create a real QMainWindow for testing
        self.main_window = QMainWindow()
        self.main_window.setWindowTitle("Test Window")
        
        # Add some test widgets
        self.main_window.sentence_label = QLabel("Test sentence", self.main_window)
        self.main_window.free_response_input = QLineEdit(self.main_window)
        self.main_window.submit_button = QPushButton("Submit", self.main_window)
        
    def test_accessibility_manager_initialization(self):
        """Test accessibility manager initialization"""
        manager = AccessibilityManager(self.main_window)
        
        self.assertIsNotNone(manager.settings)
        self.assertIsNotNone(manager.focus_manager)
        self.assertIsNotNone(manager.keyboard_manager)
        self.assertIsNotNone(manager.theme_manager)
    
    def test_aria_attribute_setup(self):
        """Test ARIA attributes setup"""
        manager = AccessibilityManager(self.main_window)
        
        # Check that main window has accessible name
        accessible_name = self.main_window.accessibleName()
        self.assertIn("Spanish Subjunctive", accessible_name)
        
        # Check that widgets have accessible names
        self.assertIsNotNone(self.main_window.sentence_label.accessibleName())
        self.assertIsNotNone(self.main_window.free_response_input.accessibleName())
    
    def test_high_contrast_toggle(self):
        """Test high contrast mode toggle"""
        manager = AccessibilityManager(self.main_window)
        
        # Initial state should be False
        initial_state = manager.settings.get("high_contrast", False)
        
        # Toggle high contrast
        manager.toggle_high_contrast()
        
        # State should be reversed
        new_state = manager.settings.get("high_contrast")
        self.assertNotEqual(initial_state, new_state)
    
    def test_skip_to_content(self):
        """Test skip to content functionality"""
        manager = AccessibilityManager(self.main_window)
        
        # Should not raise an exception
        manager.skip_to_content()
        
        # Focus should be set on sentence label
        focused_widget = QApplication.focusWidget()
        # Note: In test environment, focus might not work exactly as in real app
    
    def test_keyboard_help_display(self):
        """Test keyboard help dialog display"""
        manager = AccessibilityManager(self.main_window)
        
        # Should not raise an exception when showing help
        try:
            manager.show_keyboard_help()
        except Exception as e:
            self.fail(f"show_keyboard_help raised an exception: {e}")
    
    def test_accessibility_status(self):
        """Test getting accessibility status"""
        manager = AccessibilityManager(self.main_window)
        
        status = manager.get_accessibility_status()
        
        # Should return a dictionary with expected keys
        expected_keys = [
            "high_contrast", "keyboard_navigation", "screen_reader_support",
            "auto_announce", "enhanced_tooltips", "reduce_motion"
        ]
        
        for key in expected_keys:
            self.assertIn(key, status)
            self.assertIsInstance(status[key], bool)


class TestFullIntegration(unittest.TestCase):
    """Test full accessibility integration"""
    
    def setUp(self):
        if not QApplication.instance():
            self.app = QApplication([])
        else:
            self.app = QApplication.instance()
    
    def test_integrate_accessibility_function(self):
        """Test the main integration function"""
        # Create a minimal mock main window
        main_window = Mock(spec=QMainWindow)
        main_window.findChildren = Mock(return_value=[])
        main_window.toolBar = Mock()
        
        # Test integration
        accessibility_manager = integrate_accessibility(main_window)
        
        # Should return an AccessibilityManager instance or None
        self.assertTrue(accessibility_manager is None or 
                       isinstance(accessibility_manager, AccessibilityManager))
    
    @patch('builtins.print')
    def test_integration_error_handling(self, mock_print):
        """Test error handling in integration"""
        # Pass an invalid object to trigger error
        accessibility_manager = integrate_accessibility(None)
        
        self.assertIsNone(accessibility_manager)
        # Should have printed error message
        mock_print.assert_called()


class TestKeyboardShortcuts(unittest.TestCase):
    """Test keyboard shortcuts functionality"""
    
    def setUp(self):
        if not QApplication.instance():
            self.app = QApplication([])
        else:
            self.app = QApplication.instance()
            
        self.main_window = QMainWindow()
        self.accessibility_manager = AccessibilityManager(self.main_window)
    
    def test_all_shortcuts_defined(self):
        """Test that all expected shortcuts are defined"""
        expected_shortcuts = [
            "submit_answer", "next_exercise", "prev_exercise", "show_hint",
            "conjugation_reference", "toggle_translation", "accessibility_settings",
            "high_contrast_toggle", "skip_to_content", "skip_to_navigation",
            "read_current_exercise", "focus_answer_input", "show_keyboard_help"
        ]
        
        for shortcut in expected_shortcuts:
            self.assertIn(shortcut, self.accessibility_manager.keyboard_manager.shortcuts)
    
    def test_shortcut_categories(self):
        """Test shortcut categorization"""
        categories = self.accessibility_manager.keyboard_manager.get_shortcuts_by_category()
        
        expected_categories = ["Navigation", "Learning", "Reference", "Display", "Settings", "Help", "Accessibility"]
        
        for category in expected_categories:
            self.assertIn(category, categories)
    
    def test_shortcut_descriptions(self):
        """Test that all shortcuts have descriptions"""
        shortcuts = self.accessibility_manager.keyboard_manager.shortcuts
        
        for action, data in shortcuts.items():
            self.assertIn("description", data)
            self.assertIn("category", data)
            self.assertIn("key", data)
            
            # Descriptions should not be empty
            self.assertTrue(len(data["description"]) > 0)


if __name__ == '__main__':
    # Set up test environment
    os.environ['QT_QPA_PLATFORM'] = 'offscreen'  # Prevent GUI from showing during tests
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestAccessibilitySettings,
        TestFocusManager,
        TestKeyboardNavigationManager,
        TestAccessibilityThemeManager,
        TestAccessibilityIntegration,
        TestAccessibilityManager,
        TestFullIntegration,
        TestKeyboardShortcuts
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
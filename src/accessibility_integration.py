"""
Accessibility Integration Module

This module provides integration functions to seamlessly incorporate accessibility
features into the existing Spanish Subjunctive Practice application.

Author: Claude Code Assistant
"""

from typing import Dict, Any, Optional
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QMessageBox
from PyQt5.QtCore import QObject, QEvent, Qt
from PyQt5.QtGui import QKeyEvent

from src.accessibility_manager import AccessibilityManager


class AccessibilityIntegration:
    """Handles integration of accessibility features with the main application"""
    
    def __init__(self, main_window: QMainWindow):
        self.main_window = main_window
        self.accessibility_manager = None
        self.original_methods = {}  # Store original method references
        
    def initialize(self) -> AccessibilityManager:
        """Initialize accessibility features"""
        try:
            self.accessibility_manager = AccessibilityManager(self.main_window)
            self._setup_integration()
            self._enhance_existing_shortcuts()
            self._add_accessibility_menu_items()
            return self.accessibility_manager
        except Exception as e:
            print(f"Error initializing accessibility: {e}")
            return None
    
    def _setup_integration(self) -> None:
        """Set up integration hooks"""
        if not self.accessibility_manager:
            return
        
        # Connect accessibility manager signals to main window handlers
        self.accessibility_manager.announcement_requested.connect(self._handle_announcement)
        self.accessibility_manager.accessibility_changed.connect(self._handle_accessibility_change)
        
        # Add accessibility-specific handlers to main window
        self._add_accessibility_handlers()
    
    def _enhance_existing_shortcuts(self) -> None:
        """Enhance existing keyboard shortcuts with accessibility features"""
        if not self.accessibility_manager:
            return
        
        # Store original methods and wrap them with accessibility enhancements
        self._wrap_method('submitAnswer', self._enhanced_submit_answer)
        self._wrap_method('nextExercise', self._enhanced_next_exercise) 
        self._wrap_method('prevExercise', self._enhanced_prev_exercise)
        self._wrap_method('provideHint', self._enhanced_provide_hint)
        self._wrap_method('updateExercise', self._enhanced_update_exercise)
        self._wrap_method('handleNewExerciseResult', self._enhanced_handle_new_exercise_result)
    
    def _wrap_method(self, method_name: str, wrapper_func) -> None:
        """Wrap existing method with accessibility enhancements"""
        if hasattr(self.main_window, method_name):
            original_method = getattr(self.main_window, method_name)
            self.original_methods[method_name] = original_method
            setattr(self.main_window, method_name, lambda *args, **kwargs: wrapper_func(original_method, *args, **kwargs))
    
    def _enhanced_submit_answer(self, original_method, *args, **kwargs):
        """Enhanced submit answer with accessibility announcements"""
        result = original_method(*args, **kwargs)
        
        # Announce submission
        if self.accessibility_manager.settings.get("auto_announce"):
            user_answer = self.main_window.getUserAnswer()
            self.accessibility_manager.announcement_requested.emit(
                f"Answer submitted: {user_answer}"
            )
        
        # Focus management after submission
        if hasattr(self.main_window, 'feedback_text'):
            self.accessibility_manager.focus_manager.set_focus_with_announcement(
                self.main_window.feedback_text,
                "Review your answer feedback"
            )
        
        return result
    
    def _enhanced_next_exercise(self, original_method, *args, **kwargs):
        """Enhanced next exercise with accessibility features"""
        old_exercise = self.main_window.current_exercise
        result = original_method(*args, **kwargs)
        
        # Announce exercise change
        if (self.accessibility_manager.settings.get("auto_announce") and 
            self.main_window.current_exercise != old_exercise):
            exercise_num = self.main_window.current_exercise + 1
            total_exercises = self.main_window.total_exercises
            
            self.accessibility_manager.announcement_requested.emit(
                f"Exercise {exercise_num} of {total_exercises}"
            )
            
            # Auto-focus on exercise content
            if hasattr(self.main_window, 'sentence_label'):
                self.accessibility_manager.focus_manager.set_focus_with_announcement(
                    self.main_window.sentence_label,
                    "New exercise loaded"
                )
        
        return result
    
    def _enhanced_prev_exercise(self, original_method, *args, **kwargs):
        """Enhanced previous exercise with accessibility features"""
        old_exercise = self.main_window.current_exercise
        result = original_method(*args, **kwargs)
        
        # Announce exercise change
        if (self.accessibility_manager.settings.get("auto_announce") and 
            self.main_window.current_exercise != old_exercise):
            exercise_num = self.main_window.current_exercise + 1
            total_exercises = self.main_window.total_exercises
            
            self.accessibility_manager.announcement_requested.emit(
                f"Exercise {exercise_num} of {total_exercises}"
            )
        
        return result
    
    def _enhanced_provide_hint(self, original_method, *args, **kwargs):
        """Enhanced hint provision with accessibility announcements"""
        result = original_method(*args, **kwargs)
        
        # Announce hint availability
        if self.accessibility_manager.settings.get("auto_announce"):
            self.accessibility_manager.announcement_requested.emit(
                "Hint requested. Check the feedback area for guidance."
            )
            
            # Focus on feedback area after hint is loaded
            if hasattr(self.main_window, 'feedback_text'):
                # Use a timer to focus after the GPT response is loaded
                from PyQt5.QtCore import QTimer
                QTimer.singleShot(1000, lambda: self.accessibility_manager.focus_manager.set_focus_with_announcement(
                    self.main_window.feedback_text,
                    "Hint available in feedback area"
                ))
        
        return result
    
    def _enhanced_update_exercise(self, original_method, *args, **kwargs):
        """Enhanced update exercise with accessibility features"""
        result = original_method(*args, **kwargs)
        
        # Apply accessibility styling to newly created elements
        if hasattr(self.main_window, 'input_stack'):
            self.accessibility_manager.focus_manager.apply_focus_styling(self.main_window.input_stack)
        
        # Announce mode changes
        mode = self.main_window.mode_combo.currentText()
        if self.accessibility_manager.settings.get("auto_announce"):
            self.accessibility_manager.announcement_requested.emit(f"Exercise mode: {mode}")
        
        return result
    
    def _enhanced_handle_new_exercise_result(self, original_method, result, *args, **kwargs):
        """Enhanced new exercise result handling with accessibility features"""
        original_result = original_method(result, *args, **kwargs)
        
        # Announce new exercises generated
        if (self.accessibility_manager.settings.get("auto_announce") and 
            hasattr(self.main_window, 'total_exercises') and 
            self.main_window.total_exercises > 0):
            
            self.accessibility_manager.announcement_requested.emit(
                f"{self.main_window.total_exercises} new exercises generated. Starting with exercise 1."
            )
            
            # Auto-focus on first exercise
            if hasattr(self.main_window, 'sentence_label'):
                self.accessibility_manager.focus_manager.set_focus_with_announcement(
                    self.main_window.sentence_label,
                    "First exercise ready"
                )
        
        return original_result
    
    def _add_accessibility_handlers(self) -> None:
        """Add accessibility-specific handler methods to main window"""
        # Handler for accessibility settings shortcut
        def handle_accessibility_settings():
            self.accessibility_manager.show_accessibility_settings()
        
        # Handler for high contrast toggle
        def handle_high_contrast_toggle():
            self.accessibility_manager.toggle_high_contrast()
        
        # Handler for skip to content
        def handle_skip_to_content():
            self.accessibility_manager.skip_to_content()
        
        # Handler for skip to navigation
        def handle_skip_to_navigation():
            self.accessibility_manager.skip_to_navigation()
        
        # Handler for read current exercise
        def handle_read_current_exercise():
            self.accessibility_manager.read_current_exercise()
        
        # Handler for focus answer input
        def handle_focus_answer_input():
            self.accessibility_manager.focus_answer_input()
        
        # Handler for show keyboard help
        def handle_show_keyboard_help():
            self.accessibility_manager.show_keyboard_help()
        
        # Handler for toggle translation with announcement
        def handle_toggle_translation():
            if hasattr(self.main_window, 'toggleTranslation'):
                self.original_methods.get('toggleTranslation', self.main_window.toggleTranslation)()
            
            # Announce translation state
            show_translation = getattr(self.main_window, 'show_translation', False)
            self.accessibility_manager.announcement_requested.emit(
                f"Translation {'shown' if show_translation else 'hidden'}"
            )
        
        # Add handlers to main window
        setattr(self.main_window, 'handle_accessibility_settings', handle_accessibility_settings)
        setattr(self.main_window, 'handle_high_contrast_toggle', handle_high_contrast_toggle)
        setattr(self.main_window, 'handle_skip_to_content', handle_skip_to_content)
        setattr(self.main_window, 'handle_skip_to_navigation', handle_skip_to_navigation)
        setattr(self.main_window, 'handle_read_current_exercise', handle_read_current_exercise)
        setattr(self.main_window, 'handle_focus_answer_input', handle_focus_answer_input)
        setattr(self.main_window, 'handle_show_keyboard_help', handle_show_keyboard_help)
        setattr(self.main_window, 'handle_toggle_translation', handle_toggle_translation)
    
    def _add_accessibility_menu_items(self) -> None:
        """Add accessibility items to the toolbar"""
        if not hasattr(self.main_window, 'createToolBar'):
            return
        
        try:
            # Get the existing toolbar
            toolbar = None
            for toolbar_widget in self.main_window.findChildren(QWidget):
                if toolbar_widget.objectName() == "MainToolBar" or isinstance(toolbar_widget, type(self.main_window.toolBar())):
                    toolbar = toolbar_widget
                    break
            
            if not toolbar:
                toolbar = self.main_window.toolBar()
            
            # Add separator
            toolbar.addSeparator()
            
            # Add accessibility menu items
            from PyQt5.QtWidgets import QAction
            
            accessibility_action = QAction("Accessibility Settings", self.main_window)
            accessibility_action.setToolTip("Configure accessibility options (Ctrl+Alt+A)")
            accessibility_action.setShortcut("Ctrl+Alt+A")
            accessibility_action.triggered.connect(self.accessibility_manager.show_accessibility_settings)
            toolbar.addAction(accessibility_action)
            
            high_contrast_action = QAction("High Contrast", self.main_window)
            high_contrast_action.setToolTip("Toggle high contrast mode (Ctrl+Alt+H)")
            high_contrast_action.setShortcut("Ctrl+Alt+H")
            high_contrast_action.triggered.connect(self.accessibility_manager.toggle_high_contrast)
            toolbar.addAction(high_contrast_action)
            
            keyboard_help_action = QAction("Keyboard Help", self.main_window)
            keyboard_help_action.setToolTip("Show keyboard shortcuts (F1)")
            keyboard_help_action.setShortcut("F1")
            keyboard_help_action.triggered.connect(self.accessibility_manager.show_keyboard_help)
            toolbar.addAction(keyboard_help_action)
            
        except Exception as e:
            print(f"Error adding accessibility menu items: {e}")
    
    def _handle_announcement(self, text: str) -> None:
        """Handle accessibility announcements"""
        # In a real implementation, this would interface with screen readers
        # For now, we'll use the status bar or console
        if hasattr(self.main_window, 'updateStatus'):
            self.main_window.updateStatus(f"🔊 {text}")
        else:
            print(f"Accessibility: {text}")
    
    def _handle_accessibility_change(self, feature: str, enabled: bool) -> None:
        """Handle accessibility feature changes"""
        status = "enabled" if enabled else "disabled"
        self._handle_announcement(f"{feature.replace('_', ' ').title()} {status}")


def integrate_accessibility(main_window: QMainWindow) -> Optional[AccessibilityManager]:
    """
    Main function to integrate accessibility features into the application.
    
    Args:
        main_window: The main application window
        
    Returns:
        AccessibilityManager instance if successful, None otherwise
    """
    try:
        integration = AccessibilityIntegration(main_window)
        accessibility_manager = integration.initialize()
        
        if accessibility_manager:
            print("Accessibility features successfully integrated")
            return accessibility_manager
        else:
            print("Failed to initialize accessibility features")
            return None
            
    except Exception as e:
        print(f"Error integrating accessibility: {e}")
        return None


def add_accessibility_startup_check(main_window: QMainWindow, accessibility_manager: AccessibilityManager) -> None:
    """
    Add accessibility status check on application startup.
    
    Args:
        main_window: The main application window
        accessibility_manager: The accessibility manager instance
    """
    try:
        # Check if this is first run with accessibility
        settings = accessibility_manager.settings
        
        if not settings.get("accessibility_intro_shown", False):
            # Show accessibility introduction
            from PyQt5.QtWidgets import QMessageBox
            
            msg = QMessageBox(main_window)
            msg.setWindowTitle("Accessibility Features Available")
            msg.setIcon(QMessageBox.Information)
            msg.setText(
                "This application includes comprehensive accessibility features:\n\n"
                "• Enhanced keyboard navigation (Tab/Shift+Tab)\n"
                "• High contrast mode (Ctrl+Alt+H)\n"
                "• Screen reader support with announcements\n"
                "• Customizable focus indicators\n"
                "• Keyboard shortcuts help (F1)\n"
                "• Accessibility settings (Ctrl+Alt+A)\n\n"
                "Press F1 anytime to see all keyboard shortcuts.\n"
                "Access settings through Ctrl+Alt+A or the toolbar."
            )
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setAccessibleName("Accessibility Features Introduction")
            msg.setAccessibleDescription("Information about available accessibility features")
            
            # Add "Don't show again" option
            dont_show_checkbox = QCheckBox("Don't show this message again")
            dont_show_checkbox.setAccessibleDescription("Check to skip this message on startup")
            msg.setCheckBox(dont_show_checkbox)
            
            msg.exec_()
            
            # Save preference
            if dont_show_checkbox.isChecked():
                settings.set("accessibility_intro_shown", True)
        
        # Apply saved accessibility preferences
        if settings.get("high_contrast", False):
            accessibility_manager.theme_manager.apply_theme(main_window, "high_contrast")
        
        # Announce ready status
        if settings.get("auto_announce", True):
            accessibility_manager.announcement_requested.emit(
                "Spanish Subjunctive Practice application ready. Press F1 for keyboard shortcuts."
            )
            
    except Exception as e:
        print(f"Error in accessibility startup check: {e}")


def create_quick_accessibility_widget(parent: QWidget = None) -> QWidget:
    """
    Create a quick accessibility widget for immediate access to common features.
    
    Args:
        parent: Parent widget
        
    Returns:
        Widget with accessibility quick controls
    """
    from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
    
    widget = QWidget(parent)
    widget.setAccessibleName("Quick Accessibility Controls")
    layout = QHBoxLayout(widget)
    layout.setContentsMargins(4, 4, 4, 4)
    
    # High contrast toggle
    hc_button = QPushButton("🌗")
    hc_button.setToolTip("Toggle High Contrast (Ctrl+Alt+H)")
    hc_button.setMaximumSize(40, 30)
    hc_button.setAccessibleName("High Contrast Toggle")
    hc_button.setAccessibleDescription("Toggle high contrast mode for better visibility")
    layout.addWidget(hc_button)
    
    # Font size controls
    font_smaller_btn = QPushButton("A-")
    font_smaller_btn.setToolTip("Decrease Font Size")
    font_smaller_btn.setMaximumSize(40, 30)
    font_smaller_btn.setAccessibleName("Decrease Font Size")
    layout.addWidget(font_smaller_btn)
    
    font_larger_btn = QPushButton("A+")
    font_larger_btn.setToolTip("Increase Font Size")
    font_larger_btn.setMaximumSize(40, 30)
    font_larger_btn.setAccessibleName("Increase Font Size")
    layout.addWidget(font_larger_btn)
    
    # Keyboard help
    help_button = QPushButton("⌨")
    help_button.setToolTip("Keyboard Shortcuts (F1)")
    help_button.setMaximumSize(40, 30)
    help_button.setAccessibleName("Keyboard Help")
    help_button.setAccessibleDescription("Show keyboard shortcuts help")
    layout.addWidget(help_button)
    
    # Settings
    settings_button = QPushButton("⚙")
    settings_button.setToolTip("Accessibility Settings (Ctrl+Alt+A)")
    settings_button.setMaximumSize(40, 30)
    settings_button.setAccessibleName("Accessibility Settings")
    settings_button.setAccessibleDescription("Open accessibility settings dialog")
    layout.addWidget(settings_button)
    
    return widget
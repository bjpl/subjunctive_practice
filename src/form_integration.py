"""
Form Styling Integration Module

This module integrates the form styling fixes into the main Spanish Subjunctive Practice application.
It provides a clean interface to apply all the form improvements and handles the integration
with existing code.
"""

import logging
from typing import Optional
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QComboBox, QCheckBox, QRadioButton, QTextEdit
from PyQt5.QtCore import QTimer

try:
    from src.form_styling_fixes import FormStylingManager, apply_form_styling_fixes, create_form_state_manager, fix_form_red_boxes
except ImportError:
    from form_styling_fixes import FormStylingManager, apply_form_styling_fixes, create_form_state_manager, fix_form_red_boxes

logger = logging.getLogger(__name__)


class FormIntegrationManager:
    """
    Manages the integration of form styling fixes into the main application.
    Provides a clean interface for applying fixes and handling dynamic updates.
    """
    
    def __init__(self, app: QApplication, main_window: QMainWindow):
        self.app = app
        self.main_window = main_window
        self.styling_manager: Optional[FormStylingManager] = None
        self.form_state_manager = None
        self.dark_mode = False
        
        # Timer for responsive updates
        self.resize_timer = QTimer()
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self._handle_resize_complete)
        
        logger.info("Form Integration Manager initialized")
    
    def initialize_form_styling(self, dark_mode: bool = False):
        """
        Initialize and apply all form styling fixes to the application.
        
        Args:
            dark_mode: Whether to use dark theme styling
        """
        try:
            self.dark_mode = dark_mode
            
            # Apply the comprehensive form styling fixes
            self.styling_manager = apply_form_styling_fixes(
                self.app, 
                self.main_window, 
                dark_mode
            )
            
            # Create form state manager for validation styling
            self.form_state_manager = create_form_state_manager(self.styling_manager)
            
            # Connect to window resize events for responsive behavior
            self._setup_responsive_behavior()
            
            # Apply specific fixes to known problematic elements
            self._apply_specific_fixes()
            
            logger.info("Form styling initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize form styling: {e}")
            return False
    
    def _setup_responsive_behavior(self):
        """
        Setup responsive behavior for form elements when window is resized.
        """
        # Store original resize event
        original_resize_event = self.main_window.resizeEvent
        
        def enhanced_resize_event(event):
            # Call original resize event
            original_resize_event(event)
            
            # Trigger responsive update with debouncing
            self.resize_timer.stop()
            self.resize_timer.start(150)  # 150ms debounce
        
        # Replace resize event
        self.main_window.resizeEvent = enhanced_resize_event
        
        logger.debug("Responsive behavior setup completed")
    
    def _handle_resize_complete(self):
        """
        Handle window resize completion - apply responsive styling updates.
        """
        try:
            window_width = self.main_window.width()
            
            # Update all form elements for new window size
            for widget in self.main_window.findChildren((QLineEdit, QComboBox, QTextEdit, QCheckBox, QRadioButton)):
                if self.styling_manager:
                    self.styling_manager.apply_responsive_sizing(widget, window_width)
            
            logger.debug(f"Applied responsive styling for window width: {window_width}")
            
        except Exception as e:
            logger.error(f"Error handling resize: {e}")
    
    def _apply_specific_fixes(self):
        """
        Apply specific fixes to problematic form elements identified in the main application.
        """
        try:
            # Fix the specific elements mentioned in the main.py file
            
            # 1. Fix trigger checkboxes (these likely have the red box issue)
            trigger_checkboxes = getattr(self.main_window, 'trigger_checkboxes', [])
            for checkbox in trigger_checkboxes:
                self._fix_checkbox_styling(checkbox)
            
            # 2. Fix tense and person checkboxes
            tense_checkboxes = getattr(self.main_window, 'tense_checkboxes', {})
            for checkbox in tense_checkboxes.values():
                self._fix_checkbox_styling(checkbox)
            
            person_checkboxes = getattr(self.main_window, 'person_checkboxes', {})
            for checkbox in person_checkboxes.values():
                self._fix_checkbox_styling(checkbox)
            
            # 3. Fix input fields
            if hasattr(self.main_window, 'free_response_input'):
                self._fix_input_field(self.main_window.free_response_input)
            
            if hasattr(self.main_window, 'custom_context_input'):
                self._fix_input_field(self.main_window.custom_context_input)
            
            if hasattr(self.main_window, 'verbs_input'):
                self._fix_input_field(self.main_window.verbs_input)
            
            # 4. Fix combo boxes
            combo_boxes = [
                'mode_combo', 
                'difficulty_combo', 
                'task_type_combo'
            ]
            for combo_name in combo_boxes:
                if hasattr(self.main_window, combo_name):
                    combo = getattr(self.main_window, combo_name)
                    self._fix_combo_box(combo)
            
            # 5. Fix text edit areas
            if hasattr(self.main_window, 'feedback_text'):
                self._fix_text_edit(self.main_window.feedback_text)
            
            logger.info("Applied specific fixes to form elements")
            
        except Exception as e:
            logger.error(f"Error applying specific fixes: {e}")
    
    def _fix_checkbox_styling(self, checkbox: QCheckBox):
        """Fix styling for a specific checkbox to remove red box issues."""
        try:
            # Apply neutral state styling
            if self.form_state_manager:
                self.form_state_manager(checkbox, 'neutral')
            
            # Ensure responsive sizing
            if self.styling_manager:
                self.styling_manager.apply_responsive_sizing(checkbox, self.main_window.width())
            
        except Exception as e:
            logger.debug(f"Error fixing checkbox styling: {e}")
    
    def _fix_input_field(self, input_field: QLineEdit):
        """Fix styling for a specific input field."""
        try:
            # Apply neutral state styling
            if self.form_state_manager:
                self.form_state_manager(input_field, 'neutral')
            
            # Ensure responsive sizing and good contrast
            if self.styling_manager:
                self.styling_manager.apply_responsive_sizing(input_field, self.main_window.width())
                
        except Exception as e:
            logger.debug(f"Error fixing input field styling: {e}")
    
    def _fix_combo_box(self, combo_box: QComboBox):
        """Fix styling for a specific combo box."""
        try:
            # Apply responsive sizing
            if self.styling_manager:
                self.styling_manager.apply_responsive_sizing(combo_box, self.main_window.width())
                
        except Exception as e:
            logger.debug(f"Error fixing combo box styling: {e}")
    
    def _fix_text_edit(self, text_edit: QTextEdit):
        """Fix styling for a specific text edit area."""
        try:
            # Apply responsive sizing and improved visibility
            if self.styling_manager:
                self.styling_manager.apply_responsive_sizing(text_edit, self.main_window.width())
                
        except Exception as e:
            logger.debug(f"Error fixing text edit styling: {e}")
    
    def set_form_validation_state(self, widget: QWidget, state: str, message: str = ""):
        """
        Set validation state for a form widget with improved styling.
        
        Args:
            widget: The form widget
            state: 'success', 'error', 'warning', 'neutral' 
            message: Optional message for tooltip
        """
        if self.form_state_manager:
            self.form_state_manager(widget, state, message)
            logger.debug(f"Applied {state} validation state to widget")
    
    def toggle_dark_mode(self):
        """
        Toggle between light and dark mode styling.
        """
        try:
            self.dark_mode = not self.dark_mode
            
            # Reinitialize styling with new theme
            self.initialize_form_styling(self.dark_mode)
            
            logger.info(f"Toggled to {'dark' if self.dark_mode else 'light'} mode")
            return self.dark_mode
            
        except Exception as e:
            logger.error(f"Error toggling dark mode: {e}")
            return self.dark_mode
    
    def refresh_styling(self):
        """
        Refresh all form styling - useful after dynamic UI changes.
        """
        try:
            # Reapply specific fixes
            self._apply_specific_fixes()
            
            # Trigger responsive update
            self._handle_resize_complete()
            
            logger.debug("Form styling refreshed")
            
        except Exception as e:
            logger.error(f"Error refreshing styling: {e}")
    
    def get_current_theme(self) -> str:
        """Get the current theme name."""
        return 'dark' if self.dark_mode else 'light'


def integrate_form_fixes(app: QApplication, main_window: QMainWindow, dark_mode: bool = False) -> FormIntegrationManager:
    """
    Main integration function to apply form styling fixes to the Spanish Subjunctive Practice app.
    
    This function should be called during the application initialization to fix:
    1. Red box form selector issues
    2. Text visibility problems
    3. Poor responsive behavior
    4. Missing hover/focus states
    
    Args:
        app: The QApplication instance
        main_window: The main window instance
        dark_mode: Whether to use dark theme
    
    Returns:
        FormIntegrationManager instance for ongoing management
    """
    try:
        # Create integration manager
        integration_manager = FormIntegrationManager(app, main_window)
        
        # Initialize form styling
        success = integration_manager.initialize_form_styling(dark_mode)
        
        if success:
            logger.info("Form styling integration completed successfully")
        else:
            logger.warning("Form styling integration completed with errors")
        
        return integration_manager
        
    except Exception as e:
        logger.error(f"Failed to integrate form fixes: {e}")
        # Return a dummy manager to prevent crashes
        return FormIntegrationManager(app, main_window)


def quick_fix_red_boxes(app: QApplication):
    """
    Quick fix function to immediately address red box issues.
    Can be called as a hotfix while the full integration is being applied.
    """
    try:
        fix_form_red_boxes(app)
        logger.info("Quick red box fix applied")
    except Exception as e:
        logger.error(f"Quick red box fix failed: {e}")


# Integration helper for existing code
def patch_main_window_form_styling(main_window):
    """
    Patch the main window to apply form styling fixes.
    This can be called from the existing main.py file.
    """
    try:
        # Get the application instance
        app = QApplication.instance()
        if not app:
            logger.error("No QApplication instance found")
            return None
        
        # Apply quick red box fix immediately
        quick_fix_red_boxes(app)
        
        # Create and return integration manager
        integration_manager = integrate_form_fixes(app, main_window)
        
        return integration_manager
        
    except Exception as e:
        logger.error(f"Failed to patch main window form styling: {e}")
        return None


if __name__ == "__main__":
    """
    Test the integration
    """
    import sys
    from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QGroupBox
    
    app = QApplication(sys.argv)
    
    # Create test main window
    class TestMainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Form Integration Test")
            self.setMinimumSize(1000, 700)
            self.init_test_ui()
        
        def init_test_ui(self):
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            layout = QVBoxLayout(central_widget)
            
            # Create test form elements similar to main app
            group = QGroupBox("Test Form Integration")
            form_layout = QVBoxLayout(group)
            
            # Test elements that would have red box issues
            self.free_response_input = QLineEdit()
            self.free_response_input.setPlaceholderText("Free response input...")
            
            self.mode_combo = QComboBox()
            self.mode_combo.addItems(["Free Response", "Multiple Choice"])
            
            self.trigger_checkboxes = []
            for i in range(3):
                cb = QCheckBox(f"Test trigger {i+1}")
                self.trigger_checkboxes.append(cb)
                form_layout.addWidget(cb)
            
            form_layout.addWidget(QLabel("Input Field:"))
            form_layout.addWidget(self.free_response_input)
            form_layout.addWidget(QLabel("Mode:"))
            form_layout.addWidget(self.mode_combo)
            
            self.feedback_text = QTextEdit()
            self.feedback_text.setPlaceholderText("Feedback area...")
            form_layout.addWidget(QLabel("Feedback:"))
            form_layout.addWidget(self.feedback_text)
            
            layout.addWidget(group)
    
    # Create test window
    main_window = TestMainWindow()
    
    # Apply integration
    integration_manager = integrate_form_fixes(app, main_window)
    
    main_window.show()
    
    # Test validation states after a delay
    QTimer.singleShot(2000, lambda: integration_manager.set_form_validation_state(
        main_window.free_response_input, 'error', 'Test error state'
    ))
    
    sys.exit(app.exec_())
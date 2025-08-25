"""
UI Accessibility Module for Spanish Subjunctive Practice App

This module provides practical accessibility features including:
- Better keyboard navigation support
- Clear focus indicators
- Appropriate font sizes for readability
- High contrast mode support
- Screen reader friendly labels and descriptions
"""

import sys
from typing import Dict, Any, Optional
from PyQt5.QtWidgets import (
    QWidget, QApplication, QPushButton, QLineEdit, QLabel, 
    QCheckBox, QRadioButton, QComboBox, QTextEdit, QGroupBox,
    QProgressBar, QDialog, QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QEvent, QTimer
from PyQt5.QtGui import QFont, QKeySequence, QPalette, QColor, QFontMetrics
from PyQt5.QtTest import QTest


class AccessibilityManager(QObject):
    """
    Manages accessibility features for the Spanish subjunctive practice application.
    Provides keyboard navigation, focus management, and screen reader support.
    """
    
    # Signals for accessibility events
    focus_changed = pyqtSignal(str)  # Emits description of focused element
    navigation_mode_changed = pyqtSignal(bool)  # True when keyboard navigation is active
    
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.keyboard_navigation_active = False
        self.high_contrast_enabled = False
        self.large_font_enabled = False
        self.focus_sound_enabled = True
        
        # Font size settings
        self.base_font_size = 14
        self.large_font_size = 18
        self.extra_large_font_size = 22
        
        # High contrast colors
        self.high_contrast_palette = self._create_high_contrast_palette()
        self.normal_palette = QApplication.palette()
        
        # Initialize accessibility features
        self._setup_keyboard_navigation()
        self._setup_focus_indicators()
        self._setup_screen_reader_support()
        
    def _create_high_contrast_palette(self) -> QPalette:
        """Create high contrast color palette"""
        palette = QPalette()
        
        # High contrast colors
        bg_color = QColor(0, 0, 0)  # Black background
        text_color = QColor(255, 255, 255)  # White text
        highlight_color = QColor(255, 255, 0)  # Yellow highlight
        button_color = QColor(64, 64, 64)  # Dark gray buttons
        
        # Set palette colors
        palette.setColor(QPalette.Window, bg_color)
        palette.setColor(QPalette.WindowText, text_color)
        palette.setColor(QPalette.Base, bg_color)
        palette.setColor(QPalette.Text, text_color)
        palette.setColor(QPalette.Button, button_color)
        palette.setColor(QPalette.ButtonText, text_color)
        palette.setColor(QPalette.Highlight, highlight_color)
        palette.setColor(QPalette.HighlightedText, bg_color)
        
        return palette
    
    def _setup_keyboard_navigation(self):
        """Setup enhanced keyboard navigation"""
        # Install event filter on main window
        self.main_window.installEventFilter(self)
        
        # Create keyboard shortcuts for accessibility
        self._create_accessibility_shortcuts()
        
    def _create_accessibility_shortcuts(self):
        """Create keyboard shortcuts for accessibility features"""
        from PyQt5.QtWidgets import QShortcut
        
        # Toggle high contrast mode (Alt+H)
        contrast_shortcut = QShortcut(QKeySequence("Alt+H"), self.main_window)
        contrast_shortcut.activated.connect(self.toggle_high_contrast)
        
        # Toggle large fonts (Alt+F)
        font_shortcut = QShortcut(QKeySequence("Alt+F"), self.main_window)
        font_shortcut.activated.connect(self.toggle_large_fonts)
        
        # Navigate to specific areas (Alt+1, Alt+2, etc.)
        area_shortcuts = [
            ("Alt+1", self._focus_exercise_area),
            ("Alt+2", self._focus_answer_input),
            ("Alt+3", self._focus_trigger_selection),
            ("Alt+4", self._focus_controls),
            ("Alt+5", self._focus_feedback)
        ]
        
        for shortcut_key, callback in area_shortcuts:
            shortcut = QShortcut(QKeySequence(shortcut_key), self.main_window)
            shortcut.activated.connect(callback)
    
    def _setup_focus_indicators(self):
        """Setup clear focus indicators"""
        focus_stylesheet = """
        QWidget:focus {
            border: 3px solid #3B82F6;
            border-radius: 5px;
            background-color: rgba(59, 130, 246, 0.1);
        }
        
        QPushButton:focus {
            border: 3px solid #3B82F6;
            background-color: #2563EB;
            font-weight: bold;
        }
        
        QLineEdit:focus {
            border: 3px solid #3B82F6;
            background-color: #F0F9FF;
        }
        
        QCheckBox:focus, QRadioButton:focus {
            border: 2px dashed #3B82F6;
            padding: 2px;
        }
        
        QComboBox:focus {
            border: 3px solid #3B82F6;
            background-color: #F0F9FF;
        }
        """
        
        # Apply to main window
        current_style = self.main_window.styleSheet()
        self.main_window.setStyleSheet(current_style + focus_stylesheet)
    
    def _setup_screen_reader_support(self):
        """Setup screen reader friendly labels and descriptions"""
        # Add accessible names and descriptions to key elements
        self._add_accessible_properties()
        
        # Connect to focus events to announce changes
        QApplication.instance().focusChanged.connect(self._on_focus_changed)
    
    def _add_accessible_properties(self):
        """Add accessible names and descriptions to UI elements"""
        try:
            # Main exercise label
            if hasattr(self.main_window, 'sentence_label'):
                self.main_window.sentence_label.setAccessibleName("Current Exercise")
                self.main_window.sentence_label.setAccessibleDescription(
                    "The Spanish sentence to complete with the subjunctive form"
                )
            
            # Answer input field
            if hasattr(self.main_window, 'free_response_input'):
                self.main_window.free_response_input.setAccessibleName("Answer Input")
                self.main_window.free_response_input.setAccessibleDescription(
                    "Type your subjunctive verb form here"
                )
            
            # Control buttons with detailed descriptions
            button_descriptions = {
                'submit_button': ("Submit Answer", "Submit your current answer (Press Enter)"),
                'next_button': ("Next Exercise", "Move to the next exercise (Press Right Arrow)"),
                'prev_button': ("Previous Exercise", "Go to the previous exercise (Press Left Arrow)"),
                'hint_button': ("Get Hint", "Request a hint for the current exercise (Press H)")
            }
            
            for attr_name, (name, description) in button_descriptions.items():
                if hasattr(self.main_window, attr_name):
                    button = getattr(self.main_window, attr_name)
                    button.setAccessibleName(name)
                    button.setAccessibleDescription(description)
            
            # Progress information
            if hasattr(self.main_window, 'stats_label'):
                self.main_window.stats_label.setAccessibleName("Progress Statistics")
                self.main_window.stats_label.setAccessibleDescription(
                    "Shows current exercise number, correct answers, and accuracy percentage"
                )
            
            # Feedback area
            if hasattr(self.main_window, 'feedback_text'):
                self.main_window.feedback_text.setAccessibleName("Exercise Feedback")
                self.main_window.feedback_text.setAccessibleDescription(
                    "Displays explanations and feedback for submitted answers"
                )
                
        except Exception as e:
            print(f"Warning: Could not set all accessible properties: {e}")
    
    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        """Filter events for accessibility enhancements"""
        if event.type() == QEvent.KeyPress:
            return self._handle_key_press(event)
        elif event.type() == QEvent.FocusIn:
            self._handle_focus_in(obj)
        
        return super().eventFilter(obj, event)
    
    def _handle_key_press(self, event) -> bool:
        """Handle key press events for navigation"""
        key = event.key()
        modifiers = event.modifiers()
        
        # Enable keyboard navigation on any key press
        if not self.keyboard_navigation_active:
            self.keyboard_navigation_active = True
            self.navigation_mode_changed.emit(True)
        
        # Tab navigation enhancement
        if key == Qt.Key_Tab or key == Qt.Key_Backtab:
            self._announce_focused_element()
            return False  # Let normal tab handling continue
        
        # Enhanced Enter key handling
        elif key == Qt.Key_Return or key == Qt.Key_Enter:
            focused_widget = QApplication.focusWidget()
            if isinstance(focused_widget, QPushButton):
                # Announce button activation
                self._announce_text(f"Activated {focused_widget.text()}")
                return False
        
        # Escape key for quick access to main menu
        elif key == Qt.Key_Escape:
            self._show_accessibility_help()
            return True
        
        return False
    
    def _handle_focus_in(self, obj: QObject):
        """Handle focus in events"""
        if isinstance(obj, QWidget):
            self._announce_focused_element()
    
    def _on_focus_changed(self, old_widget, new_widget):
        """Handle focus changes for screen reader support"""
        if new_widget and hasattr(new_widget, 'accessibleName'):
            name = new_widget.accessibleName()
            description = getattr(new_widget, 'accessibleDescription', lambda: "")()
            
            if name:
                announcement = name
                if description:
                    announcement += f". {description}"
                self.focus_changed.emit(announcement)
    
    def _announce_focused_element(self):
        """Announce the currently focused element"""
        focused = QApplication.focusWidget()
        if focused:
            text = self._get_element_description(focused)
            if text:
                self._announce_text(text)
    
    def _get_element_description(self, widget: QWidget) -> str:
        """Get accessible description for a widget"""
        # Try accessible name first
        if hasattr(widget, 'accessibleName') and widget.accessibleName():
            name = widget.accessibleName()
            if hasattr(widget, 'accessibleDescription') and widget.accessibleDescription():
                return f"{name}. {widget.accessibleDescription()}"
            return name
        
        # Fallback to widget-specific descriptions
        if isinstance(widget, QPushButton):
            return f"Button: {widget.text()}"
        elif isinstance(widget, QLineEdit):
            placeholder = widget.placeholderText()
            return f"Input field. {placeholder}" if placeholder else "Input field"
        elif isinstance(widget, QCheckBox):
            state = "checked" if widget.isChecked() else "unchecked"
            return f"Checkbox: {widget.text()}, {state}"
        elif isinstance(widget, QRadioButton):
            state = "selected" if widget.isChecked() else "not selected"
            return f"Radio button: {widget.text()}, {state}"
        elif isinstance(widget, QComboBox):
            return f"Dropdown: {widget.currentText()}"
        elif isinstance(widget, QLabel):
            return f"Text: {widget.text()}"
        
        return widget.__class__.__name__
    
    def _announce_text(self, text: str):
        """Announce text (placeholder for screen reader integration)"""
        # In a full implementation, this would interface with screen readers
        # For now, we'll update the status bar or use other visual feedback
        if hasattr(self.main_window, 'updateStatus'):
            self.main_window.updateStatus(f"🔊 {text}")
        
        # Also emit signal for other components that might want to handle this
        self.focus_changed.emit(text)
    
    # Navigation helper methods
    def _focus_exercise_area(self):
        """Focus on the exercise area"""
        if hasattr(self.main_window, 'sentence_label'):
            self.main_window.sentence_label.setFocus()
            self._announce_text("Exercise area focused")
    
    def _focus_answer_input(self):
        """Focus on the answer input"""
        if hasattr(self.main_window, 'free_response_input'):
            self.main_window.free_response_input.setFocus()
        elif hasattr(self.main_window, 'mc_button_group'):
            buttons = self.main_window.mc_button_group.buttons()
            if buttons:
                buttons[0].setFocus()
        self._announce_text("Answer input focused")
    
    def _focus_trigger_selection(self):
        """Focus on trigger selection area"""
        if hasattr(self.main_window, 'trigger_checkboxes') and self.main_window.trigger_checkboxes:
            self.main_window.trigger_checkboxes[0].setFocus()
            self._announce_text("Trigger selection area focused")
    
    def _focus_controls(self):
        """Focus on control buttons"""
        if hasattr(self.main_window, 'submit_button'):
            self.main_window.submit_button.setFocus()
            self._announce_text("Control buttons focused")
    
    def _focus_feedback(self):
        """Focus on feedback area"""
        if hasattr(self.main_window, 'feedback_text'):
            self.main_window.feedback_text.setFocus()
            self._announce_text("Feedback area focused")
    
    def toggle_high_contrast(self):
        """Toggle high contrast mode"""
        self.high_contrast_enabled = not self.high_contrast_enabled
        
        if self.high_contrast_enabled:
            QApplication.setPalette(self.high_contrast_palette)
            # Add high contrast stylesheet
            high_contrast_style = """
            QMainWindow, QWidget {
                background-color: black;
                color: white;
                font-weight: bold;
            }
            QPushButton {
                background-color: #404040;
                color: white;
                border: 2px solid white;
                font-weight: bold;
                min-height: 30px;
            }
            QPushButton:focus {
                background-color: yellow;
                color: black;
                border: 3px solid #DC2626;
            }
            QLineEdit, QTextEdit {
                background-color: black;
                color: yellow;
                border: 2px solid white;
                font-weight: bold;
            }
            QLabel {
                color: white;
                font-weight: bold;
            }
            QGroupBox {
                color: white;
                border: 2px solid white;
                font-weight: bold;
            }
            """
            self.main_window.setStyleSheet(high_contrast_style)
            self._announce_text("High contrast mode enabled")
        else:
            QApplication.setPalette(self.normal_palette)
            # Reset to original stylesheet (you might want to store the original)
            self.main_window.setStyleSheet("")
            self._announce_text("High contrast mode disabled")
    
    def toggle_large_fonts(self):
        """Toggle large font mode"""
        self.large_font_enabled = not self.large_font_enabled
        
        if self.large_font_enabled:
            self._apply_large_fonts()
            self._announce_text("Large fonts enabled")
        else:
            self._apply_normal_fonts()
            self._announce_text("Large fonts disabled")
    
    def _apply_large_fonts(self):
        """Apply large fonts to the application"""
        font = QFont()
        font.setPointSize(self.large_font_size)
        QApplication.instance().setFont(font)
        
        # Apply extra large fonts to important elements
        extra_large_font = QFont()
        extra_large_font.setPointSize(self.extra_large_font_size)
        extra_large_font.setBold(True)
        
        if hasattr(self.main_window, 'sentence_label'):
            self.main_window.sentence_label.setFont(extra_large_font)
        
        if hasattr(self.main_window, 'free_response_input'):
            self.main_window.free_response_input.setFont(extra_large_font)
    
    def _apply_normal_fonts(self):
        """Reset to normal font sizes"""
        font = QFont()
        font.setPointSize(self.base_font_size)
        QApplication.instance().setFont(font)
    
    def _show_accessibility_help(self):
        """Show accessibility help dialog"""
        help_text = """
ACCESSIBILITY FEATURES & SHORTCUTS

Navigation:
• Tab/Shift+Tab: Navigate between elements
• Alt+1: Focus exercise area
• Alt+2: Focus answer input
• Alt+3: Focus trigger selection
• Alt+4: Focus control buttons
• Alt+5: Focus feedback area

Visual:
• Alt+H: Toggle high contrast mode
• Alt+F: Toggle large fonts

Exercise Controls:
• Enter: Submit answer
• H: Get hint
• Left Arrow: Previous exercise
• Right Arrow: Next exercise
• Esc: Show this help

Screen Reader:
• Elements have descriptive labels
• Progress is announced
• Focus changes are announced

For best accessibility, use with screen reader software like NVDA or JAWS.
        """
        
        dialog = QMessageBox()
        dialog.setWindowTitle("Accessibility Help")
        dialog.setText(help_text)
        dialog.setIcon(QMessageBox.Information)
        
        # Make the dialog itself accessible
        dialog.setAccessibleName("Accessibility Help Dialog")
        dialog.setAccessibleDescription("Lists available accessibility features and keyboard shortcuts")
        
        dialog.exec_()


class AccessibilityDialog(QDialog):
    """
    Dialog for configuring accessibility settings
    """
    
    def __init__(self, accessibility_manager: AccessibilityManager, parent=None):
        super().__init__(parent)
        self.accessibility_manager = accessibility_manager
        self.setWindowTitle("Accessibility Settings")
        self.setMinimumSize(400, 300)
        
        self._setup_ui()
        self._load_current_settings()
    
    def _setup_ui(self):
        """Setup the UI for accessibility settings"""
        layout = QVBoxLayout(self)
        
        # Visual settings group
        visual_group = QGroupBox("Visual Settings")
        visual_layout = QVBoxLayout(visual_group)
        
        self.high_contrast_cb = QCheckBox("Enable high contrast mode")
        self.high_contrast_cb.setAccessibleDescription("Toggle high contrast colors for better visibility")
        visual_layout.addWidget(self.high_contrast_cb)
        
        self.large_fonts_cb = QCheckBox("Enable large fonts")
        self.large_fonts_cb.setAccessibleDescription("Increase font size throughout the application")
        visual_layout.addWidget(self.large_fonts_cb)
        
        layout.addWidget(visual_group)
        
        # Keyboard settings group
        keyboard_group = QGroupBox("Keyboard & Navigation")
        keyboard_layout = QVBoxLayout(keyboard_group)
        
        self.focus_sound_cb = QCheckBox("Enable focus sound feedback")
        self.focus_sound_cb.setAccessibleDescription("Play sounds when navigating between elements")
        keyboard_layout.addWidget(self.focus_sound_cb)
        
        layout.addWidget(keyboard_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.apply_btn = QPushButton("Apply")
        self.apply_btn.setAccessibleDescription("Apply the selected accessibility settings")
        self.apply_btn.clicked.connect(self._apply_settings)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setAccessibleDescription("Cancel changes and close dialog")
        self.cancel_btn.clicked.connect(self.reject)
        
        self.help_btn = QPushButton("Help")
        self.help_btn.setAccessibleDescription("Show accessibility help and keyboard shortcuts")
        self.help_btn.clicked.connect(self._show_help)
        
        button_layout.addWidget(self.apply_btn)
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.help_btn)
        
        layout.addLayout(button_layout)
    
    def _load_current_settings(self):
        """Load current accessibility settings"""
        self.high_contrast_cb.setChecked(self.accessibility_manager.high_contrast_enabled)
        self.large_fonts_cb.setChecked(self.accessibility_manager.large_font_enabled)
        self.focus_sound_cb.setChecked(self.accessibility_manager.focus_sound_enabled)
    
    def _apply_settings(self):
        """Apply the selected settings"""
        # High contrast
        if self.high_contrast_cb.isChecked() != self.accessibility_manager.high_contrast_enabled:
            self.accessibility_manager.toggle_high_contrast()
        
        # Large fonts
        if self.large_fonts_cb.isChecked() != self.accessibility_manager.large_font_enabled:
            self.accessibility_manager.toggle_large_fonts()
        
        # Focus sound
        self.accessibility_manager.focus_sound_enabled = self.focus_sound_cb.isChecked()
        
        self.accept()
    
    def _show_help(self):
        """Show accessibility help"""
        self.accessibility_manager._show_accessibility_help()


def integrate_accessibility(main_window) -> Optional[AccessibilityManager]:
    """
    Integrate accessibility features into the main window.
    
    Args:
        main_window: The main application window
        
    Returns:
        AccessibilityManager instance or None if integration fails
    """
    try:
        accessibility_manager = AccessibilityManager(main_window)
        
        # Add accessibility menu item to toolbar if it exists
        if hasattr(main_window, 'createToolBar'):
            # This will be called after toolbar creation
            QTimer.singleShot(100, lambda: _add_accessibility_toolbar_item(main_window, accessibility_manager))
        
        return accessibility_manager
        
    except Exception as e:
        print(f"Failed to integrate accessibility features: {e}")
        return None


def _add_accessibility_toolbar_item(main_window, accessibility_manager):
    """Add accessibility item to toolbar"""
    try:
        from PyQt5.QtWidgets import QAction
        
        toolbar = main_window.findChild(QWidget.__class__, "Main Toolbar")
        if not toolbar:
            # Try to find any toolbar
            toolbars = main_window.findChildren(QWidget.__class__)
            for widget in toolbars:
                if "toolbar" in widget.__class__.__name__.lower():
                    toolbar = widget
                    break
        
        if toolbar and hasattr(toolbar, 'addAction'):
            accessibility_action = QAction("Accessibility", main_window)
            accessibility_action.setToolTip("Configure accessibility settings (Esc for help)")
            accessibility_action.setShortcut("Ctrl+Alt+A")
            accessibility_action.triggered.connect(
                lambda: show_accessibility_dialog(main_window, accessibility_manager)
            )
            toolbar.addAction(accessibility_action)
        
    except Exception as e:
        print(f"Could not add accessibility toolbar item: {e}")


def show_accessibility_dialog(parent, accessibility_manager):
    """Show the accessibility settings dialog"""
    dialog = AccessibilityDialog(accessibility_manager, parent)
    dialog.exec_()


def add_accessibility_startup_check(main_window, accessibility_manager):
    """
    Add a startup check for accessibility features.
    Shows a brief notification about available features.
    """
    try:
        # Show accessibility notification after a short delay
        def show_accessibility_notification():
            if hasattr(main_window, 'updateStatus'):
                main_window.updateStatus(
                    "♿ Accessibility: Press Esc for help, Alt+H for high contrast, Alt+F for large fonts"
                )
        
        QTimer.singleShot(2000, show_accessibility_notification)
        
    except Exception as e:
        print(f"Could not add accessibility startup check: {e}")


# Example usage for testing
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Create a simple test window
    from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
    
    class TestWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Accessibility Test")
            central = QWidget()
            self.setCentralWidget(central)
            layout = QVBoxLayout(central)
            
            # Add some test widgets
            self.submit_button = QPushButton("Submit")
            self.free_response_input = QLineEdit()
            self.sentence_label = QLabel("Test sentence")
            
            layout.addWidget(self.sentence_label)
            layout.addWidget(self.free_response_input)
            layout.addWidget(self.submit_button)
        
        def updateStatus(self, msg):
            print(f"Status: {msg}")
    
    window = TestWindow()
    accessibility_manager = integrate_accessibility(window)
    
    window.show()
    sys.exit(app.exec_())
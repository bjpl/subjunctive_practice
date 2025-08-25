"""
Accessibility Theme Integration for Spanish Subjunctive Practice App

This module provides easy integration of accessibility improvements into the existing app.
Simply replace the existing theme initialization with this module for immediate compliance.
"""

from PyQt5.QtWidgets import QApplication, QWidget, QAction, QMenu, QDialog, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QLabel, QPushButton, QCheckBox, QComboBox, QGroupBox, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
import json
import os
from typing import Dict, Optional

from .contrast_improvements import (
    AccessibleColorPalette, 
    ColorblindAccessibility, 
    HighContrastMode,
    generate_improved_stylesheet
)


class AccessibilitySettings:
    """Manages accessibility settings persistence"""
    
    def __init__(self, settings_file: str = "accessibility_settings.json"):
        self.settings_file = settings_file
        self.default_settings = {
            'theme': 'light',
            'high_contrast': False,
            'colorblind_safe': True,
            'font_size': 'normal',
            'motion_reduced': False,
            'keyboard_navigation': True
        }
        self.settings = self.load_settings()
    
    def load_settings(self) -> Dict:
        """Load accessibility settings from file"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    saved_settings = json.load(f)
                # Merge with defaults to handle new settings
                settings = self.default_settings.copy()
                settings.update(saved_settings)
                return settings
            except (json.JSONDecodeError, IOError):
                pass
        return self.default_settings.copy()
    
    def save_settings(self):
        """Save accessibility settings to file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except IOError:
            pass  # Fail silently if can't save
    
    def get(self, key: str, default=None):
        """Get setting value"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value):
        """Set setting value and save"""
        self.settings[key] = value
        self.save_settings()


class AccessibilityDialog(QDialog):
    """Accessibility settings dialog"""
    
    settings_changed = pyqtSignal(dict)
    
    def __init__(self, parent=None, current_settings: AccessibilitySettings = None):
        super().__init__(parent)
        self.settings = current_settings or AccessibilitySettings()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the accessibility settings UI"""
        self.setWindowTitle("Accessibility Settings")
        self.setMinimumSize(500, 400)
        
        layout = QVBoxLayout(self)
        
        # Visual Settings Group
        visual_group = QGroupBox("Visual Settings")
        visual_layout = QVBoxLayout(visual_group)
        
        # Theme selection
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Theme:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark"])
        self.theme_combo.setCurrentText(self.settings.get('theme', 'light').title())
        theme_layout.addWidget(self.theme_combo)
        visual_layout.addLayout(theme_layout)
        
        # High contrast mode
        self.high_contrast_cb = QCheckBox("High Contrast Mode")
        self.high_contrast_cb.setChecked(self.settings.get('high_contrast', False))
        self.high_contrast_cb.setToolTip("Increases contrast for users with low vision")
        visual_layout.addWidget(self.high_contrast_cb)
        
        # Colorblind safe colors
        self.colorblind_safe_cb = QCheckBox("Colorblind Safe Colors")
        self.colorblind_safe_cb.setChecked(self.settings.get('colorblind_safe', True))
        self.colorblind_safe_cb.setToolTip("Uses blue/pink instead of green/red for feedback")
        visual_layout.addWidget(self.colorblind_safe_cb)
        
        # Font size
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("Font Size:"))
        self.font_combo = QComboBox()
        self.font_combo.addItems(["Small", "Normal", "Large", "Extra Large"])
        self.font_combo.setCurrentText(self.settings.get('font_size', 'normal').title())
        font_layout.addWidget(self.font_combo)
        visual_layout.addLayout(font_layout)
        
        layout.addWidget(visual_group)
        
        # Motion Settings Group
        motion_group = QGroupBox("Motion & Animation")
        motion_layout = QVBoxLayout(motion_group)
        
        self.motion_reduced_cb = QCheckBox("Reduce Motion")
        self.motion_reduced_cb.setChecked(self.settings.get('motion_reduced', False))
        self.motion_reduced_cb.setToolTip("Reduces animations and transitions")
        motion_layout.addWidget(self.motion_reduced_cb)
        
        layout.addWidget(motion_group)
        
        # Navigation Settings Group  
        nav_group = QGroupBox("Navigation")
        nav_layout = QVBoxLayout(nav_group)
        
        self.keyboard_nav_cb = QCheckBox("Enhanced Keyboard Navigation")
        self.keyboard_nav_cb.setChecked(self.settings.get('keyboard_navigation', True))
        self.keyboard_nav_cb.setToolTip("Shows focus indicators and keyboard shortcuts")
        nav_layout.addWidget(self.keyboard_nav_cb)
        
        layout.addWidget(nav_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        preview_btn = QPushButton("Preview Changes")
        preview_btn.clicked.connect(self.preview_changes)
        button_layout.addWidget(preview_btn)
        
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self.apply_settings)
        apply_btn.setDefault(True)
        button_layout.addWidget(apply_btn)
        
        layout.addLayout(button_layout)
        
        # Add info label
        info_label = QLabel(
            "These settings improve accessibility for users with visual impairments, "
            "color blindness, and motor disabilities. Changes are saved automatically."
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #666; font-size: 12px; padding: 8px;")
        layout.addWidget(info_label)
        
    def get_current_settings(self) -> Dict:
        """Get current settings from UI"""
        return {
            'theme': self.theme_combo.currentText().lower(),
            'high_contrast': self.high_contrast_cb.isChecked(),
            'colorblind_safe': self.colorblind_safe_cb.isChecked(),
            'font_size': self.font_combo.currentText().lower().replace(' ', '_'),
            'motion_reduced': self.motion_reduced_cb.isChecked(),
            'keyboard_navigation': self.keyboard_nav_cb.isChecked()
        }
    
    def preview_changes(self):
        """Preview changes without applying permanently"""
        current = self.get_current_settings()
        self.settings_changed.emit(current)
        
        # Show preview message
        QMessageBox.information(
            self, 
            "Preview Applied", 
            "Preview applied! Check the main window to see changes.\n"
            "Click 'Apply' to save these settings permanently."
        )
    
    def apply_settings(self):
        """Apply and save settings"""
        current = self.get_current_settings()
        
        # Update settings object
        for key, value in current.items():
            self.settings.set(key, value)
        
        # Emit signal to update theme
        self.settings_changed.emit(current)
        
        # Show confirmation
        QMessageBox.information(
            self,
            "Settings Applied",
            "Accessibility settings have been applied and saved."
        )
        
        self.accept()


class AccessibleThemeManager:
    """Enhanced theme manager with accessibility features"""
    
    def __init__(self, app: QApplication):
        self.app = app
        self.settings = AccessibilitySettings()
        self.original_stylesheet = ""
        
        # Font size multipliers
        self.font_multipliers = {
            'small': 0.9,
            'normal': 1.0,
            'large': 1.1,
            'extra_large': 1.3
        }
        
    def apply_accessibility_theme(self, settings: Dict = None):
        """Apply accessibility theme based on settings"""
        if settings is None:
            settings = self.settings.settings
        
        # Generate stylesheet with accessibility improvements
        stylesheet = generate_improved_stylesheet(
            theme=settings.get('theme', 'light'),
            high_contrast=settings.get('high_contrast', False)
        )
        
        # Apply font size adjustments
        font_size = settings.get('font_size', 'normal')
        if font_size != 'normal':
            multiplier = self.font_multipliers.get(font_size, 1.0)
            stylesheet = self._adjust_font_sizes(stylesheet, multiplier)
        
        # Apply motion reduction if enabled
        if settings.get('motion_reduced', False):
            stylesheet = self._reduce_motion(stylesheet)
        
        # Apply enhanced focus indicators if keyboard navigation enabled
        if settings.get('keyboard_navigation', True):
            stylesheet = self._enhance_focus_indicators(stylesheet)
        
        self.app.setStyleSheet(stylesheet)
        
    def _adjust_font_sizes(self, stylesheet: str, multiplier: float) -> str:
        """Adjust font sizes in stylesheet"""
        import re
        
        def replace_font_size(match):
            size_str = match.group(1)
            try:
                size = int(size_str)
                new_size = int(size * multiplier)
                return f"font-size: {new_size}px"
            except ValueError:
                return match.group(0)
        
        # Replace font-size values
        pattern = r'font-size:\s*(\d+)px'
        return re.sub(pattern, replace_font_size, stylesheet)
    
    def _reduce_motion(self, stylesheet: str) -> str:
        """Remove animations and transitions"""
        motion_css = """
        /* MOTION REDUCTION */
        * {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
        
        QPushButton:hover {
            transform: none !important;
        }
        """
        return stylesheet + motion_css
    
    def _enhance_focus_indicators(self, stylesheet: str) -> str:
        """Add enhanced focus indicators"""
        focus_css = """
        /* ENHANCED FOCUS INDICATORS */
        *:focus {
            outline: 3px solid #4A9EFF !important;
            outline-offset: 2px !important;
        }
        
        QPushButton:focus {
            background-color: #E3F2FD !important;
            border: 3px solid #1976D2 !important;
        }
        
        QLineEdit:focus, QTextEdit:focus {
            border: 3px solid #1976D2 !important;
            background-color: #E3F2FD !important;
        }
        """
        return stylesheet + focus_css
    
    def show_accessibility_dialog(self, parent=None):
        """Show accessibility settings dialog"""
        dialog = AccessibilityDialog(parent, self.settings)
        dialog.settings_changed.connect(self.apply_accessibility_theme)
        return dialog.exec_()
    
    def toggle_high_contrast(self):
        """Toggle high contrast mode"""
        current = self.settings.get('high_contrast', False)
        self.settings.set('high_contrast', not current)
        self.apply_accessibility_theme()
        return not current
    
    def toggle_colorblind_mode(self):
        """Toggle colorblind safe colors"""
        current = self.settings.get('colorblind_safe', True)
        self.settings.set('colorblind_safe', not current)
        self.apply_accessibility_theme()
        return not current
    
    def get_current_settings(self) -> Dict:
        """Get current accessibility settings"""
        return self.settings.settings.copy()


def integrate_accessibility_menu(main_window, theme_manager: AccessibleThemeManager):
    """Add accessibility menu to main window toolbar"""
    
    # Get toolbar (assuming it exists)
    toolbar = None
    for child in main_window.children():
        if hasattr(child, 'addAction'):
            toolbar = child
            break
    
    if not toolbar:
        return  # No toolbar found
    
    # Create accessibility menu
    accessibility_action = QAction("Accessibility", main_window)
    accessibility_action.setToolTip("Open accessibility settings")
    accessibility_action.setShortcut("Ctrl+Alt+A")
    
    # Connect to show dialog
    accessibility_action.triggered.connect(
        lambda: theme_manager.show_accessibility_dialog(main_window)
    )
    
    toolbar.addAction(accessibility_action)
    
    # Add quick toggle actions
    toolbar.addSeparator()
    
    high_contrast_action = QAction("High Contrast", main_window)
    high_contrast_action.setToolTip("Toggle high contrast mode")
    high_contrast_action.setShortcut("Ctrl+Alt+H")
    high_contrast_action.triggered.connect(theme_manager.toggle_high_contrast)
    toolbar.addAction(high_contrast_action)
    
    colorblind_action = QAction("Colorblind Mode", main_window)
    colorblind_action.setToolTip("Toggle colorblind safe colors")
    colorblind_action.setShortcut("Ctrl+Alt+C")
    colorblind_action.triggered.connect(theme_manager.toggle_colorblind_mode)
    toolbar.addAction(colorblind_action)


def initialize_accessible_theme(app: QApplication, main_window=None) -> AccessibleThemeManager:
    """
    Initialize accessible theme system - drop-in replacement for existing theme init
    
    Usage:
        # Replace this:
        # style_manager = initialize_modern_ui(app)
        
        # With this:
        theme_manager = initialize_accessible_theme(app, main_window)
    """
    # Create theme manager
    theme_manager = AccessibleThemeManager(app)
    
    # Apply initial theme based on saved settings
    theme_manager.apply_accessibility_theme()
    
    # Add accessibility menu if main window provided
    if main_window:
        integrate_accessibility_menu(main_window, theme_manager)
    
    return theme_manager


# Convenience functions for easy integration
def apply_feedback_styling(widget, feedback_type: str, colorblind_safe: bool = True):
    """Apply accessible feedback styling to a widget"""
    if colorblind_safe:
        colors = ColorblindAccessibility.get_colorblind_safe_feedback_colors()
    else:
        colors = {
            'correct': '#27AE60',
            'incorrect': '#E74C3C',
            'warning': '#F39C12',
            'info': '#3498DB'
        }
    
    indicators = {
        'correct': '✓',
        'incorrect': '✗', 
        'warning': '⚠',
        'info': 'ℹ'
    }
    
    if feedback_type in colors:
        color = colors[feedback_type]
        indicator = indicators.get(feedback_type, '')
        
        # Apply styling
        widget.setProperty('feedback', feedback_type)
        widget.setStyleSheet(f"""
            background-color: {color};
            color: white;
            border: 2px solid {color};
            border-radius: 4px;
            padding: 8px;
            font-weight: bold;
        """)
        
        # Add text indicator if it's a label or button
        if hasattr(widget, 'setText'):
            current_text = widget.text()
            if not current_text.startswith(indicator):
                widget.setText(f"{indicator} {current_text}")


if __name__ == "__main__":
    """Demo the accessibility features"""
    import sys
    from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
    
    app = QApplication(sys.argv)
    
    # Create demo window
    window = QMainWindow()
    window.setWindowTitle("Accessibility Demo")
    
    central = QWidget()
    window.setCentralWidget(central)
    layout = QVBoxLayout(central)
    
    # Demo elements
    layout.addWidget(QLabel("This is primary text"))
    layout.addWidget(QLabel("This is secondary text"))
    
    correct_btn = QPushButton("Correct Answer")
    incorrect_btn = QPushButton("Incorrect Answer")
    
    layout.addWidget(correct_btn)
    layout.addWidget(incorrect_btn)
    
    # Initialize accessible theme
    theme_manager = initialize_accessible_theme(app, window)
    
    # Apply feedback styling
    apply_feedback_styling(correct_btn, 'correct')
    apply_feedback_styling(incorrect_btn, 'incorrect')
    
    window.show()
    sys.exit(app.exec_())
"""
Enhanced Keyboard Navigation and Accessibility Manager for Spanish Subjunctive Practice App

This module provides comprehensive accessibility features including:
- Advanced keyboard navigation system
- Visual focus indicators and high contrast mode
- ARIA labels and screen reader support
- Focus management for dynamic content
- Keyboard shortcuts system
- Accessibility settings management

Author: Claude Code Assistant
"""

import json
import os
from typing import Dict, List, Optional, Callable, Any
from PyQt5.QtWidgets import (
    QWidget, QApplication, QLabel, QDialog, QVBoxLayout, QHBoxLayout,
    QGroupBox, QCheckBox, QComboBox, QPushButton, QSpinBox, QSlider,
    QColorDialog, QMessageBox, QScrollArea, QTabWidget, QTextEdit,
    QKeySequenceEdit, QTableWidget, QSizePolicy
)
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QTimer, QEvent, QPoint
from PyQt5.QtGui import (
    QKeySequence, QPalette, QColor, QFont, QFontMetrics, QPainter,
    QPen, QBrush, QKeyEvent
)


class AccessibilitySettings:
    """Manages accessibility settings and preferences"""
    
    def __init__(self):
        self.settings_file = "config/accessibility_settings.json"
        self.default_settings = {
            "high_contrast": False,
            "focus_ring_width": 3,
            "focus_ring_color": "#3B82F6",
            "font_size_multiplier": 1.0,
            "keyboard_navigation_enabled": True,
            "screen_reader_support": True,
            "auto_announce": True,
            "skip_animation": False,
            "show_shortcuts": True,
            "custom_shortcuts": {},
            "color_theme": "default",  # default, high_contrast, dark_high_contrast
            "reduce_motion": False,
            "enhanced_tooltips": True
        }
        self.settings = self.load_settings()
    
    def load_settings(self) -> Dict[str, Any]:
        """Load accessibility settings from file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    merged = self.default_settings.copy()
                    merged.update(loaded)
                    return merged
        except Exception as e:
            print(f"Error loading accessibility settings: {e}")
        
        return self.default_settings.copy()
    
    def save_settings(self) -> None:
        """Save accessibility settings to file"""
        try:
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Error saving accessibility settings: {e}")
    
    def get(self, key: str, default=None):
        """Get setting value"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set setting value and save"""
        self.settings[key] = value
        self.save_settings()
    
    def reset_to_defaults(self) -> None:
        """Reset all settings to defaults"""
        self.settings = self.default_settings.copy()
        self.save_settings()


class FocusManager(QObject):
    """Advanced focus management system"""
    
    # Signals for focus events
    focus_changed = pyqtSignal(QWidget, QWidget)  # old, new
    focus_announced = pyqtSignal(str)  # announcement text
    
    def __init__(self, accessibility_settings: AccessibilitySettings):
        super().__init__()
        self.settings = accessibility_settings
        self.focus_history: List[QWidget] = []
        self.focus_groups: Dict[str, List[QWidget]] = {}
        self.current_group = None
        self.focus_ring_timer = QTimer()
        self.focus_ring_timer.timeout.connect(self._animate_focus_ring)
        self.focus_ring_frame = 0
        
    def register_focus_group(self, group_name: str, widgets: List[QWidget]) -> None:
        """Register a group of widgets for grouped navigation"""
        self.focus_groups[group_name] = widgets
        
        # Set up tab order within group
        for i, widget in enumerate(widgets):
            widget.setAccessibleName(f"{group_name}_{i}")
            if i > 0:
                QWidget.setTabOrder(widgets[i-1], widget)
    
    def set_focus_with_announcement(self, widget: QWidget, announcement: str = None) -> None:
        """Set focus with optional screen reader announcement"""
        if widget and widget.isVisible() and widget.isEnabled():
            widget.setFocus()
            
            # Add to focus history
            if widget not in self.focus_history:
                self.focus_history.append(widget)
            
            # Announce to screen reader
            if self.settings.get("auto_announce") and announcement:
                self.focus_announced.emit(announcement)
                widget.setAccessibleDescription(announcement)
    
    def navigate_to_next_in_group(self, group_name: str, current_widget: QWidget = None) -> None:
        """Navigate to next widget in specified group"""
        if group_name not in self.focus_groups:
            return
        
        widgets = [w for w in self.focus_groups[group_name] if w.isVisible() and w.isEnabled()]
        if not widgets:
            return
        
        if current_widget and current_widget in widgets:
            current_index = widgets.index(current_widget)
            next_index = (current_index + 1) % len(widgets)
        else:
            next_index = 0
        
        next_widget = widgets[next_index]
        self.set_focus_with_announcement(
            next_widget,
            f"Focused on {next_widget.accessibleName() or next_widget.objectName()}"
        )
    
    def navigate_to_previous_in_group(self, group_name: str, current_widget: QWidget = None) -> None:
        """Navigate to previous widget in specified group"""
        if group_name not in self.focus_groups:
            return
        
        widgets = [w for w in self.focus_groups[group_name] if w.isVisible() and w.isEnabled()]
        if not widgets:
            return
        
        if current_widget and current_widget in widgets:
            current_index = widgets.index(current_widget)
            prev_index = (current_index - 1) % len(widgets)
        else:
            prev_index = len(widgets) - 1
        
        prev_widget = widgets[prev_index]
        self.set_focus_with_announcement(
            prev_widget,
            f"Focused on {prev_widget.accessibleName() or prev_widget.objectName()}"
        )
    
    def apply_focus_styling(self, widget: QWidget) -> None:
        """Apply enhanced focus styling to widget"""
        if not widget or not self.settings.get("keyboard_navigation_enabled"):
            return
        
        # Create focus ring style
        ring_width = self.settings.get("focus_ring_width", 3)
        ring_color = self.settings.get("focus_ring_color", "#3B82F6")
        
        # High contrast mode adjustments
        if self.settings.get("high_contrast"):
            ring_width = max(ring_width, 4)
            ring_color = "#FFFF00"  # Yellow for high contrast
        
        focus_style = f"""
            QWidget:focus {{
                border: {ring_width}px solid {ring_color};
                border-radius: 4px;
                outline: none;
            }}
            QLineEdit:focus, QTextEdit:focus {{
                border: {ring_width}px solid {ring_color};
                background-color: {"#000033" if self.settings.get("high_contrast") else "rgba(255, 68, 68, 0.1)"};
            }}
            QPushButton:focus {{
                border: {ring_width}px solid {ring_color};
                background-color: {"#003300" if self.settings.get("high_contrast") else "rgba(255, 68, 68, 0.15)"};
            }}
            QCheckBox:focus::indicator, QRadioButton:focus::indicator {{
                border: {ring_width}px solid {ring_color};
            }}
        """
        
        # Apply to widget and children
        widget.setStyleSheet(widget.styleSheet() + focus_style)
        for child in widget.findChildren(QWidget):
            child.setStyleSheet(child.styleSheet() + focus_style)
    
    def _animate_focus_ring(self) -> None:
        """Animate focus ring for better visibility"""
        self.focus_ring_frame = (self.focus_ring_frame + 1) % 60
        # Animation logic can be implemented here if needed
    
    def start_focus_ring_animation(self) -> None:
        """Start focus ring animation"""
        if self.settings.get("keyboard_navigation_enabled") and not self.settings.get("reduce_motion"):
            self.focus_ring_timer.start(50)  # 20 FPS
    
    def stop_focus_ring_animation(self) -> None:
        """Stop focus ring animation"""
        self.focus_ring_timer.stop()


class KeyboardNavigationManager(QObject):
    """Advanced keyboard navigation and shortcuts manager"""
    
    # Signals
    shortcut_triggered = pyqtSignal(str, str)  # action, description
    navigation_changed = pyqtSignal(str)  # direction
    
    def __init__(self, accessibility_settings: AccessibilitySettings):
        super().__init__()
        self.settings = accessibility_settings
        self.shortcuts: Dict[str, Dict[str, Any]] = {}
        self.navigation_mode = "normal"  # normal, spatial, sequential
        self.setup_default_shortcuts()
    
    def setup_default_shortcuts(self) -> None:
        """Setup default keyboard shortcuts"""
        default_shortcuts = {
            "submit_answer": {
                "key": "Return",
                "description": "Submit current answer",
                "category": "Navigation"
            },
            "next_exercise": {
                "key": "Right",
                "description": "Move to next exercise",
                "category": "Navigation"
            },
            "prev_exercise": {
                "key": "Left", 
                "description": "Move to previous exercise",
                "category": "Navigation"
            },
            "show_hint": {
                "key": "H",
                "description": "Show hint for current exercise",
                "category": "Learning"
            },
            "conjugation_reference": {
                "key": "Ctrl+R",
                "description": "Open conjugation reference",
                "category": "Reference"
            },
            "toggle_translation": {
                "key": "Ctrl+T",
                "description": "Toggle English translation",
                "category": "Display"
            },
            "accessibility_settings": {
                "key": "Ctrl+Alt+A",
                "description": "Open accessibility settings",
                "category": "Settings"
            },
            "high_contrast_toggle": {
                "key": "Ctrl+Alt+H",
                "description": "Toggle high contrast mode",
                "category": "Display"
            },
            "skip_to_content": {
                "key": "Ctrl+K",
                "description": "Skip to main content area",
                "category": "Navigation"
            },
            "skip_to_navigation": {
                "key": "Ctrl+N",
                "description": "Skip to navigation buttons",
                "category": "Navigation"
            },
            "read_current_exercise": {
                "key": "Ctrl+Space",
                "description": "Read current exercise aloud",
                "category": "Accessibility"
            },
            "focus_answer_input": {
                "key": "Ctrl+I",
                "description": "Focus on answer input field",
                "category": "Navigation"
            },
            "show_keyboard_help": {
                "key": "F1",
                "description": "Show keyboard shortcuts help",
                "category": "Help"
            }
        }
        
        # Merge with custom shortcuts from settings
        custom_shortcuts = self.settings.get("custom_shortcuts", {})
        for action, shortcut_data in default_shortcuts.items():
            if action in custom_shortcuts:
                shortcut_data["key"] = custom_shortcuts[action]
            self.shortcuts[action] = shortcut_data
    
    def get_shortcut(self, action: str) -> Optional[str]:
        """Get keyboard shortcut for action"""
        return self.shortcuts.get(action, {}).get("key")
    
    def set_custom_shortcut(self, action: str, key: str) -> None:
        """Set custom keyboard shortcut"""
        if action in self.shortcuts:
            self.shortcuts[action]["key"] = key
            custom_shortcuts = self.settings.get("custom_shortcuts", {})
            custom_shortcuts[action] = key
            self.settings.set("custom_shortcuts", custom_shortcuts)
    
    def get_shortcuts_by_category(self) -> Dict[str, List[Dict[str, str]]]:
        """Get shortcuts organized by category"""
        categories = {}
        for action, data in self.shortcuts.items():
            category = data.get("category", "Other")
            if category not in categories:
                categories[category] = []
            categories[category].append({
                "action": action,
                "key": data["key"],
                "description": data["description"]
            })
        return categories
    
    def handle_key_event(self, event: QKeyEvent) -> bool:
        """Handle key event and trigger appropriate action"""
        key_sequence = QKeySequence(event.key() | int(event.modifiers())).toString()
        
        for action, data in self.shortcuts.items():
            if data["key"] == key_sequence:
                self.shortcut_triggered.emit(action, data["description"])
                return True
        
        return False


class AccessibilityThemeManager:
    """Manages accessibility themes and high contrast modes"""
    
    def __init__(self, accessibility_settings: AccessibilitySettings):
        self.settings = accessibility_settings
        self.themes = self._define_themes()
        self.current_theme = self.settings.get("color_theme", "default")
    
    def _define_themes(self) -> Dict[str, Dict[str, str]]:
        """Define accessibility color themes"""
        return {
            "default": {
                "background": "#ffffff",
                "text": "#000000", 
                "primary": "#007ACC",
                "secondary": "#f0f0f0",
                "accent": "#FF4444",
                "border": "#cccccc",
                "focus": "#FF4444",
                "success": "#28a745",
                "warning": "#ffc107",
                "error": "#dc3545"
            },
            "high_contrast": {
                "background": "#000000",
                "text": "#ffffff",
                "primary": "#ffff00",
                "secondary": "#333333", 
                "accent": "#ffff00",
                "border": "#ffffff",
                "focus": "#ffff00",
                "success": "#00ff00",
                "warning": "#ffff00",
                "error": "#DC2626"
            },
            "dark_high_contrast": {
                "background": "#1a1a1a",
                "text": "#ffffff",
                "primary": "#00ffff",
                "secondary": "#2d2d2d",
                "accent": "#00ffff", 
                "border": "#ffffff",
                "focus": "#ffff00",
                "success": "#00ff00",
                "warning": "#ffaa00",
                "error": "#EF4444"
            },
            "low_vision": {
                "background": "#fffbf0",
                "text": "#000000",
                "primary": "#0066cc",
                "secondary": "#f5f5f5",
                "accent": "#cc0000",
                "border": "#999999",
                "focus": "#cc0000", 
                "success": "#006600",
                "warning": "#cc6600",
                "error": "#cc0000"
            }
        }
    
    def get_theme_stylesheet(self, theme_name: str = None) -> str:
        """Generate stylesheet for specified theme"""
        theme_name = theme_name or self.current_theme
        if theme_name not in self.themes:
            theme_name = "default"
        
        theme = self.themes[theme_name]
        font_multiplier = self.settings.get("font_size_multiplier", 1.0)
        
        # Calculate font sizes
        base_font_size = int(18 * font_multiplier)
        small_font_size = int(16 * font_multiplier)
        large_font_size = int(20 * font_multiplier)
        
        # Focus ring properties
        focus_width = self.settings.get("focus_ring_width", 3)
        if theme_name in ["high_contrast", "dark_high_contrast"]:
            focus_width = max(focus_width, 4)
        
        stylesheet = f"""
            /* Base styles with accessibility enhancements */
            QMainWindow, QDialog {{
                background-color: {theme["background"]};
                color: {theme["text"]};
                font-size: {base_font_size}px;
                font-family: "Segoe UI", Arial, sans-serif;
            }}
            
            QWidget {{
                background-color: {theme["background"]};
                color: {theme["text"]};
                font-size: {base_font_size}px;
                selection-background-color: {theme["accent"]};
                selection-color: {theme["background"]};
            }}
            
            /* Enhanced focus indicators */
            QWidget:focus {{
                border: {focus_width}px solid {theme["focus"]};
                border-radius: 4px;
                outline: none;
                background-color: {theme["secondary"]};
            }}
            
            /* Button styling */
            QPushButton {{
                background-color: {theme["primary"]};
                color: {theme["background"] if theme_name != "default" else theme["text"]};
                border: 2px solid {theme["border"]};
                border-radius: 6px;
                padding: 12px 24px;
                font-size: {base_font_size}px;
                font-weight: bold;
                min-height: 40px;
            }}
            
            QPushButton:hover {{
                background-color: {theme["accent"]};
                border-color: {theme["focus"]};
                transform: scale(1.05);
            }}
            
            QPushButton:focus {{
                border: {focus_width}px solid {theme["focus"]};
                outline: 2px solid {theme["text"]};
                outline-offset: 2px;
            }}
            
            QPushButton:pressed {{
                background-color: {theme["secondary"]};
            }}
            
            QPushButton:disabled {{
                background-color: {theme["secondary"]};
                color: #666666;
                border-color: #999999;
            }}
            
            /* Input styling */
            QLineEdit, QTextEdit {{
                background-color: {theme["background"]};
                color: {theme["text"]};
                border: 3px solid {theme["border"]};
                border-radius: 6px;
                padding: 12px;
                font-size: {base_font_size}px;
                min-height: 40px;
            }}
            
            QLineEdit:focus, QTextEdit:focus {{
                border: {focus_width}px solid {theme["focus"]};
                background-color: {theme["secondary"]};
                outline: 2px solid {theme["accent"]};
                outline-offset: 2px;
            }}
            
            /* Checkbox and radio button styling */
            QCheckBox, QRadioButton {{
                font-size: {large_font_size}px;
                padding: 8px;
                spacing: 8px;
            }}
            
            QCheckBox::indicator, QRadioButton::indicator {{
                width: 24px;
                height: 24px;
                border: 3px solid {theme["border"]};
                background-color: {theme["background"]};
            }}
            
            QCheckBox:focus::indicator, QRadioButton:focus::indicator {{
                border: {focus_width}px solid {theme["focus"]};
                outline: 2px solid {theme["accent"]};
                outline-offset: 2px;
            }}
            
            QCheckBox::indicator:checked {{
                background-color: {theme["success"]};
                border-color: {theme["success"]};
            }}
            
            QRadioButton::indicator:checked {{
                background-color: {theme["primary"]};
                border-color: {theme["primary"]};
            }}
            
            /* Group box styling */
            QGroupBox {{
                font-size: {large_font_size}px;
                font-weight: bold;
                border: 3px solid {theme["border"]};
                border-radius: 8px;
                margin: 12px;
                padding-top: 20px;
                padding-left: 8px;
                padding-right: 8px;
                padding-bottom: 8px;
            }}
            
            QGroupBox::title {{
                color: {theme["primary"]};
                subcontrol-origin: margin;
                left: 16px;
                padding: 0 8px 0 8px;
            }}
            
            /* Label styling */
            QLabel {{
                font-size: {base_font_size}px;
                color: {theme["text"]};
                padding: 4px;
            }}
            
            /* Progress bar styling */
            QProgressBar {{
                border: 2px solid {theme["border"]};
                border-radius: 8px;
                text-align: center;
                font-size: {base_font_size}px;
                font-weight: bold;
                height: 30px;
            }}
            
            QProgressBar::chunk {{
                background-color: {theme["success"]};
                border-radius: 6px;
            }}
            
            /* Status bar styling */
            QStatusBar {{
                background-color: {theme["secondary"]};
                color: {theme["text"]};
                border-top: 2px solid {theme["border"]};
                font-size: {small_font_size}px;
                padding: 8px;
            }}
            
            /* Toolbar styling */
            QToolBar {{
                background-color: {theme["secondary"]};
                border: 2px solid {theme["border"]};
                spacing: 8px;
                padding: 8px;
            }}
            
            QToolBar QAction {{
                font-size: {base_font_size}px;
                padding: 8px 16px;
            }}
            
            /* Combo box styling */
            QComboBox {{
                background-color: {theme["background"]};
                color: {theme["text"]};
                border: 3px solid {theme["border"]};
                border-radius: 6px;
                padding: 8px 12px;
                font-size: {base_font_size}px;
                min-height: 32px;
            }}
            
            QComboBox:focus {{
                border: {focus_width}px solid {theme["focus"]};
                outline: 2px solid {theme["accent"]};
                outline-offset: 2px;
            }}
            
            QComboBox::drop-down {{
                border: none;
                width: 32px;
            }}
            
            QComboBox::down-arrow {{
                width: 16px;
                height: 16px;
                background-color: {theme["text"]};
            }}
            
            /* Table styling */
            QTableWidget {{
                background-color: {theme["background"]};
                color: {theme["text"]};
                gridline-color: {theme["border"]};
                border: 2px solid {theme["border"]};
                font-size: {base_font_size}px;
            }}
            
            QTableWidget::item {{
                padding: 8px;
                border-bottom: 1px solid {theme["border"]};
            }}
            
            QTableWidget::item:selected {{
                background-color: {theme["accent"]};
                color: {theme["background"]};
            }}
            
            QTableWidget::item:focus {{
                border: {focus_width}px solid {theme["focus"]};
                outline: 2px solid {theme["accent"]};
                outline-offset: 1px;
            }}
            
            /* Scroll area styling */
            QScrollArea {{
                border: 2px solid {theme["border"]};
                border-radius: 6px;
            }}
            
            QScrollBar:vertical {{
                background-color: {theme["secondary"]};
                width: 20px;
                border-radius: 4px;
            }}
            
            QScrollBar::handle:vertical {{
                background-color: {theme["primary"]};
                border-radius: 4px;
                min-height: 30px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background-color: {theme["accent"]};
            }}
            
            /* Tab widget styling */
            QTabWidget::pane {{
                border: 2px solid {theme["border"]};
                border-radius: 6px;
            }}
            
            QTabBar::tab {{
                background-color: {theme["secondary"]};
                color: {theme["text"]};
                border: 2px solid {theme["border"]};
                padding: 12px 24px;
                font-size: {base_font_size}px;
                margin-right: 4px;
            }}
            
            QTabBar::tab:selected {{
                background-color: {theme["primary"]};
                color: {theme["background"] if theme_name != "default" else theme["text"]};
            }}
            
            QTabBar::tab:focus {{
                border: {focus_width}px solid {theme["focus"]};
                outline: 2px solid {theme["accent"]};
                outline-offset: 2px;
            }}
            
            /* Message box styling */
            QMessageBox {{
                background-color: {theme["background"]};
                color: {theme["text"]};
                font-size: {base_font_size}px;
            }}
            
            QMessageBox QPushButton {{
                min-width: 100px;
                margin: 4px;
            }}
        """
        
        return stylesheet
    
    def apply_theme(self, widget: QWidget, theme_name: str = None) -> None:
        """Apply accessibility theme to widget"""
        theme_name = theme_name or self.current_theme
        self.current_theme = theme_name
        self.settings.set("color_theme", theme_name)
        
        stylesheet = self.get_theme_stylesheet(theme_name)
        widget.setStyleSheet(stylesheet)
        
        # Apply to QApplication for global effects
        if hasattr(QApplication, 'instance') and QApplication.instance():
            app = QApplication.instance()
            app.setStyleSheet(stylesheet)
    
    def cycle_theme(self, widget: QWidget) -> str:
        """Cycle through available themes"""
        theme_names = list(self.themes.keys())
        current_index = theme_names.index(self.current_theme)
        next_index = (current_index + 1) % len(theme_names)
        next_theme = theme_names[next_index]
        
        self.apply_theme(widget, next_theme)
        return next_theme


class AccessibilityManager(QObject):
    """Main accessibility manager that coordinates all accessibility features"""
    
    # Signals
    accessibility_changed = pyqtSignal(str, bool)  # feature, enabled
    announcement_requested = pyqtSignal(str)  # text to announce
    
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.settings = AccessibilitySettings()
        self.focus_manager = FocusManager(self.settings)
        self.keyboard_manager = KeyboardNavigationManager(self.settings)
        self.theme_manager = AccessibilityThemeManager(self.settings)
        
        # Connect signals
        self.focus_manager.focus_announced.connect(self.announcement_requested)
        self.keyboard_manager.shortcut_triggered.connect(self._handle_shortcut)
        
        # Set up initial accessibility features
        self._initialize_accessibility()
    
    def _initialize_accessibility(self) -> None:
        """Initialize accessibility features"""
        # Apply initial theme
        self.theme_manager.apply_theme(self.main_window)
        
        # Set up focus management
        self.focus_manager.apply_focus_styling(self.main_window)
        
        # Install event filter for keyboard handling
        self.main_window.installEventFilter(self)
        
        # Set up ARIA attributes
        self._setup_aria_attributes()
        
        # Register focus groups
        self._setup_focus_groups()
    
    def _setup_aria_attributes(self) -> None:
        """Set up ARIA attributes and accessible names"""
        # Main window
        self.main_window.setAccessibleName("Spanish Subjunctive Practice Application")
        self.main_window.setAccessibleDescription("Interactive learning application for Spanish subjunctive conjugation")
        
        # Find and label important widgets
        widgets_to_label = [
            ("sentence_label", "Exercise Sentence", "Current Spanish exercise sentence to practice"),
            ("translation_label", "English Translation", "English translation of the exercise sentence"),
            ("free_response_input", "Answer Input", "Type your subjunctive conjugation answer here"),
            ("submit_button", "Submit Answer", "Submit your current answer"),
            ("hint_button", "Get Hint", "Get a hint for the current exercise"),
            ("next_button", "Next Exercise", "Move to the next exercise"),
            ("prev_button", "Previous Exercise", "Move to the previous exercise"),
            ("feedback_text", "Feedback", "Detailed feedback and explanation for your answer"),
            ("progress_bar", "Exercise Progress", "Shows current progress through the exercise set"),
            ("stats_label", "Statistics", "Shows current session statistics and accuracy")
        ]
        
        for attr_name, accessible_name, accessible_description in widgets_to_label:
            if hasattr(self.main_window, attr_name):
                widget = getattr(self.main_window, attr_name)
                widget.setAccessibleName(accessible_name)
                widget.setAccessibleDescription(accessible_description)
        
        # Label trigger checkboxes
        if hasattr(self.main_window, 'trigger_checkboxes'):
            for i, checkbox in enumerate(self.main_window.trigger_checkboxes):
                checkbox.setAccessibleName(f"Subjunctive Trigger {i+1}")
                checkbox.setAccessibleDescription(f"Select trigger: {checkbox.text()}")
        
        # Label tense checkboxes
        if hasattr(self.main_window, 'tense_checkboxes'):
            for tense, checkbox in self.main_window.tense_checkboxes.items():
                checkbox.setAccessibleName(f"Tense: {tense}")
                checkbox.setAccessibleDescription(f"Practice {tense} subjunctive conjugations")
        
        # Label person checkboxes  
        if hasattr(self.main_window, 'person_checkboxes'):
            for person, checkbox in self.main_window.person_checkboxes.items():
                checkbox.setAccessibleName(f"Person: {person}")
                checkbox.setAccessibleDescription(f"Practice conjugations for {person}")
    
    def _setup_focus_groups(self) -> None:
        """Set up logical focus groups for navigation"""
        # Navigation buttons group
        nav_buttons = []
        for attr in ['prev_button', 'hint_button', 'submit_button', 'next_button']:
            if hasattr(self.main_window, attr):
                nav_buttons.append(getattr(self.main_window, attr))
        self.focus_manager.register_focus_group("navigation", nav_buttons)
        
        # Trigger checkboxes group
        if hasattr(self.main_window, 'trigger_checkboxes'):
            self.focus_manager.register_focus_group("triggers", self.main_window.trigger_checkboxes)
        
        # Tense checkboxes group
        if hasattr(self.main_window, 'tense_checkboxes'):
            tense_widgets = list(self.main_window.tense_checkboxes.values())
            self.focus_manager.register_focus_group("tenses", tense_widgets)
        
        # Person checkboxes group
        if hasattr(self.main_window, 'person_checkboxes'):
            person_widgets = list(self.main_window.person_checkboxes.values())
            self.focus_manager.register_focus_group("persons", person_widgets)
        
        # Mode controls group
        mode_controls = []
        for attr in ['mode_combo', 'difficulty_combo', 'task_type_combo']:
            if hasattr(self.main_window, attr):
                mode_controls.append(getattr(self.main_window, attr))
        if mode_controls:
            self.focus_manager.register_focus_group("mode_controls", mode_controls)
    
    def _handle_shortcut(self, action: str, description: str) -> None:
        """Handle triggered keyboard shortcut"""
        # Announce shortcut action
        if self.settings.get("auto_announce"):
            self.announcement_requested.emit(f"Activated: {description}")
        
        # Route to appropriate handler in main window
        if hasattr(self.main_window, f'handle_{action}'):
            handler = getattr(self.main_window, f'handle_{action}')
            handler()
        elif action == "accessibility_settings":
            self.show_accessibility_settings()
        elif action == "high_contrast_toggle":
            self.toggle_high_contrast()
        elif action == "skip_to_content":
            self.skip_to_content()
        elif action == "skip_to_navigation":
            self.skip_to_navigation()
        elif action == "read_current_exercise":
            self.read_current_exercise()
        elif action == "focus_answer_input":
            self.focus_answer_input()
        elif action == "show_keyboard_help":
            self.show_keyboard_help()
    
    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        """Filter events for keyboard handling"""
        if event.type() == QEvent.KeyPress:
            # Handle keyboard navigation
            if self.keyboard_manager.handle_key_event(event):
                return True
            
            # Handle arrow key navigation in groups
            if event.key() in [Qt.Key_Up, Qt.Key_Down]:
                focused_widget = QApplication.focusWidget()
                if focused_widget:
                    return self._handle_arrow_navigation(focused_widget, event.key())
        
        return super().eventFilter(obj, event)
    
    def _handle_arrow_navigation(self, widget: QWidget, key: int) -> bool:
        """Handle arrow key navigation within focus groups"""
        # Find which group the widget belongs to
        for group_name, widgets in self.focus_manager.focus_groups.items():
            if widget in widgets:
                if key == Qt.Key_Down:
                    self.focus_manager.navigate_to_next_in_group(group_name, widget)
                elif key == Qt.Key_Up:
                    self.focus_manager.navigate_to_previous_in_group(group_name, widget)
                return True
        
        return False
    
    def toggle_high_contrast(self) -> None:
        """Toggle high contrast mode"""
        current_high_contrast = self.settings.get("high_contrast", False)
        new_high_contrast = not current_high_contrast
        
        self.settings.set("high_contrast", new_high_contrast)
        
        # Switch theme
        if new_high_contrast:
            self.theme_manager.apply_theme(self.main_window, "high_contrast")
        else:
            self.theme_manager.apply_theme(self.main_window, "default")
        
        self.accessibility_changed.emit("high_contrast", new_high_contrast)
        self.announcement_requested.emit(
            f"High contrast mode {'enabled' if new_high_contrast else 'disabled'}"
        )
    
    def skip_to_content(self) -> None:
        """Skip to main content area"""
        if hasattr(self.main_window, 'sentence_label'):
            self.focus_manager.set_focus_with_announcement(
                self.main_window.sentence_label,
                "Skipped to main exercise content"
            )
    
    def skip_to_navigation(self) -> None:
        """Skip to navigation buttons"""
        if hasattr(self.main_window, 'submit_button'):
            self.focus_manager.set_focus_with_announcement(
                self.main_window.submit_button,
                "Skipped to navigation buttons"
            )
    
    def read_current_exercise(self) -> None:
        """Read current exercise aloud"""
        if hasattr(self.main_window, 'sentence_label'):
            exercise_text = self.main_window.sentence_label.text()
            if hasattr(self.main_window, 'translation_label') and self.main_window.translation_label.isVisible():
                translation_text = self.main_window.translation_label.text()
                full_text = f"Exercise: {exercise_text}. Translation: {translation_text}"
            else:
                full_text = f"Current exercise: {exercise_text}"
            
            self.announcement_requested.emit(full_text)
    
    def focus_answer_input(self) -> None:
        """Focus on answer input field"""
        if hasattr(self.main_window, 'free_response_input'):
            self.focus_manager.set_focus_with_announcement(
                self.main_window.free_response_input,
                "Focused on answer input field"
            )
    
    def show_keyboard_help(self) -> None:
        """Show keyboard shortcuts help dialog"""
        dialog = KeyboardHelpDialog(self.keyboard_manager, self.main_window)
        dialog.exec_()
    
    def show_accessibility_settings(self) -> None:
        """Show accessibility settings dialog"""
        dialog = AccessibilitySettingsDialog(self, self.main_window)
        dialog.exec_()
    
    def apply_font_scaling(self, multiplier: float) -> None:
        """Apply font size scaling"""
        self.settings.set("font_size_multiplier", multiplier)
        self.theme_manager.apply_theme(self.main_window)
        self.announcement_requested.emit(f"Font size set to {int(multiplier * 100)}%")
    
    def get_accessibility_status(self) -> Dict[str, bool]:
        """Get current accessibility feature status"""
        return {
            "high_contrast": self.settings.get("high_contrast", False),
            "keyboard_navigation": self.settings.get("keyboard_navigation_enabled", True),
            "screen_reader_support": self.settings.get("screen_reader_support", True),
            "auto_announce": self.settings.get("auto_announce", True),
            "enhanced_tooltips": self.settings.get("enhanced_tooltips", True),
            "reduce_motion": self.settings.get("reduce_motion", False)
        }


class KeyboardHelpDialog(QDialog):
    """Dialog showing keyboard shortcuts help"""
    
    def __init__(self, keyboard_manager: KeyboardNavigationManager, parent=None):
        super().__init__(parent)
        self.keyboard_manager = keyboard_manager
        self.setWindowTitle("Keyboard Shortcuts Help")
        self.setMinimumSize(700, 500)
        self.setModal(True)
        
        # Set accessible attributes
        self.setAccessibleName("Keyboard Shortcuts Help Dialog")
        self.setAccessibleDescription("Complete list of available keyboard shortcuts")
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Set up the help dialog UI"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Keyboard Shortcuts")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 16px;")
        title.setAccessibleName("Dialog Title")
        layout.addWidget(title)
        
        # Shortcuts organized by category
        categories = self.keyboard_manager.get_shortcuts_by_category()
        
        tabs = QTabWidget()
        tabs.setAccessibleName("Shortcut Categories")
        
        for category, shortcuts in categories.items():
            tab_widget = QWidget()
            tab_layout = QVBoxLayout(tab_widget)
            
            # Create table for shortcuts
            table = QTableWidget(len(shortcuts), 2)
            table.setHorizontalHeaderLabels(["Shortcut", "Description"])
            table.setAccessibleName(f"{category} Shortcuts Table")
            
            for row, shortcut in enumerate(shortcuts):
                key_item = QTableWidgetItem(shortcut["key"])
                desc_item = QTableWidgetItem(shortcut["description"])
                
                key_item.setAccessibleText(f"Shortcut key: {shortcut['key']}")
                desc_item.setAccessibleText(f"Action: {shortcut['description']}")
                
                table.setItem(row, 0, key_item)
                table.setItem(row, 1, desc_item)
            
            # Adjust table appearance
            table.resizeColumnsToContents()
            table.horizontalHeader().setStretchLastSection(True)
            table.setAlternatingRowColors(True)
            table.setSelectionBehavior(QTableWidget.SelectRows)
            
            tab_layout.addWidget(table)
            tabs.addTab(tab_widget, category)
        
        layout.addWidget(tabs)
        
        # Instructions
        instructions = QLabel(
            "Use Tab/Shift+Tab to navigate between elements. "
            "Press Escape to close this dialog."
        )
        instructions.setStyleSheet("font-style: italic; margin-top: 16px;")
        instructions.setAccessibleName("Navigation Instructions")
        layout.addWidget(instructions)
        
        # Close button
        close_button = QPushButton("Close (Esc)")
        close_button.setAccessibleName("Close Dialog Button")
        close_button.setAccessibleDescription("Close keyboard shortcuts help dialog")
        close_button.clicked.connect(self.close)
        close_button.setShortcut("Escape")
        layout.addWidget(close_button)
        
        # Set focus to first tab
        tabs.setFocus()


class AccessibilitySettingsDialog(QDialog):
    """Dialog for configuring accessibility settings"""
    
    def __init__(self, accessibility_manager: AccessibilityManager, parent=None):
        super().__init__(parent)
        self.accessibility_manager = accessibility_manager
        self.settings = accessibility_manager.settings
        self.setWindowTitle("Accessibility Settings")
        self.setMinimumSize(600, 700)
        self.setModal(True)
        
        # Set accessible attributes
        self.setAccessibleName("Accessibility Settings Dialog")
        self.setAccessibleDescription("Configure accessibility features and preferences")
        
        self._setup_ui()
        self._load_current_settings()
    
    def _setup_ui(self) -> None:
        """Set up the settings dialog UI"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Accessibility Settings")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 16px;")
        title.setAccessibleName("Settings Dialog Title")
        layout.addWidget(title)
        
        # Scroll area for settings
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setAccessibleName("Settings Scroll Area")
        
        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)
        
        # Visual Settings
        visual_group = QGroupBox("Visual Settings")
        visual_layout = QVBoxLayout(visual_group)
        
        self.high_contrast_check = QCheckBox("Enable High Contrast Mode")
        self.high_contrast_check.setAccessibleDescription("Switch to high contrast colors for better visibility")
        visual_layout.addWidget(self.high_contrast_check)
        
        self.reduce_motion_check = QCheckBox("Reduce Motion and Animations")
        self.reduce_motion_check.setAccessibleDescription("Minimize animations and motion effects")
        visual_layout.addWidget(self.reduce_motion_check)
        
        # Font size
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("Font Size:"))
        self.font_slider = QSlider(Qt.Horizontal)
        self.font_slider.setRange(50, 200)  # 50% to 200%
        self.font_slider.setValue(100)
        self.font_slider.setAccessibleName("Font Size Slider")
        self.font_slider.setAccessibleDescription("Adjust font size from 50% to 200%")
        self.font_label = QLabel("100%")
        self.font_slider.valueChanged.connect(lambda v: self.font_label.setText(f"{v}%"))
        font_layout.addWidget(self.font_slider)
        font_layout.addWidget(self.font_label)
        visual_layout.addLayout(font_layout)
        
        # Color theme
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Color Theme:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Default", "High Contrast", "Dark High Contrast", "Low Vision"])
        self.theme_combo.setAccessibleDescription("Choose color theme for better visibility")
        theme_layout.addWidget(self.theme_combo)
        visual_layout.addLayout(theme_layout)
        
        settings_layout.addWidget(visual_group)
        
        # Focus and Navigation Settings
        nav_group = QGroupBox("Navigation Settings")
        nav_layout = QVBoxLayout(nav_group)
        
        self.keyboard_nav_check = QCheckBox("Enable Enhanced Keyboard Navigation")
        self.keyboard_nav_check.setAccessibleDescription("Enable advanced keyboard navigation features")
        nav_layout.addWidget(self.keyboard_nav_check)
        
        # Focus ring settings
        focus_layout = QHBoxLayout()
        focus_layout.addWidget(QLabel("Focus Ring Width:"))
        self.focus_width_spin = QSpinBox()
        self.focus_width_spin.setRange(1, 10)
        self.focus_width_spin.setSuffix("px")
        self.focus_width_spin.setAccessibleDescription("Set width of focus indicators in pixels")
        focus_layout.addWidget(self.focus_width_spin)
        nav_layout.addLayout(focus_layout)
        
        # Focus ring color
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("Focus Ring Color:"))
        self.color_button = QPushButton()
        self.color_button.setMinimumSize(50, 30)
        self.color_button.setAccessibleDescription("Choose focus ring color")
        self.color_button.clicked.connect(self._choose_focus_color)
        color_layout.addWidget(self.color_button)
        nav_layout.addLayout(color_layout)
        
        settings_layout.addWidget(nav_group)
        
        # Screen Reader Settings
        sr_group = QGroupBox("Screen Reader Settings")
        sr_layout = QVBoxLayout(sr_group)
        
        self.screen_reader_check = QCheckBox("Enable Screen Reader Support")
        self.screen_reader_check.setAccessibleDescription("Enable features for screen reader compatibility")
        sr_layout.addWidget(self.screen_reader_check)
        
        self.auto_announce_check = QCheckBox("Automatic Announcements")
        self.auto_announce_check.setAccessibleDescription("Automatically announce focus changes and actions")
        sr_layout.addWidget(self.auto_announce_check)
        
        self.enhanced_tooltips_check = QCheckBox("Enhanced Tooltips")
        self.enhanced_tooltips_check.setAccessibleDescription("Show detailed tooltips with additional context")
        sr_layout.addWidget(self.enhanced_tooltips_check)
        
        settings_layout.addWidget(sr_group)
        
        # Keyboard Shortcuts Settings
        shortcuts_group = QGroupBox("Keyboard Shortcuts")
        shortcuts_layout = QVBoxLayout(shortcuts_group)
        
        self.show_shortcuts_check = QCheckBox("Show Keyboard Shortcuts in Interface")
        self.show_shortcuts_check.setAccessibleDescription("Display keyboard shortcuts in button labels")
        shortcuts_layout.addWidget(self.show_shortcuts_check)
        
        # Add button to customize shortcuts
        customize_btn = QPushButton("Customize Shortcuts...")
        customize_btn.setAccessibleDescription("Open dialog to customize keyboard shortcuts")
        customize_btn.clicked.connect(self._customize_shortcuts)
        shortcuts_layout.addWidget(customize_btn)
        
        settings_layout.addWidget(shortcuts_group)
        
        scroll.setWidget(settings_widget)
        layout.addWidget(scroll)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        reset_btn = QPushButton("Reset to Defaults")
        reset_btn.setAccessibleDescription("Reset all accessibility settings to default values")
        reset_btn.clicked.connect(self._reset_to_defaults)
        button_layout.addWidget(reset_btn)
        
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setAccessibleDescription("Cancel changes and close dialog")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        ok_btn = QPushButton("OK")
        ok_btn.setAccessibleDescription("Apply settings and close dialog")
        ok_btn.clicked.connect(self._apply_settings)
        ok_btn.setDefault(True)
        button_layout.addWidget(ok_btn)
        
        layout.addLayout(button_layout)
    
    def _load_current_settings(self) -> None:
        """Load current settings into UI controls"""
        self.high_contrast_check.setChecked(self.settings.get("high_contrast", False))
        self.reduce_motion_check.setChecked(self.settings.get("reduce_motion", False))
        self.keyboard_nav_check.setChecked(self.settings.get("keyboard_navigation_enabled", True))
        self.screen_reader_check.setChecked(self.settings.get("screen_reader_support", True))
        self.auto_announce_check.setChecked(self.settings.get("auto_announce", True))
        self.enhanced_tooltips_check.setChecked(self.settings.get("enhanced_tooltips", True))
        self.show_shortcuts_check.setChecked(self.settings.get("show_shortcuts", True))
        
        # Font size
        font_multiplier = self.settings.get("font_size_multiplier", 1.0)
        self.font_slider.setValue(int(font_multiplier * 100))
        
        # Focus ring width
        self.focus_width_spin.setValue(self.settings.get("focus_ring_width", 3))
        
        # Focus ring color
        color = self.settings.get("focus_ring_color", "#FF4444")
        self.color_button.setStyleSheet(f"background-color: {color};")
        
        # Theme
        theme_map = {"default": 0, "high_contrast": 1, "dark_high_contrast": 2, "low_vision": 3}
        theme_index = theme_map.get(self.settings.get("color_theme", "default"), 0)
        self.theme_combo.setCurrentIndex(theme_index)
    
    def _choose_focus_color(self) -> None:
        """Open color chooser for focus ring color"""
        current_color = QColor(self.settings.get("focus_ring_color", "#3B82F6"))
        color = QColorDialog.getColor(current_color, self, "Choose Focus Ring Color")
        
        if color.isValid():
            self.color_button.setStyleSheet(f"background-color: {color.name()};")
            self.focus_ring_color = color.name()
    
    def _customize_shortcuts(self) -> None:
        """Open shortcuts customization dialog"""
        # This would open a more detailed shortcuts customization dialog
        QMessageBox.information(self, "Customize Shortcuts", 
            "Shortcut customization dialog would open here.\n"
            "This feature allows users to remap keyboard shortcuts.")
    
    def _reset_to_defaults(self) -> None:
        """Reset all settings to defaults"""
        reply = QMessageBox.question(self, "Reset Settings",
            "Are you sure you want to reset all accessibility settings to defaults?",
            QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.settings.reset_to_defaults()
            self._load_current_settings()
    
    def _apply_settings(self) -> None:
        """Apply settings and close dialog"""
        # Save all settings
        self.settings.set("high_contrast", self.high_contrast_check.isChecked())
        self.settings.set("reduce_motion", self.reduce_motion_check.isChecked())
        self.settings.set("keyboard_navigation_enabled", self.keyboard_nav_check.isChecked())
        self.settings.set("screen_reader_support", self.screen_reader_check.isChecked())
        self.settings.set("auto_announce", self.auto_announce_check.isChecked())
        self.settings.set("enhanced_tooltips", self.enhanced_tooltips_check.isChecked())
        self.settings.set("show_shortcuts", self.show_shortcuts_check.isChecked())
        
        # Font size
        font_multiplier = self.font_slider.value() / 100.0
        self.settings.set("font_size_multiplier", font_multiplier)
        
        # Focus ring settings
        self.settings.set("focus_ring_width", self.focus_width_spin.value())
        if hasattr(self, 'focus_ring_color'):
            self.settings.set("focus_ring_color", self.focus_ring_color)
        
        # Theme
        theme_map = {0: "default", 1: "high_contrast", 2: "dark_high_contrast", 3: "low_vision"}
        theme = theme_map.get(self.theme_combo.currentIndex(), "default")
        self.settings.set("color_theme", theme)
        
        # Apply changes through accessibility manager
        self.accessibility_manager.theme_manager.apply_theme(
            self.accessibility_manager.main_window, theme
        )
        self.accessibility_manager.focus_manager.apply_focus_styling(
            self.accessibility_manager.main_window
        )
        
        self.accept()
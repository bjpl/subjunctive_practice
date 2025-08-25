# Accessibility Enhancements for Spanish Subjunctive Practice

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os

class AccessibilityManager:
    """Central manager for accessibility features"""
    
    def __init__(self, app):
        self.app = app
        self.high_contrast_mode = False
        self.font_scale = 1.0
        self.screen_reader_enabled = False
        self.keyboard_navigation = True
        
        self.load_accessibility_settings()
    
    def load_accessibility_settings(self):
        """Load accessibility preferences"""
        settings = QSettings("SpanishSubjunctive", "AccessibilitySettings")
        self.high_contrast_mode = settings.value("highContrast", False, type=bool)
        self.font_scale = settings.value("fontScale", 1.0, type=float)
        self.screen_reader_enabled = settings.value("screenReader", False, type=bool)
        self.keyboard_navigation = settings.value("keyboardNav", True, type=bool)
    
    def save_accessibility_settings(self):
        """Save accessibility preferences"""
        settings = QSettings("SpanishSubjunctive", "AccessibilitySettings")
        settings.setValue("highContrast", self.high_contrast_mode)
        settings.setValue("fontScale", self.font_scale)
        settings.setValue("screenReader", self.screen_reader_enabled)
        settings.setValue("keyboardNav", self.keyboard_navigation)
    
    def apply_high_contrast_theme(self, widget):
        """Apply high contrast theme for better visibility"""
        if not self.high_contrast_mode:
            return
            
        high_contrast_style = """
            QWidget {
                background-color: #000000;
                color: #FFFFFF;
                font-weight: bold;
            }
            QLineEdit, QTextEdit {
                background-color: #FFFFFF;
                color: #000000;
                border: 3px solid #FFFF00;
            }
            QPushButton {
                background-color: #0000FF;
                color: #FFFFFF;
                border: 2px solid #FFFFFF;
                font-weight: bold;
                font-size: {}px;
            }
            QPushButton:hover {
                background-color: #FFFFFF;
                color: #0000FF;
            }
            QPushButton:focus {
                border: 4px solid #FFFF00;
            }
            QLabel {
                color: #FFFFFF;
                font-weight: bold;
                font-size: {}px;
            }
            QGroupBox {
                color: #FFFFFF;
                border: 2px solid #FFFFFF;
                font-weight: bold;
            }
            QRadioButton, QCheckBox {
                color: #FFFFFF;
                font-weight: bold;
                font-size: {}px;
            }
            QRadioButton::indicator, QCheckBox::indicator {
                border: 2px solid #FFFFFF;
                background-color: #000000;
            }
            QRadioButton::indicator:checked, QCheckBox::indicator:checked {
                background-color: #FFFF00;
            }
        """.format(
            int(16 * self.font_scale),
            int(16 * self.font_scale), 
            int(16 * self.font_scale)
        )
        
        widget.setStyleSheet(high_contrast_style)
    
    def scale_fonts(self, widget):
        """Scale fonts based on accessibility settings"""
        font = widget.font()
        scaled_size = int(font.pointSize() * self.font_scale)
        font.setPointSize(max(8, min(72, scaled_size)))  # Keep within reasonable bounds
        widget.setFont(font)
        
        # Recursively apply to child widgets
        for child in widget.findChildren(QWidget):
            child_font = child.font()
            child_scaled_size = int(child_font.pointSize() * self.font_scale)
            child_font.setPointSize(max(8, min(72, child_scaled_size)))
            child.setFont(child_font)

class AccessibleLineEdit(QLineEdit):
    """Line edit with enhanced accessibility features"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_accessibility()
    
    def setup_accessibility(self):
        """Setup accessibility features"""
        # Set accessible name and description
        self.setAccessibleName("Answer input field")
        self.setAccessibleDescription("Type your Spanish subjunctive conjugation here")
        
        # Enhanced focus indication
        self.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px;
                font-size: 18px;
            }
            QLineEdit:focus {
                border: 3px solid #4299e1;
                outline: 2px solid #bee3f8;
                outline-offset: 2px;
            }
        """)
        
        # Connect to accessibility events
        self.textChanged.connect(self.announce_text_change)
    
    def announce_text_change(self, text):
        """Announce text changes for screen readers"""
        if len(text) > 0:
            self.setAccessibleDescription(f"Current text: {text}")
    
    def keyPressEvent(self, event):
        """Enhanced keyboard handling"""
        # Announce special keys
        if event.key() == Qt.Key_Backspace and self.text():
            # Announce deletion for screen readers
            pass
        elif event.key() == Qt.Key_Return:
            # Announce submission
            self.setAccessibleDescription("Submitting answer")
        
        super().keyPressEvent(event)

class AccessibleButton(QPushButton):
    """Button with enhanced accessibility"""
    
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setup_accessibility()
    
    def setup_accessibility(self):
        """Setup button accessibility"""
        # Set accessible role
        self.setAccessibleName(self.text())
        
        # Enhanced visual focus indicator
        self.setStyleSheet("""
            QPushButton {
                padding: 12px 24px;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                background-color: #4299e1;
                color: white;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #3182ce;
            }
            QPushButton:focus {
                border: 3px solid #ffd700;
                outline: 2px solid #4299e1;
                outline-offset: 2px;
            }
            QPushButton:pressed {
                background-color: #2c5282;
            }
        """)
        
        # Connect to accessibility events
        self.clicked.connect(self.announce_action)
    
    def announce_action(self):
        """Announce button action for screen readers"""
        action_text = f"{self.text()} button activated"
        self.setAccessibleDescription(action_text)

class ScreenReaderAnnouncer(QObject):
    """Helper for screen reader announcements"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.announcement_label = QLabel()
        self.announcement_label.setAccessibleRole(QAccessible.StaticText)
        self.announcement_label.setVisible(False)  # Hidden but accessible
    
    def announce(self, message: str, priority: str = "normal"):
        """Announce message to screen reader"""
        # For screen readers, we update the accessible description
        self.announcement_label.setAccessibleName("Announcement")
        self.announcement_label.setAccessibleDescription(message)
        self.announcement_label.setText(message)
        
        # For visual users who might miss audio, we could show a brief toast
        if priority == "urgent":
            self.show_visual_announcement(message)
    
    def show_visual_announcement(self, message: str):
        """Show visual announcement for urgent messages"""
        # Could implement a toast notification here
        pass

class KeyboardNavigationHandler(QObject):
    """Enhanced keyboard navigation handler"""
    
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.focus_order = []
        self.current_focus_index = 0
        self.setup_keyboard_shortcuts()
    
    def setup_keyboard_shortcuts(self):
        """Setup global keyboard shortcuts"""
        # Skip to main content
        skip_shortcut = QShortcut(QKeySequence("Alt+M"), self.main_window)
        skip_shortcut.activated.connect(self.skip_to_main_content)
        
        # Skip to navigation
        nav_shortcut = QShortcut(QKeySequence("Alt+N"), self.main_window)
        nav_shortcut.activated.connect(self.skip_to_navigation)
        
        # Repeat current question
        repeat_shortcut = QShortcut(QKeySequence("Alt+R"), self.main_window)
        repeat_shortcut.activated.connect(self.repeat_current_question)
        
        # Toggle high contrast
        contrast_shortcut = QShortcut(QKeySequence("Alt+H"), self.main_window)
        contrast_shortcut.activated.connect(self.toggle_high_contrast)
        
        # Increase font size
        font_up_shortcut = QShortcut(QKeySequence("Ctrl+Plus"), self.main_window)
        font_up_shortcut.activated.connect(self.increase_font_size)
        
        # Decrease font size
        font_down_shortcut = QShortcut(QKeySequence("Ctrl+Minus"), self.main_window)
        font_down_shortcut.activated.connect(self.decrease_font_size)
    
    def skip_to_main_content(self):
        """Skip to main exercise content"""
        # Find and focus the main exercise area
        exercise_widget = self.main_window.findChild(QWidget, "exercise_content")
        if exercise_widget:
            exercise_widget.setFocus()
    
    def skip_to_navigation(self):
        """Skip to navigation buttons"""
        nav_widget = self.main_window.findChild(QWidget, "navigation_buttons")
        if nav_widget:
            nav_widget.setFocus()
    
    def repeat_current_question(self):
        """Repeat current question for screen readers"""
        # Get current exercise text and announce it
        exercise_label = self.main_window.findChild(QLabel, "sentence_label")
        if exercise_label and hasattr(self.main_window, 'announcer'):
            self.main_window.announcer.announce(
                f"Current exercise: {exercise_label.text()}", 
                priority="normal"
            )
    
    def toggle_high_contrast(self):
        """Toggle high contrast mode"""
        if hasattr(self.main_window, 'accessibility_manager'):
            manager = self.main_window.accessibility_manager
            manager.high_contrast_mode = not manager.high_contrast_mode
            manager.apply_high_contrast_theme(self.main_window)
            manager.save_accessibility_settings()
    
    def increase_font_size(self):
        """Increase font size"""
        if hasattr(self.main_window, 'accessibility_manager'):
            manager = self.main_window.accessibility_manager
            manager.font_scale = min(2.0, manager.font_scale + 0.1)
            manager.scale_fonts(self.main_window)
            manager.save_accessibility_settings()
    
    def decrease_font_size(self):
        """Decrease font size"""
        if hasattr(self.main_window, 'accessibility_manager'):
            manager = self.main_window.accessibility_manager
            manager.font_scale = max(0.5, manager.font_scale - 0.1)
            manager.scale_fonts(self.main_window)
            manager.save_accessibility_settings()

class AccessibilitySettingsDialog(QDialog):
    """Dialog for configuring accessibility settings"""
    
    def __init__(self, accessibility_manager, parent=None):
        super().__init__(parent)
        self.accessibility_manager = accessibility_manager
        self.setWindowTitle("Accessibility Settings")
        self.setModal(True)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup accessibility settings UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # High contrast mode
        contrast_group = QGroupBox("Visual Settings")
        contrast_layout = QVBoxLayout(contrast_group)
        
        self.high_contrast_check = QCheckBox("Enable high contrast mode")
        self.high_contrast_check.setChecked(self.accessibility_manager.high_contrast_mode)
        self.high_contrast_check.setAccessibleName("High contrast mode toggle")
        self.high_contrast_check.setAccessibleDescription("Enables high contrast colors for better visibility")
        contrast_layout.addWidget(self.high_contrast_check)
        
        # Font size control
        font_layout = QHBoxLayout()
        font_label = QLabel("Font size:")
        font_label.setAccessibleName("Font size setting")
        
        self.font_slider = QSlider(Qt.Horizontal)
        self.font_slider.setRange(50, 200)  # 50% to 200%
        self.font_slider.setValue(int(self.accessibility_manager.font_scale * 100))
        self.font_slider.setAccessibleName("Font size slider")
        self.font_slider.setAccessibleDescription("Adjust font size from 50% to 200%")
        
        self.font_value_label = QLabel(f"{int(self.accessibility_manager.font_scale * 100)}%")
        self.font_slider.valueChanged.connect(
            lambda v: self.font_value_label.setText(f"{v}%")
        )
        
        font_layout.addWidget(font_label)
        font_layout.addWidget(self.font_slider, 1)
        font_layout.addWidget(self.font_value_label)
        
        contrast_layout.addLayout(font_layout)
        layout.addWidget(contrast_group)
        
        # Keyboard navigation
        keyboard_group = QGroupBox("Navigation Settings")
        keyboard_layout = QVBoxLayout(keyboard_group)
        
        self.keyboard_nav_check = QCheckBox("Enhanced keyboard navigation")
        self.keyboard_nav_check.setChecked(self.accessibility_manager.keyboard_navigation)
        self.keyboard_nav_check.setAccessibleName("Keyboard navigation toggle")
        keyboard_layout.addWidget(self.keyboard_nav_check)
        
        # Keyboard shortcuts help
        shortcuts_label = QLabel("""
        Keyboard Shortcuts:
        • Alt+M: Skip to main content
        • Alt+N: Skip to navigation
        • Alt+R: Repeat current question
        • Alt+H: Toggle high contrast
        • Ctrl+Plus: Increase font size
        • Ctrl+Minus: Decrease font size
        """)
        shortcuts_label.setStyleSheet("font-size: 12px; color: #6c757d; margin-top: 10px;")
        shortcuts_label.setAccessibleName("Keyboard shortcuts reference")
        keyboard_layout.addWidget(shortcuts_label)
        
        layout.addWidget(keyboard_group)
        
        # Screen reader settings
        reader_group = QGroupBox("Screen Reader Settings")
        reader_layout = QVBoxLayout(reader_group)
        
        self.screen_reader_check = QCheckBox("Optimize for screen readers")
        self.screen_reader_check.setChecked(self.accessibility_manager.screen_reader_enabled)
        self.screen_reader_check.setAccessibleName("Screen reader optimization toggle")
        reader_layout.addWidget(self.screen_reader_check)
        
        reader_help = QLabel("When enabled, provides additional announcements and descriptions for screen reader users.")
        reader_help.setWordWrap(True)
        reader_help.setStyleSheet("font-size: 12px; color: #6c757d;")
        reader_layout.addWidget(reader_help)
        
        layout.addWidget(reader_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        apply_btn = QPushButton("Apply")
        apply_btn.setAccessibleName("Apply accessibility settings")
        apply_btn.clicked.connect(self.apply_settings)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setAccessibleName("Cancel and close dialog")
        cancel_btn.clicked.connect(self.reject)
        
        ok_btn = QPushButton("OK")
        ok_btn.setAccessibleName("Apply settings and close")
        ok_btn.clicked.connect(self.accept_settings)
        ok_btn.setDefault(True)
        
        button_layout.addStretch()
        button_layout.addWidget(apply_btn)
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(ok_btn)
        
        layout.addLayout(button_layout)
        
        # Set minimum size
        self.setMinimumSize(500, 400)
    
    def apply_settings(self):
        """Apply accessibility settings"""
        self.accessibility_manager.high_contrast_mode = self.high_contrast_check.isChecked()
        self.accessibility_manager.font_scale = self.font_slider.value() / 100.0
        self.accessibility_manager.keyboard_navigation = self.keyboard_nav_check.isChecked()
        self.accessibility_manager.screen_reader_enabled = self.screen_reader_check.isChecked()
        
        self.accessibility_manager.save_accessibility_settings()
        
        # Apply changes immediately
        main_window = self.parent()
        if main_window:
            self.accessibility_manager.apply_high_contrast_theme(main_window)
            self.accessibility_manager.scale_fonts(main_window)
    
    def accept_settings(self):
        """Apply settings and close dialog"""
        self.apply_settings()
        self.accept()

def setup_accessibility_features(main_window):
    """Setup all accessibility features for the main window"""
    # Initialize accessibility manager
    accessibility_manager = AccessibilityManager(QApplication.instance())
    main_window.accessibility_manager = accessibility_manager
    
    # Initialize screen reader announcer
    announcer = ScreenReaderAnnouncer(main_window)
    main_window.announcer = announcer
    
    # Initialize keyboard navigation
    keyboard_handler = KeyboardNavigationHandler(main_window)
    main_window.keyboard_handler = keyboard_handler
    
    # Apply initial accessibility settings
    accessibility_manager.apply_high_contrast_theme(main_window)
    accessibility_manager.scale_fonts(main_window)
    
    # Add accessibility menu
    add_accessibility_menu(main_window, accessibility_manager)
    
    return accessibility_manager

def add_accessibility_menu(main_window, accessibility_manager):
    """Add accessibility menu to main window"""
    menubar = main_window.menuBar()
    accessibility_menu = menubar.addMenu("Accessibility")
    
    # Settings action
    settings_action = QAction("Accessibility Settings...", main_window)
    settings_action.setShortcut("Alt+A")
    settings_action.triggered.connect(
        lambda: AccessibilitySettingsDialog(accessibility_manager, main_window).exec_()
    )
    accessibility_menu.addAction(settings_action)
    
    accessibility_menu.addSeparator()
    
    # Quick toggles
    contrast_action = QAction("Toggle High Contrast", main_window)
    contrast_action.setShortcut("Alt+H")
    contrast_action.setCheckable(True)
    contrast_action.setChecked(accessibility_manager.high_contrast_mode)
    contrast_action.triggered.connect(
        lambda checked: toggle_high_contrast(main_window, accessibility_manager, checked)
    )
    accessibility_menu.addAction(contrast_action)

def toggle_high_contrast(main_window, accessibility_manager, enabled):
    """Toggle high contrast mode"""
    accessibility_manager.high_contrast_mode = enabled
    accessibility_manager.apply_high_contrast_theme(main_window)
    accessibility_manager.save_accessibility_settings()
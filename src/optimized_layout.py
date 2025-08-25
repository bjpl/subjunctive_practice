"""
Optimized Layout System for Spanish Subjunctive Practice Application
==================================================================

This module provides an improved layout system that addresses space utilization
and visual hierarchy issues in the subjunctive practice application.

Key improvements:
- 70-30 layout with main content priority
- Collapsible sections for space efficiency
- Card-based visual design
- Responsive design principles
- Educational effectiveness focus
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QGroupBox, QLabel,
    QLineEdit, QPushButton, QTextEdit, QProgressBar, QCheckBox,
    QComboBox, QScrollArea, QFrame, QSizePolicy, QStackedWidget,
    QRadioButton, QButtonGroup, QToolButton, QCollapsibleGroupBox,
    QGridLayout, QSpacerItem
)
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPainter, QPalette
import sys
from typing import Dict, List, Optional


class CollapsibleCard(QGroupBox):
    """
    A collapsible group box that can expand/collapse to save space
    while maintaining visual hierarchy and accessibility.
    """
    
    toggled = pyqtSignal(bool)
    
    def __init__(self, title: str, collapsed: bool = False, parent=None):
        super().__init__(title, parent)
        self.collapsed = collapsed
        self._setup_ui()
        self._apply_styles()
        
    def _setup_ui(self):
        """Setup the collapsible UI components"""
        # Create toggle button
        self.toggle_button = QToolButton()
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(not self.collapsed)
        self.toggle_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setText("▼" if not self.collapsed else "►")
        self.toggle_button.clicked.connect(self._on_toggle)
        
        # Create content area
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(10, 5, 10, 10)
        self.content_layout.setSpacing(5)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.addWidget(self.toggle_button)
        main_layout.addWidget(self.content_area)
        
        # Set initial state
        self.content_area.setVisible(not self.collapsed)
        
    def _apply_styles(self):
        """Apply modern card-like styling"""
        self.setStyleSheet("""
            CollapsibleCard {
                border: 1px solid #d0d0d0;
                border-radius: 8px;
                margin: 3px;
                padding-top: 15px;
                background-color: #fafafa;
                font-weight: bold;
                font-size: 14px;
            }
            
            CollapsibleCard QToolButton {
                border: none;
                background: transparent;
                text-align: left;
                padding: 5px;
                font-weight: bold;
                font-size: 13px;
            }
            
            CollapsibleCard QToolButton:hover {
                background-color: rgba(0, 120, 212, 0.1);
            }
        """)
        
    def _on_toggle(self, checked: bool):
        """Handle toggle button click"""
        self.collapsed = not checked
        self.content_area.setVisible(checked)
        self.toggle_button.setText("▼" if checked else "►")
        self.toggled.emit(checked)
        
        # Animate the expansion/collapse
        self._animate_toggle()
        
    def _animate_toggle(self):
        """Add smooth animation for expand/collapse"""
        # This could be enhanced with QPropertyAnimation for smoother transitions
        pass
        
    def add_widget(self, widget):
        """Add a widget to the collapsible content area"""
        self.content_layout.addWidget(widget)
        
    def add_layout(self, layout):
        """Add a layout to the collapsible content area"""
        self.content_layout.addLayout(layout)


class InformationCard(QFrame):
    """
    A modern card widget for displaying information with clear visual hierarchy
    """
    
    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self.title = title
        self._setup_ui()
        self._apply_styles()
        
    def _setup_ui(self):
        """Setup the card UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 15)
        layout.setSpacing(8)
        
        if self.title:
            title_label = QLabel(self.title)
            title_font = QFont()
            title_font.setBold(True)
            title_font.setPointSize(12)
            title_label.setFont(title_font)
            layout.addWidget(title_label)
            
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(5)
        layout.addLayout(self.content_layout)
        
    def _apply_styles(self):
        """Apply modern card styling"""
        self.setStyleSheet("""
            InformationCard {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                margin: 4px;
            }
            
            InformationCard:hover {
                border-color: #b0b0b0;
                box-shadow: 0px 2px 4px rgba(0,0,0,0.1);
            }
        """)
        
    def add_widget(self, widget):
        """Add widget to card content"""
        self.content_layout.addWidget(widget)
        
    def add_layout(self, layout):
        """Add layout to card content"""
        self.content_layout.addLayout(layout)


class CompactCheckboxGrid(QWidget):
    """
    A compact grid layout for checkboxes that uses space efficiently
    """
    
    def __init__(self, items: List[str], columns: int = 2, parent=None):
        super().__init__(parent)
        self.checkboxes = {}
        self._setup_grid(items, columns)
        
    def _setup_grid(self, items: List[str], columns: int):
        """Setup checkbox grid"""
        layout = QGridLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(5, 5, 5, 5)
        
        for i, item in enumerate(items):
            row = i // columns
            col = i % columns
            
            checkbox = QCheckBox(item)
            checkbox.setStyleSheet("""
                QCheckBox {
                    font-size: 12px;
                    spacing: 8px;
                    padding: 3px;
                }
                QCheckBox::indicator {
                    width: 16px;
                    height: 16px;
                }
            """)
            
            self.checkboxes[item] = checkbox
            layout.addWidget(checkbox, row, col)
            
    def get_selected(self) -> List[str]:
        """Get list of selected items"""
        return [item for item, cb in self.checkboxes.items() if cb.isChecked()]
        
    def set_selected(self, items: List[str]):
        """Set selected items"""
        for item, cb in self.checkboxes.items():
            cb.setChecked(item in items)


class ProgressSection(InformationCard):
    """
    Consolidated progress information section
    """
    
    def __init__(self, parent=None):
        super().__init__("Progress & Statistics", parent)
        self._setup_progress_ui()
        
    def _setup_progress_ui(self):
        """Setup progress indicators"""
        # Exercise progress
        self.exercise_label = QLabel("Exercise: 0/0")
        self.exercise_label.setStyleSheet("font-size: 13px; color: #666;")
        self.add_widget(self.exercise_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumHeight(8)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: #f0f0f0;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 3px;
            }
        """)
        self.add_widget(self.progress_bar)
        
        # Statistics
        self.stats_label = QLabel("Accuracy: 0% | Correct: 0")
        self.stats_label.setStyleSheet("font-size: 12px; color: #888;")
        self.add_widget(self.stats_label)
        
        # Streak information
        self.streak_label = QLabel("🔥 Streak: 0 days")
        self.streak_label.setStyleSheet("font-size: 12px; color: #FF9800;")
        self.add_widget(self.streak_label)
        
    def update_progress(self, current: int, total: int, correct: int, accuracy: float):
        """Update progress information"""
        self.exercise_label.setText(f"Exercise: {current}/{total}")
        self.progress_bar.setMaximum(max(total, 1))
        self.progress_bar.setValue(current)
        self.stats_label.setText(f"Accuracy: {accuracy:.1f}% | Correct: {correct}")
        
    def update_streak(self, current: int, best: int):
        """Update streak information"""
        self.streak_label.setText(f"🔥 Streak: {current} days (Best: {best})")


class OptimizedSubjunctiveLayout(QWidget):
    """
    Main optimized layout class that provides the complete UI structure
    with improved space utilization and visual hierarchy.
    """
    
    # Signals for main application integration
    exercise_generated = pyqtSignal()
    answer_submitted = pyqtSignal(str)
    hint_requested = pyqtSignal()
    navigation_requested = pyqtSignal(str)  # 'next' or 'prev'
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_main_layout()
        self._connect_signals()
        
    def _setup_main_layout(self):
        """Setup the main 70-30 layout structure"""
        # Main horizontal splitter (70-30 split)
        self.main_splitter = QSplitter(Qt.Horizontal)
        self.main_splitter.setChildrenCollapsible(False)
        
        # Create main content area (70%)
        self.content_area = self._create_content_area()
        
        # Create control panel (30%)
        self.control_panel = self._create_control_panel()
        
        # Add to splitter with proper sizing
        self.main_splitter.addWidget(self.content_area)
        self.main_splitter.addWidget(self.control_panel)
        self.main_splitter.setStretchFactor(0, 7)  # 70%
        self.main_splitter.setStretchFactor(1, 3)  # 30%
        self.main_splitter.setSizes([700, 300])  # Initial sizes
        
        # Main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.addWidget(self.main_splitter)
        
    def _create_content_area(self) -> QWidget:
        """Create the main content area (70% width)"""
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(12)
        
        # Exercise display card
        self.exercise_card = InformationCard("Current Exercise")
        self.sentence_label = QLabel("Click 'Generate Exercises' to begin")
        self.sentence_label.setWordWrap(True)
        self.sentence_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                line-height: 1.4;
                padding: 15px;
                background-color: #f8f9fa;
                border-left: 4px solid #007ACC;
                border-radius: 4px;
            }
        """)
        self.exercise_card.add_widget(self.sentence_label)
        
        # Optional translation
        self.translation_label = QLabel("")
        self.translation_label.setWordWrap(True)
        self.translation_label.setVisible(False)
        self.translation_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #666;
                font-style: italic;
                padding: 8px 15px;
                background-color: #f0f0f0;
                border-radius: 4px;
                margin-top: 5px;
            }
        """)
        self.exercise_card.add_widget(self.translation_label)
        
        content_layout.addWidget(self.exercise_card)
        
        # Progress section
        self.progress_section = ProgressSection()
        content_layout.addWidget(self.progress_section)
        
        # Answer input area
        self.input_card = InformationCard("Your Answer")
        self._setup_input_area()
        content_layout.addWidget(self.input_card)
        
        # Navigation buttons
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(8)
        
        self.prev_button = QPushButton("◀ Previous")
        self.hint_button = QPushButton("💡 Hint")
        self.submit_button = QPushButton("Submit ✓")
        self.next_button = QPushButton("Next ▶")
        
        # Style buttons
        button_style = """
            QPushButton {
                padding: 8px 16px;
                font-size: 14px;
                border-radius: 6px;
                border: 1px solid #ddd;
                background-color: white;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
        """
        
        for button in [self.prev_button, self.hint_button, self.submit_button, self.next_button]:
            button.setStyleSheet(button_style)
            
        # Special styling for submit button
        self.submit_button.setStyleSheet(button_style + """
            QPushButton {
                background-color: #007ACC;
                color: white;
                border-color: #005a9e;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
        """)
        
        nav_layout.addWidget(self.prev_button)
        nav_layout.addStretch()
        nav_layout.addWidget(self.hint_button)
        nav_layout.addWidget(self.submit_button)
        nav_layout.addStretch()
        nav_layout.addWidget(self.next_button)
        
        content_layout.addLayout(nav_layout)
        
        # Feedback area
        self.feedback_card = InformationCard("Feedback & Explanation")
        self.feedback_text = QTextEdit()
        self.feedback_text.setReadOnly(True)
        self.feedback_text.setMaximumHeight(120)
        self.feedback_text.setStyleSheet("""
            QTextEdit {
                border: none;
                background-color: #f8f9fa;
                padding: 8px;
                font-size: 13px;
                line-height: 1.4;
            }
        """)
        self.feedback_card.add_widget(self.feedback_text)
        content_layout.addWidget(self.feedback_card)
        
        content_layout.addStretch()
        return content_widget
        
    def _setup_input_area(self):
        """Setup the answer input area"""
        self.input_stack = QStackedWidget()
        
        # Free response page
        free_page = QWidget()
        free_layout = QVBoxLayout(free_page)
        free_layout.setContentsMargins(0, 0, 0, 0)
        
        self.free_response_input = QLineEdit()
        self.free_response_input.setPlaceholderText("Type your answer here...")
        self.free_response_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                font-size: 14px;
                border: 2px solid #ddd;
                border-radius: 6px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #007ACC;
            }
        """)
        free_layout.addWidget(self.free_response_input)
        
        self.input_stack.addWidget(free_page)
        
        # Multiple choice page
        mc_page = QWidget()
        mc_layout = QVBoxLayout(mc_page)
        mc_layout.setContentsMargins(0, 0, 0, 0)
        
        self.mc_button_group = QButtonGroup()
        self.mc_options_layout = QVBoxLayout()  # Vertical for better readability
        mc_layout.addLayout(self.mc_options_layout)
        
        self.input_stack.addWidget(mc_page)
        self.input_card.add_widget(self.input_stack)
        
    def _create_control_panel(self) -> QWidget:
        """Create the control panel (30% width)"""
        panel_widget = QWidget()
        panel_layout = QVBoxLayout(panel_widget)
        panel_layout.setContentsMargins(8, 10, 10, 10)
        panel_layout.setSpacing(8)
        
        # Mode and difficulty selection
        settings_card = CollapsibleCard("Exercise Settings")
        
        # Mode selection
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("Mode:"))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Free Response", "Multiple Choice"])
        mode_layout.addWidget(self.mode_combo)
        settings_card.add_layout(mode_layout)
        
        # Difficulty selection
        diff_layout = QHBoxLayout()
        diff_layout.addWidget(QLabel("Level:"))
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Beginner", "Intermediate", "Advanced"])
        self.difficulty_combo.setCurrentIndex(1)
        diff_layout.addWidget(self.difficulty_combo)
        settings_card.add_layout(diff_layout)
        
        # Task type selection
        task_layout = QHBoxLayout()
        task_layout.addWidget(QLabel("Type:"))
        self.task_type_combo = QComboBox()
        self.task_type_combo.addItems(["Traditional Grammar", "TBLT Scenarios", "Mood Contrast", "Review Mode"])
        task_layout.addWidget(self.task_type_combo)
        settings_card.add_layout(task_layout)
        
        panel_layout.addWidget(settings_card)
        
        # Tense selection - collapsible
        tense_card = CollapsibleCard("Select Tenses")
        self.tense_checkboxes = {}
        tenses = [
            "Present Subjunctive",
            "Imperfect Subjunctive (ra)",
            "Imperfect Subjunctive (se)",
            "Present Perfect Subjunctive",
            "Pluperfect Subjunctive"
        ]
        
        tense_grid = CompactCheckboxGrid(tenses, columns=1)
        self.tense_checkboxes = tense_grid.checkboxes
        tense_card.add_widget(tense_grid)
        panel_layout.addWidget(tense_card)
        
        # Person selection - collapsible
        person_card = CollapsibleCard("Select Persons")
        persons = ["yo", "tú", "él/ella/usted", "nosotros", "vosotros", "ellos/ellas/ustedes"]
        person_grid = CompactCheckboxGrid(persons, columns=2)
        self.person_checkboxes = person_grid.checkboxes
        person_card.add_widget(person_grid)
        panel_layout.addWidget(person_card)
        
        # Triggers - collapsible and more compact
        trigger_card = CollapsibleCard("Subjunctive Triggers", collapsed=True)
        
        # Scrollable trigger area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMaximumHeight(150)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(2)
        
        self.trigger_checkboxes = []
        triggers = [
            "Wishes (querer que, desear que)",
            "Emotions (gustar que, sentir que)",
            "Impersonal expressions (es bueno que)",
            "Requests (pedir que, rogar que)",
            "Doubt/Denial (dudar que, no creer que)",
            "Negation (no pensar que)",
            "Ojalá (ojalá que)",
            "Conjunctions (para que, antes de que)",
            "Superlatives (el mejor ... que)",
            "Indefinite antecedents (busco a alguien que...)",
            "Nonexistent antecedents (no hay nadie que...)"
        ]
        
        for trigger in triggers:
            cb = QCheckBox(trigger)
            cb.setStyleSheet("QCheckBox { font-size: 11px; padding: 1px; }")
            scroll_layout.addWidget(cb)
            self.trigger_checkboxes.append(cb)
            
        scroll_area.setWidget(scroll_widget)
        trigger_card.add_widget(scroll_area)
        
        # Custom context input
        self.custom_context_input = QLineEdit()
        self.custom_context_input.setPlaceholderText("Additional context...")
        self.custom_context_input.setStyleSheet("""
            QLineEdit {
                font-size: 11px;
                padding: 6px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """)
        trigger_card.add_widget(self.custom_context_input)
        panel_layout.addWidget(trigger_card)
        
        # Specific verbs - collapsible
        verb_card = CollapsibleCard("Specific Verbs", collapsed=True)
        self.verbs_input = QLineEdit()
        self.verbs_input.setPlaceholderText("e.g., hablar, comer, vivir")
        self.verbs_input.setStyleSheet("""
            QLineEdit {
                font-size: 11px;
                padding: 6px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """)
        verb_card.add_widget(self.verbs_input)
        panel_layout.addWidget(verb_card)
        
        # Generate button
        self.generate_button = QPushButton("Generate New Exercises")
        self.generate_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 12px;
                font-size: 13px;
                font-weight: bold;
                border-radius: 6px;
                margin: 5px 0px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        panel_layout.addWidget(self.generate_button)
        
        panel_layout.addStretch()
        return panel_widget
        
    def _connect_signals(self):
        """Connect internal signals to external interface"""
        self.generate_button.clicked.connect(self.exercise_generated.emit)
        self.submit_button.clicked.connect(self._on_submit_clicked)
        self.hint_button.clicked.connect(self.hint_requested.emit)
        self.next_button.clicked.connect(lambda: self.navigation_requested.emit('next'))
        self.prev_button.clicked.connect(lambda: self.navigation_requested.emit('prev'))
        
        # Enter key submits
        self.free_response_input.returnPressed.connect(self._on_submit_clicked)
        
    def _on_submit_clicked(self):
        """Handle submit button click"""
        answer = self.get_user_answer()
        self.answer_submitted.emit(answer)
        
    def get_user_answer(self) -> str:
        """Get the current user answer"""
        if self.input_stack.currentIndex() == 0:  # Free response
            return self.free_response_input.text().strip()
        else:  # Multiple choice
            for button in self.mc_button_group.buttons():
                if button.isChecked():
                    return button.text().strip()
        return ""
        
    def set_exercise_content(self, sentence: str, translation: str = "", show_translation: bool = False):
        """Set the current exercise content"""
        self.sentence_label.setText(sentence)
        self.translation_label.setText(translation)
        self.translation_label.setVisible(show_translation and bool(translation))
        
    def set_multiple_choice_options(self, options: List[str]):
        """Set multiple choice options"""
        # Clear existing options
        for i in reversed(range(self.mc_options_layout.count())):
            child = self.mc_options_layout.itemAt(i).widget()
            if child:
                child.setParent(None)
                
        self.mc_button_group = QButtonGroup()
        
        # Add new options
        for option in options:
            radio = QRadioButton(option)
            radio.setStyleSheet("""
                QRadioButton {
                    font-size: 13px;
                    padding: 6px;
                    spacing: 8px;
                }
                QRadioButton::indicator {
                    width: 16px;
                    height: 16px;
                }
            """)
            self.mc_button_group.addButton(radio)
            self.mc_options_layout.addWidget(radio)
            
        # Select first option by default
        if self.mc_button_group.buttons():
            self.mc_button_group.buttons()[0].setChecked(True)
            
    def switch_input_mode(self, mode: str):
        """Switch between free response and multiple choice"""
        if mode == "Free Response":
            self.input_stack.setCurrentIndex(0)
            self.free_response_input.clear()
            self.free_response_input.setFocus()
        else:
            self.input_stack.setCurrentIndex(1)
            
    def update_progress(self, current: int, total: int, correct: int, accuracy: float):
        """Update progress information"""
        self.progress_section.update_progress(current, total, correct, accuracy)
        
    def update_streak(self, current: int, best: int):
        """Update streak information"""
        self.progress_section.update_streak(current, best)
        
    def set_feedback(self, feedback: str):
        """Set feedback text"""
        self.feedback_text.setPlainText(feedback)
        
    def clear_feedback(self):
        """Clear feedback text"""
        self.feedback_text.clear()
        
    def clear_answer_input(self):
        """Clear the current answer input"""
        if self.input_stack.currentIndex() == 0:
            self.free_response_input.clear()
        # For multiple choice, the selection will remain
        
    def get_selected_tenses(self) -> List[str]:
        """Get selected tenses"""
        return [tense for tense, cb in self.tense_checkboxes.items() if cb.isChecked()]
        
    def get_selected_persons(self) -> List[str]:
        """Get selected persons"""
        return [person for person, cb in self.person_checkboxes.items() if cb.isChecked()]
        
    def get_selected_triggers(self) -> List[str]:
        """Get selected triggers"""
        return [cb.text() for cb in self.trigger_checkboxes if cb.isChecked()]
        
    def get_custom_context(self) -> str:
        """Get custom context text"""
        return self.custom_context_input.text().strip()
        
    def get_specific_verbs(self) -> str:
        """Get specific verbs text"""
        return self.verbs_input.text().strip()
        
    def get_difficulty(self) -> str:
        """Get selected difficulty"""
        return self.difficulty_combo.currentText()
        
    def get_mode(self) -> str:
        """Get selected mode"""
        return self.mode_combo.currentText()
        
    def get_task_type(self) -> str:
        """Get selected task type"""
        return self.task_type_combo.currentText()
        
    def set_button_enabled(self, button_name: str, enabled: bool):
        """Enable/disable specific buttons"""
        button_map = {
            'prev': self.prev_button,
            'next': self.next_button,
            'submit': self.submit_button,
            'hint': self.hint_button,
            'generate': self.generate_button
        }
        
        if button_name in button_map:
            button_map[button_name].setEnabled(enabled)


# Example integration function
def create_optimized_layout(parent=None) -> OptimizedSubjunctiveLayout:
    """
    Factory function to create an optimized layout instance
    """
    layout = OptimizedSubjunctiveLayout(parent)
    
    # Apply additional global styling
    layout.setStyleSheet("""
        QWidget {
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 8px;
            padding: 0px 8px 0px 8px;
            font-weight: bold;
            color: #333;
        }
        
        QScrollArea {
            background-color: transparent;
        }
        
        QScrollBar:vertical {
            background-color: #f0f0f0;
            width: 12px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #c0c0c0;
            border-radius: 6px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #a0a0a0;
        }
    """)
    
    return layout


if __name__ == "__main__":
    # Demo application
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    layout = create_optimized_layout()
    layout.setWindowTitle("Optimized Spanish Subjunctive Layout")
    layout.resize(1200, 800)
    layout.show()
    
    sys.exit(app.exec_())
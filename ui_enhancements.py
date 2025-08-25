# UI/UX Enhancement Module
# Provides improved styling, layout, and interaction patterns

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from clean_ui_colors import CleanColors, RichStyles, ColorScheme, primary, success, warning, error, gray

class ModernButton(QPushButton):
    """Enhanced button with hover effects and better visual feedback"""
    def __init__(self, text, button_type="primary"):
        super().__init__(text)
        self.button_type = button_type
        self.setMinimumHeight(40)
        self.setCursor(Qt.PointingHandCursor)
        self.apply_style()
        
    def apply_style(self):
        if self.button_type == "primary":
            style = f"""
                QPushButton {{
                    background: {CleanColors.PRIMARY};
                    color: {CleanColors.TEXT_WHITE};
                    border: none;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-weight: bold;
                    font-size: 16px;
                }}
                QPushButton:hover {{
                    background: {CleanColors.PRIMARY_HOVER};
                    transform: translateY(-1px);
                }}
                QPushButton:pressed {{
                    background: {CleanColors.PRIMARY_HOVER};
                }}
                QPushButton:focus {{
                    outline: 2px solid {CleanColors.FOCUS};
                    outline-offset: 2px;
                }}
            """
        elif self.button_type == "secondary":
            style = f"""
                QPushButton {{
                    background: {CleanColors.BACKGROUND_CARD};
                    color: {CleanColors.TEXT_PRIMARY};
                    border: 1px solid {CleanColors.BORDER};
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-size: 16px;
                }}
                QPushButton:hover {{
                    background: {CleanColors.HOVER};
                    border-color: {CleanColors.BORDER_FOCUS};
                }}
                QPushButton:focus {{
                    outline: 2px solid {CleanColors.FOCUS};
                    outline-offset: 2px;
                }}
            """
        self.setStyleSheet(style)

class ProgressCard(QFrame):
    """Consolidated progress display card"""
    def __init__(self):
        super().__init__()
        self.setFrameStyle(QFrame.Box)
        self.setStyleSheet(f"""
            QFrame {{
                background: {CleanColors.BACKGROUND_CARD};
                border: 1px solid {CleanColors.BORDER_LIGHT};
                border-radius: 12px;
                padding: 15px;
                margin: 5px;
            }}
        """)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("📊 Progress")
        header.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {CleanColors.TEXT_PRIMARY};")
        layout.addWidget(header)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: 6px;
                background-color: {CleanColors.GRAY_200};
                height: 12px;
            }}
            QProgressBar::chunk {{
                background: {CleanColors.SUCCESS};
                border-radius: 6px;
            }}
        """)
        layout.addWidget(self.progress_bar)
        
        # Stats grid
        stats_layout = QGridLayout()
        stats_layout.setSpacing(10)
        
        self.exercise_label = QLabel("Exercise: 0/0")
        self.accuracy_label = QLabel("Accuracy: 0%")
        self.streak_label = QLabel("Streak: 0 days")
        
        stats_layout.addWidget(self.exercise_label, 0, 0)
        stats_layout.addWidget(self.accuracy_label, 0, 1)
        stats_layout.addWidget(self.streak_label, 1, 0, 1, 2)
        
        layout.addLayout(stats_layout)
        
    def update_progress(self, current, total, accuracy, streak):
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(current)
        self.exercise_label.setText(f"Exercise: {current}/{total}")
        self.accuracy_label.setText(f"Accuracy: {accuracy:.1f}%")
        self.streak_label.setText(f"🔥 Streak: {streak} days")

class ExerciseCard(QFrame):
    """Card-based exercise display"""
    def __init__(self):
        super().__init__()
        self.setFrameStyle(QFrame.Box)
        self.setStyleSheet(f"""
            QFrame {{
                background: {CleanColors.BACKGROUND_CARD};
                border: 1px solid {CleanColors.BORDER_LIGHT};
                border-radius: 16px;
                padding: 20px;
                margin: 10px;
            }}
        """)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Context section
        self.context_label = QLabel()
        self.context_label.setStyleSheet(f"""
            background-color: {CleanColors.PRIMARY_LIGHT};
            padding: 12px;
            border-radius: 8px;
            border-left: 4px solid {CleanColors.PRIMARY};
            font-style: italic;
            color: {CleanColors.PRIMARY};
        """)
        self.context_label.setWordWrap(True)
        layout.addWidget(self.context_label)
        
        # Main sentence
        self.sentence_label = QLabel()
        self.sentence_label.setStyleSheet(f"""
            font-size: 20px;
            font-weight: 500;
            color: {CleanColors.TEXT_PRIMARY};
            padding: 15px;
            line-height: 1.4;
        """)
        self.sentence_label.setWordWrap(True)
        layout.addWidget(self.sentence_label)
        
        # Translation (optional)
        self.translation_label = QLabel()
        self.translation_label.setStyleSheet(f"""
            color: {CleanColors.TEXT_SECONDARY};
            font-style: italic;
            padding: 8px;
            border-top: 1px solid {CleanColors.BORDER_LIGHT};
        """)
        self.translation_label.setWordWrap(True)
        self.translation_label.hide()
        layout.addWidget(self.translation_label)
        
    def update_content(self, context, sentence, translation="", show_translation=False):
        if context:
            self.context_label.setText(f"📍 Context: {context}")
            self.context_label.show()
        else:
            self.context_label.hide()
            
        self.sentence_label.setText(sentence)
        
        if show_translation and translation:
            self.translation_label.setText(f"💬 {translation}")
            self.translation_label.show()
        else:
            self.translation_label.hide()

class SmartInputField(QLineEdit):
    """Enhanced input field with visual feedback"""
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(45)
        self.apply_neutral_style()
        
    def apply_neutral_style(self):
        self.setStyleSheet(f"""
            QLineEdit {{
                border: 2px solid {CleanColors.BORDER};
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 16px;
                background-color: {CleanColors.BACKGROUND};
            }}
            QLineEdit:focus {{
                border-color: {CleanColors.BORDER_FOCUS};
                background-color: {CleanColors.PRIMARY_LIGHT};
            }}
        """)
        
    def apply_correct_style(self):
        self.setStyleSheet(f"""
            QLineEdit {{
                border: 2px solid {CleanColors.SUCCESS};
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 16px;
                background-color: {CleanColors.SUCCESS_LIGHT};
                color: {CleanColors.SUCCESS_HOVER};
            }}
        """)
        
    def apply_incorrect_style(self):
        self.setStyleSheet(f"""
            QLineEdit {{
                border: 2px solid {CleanColors.ERROR};
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 16px;
                background-color: {CleanColors.ERROR_LIGHT};
                color: {CleanColors.ERROR_HOVER};
            }}
        """)
        
    def shake_animation(self):
        """Animate field on incorrect answer"""
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(500)
        start_pos = self.pos()
        
        self.animation.setKeyValueAt(0, start_pos)
        self.animation.setKeyValueAt(0.1, start_pos + QPoint(-10, 0))
        self.animation.setKeyValueAt(0.3, start_pos + QPoint(10, 0))
        self.animation.setKeyValueAt(0.5, start_pos + QPoint(-5, 0))
        self.animation.setKeyValueAt(0.7, start_pos + QPoint(5, 0))
        self.animation.setKeyValueAt(1, start_pos)
        
        self.animation.start()

class FeedbackCard(QFrame):
    """Enhanced feedback display"""
    def __init__(self):
        super().__init__()
        self.setFrameStyle(QFrame.Box)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setStyleSheet("font-size: 32px; margin: 10px;")
        layout.addWidget(self.icon_label)
        
        self.feedback_text = QTextEdit()
        self.feedback_text.setReadOnly(True)
        self.feedback_text.setMaximumHeight(120)
        layout.addWidget(self.feedback_text)
        
    def show_correct_feedback(self, text):
        self.setStyleSheet(f"""
            QFrame {{
                background: {CleanColors.SUCCESS_LIGHT};
                border: 2px solid {CleanColors.SUCCESS};
                border-radius: 12px;
                padding: 15px;
            }}
        """)
        self.icon_label.setText("✅")
        self.feedback_text.setHtml(f"<b style='color: {CleanColors.SUCCESS_HOVER};'>Correct!</b><br>{text}")
        
    def show_incorrect_feedback(self, text):
        self.setStyleSheet(f"""
            QFrame {{
                background: {CleanColors.ERROR_LIGHT};
                border: 2px solid {CleanColors.ERROR};
                border-radius: 12px;
                padding: 15px;
            }}
        """)
        self.icon_label.setText("❌")
        self.feedback_text.setHtml(f"<b style='color: {CleanColors.ERROR_HOVER};'>Incorrect</b><br>{text}")
        
    def show_hint(self, text):
        self.setStyleSheet(f"""
            QFrame {{
                background: {CleanColors.WARNING_LIGHT};
                border: 2px solid {CleanColors.WARNING};
                border-radius: 12px;
                padding: 15px;
            }}
        """)
        self.icon_label.setText("💡")
        self.feedback_text.setHtml(f"<b style='color: {CleanColors.WARNING_HOVER};'>Hint:</b><br>{text}")

class ModernTheme:
    """Modern color scheme and styling"""
    
    @staticmethod
    def get_light_theme():
        return f"""
            QMainWindow {{
                background-color: {CleanColors.BACKGROUND_SECONDARY};
                color: {CleanColors.TEXT_PRIMARY};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            QGroupBox {{
                font-weight: 600;
                border: 2px solid {CleanColors.BORDER};
                border-radius: 12px;
                margin-top: 12px;
                padding-top: 8px;
                background-color: {CleanColors.BACKGROUND};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 16px;
                padding: 0 8px 0 8px;
                color: {CleanColors.TEXT_SECONDARY};
            }}
            QComboBox {{
                border: 2px solid {CleanColors.BORDER};
                border-radius: 8px;
                padding: 8px 12px;
                min-width: 120px;
                background-color: {CleanColors.BACKGROUND};
                color: {CleanColors.TEXT_PRIMARY};
            }}
            QComboBox:focus {{
                border-color: {CleanColors.BORDER_FOCUS};
            }}
            QCheckBox, QRadioButton {{
                spacing: 8px;
                font-size: 16px;
                padding: 6px;
                color: {CleanColors.TEXT_PRIMARY};
            }}
            QCheckBox::indicator, QRadioButton::indicator {{
                width: 18px;
                height: 18px;
                border-radius: 9px;
                border: 2px solid {CleanColors.BORDER};
                background-color: {CleanColors.BACKGROUND};
            }}
            QCheckBox::indicator:checked {{
                background-color: {CleanColors.SUCCESS};
                border-color: {CleanColors.SUCCESS};
            }}
            QScrollArea {{
                border: 1px solid {CleanColors.BORDER};
                border-radius: 8px;
                background-color: {CleanColors.BACKGROUND};
            }}
            QToolBar {{
                background: {CleanColors.BACKGROUND_CARD};
                border-bottom: 1px solid {CleanColors.BORDER};
                padding: 8px;
            }}
            QStatusBar {{
                background-color: {CleanColors.BACKGROUND_CARD};
                border-top: 1px solid {CleanColors.BORDER};
                color: {CleanColors.TEXT_SECONDARY};
            }}
        """
    
    @staticmethod
    def get_dark_theme():
        # Dark theme using inverted clean colors
        return f"""
            QMainWindow {{
                background-color: {CleanColors.GRAY_900};
                color: {CleanColors.TEXT_WHITE};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            QGroupBox {{
                font-weight: 600;
                border: 2px solid {CleanColors.GRAY_600};
                border-radius: 12px;
                margin-top: 12px;
                padding-top: 8px;
                background-color: {CleanColors.GRAY_800};
                color: {CleanColors.TEXT_WHITE};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 16px;
                padding: 0 8px 0 8px;
                color: {CleanColors.TEXT_WHITE};
            }}
            QComboBox {{
                border: 2px solid {CleanColors.GRAY_600};
                border-radius: 8px;
                padding: 8px 12px;
                min-width: 120px;
                background-color: {CleanColors.GRAY_800};
                color: {CleanColors.TEXT_WHITE};
            }}
            QComboBox:focus {{
                border-color: {CleanColors.PRIMARY};
            }}
            QCheckBox, QRadioButton {{
                spacing: 8px;
                font-size: 16px;
                padding: 6px;
                color: {CleanColors.TEXT_WHITE};
            }}
            QScrollArea {{
                border: 1px solid {CleanColors.GRAY_600};
                border-radius: 8px;
                background-color: {CleanColors.GRAY_800};
            }}
            QToolBar {{
                background: {CleanColors.GRAY_800};
                border-bottom: 1px solid {CleanColors.GRAY_600};
                padding: 8px;
            }}
            QStatusBar {{
                background-color: {CleanColors.GRAY_900};
                border-top: 1px solid {CleanColors.GRAY_600};
                color: {CleanColors.TEXT_WHITE};
            }}
        """
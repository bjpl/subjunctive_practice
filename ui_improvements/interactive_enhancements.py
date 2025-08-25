# Interactive Element Improvements for Spanish Subjunctive Practice

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class AnimatedButton(QPushButton):
    """Button with hover animations and state feedback"""
    
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.original_size = None
        self.hover_animation = QPropertyAnimation(self, b"geometry")
        self.hover_animation.setDuration(150)
        self.hover_animation.setEasingCurve(QEasingCurve.OutCubic)
        
    def enterEvent(self, event):
        if not self.original_size:
            self.original_size = self.size()
        
        # Slightly grow on hover
        new_size = QSize(self.original_size.width() + 4, self.original_size.height() + 2)
        target_rect = QRect(self.pos() - QPoint(2, 1), new_size)
        
        self.hover_animation.setStartValue(self.geometry())
        self.hover_animation.setEndValue(target_rect)
        self.hover_animation.start()
        
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        if self.original_size:
            target_rect = QRect(self.pos() + QPoint(2, 1), self.original_size)
            
            self.hover_animation.setStartValue(self.geometry())
            self.hover_animation.setEndValue(target_rect)
            self.hover_animation.start()
        
        super().leaveEvent(event)

class SmartLineEdit(QLineEdit):
    """Enhanced input field with real-time feedback and suggestions"""
    
    suggestion_selected = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.suggestions = []
        self.suggestion_popup = None
        self.current_feedback_state = None
        
        # Real-time validation
        self.textChanged.connect(self.on_text_changed)
        
        # Enhanced styling with transitions
        self.setStyleSheet("""
            QLineEdit {
                font-size: 18px;
                padding: 16px;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                background-color: #ffffff;
                transition: all 0.2s ease;
            }
            QLineEdit:focus {
                border-color: #4299e1;
                background-color: #f7fafc;
            }
        """)
    
    def on_text_changed(self, text):
        """Provide real-time feedback as user types"""
        if len(text) > 2:
            self.show_suggestions(text)
        else:
            self.hide_suggestions()
    
    def show_suggestions(self, text):
        """Show contextual suggestions"""
        # Mock suggestions - in real app, these would be intelligent
        common_endings = ['e', 'es', 'a', 'as', 'emos', 'éis', 'an']
        
        if text.endswith(('habl', 'com', 'viv')):
            self.suggestions = [f"{text}{ending}" for ending in common_endings[:4]]
            self.create_suggestion_popup()
    
    def create_suggestion_popup(self):
        """Create floating suggestion popup"""
        if not self.suggestions:
            return
            
        if self.suggestion_popup:
            self.suggestion_popup.close()
        
        self.suggestion_popup = QFrame(self.parent())
        self.suggestion_popup.setFrameStyle(QFrame.Box)
        self.suggestion_popup.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #cbd5e0;
                border-radius: 8px;
                padding: 8px;
            }
        """)
        
        layout = QVBoxLayout(self.suggestion_popup)
        layout.setSpacing(2)
        
        for suggestion in self.suggestions[:4]:  # Limit to 4 suggestions
            btn = QPushButton(suggestion)
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 8px 12px;
                    border: none;
                    border-radius: 4px;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: #edf2f7;
                }
            """)
            btn.clicked.connect(lambda checked, s=suggestion: self.select_suggestion(s))
            layout.addWidget(btn)
        
        # Position popup below input
        global_pos = self.mapToGlobal(QPoint(0, self.height() + 2))
        self.suggestion_popup.move(global_pos)
        self.suggestion_popup.resize(self.width(), self.suggestion_popup.sizeHint().height())
        self.suggestion_popup.show()
    
    def select_suggestion(self, suggestion):
        """User selected a suggestion"""
        self.setText(suggestion)
        self.hide_suggestions()
        self.suggestion_selected.emit(suggestion)
    
    def hide_suggestions(self):
        """Hide suggestion popup"""
        if self.suggestion_popup:
            self.suggestion_popup.close()
            self.suggestion_popup = None
    
    def set_feedback_state(self, state: str):
        """Set visual feedback state (correct/incorrect/neutral)"""
        self.current_feedback_state = state
        
        if state == "correct":
            self.setStyleSheet(self.styleSheet() + """
                QLineEdit {
                    border-color: #48bb78;
                    background-color: #f0fff4;
                }
            """)
            self.show_success_icon()
        elif state == "incorrect":
            self.setStyleSheet(self.styleSheet() + """
                QLineEdit {
                    border-color: #f56565;
                    background-color: #fffafa;
                }
            """)
            self.show_error_icon()
            self.shake_animation()
        else:
            # Reset to neutral
            self.setStyleSheet("""
                QLineEdit {
                    font-size: 18px;
                    padding: 16px;
                    border: 2px solid #e2e8f0;
                    border-radius: 12px;
                    background-color: #ffffff;
                }
            """)
    
    def shake_animation(self):
        """Shake animation for incorrect answers"""
        self.shake_anim = QPropertyAnimation(self, b"geometry")
        self.shake_anim.setDuration(500)
        
        original_rect = self.geometry()
        shake_sequence = [
            original_rect.translated(5, 0),
            original_rect.translated(-5, 0),
            original_rect.translated(3, 0),
            original_rect.translated(-3, 0),
            original_rect
        ]
        
        for i, rect in enumerate(shake_sequence):
            self.shake_anim.setKeyValueAt(i * 0.2, rect)
        
        self.shake_anim.start()
    
    def show_success_icon(self):
        """Show checkmark icon for correct answers"""
        self.setStyleSheet(self.styleSheet() + """
            QLineEdit {
                background-image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTkgMTJMMTEgMTRMMTUgMTAiIHN0cm9rZT0iIzQ4YmI3OCIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
                background-repeat: no-repeat;
                background-position: right 12px center;
                padding-right: 45px;
            }
        """)

class InteractiveMultipleChoice(QWidget):
    """Enhanced multiple choice with card-style options"""
    
    answer_selected = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.options = []
        self.selected_option = None
        self.correct_option = None
        self.setup_ui()
    
    def setup_ui(self):
        self.layout = QGridLayout(self)
        self.layout.setSpacing(12)
        self.button_group = QButtonGroup(self)
    
    def set_options(self, options: list, correct_answer: str = None):
        """Set multiple choice options with enhanced styling"""
        self.clear_options()
        self.options = options
        self.correct_option = correct_answer
        
        for i, option in enumerate(options):
            option_card = self.create_option_card(option, i)
            row, col = divmod(i, 2)  # 2 columns
            self.layout.addWidget(option_card, row, col)
    
    def create_option_card(self, text: str, index: int):
        """Create an interactive option card"""
        card = QWidget()
        card.setObjectName(f"option_{index}")
        card.setCursor(Qt.PointingHandCursor)
        
        # Initial styling
        card.setStyleSheet(f"""
            QWidget#option_{index} {{
                background-color: white;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                padding: 16px;
                min-height: 60px;
            }}
            QWidget#option_{index}:hover {{
                border-color: #cbd5e0;
                background-color: #f7fafc;
                transform: translateY(-2px);
            }}
        """)
        
        layout = QHBoxLayout(card)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Option letter (A, B, C, D)
        letter_label = QLabel(chr(65 + index))  # A, B, C, D
        letter_label.setStyleSheet("""
            QLabel {
                background-color: #edf2f7;
                color: #4a5568;
                border-radius: 20px;
                font-weight: bold;
                font-size: 16px;
                min-width: 40px;
                min-height: 40px;
            }
        """)
        letter_label.setAlignment(Qt.AlignCenter)
        
        # Option text
        text_label = QLabel(text)
        text_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #2d3748;
                padding-left: 12px;
            }
        """)
        text_label.setWordWrap(True)
        
        layout.addWidget(letter_label)
        layout.addWidget(text_label, 1)
        
        # Make card clickable
        card.mousePressEvent = lambda event, t=text, i=index: self.select_option(t, i)
        
        return card
    
    def select_option(self, text: str, index: int):
        """Handle option selection with visual feedback"""
        # Reset all options
        for i in range(len(self.options)):
            card = self.findChild(QWidget, f"option_{i}")
            if card:
                card.setStyleSheet(card.styleSheet().replace("border-color: #4299e1", "border-color: #e2e8f0"))
        
        # Highlight selected option
        selected_card = self.findChild(QWidget, f"option_{index}")
        if selected_card:
            selected_card.setStyleSheet(selected_card.styleSheet() + """
                border-color: #4299e1 !important;
                background-color: #ebf8ff !important;
            """)
        
        self.selected_option = text
        self.answer_selected.emit(text)
    
    def show_correct_answers(self):
        """Show correct/incorrect states after submission"""
        for i, option in enumerate(self.options):
            card = self.findChild(QWidget, f"option_{i}")
            if not card:
                continue
                
            if option == self.correct_option:
                # Correct answer - green
                card.setStyleSheet(card.styleSheet() + """
                    border-color: #48bb78 !important;
                    background-color: #f0fff4 !important;
                """)
                # Add checkmark
                self.add_result_icon(card, "✓", "#48bb78")
            elif option == self.selected_option and option != self.correct_option:
                # Incorrect selected answer - red
                card.setStyleSheet(card.styleSheet() + """
                    border-color: #f56565 !important;
                    background-color: #fffafa !important;
                """)
                # Add X mark
                self.add_result_icon(card, "✗", "#f56565")
    
    def add_result_icon(self, card: QWidget, icon: str, color: str):
        """Add result icon to option card"""
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 20px;
                font-weight: bold;
                background-color: white;
                border: 2px solid {color};
                border-radius: 15px;
                min-width: 30px;
                min-height: 30px;
            }}
        """)
        icon_label.setAlignment(Qt.AlignCenter)
        
        # Position icon in top-right corner
        icon_label.setParent(card)
        icon_label.move(card.width() - 40, 10)
        icon_label.show()
    
    def clear_options(self):
        """Clear all options"""
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.options.clear()
        self.selected_option = None

class ProgressIndicator(QWidget):
    """Enhanced progress indicator with animations"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_progress = 0
        self.target_progress = 0
        self.progress_animation = QPropertyAnimation(self, b"progress")
        self.progress_animation.setDuration(800)
        self.progress_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        self.setMinimumHeight(40)
    
    def paintEvent(self, event):
        """Custom paint for enhanced progress bar"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Background
        bg_rect = QRect(10, 10, self.width() - 20, self.height() - 20)
        painter.setBrush(QColor("#f1f3f4"))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(bg_rect, 10, 10)
        
        # Progress fill
        if self.current_progress > 0:
            progress_width = int((self.width() - 20) * self.current_progress / 100)
            progress_rect = QRect(10, 10, progress_width, self.height() - 20)
            
            gradient = QLinearGradient(0, 0, progress_width, 0)
            gradient.setColorAt(0, QColor("#4CAF50"))
            gradient.setColorAt(1, QColor("#45a049"))
            
            painter.setBrush(QBrush(gradient))
            painter.drawRoundedRect(progress_rect, 10, 10)
        
        # Text
        painter.setPen(QColor("#333333"))
        painter.setFont(QFont("Segoe UI", 10, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, f"{int(self.current_progress)}%")
    
    def set_progress(self, value: int):
        """Set progress with animation"""
        self.target_progress = max(0, min(100, value))
        
        self.progress_animation.setStartValue(self.current_progress)
        self.progress_animation.setEndValue(self.target_progress)
        self.progress_animation.start()
    
    @pyqtProperty(float)
    def progress(self):
        return self.current_progress
    
    @progress.setter
    def progress(self, value):
        self.current_progress = value
        self.update()

class FeedbackDisplay(QTextEdit):
    """Enhanced feedback display with better formatting"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setup_styling()
    
    def setup_styling(self):
        """Setup enhanced styling for feedback"""
        self.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 2px solid #e9ecef;
                border-radius: 12px;
                padding: 16px;
                font-size: 16px;
                line-height: 1.6;
            }
        """)
    
    def show_feedback(self, is_correct: bool, message: str, explanation: str = ""):
        """Show formatted feedback with icons and styling"""
        
        if is_correct:
            icon = "✅"
            color = "#28a745"
            bg_color = "#d4edda"
        else:
            icon = "❌"
            color = "#dc3545"
            bg_color = "#f8d7da"
        
        html_content = f"""
        <div style="background-color: {bg_color}; padding: 16px; border-radius: 8px; margin-bottom: 16px;">
            <h3 style="color: {color}; margin: 0; font-size: 18px;">
                {icon} {message}
            </h3>
        </div>
        """
        
        if explanation:
            html_content += f"""
            <div style="background-color: #f8f9fa; padding: 16px; border-left: 4px solid #6c757d; margin-top: 16px;">
                <h4 style="color: #495057; margin: 0 0 8px 0;">📝 Explanation:</h4>
                <p style="margin: 0; color: #6c757d; line-height: 1.6;">{explanation}</p>
            </div>
            """
        
        self.setHtml(html_content)
    
    def show_hint(self, hint_text: str):
        """Show formatted hint"""
        html_content = f"""
        <div style="background-color: #fff3cd; padding: 16px; border-radius: 8px; border-left: 4px solid #ffc107;">
            <h4 style="color: #856404; margin: 0 0 8px 0;">💡 Hint:</h4>
            <p style="margin: 0; color: #856404; line-height: 1.6;">{hint_text}</p>
        </div>
        """
        self.setHtml(html_content)
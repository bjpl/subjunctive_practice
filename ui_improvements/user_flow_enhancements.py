# User Flow Enhancements for Spanish Subjunctive Practice

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class OnboardingWizard(QDialog):
    """Smooth onboarding experience for new users"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Welcome to Spanish Subjunctive Practice")
        self.setFixedSize(600, 450)
        self.setModal(True)
        
        # Remove window decorations for modern look
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        
        self.current_step = 0
        self.total_steps = 4
        self.user_preferences = {}
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup wizard UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # Content stack
        self.content_stack = QStackedWidget()
        self.create_wizard_steps()
        layout.addWidget(self.content_stack, 1)
        
        # Navigation
        nav = self.create_navigation()
        layout.addWidget(nav)
        
        # Apply styling
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 16px;
            }
        """)
    
    def create_header(self):
        """Create wizard header with progress"""
        header = QWidget()
        header.setFixedHeight(80)
        header.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #667eea, stop:1 #764ba2);
                border-radius: 16px 16px 0 0;
            }
        """)
        
        layout = QVBoxLayout(header)
        layout.setContentsMargins(30, 15, 30, 15)
        
        title = QLabel("Welcome! Let's personalize your learning")
        title.setStyleSheet("""
            color: white;
            font-size: 20px;
            font-weight: 600;
        """)
        
        # Progress indicator
        self.progress_dots = QHBoxLayout()
        for i in range(self.total_steps):
            dot = QLabel("●")
            dot.setFixedSize(12, 12)
            dot.setStyleSheet("color: rgba(255,255,255,0.5); font-size: 16px;")
            dot.setAlignment(Qt.AlignCenter)
            self.progress_dots.addWidget(dot)
        
        self.progress_dots.addStretch()
        
        layout.addWidget(title)
        layout.addLayout(self.progress_dots)
        
        self.update_progress()
        return header
    
    def create_wizard_steps(self):
        """Create all wizard steps"""
        # Step 1: Learning Goal
        step1 = self.create_goal_step()
        self.content_stack.addWidget(step1)
        
        # Step 2: Experience Level
        step2 = self.create_level_step()
        self.content_stack.addWidget(step2)
        
        # Step 3: Practice Preferences
        step3 = self.create_preferences_step()
        self.content_stack.addWidget(step3)
        
        # Step 4: Ready to Start
        step4 = self.create_ready_step()
        self.content_stack.addWidget(step4)
    
    def create_goal_step(self):
        """Step 1: Learning goals"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 30, 40, 30)
        
        title = QLabel("What's your learning goal?")
        title.setStyleSheet("font-size: 24px; font-weight: 600; color: #2d3748; margin-bottom: 20px;")
        layout.addWidget(title)
        
        goals = [
            ("🎯", "Master subjunctive conjugations", "Focus on accurate verb forms and patterns"),
            ("💬", "Improve conversational skills", "Practice real-world communication scenarios"),
            ("📚", "Academic/Test preparation", "Structured practice for exams and coursework"),
            ("🌟", "General Spanish improvement", "Well-rounded practice across all areas")
        ]
        
        self.goal_group = QButtonGroup()
        for emoji, title_text, desc in goals:
            option = self.create_goal_option(emoji, title_text, desc)
            layout.addWidget(option)
            
        layout.addStretch()
        return widget
    
    def create_goal_option(self, emoji: str, title: str, description: str):
        """Create a goal selection option"""
        container = QWidget()
        container.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border: 2px solid #e9ecef;
                border-radius: 12px;
                padding: 16px;
                margin: 8px 0;
            }
            QWidget:hover {
                background-color: #e9ecef;
                border-color: #dee2e6;
            }
        """)
        container.setCursor(Qt.PointingHandCursor)
        
        layout = QHBoxLayout(container)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Emoji
        emoji_label = QLabel(emoji)
        emoji_label.setStyleSheet("font-size: 24px;")
        emoji_label.setFixedSize(40, 40)
        emoji_label.setAlignment(Qt.AlignCenter)
        
        # Text content
        text_layout = QVBoxLayout()
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 16px; font-weight: 600; color: #2d3748;")
        
        desc_label = QLabel(description)
        desc_label.setStyleSheet("font-size: 14px; color: #6c757d; margin-top: 4px;")
        desc_label.setWordWrap(True)
        
        text_layout.addWidget(title_label)
        text_layout.addWidget(desc_label)
        
        # Radio button (hidden but functional)
        radio = QRadioButton()
        radio.setStyleSheet("QRadioButton { margin-left: 20px; }")
        self.goal_group.addButton(radio)
        
        layout.addWidget(emoji_label)
        layout.addLayout(text_layout, 1)
        layout.addWidget(radio)
        
        # Make container clickable
        container.mousePressEvent = lambda event: radio.setChecked(True)
        
        return container
    
    def create_level_step(self):
        """Step 2: Experience level"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 30, 40, 30)
        
        title = QLabel("What's your Spanish level?")
        title.setStyleSheet("font-size: 24px; font-weight: 600; color: #2d3748; margin-bottom: 20px;")
        layout.addWidget(title)
        
        levels = [
            ("🌱", "Beginner", "Just starting with subjunctive"),
            ("🌿", "Intermediate", "Know basics, need practice"),
            ("🌳", "Advanced", "Want to master nuances"),
        ]
        
        self.level_group = QButtonGroup()
        for emoji, level, desc in levels:
            option = self.create_level_option(emoji, level, desc)
            layout.addWidget(option)
        
        layout.addStretch()
        return widget
    
    def create_level_option(self, emoji: str, level: str, description: str):
        """Create level selection option"""
        # Similar to goal option but with different styling
        container = QWidget()
        container.setStyleSheet("""
            QWidget {
                background-color: #f0f4f8;
                border: 2px solid #cbd5e0;
                border-radius: 12px;
                padding: 20px;
                margin: 12px 0;
            }
            QWidget:hover {
                background-color: #e2e8f0;
                border-color: #a0aec0;
            }
        """)
        container.setCursor(Qt.PointingHandCursor)
        
        layout = QHBoxLayout(container)
        
        emoji_label = QLabel(emoji)
        emoji_label.setStyleSheet("font-size: 32px;")
        emoji_label.setFixedSize(50, 50)
        emoji_label.setAlignment(Qt.AlignCenter)
        
        text_layout = QVBoxLayout()
        level_label = QLabel(level)
        level_label.setStyleSheet("font-size: 18px; font-weight: 600; color: #2d3748;")
        
        desc_label = QLabel(description)
        desc_label.setStyleSheet("font-size: 14px; color: #4a5568;")
        
        text_layout.addWidget(level_label)
        text_layout.addWidget(desc_label)
        
        radio = QRadioButton()
        radio.setStyleSheet("QRadioButton { margin-left: 20px; }")
        self.level_group.addButton(radio)
        
        layout.addWidget(emoji_label)
        layout.addLayout(text_layout, 1)
        layout.addWidget(radio)
        
        container.mousePressEvent = lambda event: radio.setChecked(True)
        
        return container
    
    def create_preferences_step(self):
        """Step 3: Practice preferences"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 30, 40, 30)
        
        title = QLabel("How do you like to practice?")
        title.setStyleSheet("font-size: 24px; font-weight: 600; color: #2d3748; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Practice mode preferences
        modes_group = QGroupBox("Preferred Practice Mode")
        modes_layout = QVBoxLayout(modes_group)
        
        self.mode_group = QButtonGroup()
        modes = [
            ("Multiple Choice", "Quick recognition practice"),
            ("Free Response", "Type your answers for better retention"),
            ("Mixed", "Alternate between both modes")
        ]
        
        for mode, desc in modes:
            radio = QRadioButton(f"{mode} - {desc}")
            self.mode_group.addButton(radio)
            modes_layout.addWidget(radio)
        
        # Daily goal
        goal_group = QGroupBox("Daily Practice Goal")
        goal_layout = QVBoxLayout(goal_group)
        
        self.goal_slider = QSlider(Qt.Horizontal)
        self.goal_slider.setRange(5, 50)
        self.goal_slider.setValue(15)
        self.goal_slider.setTickPosition(QSlider.TicksBelow)
        self.goal_slider.setTickInterval(5)
        
        self.goal_label = QLabel("15 exercises per day")
        self.goal_label.setAlignment(Qt.AlignCenter)
        self.goal_label.setStyleSheet("font-weight: 600; color: #4a5568;")
        
        self.goal_slider.valueChanged.connect(
            lambda v: self.goal_label.setText(f"{v} exercises per day")
        )
        
        goal_layout.addWidget(self.goal_label)
        goal_layout.addWidget(self.goal_slider)
        
        layout.addWidget(modes_group)
        layout.addWidget(goal_group)
        layout.addStretch()
        
        return widget
    
    def create_ready_step(self):
        """Step 4: Ready to start"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Success icon
        icon = QLabel("🎉")
        icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet("font-size: 64px; margin-bottom: 20px;")
        layout.addWidget(icon)
        
        title = QLabel("You're all set!")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: 600; color: #2d3748; margin-bottom: 16px;")
        layout.addWidget(title)
        
        subtitle = QLabel("Your personalized learning experience is ready")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 16px; color: #6c757d; margin-bottom: 32px;")
        layout.addWidget(subtitle)
        
        # Summary of selections
        summary = self.create_preferences_summary()
        layout.addWidget(summary)
        
        layout.addStretch()
        
        return widget
    
    def create_preferences_summary(self):
        """Show summary of user preferences"""
        container = QWidget()
        container.setStyleSheet("""
            QWidget {
                background-color: #f7fafc;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(container)
        
        title = QLabel("Your Learning Profile")
        title.setStyleSheet("font-size: 18px; font-weight: 600; color: #2d3748; margin-bottom: 16px;")
        layout.addWidget(title)
        
        # Add summary items based on selections
        summary_items = [
            ("🎯 Goal", "Master subjunctive conjugations"),
            ("📊 Level", "Intermediate"),
            ("🎮 Mode", "Mixed practice"),
            ("⏰ Daily Goal", "15 exercises per day")
        ]
        
        for icon_text, value in summary_items:
            item_layout = QHBoxLayout()
            item_label = QLabel(icon_text)
            item_label.setStyleSheet("font-weight: 500; color: #4a5568;")
            
            value_label = QLabel(value)
            value_label.setStyleSheet("color: #2d3748;")
            
            item_layout.addWidget(item_label)
            item_layout.addStretch()
            item_layout.addWidget(value_label)
            
            layout.addLayout(item_layout)
        
        return container
    
    def create_navigation(self):
        """Create navigation buttons"""
        nav = QWidget()
        nav.setFixedHeight(70)
        nav.setStyleSheet("background-color: #f8f9fa; border-radius: 0 0 16px 16px;")
        
        layout = QHBoxLayout(nav)
        layout.setContentsMargins(30, 15, 30, 15)
        
        self.back_btn = QPushButton("Back")
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 2px solid #dee2e6;
                color: #6c757d;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #e9ecef;
            }
        """)
        self.back_btn.clicked.connect(self.previous_step)
        self.back_btn.setEnabled(False)
        
        self.next_btn = QPushButton("Next")
        self.next_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #4299e1, stop:1 #3182ce);
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #3182ce, stop:1 #2c5282);
            }
        """)
        self.next_btn.clicked.connect(self.next_step)
        
        layout.addWidget(self.back_btn)
        layout.addStretch()
        layout.addWidget(self.next_btn)
        
        return nav
    
    def update_progress(self):
        """Update progress dots"""
        for i in range(self.total_steps):
            dot_widget = self.progress_dots.itemAt(i).widget()
            if i <= self.current_step:
                dot_widget.setStyleSheet("color: white; font-size: 16px;")
            else:
                dot_widget.setStyleSheet("color: rgba(255,255,255,0.5); font-size: 16px;")
    
    def next_step(self):
        """Go to next step"""
        if self.current_step < self.total_steps - 1:
            self.current_step += 1
            self.content_stack.setCurrentIndex(self.current_step)
            self.update_navigation()
            self.update_progress()
    
    def previous_step(self):
        """Go to previous step"""
        if self.current_step > 0:
            self.current_step -= 1
            self.content_stack.setCurrentIndex(self.current_step)
            self.update_navigation()
            self.update_progress()
    
    def update_navigation(self):
        """Update navigation button states"""
        self.back_btn.setEnabled(self.current_step > 0)
        
        if self.current_step == self.total_steps - 1:
            self.next_btn.setText("Start Practicing!")
            self.next_btn.disconnect()
            self.next_btn.clicked.connect(self.accept)
        else:
            self.next_btn.setText("Next")

class QuickStartWidget(QWidget):
    """Quick start options for returning users"""
    
    exercise_type_selected = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup quick start UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QLabel("Quick Start")
        header.setStyleSheet("""
            font-size: 24px;
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 10px;
        """)
        layout.addWidget(header)
        
        subtitle = QLabel("Jump right into practice with these options")
        subtitle.setStyleSheet("font-size: 16px; color: #6c757d; margin-bottom: 20px;")
        layout.addWidget(subtitle)
        
        # Quick start options
        options = [
            ("🚀", "Continue where you left off", "resume"),
            ("🎯", "Practice weak areas", "review"),
            ("⚡", "Quick 5-minute session", "quick"),
            ("🌟", "New exercise set", "new"),
        ]
        
        for emoji, text, action in options:
            option_btn = self.create_quick_option(emoji, text, action)
            layout.addWidget(option_btn)
        
        layout.addStretch()
    
    def create_quick_option(self, emoji: str, text: str, action: str):
        """Create quick start option button"""
        btn = QPushButton()
        btn.setFixedHeight(60)
        btn.setCursor(Qt.PointingHandCursor)
        
        btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                padding: 16px;
                text-align: left;
            }
            QPushButton:hover {
                border-color: #cbd5e0;
                background-color: #f7fafc;
            }
        """)
        
        layout = QHBoxLayout(btn)
        layout.setContentsMargins(16, 8, 16, 8)
        
        emoji_label = QLabel(emoji)
        emoji_label.setStyleSheet("font-size: 24px;")
        emoji_label.setFixedWidth(40)
        
        text_label = QLabel(text)
        text_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 500;
            color: #2d3748;
        """)
        
        arrow_label = QLabel("→")
        arrow_label.setStyleSheet("font-size: 18px; color: #a0aec0;")
        
        layout.addWidget(emoji_label)
        layout.addWidget(text_label, 1)
        layout.addWidget(arrow_label)
        
        btn.clicked.connect(lambda: self.exercise_type_selected.emit(action))
        
        return btn

class ProgressCelebration(QDialog):
    """Celebration dialog for achievements"""
    
    def __init__(self, achievement: str, parent=None):
        super().__init__(parent)
        self.achievement = achievement
        self.setModal(True)
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        
        self.setup_ui()
        self.animate_entrance()
    
    def setup_ui(self):
        """Setup celebration UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        self.setStyleSheet("""
            QDialog {
                background: qradial-gradient(circle at center,
                                           #ffd89b 0%, #19547b 100%);
                border-radius: 20px;
            }
        """)
        
        # Celebration icon
        icon = QLabel("🎉")
        icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet("font-size: 64px; margin-bottom: 10px;")
        layout.addWidget(icon)
        
        # Achievement text
        title = QLabel("Achievement Unlocked!")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: 600;
            color: white;
            margin-bottom: 10px;
        """)
        layout.addWidget(title)
        
        achievement_text = QLabel(self.achievement)
        achievement_text.setAlignment(Qt.AlignCenter)
        achievement_text.setStyleSheet("""
            font-size: 18px;
            color: white;
            font-weight: 500;
            margin-bottom: 20px;
        """)
        achievement_text.setWordWrap(True)
        layout.addWidget(achievement_text)
        
        # Close button
        close_btn = QPushButton("¡Excelente!")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #2d3748;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: 600;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #f7fafc;
            }
        """)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        layout.addStretch()
    
    def animate_entrance(self):
        """Animate dialog entrance"""
        self.setWindowOpacity(0)
        
        self.fade_in = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in.setDuration(300)
        self.fade_in.setStartValue(0)
        self.fade_in.setEndValue(1)
        self.fade_in.setEasingCurve(QEasingCurve.OutCubic)
        self.fade_in.start()
        
        # Scale animation would require custom implementation
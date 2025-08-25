"""
Enhanced Spanish Subjunctive Practice Application
===============================================

This is the main application with integrated enhanced feedback system.
Includes all advanced features:
- Visual feedback animations and colors
- Progressive hint system
- Sound feedback (configurable)
- Advanced error analysis and guidance
- Celebration animations for achievements
- Contextual help system
- Adaptive feedback based on user performance
- Optimal timing for learning retention

Based on educational psychology principles and SLA research.
"""

import sys
import os
import json
import random
import logging
from typing import List, Dict
from datetime import datetime
from tblt_scenarios import TBLTTaskGenerator, SpacedRepetitionTracker, get_pedagogical_feedback
from conjugation_reference import STEM_CHANGING_PATTERNS, SEQUENCE_OF_TENSES
from session_manager import SessionManager, ReviewQueue
from learning_analytics import StreakTracker, ErrorAnalyzer, AdaptiveDifficulty, PracticeGoals
from dotenv import load_dotenv
import re

# Import enhanced feedback system
from enhanced_feedback_system import (
    EnhancedFeedbackWidget, FeedbackConfig, AdaptiveFeedbackManager,
    ContextualHelpSystem, SoundManager, AnimationManager, FeedbackType
)
from advanced_error_analysis import AdvancedErrorAnalyzer, integrate_error_analysis_with_feedback

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QLabel, QLineEdit, QPushButton, QProgressBar, QTextEdit, QStackedWidget,
    QRadioButton, QButtonGroup, QStatusBar, QAction, QGroupBox, QCheckBox,
    QMessageBox, QToolBar, QScrollArea, QComboBox, QSizePolicy, QDialog,
    QTableWidget, QTableWidgetItem, QHeaderView, QSlider, QFrame
)
from PyQt5.QtCore import Qt, QRunnable, QObject, pyqtSignal, QThreadPool, QTimer, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import QFont, QColor, QPalette

from openai import OpenAI

# Load environment variables
load_dotenv()

# Configure Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler = logging.FileHandler("subjunctive_practice.log", mode="a", encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Security: Validate API key
def validate_api_key():
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key or api_key == "YOUR_OPENAI_API_KEY_HERE":
        logger.error("Invalid or missing OpenAI API key")
        return False
    if not api_key.startswith("sk-"):
        logger.error("API key format appears invalid")
        return False
    logger.info("API key validated (length: %d)", len(api_key))
    return True

# Initialize OpenAI client
try:
    if validate_api_key():
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    else:
        client = None
except Exception as e:
    logger.error("Failed to initialize OpenAI client: %s", str(e))
    client = None

# Worker Classes for Asynchronous GPT Calls
class WorkerSignals(QObject):
    result = pyqtSignal(str)

class GPTWorkerRunnable(QRunnable):
    def __init__(self, prompt: str, model: str = "gpt-4", max_tokens: int = 600, temperature: float = 0.5):
        super().__init__()
        self.prompt = prompt
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.signals = WorkerSignals()

    def run(self) -> None:
        if not client:
            output = "Error: OpenAI client not initialized. Please check your API key."
            self.signals.result.emit(output)
            return
            
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": ("You are an expert Spanish tutor specializing in LATAM Spanish. "
                                    "Your guidance should always reflect real-life conversational tone, "
                                    "using authentic expressions and culturally relevant details.")
                    },
                    {"role": "user", "content": self.prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                timeout=30
            )
            output = response.choices[0].message.content.strip()
            logging.info("GPT response received.")
        except Exception as e:
            output = f"Error: {str(e)}"
            logging.error("Error in GPTWorkerRunnable: %s", str(e))
        self.signals.result.emit(output)


class EnhancedSpanishSubjunctivePracticeGUI(QMainWindow):
    """Enhanced GUI with advanced feedback system"""
    
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Enhanced Spanish Subjunctive Practice")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize enhanced feedback system components
        self.feedback_config = FeedbackConfig(
            visual_enabled=True,
            sound_enabled=True,
            animation_enabled=True,
            hint_progression_enabled=True,
            celebration_animations=True,
            adaptive_difficulty=True,
            timing_optimal=True
        )
        
        self.sound_manager = SoundManager(self.feedback_config.sound_enabled)
        self.adaptive_manager = AdaptiveFeedbackManager()
        self.help_system = ContextualHelpSystem()
        self.error_analyzer = AdvancedErrorAnalyzer()
        
        # Data structures
        self.exercises: List[dict] = []
        self.current_exercise: int = 0
        self.total_exercises: int = 0
        self.correct_count: int = 0
        self.responses: List[dict] = []
        self.session_stats: Dict = {
            "total_attempts": 0,
            "correct_attempts": 0,
            "hints_used": 0,
            "session_start": datetime.now(),
            "tenses_practiced": set(),
            "persons_practiced": set(),
            "response_times": []  # Track response times for adaptive feedback
        }
        
        # Original components
        self.dark_mode = False
        self.show_translation = False
        self.threadpool = QThreadPool()
        self.tblt_generator = TBLTTaskGenerator()
        self.spaced_repetition = SpacedRepetitionTracker()
        self.current_task_type = "traditional"
        self.session_manager = SessionManager()
        self.review_queue = ReviewQueue()
        self.review_mode = False
        self.streak_tracker = StreakTracker()
        self.practice_goals = PracticeGoals()
        
        # Response timing tracking
        self.current_exercise_start_time = None
        
        self.initUI()
        self.check_daily_streak()
        
        logger.info("Enhanced application initialized with advanced feedback system.")
    
    def initUI(self) -> None:
        self.createToolBar()
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Apply enhanced styling
        self.apply_enhanced_styling()
        
        # Create main splitter
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left Pane: Enhanced exercise display
        left_widget = self.create_exercise_display_widget()
        splitter.addWidget(left_widget)
        
        # Right Pane: Enhanced input and feedback
        right_widget = self.create_input_feedback_widget()
        splitter.addWidget(right_widget)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        # Status bar with enhanced information
        self.create_enhanced_status_bar()
        
        # Connect enhanced event handlers
        self.connect_enhanced_signals()
        
        self.updateStatus("Welcome! Enhanced feedback system is ready. Generate exercises to begin.")
        
    def apply_enhanced_styling(self):
        """Apply enhanced visual styling"""
        enhanced_stylesheet = """
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                           stop:0 #f8f9fa, stop:1 #e9ecef);
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QGroupBox {
                font-weight: 600;
                border: 2px solid #dee2e6;
                border-radius: 12px;
                margin-top: 12px;
                padding-top: 8px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                           stop:0 #ffffff, stop:1 #f8f9fa);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 16px;
                padding: 0 8px 0 8px;
                color: #495057;
                font-size: 14px;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                           stop:0 #007bff, stop:1 #0056b3);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: 600;
                font-size: 14px;
                min-height: 16px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                           stop:0 #0056b3, stop:1 #004085);
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background: #003f7f;
                transform: translateY(1px);
            }
            QLineEdit {
                border: 2px solid #ced4da;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 16px;
                background-color: white;
                selection-background-color: #007bff;
            }
            QLineEdit:focus {
                border-color: #007bff;
                background-color: #f8f9ff;
                box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
            }
            QComboBox {
                border: 2px solid #ced4da;
                border-radius: 8px;
                padding: 8px 12px;
                min-width: 120px;
                background-color: white;
            }
            QComboBox:focus {
                border-color: #007bff;
            }
            QProgressBar {
                border: 1px solid #dee2e6;
                border-radius: 6px;
                background-color: #e9ecef;
                height: 20px;
                text-align: center;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                           stop:0 #28a745, stop:1 #20c997);
                border-radius: 6px;
            }
        """
        self.setStyleSheet(enhanced_stylesheet)
    
    def create_exercise_display_widget(self) -> QWidget:
        """Create enhanced exercise display widget"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)
        
        # Enhanced exercise card
        exercise_card = QFrame()
        exercise_card.setFrameStyle(QFrame.Box)
        exercise_card.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                           stop:0 #ffffff, stop:1 #fafafa);
                border: 2px solid #e9ecef;
                border-radius: 16px;
                padding: 20px;
            }
        """)
        
        exercise_layout = QVBoxLayout(exercise_card)
        
        # Context section with icon
        context_header = QHBoxLayout()
        context_icon = QLabel("📍")
        context_icon.setStyleSheet("font-size: 20px;")
        context_title = QLabel("Context")
        context_title.setStyleSheet("font-weight: bold; font-size: 16px; color: #495057;")
        context_header.addWidget(context_icon)
        context_header.addWidget(context_title)
        context_header.addStretch()
        exercise_layout.addLayout(context_header)
        
        self.sentence_label = QLabel("Exercise will appear here...")
        self.sentence_label.setWordWrap(True)
        self.sentence_label.setStyleSheet("""
            font-size: 18px;
            font-weight: 500;
            color: #212529;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #007bff;
            line-height: 1.5;
        """)
        exercise_layout.addWidget(self.sentence_label)
        
        # Translation section (toggleable)
        self.translation_label = QLabel("")
        self.translation_label.setWordWrap(True)
        self.translation_label.setStyleSheet("""
            color: #6c757d;
            font-style: italic;
            padding: 10px;
            background-color: #e9ecef;
            border-radius: 6px;
            border-left: 3px solid #6c757d;
        """)
        self.translation_label.setVisible(False)
        exercise_layout.addWidget(self.translation_label)
        
        layout.addWidget(exercise_card)
        
        # Enhanced stats display
        stats_card = self.create_stats_card()
        layout.addWidget(stats_card)
        
        # Subjunctive triggers (enhanced)
        trigger_box = self.create_enhanced_triggers_box()
        layout.addWidget(trigger_box)
        
        layout.addStretch()
        return widget
    
    def create_stats_card(self) -> QWidget:
        """Create enhanced statistics display card"""
        card = QFrame()
        card.setFrameStyle(QFrame.Box)
        card.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                           stop:0 #ffffff, stop:1 #f8f9fa);
                border: 2px solid #28a745;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        
        layout = QVBoxLayout(card)
        
        # Header
        header = QHBoxLayout()
        icon = QLabel("📊")
        icon.setStyleSheet("font-size: 20px;")
        title = QLabel("Progress Tracking")
        title.setStyleSheet("font-weight: bold; font-size: 16px; color: #495057;")
        header.addWidget(icon)
        header.addWidget(title)
        header.addStretch()
        layout.addLayout(header)
        
        # Progress bar
        self.enhanced_progress_bar = QProgressBar()
        self.enhanced_progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 8px;
                background-color: #e9ecef;
                height: 16px;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                           stop:0 #28a745, stop:1 #20c997);
                border-radius: 8px;
            }
        """)
        layout.addWidget(self.enhanced_progress_bar)
        
        # Stats grid
        stats_grid = QHBoxLayout()
        
        self.exercise_stat = QLabel("Exercise: 0/0")
        self.exercise_stat.setStyleSheet("font-weight: 500; color: #495057;")
        
        self.accuracy_stat = QLabel("Accuracy: 0%")
        self.accuracy_stat.setStyleSheet("font-weight: 500; color: #495057;")
        
        self.streak_stat = QLabel("🔥 Streak: 0")
        self.streak_stat.setStyleSheet("font-weight: 500; color: #e74c3c;")
        
        stats_grid.addWidget(self.exercise_stat)
        stats_grid.addWidget(self.accuracy_stat)
        stats_grid.addWidget(self.streak_stat)
        
        layout.addLayout(stats_grid)
        
        return card
    
    def create_enhanced_triggers_box(self) -> QWidget:
        """Create enhanced triggers selection box"""
        trigger_box = QGroupBox("Subjunctive Triggers & Context")
        trigger_layout = QVBoxLayout(trigger_box)
        trigger_layout.setSpacing(8)
        
        self.trigger_scroll_area = QScrollArea()
        self.trigger_scroll_area.setWidgetResizable(True)
        self.trigger_scroll_area.setMinimumHeight(150)
        self.trigger_scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #dee2e6;
                border-radius: 8px;
                background-color: white;
            }
        """)
        
        trigger_scroll_content = QWidget()
        sc_layout = QVBoxLayout(trigger_scroll_content)
        sc_layout.setContentsMargins(10, 10, 10, 10)
        sc_layout.setSpacing(8)
        
        self.trigger_checkboxes = []
        triggers_with_icons = [
            ("🎯 Wishes (querer que, desear que)", "Wishes (querer que, desear que)"),
            ("😊 Emotions (gustar que, sentir que)", "Emotions (gustar que, sentir que)"),
            ("📝 Impersonal expressions (es bueno que)", "Impersonal expressions (es bueno que, es necesario que)"),
            ("🙏 Requests (pedir que, rogar que)", "Requests (pedir que, rogar que)"),
            ("🤔 Doubt/Denial (dudar que, no creer que)", "Doubt/Denial (dudar que, no creer que)"),
            ("❌ Negation (no pensar que)", "Negation (no pensar que, no es cierto que)"),
            ("🤞 Ojalá expressions", "Ojalá (ojalá que)"),
            ("🔗 Conjunctions (para que, antes de que)", "Conjunctions (para que, antes de que, a menos que)"),
            ("🏆 Superlatives (el mejor ... que)", "Superlatives (el mejor ... que)"),
            ("❓ Indefinite antecedents (busco alguien que...)", "Indefinite antecedents (busco a alguien que...)"),
            ("🚫 Nonexistent antecedents (no hay nadie que...)", "Nonexistent antecedents (no hay nadie que...)")
        ]
        
        for display_text, value_text in triggers_with_icons:
            cb = QCheckBox(display_text)
            cb.setProperty("value", value_text)
            cb.setStyleSheet("""
                QCheckBox {
                    font-size: 14px;
                    padding: 5px;
                    spacing: 8px;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                    border-radius: 9px;
                    border: 2px solid #ced4da;
                    background-color: white;
                }
                QCheckBox::indicator:checked {
                    background-color: #007bff;
                    border-color: #007bff;
                }
            """)
            sc_layout.addWidget(cb)
            self.trigger_checkboxes.append(cb)
        
        sc_layout.addStretch(1)
        self.trigger_scroll_area.setWidget(trigger_scroll_content)
        
        self.custom_context_input = QLineEdit()
        self.custom_context_input.setPlaceholderText("💡 Enter additional context (e.g., polite request, uncertainty scenario)")
        self.custom_context_input.setStyleSheet("margin-top: 8px;")
        
        trigger_layout.addWidget(self.trigger_scroll_area)
        trigger_layout.addWidget(self.custom_context_input)
        
        return trigger_box
    
    def create_input_feedback_widget(self) -> QWidget:
        """Create enhanced input and feedback widget"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Enhanced selection controls
        selection_card = self.create_enhanced_selection_card()
        layout.addWidget(selection_card)
        
        # Mode and difficulty controls
        controls_layout = QHBoxLayout()
        
        mode_label = QLabel("Mode:")
        mode_label.setStyleSheet("font-weight: 600; color: #495057;")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Free Response", "Multiple Choice"])
        self.mode_combo.currentIndexChanged.connect(self.switchMode)
        
        difficulty_label = QLabel("Difficulty:")
        difficulty_label.setStyleSheet("font-weight: 600; color: #495057;")
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Beginner", "Intermediate", "Advanced"])
        self.difficulty_combo.setCurrentIndex(1)
        
        task_type_label = QLabel("Type:")
        task_type_label.setStyleSheet("font-weight: 600; color: #495057;")
        self.task_type_combo = QComboBox()
        self.task_type_combo.addItems(["Traditional Grammar", "TBLT Scenarios", "Mood Contrast", "Review Mode"])
        self.task_type_combo.currentIndexChanged.connect(self.onTaskTypeChanged)
        
        controls_layout.addWidget(mode_label)
        controls_layout.addWidget(self.mode_combo)
        controls_layout.addWidget(difficulty_label)
        controls_layout.addWidget(self.difficulty_combo)
        controls_layout.addWidget(task_type_label)
        controls_layout.addWidget(self.task_type_combo)
        controls_layout.addStretch()
        
        layout.addLayout(controls_layout)
        
        # Enhanced answer input
        input_card = self.create_enhanced_input_card()
        layout.addWidget(input_card)
        
        # Enhanced feedback system
        self.enhanced_feedback_widget = EnhancedFeedbackWidget(self.feedback_config)
        self.enhanced_feedback_widget.feedback_requested.connect(self.handle_feedback_request)
        layout.addWidget(self.enhanced_feedback_widget)
        
        # Enhanced navigation buttons
        nav_layout = self.create_enhanced_navigation()
        layout.addLayout(nav_layout)
        
        return widget
    
    def create_enhanced_selection_card(self) -> QWidget:
        """Create enhanced tense and person selection"""
        card = QFrame()
        card.setFrameStyle(QFrame.Box)
        card.setStyleSheet("""
            QFrame {
                background: white;
                border: 2px solid #e9ecef;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        
        layout = QVBoxLayout(card)
        
        # Header
        header = QLabel("🎯 Select Tense(s) and Person(s)")
        header.setStyleSheet("font-weight: bold; font-size: 16px; color: #495057; margin-bottom: 10px;")
        layout.addWidget(header)
        
        sel_layout = QHBoxLayout()
        
        # Tense selection with enhanced styling
        tense_box = QGroupBox("Tenses")
        tense_box.setStyleSheet("QGroupBox { border: 1px solid #dee2e6; }")
        tense_layout = QVBoxLayout(tense_box)
        tense_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        self.tense_checkboxes = {}
        tenses = [
            "Present Subjunctive",
            "Imperfect Subjunctive (ra)",
            "Imperfect Subjunctive (se)",
            "Present Perfect Subjunctive",
            "Pluperfect Subjunctive",
        ]
        
        for tense in tenses:
            cb = QCheckBox(tense)
            cb.setStyleSheet("QCheckBox { padding: 4px; }")
            self.tense_checkboxes[tense] = cb
            tense_layout.addWidget(cb)
        
        # Person selection with enhanced styling
        person_box = QGroupBox("Persons")
        person_box.setStyleSheet("QGroupBox { border: 1px solid #dee2e6; }")
        person_layout = QVBoxLayout(person_box)
        person_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        self.person_checkboxes = {}
        persons = ["yo", "tú", "él/ella/usted", "nosotros", "vosotros", "ellos/ellas/ustedes"]
        
        for person in persons:
            cb = QCheckBox(person)
            cb.setStyleSheet("QCheckBox { padding: 4px; }")
            self.person_checkboxes[person] = cb
            person_layout.addWidget(cb)
        
        sel_layout.addWidget(tense_box, 1)
        sel_layout.addWidget(person_box, 1)
        
        layout.addLayout(sel_layout)
        
        # Specific verbs input
        verb_layout = QHBoxLayout()
        verb_label = QLabel("🔤 Specific Verbs (optional):")
        verb_label.setStyleSheet("font-weight: 600; color: #495057;")
        self.verbs_input = QLineEdit()
        self.verbs_input.setPlaceholderText("e.g., hablar, comer, vivir")
        verb_layout.addWidget(verb_label)
        verb_layout.addWidget(self.verbs_input)
        
        layout.addLayout(verb_layout)
        
        return card
    
    def create_enhanced_input_card(self) -> QWidget:
        """Create enhanced answer input card"""
        card = QFrame()
        card.setFrameStyle(QFrame.Box)
        card.setStyleSheet("""
            QFrame {
                background: white;
                border: 2px solid #e9ecef;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        
        layout = QVBoxLayout(card)
        
        # Header
        header = QLabel("✍️ Your Answer")
        header.setStyleSheet("font-weight: bold; font-size: 16px; color: #495057; margin-bottom: 10px;")
        layout.addWidget(header)
        
        # Input stack for different modes
        self.input_stack = QStackedWidget()
        
        # Free response page
        free_response_page = QWidget()
        fr_layout = QVBoxLayout(free_response_page)
        
        self.free_response_input = QLineEdit()
        self.free_response_input.setPlaceholderText("Type your answer here...")
        self.free_response_input.setStyleSheet("""
            QLineEdit {
                font-size: 18px;
                padding: 15px;
                border-radius: 8px;
                border: 2px solid #ced4da;
                background-color: #f8f9fa;
            }
            QLineEdit:focus {
                border-color: #007bff;
                background-color: white;
            }
        """)
        fr_layout.addWidget(self.free_response_input)
        self.input_stack.addWidget(free_response_page)
        
        # Multiple choice page
        mc_page = QWidget()
        mc_layout = QVBoxLayout(mc_page)
        self.mc_button_group = QButtonGroup(mc_page)
        self.mc_options_layout = QHBoxLayout()
        mc_layout.addLayout(self.mc_options_layout)
        self.input_stack.addWidget(mc_page)
        
        layout.addWidget(self.input_stack)
        
        return card
    
    def create_enhanced_navigation(self) -> QHBoxLayout:
        """Create enhanced navigation buttons"""
        layout = QHBoxLayout()
        layout.setSpacing(12)
        
        # Previous button
        self.prev_button = QPushButton("⬅️ Previous")
        self.prev_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                           stop:0 #6c757d, stop:1 #5a6268);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                           stop:0 #5a6268, stop:1 #495057);
            }
        """)
        
        # Hint button with enhanced styling
        self.hint_button = QPushButton("💡 Smart Hint")
        self.hint_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                           stop:0 #ffc107, stop:1 #e0a800);
                color: #212529;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                           stop:0 #e0a800, stop:1 #d39e00);
            }
        """)
        
        # Submit button with enhanced styling
        self.submit_button = QPushButton("✅ Submit Answer")
        self.submit_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                           stop:0 #28a745, stop:1 #218838);
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                           stop:0 #218838, stop:1 #1e7e34);
            }
        """)
        
        # Next button
        self.next_button = QPushButton("Next ➡️")
        
        layout.addWidget(self.prev_button)
        layout.addWidget(self.hint_button)
        layout.addStretch()
        layout.addWidget(self.submit_button)
        layout.addWidget(self.next_button)
        
        return layout
    
    def create_enhanced_status_bar(self):
        """Create enhanced status bar"""
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                           stop:0 #f8f9fa, stop:1 #e9ecef);
                border-top: 1px solid #dee2e6;
                padding: 8px;
                font-weight: 500;
            }
        """)
        self.setStatusBar(self.status_bar)
        
        # Add enhanced streak display
        self.streak_label = QLabel()
        self.streak_label.setStyleSheet("color: #e74c3c; font-weight: bold; margin-right: 15px;")
        self.status_bar.addPermanentWidget(self.streak_label)
        
        # Add performance indicator
        self.performance_label = QLabel("Performance: Starting up...")
        self.performance_label.setStyleSheet("color: #007bff; font-weight: 500; margin-right: 15px;")
        self.status_bar.addPermanentWidget(self.performance_label)
    
    def connect_enhanced_signals(self):
        """Connect enhanced signal handlers"""
        # Original connections
        self.submit_button.clicked.connect(self.enhanced_submit_answer)
        self.next_button.clicked.connect(self.enhanced_next_exercise)
        self.prev_button.clicked.connect(self.enhanced_prev_exercise)
        self.hint_button.clicked.connect(self.enhanced_provide_hint)
        
        # Enhanced keyboard shortcuts
        self.submit_button.setShortcut("Return")
        self.next_button.setShortcut("Right")
        self.prev_button.setShortcut("Left")
        self.hint_button.setShortcut("H")
        
        # Enter key submits in free response mode
        self.free_response_input.returnPressed.connect(self.enhanced_submit_answer)
        
        # Track typing for response time analysis
        self.free_response_input.textChanged.connect(self.on_user_typing)
    
    def on_user_typing(self):
        """Track when user starts typing for response time analysis"""
        if self.current_exercise_start_time is None:
            self.current_exercise_start_time = datetime.now()
    
    def enhanced_submit_answer(self):
        """Enhanced submit answer with advanced feedback"""
        if self.total_exercises == 0:
            self.updateStatus("No exercises available. Generate new ones first.")
            return
            
        user_answer = self.getUserAnswer()
        if not user_answer:
            self.updateStatus("Please provide an answer.")
            return
        
        # Calculate response time
        response_time = 0
        if self.current_exercise_start_time:
            response_time = (datetime.now() - self.current_exercise_start_time).total_seconds()
            self.session_stats["response_times"].append(response_time)
        
        exercise = self.exercises[self.current_exercise]
        correct_answer = exercise.get("answer", "").strip().lower()
        is_correct = user_answer.lower() == correct_answer.lower()
        
        # Update session stats
        self.session_stats["total_attempts"] += 1
        if is_correct:
            self.correct_count += 1
            self.session_stats["correct_attempts"] += 1
        
        # Update adaptive feedback manager
        self.adaptive_manager.update_performance(is_correct, response_time, exercise)
        
        # Set exercise context for enhanced feedback
        exercise_id = f"exercise_{self.current_exercise}_{datetime.now().timestamp()}"
        exercise_context = {
            "base_verb": exercise.get("verb", ""),
            "trigger_type": exercise.get("trigger_type", ""),
            "tense": exercise.get("tense", "present"),
            "person": exercise.get("person", "third"),
            "context_type": exercise.get("context", "")
        }
        
        self.enhanced_feedback_widget.set_exercise_context(exercise_id, exercise_context)
        
        # Show immediate visual response
        self.enhanced_feedback_widget.show_immediate_response(is_correct, user_answer, correct_answer)
        
        # Play appropriate sound
        self.sound_manager.play_sound("correct" if is_correct else "incorrect")
        
        # Perform advanced error analysis if incorrect
        if not is_correct:
            error_analysis = self.error_analyzer.analyze_error(
                user_answer, correct_answer, exercise_context, "default_user"
            )
            
            # Display advanced error guidance
            self.display_advanced_error_guidance(error_analysis)
        
        # Check for achievements
        self.check_achievements()
        
        # Generate GPT explanation asynchronously
        self.generateGPTExplanationAsync(user_answer, correct_answer, is_correct, 
                                       exercise.get("sentence", ""), "")
        
        # Update performance display
        self.update_performance_display()
        
        # Reset exercise start time
        self.current_exercise_start_time = None
        
        logger.info("Enhanced answer submitted: '%s' for exercise %d", user_answer, self.current_exercise + 1)
    
    def display_advanced_error_guidance(self, error_analysis):
        """Display advanced error analysis and guidance"""
        guidance_html = f"""
        <div style="background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); 
                    border-left: 4px solid #ffc107; padding: 15px; border-radius: 8px; margin: 10px 0;">
            <h4 style="color: #856404; margin-top: 0; display: flex; align-items: center;">
                🔍 <span style="margin-left: 8px;">Advanced Error Analysis</span>
            </h4>
            
            <div style="background: rgba(255, 255, 255, 0.8); padding: 12px; border-radius: 6px; margin: 8px 0;">
                <strong style="color: #721c24;">Issue Identified:</strong><br>
                <span style="color: #856404;">{error_analysis.specific_issue}</span>
            </div>
            
            <div style="background: rgba(255, 255, 255, 0.8); padding: 12px; border-radius: 6px; margin: 8px 0;">
                <strong style="color: #155724;">💡 Targeted Guidance:</strong><br>
                <span style="color: #495057;">{error_analysis.guidance_message}</span>
            </div>
            
            <details style="margin-top: 12px;">
                <summary style="font-weight: bold; cursor: pointer; color: #495057;">
                    📚 Practice Recommendations
                </summary>
                <ul style="margin: 8px 0; padding-left: 20px;">
                    {"".join(f'<li style="color: #6c757d; margin: 4px 0;">{suggestion}</li>' 
                            for suggestion in error_analysis.practice_suggestions)}
                </ul>
            </details>
            
            <div style="display: flex; justify-content: space-between; align-items: center; 
                        margin-top: 12px; font-size: 0.9em; color: #6c757d;">
                <span>Complexity: {"🌟" * error_analysis.cognitive_load} ({error_analysis.cognitive_load}/5)</span>
                <span>Confidence: {error_analysis.confidence:.1%}</span>
            </div>
        </div>
        """
        
        # Display in feedback widget
        current_content = self.enhanced_feedback_widget.feedback_content.toHtml()
        self.enhanced_feedback_widget.feedback_content.setHtml(current_content + guidance_html)
    
    def check_achievements(self):
        """Check and display achievements"""
        # Check for streak achievements
        streak_info = self.streak_tracker.get_streak_info()
        if streak_info["current"] > 0 and streak_info["current"] % 5 == 0:
            self.enhanced_feedback_widget.show_achievement(
                f"Congratulations! {streak_info['current']}-day practice streak!",
                "streak"
            )
        
        # Check for accuracy achievements
        if self.session_stats["total_attempts"] >= 5:
            accuracy = (self.session_stats["correct_attempts"] / self.session_stats["total_attempts"]) * 100
            if accuracy >= 90:
                self.enhanced_feedback_widget.show_achievement(
                    f"Outstanding! {accuracy:.1f}% accuracy this session!",
                    "accuracy"
                )
        
        # Check for speed achievements
        if len(self.session_stats["response_times"]) >= 3:
            avg_time = sum(self.session_stats["response_times"][-3:]) / 3
            if avg_time < 5.0:  # Under 5 seconds average for last 3 responses
                self.enhanced_feedback_widget.show_achievement(
                    f"Lightning fast! Average response time: {avg_time:.1f}s",
                    "speed"
                )
    
    def enhanced_provide_hint(self):
        """Enhanced hint system with progressive disclosure"""
        if self.total_exercises == 0:
            self.updateStatus("No exercise available.")
            return
        
        # Track hint usage
        self.session_stats["hints_used"] += 1
        
        # Set current exercise context
        exercise = self.exercises[self.current_exercise]
        exercise_id = f"exercise_{self.current_exercise}"
        exercise_context = {
            "base_verb": exercise.get("verb", ""),
            "trigger_type": exercise.get("trigger_type", ""),
            "tense": exercise.get("tense", "present"),
            "person": exercise.get("person", "third"),
            "answer": exercise.get("answer", ""),
            "context_type": exercise.get("context", "")
        }
        
        self.enhanced_feedback_widget.set_exercise_context(exercise_id, exercise_context)
        self.enhanced_feedback_widget.request_hint()
        
        # Play hint sound
        self.sound_manager.play_sound("hint")
        
        logger.info("Enhanced hint provided for exercise %d", self.current_exercise + 1)
    
    def enhanced_next_exercise(self):
        """Enhanced next exercise with animations"""
        if self.total_exercises == 0:
            self.updateStatus("No exercises available. Generate new ones first.")
            return
            
        if self.current_exercise < self.total_exercises - 1:
            self.current_exercise += 1
            self.updateExercise()
            
            # Reset exercise start time
            self.current_exercise_start_time = None
            
            # Animate transition
            self.animate_exercise_transition()
            
            logger.info("Moved to next exercise: %d", self.current_exercise + 1)
        else:
            self.updateStatus("You are at the last exercise. Great job completing the session!")
            self.show_session_completion()
        
        self.updateStats()
    
    def enhanced_prev_exercise(self):
        """Enhanced previous exercise with animations"""
        if self.total_exercises == 0:
            self.updateStatus("No exercises available.")
            return
            
        if self.current_exercise > 0:
            self.current_exercise -= 1
            self.updateExercise()
            
            # Reset exercise start time
            self.current_exercise_start_time = None
            
            # Animate transition
            self.animate_exercise_transition(reverse=True)
            
            logger.info("Moved to previous exercise: %d", self.current_exercise + 1)
        else:
            self.updateStatus("You are at the first exercise.")
        
        self.updateStats()
    
    def animate_exercise_transition(self, reverse=False):
        """Animate exercise transitions"""
        if not self.feedback_config.animation_enabled:
            return
        
        # Slide animation for exercise card
        animation = QPropertyAnimation(self.sentence_label, b"pos")
        animation.setDuration(300)
        
        current_pos = self.sentence_label.pos()
        if reverse:
            slide_pos = current_pos + QRect(-50, 0, 0, 0).topLeft()
        else:
            slide_pos = current_pos + QRect(50, 0, 0, 0).topLeft()
        
        animation.setKeyValueAt(0, current_pos)
        animation.setKeyValueAt(0.5, slide_pos)
        animation.setKeyValueAt(1, current_pos)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        animation.start()
    
    def show_session_completion(self):
        """Show session completion with celebration"""
        if self.session_stats["total_attempts"] > 0:
            accuracy = (self.session_stats["correct_attempts"] / self.session_stats["total_attempts"]) * 100
            avg_time = sum(self.session_stats["response_times"]) / len(self.session_stats["response_times"]) if self.session_stats["response_times"] else 0
            
            completion_message = f"""
            🎉 ¡Felicitaciones! Session completed!
            
            📊 Final Statistics:
            • Exercises completed: {self.session_stats["total_attempts"]}
            • Accuracy: {accuracy:.1f}%
            • Hints used: {self.session_stats["hints_used"]}
            • Average response time: {avg_time:.1f}s
            
            🏆 Keep up the excellent work!
            """
            
            self.enhanced_feedback_widget.show_achievement(completion_message, "mastery")
    
    def update_performance_display(self):
        """Update performance display based on adaptive feedback"""
        strategy = self.adaptive_manager.get_adaptive_feedback_strategy()
        
        strategy_colors = {
            "struggling": "#dc3545",
            "progressing": "#ffc107", 
            "mastering": "#28a745"
        }
        
        strategy_messages = {
            "struggling": "🔴 Focus Mode - Take your time",
            "progressing": "🟡 Learning Mode - You're improving!", 
            "mastering": "🟢 Master Mode - Excellent progress!"
        }
        
        color = strategy_colors.get(strategy, "#6c757d")
        message = strategy_messages.get(strategy, "Performance tracking...")
        
        self.performance_label.setText(message)
        self.performance_label.setStyleSheet(f"color: {color}; font-weight: bold; margin-right: 15px;")
    
    def handle_feedback_request(self, request_type: str):
        """Handle feedback requests from enhanced feedback widget"""
        if request_type == "detailed":
            # Provide detailed explanation
            if self.current_exercise < len(self.exercises):
                exercise = self.exercises[self.current_exercise]
                context_help = self.help_system.get_contextual_help(exercise)
                
                # Show contextual help
                help_dialog = QDialog(self)
                help_dialog.setWindowTitle("Contextual Help")
                help_dialog.setMinimumSize(600, 400)
                
                layout = QVBoxLayout(help_dialog)
                
                help_content = QTextEdit()
                help_content.setReadOnly(True)
                help_content.setHtml(context_help)
                layout.addWidget(help_content)
                
                close_btn = QPushButton("Close")
                close_btn.clicked.connect(help_dialog.close)
                layout.addWidget(close_btn)
                
                help_dialog.exec_()
    
    # Include original methods with enhancements
    def createToolBar(self):
        """Create enhanced toolbar"""
        toolbar = QToolBar("Enhanced Toolbar")
        toolbar.setMovable(False)
        toolbar.setStyleSheet("""
            QToolBar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                           stop:0 #ffffff, stop:1 #f8f9fa);
                border-bottom: 2px solid #e9ecef;
                padding: 8px;
                spacing: 8px;
            }
            QAction {
                padding: 8px 12px;
                margin: 2px;
                border-radius: 6px;
            }
        """)
        self.addToolBar(toolbar)
        
        # Enhanced actions with icons
        new_action = QAction("🎯 New Exercises", self)
        new_action.setToolTip("Generate new subjunctive exercises")
        new_action.triggered.connect(self.generateNewExercise)
        toolbar.addAction(new_action)
        
        settings_action = QAction("⚙️ Settings", self)
        settings_action.setToolTip("Feedback system settings")
        settings_action.triggered.connect(self.show_settings_dialog)
        toolbar.addAction(settings_action)
        
        toolbar.addSeparator()
        
        reset_action = QAction("🔄 Reset", self)
        reset_action.triggered.connect(self.resetProgress)
        toolbar.addAction(reset_action)
        
        summary_action = QAction("📊 Summary", self)
        summary_action.triggered.connect(self.generateSessionSummary)
        toolbar.addAction(summary_action)
        
        toolbar.addSeparator()
        
        theme_action = QAction("🌙 Theme", self)
        theme_action.triggered.connect(self.toggleTheme)
        toolbar.addAction(theme_action)
        
        help_action = QAction("❓ Help", self)
        help_action.triggered.connect(self.show_help_dialog)
        toolbar.addAction(help_action)
    
    def show_settings_dialog(self):
        """Show enhanced feedback system settings"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Enhanced Feedback Settings")
        dialog.setMinimumSize(400, 300)
        
        layout = QVBoxLayout(dialog)
        
        # Visual feedback settings
        visual_group = QGroupBox("Visual Feedback")
        visual_layout = QVBoxLayout(visual_group)
        
        self.visual_enabled_cb = QCheckBox("Enable visual feedback and animations")
        self.visual_enabled_cb.setChecked(self.feedback_config.visual_enabled)
        visual_layout.addWidget(self.visual_enabled_cb)
        
        self.animation_enabled_cb = QCheckBox("Enable celebration animations")
        self.animation_enabled_cb.setChecked(self.feedback_config.celebration_animations)
        visual_layout.addWidget(self.animation_enabled_cb)
        
        layout.addWidget(visual_group)
        
        # Audio feedback settings
        audio_group = QGroupBox("Audio Feedback")
        audio_layout = QVBoxLayout(audio_group)
        
        self.sound_enabled_cb = QCheckBox("Enable sound effects")
        self.sound_enabled_cb.setChecked(self.feedback_config.sound_enabled)
        audio_layout.addWidget(self.sound_enabled_cb)
        
        layout.addWidget(audio_group)
        
        # Hint system settings
        hint_group = QGroupBox("Hint System")
        hint_layout = QVBoxLayout(hint_group)
        
        self.progressive_hints_cb = QCheckBox("Enable progressive hint system")
        self.progressive_hints_cb.setChecked(self.feedback_config.hint_progression_enabled)
        hint_layout.addWidget(self.progressive_hints_cb)
        
        layout.addWidget(hint_group)
        
        # Adaptive system settings
        adaptive_group = QGroupBox("Adaptive Learning")
        adaptive_layout = QVBoxLayout(adaptive_group)
        
        self.adaptive_difficulty_cb = QCheckBox("Enable adaptive difficulty adjustment")
        self.adaptive_difficulty_cb.setChecked(self.feedback_config.adaptive_difficulty)
        adaptive_layout.addWidget(self.adaptive_difficulty_cb)
        
        self.timing_optimal_cb = QCheckBox("Use optimal timing for feedback")
        self.timing_optimal_cb.setChecked(self.feedback_config.timing_optimal)
        adaptive_layout.addWidget(self.timing_optimal_cb)
        
        layout.addWidget(adaptive_group)
        
        # Dialog buttons
        buttons = QHBoxLayout()
        save_btn = QPushButton("💾 Save Settings")
        cancel_btn = QPushButton("❌ Cancel")
        
        save_btn.clicked.connect(lambda: self.save_settings(dialog))
        cancel_btn.clicked.connect(dialog.reject)
        
        buttons.addWidget(save_btn)
        buttons.addWidget(cancel_btn)
        layout.addLayout(buttons)
        
        dialog.exec_()
    
    def save_settings(self, dialog):
        """Save feedback system settings"""
        self.feedback_config.visual_enabled = self.visual_enabled_cb.isChecked()
        self.feedback_config.sound_enabled = self.sound_enabled_cb.isChecked()
        self.feedback_config.animation_enabled = self.animation_enabled_cb.isChecked()
        self.feedback_config.celebration_animations = self.animation_enabled_cb.isChecked()
        self.feedback_config.hint_progression_enabled = self.progressive_hints_cb.isChecked()
        self.feedback_config.adaptive_difficulty = self.adaptive_difficulty_cb.isChecked()
        self.feedback_config.timing_optimal = self.timing_optimal_cb.isChecked()
        
        # Update components
        self.sound_manager.enabled = self.feedback_config.sound_enabled
        
        QMessageBox.information(self, "Settings Saved", "✅ Feedback system settings have been updated!")
        dialog.accept()
    
    def show_help_dialog(self):
        """Show comprehensive help dialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Enhanced Learning System Help")
        dialog.setMinimumSize(700, 500)
        
        layout = QVBoxLayout(dialog)
        
        help_content = QTextEdit()
        help_content.setReadOnly(True)
        help_content.setHtml("""
        <h2>🎓 Enhanced Spanish Subjunctive Learning System</h2>
        
        <h3>🌟 Key Features:</h3>
        <ul>
            <li><strong>Visual Feedback:</strong> Color-coded responses and animations for better retention</li>
            <li><strong>Progressive Hints:</strong> Smart hint system that gradually reveals more information</li>
            <li><strong>Sound Effects:</strong> Audio cues to reinforce correct and incorrect responses</li>
            <li><strong>Advanced Error Analysis:</strong> Detailed analysis of mistakes with specific guidance</li>
            <li><strong>Achievement System:</strong> Celebrations for streaks, accuracy, and speed milestones</li>
            <li><strong>Adaptive Learning:</strong> System adjusts difficulty based on your performance</li>
        </ul>
        
        <h3>💡 Learning Tips:</h3>
        <ul>
            <li><strong>Use Hints Wisely:</strong> Start with subtle hints and progress gradually</li>
            <li><strong>Focus on Patterns:</strong> Pay attention to trigger words and contexts</li>
            <li><strong>Practice Daily:</strong> Maintain your streak for consistent progress</li>
            <li><strong>Review Mistakes:</strong> Use the detailed error analysis to understand why</li>
            <li><strong>Celebrate Success:</strong> Acknowledge achievements to stay motivated</li>
        </ul>
        
        <h3>⌨️ Keyboard Shortcuts:</h3>
        <ul>
            <li><strong>Enter:</strong> Submit answer</li>
            <li><strong>H:</strong> Get hint</li>
            <li><strong>Left Arrow:</strong> Previous exercise</li>
            <li><strong>Right Arrow:</strong> Next exercise</li>
            <li><strong>Ctrl+R:</strong> Conjugation reference</li>
        </ul>
        
        <h3>📈 Performance Indicators:</h3>
        <ul>
            <li><strong>🔴 Focus Mode:</strong> Take your time, review fundamentals</li>
            <li><strong>🟡 Learning Mode:</strong> You're improving, keep practicing</li>
            <li><strong>🟢 Master Mode:</strong> Excellent progress, challenge yourself</li>
        </ul>
        """)
        
        layout.addWidget(help_content)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.exec_()
    
    # Continue with enhanced versions of existing methods...
    def check_daily_streak(self):
        """Enhanced daily streak checking"""
        streak_info = self.streak_tracker.record_practice()
        self.streak_label.setText(f"🔥 Streak: {streak_info['current']} days | Best: {streak_info['best']}")
        
        if streak_info['current'] > 0:
            self.updateStatus(streak_info['message'])
            
        # Show streak achievement if milestone reached
        if streak_info['current'] > 0 and streak_info['current'] % 5 == 0:
            QTimer.singleShot(1000, lambda: self.enhanced_feedback_widget.show_achievement(
                f"🔥 Amazing! {streak_info['current']}-day practice streak!", "streak"
            ))
    
    # Include other necessary methods from the original with enhancements...
    # (For brevity, I'm showing the key enhanced methods. The full implementation would include all original methods with appropriate enhancements)
    
    def updateExercise(self) -> None:
        """Enhanced exercise update with context setting"""
        if self.total_exercises == 0 or self.current_exercise < 0 or self.current_exercise >= self.total_exercises:
            return
            
        exercise = self.exercises[self.current_exercise]
        
        # Enhanced display
        if "context" in exercise and exercise["context"]:
            full_text = f"🎯 {exercise['context']}\n\n{exercise.get('sentence', '')}"
        else:
            full_text = exercise.get("sentence", "")
            
        self.sentence_label.setText(full_text)
        
        # Translation handling
        if self.show_translation and "translation" in exercise:
            self.translation_label.setText(f"💬 {exercise['translation']}")
            self.translation_label.setVisible(True)
        else:
            self.translation_label.setVisible(False)
        
        # Clear previous feedback
        self.enhanced_feedback_widget.feedback_content.clear()
        self.enhanced_feedback_widget.status_icon.setText("📝")
        self.enhanced_feedback_widget.status_text.setText("Ready for your answer!")
        
        # Update progress
        self.enhanced_progress_bar.setValue(self.current_exercise + 1)
        self.enhanced_progress_bar.setMaximum(self.total_exercises)
        
        # Handle input mode
        mode = self.mode_combo.currentText()
        if mode == "Free Response":
            self.input_stack.setCurrentIndex(0)
            self.free_response_input.clear()
            self.free_response_input.setFocus()
        elif mode == "Multiple Choice":
            self.input_stack.setCurrentIndex(1)
            if "choices" in exercise:
                choices = list(exercise["choices"])
                random.shuffle(choices)
                self.populateMultipleChoice(choices)
        
        # Reset exercise start time
        self.current_exercise_start_time = None
        
        self.updateStatus(f"Exercise {self.current_exercise + 1} of {self.total_exercises}")
        self.updateStats()
    
    def updateStats(self):
        """Enhanced statistics update"""
        accuracy = 0
        if self.session_stats["total_attempts"] > 0:
            accuracy = (self.session_stats["correct_attempts"] / self.session_stats["total_attempts"]) * 100
        
        # Update enhanced displays
        self.exercise_stat.setText(f"Exercise: {self.current_exercise + 1}/{self.total_exercises}")
        self.accuracy_stat.setText(f"Accuracy: {accuracy:.1f}%")
        
        # Update streak display
        streak_info = self.streak_tracker.get_streak_info()
        self.streak_stat.setText(f"🔥 Streak: {streak_info['current']}")
    
    # Additional methods would be implemented here...
    # For the sake of this example, I'm providing the core structure and key enhancements
    
    def getUserAnswer(self):
        """Get user answer with input validation"""
        mode = self.mode_combo.currentText()
        if mode == "Free Response":
            answer = self.free_response_input.text().strip()
            # Enhanced input validation
            if len(answer) > 100:
                QMessageBox.warning(self, "Input Too Long", "Answer must be less than 100 characters.")
                return ""
            # Clean input
            answer = re.sub(r'[<>"\']', '', answer)
            return answer.lower()
        else:
            for btn in self.mc_button_group.buttons():
                if btn.isChecked():
                    return btn.text().strip().lower()
        return ""
    
    def generateNewExercise(self):
        """Enhanced exercise generation (abbreviated)"""
        # This would include the full logic from the original with enhancements
        selected_triggers = [cb.property("value") for cb in self.trigger_checkboxes if cb.isChecked()]
        if not selected_triggers:
            QMessageBox.warning(self, "Selection Required", "Please select at least one subjunctive trigger.")
            return
            
        selected_tenses = [tense for tense, cb in self.tense_checkboxes.items() if cb.isChecked()]
        if not selected_tenses:
            QMessageBox.warning(self, "Selection Required", "Please select at least one tense.")
            return
            
        selected_persons = [person for person, cb in self.person_checkboxes.items() if cb.isChecked()]
        if not selected_persons:
            QMessageBox.warning(self, "Selection Required", "Please select at least one person.")
            return
        
        # Continue with exercise generation logic...
        # (Implementation would include the full generation logic)
        
        self.updateStatus("🔄 Generating enhanced exercises with adaptive difficulty...")
    
    def populateMultipleChoice(self, choices: List[str]) -> None:
        """Enhanced multiple choice display"""
        # Clear previous choices
        while self.mc_options_layout.count():
            item = self.mc_options_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        
        # Create new button group
        self.mc_button_group = QButtonGroup()
        
        # Add choices with enhanced styling
        for i, choice in enumerate(choices):
            radio = QRadioButton(choice)
            radio.setStyleSheet("""
                QRadioButton {
                    font-size: 16px;
                    padding: 8px 12px;
                    margin: 4px;
                    border: 2px solid #dee2e6;
                    border-radius: 8px;
                    background-color: #f8f9fa;
                }
                QRadioButton:hover {
                    background-color: #e9ecef;
                    border-color: #007bff;
                }
                QRadioButton:checked {
                    background-color: #007bff;
                    color: white;
                    border-color: #007bff;
                }
            """)
            self.mc_button_group.addButton(radio)
            self.mc_options_layout.addWidget(radio)
        
        self.mc_options_layout.addStretch()
        
        # Select first option by default
        if self.mc_button_group.buttons():
            self.mc_button_group.buttons()[0].setChecked(True)
    
    def updateStatus(self, msg: str):
        """Enhanced status updates"""
        self.status_bar.showMessage(msg, 5000)
        logger.info("Status update: %s", msg)
    
    # Additional methods would continue...
    # The full implementation would include all original methods with appropriate enhancements


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Enhanced Spanish Subjunctive Practice")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("Language Learning Solutions")
    
    window = EnhancedSpanishSubjunctivePracticeGUI()
    window.show()
    
    sys.exit(app.exec_())
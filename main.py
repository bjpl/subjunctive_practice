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

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QLabel, QLineEdit, QPushButton, QProgressBar, QTextEdit, QStackedWidget,
    QRadioButton, QButtonGroup, QStatusBar, QAction, QGroupBox, QCheckBox,
    QMessageBox, QToolBar, QScrollArea, QComboBox, QSizePolicy, QDialog,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QRunnable, QObject, pyqtSignal, QThreadPool, QTimer

# Import visual design system - COMMENTED OUT FOR ROLLBACK
# try:
#     from src.ui_visual import initialize_modern_ui, apply_widget_specific_styles, VisualTheme
# except ImportError:
#     print("Visual design module not available. Using basic styling.")
initialize_modern_ui = None
apply_widget_specific_styles = None
VisualTheme = None

# Import spacing optimizer - COMMENTED OUT FOR ROLLBACK
# try:
#     from src.spacing_optimizer import SpacingOptimizer, apply_spacing_to_spanish_app
# except ImportError:
#     print("Spacing optimizer not available. Using basic spacing.")
SpacingOptimizer = None
apply_spacing_to_spanish_app = None

# Import accessibility features - SIMPLIFIED FOR ROLLBACK
# try:
#     from src.accessibility_integration import integrate_accessibility, add_accessibility_startup_check
# except ImportError:
#     print("Accessibility features not available. Running in basic mode.")
integrate_accessibility = None
add_accessibility_startup_check = None

# Import enhanced typography and sizing fixes - COMMENTED OUT FOR ROLLBACK
# try:
#     from src.typography_size_fixes import apply_typography_size_fixes, get_accessibility_report
# except ImportError:
#     print("Typography size fixes not available. Using basic typography.")
apply_typography_size_fixes = None
get_accessibility_report = None

# Import form styling fixes - COMMENTED OUT FOR ROLLBACK
# try:
#     from src.form_integration import integrate_form_fixes, FormIntegrationManager
# except ImportError:
#     print("Form styling fixes not available. Using basic form styling.")
integrate_form_fixes = None
FormIntegrationManager = None

# Import the new API configuration module
try:
    from src.api_configuration_fix import (
        get_api_manager, 
        create_chat_completion,
        is_api_available,
        get_health_status,
        APIError
    )
    API_MODULE_AVAILABLE = True
except ImportError:
    print("API configuration module not available. Using basic OpenAI integration.")
    from openai import OpenAI
    API_MODULE_AVAILABLE = False

# Import progress indicators
try:
    from src.progress_indicators import (
        ProgressOverlay, LoadingButton, ProgressManager, 
        create_api_loading_message, create_error_message
    )
    PROGRESS_INDICATORS_AVAILABLE = True
except ImportError:
    print("Progress indicators module not available. Using basic status updates.")
    PROGRESS_INDICATORS_AVAILABLE = False

# Import text truncation fixes
try:
    from src.text_truncation_fixes import TextTruncationFixer, fix_text_truncation_issues
    TEXT_TRUNCATION_FIXES_AVAILABLE = True
except ImportError:
    print("Text truncation fixes not available. Text may be truncated in UI.")
    TEXT_TRUNCATION_FIXES_AVAILABLE = False

# Import checkbox rendering fixes
try:
    from src.checkbox_rendering_fixes import (
        CheckboxRenderingFixer, fix_checkbox_rendering_issues, 
        remove_red_borders_from_forms
    )
    CHECKBOX_RENDERING_FIXES_AVAILABLE = True
except ImportError:
    print("Checkbox rendering fixes not available. Checkboxes may not render properly.")
    CHECKBOX_RENDERING_FIXES_AVAILABLE = False

# Import complete responsive design integration - COMMENTED OUT FOR ROLLBACK
# try:
#     from src.complete_responsive_integration import quick_responsive_integration
#     RESPONSIVE_DESIGN_AVAILABLE = True
# except ImportError:
#     print("Responsive design module not available. Using basic layout.")
quick_responsive_integration = None
RESPONSIVE_DESIGN_AVAILABLE = False

# Load environment variables (ensure your OPENAI_API_KEY is set correctly)
load_dotenv()

# Configure Logging: logs will go to both file and console.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler = logging.FileHandler("subjunctive_practice.log", mode="a", encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Initialize API manager or fallback to basic client
if API_MODULE_AVAILABLE:
    # Use the new robust API manager
    api_manager = get_api_manager()
    client = api_manager.get_client()
    logger.info("Using enhanced API configuration with rate limiting and error handling")
    
    # Log initial health status
    health_status = get_health_status()
    logger.info(f"API Health Status: {health_status['overall_health']} - Available: {health_status['available']}")
else:
    # Fallback to basic implementation
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

    # Initialize OpenAI client securely
    try:
        if validate_api_key():
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        else:
            client = None
    except Exception as e:
        logger.error("Failed to initialize OpenAI client: %s", str(e))
        client = None

# ---------------- Worker Classes for Asynchronous GPT Calls ----------------
class WorkerSignals(QObject):
    """Signals for worker threads."""
    result = pyqtSignal(str)

class GPTWorkerRunnable(QRunnable):
    """
    Worker thread for calling GPT asynchronously using OpenAI's ChatCompletion interface.
    """
    def __init__(self, prompt: str, model: str = "gpt-4", max_tokens: int = 600, temperature: float = 0.5):
        super().__init__()
        self.prompt = prompt
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.signals = WorkerSignals()

    def run(self) -> None:
        try:
            if API_MODULE_AVAILABLE:
                # Use the enhanced API manager
                output = self._run_with_api_manager()
            else:
                # Fallback to basic implementation
                output = self._run_with_basic_client()
                
        except Exception as e:
            output = f"Unexpected error: {str(e)}"
            logging.error("Unexpected error in GPTWorkerRunnable: %s", str(e))
        
        self.signals.result.emit(output)
    
    def _run_with_api_manager(self) -> str:
        """Run request using the enhanced API manager"""
        try:
            if not is_api_available():
                return "API service is currently unavailable. Using fallback content."
            
            messages = [
                {
                    "role": "system",
                    "content": ("You are an expert Spanish tutor specializing in LATAM Spanish. "
                                "Your guidance should always reflect real-life conversational tone, "
                                "using authentic expressions and culturally relevant details.")
                },
                {"role": "user", "content": self.prompt}
            ]
            
            # Use the enhanced create_chat_completion function with built-in retry logic
            output = create_chat_completion(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                timeout=30
            )
            
            if output:
                logging.info("GPT response received via enhanced API manager")
                return output
            else:
                return "Error: No response received from API"
                
        except APIError as e:
            error_messages = {
                "authentication": "Authentication failed. Please check your API key in the .env file.",
                "rate_limit": f"Rate limit exceeded. Please wait {getattr(e, 'retry_after', 60)} seconds and try again.",
                "circuit_breaker": "API temporarily unavailable due to repeated failures. Please wait a few minutes.",
                "max_retries_exceeded": "API request failed after multiple attempts. Check your connection.",
                "not_initialized": "API not properly initialized. Please check your configuration.",
                "timeout": "Request timed out. The API may be experiencing high load. Please try again.",
                "network_error": "Network connection error. Please check your internet connection."
            }
            logging.error(f"APIError in enhanced call: {e.error_type} - {str(e)}")
            return error_messages.get(e.error_type, f"API Error: {str(e)}")
            
        except Exception as e:
            logging.error("Error in enhanced API call: %s", str(e))
            return f"Error: {str(e)}"
    
    def _run_with_basic_client(self) -> str:
        """Run request using basic OpenAI client (fallback)"""
        if not client:
            return "Error: OpenAI client not initialized. Please check your API key."
            
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
            logging.info("GPT response received via basic client.")
            return output
            
        except Exception as e:
            # Import openai here to avoid module reference issues
            try:
                import openai
                if isinstance(e, openai.APIConnectionError):
                    output = "Connection error. Please check your internet connection."
                    logging.error("API connection error: %s", str(e))
                elif isinstance(e, openai.AuthenticationError):
                    output = "Authentication failed. Please check your API key."
                    logging.error("Authentication error: %s", str(e))
                elif isinstance(e, openai.RateLimitError):
                    output = "Rate limit exceeded. Please wait a moment and try again."
                    logging.error("Rate limit error: %s", str(e))
                elif isinstance(e, openai.BadRequestError):
                    output = "Invalid request. Please check your input and try again."
                    logging.error("Bad request error: %s", str(e))
                elif hasattr(openai, 'InternalServerError') and isinstance(e, openai.InternalServerError):
                    output = "OpenAI service is temporarily unavailable. Please try again in a few minutes."
                    logging.error("Internal server error: %s", str(e))
                elif hasattr(openai, 'ServiceUnavailableError') and isinstance(e, openai.ServiceUnavailableError):
                    output = "OpenAI service is currently overloaded. Please wait and try again."
                    logging.error("Service unavailable error: %s", str(e))
                else:
                    output = f"Service temporarily unavailable: {str(e)}"
                    logging.error("Unexpected error in basic client: %s", str(e))
                return output
            except ImportError:
                return "Error: OpenAI library not available. Please install with: pip install openai"


# ---------------- Main GUI ----------------
class SpanishSubjunctivePracticeGUI(QMainWindow):
    """
    A specialized GUI for practicing all Spanish subjunctive forms and triggers.
    Selections for triggers, tenses, and persons are required (no defaults are set).
    """
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Spanish Subjunctive Practice")
        self.setGeometry(100, 100, 1200, 800)  # Increased dimensions for three-column layout
        self.setMinimumSize(1000, 600)  # Set minimum window size to ensure usability

        # Initialize style manager for theme control
        self.style_manager = None
        
        # Initialize spacing optimizer
        self.spacing_optimizer = None

        # Data structures for session management
        self.exercises: List[dict] = []
        self.current_exercise: int = 0
        self.total_exercises: int = 0
        self.correct_count: int = 0
        self.responses: List[dict] = []  # Session details
        self.session_stats: Dict = {
            "total_attempts": 0,
            "correct_attempts": 0,
            "hints_used": 0,
            "session_start": datetime.now(),
            "tenses_practiced": set(),
            "persons_practiced": set()
        }

        # Settings
        self.dark_mode = False
        self.show_translation = False
        self.threadpool = QThreadPool()
        
        # Progress management
        if PROGRESS_INDICATORS_AVAILABLE:
            self.progress_manager = ProgressManager(self)
            self.progress_overlay = None  # Will be initialized in initUI
        else:
            self.progress_manager = None
            self.progress_overlay = None
        
        # Loading states tracking
        self.loading_states = {
            'generating_exercises': False,
            'checking_answer': False,
            'getting_hint': False,
            'generating_summary': False,
            'testing_api': False
        }
        
        # TBLT and pedagogical components
        self.tblt_generator = TBLTTaskGenerator()
        self.spaced_repetition = SpacedRepetitionTracker()
        self.current_task_type = "traditional"  # Can be 'traditional' or 'tblt'
        
        # Session management
        self.session_manager = SessionManager()
        self.review_queue = ReviewQueue()
        self.review_mode = False
        
        # Learning analytics
        self.streak_tracker = StreakTracker()
        self.error_analyzer = ErrorAnalyzer()
        self.adaptive_difficulty = AdaptiveDifficulty()
        self.practice_goals = PracticeGoals()
        
        # Initialize accessibility manager
        self.accessibility_manager = None
        
        # Initialize form styling integration manager
        self.form_integration_manager = None
        
        # Initialize typography theme manager
        self.typography_theme_manager = None
        
        self.initUI()
        
        # Apply basic error fixes only - ROLLBACK MODE
        self._apply_basic_error_fixes()
        
        # Initialize basic form styling fixes - SIMPLIFIED FOR ROLLBACK
        # self._initialize_form_styling()  # COMMENTED OUT - was causing issues
        
        # Initialize basic accessibility features - SIMPLIFIED FOR ROLLBACK
        # self._initialize_accessibility()  # COMMENTED OUT - complex integration
        
        # Initialize spacing optimization - COMMENTED OUT FOR ROLLBACK
        # self._initialize_spacing_optimization()  # COMMENTED OUT - complex layout changes
        
        # Apply typography and sizing fixes - COMMENTED OUT FOR ROLLBACK
        # self._apply_typography_size_fixes()  # COMMENTED OUT - causing sizing issues
        
        # Check and display streak after UI is initialized
        self.check_daily_streak()

    def initUI(self) -> None:
        self.createToolBar()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Create the main splitter for three-column layout
        self.main_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.main_splitter)

        # ----- Left Column: Indicators, Context, Stats -----
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(10, 10, 10, 10)
        left_layout.setSpacing(10)

        self.sentence_label = QLabel("Sentence will appear here.")
        self.sentence_label.setWordWrap(True)
        left_layout.addWidget(self.sentence_label)

        self.translation_label = QLabel("")
        self.translation_label.setWordWrap(True)
        self.translation_label.setStyleSheet("color: gray;")
        self.translation_label.setVisible(False)
        left_layout.addWidget(self.translation_label)

        self.stats_label = QLabel("Exercises: 0 | Correct: 0")
        self.stats_label.setStyleSheet("color: gray;")
        left_layout.addWidget(self.stats_label)

        # Subjunctive Triggers and Additional Context
        trigger_box = QGroupBox("Subjunctive Indicators & Context")
        trigger_layout = QVBoxLayout(trigger_box)
        trigger_layout.setSpacing(8)
        self.trigger_scroll_area = QScrollArea()
        self.trigger_scroll_area.setWidgetResizable(True)
        self.trigger_scroll_area.setMinimumHeight(150)
        trigger_scroll_content = QWidget()
        sc_layout = QVBoxLayout(trigger_scroll_content)
        sc_layout.setContentsMargins(5, 5, 5, 5)
        sc_layout.setSpacing(5)
        self.trigger_checkboxes = []
        typical_triggers = [
            "Wishes (querer que, desear que)", "Emotions (gustar que, sentir que)",
            "Impersonal expressions (es bueno que, es necesario que)",
            "Requests (pedir que, rogar que)",
            "Doubt/Denial (dudar que, no creer que)", "Negation (no pensar que, no es cierto que)",
            "Ojalá (ojalá que)", "Conjunctions (para que, antes de que, a menos que)",
            "Superlatives (el mejor ... que)", "Indefinite antecedents (busco a alguien que...)",
            "Nonexistent antecedents (no hay nadie que...)"
        ]
        for trig in typical_triggers:
            cb = QCheckBox(trig)
            sc_layout.addWidget(cb)
            self.trigger_checkboxes.append(cb)
        sc_layout.addStretch(1)
        self.trigger_scroll_area.setWidget(trigger_scroll_content)
        self.custom_context_input = QLineEdit()
        self.custom_context_input.setPlaceholderText("Enter additional context (e.g., polite request, uncertainty scenario)")
        trigger_layout.addWidget(self.trigger_scroll_area)
        trigger_layout.addWidget(self.custom_context_input)
        left_layout.addWidget(trigger_box)
        left_layout.addStretch()
        
        # Set minimum width for left column to prevent content cutoff
        left_widget.setMinimumWidth(320)
        self.main_splitter.addWidget(left_widget)

        # ----- Middle Column: Exercise Controls and Input -----
        middle_widget = QWidget()
        middle_layout = QVBoxLayout(middle_widget)
        middle_layout.setContentsMargins(10, 10, 10, 10)
        middle_layout.setSpacing(10)

        # Tense and Person selections using checkboxes (no defaults)
        selection_box = QGroupBox("Select Tense(s) and Person(s)")
        sel_layout = QHBoxLayout(selection_box)
        sel_layout.setContentsMargins(10, 10, 10, 10)
        sel_layout.setSpacing(20)

        # -- Tense(s) box --
        tense_box = QGroupBox("Tense(s)")
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
            self.tense_checkboxes[tense] = cb
            tense_layout.addWidget(cb)
        tense_box.setLayout(tense_layout)

        # -- Person(s) box --
        person_box = QGroupBox("Person(s)")
        person_layout = QVBoxLayout(person_box)
        person_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.person_checkboxes = {}
        persons = ["yo", "tú", "él/ella/usted", "nosotros", "vosotros", "ellos/ellas/ustedes"]
        for person in persons:
            cb = QCheckBox(person)
            self.person_checkboxes[person] = cb
            person_layout.addWidget(cb)
        person_box.setLayout(person_layout)

        sel_layout.addWidget(tense_box, 1)
        sel_layout.addWidget(person_box, 1)
        sel_layout.addStretch()
        middle_layout.addWidget(selection_box)

        # Specific Verbs (optional)
        verb_box = QGroupBox("Specific Verbs (optional, comma-separated)")
        vb_layout = QHBoxLayout(verb_box)
        self.verbs_input = QLineEdit()
        self.verbs_input.setPlaceholderText("e.g., hablar, comer, vivir")
        vb_layout.addWidget(self.verbs_input)
        middle_layout.addWidget(verb_box)

        # Mode, Difficulty and Task Type selection
        mode_layout = QHBoxLayout()
        mode_label = QLabel("Mode:")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Free Response", "Multiple Choice"])
        self.mode_combo.currentIndexChanged.connect(self.switchMode)
        
        difficulty_label = QLabel("Difficulty:")
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Beginner", "Intermediate", "Advanced"])
        self.difficulty_combo.setCurrentIndex(1)  # Default to Intermediate
        
        task_type_label = QLabel("Type:")
        self.task_type_combo = QComboBox()
        self.task_type_combo.addItems(["Traditional Grammar", "TBLT Scenarios", "Mood Contrast", "Review Mode"])
        self.task_type_combo.currentIndexChanged.connect(self.onTaskTypeChanged)
        
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.mode_combo)
        mode_layout.addWidget(difficulty_label)
        mode_layout.addWidget(self.difficulty_combo)
        mode_layout.addWidget(task_type_label)
        mode_layout.addWidget(self.task_type_combo)
        mode_layout.addStretch()
        middle_layout.addLayout(mode_layout)

        # Input stack for answer entry
        self.input_stack = QStackedWidget()
        free_response_page = QWidget()
        fr_layout = QVBoxLayout(free_response_page)
        self.free_response_input = QLineEdit()
        self.free_response_input.setPlaceholderText("Type your answer here...")
        fr_layout.addWidget(self.free_response_input)
        self.input_stack.addWidget(free_response_page)
        mc_page = QWidget()
        mc_layout = QVBoxLayout(mc_page)
        self.mc_button_group = QButtonGroup(mc_page)
        self.mc_options_layout = QHBoxLayout()  # Horizontal arrangement for multiple choice options
        mc_layout.addLayout(self.mc_options_layout)
        self.input_stack.addWidget(mc_page)
        middle_layout.addWidget(self.input_stack)

        # Navigation Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        self.prev_button = QPushButton("Previous")
        self.hint_button = QPushButton("Hint")
        self.submit_button = QPushButton("Submit")
        self.next_button = QPushButton("Next")
        
        # Apply visual styling if available
        if apply_widget_specific_styles:
            apply_widget_specific_styles(self.submit_button, 'primary-button')
            apply_widget_specific_styles(self.hint_button, 'secondary-button')
            apply_widget_specific_styles(self.prev_button, 'secondary-button')
            apply_widget_specific_styles(self.next_button, 'secondary-button')
        
        buttons_layout.addWidget(self.prev_button)
        buttons_layout.addWidget(self.hint_button)
        buttons_layout.addWidget(self.submit_button)
        buttons_layout.addWidget(self.next_button)
        middle_layout.addLayout(buttons_layout)
        
        # Set minimum width for middle column and add to splitter
        middle_widget.setMinimumWidth(280)
        self.main_splitter.addWidget(middle_widget)

        # ----- Right Column: Feedback and Progress -----
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(10, 10, 10, 10)
        right_layout.setSpacing(10)

        # --- Feedback Text (Explanations) with Scrollability ---
        self.feedback_text = QTextEdit()
        self.feedback_text.setReadOnly(True)
        self.feedback_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        feedback_scroll = QScrollArea()
        feedback_scroll.setWidgetResizable(True)
        feedback_scroll.setWidget(self.feedback_text)
        right_layout.addWidget(feedback_scroll)

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        right_layout.addWidget(self.progress_bar)
        
        # Set minimum width for right column and add to splitter
        right_widget.setMinimumWidth(200)
        self.main_splitter.addWidget(right_widget)
        
        # Configure three-column layout proportions (40% left, 35% middle, 25% right)
        # Set stretch factors (these are relative to each other)
        self.main_splitter.setStretchFactor(0, 8)   # Left column (8/18 = 44%)
        self.main_splitter.setStretchFactor(1, 7)   # Middle column (7/18 = 39%)  
        self.main_splitter.setStretchFactor(2, 5)   # Right column (5/18 = 28%)
        
        # Set initial sizes with explicit values to ensure proper proportions
        # Using larger values to ensure stretch factors take effect
        self.main_splitter.setSizes([
            480,  # 40% of 1200px
            420,  # 35% of 1200px  
            300   # 25% of 1200px
        ])
        
        # Enable proper resizing behavior
        self.main_splitter.setChildrenCollapsible(False)  # Prevent columns from collapsing completely
        
        # Add spacing between columns for better visual separation
        self.main_splitter.setHandleWidth(8)  # Increase splitter handle width for better visibility
        
        # Store for later adjustment after window is shown
        self._initial_column_setup_done = False

        # Initialize progress overlay after UI is set up
        if PROGRESS_INDICATORS_AVAILABLE:
            self.progress_overlay = ProgressOverlay(self)
            self.progress_overlay.cancelled.connect(self.handle_operation_cancelled)
            # Connect progress manager signals
            self.progress_manager.progress_started.connect(self.handle_progress_started)
            self.progress_manager.progress_updated.connect(self.handle_progress_updated)
            self.progress_manager.progress_finished.connect(self.handle_progress_finished)
        
        # Connect buttons
        self.submit_button.clicked.connect(self.submitAnswer)
        self.next_button.clicked.connect(self.nextExercise)
        self.prev_button.clicked.connect(self.prevExercise)
        self.hint_button.clicked.connect(self.provideHint)
        
        # Add keyboard shortcuts with enhanced accessibility
        self.submit_button.setShortcut("Return")
        self.next_button.setShortcut("Right")
        self.prev_button.setShortcut("Left")
        self.hint_button.setShortcut("H")
        
        # Enhanced keyboard shortcuts for accessibility
        self.submit_button.setToolTip("Submit Answer (Return)")
        self.next_button.setToolTip("Next Exercise (Right Arrow)")
        self.prev_button.setToolTip("Previous Exercise (Left Arrow)")
        self.hint_button.setToolTip("Show Hint (H)")
        
        # Enter key submits in free response mode
        self.free_response_input.returnPressed.connect(self.submitAnswer)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Add streak label to status bar
        self.streak_label = QLabel()
        self.status_bar.addPermanentWidget(self.streak_label)
        
        self.updateStatus("Welcome! Please make all required selections and generate new exercises.")

        # Apply text truncation fixes
        if TEXT_TRUNCATION_FIXES_AVAILABLE:
            try:
                fix_text_truncation_issues(self)
                logger.info("Text truncation fixes applied successfully")
            except Exception as e:
                logger.error(f"Failed to apply text truncation fixes: {e}")
        
        # Apply checkbox rendering fixes
        if CHECKBOX_RENDERING_FIXES_AVAILABLE:
            try:
                fix_checkbox_rendering_issues(self)
                remove_red_borders_from_forms(self)
                logger.info("Checkbox rendering fixes applied successfully")
            except Exception as e:
                logger.error(f"Failed to apply checkbox rendering fixes: {e}")
        
        # Initialize exercise data
        self.exercises = []
        self.total_exercises = 0
        self.updateStats()
        logger.info("Application initialized.")
    
    def _apply_basic_error_fixes(self):
        """Apply basic error fixes only - simplified for rollback"""
        try:
            # Apply only essential fixes to prevent crashes
            logger.info("Applying basic error fixes only (rollback mode)")
            
            # Ensure widgets have proper default styles to prevent red boxes
            self.setStyleSheet("""
                QWidget {
                    background-color: #f0f0f0;
                }
                QMainWindow {
                    background-color: #f8f8f8;
                }
                QLabel {
                    background-color: transparent;
                    color: #1A202C;
                    font-weight: 500;
                    font-size: 14px;
                    padding: 2px 0;
                }
                QCheckBox {
                    color: #1A202C;
                    font-weight: 500;
                    font-size: 14px;
                    padding: 4px 0;
                }
                QRadioButton {
                    color: #1A202C;
                    font-weight: 500;
                    font-size: 14px;
                    padding: 4px 0;
                }
                QGroupBox {
                    font-weight: 600;
                    font-size: 16px;
                    color: #1A202C;
                    border: 2px solid #E2E8F0;
                    border-radius: 8px;
                    margin-top: 12px;
                    padding-top: 16px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 8px 0 8px;
                    color: #3B82F6;
                    font-weight: 600;
                }
                QPushButton {
                    background-color: #e0e0e0;
                    border: 1px solid #ccc;
                    padding: 5px 10px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #d0d0d0;
                }
                QLineEdit {
                    background-color: white;
                    border: 2px solid #CBD5E0;
                    padding: 8px 12px;
                    border-radius: 6px;
                    font-size: 14px;
                    color: #1A202C;
                    min-height: 20px;
                    outline: none;
                }
                QLineEdit:focus {
                    border-color: #3B82F6;
                    background-color: #FFFFFF;
                    outline: none;
                }
                QLineEdit:hover {
                    border-color: #A0AEC0;
                    background-color: #FAFBFC;
                }
                QLineEdit::placeholder {
                    color: #9CA3AF;
                    font-style: italic;
                }
                QTextEdit {
                    background-color: white;
                    border: 1px solid #ccc;
                    border-radius: 3px;
                }
                
                /* Checkbox styling fixes - remove red borders and ensure visibility */
                QCheckBox {
                    background-color: transparent;
                    color: #333;
                    spacing: 8px;
                    padding: 4px;
                    border: none;
                    font-size: 13px;
                }
                
                QCheckBox::indicator {
                    width: 16px;
                    height: 16px;
                    border: 2px solid #888;
                    border-radius: 3px;
                    background-color: white;
                }
                
                QCheckBox::indicator:hover {
                    border-color: #555;
                    background-color: #f5f5f5;
                }
                
                QCheckBox::indicator:checked {
                    background-color: #4a90e2;
                    border-color: #4a90e2;
                    image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOSIgdmlld0JveD0iMCAwIDEyIDkiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDQuNUw0LjUgOEwxMSAxIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K);
                }
                
                QCheckBox::indicator:checked:hover {
                    background-color: #357abd;
                    border-color: #357abd;
                }
                
                QCheckBox::indicator:focus {
                    border: 2px solid #4a90e2;
                    outline: none;
                }
                
                QCheckBox::indicator:disabled {
                    background-color: #f0f0f0;
                    border-color: #ccc;
                }
                
                /* Group box styling for consistent appearance */
                QGroupBox {
                    font-weight: bold;
                    border: 2px solid #ccc;
                    border-radius: 5px;
                    margin-top: 10px;
                    padding-top: 10px;
                }
                
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                    background-color: #f8f8f8;
                }
            """)
            
        except Exception as e:
            logger.warning(f"Failed to apply basic error fixes: {e}")
    
    # COMMENTED OUT FOR ROLLBACK - was causing red box issues
    # def _initialize_form_styling(self):
    #     """Initialize form styling fixes to address red box and visibility issues"""
    #     try:
    #         if integrate_form_fixes:
    #             # Get the application instance
    #             app = QApplication.instance()
    #             if app:
    #                 # Apply form styling fixes
    #                 self.form_integration_manager = integrate_form_fixes(
    #                     app, 
    #                     self, 
    #                     self.dark_mode  # Use current theme mode
    #                 )
    #                 
    #                 if self.form_integration_manager:
    #                     logger.info("Form styling fixes initialized successfully - red boxes and visibility issues addressed")
    #                     
    #                     # Refresh styling after UI is fully initialized
    #                     QTimer.singleShot(100, self.form_integration_manager.refresh_styling)
    #                 else:
    #                     logger.warning("Form styling integration manager creation failed")
    #             else:
    #                 logger.warning("QApplication instance not found for form styling")
    #         else:
    #             logger.info("Form styling fixes not available")
    #             
    #     except Exception as e:
    #         logger.error(f"Error initializing form styling: {e}")
    #         # Continue without form styling fixes
    #         self.form_integration_manager = None
    
    # COMMENTED OUT FOR ROLLBACK - complex accessibility integration
    # def _initialize_accessibility(self):
        """Initialize accessibility features with error fixes"""
        try:
            # Try to use patched accessibility integration first
            try:
                from src.accessibility_integration_patch import integrate_patched_accessibility
                self.accessibility_manager = integrate_patched_accessibility(self)
                if self.accessibility_manager:
                    logger.info("Patched accessibility features initialized successfully")
                    return
            except ImportError:
                logger.info("Accessibility patch not available, trying original")
            
            # Fall back to original integration
            if integrate_accessibility:
                self.accessibility_manager = integrate_accessibility(self)
                
                if self.accessibility_manager:
                    # Set up accessibility startup check
                    if add_accessibility_startup_check:
                        add_accessibility_startup_check(self, self.accessibility_manager)
                    
                    logger.info("Accessibility features initialized successfully")
                else:
                    logger.warning("Failed to initialize accessibility features")
            else:
                logger.info("Accessibility features not available")
                
        except Exception as e:
            logger.error(f"Error initializing accessibility: {e}")
            # Continue without accessibility features
            self.accessibility_manager = None
    
    # COMMENTED OUT FOR ROLLBACK - complex layout changes
    # def _initialize_spacing_optimization(self):
        """Initialize spacing and layout optimization for better readability"""
        try:
            if apply_spacing_to_spanish_app:
                self.spacing_optimizer = apply_spacing_to_spanish_app(self)
                
                if self.spacing_optimizer:
                    logger.info("Spacing optimization initialized successfully")
                    
                    # Apply specific optimizations for key text elements
                    self._optimize_text_elements()
                    
                    # Create breathing room in layouts
                    self._add_visual_breathing_room()
                    
                    logger.info("Text spacing and layout optimized for better readability")
                else:
                    logger.warning("Failed to initialize spacing optimization")
            else:
                logger.info("Spacing optimizer not available")
                
        except Exception as e:
            logger.error(f"Error initializing spacing optimization: {e}")
            # Continue without spacing optimization
            self.spacing_optimizer = None
    
    def _optimize_text_elements(self):
        """Apply specific optimizations to text elements for better readability"""
        if not self.spacing_optimizer:
            return
            
        try:
            # Optimize main content labels with enhanced line spacing
            self.sentence_label.setStyleSheet(self.sentence_label.styleSheet() + """
                QLabel {
                    line-height: 1.6;
                    padding: 16px 12px;
                    margin: 8px 0px;
                }
            """)
            
            # Optimize translation label with subtle styling
            self.translation_label.setStyleSheet(self.translation_label.styleSheet() + """
                QLabel {
                    line-height: 1.5;
                    padding: 12px;
                    margin: 6px 0px;
                    font-style: italic;
                }
            """)
            
            # Optimize stats label for quick scanning
            self.stats_label.setStyleSheet(self.stats_label.styleSheet() + """
                QLabel {
                    padding: 8px 12px;
                    margin: 4px 0px;
                    letter-spacing: 0.5px;
                }
            """)
            
            # Optimize feedback text area for extended reading
            self.feedback_text.setStyleSheet(self.feedback_text.styleSheet() + """
                QTextEdit {
                    line-height: 1.65;
                    padding: 20px;
                    margin: 12px 0px;
                }
            """)
            
            logger.debug("Applied specific text element optimizations")
            
        except Exception as e:
            logger.error(f"Error optimizing text elements: {e}")
    
    def _add_visual_breathing_room(self):
        """Add visual breathing room throughout the interface"""
        if not self.spacing_optimizer:
            return
            
        try:
            # Add breathing room to the main splitter
            central_widget = self.centralWidget()
            if central_widget and hasattr(central_widget, 'layout'):
                layout = central_widget.layout()
                if layout:
                    layout.setContentsMargins(20, 15, 20, 15)
                    layout.setSpacing(15)
            
            # Optimize group box spacing for better visual hierarchy
            for child in self.findChildren(QGroupBox):
                child.setStyleSheet(child.styleSheet() + """
                    QGroupBox {
                        margin: 16px 0px;
                        padding: 20px 16px;
                        border-radius: 6px;
                    }
                    QGroupBox::title {
                        padding: 0 8px;
                        margin-bottom: 12px;
                    }
                """)
            
            # Optimize button spacing for better touch targets
            for child in self.findChildren(QPushButton):
                child.setStyleSheet(child.styleSheet() + """
                    QPushButton {
                        padding: 12px 20px;
                        margin: 8px 4px;
                        min-height: 44px;
                    }
                """)
            
            logger.debug("Added visual breathing room to interface elements")
            
        except Exception as e:
            logger.error(f"Error adding visual breathing room: {e}")
    
    def toggleSpacingOptimization(self):
        """Toggle spacing optimization on/off"""
        try:
            if not self.spacing_optimizer:
                # Initialize spacing optimizer if not already done
                if apply_spacing_to_spanish_app:
                    self.spacing_optimizer = apply_spacing_to_spanish_app(self)
                    if self.spacing_optimizer:
                        self._optimize_text_elements()
                        self._add_visual_breathing_room()
                        self.updateStatus("Spacing optimization enabled - improved readability!")
                        logger.info("Spacing optimization enabled")
                    else:
                        self.updateStatus("Failed to initialize spacing optimization")
                else:
                    self.updateStatus("Spacing optimizer not available")
            else:
                # Reset to basic spacing
                self._reset_to_basic_spacing()
                self.spacing_optimizer = None
                self.updateStatus("Spacing optimization disabled - using basic layout")
                logger.info("Spacing optimization disabled")
                
        except Exception as e:
            logger.error(f"Error toggling spacing optimization: {e}")
            self.updateStatus("Error toggling spacing optimization")
    
    def _reset_to_basic_spacing(self):
        """Reset all widgets to basic spacing"""
        try:
            # Reset main text elements to basic styling
            basic_styles = {
                'sentence_label': "QLabel { padding: 4px; margin: 2px; }",
                'translation_label': "QLabel { padding: 4px; margin: 2px; color: gray; }",
                'stats_label': "QLabel { padding: 4px; margin: 2px; color: gray; }",
                'feedback_text': "QTextEdit { padding: 8px; margin: 4px; }"
            }
            
            for attr_name, style in basic_styles.items():
                if hasattr(self, attr_name):
                    widget = getattr(self, attr_name)
                    widget.setStyleSheet(style)
            
            # Reset layout margins
            central_widget = self.centralWidget()
            if central_widget and hasattr(central_widget, 'layout'):
                layout = central_widget.layout()
                if layout:
                    layout.setContentsMargins(10, 10, 10, 10)
                    layout.setSpacing(10)
            
            logger.debug("Reset to basic spacing")
            
        except Exception as e:
            logger.error(f"Error resetting to basic spacing: {e}")
    
    # COMMENTED OUT FOR ROLLBACK - was causing sizing issues
    # def _apply_typography_size_fixes(self):
        """Apply enhanced typography and element sizing fixes"""
        try:
            if apply_typography_size_fixes:
                result = apply_typography_size_fixes(self)
                
                if result['success']:
                    self.typography_theme_manager = result.get('theme_manager')
                    logger.info(f"Typography fixes applied successfully: {len(result['fixes_applied'])} fixes")
                    
                    # Show status message about improvements
                    fixes_count = len(result['fixes_applied'])
                    accessibility_score = result.get('accessibility_compliance', {}).get('compliant', False)
                    
                    if accessibility_score:
                        self.updateStatus(f"Enhanced typography applied: {fixes_count} improvements, accessibility compliant!")
                    else:
                        issues_count = len(result.get('accessibility_issues', []))
                        self.updateStatus(f"Enhanced typography applied: {fixes_count} improvements, {issues_count} accessibility items noted")
                    
                    # Add toolbar action for accessibility report
                    self._add_accessibility_report_action()
                    
                else:
                    logger.error(f"Typography fixes failed: {result.get('error', 'Unknown error')}")
                    self.updateStatus("Typography enhancement failed - using default styling")
            else:
                logger.info("Typography size fixes module not available")
                self.updateStatus("Using basic typography - enhanced typography module not available")
                
        except Exception as e:
            logger.error(f"Error applying typography size fixes: {e}")
            self.updateStatus("Error applying typography fixes - using default styling")
    
    def _add_accessibility_report_action(self):
        """Add accessibility report action to toolbar if typography fixes are available"""
        try:
            if hasattr(self, 'menuBar'):  # If there's a menu bar
                # Find or create accessibility menu
                menubar = self.menuBar()
                accessibility_menu = None
                
                for action in menubar.actions():
                    if action.text() == "Accessibility":
                        accessibility_menu = action.menu()
                        break
                
                if not accessibility_menu:
                    accessibility_menu = menubar.addMenu("Accessibility")
                
                # Add accessibility report action
                report_action = accessibility_menu.addAction("View Accessibility Report")
                report_action.setToolTip("View detailed accessibility and typography report")
                report_action.triggered.connect(self._show_accessibility_report)
                
            # Also add to toolbar if available
            toolbar = self.findChild(QToolBar)
            if toolbar and get_accessibility_report:
                report_toolbar_action = toolbar.addAction("A11y Report")
                report_toolbar_action.setToolTip("View accessibility report")
                report_toolbar_action.triggered.connect(self._show_accessibility_report)
                
        except Exception as e:
            logger.error(f"Error adding accessibility report action: {e}")
    
    def _show_accessibility_report(self):
        """Show accessibility report dialog"""
        try:
            if get_accessibility_report:
                report = get_accessibility_report(self)
                
                report_text = f"""Accessibility Report for Spanish Subjunctive Practice
═══════════════════════════════════════════════════════

Overall Score: {report['overall_score']}
Elements Checked: {report.get('font_sizes_checked', 0) + report.get('touch_targets_checked', 0)}
Compliant Elements: {report.get('compliant_elements', 0)}

Font Size Analysis:
• Elements checked: {report.get('font_sizes_checked', 0)}

Touch Target Analysis:
• Elements checked: {report.get('touch_targets_checked', 0)}

Accessibility Violations:
{chr(10).join(['• ' + violation for violation in report.get('accessibility_violations', [])]) if report.get('accessibility_violations') else '• None found - great job!'}

Recommendations:
{chr(10).join(['• ' + rec for rec in report.get('recommendations', [])]) if report.get('recommendations') else '• No recommendations needed'}
"""
                
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.information(self, "Accessibility Report", report_text)
                
            else:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.information(self, "Accessibility Report", 
                                      "Accessibility reporting module not available.")
                
        except Exception as e:
            logger.error(f"Error showing accessibility report: {e}")
    
    def toggle_enhanced_theme(self):
        """Toggle between light and dark themes using enhanced typography system"""
        try:
            if self.typography_theme_manager:
                new_theme = self.typography_theme_manager.toggle_theme()
                self.updateStatus(f"Switched to enhanced {new_theme} theme")
                logger.info(f"Enhanced theme switched to {new_theme}")
                return new_theme
            else:
                # Fall back to basic theme switching
                self.toggleTheme()
                return "basic"
        except Exception as e:
            logger.error(f"Error toggling enhanced theme: {e}")
            self.updateStatus("Error switching theme")
            return None

    def createToolBar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        new_action = QAction("New Exercises", self)
        new_action.setToolTip("Generate new subjunctive exercises")
        new_action.triggered.connect(self.generateNewExercise)
        toolbar.addAction(new_action)
        reset_action = QAction("Reset Progress", self)
        reset_action.setToolTip("Reset your session progress")
        reset_action.triggered.connect(self.resetProgress)
        toolbar.addAction(reset_action)
        summary_action = QAction("Summary", self)
        summary_action.setToolTip("Generate session summary")
        summary_action.triggered.connect(self.generateSessionSummary)
        toolbar.addAction(summary_action)
        theme_action = QAction("Toggle Theme", self)
        theme_action.setToolTip("Toggle Light/Dark themes")
        theme_action.triggered.connect(self.toggle_enhanced_theme)
        toolbar.addAction(theme_action)
        translation_action = QAction("Toggle Translation", self)
        translation_action.setToolTip("Show/hide English translation")
        translation_action.triggered.connect(self.toggleTranslation)
        toolbar.addAction(translation_action)
        
        # Add export and stats actions
        export_action = QAction("Export Session", self)
        export_action.setToolTip("Export session to CSV")
        export_action.triggered.connect(self.exportSession)
        toolbar.addAction(export_action)
        
        stats_action = QAction("View Stats", self)
        stats_action.setToolTip("View detailed statistics")
        stats_action.triggered.connect(self.showDetailedStats)
        toolbar.addAction(stats_action)
        
        # Add review and save actions
        review_action = QAction("Review Mistakes", self)
        review_action.setToolTip("Review incorrect answers")
        review_action.triggered.connect(self.startReviewMode)
        toolbar.addAction(review_action)
        
        save_action = QAction("Save Progress", self)
        save_action.setToolTip("Save current session")
        save_action.triggered.connect(self.saveProgress)
        toolbar.addAction(save_action)
        
        conjugation_action = QAction("Conjugation Reference", self)
        conjugation_action.setToolTip("Quick conjugation reference")
        conjugation_action.setShortcut("Ctrl+R")
        conjugation_action.triggered.connect(self.showConjugationReference)
        toolbar.addAction(conjugation_action)
        
        goals_action = QAction("Practice Goals", self)
        goals_action.setToolTip("Set and view practice goals")
        goals_action.triggered.connect(self.showGoalsDialog)
        toolbar.addAction(goals_action)
        
        spacing_action = QAction("Optimize Spacing", self)
        spacing_action.setToolTip("Toggle spacing optimization for better readability")
        spacing_action.triggered.connect(self.toggleSpacingOptimization)
        toolbar.addAction(spacing_action)
        
        # Add API health monitoring action
        api_health_action = QAction("API Health", self)
        api_health_action.setToolTip("Check OpenAI API status and performance metrics")
        api_health_action.triggered.connect(self.showAPIHealthDialog)
        toolbar.addAction(api_health_action)

    def check_daily_streak(self):
        """Check and display daily practice streak"""
        streak_info = self.streak_tracker.record_practice()
        self.streak_label.setText(f"🔥 Streak: {streak_info['current']} days | Best: {streak_info['best']}")
        
        # Show motivational message if streak is maintained
        if streak_info['current'] > 0:
            self.updateStatus(streak_info['message'])
    
    def toggleTheme(self):
        if self.style_manager:
            self.style_manager.toggle_theme()
            current_theme = self.style_manager.get_current_theme()
            self.dark_mode = (current_theme == 'dark')
            
            # Update form styling to match new theme
            if self.form_integration_manager:
                self.form_integration_manager.toggle_dark_mode()
                logger.info("Form styling updated for theme change")
            
            self.updateStatus(f"Switched to {current_theme} theme.")
            logger.info(f"Switched to {current_theme} theme.")
        else:
            # Fallback to basic theme switching if visual module not available
            if self.dark_mode:
                self.setStyleSheet("")
                self.dark_mode = False
                
                # Update form styling for light mode
                if self.form_integration_manager:
                    self.form_integration_manager.dark_mode = False
                    self.form_integration_manager.initialize_form_styling(False)
                
                self.updateStatus("Switched to light theme.")
                logger.info("Switched to light theme.")
            else:
                # Simple dark theme fallback
                basic_dark_stylesheet = """
                    QMainWindow { background-color: #2b2b2b; color: #ffffff; }
                    QWidget { background-color: transparent; color: #ffffff; }
                    QLabel { 
                        background-color: transparent; 
                        color: #F7FAFC; 
                        font-weight: 500;
                        font-size: 14px;
                        padding: 2px 0;
                    }
                    QCheckBox { 
                        color: #F7FAFC; 
                        font-weight: 500;
                        font-size: 14px;
                        padding: 4px 0;
                    }
                    QRadioButton { 
                        color: #F7FAFC; 
                        font-weight: 500;
                        font-size: 14px;
                        padding: 4px 0;
                    }
                    QGroupBox { 
                        font-weight: 600;
                        font-size: 16px;
                        color: #F7FAFC;
                        border: 2px solid #4A5568;
                        border-radius: 8px;
                        margin-top: 12px;
                        padding-top: 16px;
                        background-color: #3c3c3c;
                    }
                    QGroupBox::title {
                        subcontrol-origin: margin;
                        left: 10px;
                        padding: 0 8px 0 8px;
                        color: #63B3ED;
                        font-weight: 600;
                    }
                    QPushButton { background-color: #0066cc; color: white; padding: 8px; border-radius: 4px; }
                    QPushButton:hover { background-color: #0052a3; }
                    QLineEdit {
                        background-color: #2D3748;
                        border: 2px solid #4A5568;
                        padding: 8px 12px;
                        border-radius: 6px;
                        font-size: 14px;
                        color: #F7FAFC;
                        min-height: 20px;
                        outline: none;
                    }
                    QLineEdit:focus {
                        border-color: #63B3ED;
                        background-color: #2D3748;
                        outline: none;
                    }
                    QLineEdit:hover {
                        border-color: #718096;
                        background-color: #4A5568;
                    }
                    QLineEdit::placeholder {
                        color: #718096;
                        font-style: italic;
                    }
                    QTextEdit { background-color: #3c3c3c; border: 1px solid #555; color: #ffffff; }
                """
                self.setStyleSheet(basic_dark_stylesheet)
                self.dark_mode = True
                
                # Update form styling for dark mode
                if self.form_integration_manager:
                    self.form_integration_manager.dark_mode = True
                    self.form_integration_manager.initialize_form_styling(True)
                
                self.updateStatus("Switched to dark theme.")
                logger.info("Switched to dark theme.")

    def onTaskTypeChanged(self, index):
        """Handle task type change"""
        task_types = ["traditional", "tblt", "contrast", "review"]
        self.current_task_type = task_types[index]
        
        # Update UI based on task type
        if self.current_task_type == "tblt":
            self.updateStatus("TBLT mode: Focus on real-world communication tasks")
            self.custom_context_input.setPlaceholderText("Task context will appear here...")
            self.review_mode = False
        elif self.current_task_type == "contrast":
            self.updateStatus("Contrast mode: Compare indicative vs subjunctive")
            self.review_mode = False
        elif self.current_task_type == "review":
            self.startReviewMode()
        else:
            self.updateStatus("Traditional mode: Grammar-focused exercises")
            self.custom_context_input.setPlaceholderText("Enter additional context (optional)")
            self.review_mode = False
    
    def toggleTranslation(self):
        self.show_translation = not self.show_translation
        self.translation_label.setVisible(self.show_translation)
        self.updateExercise()
        self.updateStatus("Translation " + ("on" if self.show_translation else "off"))
        logger.info("Translation toggled %s", "on" if self.show_translation else "off")

    def updateStats(self):
        accuracy = 0
        if self.session_stats["total_attempts"] > 0:
            accuracy = (self.session_stats["correct_attempts"] / self.session_stats["total_attempts"]) * 100
            
            # Check for adaptive difficulty adjustment
            adjustment = self.adaptive_difficulty.record_performance(
                self.session_stats["correct_attempts"] > self.session_stats["total_attempts"] * 0.5
            )
            if adjustment["adjusted"]:
                self.difficulty_combo.setCurrentText(adjustment["new_level"])
                QMessageBox.information(self, "Difficulty Adjusted", 
                    f"Difficulty changed to {adjustment['new_level']} based on your performance!")
        
        self.stats_label.setText(f"Exercise: {self.current_exercise + 1}/{self.total_exercises} | Correct: {self.correct_count} | Accuracy: {accuracy:.1f}%")

    def updateStatus(self, msg: str):
        self.status_bar.showMessage(msg, 4000)
        logger.info("Status update: %s", msg)

    def getSelectedTriggers(self) -> List[str]:
        return [cb.text() for cb in self.trigger_checkboxes if cb.isChecked()]

    def getSelectedTenses(self) -> List[str]:
        return [tense for tense, cb in self.tense_checkboxes.items() if cb.isChecked()]

    def getSelectedPersons(self) -> List[str]:
        return [person for person, cb in self.person_checkboxes.items() if cb.isChecked()]

    def handle_operation_cancelled(self):
        """Handle when user cancels a long-running operation"""
        for operation in self.loading_states:
            if self.loading_states[operation]:
                if self.progress_manager:
                    self.progress_manager.cancel_operation(operation)
                self.loading_states[operation] = False
        
        # Re-enable UI
        self.set_ui_loading_state(False)
        self.updateStatus("Operation cancelled")
    
    def handle_progress_started(self, operation_id: str, message: str):
        """Handle progress start signal"""
        if self.progress_overlay:
            if operation_id in ['generating_exercises', 'generating_summary']:
                # Show with cancel option for longer operations
                self.progress_overlay.show_indeterminate(message, show_cancel=True)
            else:
                # Show without cancel for quick operations
                self.progress_overlay.show_indeterminate(message, show_cancel=False)
    
    def handle_progress_updated(self, operation_id: str, value: int, message: str):
        """Handle progress update signal"""
        if self.progress_overlay and message:
            self.progress_overlay.update_progress(value, message)
    
    def handle_progress_finished(self, operation_id: str, success: bool, message: str):
        """Handle progress finish signal"""
        if self.progress_overlay:
            self.progress_overlay.hide_progress()
        
        # Update status with result
        if success:
            self.updateStatus(message if message else "Operation completed")
        else:
            self.updateStatus(f"Error: {message}")
    
    def set_ui_loading_state(self, loading: bool, operation: str = None):
        """Enable/disable UI elements during loading operations"""
        # Disable main action buttons during loading
        self.submit_button.setEnabled(not loading)
        self.hint_button.setEnabled(not loading)
        
        # Disable navigation during exercise generation
        if operation == 'generating_exercises':
            self.next_button.setEnabled(not loading)
            self.prev_button.setEnabled(not loading)
        
        # Disable mode switching during loading
        self.mode_combo.setEnabled(not loading)
        self.difficulty_combo.setEnabled(not loading)
        self.task_type_combo.setEnabled(not loading)
        
        # Update button text for loading states
        if loading and operation:
            if operation == 'checking_answer' and hasattr(self.submit_button, 'start_loading'):
                self.submit_button.start_loading("Checking...")
            elif operation == 'getting_hint' and hasattr(self.hint_button, 'start_loading'):
                self.hint_button.start_loading("Getting hint...")
        else:
            # Reset button states
            if hasattr(self.submit_button, 'stop_loading'):
                self.submit_button.stop_loading()
            if hasattr(self.hint_button, 'stop_loading'):
                self.hint_button.stop_loading()

    def generateNewExercise(self):
        # Check task type for TBLT mode
        if self.current_task_type == "tblt":
            self.generateTBLTExercises()
            return
        elif self.current_task_type == "contrast":
            self.generateContrastExercises()
            return
            
        # Traditional mode validation
        selected_triggers = self.getSelectedTriggers()
        if not selected_triggers:
            QMessageBox.warning(self, "Selection Required", "Please select at least one subjunctive trigger.")
            return
        selected_tenses = self.getSelectedTenses()
        if not selected_tenses:
            QMessageBox.warning(self, "Selection Required", "Please select at least one tense.")
            return
        selected_persons = self.getSelectedPersons()
        if not selected_persons:
            QMessageBox.warning(self, "Selection Required", "Please select at least one person.")
            return

        triggers_text = "; ".join(selected_triggers)
        tenses_text = ", ".join(selected_tenses)
        persons_text = ", ".join(selected_persons)
        additional_context = self.custom_context_input.text().strip()
        verbs_text = self.verbs_input.text().strip() or "Any relevant verb"
        difficulty = self.difficulty_combo.currentText()
        
        # Adjust prompt based on difficulty
        difficulty_instructions = {
            "Beginner": "Use simple vocabulary, common verbs, and clear sentence structures. Focus on the most common subjunctive triggers.",
            "Intermediate": "Use varied vocabulary and more complex sentence structures. Include less common triggers and verb forms.",
            "Advanced": "Use sophisticated vocabulary, complex sentence structures, idiomatic expressions, and challenging verb forms including irregulars."
        }

        # Optimized prompt for faster responses
        prompt = f"""Create 5 Spanish subjunctive exercises. {difficulty} level.
Tenses: {tenses_text} | Persons: {persons_text}
Return only JSON array:
[{{"context": "brief scenario", "sentence": "exercise text", "answer": "correct form", "choices": ["a","b","c","d"], "translation": "English"}}]

Requirements:
- {difficulty_instructions[difficulty]}
- LATAM Spanish
- Real situations
- No extra text"""

        # Start progress indication
        operation_id = 'generating_exercises'
        self.loading_states[operation_id] = True
        
        if self.progress_manager:
            loading_msg = create_api_loading_message(operation_id)
            self.progress_manager.start_operation(operation_id, loading_msg)
        
        # Set UI loading state
        self.set_ui_loading_state(True, operation_id)
        
        worker = GPTWorkerRunnable(prompt, max_tokens=800, temperature=0.7)
        worker.signals.result.connect(lambda result: self.handleNewExerciseResult(result, operation_id))
        self.threadpool.start(worker)
        self.updateStatus("Generating new exercises...")
        logger.info("Generating new exercises with prompt: %s", prompt)

    def generateTBLTExercises(self):
        """Generate TBLT-based communicative exercises"""
        difficulty = self.difficulty_combo.currentText()
        selected_tenses = self.getSelectedTenses() or ["Present Subjunctive"]
        
        prompt = f"""Create 5 TBLT subjunctive tasks. {difficulty} level.
Tenses: {', '.join(selected_tenses)}

Real scenarios (work/travel/social). Return only JSON:
[{{"context": "scenario", "sentence": "task", "answer": "subjunctive_form", "choices": ["a","b","c","d"], "translation": "English"}}]

LATAM Spanish. No extra text."""
        
        # Start progress indication for TBLT
        operation_id = 'generating_exercises'
        self.loading_states[operation_id] = True
        
        if self.progress_manager:
            loading_msg = "Generating TBLT communicative tasks..."
            self.progress_manager.start_operation(operation_id, loading_msg)
        
        # Set UI loading state
        self.set_ui_loading_state(True, operation_id)
        
        worker = GPTWorkerRunnable(prompt, max_tokens=1000, temperature=0.7)
        worker.signals.result.connect(lambda result: self.handleNewExerciseResult(result, operation_id))
        self.threadpool.start(worker)
        self.updateStatus("Generating TBLT communicative tasks...")
        
    def generateContrastExercises(self):
        """Generate indicative vs subjunctive contrast exercises"""
        difficulty = self.difficulty_combo.currentText()
        
        prompt = f"""Create 5 mood contrast exercises. {difficulty} level.

Compare indicative vs subjunctive. Return only JSON:
[{{"context": "topic", "sentence": "choose correct mood", "answer": "subjunctive_form", "choices": ["indicative","subjunctive","c","d"], "translation": "English"}}]

No extra text."""
        
        # Start progress indication for contrast exercises
        operation_id = 'generating_exercises'
        self.loading_states[operation_id] = True
        
        if self.progress_manager:
            loading_msg = "Generating mood contrast exercises..."
            self.progress_manager.start_operation(operation_id, loading_msg)
        
        # Set UI loading state
        self.set_ui_loading_state(True, operation_id)
        
        worker = GPTWorkerRunnable(prompt, max_tokens=1000, temperature=0.6)
        worker.signals.result.connect(lambda result: self.handleNewExerciseResult(result, operation_id))
        self.threadpool.start(worker)
        self.updateStatus("Generating mood contrast exercises...")
    
    def handleNewExerciseResult(self, result: str, operation_id: str = 'generating_exercises'):
        logger.info("Raw GPT response received:\n%s", result)
        result = result.replace("```", "").replace("`", "").strip()
        start_index = result.find("[")
        end_index = result.rfind("]")
        if start_index != -1 and end_index != -1:
            json_str = result[start_index:end_index+1]
        else:
            json_str = result
        logger.info("Extracted JSON substring:\n%s", json_str)
        def remove_trailing_commas(s: str) -> str:
            return re.sub(r',\s*([\]}}])', r'\1', s)
        old_str = None
        while old_str != json_str:
            old_str = json_str
            json_str = remove_trailing_commas(json_str)
        logger.info("After removing trailing commas:\n%s", json_str)
        if not json_str.endswith("]"):
            json_str += "]"
            logger.info("Appended closing bracket:\n%s", json_str)
        try:
            new_exercises = json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error("Error parsing JSON from GPT: %s", e)
            
            # Handle error in progress indication
            self.loading_states[operation_id] = False
            self.set_ui_loading_state(False, operation_id)
            
            if self.progress_manager:
                self.progress_manager.finish_operation(operation_id, False, "Failed to parse response from AI. Please try again.")
            else:
                QMessageBox.warning(self, "Parsing Error", "Failed to parse the JSON. Please try generating new exercises.")
            return
            
        if not isinstance(new_exercises, list) or len(new_exercises) == 0:
            # Handle empty result error
            self.loading_states[operation_id] = False
            self.set_ui_loading_state(False, operation_id)
            
            if self.progress_manager:
                self.progress_manager.finish_operation(operation_id, False, "AI returned empty results. Please try again.")
            else:
                QMessageBox.warning(self, "Error", "GPT returned an empty or invalid list. Try again.")
            return
        self.exercises = new_exercises
        self.total_exercises = len(self.exercises)
        self.current_exercise = 0
        self.correct_count = 0
        self.responses.clear()
        self.progress_bar.setMaximum(self.total_exercises)
        self.updateExercise()
        self.updateStats()
        
        # Finish progress indication
        self.loading_states[operation_id] = False
        self.set_ui_loading_state(False, operation_id)
        
        if self.progress_manager:
            self.progress_manager.finish_operation(operation_id, True, "New exercises generated successfully!")
        else:
            self.updateStatus("New exercises generated.")
            
        logger.info("New exercises generated successfully.")

    def updateExercise(self) -> None:
        if self.total_exercises == 0 or self.current_exercise < 0 or self.current_exercise >= self.total_exercises:
            return
        exercise = self.exercises[self.current_exercise]
        if "context" in exercise and exercise["context"]:
            full_text = exercise["context"] + "\n\n" + exercise.get("sentence", "")
        else:
            full_text = exercise.get("sentence", "")
        self.sentence_label.setText(full_text)
        self.sentence_label.adjustSize()
        self.sentence_label.update()
        if self.show_translation and "translation" in exercise:
            self.translation_label.setText(exercise["translation"])
        else:
            self.translation_label.setText("")
        self.translation_label.adjustSize()
        self.translation_label.update()
        self.feedback_text.clear()
        self.progress_bar.setValue(self.current_exercise + 1)
        self.updateStatus(f"Exercise {self.current_exercise + 1} of {self.total_exercises}")
        mode = self.mode_combo.currentText()
        if mode == "Free Response":
            self.input_stack.setCurrentIndex(0)
            self.free_response_input.clear()
            self.free_response_input.update()
        elif mode == "Multiple Choice":
            self.input_stack.setCurrentIndex(1)
            choices = list(exercise["choices"])
            random.shuffle(choices)
            self.populateMultipleChoice(choices)
        self.updateStats()
        self.repaint()

    def switchMode(self, force=None):
        mode = self.mode_combo.currentText()
        if force == "Free":
            self.input_stack.setCurrentIndex(0)
        elif force == "MC":
            self.input_stack.setCurrentIndex(1)
        else:
            self.input_stack.setCurrentIndex(0 if mode == "Free Response" else 1)

    def populateMultipleChoice(self, choices: List[str]) -> None:
        while self.mc_options_layout.count():
            item = self.mc_options_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.mc_button_group = QButtonGroup()
        for choice in choices:
            radio = QRadioButton(choice)
            self.mc_button_group.addButton(radio)
            self.mc_options_layout.addWidget(radio)
        self.mc_options_layout.addStretch()
        buttons = self.mc_button_group.buttons()
        if buttons:
            buttons[0].setChecked(True)
        current_widget = self.input_stack.currentWidget()
        current_widget.adjustSize()
        current_widget.update()
        current_widget.repaint()

    def getUserAnswer(self):
        mode = self.mode_combo.currentText()
        if mode == "Free Response":
            answer = self.free_response_input.text().strip()
            # Input validation
            if len(answer) > 100:
                QMessageBox.warning(self, "Input Too Long", "Answer must be less than 100 characters.")
                return ""
            # Remove potentially harmful characters
            answer = re.sub(r'[<>"\']', '', answer)
            return answer.lower()
        else:
            for btn in self.mc_button_group.buttons():
                if btn.isChecked():
                    return btn.text().strip().lower()
        return ""
    
    def getCurrentInputWidget(self):
        """Get the currently active input widget for styling purposes"""
        mode = self.mode_combo.currentText()
        if mode == "Free Response":
            return self.free_response_input
        else:
            # For multiple choice, return the checked radio button or the first one
            for btn in self.mc_button_group.buttons():
                if btn.isChecked():
                    return btn
            # If no button is checked, return the first one
            buttons = self.mc_button_group.buttons()
            return buttons[0] if buttons else None

    def submitAnswer(self):
        if self.total_exercises == 0:
            self.updateStatus("No exercises available. Generate new ones first.")
            return
        user_answer = self.getUserAnswer()
        if not user_answer:
            self.updateStatus("Please provide an answer.")
            return
        exercise = self.exercises[self.current_exercise]
        correct_answer = exercise.get("answer", "").strip().lower()
        
        # Update session stats
        self.session_stats["total_attempts"] += 1
        selected_tenses = self.getSelectedTenses()
        selected_persons = self.getSelectedPersons()
        self.session_stats["tenses_practiced"].update(selected_tenses)
        self.session_stats["persons_practiced"].update(selected_persons)
        
        if user_answer == correct_answer:
            is_correct = True
            base_feedback = "Correct! Excellent use of the subjunctive."
            self.correct_count += 1
            self.session_stats["correct_attempts"] += 1
            
            # Apply success styling to input field
            if self.form_integration_manager:
                current_input = self.getCurrentInputWidget()
                if current_input:
                    self.form_integration_manager.set_form_validation_state(
                        current_input, 'success', 'Correct answer!'
                    )
        else:
            is_correct = False
            base_feedback = f"Incorrect. The correct answer is '{correct_answer}'."
            
            # Apply error styling to input field (gentle, not harsh red)
            if self.form_integration_manager:
                current_input = self.getCurrentInputWidget()
                if current_input:
                    self.form_integration_manager.set_form_validation_state(
                        current_input, 'error', f'Correct answer: {correct_answer}'
                    )
            
            # Analyze the error
            error_analysis = self.error_analyzer.analyze_error(
                user_answer, 
                correct_answer,
                {"trigger": exercise.get("context", ""), "tense": selected_tenses[0] if selected_tenses else ""}
            )
            
            if error_analysis["suggestion"]:
                base_feedback += f"\n💡 Tip: {error_analysis['suggestion']}"
        
        # Track with session manager
        self.session_manager.add_exercise_result(exercise, user_answer, is_correct)
        
        # Check for achievements
        new_achievements = self.practice_goals.check_achievement(
            "total_exercises", 
            self.session_stats["total_attempts"]
        )
        if new_achievements:
            QMessageBox.information(self, "Achievement Unlocked!", 
                f"🏆 You earned: {', '.join(new_achievements)}")
        
        sentence_for_gpt = exercise.get("sentence", "")
        
        # Start progress indication for answer explanation
        operation_id = 'checking_answer'
        self.loading_states[operation_id] = True
        
        if self.progress_manager:
            loading_msg = create_api_loading_message(operation_id)
            self.progress_manager.start_operation(operation_id, loading_msg)
        
        # Set UI loading state
        self.set_ui_loading_state(True, operation_id)
        
        self.generateGPTExplanationAsync(user_answer, correct_answer, is_correct, sentence_for_gpt, base_feedback, operation_id)
        logger.info("Submitted answer '%s' for exercise %d", user_answer, self.current_exercise + 1)

    def generateGPTExplanationAsync(self, user_ans: str, correct_ans: str, is_correct: bool, sentence: str, base_feedback: str, operation_id: str = 'checking_answer'):
        difficulty = self.difficulty_combo.currentText()
        task_type = self.current_task_type
        
        # Add pedagogical context based on task type
        if task_type == "tblt":
            pedagogical_focus = "Focus on the COMMUNICATIVE FUNCTION and how the subjunctive helps achieve the communicative goal."
        elif task_type == "contrast":
            pedagogical_focus = "Emphasize the MOOD DISTINCTION and why this context requires subjunctive vs indicative."
        else:
            pedagogical_focus = "Explain the GRAMMATICAL RULE and provide the pattern for similar cases."
        
        prompt = f"""Explain why {"✓" if is_correct else "✗"} for Spanish subjunctive.
Sentence: "{sentence}"
User: {user_ans} | Correct: {correct_ans}

{pedagogical_focus}
Give brief explanation in Spanish with example. 50 words max."""
        worker = GPTWorkerRunnable(prompt, max_tokens=150, temperature=0.5)
        worker.signals.result.connect(lambda result: self.handleExplanationResult(result, base_feedback, operation_id))
        self.threadpool.start(worker)
        logging.info("Generating explanation with prompt: %s", prompt)

    def handleExplanationResult(self, gpt_response: str, base_feedback: str, operation_id: str = 'checking_answer'):
        # Check if response is an error message
        if any(error_keyword in gpt_response.lower() for error_keyword in 
               ['error', 'failed', 'connection', 'timeout', 'authentication', 'rate limit', 'unavailable']):
            # Show base feedback only and indicate explanation failed
            full_feedback = base_feedback + "\n\n⚠️ Could not generate detailed explanation: " + gpt_response
        else:
            full_feedback = base_feedback + "\n\n" + gpt_response
        self.feedback_text.setText(full_feedback)
        self.responses.append({
            "exercise_index": self.current_exercise,
            "sentence": self.exercises[self.current_exercise].get("sentence", ""),
            "translation": self.exercises[self.current_exercise].get("translation", ""),
            "user_answer": self.getUserAnswer(),
            "correct": base_feedback.startswith("Correct"),
            "explanation": gpt_response
        })
        self.updateStats()
        
        # Finish progress indication
        self.loading_states[operation_id] = False
        self.set_ui_loading_state(False, operation_id)
        
        if self.progress_manager:
            self.progress_manager.finish_operation(operation_id, True, "Answer explanation ready")
        
        logging.info("Explanation provided for exercise %d", self.current_exercise + 1)

    def provideHint(self):
        if self.total_exercises == 0:
            self.updateStatus("No exercise available.")
            return
        
        # Update hint stats
        self.session_stats["hints_used"] += 1
        
        exercise = self.exercises[self.current_exercise]
        sentence = exercise.get("sentence", "")
        correct_ans = exercise.get("answer", "")
        hint_prompt = (
            "You are an expert Spanish tutor focusing on the subjunctive. "
            f"Sentence: \"{sentence}\"\n"
            f"Correct Subjunctive Form: {correct_ans}\n\n"
            "Provide a subtle hint in Spanish that nudges the student toward the correct subjunctive form, "
            "without revealing the answer directly."
        )
        # Start progress indication for hint
        operation_id = 'getting_hint'
        self.loading_states[operation_id] = True
        
        if self.progress_manager:
            loading_msg = create_api_loading_message(operation_id)
            self.progress_manager.start_operation(operation_id, loading_msg)
        
        # Set UI loading state
        self.set_ui_loading_state(True, operation_id)
        
        worker = GPTWorkerRunnable(hint_prompt, max_tokens=100, temperature=0.5)
        worker.signals.result.connect(lambda result: self.handleHintResult(result, operation_id))
        self.threadpool.start(worker)
        logging.info("Providing hint for exercise %d", self.current_exercise + 1)

    def handleHintResult(self, result: str, operation_id: str = 'getting_hint'):
        # Check if result is an error message
        if any(error_keyword in result.lower() for error_keyword in 
               ['error', 'failed', 'connection', 'timeout', 'authentication', 'rate limit', 'unavailable']):
            self.feedback_text.setText("❌ Unable to get hint: " + result)
        else:
            self.feedback_text.setText("💡 Hint: " + result)
        
        # Finish progress indication
        self.loading_states[operation_id] = False
        self.set_ui_loading_state(False, operation_id)
        
        if self.progress_manager:
            self.progress_manager.finish_operation(operation_id, True, "Hint provided")
        else:
            self.updateStatus("Hint provided.")
            
        logging.info("Hint provided: %s", result)

    def nextExercise(self):
        if self.total_exercises == 0:
            self.updateStatus("No exercises available. Generate new ones first.")
            return
        if self.current_exercise < self.total_exercises - 1:
            # Clear validation styling from current input
            if self.form_integration_manager:
                current_input = self.getCurrentInputWidget()
                if current_input:
                    self.form_integration_manager.set_form_validation_state(
                        current_input, 'neutral', ''
                    )
            
            self.current_exercise += 1
            self.updateExercise()
            logging.info("Moved to next exercise: %d", self.current_exercise + 1)
        else:
            self.updateStatus("You are at the last exercise.")
            logging.info("Already at the last exercise.")
        self.updateStats()

    def prevExercise(self):
        if self.total_exercises == 0:
            self.updateStatus("No exercises available.")
            return
        if self.current_exercise > 0:
            # Clear validation styling from current input
            if self.form_integration_manager:
                current_input = self.getCurrentInputWidget()
                if current_input:
                    self.form_integration_manager.set_form_validation_state(
                        current_input, 'neutral', ''
                    )
            
            self.current_exercise -= 1
            self.updateExercise()
            logging.info("Moved to previous exercise: %d", self.current_exercise + 1)
        else:
            self.updateStatus("You are at the first exercise.")
            logging.info("Already at the first exercise.")
        self.updateStats()

    def startReviewMode(self):
        """Start review mode for incorrect answers"""
        review_items = self.session_manager.get_review_items()
        
        if not review_items:
            QMessageBox.information(self, "Review Mode", "No items to review! Great job!")
            return
        
        self.review_mode = True
        self.updateStatus(f"Review mode: {len(review_items)} items to review")
        
        # Convert review items to exercise format
        self.exercises = []
        for item in review_items:
            exercise = {
                "context": f"REVIEW: {item.get('context', '')}",
                "sentence": item["sentence"],
                "answer": item["correct_answer"],
                "choices": self._generate_choices_for_review(item["correct_answer"], item["user_answer"]),
                "translation": f"You answered: {item['user_answer']} | Correct: {item['correct_answer']}",
                "review_item": True
            }
            self.exercises.append(exercise)
        
        self.total_exercises = len(self.exercises)
        self.current_exercise = 0
        self.updateExercise()
        self.updateStats()
    
    def _generate_choices_for_review(self, correct: str, incorrect: str) -> List[str]:
        """Generate multiple choice options for review"""
        choices = [correct, incorrect]
        # Add two more plausible distractors
        if "que" in correct:
            choices.append(correct.replace("que", "qu"))
            choices.append(correct.replace("a", "e") if "a" in correct else correct.replace("e", "a"))
        else:
            choices.append(correct + "s")
            choices.append(correct[:-1] if len(correct) > 3 else correct + "r")
        
        return choices[:4]  # Ensure only 4 choices
    
    def saveProgress(self):
        """Save current session progress"""
        try:
            filepath = self.session_manager.save_session()
            QMessageBox.information(self, "Progress Saved", f"Session saved successfully!\n{filepath}")
            self.updateStatus("Progress saved")
            logger.info(f"Session saved to {filepath}")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Failed to save progress: {str(e)}")
            logger.error(f"Failed to save session: {e}")
    
    def loadProgress(self):
        """Load a previous session"""
        from PyQt5.QtWidgets import QFileDialog
        
        filename, _ = QFileDialog.getOpenFileName(
            self, 
            "Load Session", 
            "user_data",
            "JSON Files (*.json)"
        )
        
        if filename:
            try:
                session_data = self.session_manager.load_session(os.path.basename(filename))
                # Restore session state
                self.responses = session_data.get("responses", [])
                self.correct_count = session_data.get("correct_answers", 0)
                self.updateStatus("Session loaded successfully")
                logger.info(f"Session loaded from {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Load Error", f"Failed to load session: {str(e)}")
                logger.error(f"Failed to load session: {e}")
    
    def resetProgress(self):
        self.current_exercise = 0
        self.correct_count = 0
        self.responses.clear()
        self.updateExercise()
        self.updateStatus("Progress reset.")
        self.updateStats()
        logging.info("Progress reset.")

    def generateSessionSummary(self):
        if not self.responses:
            QMessageBox.information(self, "Summary", "No data to summarize yet.")
            return
        session_data = "\n".join(
            f"Exercise {r['exercise_index']+1} - Sentence: {r['sentence']}\n"
            f"  Your answer: {r['user_answer']} | Correct: {r['correct']}\n"
            f"  Explanation: {r['explanation']}\n"
            for r in self.responses
        )
        summary_prompt = (
            "You are an expert Spanish tutor summarizing a student's practice on Spanish subjunctive. "
            "Here are the details:\n"
            f"{session_data}\n\n"
            "Please provide a concise summary in Spanish that highlights strengths, correct uses of the subjunctive, "
            "common errors, and suggestions for improvement. Avoid being overly long or repetitive."
        )
        # Start progress indication for summary
        operation_id = 'generating_summary'
        self.loading_states[operation_id] = True
        
        if self.progress_manager:
            loading_msg = create_api_loading_message(operation_id)
            self.progress_manager.start_operation(operation_id, loading_msg)
        
        # Set UI loading state
        self.set_ui_loading_state(True, operation_id)
        
        worker = GPTWorkerRunnable(summary_prompt, max_tokens=200, temperature=0.5)
        worker.signals.result.connect(lambda result: self.handleSummaryResult(result, operation_id))
        self.threadpool.start(worker)
        logging.info("Generating session summary.")

    def handleSummaryResult(self, result: str, operation_id: str = 'generating_summary'):
        # Check if result is an error message
        if any(error_keyword in result.lower() for error_keyword in 
               ['error', 'failed', 'connection', 'timeout', 'authentication', 'rate limit', 'unavailable']):
            QMessageBox.critical(self, "Summary Generation Failed", f"Could not generate session summary:\n\n{result}")
        else:
            QMessageBox.information(self, "Session Summary", result)
        
        # Finish progress indication
        self.loading_states[operation_id] = False
        self.set_ui_loading_state(False, operation_id)
        
        if self.progress_manager:
            self.progress_manager.finish_operation(operation_id, True, "Session summary generated")
        else:
            self.updateStatus("Session summary generated.")
            
        logging.info("Session summary generated.")

    def exportSession(self):
        """Export session data to CSV file"""
        if not self.responses:
            QMessageBox.warning(self, "No Data", "No session data to export.")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"subjunctive_session_{timestamp}.csv"
        
        try:
            import csv
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Exercise', 'Sentence', 'Translation', 'Your Answer', 'Correct Answer', 'Result', 'Explanation']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for r in self.responses:
                    exercise = self.exercises[r['exercise_index']]
                    writer.writerow({
                        'Exercise': r['exercise_index'] + 1,
                        'Sentence': r['sentence'],
                        'Translation': r['translation'],
                        'Your Answer': r['user_answer'],
                        'Correct Answer': exercise.get('answer', ''),
                        'Result': 'Correct' if r['correct'] else 'Incorrect',
                        'Explanation': r['explanation']
                    })
            
            QMessageBox.information(self, "Export Successful", f"Session exported to {filename}")
            self.updateStatus(f"Session exported to {filename}")
            logger.info(f"Session exported to {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", f"Failed to export: {str(e)}")
            logger.error(f"Export failed: {e}")
    
    def showDetailedStats(self):
        """Show detailed statistics in a message box"""
        if self.session_stats["total_attempts"] == 0:
            QMessageBox.information(self, "Statistics", "No statistics available yet. Start practicing!")
            return
        
        session_duration = (datetime.now() - self.session_stats["session_start"]).total_seconds() / 60
        accuracy = (self.session_stats["correct_attempts"] / self.session_stats["total_attempts"]) * 100
        
        stats_text = f"""Session Statistics
═══════════════════

Duration: {session_duration:.1f} minutes
Total Attempts: {self.session_stats["total_attempts"]}
Correct: {self.session_stats["correct_attempts"]}
Accuracy: {accuracy:.1f}%
Hints Used: {self.session_stats["hints_used"]}

Tenses Practiced:
{', '.join(self.session_stats["tenses_practiced"]) if self.session_stats["tenses_practiced"] else 'None'}

Persons Practiced:
{', '.join(self.session_stats["persons_practiced"]) if self.session_stats["persons_practiced"] else 'None'}

Average Time per Exercise: {session_duration / max(self.session_stats["total_attempts"], 1):.1f} min
"""
        
        QMessageBox.information(self, "Detailed Statistics", stats_text)
        logger.info("Detailed stats viewed")
    
    def showConjugationReference(self):
        """Show quick conjugation reference dialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Subjunctive Conjugation Reference")
        dialog.setMinimumSize(800, 600)
        
        layout = QVBoxLayout(dialog)
        
        # Create tabs for different tenses
        from PyQt5.QtWidgets import QTabWidget
        tabs = QTabWidget()
        
        # Present Subjunctive tab
        present_tab = self._createConjugationTable(
            "Present Subjunctive",
            {
                "Regular -AR": ["hable", "hables", "hable", "hablemos", "habléis", "hablen"],
                "Regular -ER": ["coma", "comas", "coma", "comamos", "comáis", "coman"],
                "Regular -IR": ["viva", "vivas", "viva", "vivamos", "viváis", "vivan"],
                "Irregular SER": ["sea", "seas", "sea", "seamos", "seáis", "sean"],
                "Irregular ESTAR": ["esté", "estés", "esté", "estemos", "estéis", "estén"],
                "Irregular HABER": ["haya", "hayas", "haya", "hayamos", "hayáis", "hayan"]
            }
        )
        tabs.addTab(present_tab, "Present")
        
        # Imperfect Subjunctive tab
        imperfect_tab = self._createConjugationTable(
            "Imperfect Subjunctive (-ra)",
            {
                "Regular -AR": ["hablara", "hablaras", "hablara", "habláramos", "hablarais", "hablaran"],
                "Regular -ER": ["comiera", "comieras", "comiera", "comiéramos", "comierais", "comieran"],
                "Regular -IR": ["viviera", "vivieras", "viviera", "viviéramos", "vivierais", "vivieran"],
                "Irregular SER": ["fuera", "fueras", "fuera", "fuéramos", "fuerais", "fueran"],
                "Irregular TENER": ["tuviera", "tuvieras", "tuviera", "tuviéramos", "tuvierais", "tuvieran"]
            }
        )
        tabs.addTab(imperfect_tab, "Imperfect")
        
        # Common triggers tab
        triggers_widget = QTextEdit()
        triggers_widget.setReadOnly(True)
        triggers_text = """
COMMON SUBJUNCTIVE TRIGGERS:

Wishes & Desires:
• querer que - to want that
• esperar que - to hope that
• desear que - to wish that
• ojalá (que) - hopefully/I hope that

Emotions:
• alegrarse de que - to be happy that
• sentir que - to feel sorry that
• temer que - to fear that
• gustar que - to like that

Doubt & Denial:
• dudar que - to doubt that
• no creer que - to not believe that
• negar que - to deny that
• no es cierto que - it's not certain that

Impersonal Expressions:
• es necesario que - it's necessary that
• es importante que - it's important that
• es posible que - it's possible that
• es mejor que - it's better that

Conjunctions:
• para que - so that
• antes de que - before
• a menos que - unless
• sin que - without
"""
        triggers_widget.setText(triggers_text)
        tabs.addTab(triggers_widget, "Triggers")
        
        layout.addWidget(tabs)
        
        # Close button
        close_btn = QPushButton("Close (Esc)")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.exec_()
    
    def _createConjugationTable(self, title: str, conjugations: dict) -> QWidget:
        """Create a conjugation table widget"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        table = QTableWidget()
        table.setRowCount(6)  # 6 persons
        table.setColumnCount(len(conjugations))
        
        # Set headers
        table.setHorizontalHeaderLabels(list(conjugations.keys()))
        table.setVerticalHeaderLabels(["yo", "tú", "él/ella/usted", "nosotros", "vosotros", "ellos/ellas/ustedes"])
        
        # Fill data
        for col, (verb_type, forms) in enumerate(conjugations.items()):
            for row, form in enumerate(forms):
                item = QTableWidgetItem(form)
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(row, col, item)
        
        # Adjust column widths
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(QLabel(f"<b>{title}</b>"))
        layout.addWidget(table)
        
        return widget
    
    def showGoalsDialog(self):
        """Show goals and progress dialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Practice Goals & Progress")
        dialog.setMinimumSize(500, 400)
        
        layout = QVBoxLayout(dialog)
        
        # Current goals
        goals_group = QGroupBox("Current Goals")
        goals_layout = QVBoxLayout(goals_group)
        
        goals_text = f"""
📊 Practice Goals:
• Daily exercises: {self.practice_goals.goals['daily_exercises']}
• Target accuracy: {self.practice_goals.goals['target_accuracy']}%
• Weekly minutes: {self.practice_goals.goals['weekly_minutes']}

🏆 Achievements:
{chr(10).join(f"• {achievement}" for achievement in self.practice_goals.goals['achievements']) if self.practice_goals.goals['achievements'] else "• No achievements yet - keep practicing!"}

📈 Progress Report:
{self._get_progress_summary()}
"""
        goals_label = QLabel(goals_text)
        goals_layout.addWidget(goals_label)
        layout.addWidget(goals_group)
        
        # Weakness report
        weakness_report = self.error_analyzer.get_weakness_report()
        if weakness_report["weaknesses"]:
            weakness_group = QGroupBox("Areas for Improvement")
            weakness_layout = QVBoxLayout(weakness_group)
            
            weakness_text = "Focus on these areas:\n"
            for weakness in weakness_report["weaknesses"]:
                weakness_text += f"• {weakness['type']} (frequency: {weakness['frequency']})\n"
            
            weakness_text += "\nSuggestions:\n"
            for suggestion in weakness_report["suggestions"]:
                weakness_text += f"💡 {suggestion}\n"
            
            weakness_label = QLabel(weakness_text)
            weakness_layout.addWidget(weakness_label)
            layout.addWidget(weakness_group)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.close)
        layout.addWidget(close_btn)
        
        dialog.exec_()
    
    def _get_progress_summary(self) -> str:
        """Get a summary of current progress"""
        stats = self.session_manager.get_statistics()
        streak_info = self.streak_tracker.get_streak_info()
        
        return f"""
• Session accuracy: {stats['accuracy']:.1f}%
• Current streak: {streak_info['current']} days
• Total practice days: {streak_info['total_days']}
• Items mastered: {stats.get('mastered_items', 0)}
• Items to review: {stats.get('items_to_review', 0)}
"""
    
    def showAPIHealthDialog(self):
        """Show API health status and performance metrics"""
        dialog = QDialog(self)
        dialog.setWindowTitle("OpenAI API Health Status")
        dialog.setMinimumSize(600, 500)
        
        layout = QVBoxLayout(dialog)
        
        # Create scrollable text area for health information
        health_text = QTextEdit()
        health_text.setReadOnly(True)
        health_text.setFont(QFont("Consolas", 10))  # Monospace font for better formatting
        
        try:
            if API_MODULE_AVAILABLE:
                # Get comprehensive health status
                health_status = get_health_status()
                api_metrics = get_api_metrics()
                
                health_info = f"""
🔧 OpenAI API Health Monitor
═══════════════════════════════════════════════════════

📊 OVERALL STATUS: {health_status['overall_health'].upper()}
🌐 API Available: {'✅ Yes' if health_status['available'] else '❌ No'}
🔑 API Key Valid: {'✅ Yes' if health_status['api_key_valid'] else '❌ No'}
📦 OpenAI Library: {'✅ Available' if health_status['openai_library_available'] else '❌ Missing'}

🏥 HEALTH METRICS
═══════════════════════════════════════════════════════
• Success Rate: {health_status['success_rate']:.1f}%
• Average Response Time: {health_status['average_response_time']:.2f}s
• Total Requests: {health_status['total_requests']}
• Uptime: {health_status['uptime_hours']:.1f} hours

🔄 REQUEST STATISTICS
═══════════════════════════════════════════════════════
• Successful Requests: {api_metrics.get('successful_requests', 0)}
• Failed Requests: {api_metrics.get('failed_requests', 0)}
• Rate Limit Hits: {api_metrics.get('rate_limit_hits', 0)}
• Circuit Breaker Open: {'⚠️  Yes' if api_metrics.get('circuit_breaker_open', False) else '✅ No'}
• Circuit Breaker Failures: {api_metrics.get('circuit_breaker_failures', 0)}

⚡ RATE LIMITING
═══════════════════════════════════════════════════════
• Available Tokens: {api_metrics.get('rate_limiter_tokens', 0):.1f}
• Status: {api_metrics.get('status', 'unknown').title()}

🕒 TIMING INFORMATION  
═══════════════════════════════════════════════════════
• Last Request: {api_metrics.get('last_request_time', 'Never')}
• Last Error: {api_metrics.get('last_error', 'None')}
• Timestamp: {health_status['timestamp']}

💡 RECOMMENDATIONS
═══════════════════════════════════════════════════════
"""
                
                # Add recommendations based on status
                if not health_status['available']:
                    health_info += "• ❌ API is unavailable. Check your internet connection and API key.\n"
                if not health_status['api_key_valid']:
                    health_info += "• 🔑 Update your API key in the .env file.\n"
                if health_status['success_rate'] < 80:
                    health_info += "• ⚠️  Low success rate. Check network stability.\n"
                if api_metrics.get('circuit_breaker_open', False):
                    health_info += "• 🔄 Circuit breaker is open. Wait for automatic recovery.\n"
                if api_metrics.get('rate_limit_hits', 0) > 5:
                    health_info += "• 🚦 Frequent rate limiting. Consider reducing request frequency.\n"
                if health_status['success_rate'] >= 95 and health_status['available']:
                    health_info += "• ✅ API is performing excellently!\n"
                
            else:
                health_info = f"""
🔧 OpenAI API Health Monitor
═══════════════════════════════════════════════════════

⚠️  BASIC MODE ACTIVE
The enhanced API configuration module is not available.
Using basic OpenAI integration.

📦 OpenAI Library: {'✅ Available' if client else '❌ Missing or Invalid'}
🔑 API Key: {'✅ Configured' if client else '❌ Not Set'}

💡 RECOMMENDATIONS
═══════════════════════════════════════════════════════
• Install enhanced API module for better monitoring
• Check that your .env file contains OPENAI_API_KEY
• Ensure OpenAI library is installed: pip install openai
"""
            
            health_text.setText(health_info)
            
        except Exception as e:
            health_text.setText(f"""
❌ ERROR RETRIEVING API HEALTH STATUS

Error Details: {str(e)}

This may indicate:
• API configuration module issues
• Missing dependencies  
• Network connectivity problems

Please check the application logs for more details.
""")
        
        layout.addWidget(health_text)
        
        # Add action buttons
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(lambda: self.showAPIHealthDialog())
        refresh_btn.setToolTip("Refresh API health status")
        
        test_btn = QPushButton("🧪 Test API")
        test_btn.clicked.connect(lambda: self.testAPIConnection(health_text))
        test_btn.setToolTip("Send a test request to verify API functionality")
        
        close_btn = QPushButton("✅ Close")
        close_btn.clicked.connect(dialog.close)
        close_btn.setToolTip("Close health monitor")
        
        button_layout.addWidget(refresh_btn)
        button_layout.addWidget(test_btn)
        button_layout.addStretch()
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        dialog.exec_()
    
    def testAPIConnection(self, health_text_widget):
        """Test API connection and update health display"""
        # Start progress indication for API test
        operation_id = 'testing_api'
        self.loading_states[operation_id] = True
        
        if self.progress_manager:
            loading_msg = create_api_loading_message(operation_id)
            self.progress_manager.start_operation(operation_id, loading_msg)
        
        try:
            health_text_widget.append("\n🧪 TESTING API CONNECTION...")
            health_text_widget.append("═══════════════════════════════════════════════════════")
            
            # Send a minimal test request
            test_prompt = "Test connection"
            start_time = time.time()
            
            # Update progress
            if self.progress_manager:
                self.progress_manager.update_operation(operation_id, message="Sending test request...")
            
            if API_MODULE_AVAILABLE:
                response = create_chat_completion(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": test_prompt}],
                    max_tokens=5,
                    temperature=0.1
                )
                response_time = time.time() - start_time
                
                if response:
                    health_text_widget.append(f"✅ API CONNECTION SUCCESSFUL")
                    health_text_widget.append(f"• Response Time: {response_time:.2f}s")
                    health_text_widget.append(f"• Response Preview: {response[:50]}...")
                    
                    # Finish progress indication - success
                    self.loading_states[operation_id] = False
                    if self.progress_manager:
                        self.progress_manager.finish_operation(operation_id, True, "API test successful")
                    else:
                        self.updateStatus("API test successful")
                else:
                    health_text_widget.append("❌ API TEST FAILED - No response received")
                    
                    # Finish progress indication - failure
                    self.loading_states[operation_id] = False
                    if self.progress_manager:
                        self.progress_manager.finish_operation(operation_id, False, "API test failed - no response")
                    else:
                        self.updateStatus("API test failed")
                    
            elif client:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": test_prompt}],
                    max_tokens=5,
                    timeout=10
                )
                response_time = time.time() - start_time
                
                if response and response.choices:
                    content = response.choices[0].message.content
                    health_text_widget.append(f"✅ API CONNECTION SUCCESSFUL (Basic Mode)")
                    health_text_widget.append(f"• Response Time: {response_time:.2f}s") 
                    health_text_widget.append(f"• Response Preview: {content[:50]}...")
                    
                    # Finish progress indication - success
                    self.loading_states[operation_id] = False
                    if self.progress_manager:
                        self.progress_manager.finish_operation(operation_id, True, "API test successful")
                    else:
                        self.updateStatus("API test successful")
                else:
                    health_text_widget.append("❌ API TEST FAILED - No response received")
                    
                    # Finish progress indication - failure
                    self.loading_states[operation_id] = False
                    if self.progress_manager:
                        self.progress_manager.finish_operation(operation_id, False, "API test failed - no response")
                    else:
                        self.updateStatus("API test failed")
            else:
                health_text_widget.append("❌ API TEST FAILED - No client available")
                
                # Finish progress indication - failure
                self.loading_states[operation_id] = False
                if self.progress_manager:
                    self.progress_manager.finish_operation(operation_id, False, "API test failed - no client")
                else:
                    self.updateStatus("API test failed - no client")
                
        except Exception as e:
            health_text_widget.append(f"❌ API TEST FAILED")
            health_text_widget.append(f"• Error: {str(e)}")
            
            # Finish progress indication - error
            self.loading_states[operation_id] = False
            if self.progress_manager:
                error_msg = create_error_message(operation_id, str(e))
                self.progress_manager.finish_operation(operation_id, False, error_msg)
            else:
                self.updateStatus(f"API test error: {str(e)}")
        
        # Scroll to bottom to show latest results
        health_text_widget.moveCursor(health_text_widget.textCursor().End)
        
        # Ensure progress state is cleaned up
        if operation_id in self.loading_states and self.loading_states[operation_id]:
            self.loading_states[operation_id] = False
            if self.progress_manager:
                self.progress_manager.finish_operation(operation_id, False, "API test completed")
    
    def keyPressEvent(self, event):
        """Enhanced key press event handling with accessibility support"""
        # Let accessibility manager handle the event first
        if self.accessibility_manager:
            # The accessibility manager's event filter will handle this
            pass
        
        # Call parent implementation
        super().keyPressEvent(event)
    
    def showEvent(self, event):
        """Handle window show event to set proper column proportions"""
        super().showEvent(event)
        
        # Adjust column proportions after window is fully shown
        if not self._initial_column_setup_done:
            # Use QTimer to defer the sizing adjustment
            from PyQt5.QtCore import QTimer
            QTimer.singleShot(100, self._adjust_column_proportions)
            self._initial_column_setup_done = True
    
    def _adjust_column_proportions(self):
        """Adjust splitter column proportions to target values"""
        try:
            if hasattr(self, 'main_splitter'):
                total_width = self.main_splitter.width()
                if total_width > 100:  # Only adjust if we have reasonable width
                    self.main_splitter.setSizes([
                        int(total_width * 0.40),  # 40% for left
                        int(total_width * 0.35),  # 35% for middle
                        int(total_width * 0.25)   # 25% for right
                    ])
        except Exception as e:
            logger.error(f"Error adjusting column proportions: {e}")
    
    def resizeEvent(self, event):
        """Handle window resize to maintain progress overlay positioning"""
        super().resizeEvent(event)
        if self.progress_overlay:
            self.progress_overlay.resize(self.size())
    
    def closeEvent(self, event):
        # Cancel any ongoing operations before closing
        for operation in list(self.loading_states.keys()):
            if self.loading_states[operation]:
                if self.progress_manager:
                    self.progress_manager.cancel_operation(operation)
                self.loading_states[operation] = False
        
        try:
            with open("subjunctive_session_log.txt", "a", encoding="utf-8") as f:
                f.write("\n=== Subjunctive Session Log ===\n")
                for r in self.responses:
                    f.write(
                        f"Exercise {r['exercise_index']+1}\n"
                        f"  Sentence: {r['sentence']}\n"
                        f"  Translation: {r['translation']}\n"
                        f"  User answer: {r['user_answer']}\n"
                        f"  Correct: {r['correct']}\n"
                        f"  Explanation: {r['explanation']}\n\n"
                    )
                f.write("=== End of Session ===\n\n")
            logging.info("Subjunctive practice session log saved.")
        except Exception as e:
            logging.error("Error writing log: %s", e)
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Initialize modern visual design system - COMMENTED OUT FOR ROLLBACK
    # if initialize_modern_ui:
    #     try:
    #         style_manager = initialize_modern_ui(app)
    #         logger.info("Modern UI theme initialized successfully")
    #     except Exception as e:
    #         logger.warning(f"Failed to initialize modern UI: {e}")
    #         style_manager = None
    # else:
    style_manager = None
    logger.info("Using basic UI styling - rollback mode")
    
    window = SpanishSubjunctivePracticeGUI()
    
    # Assign style manager to window for theme control - COMMENTED OUT FOR ROLLBACK
    # if style_manager:
    #     window.style_manager = style_manager
    
    # Apply responsive design integration - COMMENTED OUT FOR ROLLBACK
    # if RESPONSIVE_DESIGN_AVAILABLE and quick_responsive_integration:
    #     try:
    #         responsive_integration = quick_responsive_integration(window)
    #         window.responsive_integration = responsive_integration
    #         logger.info("Responsive design system integrated successfully")
    #     except Exception as e:
    #         logger.warning(f"Failed to integrate responsive design: {e}")
    
    window.show()
    sys.exit(app.exec_())

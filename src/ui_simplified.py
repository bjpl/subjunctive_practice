"""
Simplified Spanish Subjunctive Practice UI

A streamlined version of the main UI that focuses on essential functionality
while reducing cognitive load and eliminating redundant elements.

Key simplifications:
1. Combined tense/person selection into preset patterns
2. Consolidated toolbar with essential actions only
3. Simplified task type selection (Traditional/Communicative only)
4. Streamlined feedback display
5. Reduced layout complexity with single column design
6. Essential navigation controls only
"""

import sys
import os
import json
import random
import logging
from typing import List, Dict
from datetime import datetime
from tblt_scenarios import TBLTTaskGenerator, SpacedRepetitionTracker
from session_manager import SessionManager
from learning_analytics import StreakTracker, ErrorAnalyzer, AdaptiveDifficulty
from dotenv import load_dotenv
import re

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QProgressBar, QTextEdit,
    QRadioButton, QButtonGroup, QStatusBar, QAction, QGroupBox,
    QMessageBox, QToolBar, QComboBox, QSizePolicy, QDialog
)
from PyQt5.QtCore import Qt, QRunnable, QObject, pyqtSignal, QThreadPool

from openai import OpenAI

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Initialize OpenAI client
client = None
try:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key.startswith("sk-"):
        client = OpenAI(api_key=api_key)
        logger.info("OpenAI client initialized")
except Exception as e:
    logger.error("Failed to initialize OpenAI client: %s", str(e))

# Worker class for async GPT calls
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
                        "content": "You are an expert Spanish tutor specializing in LATAM Spanish. "
                                  "Provide clear, concise explanations using real-life examples."
                    },
                    {"role": "user", "content": self.prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                timeout=30
            )
            output = response.choices[0].message.content.strip()
            logger.info("GPT response received")
        except Exception as e:
            output = f"Error: {str(e)}"
            logger.error("Error in GPT call: %s", str(e))
        self.signals.result.emit(output)


class SimplifiedSubjunctivePracticeGUI(QMainWindow):
    """
    Simplified Spanish Subjunctive Practice Interface
    
    Key simplifications:
    - Preset learning patterns instead of granular controls
    - Essential toolbar actions only
    - Single-column layout for clarity
    - Consolidated feedback display
    """
    
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Spanish Subjunctive Practice - Simplified")
        self.setGeometry(100, 100, 800, 600)
        
        # Apply clean, minimal styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            QWidget {
                background-color: #ffffff;
                color: #2c3e50;
                font-size: 14px;
            }
            
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                margin: 10px;
                padding-top: 15px;
                background-color: #ffffff;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px;
                color: #495057;
                background-color: #ffffff;
            }
            
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 16px;
                font-weight: 500;
                margin: 4px;
                min-height: 14px;
            }
            
            QPushButton:hover {
                background-color: #0056b3;
            }
            
            QPushButton:pressed {
                background-color: #004085;
            }
            
            QPushButton:disabled {
                background-color: #6c757d;
                color: #adb5bd;
            }
            
            QLineEdit, QTextEdit {
                border: 2px solid #ced4da;
                border-radius: 4px;
                padding: 8px;
                background-color: #ffffff;
                font-size: 14px;
            }
            
            QLineEdit:focus, QTextEdit:focus {
                border-color: #007bff;
                outline: none;
            }
            
            QComboBox {
                border: 2px solid #ced4da;
                border-radius: 4px;
                padding: 6px 10px;
                background-color: #ffffff;
                min-width: 120px;
            }
            
            QComboBox:focus {
                border-color: #007bff;
            }
            
            QRadioButton {
                padding: 8px;
                margin: 4px;
                font-size: 14px;
            }
            
            QProgressBar {
                border: 2px solid #e9ecef;
                border-radius: 4px;
                background-color: #f8f9fa;
                text-align: center;
                font-weight: bold;
                height: 20px;
            }
            
            QProgressBar::chunk {
                background-color: #28a745;
                border-radius: 2px;
            }
            
            QStatusBar {
                background-color: #f8f9fa;
                border-top: 1px solid #dee2e6;
                color: #6c757d;
                font-size: 12px;
            }
        """)
        
        # Initialize data structures
        self.exercises: List[dict] = []
        self.current_exercise: int = 0
        self.total_exercises: int = 0
        self.correct_count: int = 0
        self.responses: List[dict] = []
        self.session_stats = {
            "total_attempts": 0,
            "correct_attempts": 0,
            "session_start": datetime.now()
        }
        
        # Initialize components
        self.threadpool = QThreadPool()
        self.tblt_generator = TBLTTaskGenerator()
        self.session_manager = SessionManager()
        self.streak_tracker = StreakTracker()
        self.error_analyzer = ErrorAnalyzer()
        self.adaptive_difficulty = AdaptiveDifficulty()
        
        # Current settings
        self.practice_mode = "traditional"  # traditional or communicative
        self.difficulty_level = "intermediate"
        self.selected_pattern = "present_common"  # Preset pattern
        
        self.initUI()
        self.check_daily_streak()
        
    def initUI(self) -> None:
        """Initialize the simplified user interface"""
        # Create toolbar with essential actions only
        self.createSimplifiedToolBar()
        
        # Main container
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Exercise display section
        exercise_group = QGroupBox("Current Exercise")
        exercise_layout = QVBoxLayout(exercise_group)
        
        self.sentence_label = QLabel("Generate exercises to begin practicing!")
        self.sentence_label.setWordWrap(True)
        self.sentence_label.setStyleSheet("font-size: 16px; color: #495057; padding: 10px;")
        exercise_layout.addWidget(self.sentence_label)
        
        self.translation_label = QLabel("")
        self.translation_label.setWordWrap(True)
        self.translation_label.setStyleSheet("color: #6c757d; font-style: italic; padding: 0 10px;")
        self.translation_label.setVisible(False)
        exercise_layout.addWidget(self.translation_label)
        
        layout.addWidget(exercise_group)
        
        # Simplified practice settings
        settings_group = QGroupBox("Practice Settings")
        settings_layout = QHBoxLayout(settings_group)
        
        # Practice mode selector
        mode_label = QLabel("Mode:")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Traditional Grammar", "Real-World Communication"])
        self.mode_combo.currentTextChanged.connect(self.onModeChanged)
        
        # Difficulty selector
        difficulty_label = QLabel("Level:")
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Beginner", "Intermediate", "Advanced"])
        self.difficulty_combo.setCurrentText("Intermediate")
        
        # Pattern selector (simplified presets)
        pattern_label = QLabel("Focus:")
        self.pattern_combo = QComboBox()
        self.pattern_combo.addItems([
            "Present + Common Triggers",
            "Past + Emotions",
            "All Tenses + Mixed",
            "Review Mistakes"
        ])
        
        settings_layout.addWidget(mode_label)
        settings_layout.addWidget(self.mode_combo)
        settings_layout.addWidget(difficulty_label)
        settings_layout.addWidget(self.difficulty_combo)
        settings_layout.addWidget(pattern_label)
        settings_layout.addWidget(self.pattern_combo)
        settings_layout.addStretch()
        
        layout.addWidget(settings_group)
        
        # Answer input section
        answer_group = QGroupBox("Your Answer")
        answer_layout = QVBoxLayout(answer_group)
        
        # Simple text input (removing mode switching complexity)
        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText("Type your subjunctive form here...")
        self.answer_input.setStyleSheet("font-size: 16px; padding: 12px;")
        self.answer_input.returnPressed.connect(self.submitAnswer)
        answer_layout.addWidget(self.answer_input)
        
        # Navigation buttons (simplified)
        nav_layout = QHBoxLayout()
        self.prev_button = QPushButton("← Previous")
        self.hint_button = QPushButton("💡 Hint")
        self.submit_button = QPushButton("✓ Check Answer")
        self.next_button = QPushButton("Next →")
        
        # Set button shortcuts
        self.submit_button.setShortcut("Return")
        self.hint_button.setShortcut("H")
        self.next_button.setShortcut("Right")
        self.prev_button.setShortcut("Left")
        
        nav_layout.addWidget(self.prev_button)
        nav_layout.addWidget(self.hint_button)
        nav_layout.addWidget(self.submit_button)
        nav_layout.addWidget(self.next_button)
        
        answer_layout.addLayout(nav_layout)
        layout.addWidget(answer_group)
        
        # Consolidated feedback section
        feedback_group = QGroupBox("Feedback & Progress")
        feedback_layout = QVBoxLayout(feedback_group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        feedback_layout.addWidget(self.progress_bar)
        
        # Stats display
        self.stats_label = QLabel("Ready to practice! Select your settings and generate exercises.")
        self.stats_label.setStyleSheet("font-weight: bold; color: #495057; padding: 5px;")
        feedback_layout.addWidget(self.stats_label)
        
        # Feedback text
        self.feedback_text = QTextEdit()
        self.feedback_text.setReadOnly(True)
        self.feedback_text.setMaximumHeight(120)
        self.feedback_text.setStyleSheet("background-color: #f8f9fa; border: 1px solid #dee2e6;")
        feedback_layout.addWidget(self.feedback_text)
        
        layout.addWidget(feedback_group)
        
        # Connect button signals
        self.submit_button.clicked.connect(self.submitAnswer)
        self.next_button.clicked.connect(self.nextExercise)
        self.prev_button.clicked.connect(self.prevExercise)
        self.hint_button.clicked.connect(self.provideHint)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Streak display in status bar
        self.streak_label = QLabel()
        self.status_bar.addPermanentWidget(self.streak_label)
        
        # Initialize
        self.updateStats()
        self.updateStatus("Welcome! Choose your settings and click 'Generate Exercises' to begin.")
        
    def createSimplifiedToolBar(self):
        """Create a simplified toolbar with only essential actions"""
        toolbar = QToolBar("Main Actions")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # Essential actions only
        generate_action = QAction("🎯 Generate Exercises", self)
        generate_action.setToolTip("Generate new practice exercises")
        generate_action.triggered.connect(self.generateNewExercise)
        generate_action.setShortcut("Ctrl+G")
        toolbar.addAction(generate_action)
        
        toolbar.addSeparator()
        
        review_action = QAction("📝 Review Mistakes", self)
        review_action.setToolTip("Review previous mistakes")
        review_action.triggered.connect(self.startReviewMode)
        review_action.setShortcut("Ctrl+R")
        toolbar.addAction(review_action)
        
        stats_action = QAction("📊 View Progress", self)
        stats_action.setToolTip("View your learning statistics")
        stats_action.triggered.connect(self.showStats)
        stats_action.setShortcut("Ctrl+S")
        toolbar.addAction(stats_action)
        
        toolbar.addSeparator()
        
        export_action = QAction("💾 Save Session", self)
        export_action.setToolTip("Save your practice session")
        export_action.triggered.connect(self.exportSession)
        toolbar.addAction(export_action)
        
    def check_daily_streak(self):
        """Check and display practice streak"""
        streak_info = self.streak_tracker.record_practice()
        self.streak_label.setText(f"🔥 {streak_info['current']} day streak")
        
        if streak_info['current'] > 0:
            self.updateStatus(streak_info['message'])
    
    def onModeChanged(self, mode_text):
        """Handle practice mode changes"""
        if "Traditional" in mode_text:
            self.practice_mode = "traditional"
            self.updateStatus("Traditional mode: Focus on grammar patterns")
        else:
            self.practice_mode = "communicative"
            self.updateStatus("Communicative mode: Real-world scenarios")
    
    def generateNewExercise(self):
        """Generate new exercises based on current settings"""
        difficulty = self.difficulty_combo.currentText().lower()
        pattern = self.pattern_combo.currentText()
        
        # Map pattern to specific requirements
        pattern_mapping = {
            "Present + Common Triggers": {
                "tenses": ["Present Subjunctive"],
                "triggers": "common wishes and emotions",
                "focus": "basic present subjunctive with everyday triggers"
            },
            "Past + Emotions": {
                "tenses": ["Imperfect Subjunctive"],
                "triggers": "emotional reactions and past situations",
                "focus": "past subjunctive with emotional expressions"
            },
            "All Tenses + Mixed": {
                "tenses": ["Present Subjunctive", "Imperfect Subjunctive", "Present Perfect Subjunctive"],
                "triggers": "mixed triggers requiring tense sequence",
                "focus": "comprehensive subjunctive practice"
            },
            "Review Mistakes": {
                "tenses": ["varies"],
                "triggers": "previously incorrect patterns",
                "focus": "targeted review of weak areas"
            }
        }
        
        if pattern == "Review Mistakes":
            self.startReviewMode()
            return
        
        selected_pattern = pattern_mapping[pattern]
        
        # Create optimized prompt based on mode
        if self.practice_mode == "communicative":
            prompt = self._create_communicative_prompt(difficulty, selected_pattern)
        else:
            prompt = self._create_traditional_prompt(difficulty, selected_pattern)
        
        # Start GPT worker
        worker = GPTWorkerRunnable(prompt, max_tokens=1000, temperature=0.7)
        worker.signals.result.connect(self.handleNewExerciseResult)
        self.threadpool.start(worker)
        
        self.updateStatus("Generating exercises... Please wait.")
        logger.info("Generating exercises with pattern: %s", pattern)
    
    def _create_traditional_prompt(self, difficulty, pattern):
        """Create prompt for traditional grammar exercises"""
        return f"""Create 5 Spanish subjunctive exercises. {difficulty.capitalize()} level.
        
Focus: {pattern['focus']}
Tenses: {', '.join(pattern['tenses'])}
Context: {pattern['triggers']}

Return ONLY this JSON format:
[{{"sentence": "Spanish exercise", "answer": "correct_subjunctive_form", "translation": "English translation", "explanation": "brief why subjunctive"}}]

Requirements:
- LATAM Spanish only
- Real-life situations
- Clear subjunctive triggers
- No extra text outside JSON"""
    
    def _create_communicative_prompt(self, difficulty, pattern):
        """Create prompt for communicative exercises"""
        return f"""Create 5 communicative Spanish subjunctive tasks. {difficulty.capitalize()} level.

Focus: {pattern['focus']}
Tenses: {', '.join(pattern['tenses'])}
Scenarios: Work, travel, social situations

Return ONLY this JSON format:
[{{"sentence": "Complete this real conversation", "answer": "subjunctive_form", "translation": "English context", "explanation": "why this communicates the meaning"}}]

Requirements:
- Authentic dialogues
- LATAM Spanish
- Real communication needs
- No extra text outside JSON"""
    
    def handleNewExerciseResult(self, result: str):
        """Handle the GPT response for new exercises"""
        logger.info("Received GPT response: %s", result[:200] + "..." if len(result) > 200 else result)
        
        # Clean and parse JSON response
        try:
            # Extract JSON from response
            start_index = result.find("[")
            end_index = result.rfind("]")
            if start_index != -1 and end_index != -1:
                json_str = result[start_index:end_index+1]
            else:
                json_str = result
            
            # Remove trailing commas and fix common JSON issues
            json_str = re.sub(r',\s*([\]}])', r'\1', json_str)
            
            # Parse exercises
            new_exercises = json.loads(json_str)
            
            if not isinstance(new_exercises, list) or len(new_exercises) == 0:
                raise ValueError("Invalid exercise format")
            
            # Update exercise data
            self.exercises = new_exercises
            self.total_exercises = len(self.exercises)
            self.current_exercise = 0
            self.correct_count = 0
            self.responses.clear()
            
            # Update UI
            self.progress_bar.setMaximum(self.total_exercises)
            self.updateExercise()
            self.updateStats()
            self.updateStatus("New exercises generated! Start practicing.")
            
            logger.info("Successfully generated %d exercises", self.total_exercises)
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.error("Error parsing exercises: %s", str(e))
            QMessageBox.warning(self, "Generation Error", 
                              "Failed to generate exercises. Please try again with different settings.")
            self.updateStatus("Exercise generation failed. Please try again.")
    
    def updateExercise(self):
        """Update the display with the current exercise"""
        if self.total_exercises == 0 or self.current_exercise >= self.total_exercises:
            return
        
        exercise = self.exercises[self.current_exercise]
        
        # Display exercise
        self.sentence_label.setText(exercise.get("sentence", ""))
        
        # Show translation if available
        if "translation" in exercise:
            self.translation_label.setText(f"💭 {exercise['translation']}")
            self.translation_label.setVisible(True)
        else:
            self.translation_label.setVisible(False)
        
        # Clear previous feedback and answer
        self.feedback_text.clear()
        self.answer_input.clear()
        self.answer_input.setFocus()
        
        # Update progress
        self.progress_bar.setValue(self.current_exercise + 1)
        self.updateStatus(f"Exercise {self.current_exercise + 1} of {self.total_exercises}")
        
    def submitAnswer(self):
        """Process the submitted answer"""
        if self.total_exercises == 0:
            self.updateStatus("No exercises available. Generate exercises first.")
            return
        
        user_answer = self.answer_input.text().strip().lower()
        if not user_answer:
            self.updateStatus("Please enter an answer.")
            return
        
        exercise = self.exercises[self.current_exercise]
        correct_answer = exercise.get("answer", "").strip().lower()
        
        # Update statistics
        self.session_stats["total_attempts"] += 1
        
        # Check if correct
        is_correct = user_answer == correct_answer
        
        if is_correct:
            self.correct_count += 1
            self.session_stats["correct_attempts"] += 1
            feedback = f"✅ Correct! '{correct_answer}' is right."
        else:
            feedback = f"❌ Incorrect. The answer is '{correct_answer}'."
            
            # Add to review items
            self.session_manager.add_exercise_result(exercise, user_answer, is_correct)
        
        # Add explanation if available
        if "explanation" in exercise:
            feedback += f"\n\n💡 {exercise['explanation']}"
        
        # Display feedback
        self.feedback_text.setText(feedback)
        
        # Log response
        self.responses.append({
            "exercise_index": self.current_exercise,
            "sentence": exercise.get("sentence", ""),
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "correct": is_correct,
            "explanation": exercise.get("explanation", "")
        })
        
        self.updateStats()
        logger.info("Answer submitted: %s (correct: %s)", user_answer, is_correct)
    
    def provideHint(self):
        """Provide a hint for the current exercise"""
        if self.total_exercises == 0:
            self.updateStatus("No exercise available.")
            return
        
        exercise = self.exercises[self.current_exercise]
        sentence = exercise.get("sentence", "")
        
        # Create hint prompt
        hint_prompt = f"""Provide a subtle hint for this Spanish subjunctive exercise.
        
Sentence: "{sentence}"
Give a helpful clue without revealing the answer. Focus on the trigger or pattern. 30 words max."""
        
        worker = GPTWorkerRunnable(hint_prompt, max_tokens=100, temperature=0.5)
        worker.signals.result.connect(self.handleHintResult)
        self.threadpool.start(worker)
        
        self.updateStatus("Generating hint...")
        
    def handleHintResult(self, hint: str):
        """Display the hint result"""
        self.feedback_text.setText(f"💡 Hint: {hint}")
        self.updateStatus("Hint provided!")
    
    def nextExercise(self):
        """Move to the next exercise"""
        if self.total_exercises == 0:
            self.updateStatus("No exercises available.")
            return
        
        if self.current_exercise < self.total_exercises - 1:
            self.current_exercise += 1
            self.updateExercise()
            self.updateStats()
        else:
            self.updateStatus("You've completed all exercises!")
    
    def prevExercise(self):
        """Move to the previous exercise"""
        if self.total_exercises == 0:
            self.updateStatus("No exercises available.")
            return
        
        if self.current_exercise > 0:
            self.current_exercise -= 1
            self.updateExercise()
            self.updateStats()
        else:
            self.updateStatus("You're at the first exercise.")
    
    def startReviewMode(self):
        """Start reviewing previous mistakes"""
        review_items = self.session_manager.get_review_items()
        
        if not review_items:
            QMessageBox.information(self, "Review Mode", "No mistakes to review! Keep practicing!")
            return
        
        # Convert to exercise format
        self.exercises = []
        for item in review_items:
            exercise = {
                "sentence": f"REVIEW: {item['sentence']}",
                "answer": item["correct_answer"],
                "translation": f"You previously answered: '{item['user_answer']}'",
                "explanation": "Focus on why the subjunctive is needed here."
            }
            self.exercises.append(exercise)
        
        self.total_exercises = len(self.exercises)
        self.current_exercise = 0
        self.updateExercise()
        self.updateStats()
        
        self.updateStatus(f"Review mode: {self.total_exercises} items to review")
    
    def showStats(self):
        """Show detailed statistics"""
        if self.session_stats["total_attempts"] == 0:
            QMessageBox.information(self, "Statistics", "No practice data yet. Start with some exercises!")
            return
        
        accuracy = (self.session_stats["correct_attempts"] / self.session_stats["total_attempts"]) * 100
        session_time = (datetime.now() - self.session_stats["session_start"]).total_seconds() / 60
        
        stats_text = f"""📊 Practice Statistics

🎯 Accuracy: {accuracy:.1f}%
📝 Exercises Completed: {self.session_stats['total_attempts']}
✅ Correct Answers: {self.session_stats['correct_attempts']}
⏱️ Session Time: {session_time:.1f} minutes

🔥 Current Streak: {self.streak_tracker.get_streak_info()['current']} days

Keep up the great work!"""
        
        QMessageBox.information(self, "Your Progress", stats_text)
    
    def exportSession(self):
        """Export current session to CSV"""
        if not self.responses:
            QMessageBox.warning(self, "No Data", "No practice data to export.")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"subjunctive_practice_{timestamp}.csv"
        
        try:
            import csv
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Exercise', 'Sentence', 'Your Answer', 'Correct Answer', 'Result']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for i, response in enumerate(self.responses, 1):
                    writer.writerow({
                        'Exercise': i,
                        'Sentence': response['sentence'],
                        'Your Answer': response['user_answer'],
                        'Correct Answer': response['correct_answer'],
                        'Result': 'Correct' if response['correct'] else 'Incorrect'
                    })
            
            QMessageBox.information(self, "Export Successful", f"Session saved to {filename}")
            self.updateStatus("Session exported successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", f"Could not save session: {str(e)}")
    
    def updateStats(self):
        """Update the statistics display"""
        if self.session_stats["total_attempts"] > 0:
            accuracy = (self.session_stats["correct_attempts"] / self.session_stats["total_attempts"]) * 100
            self.stats_label.setText(
                f"Progress: {self.current_exercise + 1}/{self.total_exercises} | "
                f"Accuracy: {accuracy:.0f}% ({self.correct_count} correct)"
            )
        else:
            self.stats_label.setText("Ready to practice! Generate exercises to begin.")
    
    def updateStatus(self, message: str):
        """Update the status bar message"""
        self.status_bar.showMessage(message, 5000)
        logger.info("Status: %s", message)


def main():
    """Run the simplified Spanish subjunctive practice application"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Spanish Subjunctive Practice")
    app.setApplicationVersion("2.0 Simplified")
    app.setOrganizationName("Spanish Learning Tools")
    
    # Create and show main window
    window = SimplifiedSubjunctivePracticeGUI()
    window.show()
    
    # Run application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
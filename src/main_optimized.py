"""
Optimized Version of the Spanish Subjunctive Practice Application
================================================================

This file demonstrates how to integrate the optimized layout system with
the existing Spanish Subjunctive Practice application functionality.

It maintains all existing features while providing:
- 70-30 layout optimization
- Modern card-based design
- Collapsible sections
- Responsive design
- Enhanced educational feedback

To use this optimized version:
1. Copy your existing application logic
2. Replace the UI setup with optimized components
3. Connect signals to existing methods
4. Test and adjust as needed
"""

import sys
import os
import json
import random
import logging
from typing import List, Dict
from datetime import datetime

# Add the parent directory to path to import existing modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import Qt, QTimer, QThreadPool

# Import existing application modules
try:
    from tblt_scenarios import TBLTTaskGenerator, SpacedRepetitionTracker
    from conjugation_reference import STEM_CHANGING_PATTERNS, SEQUENCE_OF_TENSES
    from session_manager import SessionManager, ReviewQueue
    from learning_analytics import StreakTracker, ErrorAnalyzer, AdaptiveDifficulty, PracticeGoals
except ImportError as e:
    print(f"Warning: Could not import existing modules: {e}")
    print("Creating mock classes for demonstration...")
    
    # Mock classes for demonstration if imports fail
    class TBLTTaskGenerator:
        pass
    class SpacedRepetitionTracker:
        pass
    class SessionManager:
        def add_exercise_result(self, exercise, answer, correct):
            pass
        def get_review_items(self):
            return []
        def save_session(self):
            return "demo_session.json"
        def get_statistics(self):
            return {"accuracy": 85.0, "mastered_items": 10, "items_to_review": 3}
    class ReviewQueue:
        pass
    class StreakTracker:
        def record_practice(self):
            return {"current": 5, "best": 12, "message": "Keep up the good work!"}
        def get_streak_info(self):
            return {"current": 5, "best": 12, "total_days": 25}
    class ErrorAnalyzer:
        def analyze_error(self, user_answer, correct_answer, context):
            return {"suggestion": "Remember to use subjunctive after expressions of doubt"}
        def get_weakness_report(self):
            return {"weaknesses": [], "suggestions": []}
    class AdaptiveDifficulty:
        def record_performance(self, correct):
            return {"adjusted": False, "new_level": "Intermediate"}
    class PracticeGoals:
        def __init__(self):
            self.goals = {
                "daily_exercises": 10,
                "target_accuracy": 85,
                "weekly_minutes": 120,
                "achievements": []
            }
        def check_achievement(self, metric, value):
            return []

# Import optimized layout components
from optimized_layout import OptimizedSubjunctiveLayout, create_optimized_layout
from layout_integration import LayoutIntegrationMixin
from responsive_design import ResponsiveManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OptimizedSpanishSubjunctivePracticeGUI(QMainWindow, LayoutIntegrationMixin):
    """
    Optimized version of the Spanish Subjunctive Practice GUI that integrates
    the new layout system with existing application functionality.
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spanish Subjunctive Practice - Optimized Layout")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize existing data structures
        self.exercises = []
        self.current_exercise = 0
        self.total_exercises = 0
        self.correct_count = 0
        self.responses = []
        self.session_stats = {
            "total_attempts": 0,
            "correct_attempts": 0,
            "hints_used": 0,
            "session_start": datetime.now(),
            "tenses_practiced": set(),
            "persons_practiced": set()
        }
        
        # Initialize existing components
        self.threadpool = QThreadPool()
        self.tblt_generator = TBLTTaskGenerator()
        self.spaced_repetition = SpacedRepetitionTracker()
        self.session_manager = SessionManager()
        self.review_queue = ReviewQueue()
        self.streak_tracker = StreakTracker()
        self.error_analyzer = ErrorAnalyzer()
        self.adaptive_difficulty = AdaptiveDifficulty()
        self.practice_goals = PracticeGoals()
        
        # UI state
        self.dark_mode = False
        self.show_translation = False
        self.current_task_type = "traditional"
        self.review_mode = False
        
        # Initialize optimized UI
        self._setup_optimized_ui()
        
        # Setup existing functionality
        self._setup_existing_functionality()
        
        logger.info("Optimized Spanish Subjunctive Practice GUI initialized")
        
    def _setup_optimized_ui(self):
        """Setup the optimized layout system"""
        # Create optimized layout
        self.layout_widget = create_optimized_layout(self)
        self.setCentralWidget(self.layout_widget)
        
        # Setup responsive design
        self.responsive_manager = ResponsiveManager(self.layout_widget)
        
        # Connect optimized layout signals to existing methods
        self.layout_widget.exercise_generated.connect(self.generateNewExercise)
        self.layout_widget.answer_submitted.connect(self.handleOptimizedSubmission)
        self.layout_widget.hint_requested.connect(self.provideHint)
        self.layout_widget.navigation_requested.connect(self.handleNavigation)
        
        # Connect UI change signals
        self.layout_widget.mode_combo.currentTextChanged.connect(self.switchMode)
        self.layout_widget.task_type_combo.currentIndexChanged.connect(self.onTaskTypeChanged)
        
        # Setup status bar
        self.status_bar = self.statusBar()
        self.updateStatus("Optimized layout ready! Select options and generate exercises.")
        
        # Initialize streak display
        self.check_daily_streak()
        
    def _setup_existing_functionality(self):
        """Setup existing application functionality"""
        # This is where you would integrate your existing GPT worker,
        # exercise generation logic, etc.
        
        # For demo purposes, we'll create sample data
        self._create_sample_exercises()
        
    def _create_sample_exercises(self):
        """Create sample exercises for demonstration"""
        sample_exercises = [
            {
                "context": "Expressing wishes",
                "sentence": "Espero que tú _____ (estudiar) mucho para el examen.",
                "answer": "estudies",
                "choices": ["estudias", "estudies", "estudiarás", "estudiabas"],
                "translation": "I hope you study a lot for the exam."
            },
            {
                "context": "Expressing doubt",
                "sentence": "Dudo que ella _____ (llegar) a tiempo mañana.",
                "answer": "llegue",
                "choices": ["llega", "llegue", "llegará", "llegaba"],
                "translation": "I doubt she will arrive on time tomorrow."
            },
            {
                "context": "Impersonal expression",
                "sentence": "Es necesario que nosotros _____ (terminar) el proyecto hoy.",
                "answer": "terminemos",
                "choices": ["terminamos", "terminemos", "terminaremos", "terminábamos"],
                "translation": "It's necessary that we finish the project today."
            }
        ]
        
        self.exercises = sample_exercises
        self.total_exercises = len(self.exercises)
        self.current_exercise = 0
        self.updateExercise()
        
    def handleOptimizedSubmission(self, answer: str):
        """Handle answer submission from optimized layout"""
        if not answer.strip():
            self.updateStatus("Please provide an answer.")
            return
            
        # Use existing submission logic
        self.submitAnswer()
        
    def handleNavigation(self, direction: str):
        """Handle navigation from optimized layout"""
        if direction == 'next':
            self.nextExercise()
        elif direction == 'prev':
            self.prevExercise()
            
    def generateNewExercise(self):
        """Generate new exercises - adapted for optimized layout"""
        # Get selections from optimized layout
        selected_triggers = self.layout_widget.get_selected_triggers()
        selected_tenses = self.layout_widget.get_selected_tenses()
        selected_persons = self.layout_widget.get_selected_persons()
        task_type = self.layout_widget.get_task_type()
        
        # Validate selections
        if not selected_tenses:
            QMessageBox.warning(self, "Selection Required", "Please select at least one tense.")
            return
        if not selected_persons:
            QMessageBox.warning(self, "Selection Required", "Please select at least one person.")
            return
        if task_type == "Traditional Grammar" and not selected_triggers:
            QMessageBox.warning(self, "Selection Required", "Please select at least one subjunctive trigger.")
            return
            
        self.updateStatus("Generating new exercises...")
        
        # For demo, create new sample exercises
        QTimer.singleShot(1000, self._complete_exercise_generation)
        
    def _complete_exercise_generation(self):
        """Complete exercise generation"""
        # Create new exercises (in real app, this would call GPT)
        self._create_sample_exercises()
        self.updateStatus("New exercises generated!")
        
    def updateExercise(self):
        """Update exercise display - adapted for optimized layout"""
        if self.total_exercises == 0 or self.current_exercise < 0 or self.current_exercise >= self.total_exercises:
            return
            
        exercise = self.exercises[self.current_exercise]
        
        # Prepare content
        context = exercise.get("context", "")
        sentence = exercise.get("sentence", "")
        if context:
            full_text = f"**{context}**\n\n{sentence}"
        else:
            full_text = sentence
            
        translation = exercise.get("translation", "")
        
        # Update optimized layout
        self.layout_widget.set_exercise_content(full_text, translation, self.show_translation)
        
        # Handle multiple choice
        mode = self.layout_widget.get_mode()
        if mode == "Multiple Choice" and "choices" in exercise:
            choices = exercise["choices"].copy()
            random.shuffle(choices)
            self.layout_widget.set_multiple_choice_options(choices)
        else:
            self.layout_widget.switch_input_mode(mode)
            
        # Clear previous feedback
        self.layout_widget.clear_feedback()
        
        # Update progress
        self.updateStats()
        self.updateStatus(f"Exercise {self.current_exercise + 1} of {self.total_exercises}")
        
    def submitAnswer(self):
        """Submit answer - adapted for optimized layout"""
        if self.total_exercises == 0:
            self.updateStatus("No exercises available.")
            return
            
        user_answer = self.layout_widget.get_user_answer().strip().lower()
        if not user_answer:
            self.updateStatus("Please provide an answer.")
            return
            
        exercise = self.exercises[self.current_exercise]
        correct_answer = exercise.get("answer", "").strip().lower()
        
        # Update session stats
        self.session_stats["total_attempts"] += 1
        
        # Check answer
        is_correct = user_answer == correct_answer
        
        if is_correct:
            self.correct_count += 1
            self.session_stats["correct_attempts"] += 1
            feedback = f"✅ Correct! The answer is '{correct_answer}'."
            self.updateStatus("Correct answer!")
        else:
            feedback = f"❌ Incorrect. The correct answer is '{correct_answer}'."
            self.updateStatus("Incorrect answer.")
            
            # Add error analysis
            error_analysis = self.error_analyzer.analyze_error(
                user_answer, correct_answer, {"trigger": exercise.get("context", "")}
            )
            if error_analysis["suggestion"]:
                feedback += f"\n\n💡 Tip: {error_analysis['suggestion']}"
                
        # Add explanation
        if "context" in exercise:
            context = exercise["context"].lower()
            if "wish" in context:
                feedback += "\n\nThis context expresses a wish, which requires the subjunctive mood."
            elif "doubt" in context:
                feedback += "\n\nExpressions of doubt trigger the subjunctive mood in Spanish."
            elif "necessary" in context or "important" in context:
                feedback += "\n\nImpersonal expressions of necessity require the subjunctive."
                
        # Update display
        self.layout_widget.set_feedback(feedback)
        
        # Record session data
        self.session_manager.add_exercise_result(exercise, user_answer, is_correct)
        self.updateStats()
        
        logger.info(f"Answer submitted: '{user_answer}' (correct: {is_correct})")
        
    def provideHint(self):
        """Provide hint - adapted for optimized layout"""
        if self.total_exercises == 0:
            return
            
        self.session_stats["hints_used"] += 1
        
        exercise = self.exercises[self.current_exercise]
        answer = exercise.get("answer", "")
        context = exercise.get("context", "")
        
        # Generate hint
        hints = []
        hints.append(f"The answer has {len(answer)} letters.")
        if answer:
            hints.append(f"The answer starts with '{answer[0].upper()}'.")
        if "wish" in context.lower():
            hints.append("This context expresses a wish or hope.")
        elif "doubt" in context.lower():
            hints.append("This context expresses doubt or uncertainty.")
            
        hint = random.choice(hints)
        self.layout_widget.set_feedback(f"💡 Hint: {hint}")
        self.updateStatus("Hint provided")
        
    def nextExercise(self):
        """Navigate to next exercise"""
        if self.current_exercise < self.total_exercises - 1:
            self.current_exercise += 1
            self.layout_widget.clear_answer_input()
            self.updateExercise()
            
    def prevExercise(self):
        """Navigate to previous exercise"""
        if self.current_exercise > 0:
            self.current_exercise -= 1
            self.layout_widget.clear_answer_input()
            self.updateExercise()
            
    def updateStats(self):
        """Update statistics display"""
        accuracy = 0
        if self.session_stats["total_attempts"] > 0:
            accuracy = (self.session_stats["correct_attempts"] / self.session_stats["total_attempts"]) * 100
            
        # Update optimized layout
        self.layout_widget.update_progress(
            self.current_exercise + 1,
            self.total_exercises,
            self.correct_count,
            accuracy
        )
        
    def check_daily_streak(self):
        """Check and display daily practice streak"""
        streak_info = self.streak_tracker.record_practice()
        self.layout_widget.update_streak(streak_info['current'], streak_info['best'])
        
    def updateStatus(self, message: str):
        """Update status bar"""
        self.status_bar.showMessage(message, 4000)
        logger.info(f"Status: {message}")
        
    def switchMode(self, mode: str = None):
        """Switch input mode"""
        if mode is None:
            mode = self.layout_widget.get_mode()
        self.layout_widget.switch_input_mode(mode)
        self.updateExercise()  # Refresh display for new mode
        
    def onTaskTypeChanged(self, index):
        """Handle task type change"""
        task_types = ["traditional", "tblt", "contrast", "review"]
        self.current_task_type = task_types[index] if index < len(task_types) else "traditional"
        
        if self.current_task_type == "tblt":
            self.updateStatus("TBLT mode: Focus on real-world communication tasks")
        elif self.current_task_type == "contrast":
            self.updateStatus("Contrast mode: Compare indicative vs subjunctive")
        elif self.current_task_type == "review":
            self.updateStatus("Review mode: Practice previous mistakes")
        else:
            self.updateStatus("Traditional mode: Grammar-focused exercises")
            
    def resizeEvent(self, event):
        """Handle window resize for responsive design"""
        super().resizeEvent(event)
        if hasattr(self, 'responsive_manager'):
            self.responsive_manager.schedule_resize(event.size())
            
    def closeEvent(self, event):
        """Handle application close"""
        logger.info("Application closing")
        
        # Save session data if needed
        if self.session_stats["total_attempts"] > 0:
            try:
                self.session_manager.save_session()
                logger.info("Session saved successfully")
            except Exception as e:
                logger.error(f"Failed to save session: {e}")
                
        event.accept()


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Spanish Subjunctive Practice - Optimized")
    
    # Set application font for better readability
    from PyQt5.QtGui import QFont
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    try:
        # Create and show main window
        window = OptimizedSpanishSubjunctivePracticeGUI()
        window.show()
        
        # Show welcome message
        QTimer.singleShot(1000, lambda: QMessageBox.information(
            window, 
            "Welcome to the Optimized Layout!", 
            """🎉 Welcome to the optimized Spanish Subjunctive Practice!

Key improvements:
• 70-30 layout for better content focus
• Modern card-based design
• Collapsible sections for space efficiency
• Responsive design for all screen sizes
• Enhanced educational feedback

Try resizing the window to see responsive design in action!

Select your tenses and persons, then click 'Generate New Exercises' to begin."""
        ))
        
        # Start event loop
        sys.exit(app.exec_())
        
    except Exception as e:
        logger.error(f"Application error: {e}")
        
        # Show error dialog
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Application Error")
        error_dialog.setText(f"Failed to start application:\n\n{str(e)}")
        error_dialog.exec_()
        
        sys.exit(1)


if __name__ == "__main__":
    main()
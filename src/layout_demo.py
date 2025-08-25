"""
Layout Demonstration Script
===========================

This script demonstrates the complete optimized layout system for the
Spanish Subjunctive Practice application, including:

1. Modern card-based design
2. 70-30 layout optimization
3. Collapsible sections for space efficiency
4. Responsive design capabilities
5. Educational effectiveness improvements
6. Integration with existing application features

Run this script to see a complete working demo of the optimized layout.
"""

import sys
import random
import logging
from typing import List, Dict, Optional

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QMessageBox, QStatusBar, QLabel, QPushButton, QTextEdit,
    QProgressBar, QSplashScreen
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont, QPalette

# Import our custom modules
from optimized_layout import OptimizedSubjunctiveLayout, create_optimized_layout
from layout_integration import LayoutIntegrationMixin
from responsive_design import ResponsiveManager, get_screen_info

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('layout_demo.log')
    ]
)


class DemoDataGenerator:
    """Generate sample data for demonstration purposes"""
    
    @staticmethod
    def generate_sample_exercises(count: int = 5) -> List[Dict]:
        """Generate sample Spanish subjunctive exercises"""
        exercises = []
        
        sample_data = [
            {
                "context": "Expressing wishes",
                "sentence": "Espero que tú _____ (estudiar) español todos los días.",
                "answer": "estudies",
                "choices": ["estudias", "estudies", "estudiarás", "estudiabas"],
                "translation": "I hope you study Spanish every day.",
                "explanation": "We use the present subjunctive after 'espero que' because it expresses a wish or hope."
            },
            {
                "context": "Expressing doubt",
                "sentence": "Dudo que ella _____ (venir) a la fiesta mañana.",
                "answer": "venga",
                "choices": ["viene", "venga", "vendrá", "venía"],
                "translation": "I doubt she will come to the party tomorrow.",
                "explanation": "We use the subjunctive after 'dudar que' because it expresses doubt or uncertainty."
            },
            {
                "context": "Impersonal expression",
                "sentence": "Es importante que nosotros _____ (llegar) a tiempo.",
                "answer": "lleguemos",
                "choices": ["llegamos", "lleguemos", "llegaremos", "llegábamos"],
                "translation": "It's important that we arrive on time.",
                "explanation": "Impersonal expressions of necessity like 'es importante que' require the subjunctive."
            },
            {
                "context": "Emotional reaction",
                "sentence": "Me alegra que ustedes _____ (estar) aquí con nosotros.",
                "answer": "estén",
                "choices": ["están", "estén", "estarán", "estaban"],
                "translation": "I'm glad you are here with us.",
                "explanation": "Expressions of emotion like 'me alegra que' trigger the subjunctive mood."
            },
            {
                "context": "Negative opinion",
                "sentence": "No creo que el examen _____ (ser) muy difícil.",
                "answer": "sea",
                "choices": ["es", "sea", "será", "era"],
                "translation": "I don't think the exam will be very difficult.",
                "explanation": "Negative opinions like 'no creo que' require the subjunctive mood."
            },
            {
                "context": "TBLT: Planning a trip",
                "sentence": "Necesitamos un hotel que _____ (tener) piscina y gimnasio.",
                "answer": "tenga",
                "choices": ["tiene", "tenga", "tendrá", "tenía"],
                "translation": "We need a hotel that has a pool and gym.",
                "explanation": "When referring to an indefinite or unknown antecedent, we use the subjunctive."
            },
            {
                "context": "Making recommendations",
                "sentence": "Te sugiero que _____ (hablar) con el profesor antes del examen.",
                "answer": "hables",
                "choices": ["hablas", "hables", "hablarás", "hablabas"],
                "translation": "I suggest you talk to the professor before the exam.",
                "explanation": "Verbs of influence and recommendation like 'sugerir' require the subjunctive."
            },
            {
                "context": "Expressing purpose",
                "sentence": "Voy a explicar otra vez para que todos _____ (entender).",
                "answer": "entiendan",
                "choices": ["entienden", "entiendan", "entenderán", "entendían"],
                "translation": "I'm going to explain again so that everyone understands.",
                "explanation": "The conjunction 'para que' (so that) always requires the subjunctive."
            }
        ]
        
        # Return requested number of exercises
        selected_exercises = random.sample(sample_data, min(count, len(sample_data)))
        return selected_exercises


class OptimizedDemoApplication(QMainWindow):
    """
    Complete demonstration application showing the optimized layout system
    """
    
    def __init__(self):
        super().__init__()
        
        # Application state
        self.exercises = []
        self.current_exercise = 0
        self.total_exercises = 0
        self.correct_count = 0
        self.session_stats = {
            "total_attempts": 0,
            "correct_attempts": 0,
            "hints_used": 0,
            "start_time": None
        }
        
        # Setup UI
        self._setup_application()
        self._setup_demo_data()
        
        # Show welcome message
        QTimer.singleShot(1000, self._show_welcome_message)
        
    def _setup_application(self):
        """Setup the main application window and layout"""
        self.setWindowTitle("Spanish Subjunctive Practice - Optimized Layout Demo")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create optimized layout
        self.layout_widget = create_optimized_layout(self)
        self.setCentralWidget(self.layout_widget)
        
        # Setup responsive design
        self.responsive_manager = ResponsiveManager(self.layout_widget)
        
        # Connect signals
        self._connect_signals()
        
        # Setup status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Add application info to status bar
        screen_info = get_screen_info()
        if screen_info:
            primary_screen = next((info for info in screen_info.values() if info.get('primary')), None)
            if primary_screen:
                self.status_bar.addPermanentWidget(
                    QLabel(f"Screen: {primary_screen['size'][0]}x{primary_screen['size'][1]}")
                )
        
        # Apply styling
        self._apply_application_styling()
        
        logging.info("Demo application initialized")
        
    def _connect_signals(self):
        """Connect layout signals to demo functionality"""
        self.layout_widget.exercise_generated.connect(self.generate_new_exercises)
        self.layout_widget.answer_submitted.connect(self.submit_answer)
        self.layout_widget.hint_requested.connect(self.provide_hint)
        self.layout_widget.navigation_requested.connect(self.handle_navigation)
        
        # Connect combo box changes
        self.layout_widget.mode_combo.currentTextChanged.connect(self.on_mode_changed)
        self.layout_widget.task_type_combo.currentTextChanged.connect(self.on_task_type_changed)
        
    def _apply_application_styling(self):
        """Apply global application styling"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            
            QStatusBar {
                background-color: #e9ecef;
                border-top: 1px solid #dee2e6;
                color: #6c757d;
                font-size: 12px;
            }
            
            QStatusBar QLabel {
                color: #6c757d;
                padding: 2px 8px;
            }
        """)
        
    def _setup_demo_data(self):
        """Setup initial demo data"""
        self.exercises = DemoDataGenerator.generate_sample_exercises(8)
        self.total_exercises = len(self.exercises)
        self.current_exercise = 0
        
        # Update display
        self._update_exercise_display()
        self._show_status("Demo ready! Select options and generate exercises.")
        
    def generate_new_exercises(self):
        """Generate new exercises based on current selections"""
        # Validate selections
        if not self._validate_selections():
            return
            
        # Get current selections
        selections = {
            'tenses': self.layout_widget.get_selected_tenses(),
            'persons': self.layout_widget.get_selected_persons(),
            'triggers': self.layout_widget.get_selected_triggers(),
            'difficulty': self.layout_widget.get_difficulty(),
            'task_type': self.layout_widget.get_task_type(),
            'mode': self.layout_widget.get_mode()
        }
        
        self._show_status("Generating exercises...")
        logging.info(f"Generating exercises with selections: {selections}")
        
        # Simulate exercise generation delay
        QTimer.singleShot(1500, self._complete_exercise_generation)
        
    def _complete_exercise_generation(self):
        """Complete the exercise generation process"""
        # Generate new exercises based on selections
        exercise_count = random.randint(5, 8)
        self.exercises = DemoDataGenerator.generate_sample_exercises(exercise_count)
        self.total_exercises = len(self.exercises)
        self.current_exercise = 0
        self.correct_count = 0
        
        # Reset session stats
        self.session_stats = {
            "total_attempts": 0,
            "correct_attempts": 0,
            "hints_used": 0,
            "start_time": None
        }
        
        # Update display
        self._update_exercise_display()
        self._show_status(f"Generated {self.total_exercises} new exercises!")
        
    def _validate_selections(self) -> bool:
        """Validate current selections"""
        tenses = self.layout_widget.get_selected_tenses()
        persons = self.layout_widget.get_selected_persons()
        
        if not tenses:
            QMessageBox.warning(self, "Selection Required", 
                              "Please select at least one tense before generating exercises.")
            return False
            
        if not persons:
            QMessageBox.warning(self, "Selection Required",
                              "Please select at least one person before generating exercises.")
            return False
            
        # For traditional grammar, require triggers
        task_type = self.layout_widget.get_task_type()
        if task_type == "Traditional Grammar":
            triggers = self.layout_widget.get_selected_triggers()
            if not triggers:
                QMessageBox.warning(self, "Selection Required",
                                  "Please select at least one subjunctive trigger for traditional grammar exercises.")
                return False
                
        return True
        
    def submit_answer(self, user_answer: str):
        """Handle answer submission"""
        if not user_answer.strip():
            self._show_status("Please provide an answer.")
            return
            
        if not self.exercises or self.current_exercise >= len(self.exercises):
            self._show_status("No exercise available.")
            return
            
        # Initialize session stats if needed
        if self.session_stats["start_time"] is None:
            import datetime
            self.session_stats["start_time"] = datetime.datetime.now()
            
        exercise = self.exercises[self.current_exercise]
        correct_answer = exercise.get("answer", "").strip().lower()
        user_answer_clean = user_answer.strip().lower()
        
        # Update stats
        self.session_stats["total_attempts"] += 1
        
        # Check answer
        is_correct = user_answer_clean == correct_answer
        
        if is_correct:
            self.correct_count += 1
            self.session_stats["correct_attempts"] += 1
            feedback = f"✅ ¡Correcto! The answer is '{correct_answer}'."
            self._show_status("Correct answer!")
        else:
            feedback = f"❌ Incorrect. The correct answer is '{correct_answer}'."
            self._show_status("Incorrect answer.")
            
        # Add explanation
        explanation = exercise.get("explanation", "")
        if explanation:
            feedback += f"\n\n💡 Explanation: {explanation}"
            
        # Add context-specific tips
        context_tips = self._get_context_tips(exercise.get("context", ""))
        if context_tips:
            feedback += f"\n\n🎯 Tip: {context_tips}"
            
        # Update display
        self.layout_widget.set_feedback(feedback)
        self._update_progress_display()
        
        # Check for session milestones
        self._check_session_milestones()
        
        logging.info(f"Answer submitted: '{user_answer}' (correct: {is_correct})")
        
    def _get_context_tips(self, context: str) -> str:
        """Get context-specific learning tips"""
        tips = {
            "wishes": "Remember: expressions of desire or wish always trigger the subjunctive.",
            "doubt": "Doubt and uncertainty require the subjunctive mood in Spanish.",
            "emotion": "Emotional reactions to events require the subjunctive.",
            "impersonal": "Impersonal expressions of opinion or necessity use the subjunctive.",
            "negative": "Negative opinions often require the subjunctive.",
            "recommendation": "Verbs of influence and recommendation trigger the subjunctive.",
            "purpose": "Conjunctions expressing purpose (para que) always use subjunctive.",
            "indefinite": "Unknown or indefinite antecedents require the subjunctive."
        }
        
        context_lower = context.lower()
        for key, tip in tips.items():
            if key in context_lower:
                return tip
                
        return "Practice recognizing subjunctive triggers in different contexts!"
        
    def provide_hint(self):
        """Provide a hint for the current exercise"""
        if not self.exercises or self.current_exercise >= len(self.exercises):
            return
            
        self.session_stats["hints_used"] += 1
        
        exercise = self.exercises[self.current_exercise]
        answer = exercise.get("answer", "")
        context = exercise.get("context", "")
        
        # Generate different types of hints
        hints = []
        
        # Length hint
        hints.append(f"The answer has {len(answer)} letters.")
        
        # First letter hint
        if answer:
            hints.append(f"The answer starts with '{answer[0].upper()}'.")
            
        # Context hint
        if "wish" in context.lower() or "hope" in context.lower():
            hints.append("This context expresses a wish or hope.")
        elif "doubt" in context.lower():
            hints.append("This context expresses doubt or uncertainty.")
        elif "emotion" in context.lower() or "glad" in context.lower():
            hints.append("This context expresses an emotional reaction.")
        elif "important" in context.lower() or "necessary" in context.lower():
            hints.append("This is an impersonal expression of necessity.")
            
        # Conjugation hint
        if answer.endswith("e") or answer.endswith("es") or answer.endswith("en"):
            hints.append("Look for the present subjunctive ending.")
        elif answer.endswith("a") or answer.endswith("as") or answer.endswith("an"):
            hints.append("Remember the subjunctive vowel change.")
            
        # Select a random hint
        selected_hint = random.choice(hints)
        hint_text = f"💡 Hint: {selected_hint}"
        
        self.layout_widget.set_feedback(hint_text)
        self._show_status("Hint provided")
        
        logging.info(f"Hint provided: {selected_hint}")
        
    def handle_navigation(self, direction: str):
        """Handle navigation between exercises"""
        if direction == 'next':
            if self.current_exercise < self.total_exercises - 1:
                self.current_exercise += 1
                self._update_exercise_display()
                self._show_status(f"Exercise {self.current_exercise + 1} of {self.total_exercises}")
            else:
                self._show_session_summary()
                
        elif direction == 'prev':
            if self.current_exercise > 0:
                self.current_exercise -= 1
                self._update_exercise_display()
                self._show_status(f"Exercise {self.current_exercise + 1} of {self.total_exercises}")
                
        logging.info(f"Navigation: {direction} to exercise {self.current_exercise + 1}")
        
    def on_mode_changed(self, mode: str):
        """Handle mode changes"""
        self.layout_widget.switch_input_mode(mode)
        self._show_status(f"Switched to {mode.lower()} mode")
        
        # If current exercise has choices and mode is MC, set them up
        if (mode == "Multiple Choice" and self.exercises and 
            self.current_exercise < len(self.exercises)):
            exercise = self.exercises[self.current_exercise]
            if "choices" in exercise:
                choices = exercise["choices"].copy()
                random.shuffle(choices)
                self.layout_widget.set_multiple_choice_options(choices)
                
    def on_task_type_changed(self):
        """Handle task type changes"""
        task_type = self.layout_widget.get_task_type()
        self._show_status(f"Task type: {task_type}")
        
        if task_type == "TBLT Scenarios":
            self._show_status("TBLT mode: Focus on real-world communication")
        elif task_type == "Mood Contrast":
            self._show_status("Contrast mode: Compare indicative vs subjunctive")
        elif task_type == "Review Mode":
            self._show_status("Review mode: Practice previous mistakes")
        else:
            self._show_status("Traditional mode: Grammar-focused exercises")
            
    def _update_exercise_display(self):
        """Update the exercise display"""
        if not self.exercises or self.current_exercise >= len(self.exercises):
            return
            
        exercise = self.exercises[self.current_exercise]
        
        # Prepare content
        context = exercise.get("context", "")
        sentence = exercise.get("sentence", "")
        
        if context:
            display_text = f"**Context: {context}**\n\n{sentence}"
        else:
            display_text = sentence
            
        translation = exercise.get("translation", "")
        
        # Update layout
        self.layout_widget.set_exercise_content(display_text, translation, True)
        
        # Handle multiple choice if needed
        mode = self.layout_widget.get_mode()
        if mode == "Multiple Choice" and "choices" in exercise:
            choices = exercise["choices"].copy()
            random.shuffle(choices)
            self.layout_widget.set_multiple_choice_options(choices)
        else:
            self.layout_widget.switch_input_mode(mode)
            
        # Clear previous input and feedback
        self.layout_widget.clear_answer_input()
        self.layout_widget.clear_feedback()
        
        # Update progress
        self._update_progress_display()
        
        # Update navigation buttons
        self.layout_widget.set_button_enabled('prev', self.current_exercise > 0)
        self.layout_widget.set_button_enabled('next', self.current_exercise < self.total_exercises - 1)
        
    def _update_progress_display(self):
        """Update progress information"""
        current = self.current_exercise + 1
        total = self.total_exercises
        correct = self.correct_count
        
        # Calculate accuracy
        attempts = self.session_stats.get("total_attempts", 0)
        accuracy = (self.session_stats["correct_attempts"] / max(attempts, 1)) * 100 if attempts > 0 else 0
        
        # Update layout
        self.layout_widget.update_progress(current, total, correct, accuracy)
        
        # Update streak (demo with random values)
        current_streak = random.randint(0, 15)
        best_streak = random.randint(current_streak, 30)
        self.layout_widget.update_streak(current_streak, best_streak)
        
    def _check_session_milestones(self):
        """Check for session milestones and achievements"""
        attempts = self.session_stats["total_attempts"]
        correct = self.session_stats["correct_attempts"]
        accuracy = (correct / max(attempts, 1)) * 100
        
        # Achievement notifications
        if attempts == 5 and accuracy >= 80:
            QMessageBox.information(self, "Achievement!", 
                                  "🏆 Great start! You have 80% accuracy after 5 exercises!")
        elif attempts == 10 and accuracy >= 85:
            QMessageBox.information(self, "Achievement!",
                                  "🏆 Excellent! You're maintaining high accuracy!")
        elif correct == 5:
            QMessageBox.information(self, "Achievement!",
                                  "🏆 Five correct answers in a row!")
            
    def _show_session_summary(self):
        """Show session completion summary"""
        attempts = self.session_stats["total_attempts"]
        correct = self.session_stats["correct_attempts"]
        hints = self.session_stats["hints_used"]
        accuracy = (correct / max(attempts, 1)) * 100
        
        # Calculate session time
        session_time = "N/A"
        if self.session_stats["start_time"]:
            import datetime
            duration = datetime.datetime.now() - self.session_stats["start_time"]
            minutes = int(duration.total_seconds() / 60)
            seconds = int(duration.total_seconds() % 60)
            session_time = f"{minutes}m {seconds}s"
        
        summary = f"""
        🎉 Session Complete!
        
        📊 Your Performance:
        • Total Exercises: {self.total_exercises}
        • Attempts: {attempts}
        • Correct: {correct}
        • Accuracy: {accuracy:.1f}%
        • Hints Used: {hints}
        • Time: {session_time}
        
        {'🏆 Excellent work!' if accuracy >= 80 else '📚 Keep practicing!'}
        """
        
        QMessageBox.information(self, "Session Summary", summary)
        self._show_status("Session completed!")
        
    def _show_welcome_message(self):
        """Show welcome message"""
        welcome = """
        Welcome to the Optimized Spanish Subjunctive Practice!
        
        🎯 New Features:
        • 70-30 layout for better content focus
        • Collapsible sections to save space
        • Responsive design for all screen sizes
        • Modern card-based interface
        • Enhanced educational feedback
        
        📋 To get started:
        1. Select your preferred tenses and persons
        2. Choose subjunctive triggers (for traditional mode)
        3. Click "Generate New Exercises"
        4. Practice and receive detailed feedback!
        
        💡 Try resizing the window to see responsive design in action!
        """
        
        QMessageBox.information(self, "Welcome!", welcome)
        
    def _show_status(self, message: str):
        """Show status message"""
        self.status_bar.showMessage(message, 5000)
        logging.info(f"Status: {message}")
        
    def resizeEvent(self, event):
        """Handle window resize events"""
        super().resizeEvent(event)
        
        # Apply responsive layout
        if hasattr(self, 'responsive_manager'):
            self.responsive_manager.schedule_resize(event.size())
            
        # Update status with window size
        size = event.size()
        self._show_status(f"Window resized to {size.width()}x{size.height()}")
        
    def closeEvent(self, event):
        """Handle application close"""
        # Log session completion
        logging.info("Demo application closing")
        
        if self.session_stats["total_attempts"] > 0:
            accuracy = (self.session_stats["correct_attempts"] / self.session_stats["total_attempts"]) * 100
            logging.info(f"Final session stats: {self.session_stats['total_attempts']} attempts, "
                        f"{accuracy:.1f}% accuracy")
        
        event.accept()


def create_splash_screen() -> QSplashScreen:
    """Create a splash screen for the demo application"""
    # Create a simple splash screen
    splash_pix = QPixmap(400, 200)
    splash_pix.fill(Qt.white)
    
    splash = QSplashScreen(splash_pix)
    splash.setWindowFlag(Qt.WindowStaysOnTopHint)
    
    splash.showMessage("Loading Optimized Layout Demo...", 
                      Qt.AlignCenter | Qt.AlignBottom, Qt.black)
    
    return splash


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Spanish Subjunctive Practice - Optimized Demo")
    app.setApplicationVersion("2.0.0")
    
    # Set application font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Show splash screen
    splash = create_splash_screen()
    splash.show()
    app.processEvents()
    
    # Log system information
    screen_info = get_screen_info()
    logging.info(f"Starting demo application on system with screens: {screen_info}")
    
    try:
        # Create and show main window
        window = OptimizedDemoApplication()
        
        # Hide splash and show main window
        splash.finish(window)
        window.show()
        
        # Start event loop
        sys.exit(app.exec_())
        
    except Exception as e:
        logging.error(f"Application error: {e}")
        splash.close()
        
        # Show error message
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setWindowTitle("Application Error")
        error_box.setText(f"An error occurred starting the application:\n\n{str(e)}")
        error_box.exec_()
        
        sys.exit(1)


if __name__ == "__main__":
    main()
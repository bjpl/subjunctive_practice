"""
Layout Integration Module
========================

This module provides integration utilities for upgrading the existing
Spanish Subjunctive Practice application to use the optimized layout system.

It demonstrates how to:
1. Migrate from the old 50-50 splitter to the new 70-30 layout
2. Connect the optimized layout to existing application logic
3. Maintain compatibility with existing features
4. Improve user experience with modern UI patterns
"""

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from typing import List, Dict, Optional
import logging

from .optimized_layout import OptimizedSubjunctiveLayout


class LayoutIntegrationMixin:
    """
    Mixin class to add optimized layout capabilities to the existing
    SpanishSubjunctivePracticeGUI class.
    
    This allows for gradual migration without breaking existing functionality.
    """
    
    def initialize_optimized_layout(self):
        """Initialize the optimized layout system"""
        # Create the optimized layout
        self.optimized_layout = OptimizedSubjunctiveLayout()
        
        # Connect signals to existing methods
        self._connect_optimized_signals()
        
        # Replace the central widget
        self.setCentralWidget(self.optimized_layout)
        
        # Migrate existing data to new layout
        self._migrate_ui_data()
        
        logging.info("Optimized layout initialized successfully")
        
    def _connect_optimized_signals(self):
        """Connect optimized layout signals to existing methods"""
        # Exercise generation
        self.optimized_layout.exercise_generated.connect(self.generateNewExercise)
        
        # Answer submission
        self.optimized_layout.answer_submitted.connect(self._handle_optimized_answer)
        
        # Hint request
        self.optimized_layout.hint_requested.connect(self.provideHint)
        
        # Navigation
        self.optimized_layout.navigation_requested.connect(self._handle_navigation)
        
        # Mode changes
        self.optimized_layout.mode_combo.currentTextChanged.connect(self._on_mode_changed)
        self.optimized_layout.task_type_combo.currentTextChanged.connect(self._on_task_type_changed)
        
    def _handle_optimized_answer(self, answer: str):
        """Handle answer submission from optimized layout"""
        # Set the answer in the appropriate input field for compatibility
        if self.optimized_layout.get_mode() == "Free Response":
            # Simulate the old free response input behavior
            self._simulate_free_response_input(answer)
        
        # Call existing submit method
        self.submitAnswer()
        
    def _handle_navigation(self, direction: str):
        """Handle navigation requests from optimized layout"""
        if direction == 'next':
            self.nextExercise()
        elif direction == 'prev':
            self.prevExercise()
            
    def _on_mode_changed(self, mode: str):
        """Handle mode changes in optimized layout"""
        self.optimized_layout.switch_input_mode(mode)
        if hasattr(self, 'switchMode'):
            self.switchMode()
            
    def _on_task_type_changed(self):
        """Handle task type changes in optimized layout"""
        task_types = ["traditional", "tblt", "contrast", "review"]
        index = self.optimized_layout.task_type_combo.currentIndex()
        if hasattr(self, 'current_task_type'):
            self.current_task_type = task_types[index] if index < len(task_types) else "traditional"
            
        if hasattr(self, 'onTaskTypeChanged'):
            self.onTaskTypeChanged(index)
            
    def _simulate_free_response_input(self, answer: str):
        """Simulate setting answer in old input system for compatibility"""
        # This maintains compatibility with existing validation logic
        if hasattr(self, 'free_response_input'):
            self.free_response_input.setText(answer)
            
    def _migrate_ui_data(self):
        """Migrate existing UI state to optimized layout"""
        # Migrate exercise content if available
        if hasattr(self, 'exercises') and self.exercises and hasattr(self, 'current_exercise'):
            if 0 <= self.current_exercise < len(self.exercises):
                exercise = self.exercises[self.current_exercise]
                sentence = exercise.get("sentence", "")
                translation = exercise.get("translation", "")
                self.optimized_layout.set_exercise_content(sentence, translation, getattr(self, 'show_translation', False))
                
        # Migrate progress information
        if hasattr(self, 'current_exercise') and hasattr(self, 'total_exercises'):
            current = getattr(self, 'current_exercise', 0) + 1
            total = getattr(self, 'total_exercises', 0)
            correct = getattr(self, 'correct_count', 0)
            accuracy = (correct / max(current - 1, 1)) * 100 if current > 1 else 0
            self.optimized_layout.update_progress(current, total, correct, accuracy)
            
        # Migrate streak information if available
        if hasattr(self, 'streak_tracker'):
            streak_info = self.streak_tracker.get_streak_info()
            self.optimized_layout.update_streak(
                streak_info.get('current', 0),
                streak_info.get('best', 0)
            )
            
    def update_optimized_exercise_display(self):
        """Update exercise display in optimized layout"""
        if not hasattr(self, 'optimized_layout'):
            return
            
        if hasattr(self, 'exercises') and self.exercises and hasattr(self, 'current_exercise'):
            if 0 <= self.current_exercise < len(self.exercises):
                exercise = self.exercises[self.current_exercise]
                
                # Prepare content
                sentence = exercise.get("sentence", "")
                context = exercise.get("context", "")
                if context:
                    full_text = f"{context}\n\n{sentence}"
                else:
                    full_text = sentence
                    
                translation = exercise.get("translation", "")
                show_translation = getattr(self, 'show_translation', False)
                
                # Update layout
                self.optimized_layout.set_exercise_content(full_text, translation, show_translation)
                
                # Handle multiple choice if needed
                mode = self.optimized_layout.get_mode()
                if mode == "Multiple Choice" and "choices" in exercise:
                    choices = exercise["choices"]
                    if isinstance(choices, list):
                        import random
                        shuffled_choices = choices.copy()
                        random.shuffle(shuffled_choices)
                        self.optimized_layout.set_multiple_choice_options(shuffled_choices)
                        
                # Clear previous input
                self.optimized_layout.clear_answer_input()
                self.optimized_layout.clear_feedback()
                
    def update_optimized_stats(self):
        """Update statistics in optimized layout"""
        if not hasattr(self, 'optimized_layout'):
            return
            
        current = getattr(self, 'current_exercise', 0) + 1
        total = getattr(self, 'total_exercises', 0)
        correct = getattr(self, 'correct_count', 0)
        
        # Calculate accuracy
        attempts = getattr(self, 'session_stats', {}).get('total_attempts', current - 1)
        accuracy = (correct / max(attempts, 1)) * 100 if attempts > 0 else 0
        
        self.optimized_layout.update_progress(current, total, correct, accuracy)
        
    def update_optimized_feedback(self, feedback: str):
        """Update feedback in optimized layout"""
        if hasattr(self, 'optimized_layout'):
            self.optimized_layout.set_feedback(feedback)
            
    def get_optimized_selections(self) -> Dict:
        """Get current selections from optimized layout"""
        if not hasattr(self, 'optimized_layout'):
            return {}
            
        return {
            'tenses': self.optimized_layout.get_selected_tenses(),
            'persons': self.optimized_layout.get_selected_persons(),
            'triggers': self.optimized_layout.get_selected_triggers(),
            'custom_context': self.optimized_layout.get_custom_context(),
            'specific_verbs': self.optimized_layout.get_specific_verbs(),
            'difficulty': self.optimized_layout.get_difficulty(),
            'mode': self.optimized_layout.get_mode(),
            'task_type': self.optimized_layout.get_task_type()
        }
        
    def validate_optimized_selections(self) -> tuple[bool, str]:
        """Validate selections in optimized layout"""
        selections = self.get_optimized_selections()
        
        if not selections['tenses']:
            return False, "Please select at least one tense."
            
        if not selections['persons']:
            return False, "Please select at least one person."
            
        # For traditional mode, require triggers
        if selections['task_type'] == "Traditional Grammar" and not selections['triggers']:
            return False, "Please select at least one subjunctive trigger for traditional grammar exercises."
            
        return True, "Selections are valid."
        
    def enable_optimized_navigation(self, prev: bool = True, next: bool = True, 
                                  submit: bool = True, hint: bool = True):
        """Enable/disable navigation buttons in optimized layout"""
        if not hasattr(self, 'optimized_layout'):
            return
            
        self.optimized_layout.set_button_enabled('prev', prev)
        self.optimized_layout.set_button_enabled('next', next)
        self.optimized_layout.set_button_enabled('submit', submit)
        self.optimized_layout.set_button_enabled('hint', hint)


class OptimizedSpanishSubjunctiveGUI(QMainWindow):
    """
    Demonstration of a fully optimized Spanish Subjunctive Practice GUI
    that uses the new layout system from the ground up.
    
    This shows how a new implementation would look.
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spanish Subjunctive Practice - Optimized")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize data structures
        self.exercises = []
        self.current_exercise = 0
        self.total_exercises = 0
        self.correct_count = 0
        self.session_stats = {
            "total_attempts": 0,
            "correct_attempts": 0,
            "hints_used": 0
        }
        
        # Setup optimized layout
        self.layout_widget = OptimizedSubjunctiveLayout()
        self.setCentralWidget(self.layout_widget)
        
        # Connect signals
        self._connect_signals()
        
        # Apply application-wide styling
        self._apply_global_styles()
        
        logging.info("Optimized Spanish Subjunctive GUI initialized")
        
    def _connect_signals(self):
        """Connect layout signals to application logic"""
        self.layout_widget.exercise_generated.connect(self.generate_exercises)
        self.layout_widget.answer_submitted.connect(self.submit_answer)
        self.layout_widget.hint_requested.connect(self.provide_hint)
        self.layout_widget.navigation_requested.connect(self.handle_navigation)
        
    def _apply_global_styles(self):
        """Apply global application styles"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            
            QToolTip {
                background-color: #333;
                color: white;
                border: 1px solid #555;
                padding: 4px;
                border-radius: 4px;
                font-size: 12px;
            }
        """)
        
    def generate_exercises(self):
        """Generate new exercises based on current selections"""
        # Validate selections
        valid, message = self._validate_selections()
        if not valid:
            QMessageBox.warning(self, "Invalid Selection", message)
            return
            
        # TODO: Implement exercise generation logic
        # This would integrate with your existing GPT-based generation
        self._show_status("Generating exercises...")
        
        # For demo purposes, create sample exercises
        self._create_sample_exercises()
        
    def _validate_selections(self) -> tuple[bool, str]:
        """Validate current selections"""
        tenses = self.layout_widget.get_selected_tenses()
        persons = self.layout_widget.get_selected_persons()
        
        if not tenses:
            return False, "Please select at least one tense."
            
        if not persons:
            return False, "Please select at least one person."
            
        return True, ""
        
    def _create_sample_exercises(self):
        """Create sample exercises for demonstration"""
        self.exercises = [
            {
                "context": "Your friend wants to travel",
                "sentence": "Espero que tu amigo _____ (viajar) a España pronto.",
                "answer": "viaje",
                "choices": ["viaja", "viaje", "viajará", "viajaba"],
                "translation": "I hope your friend travels to Spain soon."
            },
            {
                "context": "Expressing doubt",
                "sentence": "Dudo que ella _____ (tener) tiempo para estudiar.",
                "answer": "tenga",
                "choices": ["tiene", "tenga", "tendrá", "tenía"],
                "translation": "I doubt she has time to study."
            }
        ]
        
        self.total_exercises = len(self.exercises)
        self.current_exercise = 0
        self.correct_count = 0
        
        self._update_exercise_display()
        self._show_status(f"Generated {self.total_exercises} exercises")
        
    def _update_exercise_display(self):
        """Update the exercise display"""
        if not self.exercises or self.current_exercise >= len(self.exercises):
            return
            
        exercise = self.exercises[self.current_exercise]
        
        # Set content
        sentence = exercise.get("sentence", "")
        context = exercise.get("context", "")
        if context:
            full_text = f"**{context}**\n\n{sentence}"
        else:
            full_text = sentence
            
        translation = exercise.get("translation", "")
        self.layout_widget.set_exercise_content(full_text, translation, True)
        
        # Set multiple choice if available and mode is MC
        if (self.layout_widget.get_mode() == "Multiple Choice" and 
            "choices" in exercise):
            choices = exercise["choices"].copy()
            import random
            random.shuffle(choices)
            self.layout_widget.set_multiple_choice_options(choices)
        else:
            self.layout_widget.switch_input_mode(self.layout_widget.get_mode())
            
        # Update progress
        accuracy = (self.correct_count / max(self.session_stats["total_attempts"], 1)) * 100
        self.layout_widget.update_progress(
            self.current_exercise + 1, 
            self.total_exercises, 
            self.correct_count, 
            accuracy
        )
        
        # Update navigation buttons
        self.layout_widget.set_button_enabled('prev', self.current_exercise > 0)
        self.layout_widget.set_button_enabled('next', self.current_exercise < self.total_exercises - 1)
        
    def submit_answer(self, user_answer: str):
        """Handle answer submission"""
        if not user_answer.strip():
            self._show_status("Please provide an answer.")
            return
            
        if not self.exercises or self.current_exercise >= len(self.exercises):
            return
            
        exercise = self.exercises[self.current_exercise]
        correct_answer = exercise.get("answer", "").strip().lower()
        user_answer = user_answer.strip().lower()
        
        # Update stats
        self.session_stats["total_attempts"] += 1
        
        if user_answer == correct_answer:
            self.correct_count += 1
            self.session_stats["correct_attempts"] += 1
            feedback = f"✓ Correct! The answer is '{correct_answer}'."
            self._show_status("Correct answer!")
        else:
            feedback = f"✗ Incorrect. The correct answer is '{correct_answer}'."
            self._show_status("Incorrect answer.")
            
        # Add explanation (simplified for demo)
        feedback += f"\n\nThis sentence uses the subjunctive because it expresses {exercise.get('context', 'uncertainty')}."
        
        self.layout_widget.set_feedback(feedback)
        self._update_exercise_display()  # Update progress
        
    def provide_hint(self):
        """Provide a hint for the current exercise"""
        if not self.exercises or self.current_exercise >= len(self.exercises):
            return
            
        self.session_stats["hints_used"] += 1
        
        # Simple hint logic (could be enhanced with GPT)
        exercise = self.exercises[self.current_exercise]
        answer = exercise.get("answer", "")
        
        hint = f"💡 Hint: The answer starts with '{answer[0]}' and has {len(answer)} letters."
        self.layout_widget.set_feedback(hint)
        self._show_status("Hint provided")
        
    def handle_navigation(self, direction: str):
        """Handle navigation requests"""
        if direction == 'next' and self.current_exercise < self.total_exercises - 1:
            self.current_exercise += 1
            self.layout_widget.clear_feedback()
            self._update_exercise_display()
            self._show_status(f"Exercise {self.current_exercise + 1} of {self.total_exercises}")
            
        elif direction == 'prev' and self.current_exercise > 0:
            self.current_exercise -= 1
            self.layout_widget.clear_feedback()
            self._update_exercise_display()
            self._show_status(f"Exercise {self.current_exercise + 1} of {self.total_exercises}")
            
    def _show_status(self, message: str):
        """Show status message"""
        if hasattr(self, 'statusBar'):
            self.statusBar().showMessage(message, 3000)
        logging.info(f"Status: {message}")


def demonstrate_integration():
    """
    Demonstrate how to integrate the optimized layout into an existing application
    """
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    # Create the optimized GUI
    gui = OptimizedSpanishSubjunctiveGUI()
    gui.show()
    
    return app.exec_()


if __name__ == "__main__":
    demonstrate_integration()
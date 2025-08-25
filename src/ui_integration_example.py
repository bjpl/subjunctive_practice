"""
Integration Example: How to integrate UIInteractionManager with the main application

This file demonstrates how to modify the existing SpanishSubjunctivePracticeGUI 
to use the new UIInteractionManager for optimal user experience.
"""

from typing import Optional
import logging
from src.ui_interactions import UIInteractionManager, SmartNavigation, InteractionState

logger = logging.getLogger(__name__)


class EnhancedSpanishSubjunctivePracticeGUI:
    """
    Example of how to integrate UIInteractionManager with the main GUI class.
    
    Key Integration Points:
    1. Initialize interaction manager in __init__
    2. Connect existing methods to interaction manager
    3. Update event handlers to use interaction states
    4. Add enhanced keyboard shortcuts and feedback
    """
    
    def __init__(self):
        # ... existing initialization code ...
        
        # Initialize UI interaction management
        self.ui_manager = UIInteractionManager(self)
        self.smart_nav = SmartNavigation(self.ui_manager)
        
        # Connect existing methods to interaction manager
        self._connect_interaction_signals()
        
        # Set initial state
        self.ui_manager.set_state(InteractionState.SETUP)
        
        logger.info("Enhanced GUI with UI interaction management initialized")

    def _connect_interaction_signals(self):
        """Connect existing GUI methods to the interaction manager"""
        
        # Override existing button connections to use interaction manager
        if hasattr(self, 'submit_button'):
            # Disconnect existing connection
            try:
                self.submit_button.clicked.disconnect()
            except TypeError:
                pass  # No connections existed
            
            # Connect to interaction manager
            self.submit_button.clicked.connect(self._on_submit_with_interaction)
        
        # Connect navigation buttons
        if hasattr(self, 'next_button'):
            try:
                self.next_button.clicked.disconnect()
            except TypeError:
                pass
            self.next_button.clicked.connect(lambda: self.ui_manager.handle_exercise_navigation("next"))
        
        if hasattr(self, 'prev_button'):
            try:
                self.prev_button.clicked.disconnect()
            except TypeError:
                pass
            self.prev_button.clicked.connect(lambda: self.ui_manager.handle_exercise_navigation("previous"))

    def _on_submit_with_interaction(self):
        """Enhanced submit handler that uses interaction manager"""
        current_state = self.ui_manager.get_current_state()
        
        if current_state == InteractionState.SETUP:
            # Generate new exercises
            if self.ui_manager._validate_required_selections():
                self.generateNewExercise()
                self.ui_manager.enable_practice_mode()
            return
        
        elif current_state == InteractionState.PRACTICING:
            # Submit answer with enhanced feedback
            if self.total_exercises == 0:
                self.ui_manager._show_feedback(
                    self.ui_manager.FeedbackType.INCORRECT,
                    "No hay ejercicios disponibles"
                )
                return
            
            user_answer = self.getUserAnswer()
            if not user_answer:
                self.ui_manager._show_feedback(
                    self.ui_manager.FeedbackType.INCORRECT,
                    "Por favor proporciona una respuesta"
                )
                return
            
            # Process answer with interaction feedback
            self._process_answer_with_feedback(user_answer)

    def _process_answer_with_feedback(self, user_answer: str):
        """Process answer submission with enhanced interaction feedback"""
        exercise = self.exercises[self.current_exercise]
        correct_answer = exercise.get("answer", "").strip().lower()
        is_correct = user_answer.lower() == correct_answer
        
        # Update session stats (existing logic)
        self.session_stats["total_attempts"] += 1
        if is_correct:
            self.correct_count += 1
            self.session_stats["correct_attempts"] += 1
        
        # Use interaction manager for feedback
        self.ui_manager.handle_answer_submission(is_correct, user_answer, correct_answer)
        
        # Continue with existing GPT explanation logic
        self.generateGPTExplanationAsync(
            user_answer, correct_answer, is_correct, 
            exercise.get("sentence", ""), 
            "Correct!" if is_correct else f"Incorrect. The answer is '{correct_answer}'."
        )
        
        # Smart navigation: auto-advance if enabled and correct
        if is_correct and self.smart_nav.auto_advance_enabled:
            from PyQt5.QtCore import QTimer
            QTimer.singleShot(self.smart_nav.auto_advance_delay, 
                            lambda: self.ui_manager.handle_exercise_navigation("next"))

    def generateNewExercise(self):
        """Enhanced exercise generation with interaction state management"""
        # Call original method
        super().generateNewExercise() if hasattr(super(), 'generateNewExercise') else self._original_generate_new_exercise()
        
        # Update interaction state
        if self.exercises:  # If exercises were generated successfully
            self.ui_manager.enable_practice_mode()

    def nextExercise(self):
        """Enhanced next exercise with interaction management"""
        if self.total_exercises == 0:
            self.ui_manager._show_feedback(
                self.ui_manager.FeedbackType.INCORRECT,
                "No hay ejercicios disponibles"
            )
            return
        
        if self.current_exercise < self.total_exercises - 1:
            self.current_exercise += 1
            self.updateExercise()
            # Keep in practicing state
            self.ui_manager.set_state(InteractionState.PRACTICING)
        else:
            self.ui_manager._show_feedback(
                self.ui_manager.FeedbackType.NEUTRAL,
                "Estás en el último ejercicio"
            )

    def prevExercise(self):
        """Enhanced previous exercise with interaction management"""
        if self.total_exercises == 0:
            self.ui_manager._show_feedback(
                self.ui_manager.FeedbackType.INCORRECT,
                "No hay ejercicios disponibles"
            )
            return
        
        if self.current_exercise > 0:
            self.current_exercise -= 1
            self.updateExercise()
            # Keep in practicing state
            self.ui_manager.set_state(InteractionState.PRACTICING)
        else:
            self.ui_manager._show_feedback(
                self.ui_manager.FeedbackType.NEUTRAL,
                "Estás en el primer ejercicio"
            )

    def startReviewMode(self):
        """Enhanced review mode with interaction management"""
        # Call original method
        super().startReviewMode() if hasattr(super(), 'startReviewMode') else self._original_start_review_mode()
        
        # Update interaction state
        self.ui_manager.enable_review_mode()

    def updateExercise(self):
        """Enhanced exercise update with state-aware focus management"""
        # Call original method
        super().updateExercise() if hasattr(super(), 'updateExercise') else self._original_update_exercise()
        
        # Set appropriate focus based on mode
        current_state = self.ui_manager.get_current_state()
        if current_state == InteractionState.PRACTICING:
            # Focus on input field
            if hasattr(self, 'mode_combo'):
                mode = self.mode_combo.currentText()
                if mode == "Free Response" and hasattr(self, 'free_response_input'):
                    self.free_response_input.setFocus()
                    self.free_response_input.selectAll()  # Select all for easy overwriting

    def keyPressEvent(self, event):
        """Enhanced key handling with interaction manager integration"""
        # Let interaction manager handle first
        # The UIInteractionManager's shortcuts will handle most cases
        
        # Handle special cases that need direct GUI access
        if event.key() == Qt.Key_Escape:
            # ESC key for quick exit from modes
            current_state = self.ui_manager.get_current_state()
            if current_state == InteractionState.REVIEW:
                # Exit review mode
                self.ui_manager.set_state(InteractionState.SETUP)
                self.review_mode = False
                return
        
        # Call parent implementation
        super().keyPressEvent(event)

    def showEvent(self, event):
        """Enhanced show event with smart focus management"""
        super().showEvent(event) if hasattr(super(), 'showEvent') else None
        
        # Set initial focus based on current state
        current_state = self.ui_manager.get_current_state()
        if current_state == InteractionState.SETUP:
            # Focus on first trigger checkbox
            if hasattr(self, 'trigger_checkboxes') and self.trigger_checkboxes:
                self.trigger_checkboxes[0].setFocus()
        elif current_state == InteractionState.PRACTICING:
            # Focus on input field
            if hasattr(self, 'free_response_input'):
                self.free_response_input.setFocus()

    def closeEvent(self, event):
        """Enhanced close event with interaction cleanup"""
        # Disable shortcuts to prevent issues during shutdown
        if hasattr(self, 'ui_manager'):
            self.ui_manager.disable_all_shortcuts()
        
        # Call original close event
        super().closeEvent(event)

    # Helper methods for backward compatibility
    def _original_generate_new_exercise(self):
        """Placeholder for original generateNewExercise logic"""
        # This would contain the original logic if not calling super()
        pass

    def _original_start_review_mode(self):
        """Placeholder for original startReviewMode logic"""
        # This would contain the original logic if not calling super()
        pass

    def _original_update_exercise(self):
        """Placeholder for original updateExercise logic"""
        # This would contain the original logic if not calling super()
        pass

    # New convenience methods enabled by interaction manager
    def get_suggested_action(self) -> str:
        """Get suggestion for next user action"""
        return self.smart_nav.suggest_next_action()

    def get_relevant_shortcuts(self) -> list:
        """Get keyboard shortcuts relevant to current state"""
        return self.smart_nav.get_navigation_shortcuts_for_state()

    def enable_auto_advance(self, delay_ms: int = 2000):
        """Enable automatic advancement after correct answers"""
        self.smart_nav.enable_auto_advance(delay_ms)

    def show_contextual_help(self):
        """Show help relevant to current interaction state"""
        shortcuts = self.get_relevant_shortcuts()
        suggestion = self.get_suggested_action()
        
        help_text = f"<b>Sugerencia:</b> {suggestion}<br><br>"
        if shortcuts:
            help_text += "<b>Atajos útiles:</b><br>"
            for shortcut in shortcuts[:5]:  # Show max 5 shortcuts
                help_text += f"• {shortcut}<br>"
        
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, "Ayuda Contextual", help_text)


def create_enhanced_gui():
    """Factory function to create enhanced GUI with interaction management"""
    # This would replace the original SpanishSubjunctivePracticeGUI instantiation
    return EnhancedSpanishSubjunctivePracticeGUI()


# Integration checklist for existing code:
"""
INTEGRATION CHECKLIST:

1. □ Import ui_interactions module
   from src.ui_interactions import UIInteractionManager, SmartNavigation, InteractionState

2. □ Add interaction manager to __init__:
   self.ui_manager = UIInteractionManager(self)
   self.smart_nav = SmartNavigation(self.ui_manager)

3. □ Update button connections:
   # Replace direct connections with interaction-aware ones
   self.submit_button.clicked.connect(self._on_submit_with_interaction)

4. □ Enhance key methods:
   # Add state management to key methods like submitAnswer(), nextExercise()

5. □ Add state transitions:
   # Call self.ui_manager.set_state() at appropriate points

6. □ Update focus management:
   # Use interaction states to set appropriate focus

7. □ Add enhanced feedback:
   # Replace basic status updates with rich interaction feedback

8. □ Test keyboard shortcuts:
   # Verify all new shortcuts work correctly

9. □ Test state transitions:
   # Ensure smooth flow between setup -> practice -> feedback

10. □ Add contextual help:
    # Implement state-aware help system

BENEFITS AFTER INTEGRATION:
• Intuitive keyboard shortcuts for all actions
• State-aware focus management
• Smooth visual transitions
• Clear feedback for all user actions
• Logical grouping of related functions
• Auto-advance options for fluent practice
• Contextual help based on current activity
"""
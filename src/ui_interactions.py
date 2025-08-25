"""
UI Interactions Module for Spanish Subjunctive Practice App

This module provides optimized user interaction flows with:
1. Streamlined navigation between practice modes
2. Clear feedback for correct/incorrect answers
3. Intuitive keyboard shortcuts
4. Smooth transitions between screens
5. Logical grouping of related functions
"""

from typing import Dict, List, Optional, Callable, Any
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QStackedWidget, QGroupBox, QButtonGroup, QRadioButton,
    QLineEdit, QTextEdit, QProgressBar, QFrame, QSizePolicy,
    QMessageBox, QApplication, QShortcut, QComboBox
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, pyqtSignal, QTimer
from PyQt5.QtGui import QKeySequence, QPalette, QFont
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class InteractionState(Enum):
    """Defines different interaction states for the practice app"""
    SETUP = "setup"
    PRACTICING = "practicing"
    FEEDBACK = "feedback"
    NAVIGATION = "navigation"
    REVIEW = "review"


class FeedbackType(Enum):
    """Different types of feedback to display"""
    CORRECT = "correct"
    INCORRECT = "incorrect"
    HINT = "hint"
    NEUTRAL = "neutral"


class UIInteractionManager:
    """
    Manages user interactions and provides streamlined navigation flows.
    Coordinates between different UI components for optimal user experience.
    """
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.current_state = InteractionState.SETUP
        self.feedback_animations = {}
        self.transition_animations = {}
        self.keyboard_shortcuts = {}
        
        # Initialize interaction components
        self._setup_keyboard_shortcuts()
        self._setup_feedback_system()
        self._setup_navigation_flow()
        
        logger.info("UI Interaction Manager initialized")

    def _setup_keyboard_shortcuts(self):
        """Configure intuitive keyboard shortcuts for common actions"""
        shortcuts = {
            # Primary actions
            'submit': ('Return', 'Enter', 'Space'),
            'next': ('Right', 'N', 'Ctrl+Right'),
            'previous': ('Left', 'P', 'Ctrl+Left'),
            'hint': ('H', 'Ctrl+H', '?'),
            
            # Mode switching
            'toggle_mode': ('Tab', 'M'),
            'review_mode': ('R', 'Ctrl+R'),
            'new_exercise': ('Ctrl+N', 'F5'),
            
            # Quick settings
            'toggle_translation': ('T', 'Ctrl+T'),
            'toggle_theme': ('Ctrl+D',),
            'show_stats': ('S', 'Ctrl+S'),
            
            # Navigation
            'first_exercise': ('Home', 'Ctrl+Home'),
            'last_exercise': ('End', 'Ctrl+End'),
            'jump_to': ('G', 'Ctrl+G'),
            
            # Help and reference
            'help': ('F1', 'Ctrl+?'),
            'conjugation_ref': ('Ctrl+R', 'F2'),
            'quick_summary': ('Ctrl+I',)
        }
        
        for action, keys in shortcuts.items():
            self.keyboard_shortcuts[action] = []
            for key in keys:
                shortcut = QShortcut(QKeySequence(key), self.main_window)
                shortcut.activated.connect(getattr(self, f'_handle_{action}', self._default_handler))
                self.keyboard_shortcuts[action].append(shortcut)

    def _setup_feedback_system(self):
        """Initialize visual feedback system for immediate user response"""
        self.feedback_colors = {
            FeedbackType.CORRECT: "#27ae60",    # Green
            FeedbackType.INCORRECT: "#e74c3c",  # Red
            FeedbackType.HINT: "#f39c12",       # Orange
            FeedbackType.NEUTRAL: "#3498db"     # Blue
        }
        
        self.feedback_messages = {
            FeedbackType.CORRECT: "¡Excelente! 🎉",
            FeedbackType.INCORRECT: "Inténtalo de nuevo 🤔",
            FeedbackType.HINT: "Pista 💡",
            FeedbackType.NEUTRAL: "Continúa practicando 📚"
        }

    def _setup_navigation_flow(self):
        """Configure smooth navigation flow between different screens"""
        self.navigation_states = {
            InteractionState.SETUP: {
                'next_states': [InteractionState.PRACTICING],
                'required_selections': ['triggers', 'tenses', 'persons'],
                'primary_action': 'generate_exercises'
            },
            InteractionState.PRACTICING: {
                'next_states': [InteractionState.FEEDBACK, InteractionState.NAVIGATION],
                'required_selections': [],
                'primary_action': 'submit_answer'
            },
            InteractionState.FEEDBACK: {
                'next_states': [InteractionState.PRACTICING, InteractionState.NAVIGATION],
                'required_selections': [],
                'primary_action': 'continue_practice'
            },
            InteractionState.NAVIGATION: {
                'next_states': [InteractionState.PRACTICING, InteractionState.REVIEW, InteractionState.SETUP],
                'required_selections': [],
                'primary_action': 'navigate'
            },
            InteractionState.REVIEW: {
                'next_states': [InteractionState.PRACTICING, InteractionState.SETUP],
                'required_selections': [],
                'primary_action': 'review_items'
            }
        }

    # Keyboard shortcut handlers
    def _handle_submit(self):
        """Handle submit action based on current state"""
        if self.current_state == InteractionState.SETUP:
            if self._validate_required_selections():
                self.main_window.generateNewExercise()
                self._transition_to_state(InteractionState.PRACTICING)
        elif self.current_state == InteractionState.PRACTICING:
            self.main_window.submitAnswer()
            self._transition_to_state(InteractionState.FEEDBACK)

    def _handle_next(self):
        """Navigate to next exercise with smooth transition"""
        if hasattr(self.main_window, 'nextExercise'):
            self.main_window.nextExercise()
            self._show_transition_feedback("➡️ Siguiente ejercicio")

    def _handle_previous(self):
        """Navigate to previous exercise with smooth transition"""
        if hasattr(self.main_window, 'prevExercise'):
            self.main_window.prevExercise()
            self._show_transition_feedback("⬅️ Ejercicio anterior")

    def _handle_hint(self):
        """Provide hint with visual feedback"""
        if hasattr(self.main_window, 'provideHint'):
            self.main_window.provideHint()
            self._show_feedback(FeedbackType.HINT, "💡 Pista disponible")

    def _handle_toggle_mode(self):
        """Switch between Free Response and Multiple Choice modes"""
        if hasattr(self.main_window, 'mode_combo'):
            combo = self.main_window.mode_combo
            current_index = combo.currentIndex()
            next_index = (current_index + 1) % combo.count()
            combo.setCurrentIndex(next_index)
            mode_name = combo.currentText()
            self._show_feedback(FeedbackType.NEUTRAL, f"Modo: {mode_name}")

    def _handle_review_mode(self):
        """Switch to review mode"""
        if hasattr(self.main_window, 'startReviewMode'):
            self.main_window.startReviewMode()
            self._transition_to_state(InteractionState.REVIEW)

    def _handle_new_exercise(self):
        """Generate new exercises"""
        if hasattr(self.main_window, 'generateNewExercise'):
            self.main_window.generateNewExercise()

    def _handle_toggle_translation(self):
        """Toggle translation visibility"""
        if hasattr(self.main_window, 'toggleTranslation'):
            self.main_window.toggleTranslation()

    def _handle_toggle_theme(self):
        """Toggle between light and dark themes"""
        if hasattr(self.main_window, 'toggleTheme'):
            self.main_window.toggleTheme()

    def _handle_show_stats(self):
        """Show detailed statistics"""
        if hasattr(self.main_window, 'showDetailedStats'):
            self.main_window.showDetailedStats()

    def _handle_first_exercise(self):
        """Jump to first exercise"""
        if hasattr(self.main_window, 'current_exercise'):
            self.main_window.current_exercise = 0
            if hasattr(self.main_window, 'updateExercise'):
                self.main_window.updateExercise()
            self._show_transition_feedback("⏮️ Primer ejercicio")

    def _handle_last_exercise(self):
        """Jump to last exercise"""
        if hasattr(self.main_window, 'current_exercise') and hasattr(self.main_window, 'total_exercises'):
            self.main_window.current_exercise = max(0, self.main_window.total_exercises - 1)
            if hasattr(self.main_window, 'updateExercise'):
                self.main_window.updateExercise()
            self._show_transition_feedback("⏭️ Último ejercicio")

    def _handle_jump_to(self):
        """Show dialog to jump to specific exercise"""
        self._show_jump_to_dialog()

    def _handle_help(self):
        """Show help information"""
        self._show_help_dialog()

    def _handle_conjugation_ref(self):
        """Show conjugation reference"""
        if hasattr(self.main_window, 'showConjugationReference'):
            self.main_window.showConjugationReference()

    def _handle_quick_summary(self):
        """Show quick session summary"""
        self._show_quick_summary()

    def _default_handler(self):
        """Default handler for unimplemented shortcuts"""
        logger.warning("Keyboard shortcut handler not implemented")

    # State management
    def _transition_to_state(self, new_state: InteractionState):
        """Smoothly transition between interaction states"""
        old_state = self.current_state
        self.current_state = new_state
        
        logger.info(f"State transition: {old_state.value} -> {new_state.value}")
        
        # Trigger state-specific UI updates
        self._update_ui_for_state(new_state)
        
        # Show transition animation
        self._animate_state_transition(old_state, new_state)

    def _update_ui_for_state(self, state: InteractionState):
        """Update UI elements based on current state"""
        state_configs = {
            InteractionState.SETUP: {
                'focus_element': 'trigger_checkboxes',
                'highlight_sections': ['selections', 'options'],
                'show_help_text': 'Selecciona las opciones para generar ejercicios'
            },
            InteractionState.PRACTICING: {
                'focus_element': 'answer_input',
                'highlight_sections': ['exercise', 'input'],
                'show_help_text': 'Escribe tu respuesta y presiona Enter'
            },
            InteractionState.FEEDBACK: {
                'focus_element': 'feedback_area',
                'highlight_sections': ['feedback', 'navigation'],
                'show_help_text': 'Lee la explicación y continúa con el siguiente'
            },
            InteractionState.NAVIGATION: {
                'focus_element': 'navigation_buttons',
                'highlight_sections': ['controls'],
                'show_help_text': 'Usa las flechas para navegar entre ejercicios'
            },
            InteractionState.REVIEW: {
                'focus_element': 'review_area',
                'highlight_sections': ['exercise', 'review_info'],
                'show_help_text': 'Repasa los ejercicios incorrectos'
            }
        }
        
        config = state_configs.get(state, {})
        self._apply_ui_config(config)

    def _apply_ui_config(self, config: Dict):
        """Apply UI configuration for current state"""
        # Focus management
        focus_element = config.get('focus_element')
        if focus_element and hasattr(self.main_window, focus_element):
            element = getattr(self.main_window, focus_element)
            if hasattr(element, 'setFocus'):
                element.setFocus()

        # Update help text
        help_text = config.get('show_help_text')
        if help_text and hasattr(self.main_window, 'updateStatus'):
            self.main_window.updateStatus(help_text)

    # Validation and feedback
    def _validate_required_selections(self) -> bool:
        """Validate that required selections are made"""
        if not hasattr(self.main_window, 'getSelectedTriggers'):
            return False
            
        selected_triggers = self.main_window.getSelectedTriggers()
        selected_tenses = self.main_window.getSelectedTenses() if hasattr(self.main_window, 'getSelectedTenses') else []
        selected_persons = self.main_window.getSelectedPersons() if hasattr(self.main_window, 'getSelectedPersons') else []
        
        missing = []
        if not selected_triggers:
            missing.append("subjunctive triggers")
        if not selected_tenses:
            missing.append("tenses")
        if not selected_persons:
            missing.append("persons")
        
        if missing:
            error_msg = f"Por favor selecciona: {', '.join(missing)}"
            self._show_feedback(FeedbackType.INCORRECT, error_msg)
            QMessageBox.warning(self.main_window, "Selecciones requeridas", 
                              f"Debes seleccionar: {', '.join(missing)}")
            return False
        
        return True

    def _show_feedback(self, feedback_type: FeedbackType, message: str, duration: int = 3000):
        """Show visual feedback to user"""
        if hasattr(self.main_window, 'updateStatus'):
            self.main_window.updateStatus(f"{self.feedback_messages[feedback_type]} {message}")
        
        # Could add more sophisticated visual feedback here
        logger.info(f"Feedback: {feedback_type.value} - {message}")

    def _show_transition_feedback(self, message: str):
        """Show brief transition feedback"""
        self._show_feedback(FeedbackType.NEUTRAL, message, duration=1500)

    # Animation helpers
    def _animate_state_transition(self, old_state: InteractionState, new_state: InteractionState):
        """Add smooth animations for state transitions"""
        # This could include fade effects, sliding animations, etc.
        # For now, we'll just log the transition
        logger.info(f"Animated transition from {old_state.value} to {new_state.value}")

    # Dialog helpers
    def _show_jump_to_dialog(self):
        """Show dialog to jump to specific exercise"""
        if not hasattr(self.main_window, 'total_exercises') or self.main_window.total_exercises == 0:
            QMessageBox.information(self.main_window, "Sin ejercicios", 
                                  "No hay ejercicios disponibles. Genera algunos primero.")
            return
            
        from PyQt5.QtWidgets import QInputDialog
        exercise_num, ok = QInputDialog.getInt(
            self.main_window, 
            "Saltar a ejercicio",
            f"Número de ejercicio (1-{self.main_window.total_exercises}):",
            1, 1, self.main_window.total_exercises
        )
        
        if ok:
            self.main_window.current_exercise = exercise_num - 1
            if hasattr(self.main_window, 'updateExercise'):
                self.main_window.updateExercise()
            self._show_transition_feedback(f"📍 Ejercicio {exercise_num}")

    def _show_help_dialog(self):
        """Show help dialog with keyboard shortcuts"""
        help_text = """
<h3>Atajos de Teclado</h3>

<b>Acciones Principales:</b><br>
• <b>Enter/Espacio</b>: Enviar respuesta<br>
• <b>→/N</b>: Siguiente ejercicio<br>
• <b>←/P</b>: Ejercicio anterior<br>
• <b>H/?</b>: Mostrar pista<br>

<b>Modos:</b><br>
• <b>Tab/M</b>: Cambiar modo<br>
• <b>R</b>: Modo revisión<br>
• <b>Ctrl+N/F5</b>: Nuevos ejercicios<br>

<b>Configuración:</b><br>
• <b>T</b>: Mostrar/ocultar traducción<br>
• <b>Ctrl+D</b>: Cambiar tema<br>
• <b>S</b>: Mostrar estadísticas<br>

<b>Navegación:</b><br>
• <b>Home</b>: Primer ejercicio<br>
• <b>End</b>: Último ejercicio<br>
• <b>G</b>: Saltar a ejercicio<br>

<b>Ayuda:</b><br>
• <b>F1</b>: Esta ayuda<br>
• <b>F2</b>: Referencia de conjugación<br>
• <b>Ctrl+I</b>: Resumen rápido<br>
        """
        
        QMessageBox.information(self.main_window, "Ayuda - Atajos de Teclado", help_text)

    def _show_quick_summary(self):
        """Show quick session summary"""
        if not hasattr(self.main_window, 'session_stats'):
            QMessageBox.information(self.main_window, "Sin datos", 
                                  "No hay datos de sesión disponibles.")
            return
            
        stats = self.main_window.session_stats
        accuracy = 0
        if stats["total_attempts"] > 0:
            accuracy = (stats["correct_attempts"] / stats["total_attempts"]) * 100
        
        summary = f"""
<h3>Resumen Rápido</h3>

<b>Intentos:</b> {stats["total_attempts"]}<br>
<b>Correctos:</b> {stats["correct_attempts"]}<br>
<b>Precisión:</b> {accuracy:.1f}%<br>
<b>Pistas usadas:</b> {stats["hints_used"]}<br>

<b>Estado:</b> {"¡Excelente trabajo! 🎉" if accuracy >= 80 else "¡Sigue practicando! 💪" if accuracy >= 60 else "Necesitas más práctica 📚"}
        """
        
        QMessageBox.information(self.main_window, "Resumen de Sesión", summary)

    # Public interface methods
    def set_state(self, state: InteractionState):
        """Manually set interaction state"""
        self._transition_to_state(state)

    def get_current_state(self) -> InteractionState:
        """Get current interaction state"""
        return self.current_state

    def handle_answer_submission(self, is_correct: bool, user_answer: str, correct_answer: str):
        """Handle answer submission with appropriate feedback"""
        if is_correct:
            self._show_feedback(FeedbackType.CORRECT, f"¡Correcto! '{user_answer}'")
        else:
            self._show_feedback(FeedbackType.INCORRECT, f"Incorrecto. Respuesta: '{correct_answer}'")
        
        self._transition_to_state(InteractionState.FEEDBACK)

    def handle_exercise_navigation(self, direction: str):
        """Handle exercise navigation with visual feedback"""
        if direction == "next":
            self._handle_next()
        elif direction == "previous":
            self._handle_previous()
        elif direction == "first":
            self._handle_first_exercise()
        elif direction == "last":
            self._handle_last_exercise()

    def enable_practice_mode(self):
        """Enable practice mode optimizations"""
        self._transition_to_state(InteractionState.PRACTICING)
        
        # Set focus to input field
        if hasattr(self.main_window, 'free_response_input'):
            self.main_window.free_response_input.setFocus()
        
        # Update status
        self._show_feedback(FeedbackType.NEUTRAL, "¡Modo práctica activado!")

    def enable_review_mode(self):
        """Enable review mode optimizations"""
        self._transition_to_state(InteractionState.REVIEW)
        self._show_feedback(FeedbackType.NEUTRAL, "Revisando ejercicios incorrectos...")

    def disable_all_shortcuts(self):
        """Disable all keyboard shortcuts (for dialogs, etc.)"""
        for shortcuts in self.keyboard_shortcuts.values():
            for shortcut in shortcuts:
                shortcut.setEnabled(False)

    def enable_all_shortcuts(self):
        """Re-enable all keyboard shortcuts"""
        for shortcuts in self.keyboard_shortcuts.values():
            for shortcut in shortcuts:
                shortcut.setEnabled(True)


class SmartNavigation:
    """
    Provides intelligent navigation features based on user behavior and progress
    """
    
    def __init__(self, interaction_manager: UIInteractionManager):
        self.interaction_manager = interaction_manager
        self.navigation_history = []
        self.auto_advance_enabled = False
        self.smart_hints_enabled = True
        
    def enable_auto_advance(self, delay_ms: int = 2000):
        """Enable automatic advancement to next exercise after correct answers"""
        self.auto_advance_enabled = True
        self.auto_advance_delay = delay_ms
        
    def suggest_next_action(self) -> str:
        """Suggest the most appropriate next action based on current context"""
        state = self.interaction_manager.get_current_state()
        
        suggestions = {
            InteractionState.SETUP: "Selecciona opciones y genera ejercicios",
            InteractionState.PRACTICING: "Responde y presiona Enter",
            InteractionState.FEEDBACK: "Lee la explicación y continúa",
            InteractionState.NAVIGATION: "Usa las flechas para navegar",
            InteractionState.REVIEW: "Revisa los ejercicios incorrectos"
        }
        
        return suggestions.get(state, "Continúa practicando")

    def get_navigation_shortcuts_for_state(self) -> List[str]:
        """Get relevant keyboard shortcuts for current state"""
        state = self.interaction_manager.get_current_state()
        
        shortcuts = {
            InteractionState.SETUP: ["Ctrl+N: Generar", "Tab: Cambiar modo"],
            InteractionState.PRACTICING: ["Enter: Enviar", "H: Pista", "→: Siguiente"],
            InteractionState.FEEDBACK: ["→: Siguiente", "←: Anterior", "R: Revisar"],
            InteractionState.NAVIGATION: ["→←: Navegar", "Home/End: Saltar", "G: Ir a..."],
            InteractionState.REVIEW: ["Enter: Intentar", "Esc: Salir revisión"]
        }
        
        return shortcuts.get(state, [])


# Export main classes
__all__ = [
    'UIInteractionManager',
    'SmartNavigation', 
    'InteractionState',
    'FeedbackType'
]
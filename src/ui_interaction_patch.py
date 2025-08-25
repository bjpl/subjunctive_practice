"""
UI Interaction Patch for Existing main.py

This module provides minimal modifications to integrate UI interaction improvements
into the existing SpanishSubjunctivePracticeGUI without major refactoring.

Usage:
1. Import this module in main.py
2. Call apply_ui_enhancements(window) after creating the GUI
3. Enjoy improved user interactions!
"""

import logging
from typing import Optional, Dict, Any
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QShortcut
from PyQt5.QtGui import QKeySequence

logger = logging.getLogger(__name__)


class UIEnhancementPatch:
    """
    Lightweight patch to add UI interaction improvements to existing GUI.
    
    This provides the key benefits of the full UIInteractionManager
    without requiring major code changes.
    """
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.enhanced_shortcuts = []
        self.feedback_timer = QTimer()
        self.auto_advance_enabled = False
        
        logger.info("UI Enhancement Patch initialized")

    def apply_enhancements(self):
        """Apply all UI enhancements to the main window"""
        self._add_enhanced_shortcuts()
        self._enhance_feedback_system()
        self._improve_navigation_flow()
        self._add_smart_focus_management()
        
        logger.info("UI enhancements applied successfully")

    def _add_enhanced_shortcuts(self):
        """Add intuitive keyboard shortcuts"""
        shortcuts = [
            # Navigation shortcuts
            ('Ctrl+Right', self._next_exercise_smart),
            ('Ctrl+Left', self._prev_exercise_smart),
            ('Home', self._first_exercise),
            ('End', self._last_exercise),
            ('Ctrl+G', self._jump_to_exercise),
            
            # Mode shortcuts  
            ('Tab', self._toggle_mode_smart),
            ('Ctrl+M', self._toggle_mode_smart),
            ('Ctrl+R', self._toggle_review_mode),
            
            # Quick actions
            ('F5', self._generate_exercises_smart),
            ('Ctrl+N', self._generate_exercises_smart),
            ('Ctrl+T', self._toggle_translation_smart),
            ('Ctrl+D', self._toggle_theme_smart),
            
            # Help shortcuts
            ('F1', self._show_contextual_help),
            ('Ctrl+?', self._show_contextual_help),
            ('Ctrl+H', self._show_contextual_help),
            
            # Quick stats
            ('Ctrl+I', self._show_quick_stats),
            ('Ctrl+S', self._show_detailed_stats_smart)
        ]
        
        for key_seq, handler in shortcuts:
            shortcut = QShortcut(QKeySequence(key_seq), self.main_window)
            shortcut.activated.connect(handler)
            self.enhanced_shortcuts.append(shortcut)
            
        logger.info(f"Added {len(shortcuts)} enhanced keyboard shortcuts")

    def _enhance_feedback_system(self):
        """Enhance the feedback system with better visual cues"""
        # Store original submitAnswer method
        if hasattr(self.main_window, 'submitAnswer'):
            self.main_window._original_submitAnswer = self.main_window.submitAnswer
            self.main_window.submitAnswer = self._enhanced_submit_answer
        
        # Store original updateStatus method  
        if hasattr(self.main_window, 'updateStatus'):
            self.main_window._original_updateStatus = self.main_window.updateStatus
            self.main_window.updateStatus = self._enhanced_update_status

    def _improve_navigation_flow(self):
        """Improve navigation flow between exercises"""
        # Enhance next/prev methods with better feedback
        if hasattr(self.main_window, 'nextExercise'):
            self.main_window._original_nextExercise = self.main_window.nextExercise
            self.main_window.nextExercise = self._enhanced_next_exercise
            
        if hasattr(self.main_window, 'prevExercise'):
            self.main_window._original_prevExercise = self.main_window.prevExercise
            self.main_window.prevExercise = self._enhanced_prev_exercise

    def _add_smart_focus_management(self):
        """Add intelligent focus management"""
        # Enhance updateExercise for better focus
        if hasattr(self.main_window, 'updateExercise'):
            self.main_window._original_updateExercise = self.main_window.updateExercise
            self.main_window.updateExercise = self._enhanced_update_exercise

    # Enhanced method implementations
    def _enhanced_submit_answer(self):
        """Enhanced submit answer with better feedback"""
        if self.main_window.total_exercises == 0:
            self._show_smart_feedback("❌ No hay ejercicios disponibles. Genera algunos primero (F5).")
            return
            
        user_answer = self.main_window.getUserAnswer()
        if not user_answer:
            self._show_smart_feedback("⚠️ Por favor proporciona una respuesta.")
            return
        
        # Call original method
        self.main_window._original_submitAnswer()
        
        # Add smart feedback
        exercise = self.main_window.exercises[self.main_window.current_exercise]
        correct_answer = exercise.get("answer", "").strip().lower()
        is_correct = user_answer.lower() == correct_answer
        
        if is_correct:
            feedback_msgs = ["¡Excelente! 🎉", "¡Perfecto! ✨", "¡Muy bien! 👏", "¡Correcto! 🌟"]
            import random
            self._show_smart_feedback(random.choice(feedback_msgs))
            
            # Auto-advance if enabled
            if self.auto_advance_enabled:
                QTimer.singleShot(1500, self._next_exercise_smart)
        else:
            self._show_smart_feedback(f"❌ Incorrecto. La respuesta es: '{correct_answer}'")

    def _enhanced_next_exercise(self):
        """Enhanced next exercise with smart feedback"""
        if self.main_window.total_exercises == 0:
            self._show_smart_feedback("❌ No hay ejercicios disponibles.")
            return
            
        if self.main_window.current_exercise < self.main_window.total_exercises - 1:
            self.main_window._original_nextExercise()
            self._show_smart_feedback(f"➡️ Ejercicio {self.main_window.current_exercise + 1}/{self.main_window.total_exercises}")
            self._smart_focus()
        else:
            self._show_smart_feedback("ℹ️ Ya estás en el último ejercicio. ¿Generar más? (F5)")

    def _enhanced_prev_exercise(self):
        """Enhanced previous exercise with smart feedback"""
        if self.main_window.total_exercises == 0:
            self._show_smart_feedback("❌ No hay ejercicios disponibles.")
            return
            
        if self.main_window.current_exercise > 0:
            self.main_window._original_prevExercise()
            self._show_smart_feedback(f"⬅️ Ejercicio {self.main_window.current_exercise + 1}/{self.main_window.total_exercises}")
            self._smart_focus()
        else:
            self._show_smart_feedback("ℹ️ Ya estás en el primer ejercicio.")

    def _enhanced_update_exercise(self):
        """Enhanced update exercise with smart focus"""
        self.main_window._original_updateExercise()
        self._smart_focus()

    def _enhanced_update_status(self, message: str):
        """Enhanced status updates with emoji and better formatting"""
        # Add emoji based on message content
        if "correct" in message.lower() or "excelente" in message.lower():
            message = "✅ " + message
        elif "incorrect" in message.lower() or "error" in message.lower():
            message = "❌ " + message
        elif "hint" in message.lower() or "pista" in message.lower():
            message = "💡 " + message
        elif "generated" in message.lower() or "generado" in message.lower():
            message = "🎯 " + message
        elif "welcome" in message.lower() or "bienvenido" in message.lower():
            message = "👋 " + message
        
        self.main_window._original_updateStatus(message)

    # Shortcut handlers
    def _next_exercise_smart(self):
        """Smart next exercise"""
        self._enhanced_next_exercise()

    def _prev_exercise_smart(self):
        """Smart previous exercise"""  
        self._enhanced_prev_exercise()

    def _first_exercise(self):
        """Jump to first exercise"""
        if self.main_window.total_exercises > 0:
            self.main_window.current_exercise = 0
            self._enhanced_update_exercise()
            self._show_smart_feedback("⏮️ Primer ejercicio")

    def _last_exercise(self):
        """Jump to last exercise"""
        if self.main_window.total_exercises > 0:
            self.main_window.current_exercise = self.main_window.total_exercises - 1
            self._enhanced_update_exercise()
            self._show_smart_feedback("⏭️ Último ejercicio")

    def _jump_to_exercise(self):
        """Jump to specific exercise"""
        if self.main_window.total_exercises == 0:
            self._show_smart_feedback("❌ No hay ejercicios disponibles.")
            return
            
        exercise_num, ok = QInputDialog.getInt(
            self.main_window,
            "Saltar a ejercicio",
            f"Número de ejercicio (1-{self.main_window.total_exercises}):",
            self.main_window.current_exercise + 1,
            1, self.main_window.total_exercises
        )
        
        if ok:
            self.main_window.current_exercise = exercise_num - 1
            self._enhanced_update_exercise()
            self._show_smart_feedback(f"📍 Ejercicio {exercise_num}")

    def _toggle_mode_smart(self):
        """Smart mode toggle with feedback"""
        if hasattr(self.main_window, 'mode_combo'):
            combo = self.main_window.mode_combo
            current_index = combo.currentIndex()
            next_index = (current_index + 1) % combo.count()
            combo.setCurrentIndex(next_index)
            mode_name = combo.currentText()
            self._show_smart_feedback(f"🔄 Modo: {mode_name}")
            self._smart_focus()

    def _toggle_review_mode(self):
        """Toggle review mode"""
        if hasattr(self.main_window, 'startReviewMode'):
            self.main_window.startReviewMode()
            self._show_smart_feedback("📚 Modo revisión activado")

    def _generate_exercises_smart(self):
        """Smart exercise generation with validation"""
        # Check required selections
        if hasattr(self.main_window, 'getSelectedTriggers'):
            triggers = self.main_window.getSelectedTriggers()
            tenses = self.main_window.getSelectedTenses() if hasattr(self.main_window, 'getSelectedTenses') else []
            persons = self.main_window.getSelectedPersons() if hasattr(self.main_window, 'getSelectedPersons') else []
            
            missing = []
            if not triggers:
                missing.append("triggers")
            if not tenses:
                missing.append("tenses")
            if not persons:
                missing.append("persons")
                
            if missing:
                self._show_smart_feedback(f"⚠️ Selecciona: {', '.join(missing)}")
                return
        
        if hasattr(self.main_window, 'generateNewExercise'):
            self.main_window.generateNewExercise()
            self._show_smart_feedback("🎯 Generando nuevos ejercicios...")

    def _toggle_translation_smart(self):
        """Smart translation toggle"""
        if hasattr(self.main_window, 'toggleTranslation'):
            self.main_window.toggleTranslation()
            status = "activada" if self.main_window.show_translation else "desactivada"
            self._show_smart_feedback(f"🔤 Traducción {status}")

    def _toggle_theme_smart(self):
        """Smart theme toggle"""
        if hasattr(self.main_window, 'toggleTheme'):
            self.main_window.toggleTheme()
            theme = "oscuro" if self.main_window.dark_mode else "claro"
            self._show_smart_feedback(f"🎨 Tema {theme} activado")

    def _show_contextual_help(self):
        """Show contextual help based on current state"""
        help_text = """
<h3>🚀 Atajos de Teclado Mejorados</h3>

<b>⚡ Acciones Principales:</b><br>
• <b>Enter/Espacio</b>: Enviar respuesta<br>
• <b>Ctrl+→/←</b>: Navegar ejercicios<br>
• <b>F5/Ctrl+N</b>: Generar ejercicios<br>

<b>🎯 Navegación Inteligente:</b><br>
• <b>Home/End</b>: Primer/último ejercicio<br>
• <b>Ctrl+G</b>: Saltar a ejercicio específico<br>
• <b>Tab/Ctrl+M</b>: Cambiar modo<br>

<b>⚙️ Configuración Rápida:</b><br>
• <b>Ctrl+T</b>: Mostrar/ocultar traducción<br>
• <b>Ctrl+D</b>: Cambiar tema<br>
• <b>Ctrl+R</b>: Modo revisión<br>

<b>📊 Información:</b><br>
• <b>Ctrl+I</b>: Estadísticas rápidas<br>
• <b>Ctrl+S</b>: Estadísticas detalladas<br>
• <b>F1/Ctrl+H</b>: Esta ayuda<br>

<b>💡 Consejos:</b><br>
• Usa Tab para cambiar entre modos rápidamente<br>
• Home/End para revisar primer/último ejercicio<br>
• Ctrl+G para saltar a cualquier ejercicio<br>
        """
        QMessageBox.information(self.main_window, "Ayuda - Atajos Mejorados", help_text)

    def _show_quick_stats(self):
        """Show quick session statistics"""
        if not hasattr(self.main_window, 'session_stats'):
            self._show_smart_feedback("ℹ️ No hay estadísticas disponibles aún.")
            return
            
        stats = self.main_window.session_stats
        accuracy = 0
        if stats["total_attempts"] > 0:
            accuracy = (stats["correct_attempts"] / stats["total_attempts"]) * 100
        
        # Quick status bar message
        streak_emoji = "🔥" if accuracy >= 80 else "👍" if accuracy >= 60 else "💪"
        self._show_smart_feedback(
            f"{streak_emoji} {stats['correct_attempts']}/{stats['total_attempts']} "
            f"({accuracy:.0f}%) - {stats['hints_used']} pistas usadas"
        )

    def _show_detailed_stats_smart(self):
        """Show detailed statistics if available"""
        if hasattr(self.main_window, 'showDetailedStats'):
            self.main_window.showDetailedStats()
        else:
            self._show_quick_stats()

    # Utility methods
    def _show_smart_feedback(self, message: str, duration: int = 3000):
        """Show smart feedback with appropriate timing"""
        if hasattr(self.main_window, 'updateStatus'):
            self.main_window.updateStatus(message)
        logger.info(f"Smart feedback: {message}")

    def _smart_focus(self):
        """Set focus to appropriate input field based on current mode"""
        if not hasattr(self.main_window, 'mode_combo'):
            return
            
        mode = self.main_window.mode_combo.currentText()
        if mode == "Free Response" and hasattr(self.main_window, 'free_response_input'):
            self.main_window.free_response_input.setFocus()
            self.main_window.free_response_input.selectAll()
        # For multiple choice, focus is handled automatically by radio buttons

    def enable_auto_advance(self, enabled: bool = True, delay_ms: int = 1500):
        """Enable/disable auto-advance after correct answers"""
        self.auto_advance_enabled = enabled
        if enabled:
            self._show_smart_feedback(f"🚀 Auto-avance activado ({delay_ms/1000:.1f}s)")
        else:
            self._show_smart_feedback("⏸️ Auto-avance desactivado")

    def get_enhancement_info(self) -> Dict[str, Any]:
        """Get information about applied enhancements"""
        return {
            'shortcuts_added': len(self.enhanced_shortcuts),
            'auto_advance_enabled': self.auto_advance_enabled,
            'enhancements_applied': True,
            'version': '1.0.0'
        }


def apply_ui_enhancements(main_window) -> UIEnhancementPatch:
    """
    Apply UI enhancements to existing SpanishSubjunctivePracticeGUI.
    
    Usage:
        window = SpanishSubjunctivePracticeGUI()
        ui_patch = apply_ui_enhancements(window)
        window.show()
    
    Args:
        main_window: Instance of SpanishSubjunctivePracticeGUI
    
    Returns:
        UIEnhancementPatch instance for further customization
    """
    patch = UIEnhancementPatch(main_window)
    patch.apply_enhancements()
    
    # Store patch reference on main window for later access
    main_window._ui_enhancement_patch = patch
    
    logger.info("UI enhancements successfully applied")
    return patch


# Convenience function for easy integration
def enhance_spanish_gui(gui_instance):
    """
    One-line function to enhance existing Spanish subjunctive GUI.
    
    Usage in main.py:
        from src.ui_interaction_patch import enhance_spanish_gui
        
        window = SpanishSubjunctivePracticeGUI()
        enhance_spanish_gui(window)  # <- Add this line
        window.show()
    """
    return apply_ui_enhancements(gui_instance)


if __name__ == "__main__":
    print("""
UI Interaction Patch for Spanish Subjunctive Practice

To integrate this patch:

1. Add to main.py imports:
   from src.ui_interaction_patch import enhance_spanish_gui

2. After creating the window, add:
   window = SpanishSubjunctivePracticeGUI()
   enhance_spanish_gui(window)  # <- Add this line
   window.show()

3. Enjoy enhanced interactions:
   - Intuitive keyboard shortcuts (F1 for help)
   - Smart feedback with emojis
   - Improved navigation flow
   - Auto-focus management
   - Contextual help system

Key shortcuts to remember:
- F5: Generate exercises
- Ctrl+→/←: Navigate
- Tab: Switch modes
- F1: Help
- Ctrl+G: Jump to exercise
    """)
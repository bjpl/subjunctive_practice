"""
Enhanced Feedback System for Spanish Subjunctive Practice
========================================================

This module implements an advanced feedback system based on educational psychology principles:
1. Immediate visual response to user actions
2. Progressive hint system (subtle → detailed)
3. Visual feedback with animations and colors
4. Sound feedback (configurable)
5. Better error messaging with specific guidance
6. Celebration animations for achievements
7. Contextual help system
8. Adaptive feedback based on user performance

Educational Psychology Principles Applied:
- Immediate reinforcement for better retention
- Progressive disclosure to avoid cognitive overload
- Multi-sensory feedback (visual + auditory)
- Constructive error correction
- Achievement recognition for motivation
- Spaced repetition through adaptive difficulty
"""

import sys
import os
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from clean_ui_colors import CleanColors, RichStyles, ColorScheme, primary, success, warning, error, gray


class FeedbackType(Enum):
    CORRECT = "correct"
    INCORRECT = "incorrect"
    HINT = "hint"
    ACHIEVEMENT = "achievement"
    WARNING = "warning"
    INFO = "info"


class HintLevel(Enum):
    SUBTLE = 1
    MODERATE = 2
    DETAILED = 3
    EXPLICIT = 4


@dataclass
class FeedbackConfig:
    """Configuration for the feedback system"""
    visual_enabled: bool = True
    sound_enabled: bool = True
    animation_enabled: bool = True
    hint_progression_enabled: bool = True
    celebration_animations: bool = True
    adaptive_difficulty: bool = True
    timing_optimal: bool = True  # Use timing based on educational research
    
    # Timing configurations (in milliseconds)
    immediate_feedback_delay: int = 100  # Near-immediate response
    error_highlight_duration: int = 3000  # 3 seconds for error visibility
    success_highlight_duration: int = 2000  # 2 seconds for success
    hint_display_duration: int = 5000  # 5 seconds for hints
    achievement_duration: int = 4000  # 4 seconds for celebrations


class SoundManager:
    """Handles sound feedback with configurable options"""
    
    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self.sounds = {
            "correct": "sounds/correct.wav",
            "incorrect": "sounds/incorrect.wav",
            "hint": "sounds/hint.wav",
            "achievement": "sounds/achievement.wav",
            "click": "sounds/click.wav"
        }
    
    def play_sound(self, sound_type: str):
        """Play sound if enabled and file exists"""
        if not self.enabled:
            return
            
        try:
            # For this implementation, we'll create system sounds
            # In a full implementation, you'd use QMediaPlayer or similar
            if sound_type == "correct":
                QApplication.beep()  # System success sound
            elif sound_type == "incorrect":
                # Create a brief error tone
                pass  # Would implement with QMediaPlayer
            elif sound_type == "achievement":
                # Create celebration sound sequence
                for _ in range(3):
                    QApplication.beep()
                    QThread.msleep(150)
        except Exception as e:
            print(f"Sound error: {e}")


class AnimationManager:
    """Handles visual animations for feedback"""
    
    def __init__(self, parent_widget: QWidget):
        self.parent = parent_widget
        self.active_animations = []
    
    def shake_widget(self, widget: QWidget, intensity: int = 10, duration: int = 500):
        """Shake animation for incorrect answers"""
        animation = QPropertyAnimation(widget, b"pos")
        animation.setDuration(duration)
        
        start_pos = widget.pos()
        
        # Create shake keyframes
        keyframes = [
            (0.0, start_pos),
            (0.1, start_pos + QPoint(-intensity, 0)),
            (0.2, start_pos + QPoint(intensity, 0)),
            (0.3, start_pos + QPoint(-intensity//2, 0)),
            (0.4, start_pos + QPoint(intensity//2, 0)),
            (0.5, start_pos + QPoint(-intensity//4, 0)),
            (0.6, start_pos + QPoint(intensity//4, 0)),
            (1.0, start_pos)
        ]
        
        for time, pos in keyframes:
            animation.setKeyValueAt(time, pos)
        
        animation.finished.connect(lambda: self.active_animations.remove(animation))
        self.active_animations.append(animation)
        animation.start()
    
    def pulse_widget(self, widget: QWidget, scale_factor: float = 1.1, duration: int = 300):
        """Pulse animation for correct answers"""
        animation = QPropertyAnimation(widget, b"geometry")
        animation.setDuration(duration)
        
        original_geometry = widget.geometry()
        center = original_geometry.center()
        
        # Calculate scaled geometry
        scaled_width = int(original_geometry.width() * scale_factor)
        scaled_height = int(original_geometry.height() * scale_factor)
        scaled_geometry = QRect(0, 0, scaled_width, scaled_height)
        scaled_geometry.moveCenter(center)
        
        # Create pulse keyframes
        animation.setKeyValueAt(0.0, original_geometry)
        animation.setKeyValueAt(0.5, scaled_geometry)
        animation.setKeyValueAt(1.0, original_geometry)
        
        animation.setEasingCurve(QEasingCurve.OutElastic)
        animation.finished.connect(lambda: self.active_animations.remove(animation))
        self.active_animations.append(animation)
        animation.start()
    
    def celebration_burst(self, widget: QWidget):
        """Celebration animation for achievements"""
        # Create multiple floating celebration elements
        for i in range(8):
            label = QLabel("🎉")
            label.setParent(self.parent)
            label.setStyleSheet("font-size: 24px; background: transparent;")
            
            # Random starting position around the widget
            start_x = widget.x() + random.randint(-50, widget.width() + 50)
            start_y = widget.y() + random.randint(-30, widget.height() + 30)
            label.move(start_x, start_y)
            label.show()
            
            # Animate upward and fade
            animation_group = QParallelAnimationGroup()
            
            # Position animation
            pos_anim = QPropertyAnimation(label, b"pos")
            pos_anim.setDuration(2000)
            pos_anim.setStartValue(QPoint(start_x, start_y))
            pos_anim.setEndValue(QPoint(start_x + random.randint(-100, 100), start_y - 200))
            pos_anim.setEasingCurve(QEasingCurve.OutQuad)
            
            # Opacity animation
            opacity_effect = QGraphicsOpacityEffect()
            label.setGraphicsEffect(opacity_effect)
            opacity_anim = QPropertyAnimation(opacity_effect, b"opacity")
            opacity_anim.setDuration(2000)
            opacity_anim.setStartValue(1.0)
            opacity_anim.setEndValue(0.0)
            
            animation_group.addAnimation(pos_anim)
            animation_group.addAnimation(opacity_anim)
            
            # Clean up when finished
            animation_group.finished.connect(lambda l=label: l.deleteLater())
            animation_group.finished.connect(lambda ag=animation_group: self.active_animations.remove(ag))
            
            self.active_animations.append(animation_group)
            animation_group.start()
    
    def typing_indicator(self, widget: QLineEdit):
        """Show typing indicator animation"""
        original_text = widget.text()
        dots = 0
        
        def animate_dots():
            nonlocal dots
            dots = (dots + 1) % 4
            widget.setPlaceholderText("Thinking" + "." * dots)
        
        timer = QTimer()
        timer.timeout.connect(animate_dots)
        timer.start(500)
        
        # Stop after 3 seconds
        QTimer.singleShot(3000, timer.stop)
        return timer


class ProgressiveHintSystem:
    """Implements progressive hint disclosure"""
    
    def __init__(self):
        self.hint_history = {}  # Track hints per exercise
        self.hint_templates = {
            HintLevel.SUBTLE: [
                "Think about the trigger word in this sentence...",
                "Consider what mood this context requires...",
                "Look for expressions of doubt, emotion, or wish...",
                "What kind of clause follows the main verb?"
            ],
            HintLevel.MODERATE: [
                "This sentence expresses {trigger_type}, which requires subjunctive.",
                "The verb '{trigger_verb}' typically triggers the subjunctive mood.",
                "Look for the conjunction 'que' - what follows often needs subjunctive.",
                "This is a case of {grammatical_context} requiring subjunctive."
            ],
            HintLevel.DETAILED: [
                "The correct form is the {tense} subjunctive of '{verb}'.",
                "Start with the yo form: '{yo_form}', then adjust for {person}.",
                "Remember the pattern: {pattern_explanation}.",
                "The stem changes to '{stem}' in subjunctive forms."
            ],
            HintLevel.EXPLICIT: [
                "The answer is '{answer}' because {detailed_explanation}.",
                "Type '{answer}' - this is the {person} form of {tense} subjunctive.",
                "The complete conjugation pattern here is: {full_pattern}."
            ]
        }
    
    def get_hint(self, exercise_id: str, exercise_data: Dict, current_level: Optional[HintLevel] = None) -> Tuple[str, HintLevel]:
        """Get progressive hint based on previous requests"""
        if exercise_id not in self.hint_history:
            self.hint_history[exercise_id] = []
        
        # Determine next hint level
        if current_level:
            next_level = min(HintLevel.EXPLICIT, HintLevel(current_level.value + 1))
        else:
            next_level = HintLevel.SUBTLE
        
        self.hint_history[exercise_id].append(next_level)
        
        # Generate contextual hint
        hint_text = self._generate_contextual_hint(next_level, exercise_data)
        
        return hint_text, next_level
    
    def _generate_contextual_hint(self, level: HintLevel, exercise_data: Dict) -> str:
        """Generate hint based on specific exercise context"""
        templates = self.hint_templates[level]
        
        if level == HintLevel.SUBTLE:
            return random.choice(templates)
        
        elif level == HintLevel.MODERATE:
            template = random.choice(templates)
            return template.format(
                trigger_type=exercise_data.get('trigger_type', 'uncertainty'),
                trigger_verb=exercise_data.get('trigger_verb', 'unknown'),
                grammatical_context=exercise_data.get('context_type', 'complex sentence')
            )
        
        elif level == HintLevel.DETAILED:
            template = random.choice(templates)
            return template.format(
                tense=exercise_data.get('tense', 'present'),
                verb=exercise_data.get('base_verb', 'verb'),
                yo_form=exercise_data.get('yo_form', ''),
                person=exercise_data.get('person', 'third person'),
                pattern_explanation=exercise_data.get('pattern', 'standard conjugation'),
                stem=exercise_data.get('stem', 'root')
            )
        
        else:  # EXPLICIT
            template = random.choice(templates)
            return template.format(
                answer=exercise_data.get('answer', ''),
                detailed_explanation=exercise_data.get('explanation', 'standard rule'),
                person=exercise_data.get('person', 'third person'),
                tense=exercise_data.get('tense', 'present'),
                full_pattern=exercise_data.get('conjugation_pattern', 'see reference')
            )


class EnhancedFeedbackWidget(QFrame):
    """Main feedback display widget with enhanced features"""
    
    feedback_requested = pyqtSignal(str)  # Request more detailed explanation
    
    def __init__(self, config: FeedbackConfig = None):
        super().__init__()
        self.config = config or FeedbackConfig()
        self.sound_manager = SoundManager(self.config.sound_enabled)
        self.animation_manager = AnimationManager(self)
        self.hint_system = ProgressiveHintSystem()
        
        self.current_feedback_type = None
        self.current_exercise_id = None
        
        self.init_ui()
        self.apply_styles()
    
    def init_ui(self):
        """Initialize the feedback widget UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Header with icon and status
        header_layout = QHBoxLayout()
        
        self.status_icon = QLabel()
        self.status_icon.setFixedSize(32, 32)
        self.status_icon.setStyleSheet("font-size: 24px;")
        
        self.status_text = QLabel("Ready for your answer!")
        self.status_text.setStyleSheet("font-weight: bold; font-size: 16px;")
        
        header_layout.addWidget(self.status_icon)
        header_layout.addWidget(self.status_text)
        header_layout.addStretch()
        
        # Action buttons
        self.hint_button = QPushButton("💡 Hint")
        self.explain_button = QPushButton("📚 Explain")
        self.explain_button.hide()  # Show only after submission
        
        header_layout.addWidget(self.hint_button)
        header_layout.addWidget(self.explain_button)
        
        layout.addLayout(header_layout)
        
        # Feedback content area
        self.feedback_content = QTextEdit()
        self.feedback_content.setReadOnly(True)
        self.feedback_content.setMaximumHeight(150)
        layout.addWidget(self.feedback_content)
        
        # Progress indicator for hints
        self.hint_progress = QProgressBar()
        self.hint_progress.setMaximum(4)  # 4 hint levels
        self.hint_progress.setValue(0)
        self.hint_progress.setFormat("Hint Level: %v/4")
        self.hint_progress.hide()
        layout.addWidget(self.hint_progress)
        
        # Connect signals
        self.hint_button.clicked.connect(self.request_hint)
        self.explain_button.clicked.connect(lambda: self.feedback_requested.emit("detailed"))
    
    def apply_styles(self):
        """Apply visual styling to the widget"""
        self.setFrameStyle(QFrame.Box)
        self.setStyleSheet(f"""
            QFrame {{
                background: {CleanColors.BACKGROUND_CARD};
                border: 2px solid {CleanColors.BORDER};
                border-radius: 12px;
                padding: 8px;
            }}
            QPushButton {{
                background: {CleanColors.PRIMARY};
                color: {CleanColors.TEXT_WHITE};
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: {CleanColors.PRIMARY_HOVER};
            }}
            QPushButton:pressed {{
                background: {CleanColors.PRIMARY_HOVER};
            }}
            QPushButton:focus {{
                outline: 2px solid {CleanColors.FOCUS};
                outline-offset: 2px;
            }}
            QTextEdit {{
                border: 1px solid {CleanColors.BORDER_LIGHT};
                border-radius: 6px;
                background-color: {CleanColors.BACKGROUND};
                padding: 8px;
                color: {CleanColors.TEXT_PRIMARY};
            }}
        """)
    
    def show_immediate_response(self, is_correct: bool, user_answer: str = "", correct_answer: str = ""):
        """Show immediate visual response to user input"""
        if is_correct:
            self.show_correct_feedback()
        else:
            self.show_incorrect_feedback(user_answer, correct_answer)
    
    def show_correct_feedback(self):
        """Display positive feedback for correct answers"""
        self.current_feedback_type = FeedbackType.CORRECT
        
        # Visual feedback
        self.status_icon.setText("✅")
        self.status_text.setText("Excellent! Correct answer!")
        
        # Apply success styling
        self.setStyleSheet(self.styleSheet().replace(
            f"border: 2px solid {CleanColors.BORDER};",
            f"border: 2px solid {CleanColors.SUCCESS};"
        ))
        
        # Sound feedback
        self.sound_manager.play_sound("correct")
        
        # Animation
        if self.config.animation_enabled:
            self.animation_manager.pulse_widget(self)
        
        # Show explain button
        self.explain_button.show()
        
        # Auto-hide success styling after duration
        QTimer.singleShot(self.config.success_highlight_duration, self._reset_styling)
        
        # Positive reinforcement messages
        positive_messages = [
            "¡Excelente! Your subjunctive skills are improving!",
            "Perfect! You've mastered this construction!",
            "¡Muy bien! You understand the subjunctive trigger!",
            "Outstanding! Your Spanish is getting stronger!",
            "Brilliant! You've got the mood distinction!"
        ]
        
        self.feedback_content.setHtml(f"""
            <div style="color: {CleanColors.SUCCESS_HOVER}; background-color: {CleanColors.SUCCESS_LIGHT}; padding: 10px; border-radius: 6px; border-left: 4px solid {CleanColors.SUCCESS};">
                <strong>✅ Correcto!</strong><br>
                {random.choice(positive_messages)}
            </div>
        """)
    
    def show_incorrect_feedback(self, user_answer: str, correct_answer: str):
        """Display constructive feedback for incorrect answers"""
        self.current_feedback_type = FeedbackType.INCORRECT
        
        # Visual feedback
        self.status_icon.setText("❌")
        self.status_text.setText("Not quite right - let's learn!")
        
        # Apply error styling
        self.setStyleSheet(self.styleSheet().replace(
            f"border: 2px solid {CleanColors.BORDER};",
            f"border: 2px solid {CleanColors.ERROR};"
        ))
        
        # Sound feedback
        self.sound_manager.play_sound("incorrect")
        
        # Animation
        if self.config.animation_enabled:
            self.animation_manager.shake_widget(self)
        
        # Show explain button
        self.explain_button.show()
        
        # Auto-hide error styling after duration
        QTimer.singleShot(self.config.error_highlight_duration, self._reset_styling)
        
        # Constructive error messages
        self.feedback_content.setHtml(f"""
            <div style="color: {CleanColors.ERROR_HOVER}; background-color: {CleanColors.ERROR_LIGHT}; padding: 10px; border-radius: 6px; border-left: 4px solid {CleanColors.ERROR};">
                <strong>❌ Incorrecto</strong><br>
                You answered: <em>{user_answer}</em><br>
                Correct answer: <strong>{correct_answer}</strong><br>
                <br>
                💡 <em>Don't worry! Mistakes help us learn. Let's understand why...</em>
            </div>
        """)
    
    def request_hint(self):
        """Request and display progressive hint"""
        if not self.current_exercise_id:
            return
        
        # Get exercise data (this would come from the main application)
        exercise_data = self._get_current_exercise_data()
        
        hint_text, hint_level = self.hint_system.get_hint(
            self.current_exercise_id, 
            exercise_data
        )
        
        self.show_hint(hint_text, hint_level)
    
    def show_hint(self, hint_text: str, hint_level: HintLevel):
        """Display hint with appropriate styling"""
        self.current_feedback_type = FeedbackType.HINT
        
        # Visual feedback
        self.status_icon.setText("💡")
        self.status_text.setText(f"Hint Level {hint_level.value}")
        
        # Update hint progress
        self.hint_progress.show()
        self.hint_progress.setValue(hint_level.value)
        
        # Apply hint styling
        self.setStyleSheet(self.styleSheet().replace(
            f"border: 2px solid {CleanColors.BORDER};",
            f"border: 2px solid {CleanColors.WARNING};"
        ))
        
        # Sound feedback
        self.sound_manager.play_sound("hint")
        
        # Show hint content
        hint_icons = ["💭", "🤔", "📝", "🎯"]
        icon = hint_icons[min(hint_level.value - 1, len(hint_icons) - 1)]
        
        self.feedback_content.setHtml(f"""
            <div style="color: {CleanColors.WARNING_HOVER}; background-color: {CleanColors.WARNING_LIGHT}; padding: 10px; border-radius: 6px; border-left: 4px solid {CleanColors.WARNING};">
                <strong>{icon} Hint (Level {hint_level.value})</strong><br>
                {hint_text}
            </div>
        """)
        
        # Auto-hide hint styling after duration
        QTimer.singleShot(self.config.hint_display_duration, self._reset_styling)
    
    def show_achievement(self, achievement_text: str, achievement_type: str = "general"):
        """Display achievement celebration"""
        self.current_feedback_type = FeedbackType.ACHIEVEMENT
        
        # Visual feedback
        self.status_icon.setText("🏆")
        self.status_text.setText("Achievement Unlocked!")
        
        # Apply achievement styling
        self.setStyleSheet(self.styleSheet().replace(
            f"border: 2px solid {CleanColors.BORDER};",
            f"border: 2px solid {CleanColors.WARNING}; background: {CleanColors.WARNING_LIGHT};"
        ))
        
        # Sound feedback
        self.sound_manager.play_sound("achievement")
        
        # Celebration animation
        if self.config.celebration_animations:
            self.animation_manager.celebration_burst(self)
        
        # Achievement content
        achievement_icons = {
            "streak": "🔥",
            "accuracy": "🎯",
            "speed": "⚡",
            "mastery": "👑",
            "general": "🏆"
        }
        
        icon = achievement_icons.get(achievement_type, "🏆")
        
        self.feedback_content.setHtml(f"""
            <div style="color: {CleanColors.WARNING_HOVER}; background: {CleanColors.WARNING_LIGHT}; 
                        padding: 12px; border-radius: 8px; border: 2px solid {CleanColors.WARNING}; text-align: center;">
                <h3 style="margin: 0; color: {CleanColors.WARNING_HOVER};">{icon} ¡Felicidades!</h3>
                <p style="margin: 8px 0; font-weight: bold; color: {CleanColors.TEXT_PRIMARY};">{achievement_text}</p>
                <p style="margin: 0; font-style: italic; color: {CleanColors.TEXT_SECONDARY};">Keep up the excellent work!</p>
            </div>
        """)
        
        # Auto-hide achievement styling after duration
        QTimer.singleShot(self.config.achievement_duration, self._reset_styling)
    
    def set_exercise_context(self, exercise_id: str, exercise_data: Dict):
        """Set current exercise context for hint system"""
        self.current_exercise_id = exercise_id
        self._current_exercise_data = exercise_data
        
        # Reset hint progress
        self.hint_progress.setValue(0)
        self.hint_progress.hide()
        self.explain_button.hide()
    
    def _get_current_exercise_data(self) -> Dict:
        """Get current exercise data for hint generation"""
        return getattr(self, '_current_exercise_data', {})
    
    def _reset_styling(self):
        """Reset widget styling to default"""
        self.apply_styles()
        self.status_icon.setText("📝")
        self.status_text.setText("Ready for your next answer!")
        self.status_text.setStyleSheet(f"font-weight: bold; font-size: 16px; color: {CleanColors.TEXT_PRIMARY};")


class AdaptiveFeedbackManager:
    """Manages adaptive feedback based on user performance patterns"""
    
    def __init__(self):
        self.user_performance = {
            "accuracy_history": [],
            "response_times": [],
            "error_patterns": {},
            "learning_velocity": 0,
            "difficulty_progression": []
        }
        
        self.feedback_strategies = {
            "struggling": {
                "hint_frequency": "high",
                "explanation_detail": "detailed",
                "encouragement": "frequent",
                "difficulty_adjustment": "decrease"
            },
            "progressing": {
                "hint_frequency": "moderate",
                "explanation_detail": "moderate",
                "encouragement": "balanced",
                "difficulty_adjustment": "maintain"
            },
            "mastering": {
                "hint_frequency": "minimal",
                "explanation_detail": "concise",
                "encouragement": "achievement_focused",
                "difficulty_adjustment": "increase"
            }
        }
    
    def update_performance(self, is_correct: bool, response_time: float, exercise_data: Dict):
        """Update user performance metrics"""
        self.user_performance["accuracy_history"].append(is_correct)
        self.user_performance["response_times"].append(response_time)
        
        # Track error patterns
        if not is_correct:
            error_type = self._classify_error(exercise_data)
            self.user_performance["error_patterns"][error_type] = \
                self.user_performance["error_patterns"].get(error_type, 0) + 1
        
        # Calculate learning velocity
        self._update_learning_velocity()
    
    def get_adaptive_feedback_strategy(self) -> str:
        """Determine appropriate feedback strategy based on performance"""
        recent_accuracy = self._get_recent_accuracy()
        learning_trend = self._get_learning_trend()
        
        if recent_accuracy < 0.4 or learning_trend < -0.1:
            return "struggling"
        elif recent_accuracy > 0.8 and learning_trend > 0.1:
            return "mastering"
        else:
            return "progressing"
    
    def _get_recent_accuracy(self, window_size: int = 10) -> float:
        """Calculate accuracy over recent exercises"""
        recent_results = self.user_performance["accuracy_history"][-window_size:]
        if not recent_results:
            return 0.0
        return sum(recent_results) / len(recent_results)
    
    def _get_learning_trend(self) -> float:
        """Calculate learning trend (improvement over time)"""
        history = self.user_performance["accuracy_history"]
        if len(history) < 6:
            return 0.0
        
        # Compare recent half vs earlier half
        mid = len(history) // 2
        earlier = sum(history[:mid]) / mid if mid > 0 else 0
        recent = sum(history[mid:]) / (len(history) - mid)
        
        return recent - earlier
    
    def _classify_error(self, exercise_data: Dict) -> str:
        """Classify error type for pattern tracking"""
        # This would analyze the specific type of error
        # For now, return a simple classification
        return exercise_data.get("error_category", "general")
    
    def _update_learning_velocity(self):
        """Update learning velocity metric"""
        if len(self.user_performance["accuracy_history"]) >= 5:
            recent_trend = self._get_learning_trend()
            self.user_performance["learning_velocity"] = recent_trend


class ContextualHelpSystem:
    """Provides contextual help based on current exercise and user needs"""
    
    def __init__(self):
        self.help_topics = {
            "subjunctive_triggers": {
                "title": "Subjunctive Triggers",
                "content": """
                <h3>When to use the Subjunctive:</h3>
                <ul>
                    <li><strong>Wish/Desire:</strong> querer que, esperar que, ojalá</li>
                    <li><strong>Emotion:</strong> alegrarse que, temer que, sentir que</li>
                    <li><strong>Doubt/Denial:</strong> dudar que, negar que, no creer que</li>
                    <li><strong>Impersonal expressions:</strong> es necesario que, es posible que</li>
                </ul>
                """,
                "examples": [
                    "Espero que <strong>tengas</strong> un buen día.",
                    "No creo que <strong>venga</strong> mañana.",
                    "Es importante que <strong>estudies</strong> español."
                ]
            },
            "conjugation_patterns": {
                "title": "Conjugation Patterns",
                "content": """
                <h3>Present Subjunctive Formation:</h3>
                <ol>
                    <li>Start with yo form of present indicative</li>
                    <li>Remove the -o ending</li>
                    <li>Add opposite vowel endings</li>
                </ol>
                """,
                "examples": [
                    "hablar → hablo → habl → <strong>hable</strong>",
                    "comer → como → com → <strong>coma</strong>",
                    "vivir → vivo → viv → <strong>viva</strong>"
                ]
            }
        }
    
    def get_contextual_help(self, exercise_context: Dict) -> str:
        """Get help content based on exercise context"""
        # Determine what type of help is most relevant
        context_type = exercise_context.get("context_type", "general")
        
        if "trigger" in context_type.lower():
            return self._format_help_content("subjunctive_triggers")
        elif "conjugation" in context_type.lower():
            return self._format_help_content("conjugation_patterns")
        else:
            return self._get_general_help()
    
    def _format_help_content(self, topic_key: str) -> str:
        """Format help content for display"""
        topic = self.help_topics[topic_key]
        
        content = f"<h2>{topic['title']}</h2>"
        content += topic['content']
        
        if topic.get('examples'):
            content += "<h4>Examples:</h4><ul>"
            for example in topic['examples']:
                content += f"<li>{example}</li>"
            content += "</ul>"
        
        return content
    
    def _get_general_help(self) -> str:
        """Provide general subjunctive help"""
        return """
        <h2>Spanish Subjunctive Quick Guide</h2>
        <p>The subjunctive mood expresses:</p>
        <ul>
            <li>🎯 <strong>Subjectivity</strong> - opinions, emotions, desires</li>
            <li>❓ <strong>Uncertainty</strong> - doubt, possibility, hypothetical situations</li>
            <li>🎭 <strong>Non-reality</strong> - wishes, commands, unreal conditions</li>
        </ul>
        <p><em>Remember: If it's objective and certain, use indicative. If it's subjective or uncertain, consider subjunctive!</em></p>
        """


# Integration helper for the main application
class FeedbackSystemIntegration:
    """Helper class to integrate the enhanced feedback system with the main application"""
    
    @staticmethod
    def enhance_main_application(main_window):
        """Add enhanced feedback system to existing main window"""
        # This would be called from the main application to add the enhanced feedback
        config = FeedbackConfig()
        
        # Replace existing feedback widget
        enhanced_feedback = EnhancedFeedbackWidget(config)
        
        # Set up adaptive feedback manager
        adaptive_manager = AdaptiveFeedbackManager()
        
        # Add contextual help system
        help_system = ContextualHelpSystem()
        
        return {
            'feedback_widget': enhanced_feedback,
            'adaptive_manager': adaptive_manager,
            'help_system': help_system,
            'config': config
        }


if __name__ == "__main__":
    # Demo application
    app = QApplication(sys.argv)
    
    # Create demo window
    window = QMainWindow()
    window.setWindowTitle("Enhanced Feedback System Demo")
    window.setGeometry(100, 100, 800, 600)
    
    # Add feedback widget
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    layout = QVBoxLayout(central_widget)
    
    feedback_widget = EnhancedFeedbackWidget()
    layout.addWidget(feedback_widget)
    
    # Demo buttons
    button_layout = QHBoxLayout()
    
    correct_btn = QPushButton("Demo Correct")
    incorrect_btn = QPushButton("Demo Incorrect")
    achievement_btn = QPushButton("Demo Achievement")
    hint_btn = QPushButton("Demo Hint")
    
    correct_btn.clicked.connect(lambda: feedback_widget.show_correct_feedback())
    incorrect_btn.clicked.connect(lambda: feedback_widget.show_incorrect_feedback("hablo", "hable"))
    achievement_btn.clicked.connect(lambda: feedback_widget.show_achievement("5-day practice streak!", "streak"))
    hint_btn.clicked.connect(lambda: feedback_widget.show_hint("Look for emotion words that trigger subjunctive...", HintLevel.SUBTLE))
    
    button_layout.addWidget(correct_btn)
    button_layout.addWidget(incorrect_btn)
    button_layout.addWidget(achievement_btn)
    button_layout.addWidget(hint_btn)
    
    layout.addLayout(button_layout)
    
    window.show()
    sys.exit(app.exec_())
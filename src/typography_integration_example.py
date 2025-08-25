"""
Typography Integration Example for Spanish Subjunctive Practice App

This module demonstrates how to integrate the Spanish Typography System
into the existing main.py application. It shows practical examples of
applying Spanish-optimized typography to various UI elements.

Usage:
    Run this file directly to see a demo of typography integration,
    or import the functions to apply to your existing application.
"""

import sys
import os
from typing import List, Optional
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QGroupBox, QTextEdit, QCheckBox
)
from PyQt5.QtCore import Qt

# Import the typography system
try:
    from typography_system import (
        create_spanish_typography, 
        apply_spanish_typography_to_app,
        TypographyPresets,
        get_typography_info
    )
except ImportError:
    # Handle case where we're running from different directory
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from typography_system import (
        create_spanish_typography, 
        apply_spanish_typography_to_app,
        TypographyPresets,
        get_typography_info
    )


class TypographyIntegrationMixin:
    """
    Mixin class that can be added to existing GUI classes to provide
    Spanish typography integration functionality.
    """
    
    def initialize_spanish_typography(self):
        """
        Initialize the Spanish typography system for this widget.
        Call this method after UI initialization but before showing the widget.
        """
        self.typography = create_spanish_typography()
        self.typography_presets = TypographyPresets(self.typography)
        
        # Store original fonts for potential restoration
        self._original_fonts = {}
        
        # Apply typography to the widget
        self._apply_spanish_typography()
    
    def _apply_spanish_typography(self):
        """
        Apply Spanish-optimized typography to UI elements.
        Override this method in subclasses to customize typography application.
        """
        # Apply to main sentence/exercise labels
        exercise_labels = self._find_widgets_by_property('role', 'exercise')
        exercise_labels.extend(self._find_widgets_by_class(QLabel, lambda w: 'sentence' in w.objectName().lower()))
        
        for label in exercise_labels:
            self._apply_preset_to_widget(label, 'exercise_text')
            label.setProperty('typography_role', 'exercise')
        
        # Apply to translation labels
        translation_labels = self._find_widgets_by_property('role', 'translation')
        translation_labels.extend(self._find_widgets_by_class(QLabel, lambda w: 'translation' in w.objectName().lower()))
        
        for label in translation_labels:
            self._apply_preset_to_widget(label, 'translation_text')
            label.setProperty('typography_role', 'translation')
        
        # Apply to headings and group boxes
        for groupbox in self.findChildren(QGroupBox):
            self._apply_preset_to_widget(groupbox, 'heading_medium')
        
        # Apply to buttons
        for button in self.findChildren(QPushButton):
            self._apply_preset_to_widget(button, 'button_text')
        
        # Apply to input fields
        for input_widget in self.findChildren(QLineEdit):
            self._apply_preset_to_widget(input_widget, 'body_text')
        
        # Apply to text areas
        for text_area in self.findChildren(QTextEdit):
            if 'feedback' in text_area.objectName().lower():
                self._apply_preset_to_widget(text_area, 'feedback_text')
                text_area.setProperty('typography_role', 'feedback')
            else:
                self._apply_preset_to_widget(text_area, 'body_text')
        
        # Apply to checkboxes and other controls
        for checkbox in self.findChildren(QCheckBox):
            self._apply_preset_to_widget(checkbox, 'label_text')
        
        # Apply to statistics and status labels
        stats_labels = self._find_widgets_by_class(QLabel, lambda w: 'stat' in w.objectName().lower())
        for label in stats_labels:
            self._apply_preset_to_widget(label, 'stats_text')
    
    def _apply_preset_to_widget(self, widget: QWidget, preset_name: str):
        """
        Apply a typography preset to a specific widget.
        
        Args:
            widget: Widget to apply typography to
            preset_name: Name of the typography preset
        """
        try:
            # Store original font if not already stored
            widget_key = f"{widget.__class__.__name__}_{id(widget)}"
            if widget_key not in self._original_fonts:
                self._original_fonts[widget_key] = widget.font()
            
            # Create and apply new font
            font = self.typography_presets.create_preset_font(preset_name)
            widget.setFont(font)
            
            # Set property for potential stylesheet targeting
            widget.setProperty('typography_preset', preset_name)
            
        except Exception as e:
            print(f"Warning: Could not apply typography preset '{preset_name}' to {widget.__class__.__name__}: {e}")
    
    def _find_widgets_by_property(self, property_name: str, property_value: str) -> List[QWidget]:
        """Find widgets with a specific property value."""
        widgets = []
        for widget in self.findChildren(QWidget):
            if widget.property(property_name) == property_value:
                widgets.append(widget)
        return widgets
    
    def _find_widgets_by_class(self, widget_class, filter_func=None) -> List[QWidget]:
        """Find widgets by class, optionally with a filter function."""
        widgets = []
        for widget in self.findChildren(widget_class):
            if filter_func is None or filter_func(widget):
                widgets.append(widget)
        return widgets
    
    def restore_original_typography(self):
        """
        Restore original fonts for all widgets.
        Useful for testing or user preferences.
        """
        for widget_key, original_font in self._original_fonts.items():
            try:
                # This is a simplified approach - in practice you'd need
                # to track widgets more carefully
                pass  # Implementation would depend on widget tracking
            except Exception:
                pass  # Widget might have been deleted
    
    def get_typography_info(self) -> dict:
        """Get information about the current typography configuration."""
        if hasattr(self, 'typography'):
            return get_typography_info()
        else:
            return {"error": "Typography system not initialized"}


class SpanishSubjunctiveGUIWithTypography(QMainWindow, TypographyIntegrationMixin):
    """
    Example integration of Spanish typography into a simplified version
    of the Spanish Subjunctive Practice GUI.
    
    This demonstrates how to modify the existing main.py to use
    the typography system.
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spanish Subjunctive Practice - Typography Demo")
        self.setGeometry(100, 100, 1000, 700)
        
        # Initialize UI first
        self.initUI()
        
        # Then apply Spanish typography
        self.initialize_spanish_typography()
    
    def initUI(self):
        """Initialize the user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Title
        title_label = QLabel("Spanish Subjunctive Practice")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setProperty('role', 'heading')
        layout.addWidget(title_label)
        
        # Main exercise area
        exercise_group = QGroupBox("Exercise")
        exercise_layout = QVBoxLayout(exercise_group)
        
        # Spanish sentence (main content)
        self.sentence_label = QLabel("Espero que tengas éxito en el aprendizaje del subjuntivo español.")
        self.sentence_label.setObjectName("sentence_label")
        self.sentence_label.setWordWrap(True)
        self.sentence_label.setProperty('role', 'exercise')
        exercise_layout.addWidget(self.sentence_label)
        
        # English translation
        self.translation_label = QLabel("I hope you succeed in learning the Spanish subjunctive.")
        self.translation_label.setObjectName("translation_label")
        self.translation_label.setWordWrap(True)
        self.translation_label.setProperty('role', 'translation')
        self.translation_label.setStyleSheet("color: #666; font-style: italic;")
        exercise_layout.addWidget(self.translation_label)
        
        layout.addWidget(exercise_group)
        
        # Input area
        input_group = QGroupBox("Your Answer")
        input_layout = QVBoxLayout(input_group)
        
        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText("Escribe tu respuesta aquí...")
        input_layout.addWidget(self.answer_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.hint_button = QPushButton("Pista")
        self.submit_button = QPushButton("Enviar")
        self.next_button = QPushButton("Siguiente")
        
        button_layout.addWidget(self.hint_button)
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.next_button)
        
        input_layout.addLayout(button_layout)
        layout.addWidget(input_group)
        
        # Feedback area
        feedback_group = QGroupBox("Feedback")
        feedback_layout = QVBoxLayout(feedback_group)
        
        self.feedback_text = QTextEdit()
        self.feedback_text.setObjectName("feedback_text")
        self.feedback_text.setPlainText(
            "¡Excelente! Has usado correctamente el subjuntivo. El verbo 'tengas' es la forma "
            "correcta del presente de subjuntivo para 'tú' del verbo 'tener'. Se usa aquí "
            "porque expresa un deseo o esperanza introducido por 'espero que'."
        )
        self.feedback_text.setMaximumHeight(120)
        feedback_layout.addWidget(self.feedback_text)
        
        layout.addWidget(feedback_group)
        
        # Statistics area
        stats_group = QGroupBox("Statistics")
        stats_layout = QVBoxLayout(stats_group)
        
        self.stats_label = QLabel("Ejercicios: 15/20 | Correctos: 12 | Precisión: 80%")
        self.stats_label.setObjectName("stats_label")
        stats_layout.addWidget(self.stats_label)
        
        layout.addWidget(stats_group)
        
        # Typography controls
        controls_group = QGroupBox("Typography Controls")
        controls_layout = QHBoxLayout(controls_group)
        
        info_button = QPushButton("Typography Info")
        info_button.clicked.connect(self.show_typography_info)
        controls_layout.addWidget(info_button)
        
        demo_button = QPushButton("Toggle Demo Text")
        demo_button.clicked.connect(self.toggle_demo_text)
        controls_layout.addWidget(demo_button)
        
        layout.addWidget(controls_group)
        
        # Add some checkboxes for demo
        options_group = QGroupBox("Practice Options")
        options_layout = QVBoxLayout(options_group)
        
        self.show_translation_cb = QCheckBox("Mostrar traducción")
        self.show_translation_cb.setChecked(True)
        options_layout.addWidget(self.show_translation_cb)
        
        self.audio_feedback_cb = QCheckBox("Retroalimentación de audio")
        options_layout.addWidget(self.audio_feedback_cb)
        
        layout.addWidget(options_group)
    
    def show_typography_info(self):
        """Display typography system information."""
        info = self.get_typography_info()
        
        info_text = f"""
Typography System Information:

Version: {info.get('version', 'Unknown')}
Optimized for: {info.get('optimized_for', 'Spanish text')}
Current scale factor: {info.get('current_scale_factor', 1.0):.2f}
Screen DPI: {info.get('screen_info', {}).get('dpi', 'Unknown')}
Screen size: {info.get('screen_info', {}).get('width', 'Unknown')}x{info.get('screen_info', {}).get('height', 'Unknown')}

Primary fonts: {', '.join(info.get('primary_fonts', [])[:3])}

Available presets:
• exercise_text - Spanish sentence display
• translation_text - English translations  
• heading_large - Main section titles
• button_text - Button labels
• feedback_text - Explanation text
• stats_text - Statistics display
        """.strip()
        
        # Create info dialog
        from PyQt5.QtWidgets import QMessageBox
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Typography System Information")
        msg_box.setText(info_text)
        msg_box.exec_()
    
    def toggle_demo_text(self):
        """Toggle between different demo text samples."""
        demo_sentences = [
            "Espero que tengas éxito en el aprendizaje del subjuntivo español.",
            "Es importante que practiques todos los días para mejorar tu español.",
            "No creo que sea difícil aprender con esta tipografía optimizada.",
            "Ojalá que encuentres útil este sistema de tipografía para el español.",
            "Dudo que haya una mejor fuente para estudiar acentos y tildes."
        ]
        
        demo_translations = [
            "I hope you succeed in learning the Spanish subjunctive.",
            "It's important that you practice every day to improve your Spanish.",
            "I don't think it's difficult to learn with this optimized typography.",
            "I hope you find this typography system useful for Spanish.",
            "I doubt there's a better font for studying accents and tildes."
        ]
        
        # Get current text and find next one
        current_text = self.sentence_label.text()
        try:
            current_index = demo_sentences.index(current_text)
            next_index = (current_index + 1) % len(demo_sentences)
        except ValueError:
            next_index = 0
        
        # Update text
        self.sentence_label.setText(demo_sentences[next_index])
        self.translation_label.setText(demo_translations[next_index])


def create_typography_demo_app():
    """
    Create a complete demo application showing Spanish typography integration.
    
    Returns:
        Tuple of (app, main_window)
    """
    app = QApplication(sys.argv)
    
    # Apply Spanish typography system to entire app
    typography_system = apply_spanish_typography_to_app(app)
    
    # Create main window with typography integration
    main_window = SpanishSubjunctiveGUIWithTypography()
    
    return app, main_window


def demonstrate_typography_integration():
    """
    Demonstrate how to integrate typography into existing code.
    Shows before/after comparison and integration steps.
    """
    print("=== Spanish Typography System Integration Demo ===\n")
    
    # Show system information
    info = get_typography_info()
    print(f"Typography System Version: {info['version']}")
    print(f"Optimized for: {info['optimized_for']}")
    print(f"Current scale factor: {info['current_scale_factor']:.2f}")
    print(f"Screen DPI: {info['screen_info']['dpi']}")
    print(f"Primary fonts: {', '.join(info['primary_fonts'][:3])}")
    print()
    
    # Integration steps
    print("Integration Steps:")
    print("1. Import typography system:")
    print("   from src.typography_system import create_spanish_typography, TypographyPresets")
    print()
    print("2. Initialize in your GUI class __init__:")
    print("   self.typography = create_spanish_typography()")
    print("   self.typography_presets = TypographyPresets(self.typography)")
    print()
    print("3. Apply to specific elements:")
    print("   # Spanish exercise text")
    print("   exercise_font = self.typography_presets.create_preset_font('exercise_text')")
    print("   self.sentence_label.setFont(exercise_font)")
    print()
    print("   # English translation")
    print("   translation_font = self.typography_presets.create_preset_font('translation_text')")
    print("   self.translation_label.setFont(translation_font)")
    print()
    print("4. Or use the mixin class for automatic application:")
    print("   class YourGUI(QMainWindow, TypographyIntegrationMixin):")
    print("       def __init__(self):")
    print("           super().__init__()")
    print("           self.initUI()")
    print("           self.initialize_spanish_typography()  # Auto-applies to common elements")
    print()
    
    print("Demo application will show typography in action...")
    print("Look for improved readability of Spanish text with accents!")


# Functions for easy integration into existing code
def apply_typography_to_existing_gui(gui_instance):
    """
    Apply Spanish typography to an existing GUI instance.
    
    Args:
        gui_instance: Existing QMainWindow or QWidget instance
        
    Example:
        window = SpanishSubjunctivePracticeGUI()
        apply_typography_to_existing_gui(window)
    """
    # Add the mixin functionality dynamically
    if not hasattr(gui_instance, 'initialize_spanish_typography'):
        # Add mixin methods to existing instance
        for method_name in dir(TypographyIntegrationMixin):
            if not method_name.startswith('_') or method_name in ['_apply_spanish_typography', '_apply_preset_to_widget']:
                method = getattr(TypographyIntegrationMixin, method_name)
                setattr(gui_instance, method_name, method.__get__(gui_instance))
    
    # Initialize typography
    gui_instance.initialize_spanish_typography()


def get_integration_stylesheet():
    """
    Get a complete stylesheet with Spanish typography integration.
    Can be applied to existing applications.
    
    Returns:
        CSS stylesheet string for Qt applications
    """
    typography = create_spanish_typography()
    presets = TypographyPresets(typography)
    
    styles = []
    
    # Generate styles for each preset
    preset_mappings = {
        'QLabel[role="exercise"]': 'exercise_text',
        'QLabel[role="translation"]': 'translation_text',
        'QLabel[role="heading"]': 'heading_large',
        'QPushButton': 'button_text',
        'QLineEdit': 'body_text',
        'QTextEdit[role="feedback"]': 'feedback_text',
        'QGroupBox': 'heading_medium',
        'QCheckBox': 'label_text',
        'QLabel[role="stats"]': 'stats_text'
    }
    
    for selector, preset in preset_mappings.items():
        style = presets.get_preset_stylesheet(selector, preset)
        styles.append(style)
    
    return '\n\n'.join(styles)


if __name__ == "__main__":
    """
    Run the typography integration demo.
    """
    print("Starting Spanish Typography Integration Demo...")
    
    # Show integration information
    demonstrate_typography_integration()
    
    # Create and run demo app
    app, main_window = create_typography_demo_app()
    
    print("\nDemo app created. Notice the improved typography for Spanish text!")
    print("Features to observe:")
    print("• Larger, more readable Spanish sentences")
    print("• Proper line height for accented characters")
    print("• Optimized letter spacing")
    print("• Clear font hierarchy")
    print("• Responsive scaling based on your screen")
    
    main_window.show()
    sys.exit(app.exec_())
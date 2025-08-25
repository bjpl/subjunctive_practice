"""
Test script for the visual design improvements.
This script verifies that the new UI visual module works correctly.
"""

import sys
import os

# Add the parent directory to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QGroupBox, QTextEdit, QProgressBar, QComboBox, QCheckBox
from PyQt5.QtCore import Qt

def test_visual_module():
    """Test that the visual module can be imported and used."""
    try:
        from src.ui_visual import initialize_modern_ui, apply_widget_specific_styles, VisualTheme
        print("✓ Visual module imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import visual module: {e}")
        return False

def create_test_ui(app):
    """Create a test UI to preview the visual improvements."""
    from src.ui_visual import initialize_modern_ui, apply_widget_specific_styles, VisualTheme
    
    # Initialize modern UI
    style_manager = initialize_modern_ui(app)
    
    # Create test window
    window = QWidget()
    window.setWindowTitle("Spanish Subjunctive Practice - Visual Test")
    window.setMinimumSize(900, 700)
    window.resize(900, 700)
    
    layout = QVBoxLayout(window)
    
    # Title
    title = QLabel("Spanish Subjunctive Practice - Refined Visual Design")
    title.setStyleSheet(f"""
        font-size: {VisualTheme.FONTS['sizes']['title']};
        font-weight: {VisualTheme.FONTS['weights']['bold']};
        color: {VisualTheme.COLORS['primary']};
        margin: {VisualTheme.SPACING['lg']} 0;
    """)
    layout.addWidget(title)
    
    # Main content area split
    content_layout = QHBoxLayout()
    
    # Left panel - similar to the actual app
    left_panel = QGroupBox("Subjunctive Context & Triggers")
    left_layout = QVBoxLayout(left_panel)
    
    sentence_label = QLabel("Espero que tú _____ (venir) a la fiesta mañana.")
    sentence_label.setWordWrap(True)
    left_layout.addWidget(sentence_label)
    
    translation_label = QLabel("I hope that you come to the party tomorrow.")
    translation_label.setProperty('role', 'secondary')
    translation_label.setStyleSheet(f"color: {VisualTheme.COLORS['text_secondary']};")
    left_layout.addWidget(translation_label)
    
    # Trigger checkboxes
    trigger_group = QGroupBox("Select Triggers")
    trigger_layout = QVBoxLayout(trigger_group)
    
    triggers = ["Wishes (esperar que)", "Emotions (sentir que)", "Doubt (dudar que)"]
    for trigger in triggers:
        cb = QCheckBox(trigger)
        if trigger == triggers[0]:  # Check first one
            cb.setChecked(True)
        trigger_layout.addWidget(cb)
    
    left_layout.addWidget(trigger_group)
    left_layout.addStretch()
    
    content_layout.addWidget(left_panel, 1)
    
    # Right panel - controls
    right_panel = QGroupBox("Practice Controls")
    right_layout = QVBoxLayout(right_panel)
    
    # Tense selection
    tense_group = QGroupBox("Select Tense")
    tense_layout = QVBoxLayout(tense_group)
    
    tenses = ["Present Subjunctive", "Imperfect Subjunctive", "Present Perfect Subjunctive"]
    for tense in tenses:
        cb = QCheckBox(tense)
        if tense == tenses[0]:
            cb.setChecked(True)
        tense_layout.addWidget(cb)
    
    right_layout.addWidget(tense_group)
    
    # Mode selection
    mode_layout = QHBoxLayout()
    mode_label = QLabel("Mode:")
    mode_combo = QComboBox()
    mode_combo.addItems(["Free Response", "Multiple Choice"])
    mode_layout.addWidget(mode_label)
    mode_layout.addWidget(mode_combo)
    mode_layout.addStretch()
    right_layout.addLayout(mode_layout)
    
    # Answer input
    answer_input = QLineEdit()
    answer_input.setPlaceholderText("Type your answer here (e.g., vengas)...")
    right_layout.addWidget(answer_input)
    
    # Buttons with improved styling
    button_layout = QHBoxLayout()
    prev_btn = QPushButton("Previous")
    hint_btn = QPushButton("Hint")
    submit_btn = QPushButton("Submit")
    next_btn = QPushButton("Next")
    
    # Apply visual styling
    apply_widget_specific_styles(submit_btn, 'primary-button')
    apply_widget_specific_styles(hint_btn, 'secondary-button')
    apply_widget_specific_styles(prev_btn, 'secondary-button')
    apply_widget_specific_styles(next_btn, 'secondary-button')
    
    button_layout.addWidget(prev_btn)
    button_layout.addWidget(hint_btn)
    button_layout.addWidget(submit_btn)
    button_layout.addWidget(next_btn)
    right_layout.addLayout(button_layout)
    
    # Feedback area
    feedback = QTextEdit()
    feedback.setPlaceholderText("Feedback and explanations will appear here...")
    feedback.setMaximumHeight(150)
    right_layout.addWidget(feedback)
    
    # Progress bar
    progress = QProgressBar()
    progress.setValue(3)
    progress.setMaximum(10)
    progress.setFormat("Exercise %v of %m")
    right_layout.addWidget(progress)
    
    content_layout.addWidget(right_panel, 2)
    layout.addLayout(content_layout)
    
    # Theme toggle button
    theme_toggle = QPushButton("Toggle Dark Theme")
    theme_toggle.clicked.connect(style_manager.toggle_theme)
    layout.addWidget(theme_toggle)
    
    # Test results label
    results_label = QLabel("✓ Visual design improvements applied successfully!")
    results_label.setStyleSheet(f"""
        background-color: {VisualTheme.COLORS['success_light']};
        color: {VisualTheme.COLORS['success']};
        padding: {VisualTheme.SPACING['md']};
        border-radius: {VisualTheme.RADIUS['base']};
        font-weight: {VisualTheme.FONTS['weights']['medium']};
    """)
    layout.addWidget(results_label)
    
    return window, style_manager

def main():
    """Run the visual test."""
    print("Testing Spanish Subjunctive Practice UI Visual Improvements")
    print("=" * 60)
    
    # Test import
    if not test_visual_module():
        print("Cannot proceed with visual tests - module not available")
        return 1
    
    # Create test application
    app = QApplication(sys.argv)
    
    try:
        window, style_manager = create_test_ui(app)
        window.show()
        
        print("✓ Visual test window created successfully")
        print("✓ Modern theme applied")
        print("✓ Interactive theme switching available")
        print("\nFeatures demonstrated:")
        print("  • Clean, modern color scheme with good contrast")
        print("  • Simplified button styling with clear hover states")
        print("  • Better spacing and typography")
        print("  • Cohesive visual language across components")
        print("  • Theme switching (light/dark)")
        print("\nClose the window to complete the test.")
        
        return app.exec_()
        
    except Exception as e:
        print(f"✗ Error creating test UI: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
"""
Practical demonstration of the Clean UI Color System integration
with the Subjunctive Practice application components.
"""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    PYQT_AVAILABLE = True
except ImportError:
    PYQT_AVAILABLE = False
    print("PyQt5 not available. This demo requires PyQt5 to run.")

if PYQT_AVAILABLE:
    from clean_ui_colors import CleanColors, ColorScheme, primary, success, warning, error, gray
    from ui_enhancements import ModernButton, ExerciseCard, SmartInputField, FeedbackCard, ModernTheme


class ColorSystemDemo(QMainWindow):
    """Demonstration of the clean color system in action"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clean UI Color System - Subjunctive Practice Demo")
        self.setGeometry(100, 100, 1000, 700)
        
        # Apply the modern theme
        self.setStyleSheet(ModernTheme.get_light_theme())
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the demonstration interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        
        # Header
        header = QLabel("🎨 Clean UI Color System Demonstration")
        header.setStyleSheet(f"""
            font-size: 24px; 
            font-weight: bold; 
            color: {CleanColors.TEXT_PRIMARY}; 
            padding: 20px;
            background: {CleanColors.PRIMARY_LIGHT};
            border-radius: 12px;
            border-left: 4px solid {CleanColors.PRIMARY};
        """)
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)
        
        # Create demo sections
        demo_scroll = QScrollArea()
        demo_widget = QWidget()
        demo_layout = QVBoxLayout(demo_widget)
        
        # Button demonstrations
        self.add_button_demo(demo_layout)
        
        # Input field demonstrations
        self.add_input_demo(demo_layout)
        
        # Feedback card demonstrations
        self.add_feedback_demo(demo_layout)
        
        # Exercise card demonstration
        self.add_exercise_demo(demo_layout)
        
        # Color palette display
        self.add_palette_demo(demo_layout)
        
        demo_scroll.setWidget(demo_widget)
        demo_scroll.setWidgetResizable(True)
        main_layout.addWidget(demo_scroll)
        
        # Theme toggle
        theme_layout = QHBoxLayout()
        theme_layout.addStretch()
        
        light_btn = ModernButton("Light Theme", "primary")
        dark_btn = ModernButton("Dark Theme", "secondary")
        
        light_btn.clicked.connect(self.apply_light_theme)
        dark_btn.clicked.connect(self.apply_dark_theme)
        
        theme_layout.addWidget(light_btn)
        theme_layout.addWidget(dark_btn)
        theme_layout.addStretch()
        
        main_layout.addLayout(theme_layout)
    
    def add_button_demo(self, layout):
        """Add button demonstrations"""
        section = self.create_demo_section("Modern Buttons", layout)
        
        button_layout = QHBoxLayout()
        
        # Different button types
        primary_btn = ModernButton("Primary Action", "primary")
        secondary_btn = ModernButton("Secondary Action", "secondary")
        
        # Status buttons
        success_btn = QPushButton("Success State")
        success_btn.setStyleSheet(f"""
            QPushButton {{
                background: {CleanColors.SUCCESS};
                color: {CleanColors.TEXT_WHITE};
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background: {CleanColors.SUCCESS_HOVER};
            }}
        """)
        
        error_btn = QPushButton("Error State")
        error_btn.setStyleSheet(f"""
            QPushButton {{
                background: {CleanColors.ERROR};
                color: {CleanColors.TEXT_WHITE};
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background: {CleanColors.ERROR_HOVER};
            }}
        """)
        
        warning_btn = QPushButton("Warning State")
        warning_btn.setStyleSheet(f"""
            QPushButton {{
                background: {CleanColors.WARNING};
                color: {CleanColors.TEXT_WHITE};
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background: {CleanColors.WARNING_HOVER};
            }}
        """)
        
        button_layout.addWidget(primary_btn)
        button_layout.addWidget(secondary_btn)
        button_layout.addWidget(success_btn)
        button_layout.addWidget(error_btn)
        button_layout.addWidget(warning_btn)
        
        section.addLayout(button_layout)
    
    def add_input_demo(self, layout):
        """Add input field demonstrations"""
        section = self.create_demo_section("Smart Input Fields", layout)
        
        input_layout = QVBoxLayout()
        
        # Different input states
        neutral_input = SmartInputField()
        neutral_input.setPlaceholderText("Neutral state - type your answer")
        
        correct_input = SmartInputField()
        correct_input.setText("¡Excelente!")
        correct_input.apply_correct_style()
        
        incorrect_input = SmartInputField()
        incorrect_input.setText("hablo (incorrect)")
        incorrect_input.apply_incorrect_style()
        
        # Add demo buttons
        demo_buttons = QHBoxLayout()
        neutral_btn = QPushButton("Show Neutral")
        correct_btn = QPushButton("Show Correct")
        incorrect_btn = QPushButton("Show Incorrect")
        
        neutral_btn.clicked.connect(lambda: self.demo_input_state(neutral_input, 'neutral'))
        correct_btn.clicked.connect(lambda: self.demo_input_state(neutral_input, 'correct'))
        incorrect_btn.clicked.connect(lambda: self.demo_input_state(neutral_input, 'incorrect'))
        
        demo_buttons.addWidget(neutral_btn)
        demo_buttons.addWidget(correct_btn)
        demo_buttons.addWidget(incorrect_btn)
        demo_buttons.addStretch()
        
        input_layout.addWidget(QLabel("Interactive Input (try the buttons):"))
        input_layout.addWidget(neutral_input)
        input_layout.addLayout(demo_buttons)
        
        input_layout.addWidget(QLabel("Correct Answer State:"))
        input_layout.addWidget(correct_input)
        
        input_layout.addWidget(QLabel("Incorrect Answer State:"))
        input_layout.addWidget(incorrect_input)
        
        section.addLayout(input_layout)
    
    def add_feedback_demo(self, layout):
        """Add feedback card demonstrations"""
        section = self.create_demo_section("Feedback Cards", layout)
        
        feedback_layout = QHBoxLayout()
        
        # Success feedback
        success_card = FeedbackCard()
        success_card.show_correct_feedback("¡Perfecto! You've mastered the subjunctive trigger!")
        
        # Error feedback
        error_card = FeedbackCard()
        error_card.show_incorrect_feedback("Remember: emotions trigger the subjunctive mood.")
        
        # Hint feedback
        hint_card = FeedbackCard()
        hint_card.show_hint("Look for words expressing doubt, emotion, or desire...")
        
        feedback_layout.addWidget(success_card)
        feedback_layout.addWidget(error_card)
        feedback_layout.addWidget(hint_card)
        
        section.addLayout(feedback_layout)
    
    def add_exercise_demo(self, layout):
        """Add exercise card demonstration"""
        section = self.create_demo_section("Exercise Card", layout)
        
        exercise_card = ExerciseCard()
        exercise_card.update_content(
            context="Expressing emotion about future events",
            sentence="Espero que tú _____ (tener) éxito en el examen.",
            translation="I hope you have success on the exam.",
            show_translation=True
        )
        
        section.addWidget(exercise_card)
    
    def add_palette_demo(self, layout):
        """Add color palette demonstration"""
        section = self.create_demo_section("Complete Color Palette", layout)
        
        palette_layout = QGridLayout()
        
        # Color categories with swatches
        color_categories = [
            ("Primary", [
                ("Primary", CleanColors.PRIMARY),
                ("Primary Hover", CleanColors.PRIMARY_HOVER),
                ("Primary Light", CleanColors.PRIMARY_LIGHT)
            ]),
            ("Success", [
                ("Success", CleanColors.SUCCESS),
                ("Success Hover", CleanColors.SUCCESS_HOVER),
                ("Success Light", CleanColors.SUCCESS_LIGHT)
            ]),
            ("Warning", [
                ("Warning", CleanColors.WARNING),
                ("Warning Hover", CleanColors.WARNING_HOVER),
                ("Warning Light", CleanColors.WARNING_LIGHT)
            ]),
            ("Error", [
                ("Error", CleanColors.ERROR),
                ("Error Hover", CleanColors.ERROR_HOVER),
                ("Error Light", CleanColors.ERROR_LIGHT)
            ])
        ]
        
        row = 0
        for category_name, colors in color_categories:
            # Category header
            header = QLabel(f"🎨 {category_name}")
            header.setStyleSheet(f"font-weight: bold; color: {CleanColors.TEXT_PRIMARY}; padding: 5px;")
            palette_layout.addWidget(header, row, 0, 1, 3)
            row += 1
            
            # Color swatches
            col = 0
            for color_name, color_value in colors:
                swatch = self.create_color_swatch(color_name, color_value)
                palette_layout.addWidget(swatch, row, col)
                col += 1
            row += 1
        
        # Gray scale
        gray_header = QLabel("⚫ Gray Scale")
        gray_header.setStyleSheet(f"font-weight: bold; color: {CleanColors.TEXT_PRIMARY}; padding: 5px;")
        palette_layout.addWidget(gray_header, row, 0, 1, 3)
        row += 1
        
        gray_layout = QHBoxLayout()
        for level in [100, 300, 500, 700, 900]:
            swatch = self.create_color_swatch(f"Gray {level}", gray(level))
            gray_layout.addWidget(swatch)
        
        gray_widget = QWidget()
        gray_widget.setLayout(gray_layout)
        palette_layout.addWidget(gray_widget, row, 0, 1, 3)
        
        section.addLayout(palette_layout)
    
    def create_demo_section(self, title, parent_layout):
        """Create a demo section with title"""
        # Section container
        section_frame = QFrame()
        section_frame.setStyleSheet(f"""
            QFrame {{
                background: {CleanColors.BACKGROUND_CARD};
                border: 1px solid {CleanColors.BORDER_LIGHT};
                border-radius: 12px;
                padding: 16px;
                margin: 8px;
            }}
        """)
        
        section_layout = QVBoxLayout(section_frame)
        
        # Section title
        section_title = QLabel(title)
        section_title.setStyleSheet(f"""
            font-size: 18px;
            font-weight: bold;
            color: {CleanColors.TEXT_PRIMARY};
            padding: 8px 0px;
            border-bottom: 2px solid {CleanColors.PRIMARY};
        """)
        section_layout.addWidget(section_title)
        
        parent_layout.addWidget(section_frame)
        return section_layout
    
    def create_color_swatch(self, name, color):
        """Create a color swatch widget"""
        swatch_widget = QWidget()
        swatch_widget.setFixedSize(80, 80)
        
        layout = QVBoxLayout(swatch_widget)
        layout.setContentsMargins(2, 2, 2, 2)
        
        # Color box
        color_box = QLabel()
        color_box.setFixedSize(60, 40)
        color_box.setStyleSheet(f"""
            background: {color};
            border: 1px solid {CleanColors.BORDER};
            border-radius: 4px;
        """)
        
        # Color name
        color_label = QLabel(name)
        color_label.setStyleSheet(f"""
            font-size: 10px;
            color: {CleanColors.TEXT_SECONDARY};
            text-align: center;
        """)
        color_label.setAlignment(Qt.AlignCenter)
        color_label.setWordWrap(True)
        
        # Color value
        value_label = QLabel(color)
        value_label.setStyleSheet(f"""
            font-size: 8px;
            color: {CleanColors.TEXT_MUTED};
            text-align: center;
            font-family: monospace;
        """)
        value_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(color_box)
        layout.addWidget(color_label)
        layout.addWidget(value_label)
        
        return swatch_widget
    
    def demo_input_state(self, input_field, state):
        """Demonstrate different input states"""
        if state == 'neutral':
            input_field.setText("")
            input_field.setPlaceholderText("Type your answer here...")
            input_field.apply_neutral_style()
        elif state == 'correct':
            input_field.setText("¡tengas!")
            input_field.apply_correct_style()
        elif state == 'incorrect':
            input_field.setText("tienes")
            input_field.apply_incorrect_style()
            input_field.shake_animation()
    
    def apply_light_theme(self):
        """Apply light theme"""
        self.setStyleSheet(ModernTheme.get_light_theme())
    
    def apply_dark_theme(self):
        """Apply dark theme"""
        self.setStyleSheet(ModernTheme.get_dark_theme())


def run_demo():
    """Run the color system demonstration"""
    if not PYQT_AVAILABLE:
        print("This demo requires PyQt5 to run.")
        print("Install PyQt5 with: pip install PyQt5")
        return
    
    app = QApplication(sys.argv)
    
    # Set application-wide styling
    app.setStyle('Fusion')  # Use Fusion style for better consistency
    
    demo = ColorSystemDemo()
    demo.show()
    
    print("Clean UI Color System Demo launched!")
    print("Features demonstrated:")
    print("• Modern button styles with hover effects")
    print("• Smart input fields with state-based styling")
    print("• Feedback cards with semantic colors")
    print("• Exercise card with contextual styling")
    print("• Complete color palette with swatches")
    print("• Light/dark theme switching")
    print("• WCAG 2.1 AA compliant color combinations")
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_demo()
"""
Test Script for Form Styling Fixes

This script tests the form styling fixes to ensure:
1. Red box issues are resolved
2. Text visibility is improved
3. Form elements are responsive
4. Hover and focus states work properly
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QCheckBox, QRadioButton, QTextEdit,
    QGroupBox, QPushButton, QButtonGroup
)
from PyQt5.QtCore import QTimer

# Import our form fixes
try:
    from form_integration import integrate_form_fixes, FormIntegrationManager
    FIXES_AVAILABLE = True
except ImportError:
    print("Form styling fixes not available - testing without fixes")
    FIXES_AVAILABLE = False


class FormTestWindow(QMainWindow):
    """
    Test window that replicates the form elements from the main application
    to test styling fixes.
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Form Styling Fixes - Test Window")
        self.setGeometry(100, 100, 1100, 700)
        
        # Initialize form integration manager
        self.form_integration_manager = None
        
        self.initUI()
        self.initFormFixes()
        
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("Form Styling Fixes Test")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        main_layout.addWidget(title)
        
        # Create form elements similar to main app
        self.createTriggerCheckboxes(main_layout)
        self.createSelectionBoxes(main_layout)
        self.createInputFields(main_layout)
        self.createTestButtons(main_layout)
        
    def createTriggerCheckboxes(self, layout):
        """Create trigger checkboxes like in main app"""
        trigger_box = QGroupBox("Subjunctive Indicators & Context")
        trigger_layout = QVBoxLayout(trigger_box)
        
        self.trigger_checkboxes = []
        triggers = [
            "Wishes (querer que, desear que)",
            "Emotions (gustar que, sentir que)", 
            "Impersonal expressions (es bueno que)",
            "Doubt/Denial (dudar que, no creer que)"
        ]
        
        for trigger in triggers:
            cb = QCheckBox(trigger)
            self.trigger_checkboxes.append(cb)
            trigger_layout.addWidget(cb)
            
        layout.addWidget(trigger_box)
        
    def createSelectionBoxes(self, layout):
        """Create tense and person selection boxes"""
        selection_box = QGroupBox("Select Tense(s) and Person(s)")
        sel_layout = QHBoxLayout(selection_box)
        
        # Tense checkboxes
        tense_box = QGroupBox("Tense(s)")
        tense_layout = QVBoxLayout(tense_box)
        
        self.tense_checkboxes = {}
        tenses = [
            "Present Subjunctive",
            "Imperfect Subjunctive (ra)",
            "Present Perfect Subjunctive"
        ]
        
        for tense in tenses:
            cb = QCheckBox(tense)
            self.tense_checkboxes[tense] = cb
            tense_layout.addWidget(cb)
            
        # Person checkboxes
        person_box = QGroupBox("Person(s)")
        person_layout = QVBoxLayout(person_box)
        
        self.person_checkboxes = {}
        persons = ["yo", "tú", "él/ella/usted", "nosotros"]
        
        for person in persons:
            cb = QCheckBox(person)
            self.person_checkboxes[person] = cb
            person_layout.addWidget(cb)
            
        sel_layout.addWidget(tense_box)
        sel_layout.addWidget(person_box)
        layout.addWidget(selection_box)
        
    def createInputFields(self, layout):
        """Create input fields and combo boxes"""
        input_group = QGroupBox("Input Fields Test")
        input_layout = QVBoxLayout(input_group)
        
        # Text input
        input_layout.addWidget(QLabel("Free Response Input:"))
        self.free_response_input = QLineEdit()
        self.free_response_input.setPlaceholderText("Type your Spanish answer here...")
        input_layout.addWidget(self.free_response_input)
        
        # Context input
        input_layout.addWidget(QLabel("Custom Context:"))
        self.custom_context_input = QLineEdit()
        self.custom_context_input.setPlaceholderText("Enter additional context...")
        input_layout.addWidget(self.custom_context_input)
        
        # Combo boxes
        combo_layout = QHBoxLayout()
        
        combo_layout.addWidget(QLabel("Mode:"))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Free Response", "Multiple Choice"])
        combo_layout.addWidget(self.mode_combo)
        
        combo_layout.addWidget(QLabel("Difficulty:"))
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Beginner", "Intermediate", "Advanced"])
        combo_layout.addWidget(self.difficulty_combo)
        
        input_layout.addLayout(combo_layout)
        
        # Multiple choice radio buttons
        mc_group = QGroupBox("Multiple Choice Options")
        mc_layout = QVBoxLayout(mc_group)
        
        self.mc_button_group = QButtonGroup()
        for i, option in enumerate(["hable", "habla", "hablar", "hablara"]):
            radio = QRadioButton(option)
            self.mc_button_group.addButton(radio, i)
            mc_layout.addWidget(radio)
            
        input_layout.addWidget(mc_group)
        
        # Text edit area
        input_layout.addWidget(QLabel("Feedback Area:"))
        self.feedback_text = QTextEdit()
        self.feedback_text.setPlaceholderText("Feedback will appear here...")
        self.feedback_text.setMaximumHeight(120)
        input_layout.addWidget(self.feedback_text)
        
        layout.addWidget(input_group)
        
    def createTestButtons(self, layout):
        """Create test buttons"""
        button_layout = QHBoxLayout()
        
        test_success_btn = QPushButton("Test Success State")
        test_success_btn.clicked.connect(self.testSuccessState)
        
        test_error_btn = QPushButton("Test Error State")
        test_error_btn.clicked.connect(self.testErrorState)
        
        test_neutral_btn = QPushButton("Reset to Neutral")
        test_neutral_btn.clicked.connect(self.testNeutralState)
        
        toggle_theme_btn = QPushButton("Toggle Dark Mode")
        toggle_theme_btn.clicked.connect(self.toggleTheme)
        
        button_layout.addWidget(test_success_btn)
        button_layout.addWidget(test_error_btn)
        button_layout.addWidget(test_neutral_btn)
        button_layout.addWidget(toggle_theme_btn)
        
        layout.addLayout(button_layout)
        
    def initFormFixes(self):
        """Initialize form styling fixes"""
        if FIXES_AVAILABLE:
            app = QApplication.instance()
            if app:
                self.form_integration_manager = integrate_form_fixes(app, self, False)
                if self.form_integration_manager:
                    print("✅ Form styling fixes initialized successfully!")
                    print("   - Red box issues should be resolved")
                    print("   - Text visibility should be improved") 
                    print("   - Form elements should be responsive")
                    print("   - Hover/focus states should work properly")
                else:
                    print("❌ Failed to initialize form styling fixes")
            else:
                print("❌ No QApplication instance found")
        else:
            print("❌ Form styling fixes not available")
            
    def testSuccessState(self):
        """Test success validation state"""
        if self.form_integration_manager:
            self.form_integration_manager.set_form_validation_state(
                self.free_response_input, 'success', 'Great job!'
            )
            print("✅ Applied success state to input field")
            
    def testErrorState(self):
        """Test error validation state"""
        if self.form_integration_manager:
            self.form_integration_manager.set_form_validation_state(
                self.free_response_input, 'error', 'Incorrect answer'
            )
            print("❌ Applied error state to input field")
            
    def testNeutralState(self):
        """Test neutral state"""
        if self.form_integration_manager:
            self.form_integration_manager.set_form_validation_state(
                self.free_response_input, 'neutral', ''
            )
            print("🔄 Reset to neutral state")
            
    def toggleTheme(self):
        """Toggle dark mode"""
        if self.form_integration_manager:
            new_mode = self.form_integration_manager.toggle_dark_mode()
            mode_name = "dark" if new_mode else "light"
            print(f"🌓 Switched to {mode_name} mode")


def run_form_tests():
    """Run comprehensive form styling tests"""
    print("🧪 Starting Form Styling Fixes Test")
    print("=" * 50)
    
    app = QApplication(sys.argv)
    
    # Create test window
    test_window = FormTestWindow()
    
    print("\n📋 Test Instructions:")
    print("1. Check that checkboxes don't have harsh red focus boxes")
    print("2. Verify input fields have good text visibility")
    print("3. Test responsive behavior by resizing window")
    print("4. Try hover and focus states on all elements")
    print("5. Use buttons to test validation states")
    print("6. Toggle dark mode to test theme switching")
    print("\n" + "=" * 50)
    
    test_window.show()
    
    # Schedule some automated tests
    def run_automated_tests():
        print("\n🤖 Running automated tests...")
        test_window.testSuccessState()
        QTimer.singleShot(2000, test_window.testErrorState)
        QTimer.singleShot(4000, test_window.testNeutralState)
        QTimer.singleShot(6000, test_window.toggleTheme)
    
    QTimer.singleShot(3000, run_automated_tests)
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_form_tests()
"""
Test script for input field display fixes
Verifies that all input field styling issues have been resolved.
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QGroupBox, QCheckBox, QRadioButton, QPushButton
from PyQt5.QtCore import Qt

class InputFieldTestWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Input Field Fixes Test')
        self.setGeometry(100, 100, 800, 600)
        
        layout = QVBoxLayout()
        
        # Test title
        title = QLabel("Input Field Display Fixes Test")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px 0;")
        layout.addWidget(title)
        
        # Test group for pronouns (like in the subjunctive app)
        pronoun_group = QGroupBox("Pronouns (yo, tú, él/ella/usted)")
        pronoun_layout = QVBoxLayout(pronoun_group)
        
        # Add pronoun checkboxes like in the original app
        pronouns = ["yo", "tú", "él/ella/usted", "nosotros", "vosotros", "ellos/ellas/ustedes"]
        for pronoun in pronouns:
            cb = QCheckBox(pronoun)
            pronoun_layout.addWidget(cb)
        
        layout.addWidget(pronoun_group)
        
        # Test input fields group
        input_group = QGroupBox("Test Input Fields")
        input_layout = QVBoxLayout(input_group)
        
        # Free response input (like in the subjunctive app)
        input_layout.addWidget(QLabel("Free Response Input:"))
        free_response = QLineEdit()
        free_response.setPlaceholderText("Type your Spanish answer here...")
        input_layout.addWidget(free_response)
        
        # Context input (like in the subjunctive app)
        input_layout.addWidget(QLabel("Custom Context:"))
        context_input = QLineEdit()
        context_input.setPlaceholderText("Enter additional context (e.g., polite request, uncertainty scenario)")
        input_layout.addWidget(context_input)
        
        # Verbs input (like in the subjunctive app)
        input_layout.addWidget(QLabel("Specific Verbs:"))
        verbs_input = QLineEdit()
        verbs_input.setPlaceholderText("e.g., hablar, comer, vivir")
        input_layout.addWidget(verbs_input)
        
        layout.addWidget(input_group)
        
        # Test buttons
        button_layout = QHBoxLayout()
        
        test_light_btn = QPushButton("Test Light Theme")
        test_light_btn.clicked.connect(self.apply_light_theme)
        button_layout.addWidget(test_light_btn)
        
        test_dark_btn = QPushButton("Test Dark Theme")
        test_dark_btn.clicked.connect(self.apply_dark_theme)
        button_layout.addWidget(test_dark_btn)
        
        layout.addLayout(button_layout)
        
        # Results label
        self.results_label = QLabel("Click buttons to test themes. Check that:\n• Input fields have clean borders (no red)\n• Text is visible when typed\n• Placeholder text is visible\n• Pronoun labels are clearly visible")
        self.results_label.setWordWrap(True)
        self.results_label.setStyleSheet("margin: 20px 0; padding: 10px; background-color: #f0f0f0; border-radius: 5px;")
        layout.addWidget(self.results_label)
        
        self.setLayout(layout)
    
    def apply_light_theme(self):
        """Apply the same light theme styles as in main.py"""
        light_style = """
            QWidget {
                background-color: #f0f0f0;
            }
            QMainWindow {
                background-color: #f8f8f8;
            }
            QLabel {
                background-color: transparent;
                color: #1A202C;
                font-weight: 500;
                font-size: 14px;
                padding: 2px 0;
            }
            QCheckBox {
                color: #1A202C;
                font-weight: 500;
                font-size: 14px;
                padding: 4px 0;
            }
            QRadioButton {
                color: #1A202C;
                font-weight: 500;
                font-size: 14px;
                padding: 4px 0;
            }
            QGroupBox {
                font-weight: 600;
                font-size: 16px;
                color: #1A202C;
                border: 2px solid #E2E8F0;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 16px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                color: #3B82F6;
                font-weight: 600;
            }
            QPushButton {
                background-color: #e0e0e0;
                border: 1px solid #ccc;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
            QLineEdit {
                background-color: white;
                border: 2px solid #CBD5E0;
                padding: 8px 12px;
                border-radius: 6px;
                font-size: 14px;
                color: #1A202C;
                min-height: 20px;
                outline: none;
            }
            QLineEdit:focus {
                border-color: #3B82F6;
                background-color: #FFFFFF;
                outline: none;
            }
            QLineEdit:hover {
                border-color: #A0AEC0;
                background-color: #FAFBFC;
            }
            QLineEdit::placeholder {
                color: #9CA3AF;
                font-style: italic;
            }
        """
        self.setStyleSheet(light_style)
        self.results_label.setText("✅ Light theme applied. Check that input fields display correctly with clean borders.")
    
    def apply_dark_theme(self):
        """Apply the same dark theme styles as in main.py"""
        dark_style = """
            QMainWindow { background-color: #2b2b2b; color: #ffffff; }
            QWidget { background-color: transparent; color: #ffffff; }
            QLabel { 
                background-color: transparent; 
                color: #F7FAFC; 
                font-weight: 500;
                font-size: 14px;
                padding: 2px 0;
            }
            QCheckBox { 
                color: #F7FAFC; 
                font-weight: 500;
                font-size: 14px;
                padding: 4px 0;
            }
            QRadioButton { 
                color: #F7FAFC; 
                font-weight: 500;
                font-size: 14px;
                padding: 4px 0;
            }
            QGroupBox { 
                font-weight: 600;
                font-size: 16px;
                color: #F7FAFC;
                border: 2px solid #4A5568;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 16px;
                background-color: #3c3c3c;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                color: #63B3ED;
                font-weight: 600;
            }
            QPushButton { background-color: #0066cc; color: white; padding: 8px; border-radius: 4px; }
            QPushButton:hover { background-color: #0052a3; }
            QLineEdit {
                background-color: #2D3748;
                border: 2px solid #4A5568;
                padding: 8px 12px;
                border-radius: 6px;
                font-size: 14px;
                color: #F7FAFC;
                min-height: 20px;
                outline: none;
            }
            QLineEdit:focus {
                border-color: #63B3ED;
                background-color: #2D3748;
                outline: none;
            }
            QLineEdit:hover {
                border-color: #718096;
                background-color: #4A5568;
            }
            QLineEdit::placeholder {
                color: #718096;
                font-style: italic;
            }
        """
        self.setStyleSheet(dark_style)
        self.results_label.setText("✅ Dark theme applied. Check that input fields display correctly with clean borders.")

def main():
    app = QApplication(sys.argv)
    
    # Create and show the test widget
    test_widget = InputFieldTestWidget()
    test_widget.show()
    
    # Apply initial light theme
    test_widget.apply_light_theme()
    
    print("Input Field Fixes Test Started")
    print("=" * 50)
    print("Test the following:")
    print("1. Input fields have clean, professional borders (no red)")
    print("2. Text is visible when typed in input fields")
    print("3. Placeholder text is clearly visible")
    print("4. Pronoun labels are clearly readable")
    print("5. Both light and dark themes work properly")
    print("6. Hover and focus states work correctly")
    print("=" * 50)
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
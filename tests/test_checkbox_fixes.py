#!/usr/bin/env python3
"""
Test script to verify checkbox styling fixes
Tests that checkboxes render properly without red borders and with clear checked/unchecked states
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QGroupBox, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class CheckboxTestWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Checkbox Styling Test")
        self.setGeometry(300, 300, 600, 400)
        
        # Apply the same stylesheet as the main application
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            QLabel {
                background-color: transparent;
                color: #333;
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
            
            /* Checkbox styling fixes - remove red borders and ensure visibility */
            QCheckBox {
                background-color: transparent;
                color: #333;
                spacing: 8px;
                padding: 4px;
                border: none;
                font-size: 13px;
            }
            
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid #888;
                border-radius: 3px;
                background-color: white;
            }
            
            QCheckBox::indicator:hover {
                border-color: #555;
                background-color: #f5f5f5;
            }
            
            QCheckBox::indicator:checked {
                background-color: #4a90e2;
                border-color: #4a90e2;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOSIgdmlld0JveD0iMCAwIDEyIDkiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDQuNUw0LjUgOEwxMSAxIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K);
            }
            
            QCheckBox::indicator:checked:hover {
                background-color: #357abd;
                border-color: #357abd;
            }
            
            QCheckBox::indicator:focus {
                border: 2px solid #4a90e2;
                outline: none;
            }
            
            QCheckBox::indicator:disabled {
                background-color: #f0f0f0;
                border-color: #ccc;
            }
            
            /* Group box styling for consistent appearance */
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                background-color: #f0f0f0;
            }
        """)
        
        self.setup_ui()
    
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Checkbox Styling Test")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Bold))
        main_layout.addWidget(title)
        
        # Test instructions
        instructions = QLabel("""
        This test verifies checkbox styling fixes:
        1. No red borders should be visible
        2. Checkbox indicators should be clearly visible
        3. Checked/unchecked states should be distinct
        4. Hover effects should work properly
        5. Focus states should be visible
        """)
        instructions.setWordWrap(True)
        main_layout.addWidget(instructions)
        
        # Test sections layout
        test_layout = QHBoxLayout()
        main_layout.addLayout(test_layout)
        
        # Tense checkboxes (mimicking the main app)
        tense_box = QGroupBox("Tense(s)")
        tense_layout = QVBoxLayout(tense_box)
        
        tenses = [
            "Present Subjunctive",
            "Imperfect Subjunctive (ra)",
            "Imperfect Subjunctive (se)",
            "Present Perfect Subjunctive",
            "Pluperfect Subjunctive",
        ]
        
        self.tense_checkboxes = {}
        for tense in tenses:
            cb = QCheckBox(tense)
            self.tense_checkboxes[tense] = cb
            tense_layout.addWidget(cb)
        
        test_layout.addWidget(tense_box)
        
        # Person checkboxes (mimicking the main app)
        person_box = QGroupBox("Person(s)")
        person_layout = QVBoxLayout(person_box)
        
        persons = ["yo", "tú", "él/ella/usted", "nosotros", "vosotros", "ellos/ellas/ustedes"]
        
        self.person_checkboxes = {}
        for person in persons:
            cb = QCheckBox(person)
            self.person_checkboxes[person] = cb
            person_layout.addWidget(cb)
        
        test_layout.addWidget(person_box)
        
        # Trigger checkboxes (mimicking the main app)
        trigger_box = QGroupBox("Subjunctive Triggers")
        trigger_layout = QVBoxLayout(trigger_box)
        
        triggers = [
            "Wishes (querer que, desear que)",
            "Emotions (gustar que, sentir que)",
            "Impersonal expressions (es bueno que)",
            "Requests (pedir que, rogar que)",
            "Doubt/Denial (dudar que, no creer que)",
        ]
        
        self.trigger_checkboxes = []
        for trigger in triggers:
            cb = QCheckBox(trigger)
            self.trigger_checkboxes.append(cb)
            trigger_layout.addWidget(cb)
        
        test_layout.addWidget(trigger_box)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        check_all_btn = QPushButton("Check All")
        check_all_btn.clicked.connect(self.check_all)
        button_layout.addWidget(check_all_btn)
        
        uncheck_all_btn = QPushButton("Uncheck All")
        uncheck_all_btn.clicked.connect(self.uncheck_all)
        button_layout.addWidget(uncheck_all_btn)
        
        test_states_btn = QPushButton("Test States")
        test_states_btn.clicked.connect(self.test_states)
        button_layout.addWidget(test_states_btn)
        
        main_layout.addLayout(button_layout)
        
        # Status label
        self.status_label = QLabel("Ready to test checkbox styling")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)
    
    def check_all(self):
        """Check all checkboxes to test checked state visibility"""
        for cb in self.tense_checkboxes.values():
            cb.setChecked(True)
        for cb in self.person_checkboxes.values():
            cb.setChecked(True)
        for cb in self.trigger_checkboxes:
            cb.setChecked(True)
        self.status_label.setText("All checkboxes checked - verify check marks are visible")
    
    def uncheck_all(self):
        """Uncheck all checkboxes to test unchecked state visibility"""
        for cb in self.tense_checkboxes.values():
            cb.setChecked(False)
        for cb in self.person_checkboxes.values():
            cb.setChecked(False)
        for cb in self.trigger_checkboxes:
            cb.setChecked(False)
        self.status_label.setText("All checkboxes unchecked - verify empty boxes are visible")
    
    def test_states(self):
        """Test alternating states to verify both checked and unchecked are visible"""
        # Check every other checkbox
        tense_items = list(self.tense_checkboxes.values())
        for i, cb in enumerate(tense_items):
            cb.setChecked(i % 2 == 0)
        
        person_items = list(self.person_checkboxes.values())
        for i, cb in enumerate(person_items):
            cb.setChecked(i % 2 == 1)
        
        for i, cb in enumerate(self.trigger_checkboxes):
            cb.setChecked(i % 2 == 0)
        
        self.status_label.setText("Alternating states - verify both checked and unchecked are clearly visible")


def main():
    """Run the checkbox styling test"""
    app = QApplication(sys.argv)
    
    # Test window
    test_widget = CheckboxTestWidget()
    test_widget.show()
    
    print("Checkbox styling test started")
    print("Visual checks to perform:")
    print("1. No red borders around checkboxes")
    print("2. Clear distinction between checked/unchecked states")
    print("3. Hover effects work properly")
    print("4. Focus states are visible when using tab navigation")
    print("5. Consistent styling across all sections")
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
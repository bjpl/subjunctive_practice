#!/usr/bin/env python3
"""
Simple test to verify main application checkbox fixes work
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

def test_main_app():
    """Test the main application with checkbox fixes"""
    try:
        # Import and initialize the main GUI
        from main import SpanishSubjunctivePracticeGUI
        
        app = QApplication(sys.argv)
        
        # Create the main window
        window = SpanishSubjunctivePracticeGUI()
        
        # Show the window
        window.show()
        
        print("Main application started successfully with checkbox fixes")
        print("Visual verification points:")
        print("1. Check 'Subjunctive Indicators & Context' section - checkboxes should have no red borders")
        print("2. Check 'Select Tense(s) and Person(s)' section - checkboxes should render clearly")
        print("3. All checkboxes should show clear checked/unchecked states")
        print("4. Hover over checkboxes to verify hover effects work")
        print("5. Use Tab key to verify focus states are visible")
        
        # Close after a few seconds for automated testing
        QTimer.singleShot(3000, app.quit)
        
        return app.exec_()
        
    except Exception as e:
        print(f"Error testing main application: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(test_main_app())
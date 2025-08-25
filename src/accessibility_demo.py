"""
Accessibility Features Demo for Spanish Subjunctive Practice App

This module demonstrates and tests the accessibility features implemented
in the ui_accessibility.py module. It can be run independently to test
accessibility features or used as a reference for implementation.
"""

import sys
from typing import Dict, List
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
    QPushButton, QLineEdit, QLabel, QCheckBox, QRadioButton, QComboBox,
    QTextEdit, QGroupBox, QProgressBar, QDialog, QMessageBox, QButtonGroup
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QKeySequence

from ui_accessibility import AccessibilityManager, AccessibilityDialog


class AccessibilityDemoWindow(QMainWindow):
    """
    Demo window that simulates the main Spanish subjunctive practice app
    but focuses on showcasing accessibility features.
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Accessibility Features Demo - Spanish Subjunctive Practice")
        self.setGeometry(100, 100, 1000, 700)
        
        # Simulate main app attributes
        self.current_exercise = 0
        self.total_exercises = 5
        self.correct_count = 0
        
        self.init_ui()
        self.setup_accessibility()
    
    def init_ui(self):
        """Initialize the demo UI with elements similar to the main app"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Header with accessibility info
        header_group = QGroupBox("Accessibility Demo")
        header_layout = QVBoxLayout(header_group)
        
        info_label = QLabel(
            "This demo showcases accessibility features for the Spanish Subjunctive Practice app.\n"
            "Press ESC for help, Alt+H for high contrast, Alt+F for large fonts."
        )
        info_label.setWordWrap(True)
        header_layout.addWidget(info_label)
        main_layout.addWidget(header_group)
        
        # Simulate exercise area
        exercise_group = QGroupBox("Exercise Area")
        exercise_layout = QVBoxLayout(exercise_group)
        
        self.sentence_label = QLabel("Ejemplo: Espero que tú _____ (hablar) español bien.")
        self.sentence_label.setFont(QFont("Arial", 14))
        self.sentence_label.setAccessibleName("Current Exercise")
        self.sentence_label.setAccessibleDescription("Spanish sentence to complete with subjunctive form")
        exercise_layout.addWidget(self.sentence_label)
        
        self.translation_label = QLabel("Translation: I hope that you speak Spanish well.")
        self.translation_label.setStyleSheet("color: gray; font-style: italic;")
        self.translation_label.setAccessibleName("Exercise Translation")
        exercise_layout.addWidget(self.translation_label)
        
        main_layout.addWidget(exercise_group)
        
        # Answer input area
        answer_group = QGroupBox("Answer Input")
        answer_layout = QVBoxLayout(answer_group)
        
        # Free response input
        self.free_response_input = QLineEdit()
        self.free_response_input.setPlaceholderText("Type your subjunctive verb form here...")
        self.free_response_input.setAccessibleName("Answer Input Field")
        self.free_response_input.setAccessibleDescription("Enter the correct subjunctive form of the verb")
        answer_layout.addWidget(self.free_response_input)
        
        # Multiple choice simulation
        mc_group = QGroupBox("Multiple Choice (Demo)")
        mc_layout = QHBoxLayout(mc_group)
        
        self.mc_button_group = QButtonGroup()
        choices = ["hables", "hablas", "hablaste", "hablarás"]
        for i, choice in enumerate(choices):
            radio = QRadioButton(choice)
            radio.setAccessibleDescription(f"Choice {i+1}: {choice}")
            self.mc_button_group.addButton(radio)
            mc_layout.addWidget(radio)
        
        answer_layout.addWidget(mc_group)
        main_layout.addWidget(answer_group)
        
        # Control buttons
        controls_group = QGroupBox("Controls")
        controls_layout = QHBoxLayout(controls_group)
        
        self.submit_button = QPushButton("Submit Answer")
        self.submit_button.setAccessibleName("Submit Answer")
        self.submit_button.setAccessibleDescription("Submit your current answer (Press Enter)")
        self.submit_button.setShortcut(QKeySequence("Return"))
        self.submit_button.clicked.connect(self.demo_submit)
        
        self.hint_button = QPushButton("Get Hint")
        self.hint_button.setAccessibleName("Get Hint")
        self.hint_button.setAccessibleDescription("Request a hint for the current exercise (Press H)")
        self.hint_button.setShortcut(QKeySequence("H"))
        self.hint_button.clicked.connect(self.demo_hint)
        
        self.prev_button = QPushButton("Previous")
        self.prev_button.setAccessibleName("Previous Exercise")
        self.prev_button.setAccessibleDescription("Go to previous exercise (Press Left Arrow)")
        self.prev_button.setShortcut(QKeySequence("Left"))
        self.prev_button.clicked.connect(self.demo_prev)
        
        self.next_button = QPushButton("Next")
        self.next_button.setAccessibleName("Next Exercise")
        self.next_button.setAccessibleDescription("Move to next exercise (Press Right Arrow)")
        self.next_button.setShortcut(QKeySequence("Right"))
        self.next_button.clicked.connect(self.demo_next)
        
        controls_layout.addWidget(self.prev_button)
        controls_layout.addWidget(self.hint_button)
        controls_layout.addWidget(self.submit_button)
        controls_layout.addWidget(self.next_button)
        main_layout.addWidget(controls_group)
        
        # Feedback area
        feedback_group = QGroupBox("Feedback")
        feedback_layout = QVBoxLayout(feedback_group)
        
        self.feedback_text = QTextEdit()
        self.feedback_text.setReadOnly(True)
        self.feedback_text.setAccessibleName("Exercise Feedback")
        self.feedback_text.setAccessibleDescription("Displays explanations and feedback for answers")
        self.feedback_text.setPlainText("Feedback will appear here after submitting an answer.")
        feedback_layout.addWidget(self.feedback_text)
        
        main_layout.addWidget(feedback_group)
        
        # Progress and stats
        stats_group = QGroupBox("Progress")
        stats_layout = QVBoxLayout(stats_group)
        
        self.stats_label = QLabel(f"Exercise: {self.current_exercise + 1}/{self.total_exercises} | Correct: {self.correct_count}")
        self.stats_label.setAccessibleName("Progress Statistics")
        self.stats_label.setAccessibleDescription("Shows current exercise number and correct answers")
        stats_layout.addWidget(self.stats_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(self.total_exercises)
        self.progress_bar.setValue(self.current_exercise + 1)
        self.progress_bar.setAccessibleName("Exercise Progress")
        self.progress_bar.setAccessibleDescription("Visual progress indicator showing completion")
        stats_layout.addWidget(self.progress_bar)
        
        main_layout.addWidget(stats_group)
        
        # Accessibility test controls
        test_group = QGroupBox("Accessibility Test Controls")
        test_layout = QHBoxLayout(test_group)
        
        contrast_btn = QPushButton("Toggle High Contrast")
        contrast_btn.clicked.connect(self.test_high_contrast)
        contrast_btn.setAccessibleDescription("Test high contrast mode toggle")
        
        font_btn = QPushButton("Toggle Large Fonts")
        font_btn.clicked.connect(self.test_large_fonts)
        font_btn.setAccessibleDescription("Test large font mode toggle")
        
        settings_btn = QPushButton("Accessibility Settings")
        settings_btn.clicked.connect(self.show_accessibility_settings)
        settings_btn.setAccessibleDescription("Open accessibility settings dialog")
        
        test_layout.addWidget(contrast_btn)
        test_layout.addWidget(font_btn)
        test_layout.addWidget(settings_btn)
        main_layout.addWidget(test_group)
        
        # Status bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Accessibility demo ready. Press ESC for help.")
    
    def setup_accessibility(self):
        """Set up accessibility features for the demo"""
        try:
            self.accessibility_manager = AccessibilityManager(self)
            
            # Connect signals for demo feedback
            self.accessibility_manager.focus_changed.connect(self.on_accessibility_announcement)
            
            self.updateStatus("Accessibility features initialized successfully!")
            
        except Exception as e:
            self.updateStatus(f"Accessibility setup failed: {e}")
            self.accessibility_manager = None
    
    def updateStatus(self, message: str):
        """Update status bar with message"""
        self.status_bar.showMessage(message, 5000)
    
    def on_accessibility_announcement(self, text: str):
        """Handle accessibility announcements"""
        self.updateStatus(f"🔊 {text}")
    
    # Demo button handlers
    def demo_submit(self):
        """Demo submit functionality"""
        answer = self.free_response_input.text().strip()
        if not answer:
            self.updateStatus("Please enter an answer first.")
            return
        
        # Simulate correct/incorrect feedback
        if answer.lower() in ["hables", "hable"]:
            self.feedback_text.setPlainText(
                f"Correct! '{answer}' is the proper subjunctive form.\n\n"
                "Explanation: After 'espero que' (I hope that), we use the present subjunctive. "
                "For the verb 'hablar' with 'tú', the form is 'hables'."
            )
            self.correct_count += 1
            if self.accessibility_manager:
                self.accessibility_manager._announce_text("Correct answer! Well done.")
        else:
            self.feedback_text.setPlainText(
                f"Incorrect. You answered '{answer}', but the correct form is 'hables'.\n\n"
                "Remember: 'Esperar que' triggers the subjunctive mood. "
                "The present subjunctive of 'hablar' for 'tú' is 'hables'."
            )
            if self.accessibility_manager:
                self.accessibility_manager._announce_text("Incorrect. Check the feedback for explanation.")
        
        self.update_stats()
        self.free_response_input.clear()
    
    def demo_hint(self):
        """Demo hint functionality"""
        hint = (
            "Hint: The verb 'esperar que' (to hope that) requires the subjunctive mood. "
            "Think about the present subjunctive conjugation of 'hablar' for 'tú'."
        )
        self.feedback_text.setPlainText(hint)
        if self.accessibility_manager:
            self.accessibility_manager._announce_text("Hint provided. Check feedback area.")
    
    def demo_next(self):
        """Demo next exercise functionality"""
        if self.current_exercise < self.total_exercises - 1:
            self.current_exercise += 1
            self.update_exercise()
            if self.accessibility_manager:
                self.accessibility_manager._announce_text(
                    f"Exercise {self.current_exercise + 1} of {self.total_exercises}"
                )
        else:
            self.updateStatus("You're at the last exercise.")
    
    def demo_prev(self):
        """Demo previous exercise functionality"""
        if self.current_exercise > 0:
            self.current_exercise -= 1
            self.update_exercise()
            if self.accessibility_manager:
                self.accessibility_manager._announce_text(
                    f"Exercise {self.current_exercise + 1} of {self.total_exercises}"
                )
        else:
            self.updateStatus("You're at the first exercise.")
    
    def update_exercise(self):
        """Update exercise display"""
        exercises = [
            ("Espero que tú _____ (hablar) español bien.", "I hope that you speak Spanish well.", "hables"),
            ("Es importante que nosotros _____ (estudiar) mucho.", "It's important that we study a lot.", "estudiemos"),
            ("Dudo que ella _____ (venir) a la fiesta.", "I doubt that she will come to the party.", "venga"),
            ("Me alegra que ustedes _____ (estar) aquí.", "I'm happy that you all are here.", "estén"),
            ("No creo que él _____ (saber) la respuesta.", "I don't think he knows the answer.", "sepa")
        ]
        
        if 0 <= self.current_exercise < len(exercises):
            spanish, english, correct = exercises[self.current_exercise]
            self.sentence_label.setText(spanish)
            self.translation_label.setText(f"Translation: {english}")
            self.feedback_text.clear()
        
        self.update_stats()
    
    def update_stats(self):
        """Update statistics display"""
        self.stats_label.setText(
            f"Exercise: {self.current_exercise + 1}/{self.total_exercises} | Correct: {self.correct_count}"
        )
        self.progress_bar.setValue(self.current_exercise + 1)
    
    # Accessibility test methods
    def test_high_contrast(self):
        """Test high contrast toggle"""
        if self.accessibility_manager:
            self.accessibility_manager.toggle_high_contrast()
        else:
            self.updateStatus("Accessibility manager not available")
    
    def test_large_fonts(self):
        """Test large fonts toggle"""
        if self.accessibility_manager:
            self.accessibility_manager.toggle_large_fonts()
        else:
            self.updateStatus("Accessibility manager not available")
    
    def show_accessibility_settings(self):
        """Show accessibility settings dialog"""
        if self.accessibility_manager:
            dialog = AccessibilityDialog(self.accessibility_manager, self)
            dialog.exec_()
        else:
            QMessageBox.warning(self, "Not Available", "Accessibility manager not initialized.")


class AccessibilityFeatureTest:
    """
    Test class for validating accessibility features
    """
    
    def __init__(self, demo_window: AccessibilityDemoWindow):
        self.demo = demo_window
        self.test_results = {}
    
    def run_all_tests(self) -> Dict[str, bool]:
        """Run all accessibility tests"""
        tests = [
            ("keyboard_navigation", self.test_keyboard_navigation),
            ("focus_indicators", self.test_focus_indicators),
            ("screen_reader_support", self.test_screen_reader_support),
            ("high_contrast", self.test_high_contrast_mode),
            ("font_scaling", self.test_font_scaling),
            ("accessible_labels", self.test_accessible_labels),
            ("keyboard_shortcuts", self.test_keyboard_shortcuts)
        ]
        
        for test_name, test_func in tests:
            try:
                self.test_results[test_name] = test_func()
                print(f"✓ {test_name}: {'PASS' if self.test_results[test_name] else 'FAIL'}")
            except Exception as e:
                self.test_results[test_name] = False
                print(f"✗ {test_name}: ERROR - {e}")
        
        return self.test_results
    
    def test_keyboard_navigation(self) -> bool:
        """Test keyboard navigation functionality"""
        # Check if tab navigation works
        focusable_widgets = []
        for widget in self.demo.findChildren(QWidget):
            if widget.focusPolicy() != Qt.NoFocus and widget.isVisible():
                focusable_widgets.append(widget)
        
        return len(focusable_widgets) > 0
    
    def test_focus_indicators(self) -> bool:
        """Test focus indicator visibility"""
        # Test that focus styling is applied
        test_widget = self.demo.submit_button
        test_widget.setFocus()
        
        # Check if accessibility manager exists and has focus styling
        return (self.demo.accessibility_manager is not None and
                hasattr(self.demo.accessibility_manager, '_setup_focus_indicators'))
    
    def test_screen_reader_support(self) -> bool:
        """Test screen reader support features"""
        # Check if widgets have accessible names and descriptions
        test_widgets = [
            self.demo.sentence_label,
            self.demo.free_response_input,
            self.demo.submit_button,
            self.demo.feedback_text
        ]
        
        has_accessible_properties = True
        for widget in test_widgets:
            if not (hasattr(widget, 'accessibleName') and widget.accessibleName()):
                has_accessible_properties = False
                break
        
        return has_accessible_properties
    
    def test_high_contrast_mode(self) -> bool:
        """Test high contrast mode toggle"""
        if not self.demo.accessibility_manager:
            return False
        
        initial_state = self.demo.accessibility_manager.high_contrast_enabled
        self.demo.accessibility_manager.toggle_high_contrast()
        changed_state = self.demo.accessibility_manager.high_contrast_enabled
        
        # Toggle back to original state
        if initial_state != changed_state:
            self.demo.accessibility_manager.toggle_high_contrast()
        
        return initial_state != changed_state
    
    def test_font_scaling(self) -> bool:
        """Test font scaling functionality"""
        if not self.demo.accessibility_manager:
            return False
        
        initial_state = self.demo.accessibility_manager.large_font_enabled
        self.demo.accessibility_manager.toggle_large_fonts()
        changed_state = self.demo.accessibility_manager.large_font_enabled
        
        # Toggle back to original state
        if initial_state != changed_state:
            self.demo.accessibility_manager.toggle_large_fonts()
        
        return initial_state != changed_state
    
    def test_accessible_labels(self) -> bool:
        """Test that all interactive elements have accessible labels"""
        interactive_widgets = [
            self.demo.submit_button,
            self.demo.hint_button,
            self.demo.next_button,
            self.demo.prev_button,
            self.demo.free_response_input
        ]
        
        for widget in interactive_widgets:
            if not widget.accessibleName():
                return False
        
        return True
    
    def test_keyboard_shortcuts(self) -> bool:
        """Test keyboard shortcuts are properly configured"""
        shortcuts_exist = (
            self.demo.submit_button.shortcut() == QKeySequence("Return") and
            self.demo.hint_button.shortcut() == QKeySequence("H") and
            self.demo.next_button.shortcut() == QKeySequence("Right") and
            self.demo.prev_button.shortcut() == QKeySequence("Left")
        )
        
        return shortcuts_exist
    
    def generate_report(self) -> str:
        """Generate accessibility test report"""
        if not self.test_results:
            return "No tests have been run yet."
        
        passed = sum(1 for result in self.test_results.values() if result)
        total = len(self.test_results)
        
        report = f"ACCESSIBILITY TEST REPORT\n"
        report += f"={'=' * 40}\n\n"
        report += f"Overall: {passed}/{total} tests passed\n\n"
        
        for test_name, result in self.test_results.items():
            status = "PASS ✓" if result else "FAIL ✗"
            report += f"{test_name.replace('_', ' ').title()}: {status}\n"
        
        report += f"\n{'=' * 40}\n"
        
        if passed == total:
            report += "All accessibility tests passed! The application meets basic accessibility requirements."
        else:
            report += f"{total - passed} test(s) failed. Review the implementation for the failing features."
        
        return report


def main():
    """Main function to run the accessibility demo"""
    app = QApplication(sys.argv)
    
    # Set application properties for accessibility
    app.setApplicationName("Spanish Subjunctive Practice - Accessibility Demo")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Educational Software")
    
    # Create demo window
    demo_window = AccessibilityDemoWindow()
    demo_window.show()
    
    # Run accessibility tests after a short delay
    def run_tests():
        tester = AccessibilityFeatureTest(demo_window)
        results = tester.run_all_tests()
        report = tester.generate_report()
        print("\n" + report)
        
        # Show results in the demo window
        demo_window.feedback_text.setPlainText(report)
        demo_window.updateStatus(f"Accessibility tests completed: {sum(results.values())}/{len(results)} passed")
    
    # Run tests after 2 seconds to allow UI to fully initialize
    QTimer.singleShot(2000, run_tests)
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
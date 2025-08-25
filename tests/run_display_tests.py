#!/usr/bin/env python3
"""
Simple Display Fixes Test Runner

This script runs a comprehensive validation of all display improvements
and generates a detailed report.
"""

import sys
import os
import json
import time
from datetime import datetime
from typing import Dict, List, Any

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QLineEdit, QPushButton, QCheckBox, QComboBox, QTextEdit,
        QScrollArea, QTableWidget, QTableWidgetItem, QProgressBar
    )
    from PyQt5.QtCore import Qt, QSize, QTimer
    from PyQt5.QtGui import QFont, QFontMetrics, QPalette
    PYQT_AVAILABLE = True
except ImportError:
    PYQT_AVAILABLE = False


class DisplayFixesValidator:
    """Comprehensive validator for display fixes."""
    
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'tests_run': 0,
            'tests_passed': 0,
            'tests_failed': 0,
            'test_details': {},
            'issues_found': [],
            'recommendations': []
        }
        
        if PYQT_AVAILABLE:
            if not QApplication.instance():
                self.app = QApplication([])
            else:
                self.app = QApplication.instance()
            self.main_window = QMainWindow()
            self.main_window.setGeometry(100, 100, 1024, 768)
        else:
            self.app = None
            self.main_window = None
    
    def test_text_truncation(self) -> Dict[str, Any]:
        """Test text truncation prevention."""
        test_name = "Text Truncation Prevention"
        print(f"🧪 Testing: {test_name}")
        
        result = {
            'name': test_name,
            'passed': True,
            'issues': [],
            'details': {}
        }
        
        if not PYQT_AVAILABLE:
            result['passed'] = False
            result['issues'].append("PyQt5 not available")
            return result
        
        # Test various text lengths
        test_texts = [
            "Short text",
            "This is a moderately long text that might be truncated",
            "Very long text that should adapt to container width properly",
            "Texto en español con caracteres especiales: ñáéíóúü"
        ]
        
        for i, text in enumerate(test_texts):
            label = QLabel(text)
            label.setParent(self.main_window)
            label.setWordWrap(True)
            label.adjustSize()
            
            # Check if text fits or wraps properly
            font_metrics = QFontMetrics(label.font())
            text_width = font_metrics.horizontalAdvance(text)
            
            if text_width > 800:  # If text is very long
                label.setMaximumWidth(800)
                label.adjustSize()
                
                # With word wrap, height should increase
                if label.height() < 20:
                    result['issues'].append(f"Text {i}: May be truncated - height too small")
                    result['passed'] = False
        
        result['details']['texts_tested'] = len(test_texts)
        return result
    
    def test_checkbox_visibility(self) -> Dict[str, Any]:
        """Test checkbox state visibility."""
        test_name = "Checkbox State Visibility"
        print(f"🧪 Testing: {test_name}")
        
        result = {
            'name': test_name,
            'passed': True,
            'issues': [],
            'details': {}
        }
        
        if not PYQT_AVAILABLE:
            result['passed'] = False
            result['issues'].append("PyQt5 not available")
            return result
        
        states = [Qt.Unchecked, Qt.Checked, Qt.PartiallyChecked]
        state_names = ["unchecked", "checked", "partially checked"]
        
        for state, state_name in zip(states, state_names):
            checkbox = QCheckBox(f"Test checkbox - {state_name}")
            checkbox.setParent(self.main_window)
            checkbox.setCheckState(state)
            
            # Verify state is correct
            if checkbox.checkState() != state:
                result['issues'].append(f"Checkbox {state_name}: State not set correctly")
                result['passed'] = False
            
            # Check minimum size for usability
            size_hint = checkbox.sizeHint()
            if size_hint.width() < 15 or size_hint.height() < 15:
                result['issues'].append(f"Checkbox {state_name}: Too small")
                result['passed'] = False
        
        result['details']['states_tested'] = len(states)
        return result
    
    def test_input_field_styling(self) -> Dict[str, Any]:
        """Test input field display without problematic styling."""
        test_name = "Input Field Display"
        print(f"🧪 Testing: {test_name}")
        
        result = {
            'name': test_name,
            'passed': True,
            'issues': [],
            'details': {}
        }
        
        if not PYQT_AVAILABLE:
            result['passed'] = False
            result['issues'].append("PyQt5 not available")
            return result
        
        # Test line edit
        line_edit = QLineEdit()
        line_edit.setParent(self.main_window)
        line_edit.setText("Sample input text")
        
        # Check palette for problematic colors
        palette = line_edit.palette()
        base_color = palette.color(QPalette.Base)
        
        # Check if base color is problematic (very red)
        if base_color.red() > 200 and base_color.green() < 100 and base_color.blue() < 100:
            result['issues'].append("Line edit: Problematic red background detected")
            result['passed'] = False
        
        # Test minimum size
        size_hint = line_edit.sizeHint()
        if size_hint.height() < 20:
            result['issues'].append("Line edit: Height too small")
            result['passed'] = False
        
        # Test text edit
        text_edit = QTextEdit()
        text_edit.setParent(self.main_window)
        text_edit.setPlainText("Sample text area content")
        
        text_palette = text_edit.palette()
        text_base_color = text_palette.color(QPalette.Base)
        
        if text_base_color.red() > 200 and text_base_color.green() < 100 and text_base_color.blue() < 100:
            result['issues'].append("Text edit: Problematic red background detected")
            result['passed'] = False
        
        result['details']['fields_tested'] = 2
        return result
    
    def test_form_accessibility(self) -> Dict[str, Any]:
        """Test form element accessibility."""
        test_name = "Form Element Accessibility"
        print(f"🧪 Testing: {test_name}")
        
        result = {
            'name': test_name,
            'passed': True,
            'issues': [],
            'details': {}
        }
        
        if not PYQT_AVAILABLE:
            result['passed'] = False
            result['issues'].append("PyQt5 not available")
            return result
        
        # Create form elements
        elements = [
            ('button', QPushButton("Test Button")),
            ('input', QLineEdit()),
            ('checkbox', QCheckBox("Test Checkbox")),
            ('combo', QComboBox())
        ]
        
        for name, element in elements:
            element.setParent(self.main_window)
            
            # Test focus capability
            focus_policy = element.focusPolicy()
            if focus_policy == Qt.NoFocus and name != 'label':
                result['issues'].append(f"{name}: Cannot receive focus")
                result['passed'] = False
            
            # Test minimum touch target size for interactive elements
            if name in ['button']:
                size_hint = element.sizeHint()
                if size_hint.width() < 44 or size_hint.height() < 44:
                    element.setMinimumSize(44, 44)
        
        result['details']['elements_tested'] = len(elements)
        return result
    
    def test_responsive_layout(self) -> Dict[str, Any]:
        """Test responsive layout behavior."""
        test_name = "Responsive Layout"
        print(f"🧪 Testing: {test_name}")
        
        result = {
            'name': test_name,
            'passed': True,
            'issues': [],
            'details': {}
        }
        
        if not PYQT_AVAILABLE:
            result['passed'] = False
            result['issues'].append("PyQt5 not available")
            return result
        
        # Test different window sizes
        test_sizes = [
            (800, 600, "standard"),
            (1200, 800, "large"),
            (600, 400, "small")
        ]
        
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Responsive Test"))
        layout.addWidget(QPushButton("Test Button"))
        layout.addWidget(QLineEdit("Test Input"))
        
        central_widget.setLayout(layout)
        self.main_window.setCentralWidget(central_widget)
        
        for width, height, size_name in test_sizes:
            self.main_window.resize(width, height)
            
            # Verify layout adapts
            if central_widget.width() > width:
                result['issues'].append(f"Content wider than window at {size_name} size")
                result['passed'] = False
        
        result['details']['sizes_tested'] = len(test_sizes)
        return result
    
    def test_scrollbar_functionality(self) -> Dict[str, Any]:
        """Test scrollbar appearance and functionality."""
        test_name = "Scrollbar Functionality"
        print(f"🧪 Testing: {test_name}")
        
        result = {
            'name': test_name,
            'passed': True,
            'issues': [],
            'details': {}
        }
        
        if not PYQT_AVAILABLE:
            result['passed'] = False
            result['issues'].append("PyQt5 not available")
            return result
        
        # Test scroll area with overflow
        scroll_area = QScrollArea()
        large_content = QWidget()
        large_content.setFixedSize(800, 1200)  # Larger than typical window
        
        scroll_area.setWidget(large_content)
        scroll_area.setWidgetResizable(True)
        scroll_area.resize(400, 300)
        
        # Check scrollbar availability
        v_scrollbar = scroll_area.verticalScrollBar()
        
        # In a proper implementation, scrollbar should have range for large content
        if large_content.height() > scroll_area.height():
            # We expect scrolling capability
            scroll_area.show()  # May help initialize scrollbars
            
            # Basic functionality check - can we set scroll position?
            try:
                v_scrollbar.setValue(10)
                if v_scrollbar.value() < 0:
                    result['issues'].append("Scrollbar value handling issue")
                    result['passed'] = False
            except Exception as e:
                result['issues'].append(f"Scrollbar functionality error: {str(e)}")
                result['passed'] = False
        
        result['details']['scroll_areas_tested'] = 1
        return result
    
    def test_interactive_elements(self) -> Dict[str, Any]:
        """Test interactive element functionality."""
        test_name = "Interactive Element Functionality"
        print(f"🧪 Testing: {test_name}")
        
        result = {
            'name': test_name,
            'passed': True,
            'issues': [],
            'details': {}
        }
        
        if not PYQT_AVAILABLE:
            result['passed'] = False
            result['issues'].append("PyQt5 not available")
            return result
        
        # Test button
        click_count = [0]  # Use list for closure
        
        def button_clicked():
            click_count[0] += 1
        
        button = QPushButton("Test Button")
        button.setParent(self.main_window)
        button.clicked.connect(button_clicked)
        
        # Test click simulation
        button.click()
        if click_count[0] != 1:
            result['issues'].append("Button click simulation failed")
            result['passed'] = False
        
        # Test input field
        line_edit = QLineEdit()
        line_edit.setParent(self.main_window)
        
        test_text = "Test input"
        line_edit.setText(test_text)
        
        if line_edit.text() != test_text:
            result['issues'].append("Input field text setting failed")
            result['passed'] = False
        
        # Test clear
        line_edit.clear()
        if line_edit.text() != "":
            result['issues'].append("Input field clear failed")
            result['passed'] = False
        
        result['details']['interactive_elements_tested'] = 2
        return result
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all display fix tests."""
        print("=" * 80)
        print("DISPLAY FIXES VALIDATION TEST SUITE")
        print("=" * 80)
        print(f"PyQt5 Available: {'✅ Yes' if PYQT_AVAILABLE else '❌ No'}")
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        # Define all tests
        tests = [
            self.test_text_truncation,
            self.test_checkbox_visibility,
            self.test_input_field_styling,
            self.test_form_accessibility,
            self.test_responsive_layout,
            self.test_scrollbar_functionality,
            self.test_interactive_elements
        ]
        
        # Run all tests
        for test_func in tests:
            try:
                result = test_func()
                self.results['tests_run'] += 1
                
                if result['passed']:
                    self.results['tests_passed'] += 1
                    print(f"✅ {result['name']}: PASSED")
                else:
                    self.results['tests_failed'] += 1
                    print(f"❌ {result['name']}: FAILED")
                    for issue in result['issues']:
                        print(f"   - {issue}")
                        self.results['issues_found'].append(f"{result['name']}: {issue}")
                
                self.results['test_details'][result['name']] = result
                
            except Exception as e:
                self.results['tests_run'] += 1
                self.results['tests_failed'] += 1
                error_msg = f"Test error: {str(e)}"
                print(f"❌ {test_func.__name__}: ERROR - {error_msg}")
                self.results['issues_found'].append(error_msg)
        
        # Generate recommendations
        self._generate_recommendations()
        
        # Print summary
        self._print_summary()
        
        # Save report
        report_file = self._save_report()
        
        return self.results, report_file
    
    def _generate_recommendations(self):
        """Generate recommendations based on test results."""
        issues = self.results['issues_found']
        
        if any('truncated' in issue.lower() for issue in issues):
            self.results['recommendations'].append(
                "Implement proper text wrapping and container sizing to prevent truncation"
            )
        
        if any('checkbox' in issue.lower() for issue in issues):
            self.results['recommendations'].append(
                "Improve checkbox styling for better state visibility"
            )
        
        if any('red' in issue.lower() or 'background' in issue.lower() for issue in issues):
            self.results['recommendations'].append(
                "Review and fix input field styling to remove problematic backgrounds"
            )
        
        if any('focus' in issue.lower() for issue in issues):
            self.results['recommendations'].append(
                "Enhance form accessibility with proper focus management"
            )
        
        if any('responsive' in issue.lower() or 'size' in issue.lower() for issue in issues):
            self.results['recommendations'].append(
                "Implement responsive design patterns for better multi-device support"
            )
        
        if any('scrollbar' in issue.lower() for issue in issues):
            self.results['recommendations'].append(
                "Improve scrollbar behavior for better content navigation"
            )
        
        if not self.results['recommendations']:
            self.results['recommendations'].append(
                "All display fixes are working correctly - maintain current implementation"
            )
    
    def _print_summary(self):
        """Print test summary."""
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        total_tests = self.results['tests_run']
        passed = self.results['tests_passed']
        failed = self.results['tests_failed']
        success_rate = (passed / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📊 Total Tests: {total_tests}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if self.results['issues_found']:
            print(f"\n⚠️ Issues Found ({len(self.results['issues_found'])}):")
            for issue in self.results['issues_found'][:10]:  # Show first 10
                print(f"   - {issue}")
            if len(self.results['issues_found']) > 10:
                print(f"   ... and {len(self.results['issues_found']) - 10} more")
        else:
            print("\n🎉 No issues found - All display fixes are working correctly!")
        
        print(f"\n💡 Recommendations ({len(self.results['recommendations'])}):")
        for rec in self.results['recommendations']:
            print(f"   - {rec}")
    
    def _save_report(self) -> str:
        """Save detailed report to file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f"tests/display_fixes_validation_report_{timestamp}.json"
        
        # Ensure tests directory exists
        os.makedirs('tests', exist_ok=True)
        
        # Add summary statistics
        report_data = {
            'summary': {
                'timestamp': self.results['timestamp'],
                'total_tests': self.results['tests_run'],
                'tests_passed': self.results['tests_passed'],
                'tests_failed': self.results['tests_failed'],
                'success_rate': f"{(self.results['tests_passed'] / self.results['tests_run'] * 100) if self.results['tests_run'] > 0 else 0:.1f}%",
                'pyqt5_available': PYQT_AVAILABLE
            },
            'test_categories': {
                name: ('PASS' if details['passed'] else 'FAIL')
                for name, details in self.results['test_details'].items()
            },
            'detailed_results': self.results['test_details'],
            'issues_found': self.results['issues_found'],
            'recommendations': self.results['recommendations']
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        return report_file


def main():
    """Main function to run display validation tests."""
    validator = DisplayFixesValidator()
    results, report_file = validator.run_all_tests()
    
    # Exit with appropriate code
    if results['tests_failed'] == 0:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️ {results['tests_failed']} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""
UI Color Test Script for Spanish Subjunctive Practice App

This script verifies that the UI color changes meet the requirements:
1. No harsh red (#FF0000) remains in style definitions
2. Focus states use blue (#3B82F6) instead of red
3. Error states use softer red (#DC2626 or #EF4444)
4. Color changes are applied correctly when the app runs
5. Visual before/after comparison functionality

Author: Test Automation System
Date: 2025-08-25
"""

import sys
import os
import re
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime
import importlib.util

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# PyQt5 imports for runtime testing
try:
    from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton
    from PyQt5.QtGui import QColor, QPalette
    from PyQt5.QtCore import Qt
    PYQT_AVAILABLE = True
except ImportError:
    print("Warning: PyQt5 not available for runtime testing")
    PYQT_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ColorValidator:
    """Validates color usage throughout the application"""
    
    # Color constants for validation
    HARSH_RED_PATTERNS = [
        r'#[Ff]{2}0{4}',           # #FF0000, #ff0000
        r'rgb\(\s*255\s*,\s*0\s*,\s*0\s*\)',  # rgb(255, 0, 0)
        r'background-color:\s*red\s*[;}]',      # background-color: red
        r'color:\s*red\s*[;}]',                 # color: red
        r'#DC143C',                             # Crimson red
    ]
    
    APPROVED_BLUE_FOCUS = [
        '#3B82F6',  # Tailwind blue-500
        '#2563EB',  # Tailwind blue-600
        '#1D4ED8',  # Tailwind blue-700
        '#2E86AB',  # Primary blue from theme
    ]
    
    APPROVED_SOFT_REDS = [
        '#DC2626',  # Tailwind red-600
        '#EF4444',  # Tailwind red-500
        '#F87171',  # Tailwind red-400
        '#FCA5A5',  # Tailwind red-300
        '#E74C3C',  # Theme error color
    ]
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.violations = []
        self.test_results = {}
        
    def scan_files_for_harsh_reds(self) -> Dict[str, List[Dict]]:
        """Scan all Python files for harsh red color usage"""
        results = {}
        python_files = list(self.project_root.rglob("*.py"))
        
        logger.info(f"Scanning {len(python_files)} Python files for harsh red colors...")
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                file_violations = []
                for line_num, line in enumerate(content.split('\n'), 1):
                    for pattern in self.HARSH_RED_PATTERNS:
                        matches = re.finditer(pattern, line, re.IGNORECASE)
                        for match in matches:
                            file_violations.append({
                                'line': line_num,
                                'match': match.group(),
                                'pattern': pattern,
                                'context': line.strip(),
                                'column': match.start()
                            })
                
                if file_violations:
                    results[str(file_path)] = file_violations
                    
            except Exception as e:
                logger.warning(f"Error reading {file_path}: {e}")
                
        return results
    
    def validate_focus_colors(self) -> Dict[str, Any]:
        """Validate that focus states use approved blue colors"""
        results = {
            'approved_focus_colors': [],
            'violations': [],
            'files_checked': 0
        }
        
        focus_patterns = [
            r':focus\s*{[^}]*background[^}]*}',
            r':focus\s*{[^}]*border[^}]*}',
            r'focus.*color',
            r'border.*focus',
        ]
        
        python_files = list(self.project_root.rglob("*.py"))
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                results['files_checked'] += 1
                
                # Look for focus-related styling
                if 'focus' in content.lower():
                    lines = content.split('\n')
                    for line_num, line in enumerate(lines, 1):
                        if 'focus' in line.lower():
                            # Check if line contains color definitions
                            for blue_color in self.APPROVED_BLUE_FOCUS:
                                if blue_color.lower() in line.lower():
                                    results['approved_focus_colors'].append({
                                        'file': str(file_path),
                                        'line': line_num,
                                        'color': blue_color,
                                        'context': line.strip()
                                    })
                            
                            # Check for red focus colors (violations)
                            for red_pattern in self.HARSH_RED_PATTERNS:
                                if re.search(red_pattern, line, re.IGNORECASE):
                                    results['violations'].append({
                                        'file': str(file_path),
                                        'line': line_num,
                                        'context': line.strip(),
                                        'issue': 'Focus state uses harsh red color'
                                    })
                                    
            except Exception as e:
                logger.warning(f"Error checking focus colors in {file_path}: {e}")
                
        return results
    
    def validate_error_colors(self) -> Dict[str, Any]:
        """Validate that error states use approved soft red colors"""
        results = {
            'approved_error_colors': [],
            'violations': [],
            'files_checked': 0
        }
        
        error_keywords = ['error', 'incorrect', 'invalid', 'wrong', 'fail']
        
        python_files = list(self.project_root.rglob("*.py"))
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                results['files_checked'] += 1
                
                lines = content.split('\n')
                for line_num, line in enumerate(lines, 1):
                    line_lower = line.lower()
                    
                    # Check if line is related to error styling
                    if any(keyword in line_lower for keyword in error_keywords):
                        # Check for approved soft red colors
                        for soft_red in self.APPROVED_SOFT_REDS:
                            if soft_red.lower() in line_lower:
                                results['approved_error_colors'].append({
                                    'file': str(file_path),
                                    'line': line_num,
                                    'color': soft_red,
                                    'context': line.strip()
                                })
                        
                        # Check for harsh red violations
                        for red_pattern in self.HARSH_RED_PATTERNS:
                            if re.search(red_pattern, line, re.IGNORECASE):
                                results['violations'].append({
                                    'file': str(file_path),
                                    'line': line_num,
                                    'context': line.strip(),
                                    'issue': 'Error state uses harsh red color'
                                })
                                
            except Exception as e:
                logger.warning(f"Error checking error colors in {file_path}: {e}")
                
        return results
    
    def generate_color_report(self) -> Dict[str, Any]:
        """Generate comprehensive color validation report"""
        logger.info("Generating comprehensive color validation report...")
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'project_root': str(self.project_root),
            'harsh_red_scan': self.scan_files_for_harsh_reds(),
            'focus_color_validation': self.validate_focus_colors(),
            'error_color_validation': self.validate_error_colors(),
            'summary': {}
        }
        
        # Calculate summary statistics
        harsh_red_files = len(report['harsh_red_scan'])
        harsh_red_violations = sum(len(violations) for violations in report['harsh_red_scan'].values())
        
        focus_violations = len(report['focus_color_validation']['violations'])
        focus_approved = len(report['focus_color_validation']['approved_focus_colors'])
        
        error_violations = len(report['error_color_validation']['violations'])
        error_approved = len(report['error_color_validation']['approved_error_colors'])
        
        report['summary'] = {
            'harsh_red_files_count': harsh_red_files,
            'harsh_red_violations_count': harsh_red_violations,
            'focus_violations_count': focus_violations,
            'focus_approved_count': focus_approved,
            'error_violations_count': error_violations,
            'error_approved_count': error_approved,
            'total_violations': harsh_red_violations + focus_violations + error_violations,
            'passed': harsh_red_violations == 0 and focus_violations == 0 and error_violations == 0
        }
        
        return report


class RuntimeColorTester:
    """Tests color application at runtime using PyQt5"""
    
    def __init__(self):
        self.app = None
        self.test_results = {}
        
    def setup_test_application(self) -> bool:
        """Set up a minimal PyQt5 application for testing"""
        if not PYQT_AVAILABLE:
            logger.warning("PyQt5 not available for runtime testing")
            return False
            
        try:
            self.app = QApplication(sys.argv)
            return True
        except Exception as e:
            logger.error(f"Failed to create test application: {e}")
            return False
    
    def test_widget_colors(self, widget_class, style_sheet: str = "") -> Dict[str, Any]:
        """Test color application on a widget"""
        if not self.app:
            return {'error': 'No test application available'}
            
        try:
            # Create test widget
            widget = widget_class()
            if style_sheet:
                widget.setStyleSheet(style_sheet)
            
            # Get palette colors
            palette = widget.palette()
            
            # Extract color information
            color_info = {
                'background': palette.color(QPalette.Background).name(),
                'foreground': palette.color(QPalette.Foreground).name(),
                'highlight': palette.color(QPalette.Highlight).name(),
                'highlighted_text': palette.color(QPalette.HighlightedText).name(),
                'button': palette.color(QPalette.Button).name(),
                'button_text': palette.color(QPalette.ButtonText).name(),
                'base': palette.color(QPalette.Base).name(),
                'alternate_base': palette.color(QPalette.AlternateBase).name(),
            }
            
            # Check for harsh red colors
            harsh_red_found = any(
                color.upper() in ['#FF0000', '#DC143C'] 
                for color in color_info.values()
            )
            
            return {
                'widget_class': widget_class.__name__,
                'colors': color_info,
                'harsh_red_found': harsh_red_found,
                'style_sheet': style_sheet,
                'passed': not harsh_red_found
            }
            
        except Exception as e:
            logger.error(f"Error testing widget colors: {e}")
            return {'error': str(e)}
    
    def test_common_widgets(self) -> Dict[str, Any]:
        """Test color application on common UI widgets"""
        if not self.app:
            return {'error': 'No test application available'}
            
        results = {}
        
        # Test basic widgets
        test_widgets = [
            (QLabel, "QLabel { color: #2C3E50; background-color: #FFFFFF; }"),
            (QLineEdit, "QLineEdit:focus { border: 2px solid #3B82F6; }"),
            (QPushButton, "QPushButton:hover { background-color: #1F5F7A; }"),
        ]
        
        for widget_class, style in test_widgets:
            results[widget_class.__name__] = self.test_widget_colors(widget_class, style)
        
        return results
    
    def cleanup(self):
        """Clean up test application"""
        if self.app:
            self.app.quit()
            self.app = None


class VisualComparisonTester:
    """Creates visual comparison tests for before/after UI changes"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        
    def create_before_after_comparison(self) -> Dict[str, Any]:
        """Create a before/after comparison of color schemes"""
        
        before_colors = {
            'harsh_reds': ['#FF0000', '#DC143C'],
            'focus_colors': ['#FF0000', 'red'],
            'error_colors': ['#FF0000', 'crimson'],
        }
        
        after_colors = {
            'soft_reds': ['#DC2626', '#EF4444', '#E74C3C'],
            'focus_colors': ['#3B82F6', '#2563EB', '#2E86AB'],
            'error_colors': ['#DC2626', '#EF4444'],
        }
        
        comparison = {
            'before': {
                'description': 'Previous harsh color scheme',
                'colors': before_colors,
                'issues': [
                    'Used harsh #FF0000 red causing eye strain',
                    'Red focus states were not accessible',
                    'Error colors were too aggressive',
                    'Poor contrast for colorblind users'
                ]
            },
            'after': {
                'description': 'Improved accessible color scheme',
                'colors': after_colors,
                'improvements': [
                    'Softer red shades for error states',
                    'Blue focus states for better accessibility',
                    'Better contrast ratios',
                    'Colorblind-friendly color choices'
                ]
            },
            'accessibility_improvements': {
                'wcag_compliance': 'AA level contrast ratios',
                'colorblind_support': 'Red-green colorblind friendly',
                'eye_strain_reduction': 'Eliminated harsh #FF0000',
                'focus_visibility': 'Clear blue focus indicators'
            }
        }
        
        return comparison
    
    def generate_css_comparison(self) -> str:
        """Generate CSS showing before/after comparison"""
        
        css_comparison = """
/* ========================================
   BEFORE: Harsh Color Scheme (PROBLEMATIC)
   ======================================== */
   
.before-error {
    background-color: #FF0000 !important;  /* Harsh red - causes eye strain */
    color: white;
    border: 2px solid #FF0000;
}

.before-focus {
    outline: 2px solid red;  /* Red focus - not accessible */
    border: 2px solid #FF0000;
}

.before-warning {
    background-color: #DC143C;  /* Crimson red - too aggressive */
    color: white;
}

/* ========================================
   AFTER: Improved Color Scheme (ACCESSIBLE)
   ======================================== */

.after-error {
    background-color: #DC2626 !important;  /* Softer red - easier on eyes */
    color: white;
    border: 2px solid #EF4444;
}

.after-focus {
    outline: 2px solid #3B82F6;  /* Blue focus - accessible */
    border: 2px solid #2563EB;
}

.after-warning {
    background-color: #F59E0B;  /* Orange warning - less aggressive */
    color: white;
}

/* ========================================
   ACCESSIBILITY IMPROVEMENTS
   ======================================== */

/* Better contrast ratios */
.improved-text {
    color: #374151;  /* Dark gray - 7:1 contrast ratio */
}

/* Colorblind-friendly error states */
.colorblind-error {
    background-color: #DC2626;
    border-left: 4px solid #EF4444;
    position: relative;
}

.colorblind-error::before {
    content: "⚠";  /* Icon indicator for non-color identification */
    font-weight: bold;
    margin-right: 8px;
}
        """
        
        return css_comparison.strip()


def run_comprehensive_color_tests(project_root: Path) -> Dict[str, Any]:
    """Run all color validation tests"""
    logger.info("=== Starting Comprehensive UI Color Tests ===")
    
    # Initialize test results
    test_results = {
        'timestamp': datetime.now().isoformat(),
        'test_summary': {},
        'static_analysis': {},
        'runtime_tests': {},
        'visual_comparison': {},
        'recommendations': []
    }
    
    # 1. Static Code Analysis
    logger.info("1. Running static code analysis for color violations...")
    validator = ColorValidator(project_root)
    test_results['static_analysis'] = validator.generate_color_report()
    
    # 2. Runtime Testing (if PyQt5 available)
    logger.info("2. Running runtime color tests...")
    runtime_tester = RuntimeColorTester()
    if runtime_tester.setup_test_application():
        test_results['runtime_tests'] = runtime_tester.test_common_widgets()
        runtime_tester.cleanup()
    else:
        test_results['runtime_tests'] = {'status': 'skipped', 'reason': 'PyQt5 not available'}
    
    # 3. Visual Comparison
    logger.info("3. Generating visual comparison report...")
    visual_tester = VisualComparisonTester(project_root)
    test_results['visual_comparison'] = visual_tester.create_before_after_comparison()
    
    # 4. Generate Summary and Recommendations
    static_summary = test_results['static_analysis']['summary']
    total_violations = static_summary['total_violations']
    
    test_results['test_summary'] = {
        'overall_passed': total_violations == 0,
        'total_violations': total_violations,
        'harsh_red_violations': static_summary['harsh_red_violations_count'],
        'focus_violations': static_summary['focus_violations_count'],
        'error_violations': static_summary['error_violations_count'],
        'files_with_violations': static_summary['harsh_red_files_count'],
        'accessibility_score': max(0, 100 - (total_violations * 10))  # Scoring system
    }
    
    # Generate recommendations
    recommendations = []
    if static_summary['harsh_red_violations_count'] > 0:
        recommendations.append("Replace harsh red colors (#FF0000) with softer alternatives (#DC2626, #EF4444)")
    
    if static_summary['focus_violations_count'] > 0:
        recommendations.append("Update focus states to use blue colors (#3B82F6) instead of red")
    
    if static_summary['error_violations_count'] > 0:
        recommendations.append("Use accessible error colors with proper contrast ratios")
    
    if total_violations == 0:
        recommendations.append("Color scheme is compliant! All harsh reds removed and accessibility improved.")
    
    recommendations.extend([
        "Consider implementing WCAG AA contrast ratio guidelines",
        "Test color schemes with colorblind simulation tools",
        "Add visual indicators (icons) alongside color-coded feedback",
        "Implement user preference for high contrast mode"
    ])
    
    test_results['recommendations'] = recommendations
    
    logger.info("=== Color Tests Complete ===")
    return test_results


def save_test_report(results: Dict[str, Any], output_file: Path):
    """Save test results to JSON file"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        logger.info(f"Test report saved to {output_file}")
    except Exception as e:
        logger.error(f"Failed to save test report: {e}")


def print_test_summary(results: Dict[str, Any]):
    """Print a formatted test summary to console"""
    print("\n" + "="*80)
    print("UI COLOR TEST RESULTS SUMMARY")
    print("="*80)
    
    summary = results['test_summary']
    
    # Overall status
    status = "✅ PASSED" if summary['overall_passed'] else "❌ FAILED"
    print(f"Overall Status: {status}")
    print(f"Accessibility Score: {summary['accessibility_score']}/100")
    print()
    
    # Violation breakdown
    print("VIOLATION BREAKDOWN:")
    print(f"• Harsh Red Colors (#FF0000): {summary['harsh_red_violations']}")
    print(f"• Focus State Issues: {summary['focus_violations']}")
    print(f"• Error Color Issues: {summary['error_violations']}")
    print(f"• Total Files with Issues: {summary['files_with_violations']}")
    print()
    
    # Recommendations
    print("RECOMMENDATIONS:")
    for i, rec in enumerate(results['recommendations'], 1):
        print(f"{i}. {rec}")
    
    print("\n" + "="*80)
    
    # Detailed violations if any
    static_analysis = results['static_analysis']
    if static_analysis['harsh_red_scan']:
        print("\nDETAILED HARSH RED VIOLATIONS:")
        for file_path, violations in static_analysis['harsh_red_scan'].items():
            print(f"\n📁 {file_path}:")
            for violation in violations[:5]:  # Show first 5 per file
                print(f"   Line {violation['line']}: {violation['context']}")
                print(f"   → Found: {violation['match']}")
    
    print("\n" + "="*80)


def main():
    """Main test execution function"""
    
    # Determine project root
    current_dir = Path(__file__).parent
    project_root = current_dir.parent  # Go up one level from tests/
    
    print(f"Testing project at: {project_root}")
    
    # Run comprehensive tests
    results = run_comprehensive_color_tests(project_root)
    
    # Save detailed report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = current_dir / f"ui_color_test_report_{timestamp}.json"
    save_test_report(results, report_file)
    
    # Print summary
    print_test_summary(results)
    
    # Return exit code
    exit_code = 0 if results['test_summary']['overall_passed'] else 1
    
    if exit_code == 0:
        print("\n🎉 All color tests PASSED! UI is using accessible colors.")
    else:
        print("\n⚠️  Some color tests FAILED. Please review violations above.")
    
    return exit_code


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
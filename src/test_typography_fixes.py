"""
Test Script for Typography and Element Sizing Fixes

This script validates that the typography and sizing fixes are working correctly
by running various tests and generating reports.
"""

import sys
import os
from typing import Dict, List, Tuple

# Add the parent directory to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.enhanced_typography_system import (
        AccessibleTypography, AccessibleThemeManager, 
        create_accessible_typography_system
    )
    from src.typography_size_fixes import (
        apply_typography_size_fixes, get_accessibility_report,
        TypographySizeFixer
    )
    
    from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit
    from PyQt5.QtCore import Qt
    
    MODULES_AVAILABLE = True
    
except ImportError as e:
    print(f"Import error: {e}")
    MODULES_AVAILABLE = False


def create_test_window() -> QMainWindow:
    """Create a test window with various UI elements."""
    window = QMainWindow()
    window.setWindowTitle("Typography Fixes Test Window")
    window.setGeometry(100, 100, 800, 600)
    
    central = QWidget()
    window.setCentralWidget(central)
    layout = QVBoxLayout(central)
    
    # Add test elements
    title = QLabel("Test Typography System")
    layout.addWidget(title)
    
    sentence = QLabel("Es importante que tengas una buena experiencia de lectura con acentos y tildes.")
    layout.addWidget(sentence)
    
    translation = QLabel("It's important that you have a good reading experience with accents and tildes.")
    layout.addWidget(translation)
    
    # Buttons with different sizes
    small_btn = QPushButton("Small Button")
    normal_btn = QPushButton("Normal Button") 
    large_btn = QPushButton("Large Primary Button")
    
    layout.addWidget(small_btn)
    layout.addWidget(normal_btn)
    layout.addWidget(large_btn)
    
    # Input field
    input_field = QLineEdit()
    input_field.setPlaceholderText("Test input field")
    layout.addWidget(input_field)
    
    # Store references for testing
    window.sentence_label = sentence
    window.translation_label = translation
    window.submit_button = large_btn
    window.free_response_input = input_field
    
    return window


def test_font_sizes(window: QMainWindow) -> Dict[str, List[str]]:
    """Test that all text elements meet minimum font size requirements."""
    results = {
        'passed': [],
        'failed': [],
        'issues': []
    }
    
    # Test all labels
    labels = window.findChildren(QLabel)
    for label in labels:
        font = label.font()
        size = font.pixelSize() if font.pixelSize() > 0 else font.pointSize() * 1.33
        
        if size >= 14:  # Minimum readable size
            results['passed'].append(f"Label font size {size:.0f}px meets minimum requirement")
        else:
            results['failed'].append(f"Label font size {size:.0f}px below minimum (14px)")
    
    return results


def test_touch_targets(window: QMainWindow) -> Dict[str, List[str]]:
    """Test that interactive elements meet minimum touch target requirements."""
    results = {
        'passed': [],
        'failed': [],
        'issues': []
    }
    
    # Test buttons
    buttons = window.findChildren(QPushButton)
    for button in buttons:
        size = button.minimumSize()
        if size.width() >= 44 and size.height() >= 44:
            results['passed'].append(f"Button '{button.text()}' meets touch target requirement ({size.width()}x{size.height()}px)")
        else:
            results['failed'].append(f"Button '{button.text()}' below minimum touch target: {size.width()}x{size.height()}px (need 44x44px)")
    
    # Test input fields
    inputs = window.findChildren(QLineEdit)
    for input_field in inputs:
        height = input_field.minimumHeight()
        if height >= 44:
            results['passed'].append(f"Input field meets height requirement ({height}px)")
        else:
            results['failed'].append(f"Input field height {height}px below minimum (44px)")
    
    return results


def test_typography_system() -> Dict[str, any]:
    """Test the typography system components."""
    results = {
        'system_created': False,
        'fonts_created': False,
        'stylesheets_generated': False,
        'scaling_working': False,
        'errors': []
    }
    
    try:
        # Test typography system creation
        typography = AccessibleTypography()
        results['system_created'] = True
        
        # Test font creation
        font = typography.create_accessible_font('body', 'regular')
        if font and font.family():
            results['fonts_created'] = True
        
        # Test stylesheet generation
        stylesheet = typography.create_accessible_stylesheet('light')
        if stylesheet and 'font-size' in stylesheet:
            results['stylesheets_generated'] = True
        
        # Test scaling
        base_size = 16
        scaled_size = typography.scaler.get_scaled_font_size(base_size)
        if scaled_size >= 14:  # Should meet minimum
            results['scaling_working'] = True
        
    except Exception as e:
        results['errors'].append(str(e))
    
    return results


def run_comprehensive_test():
    """Run comprehensive tests of the typography and sizing fixes."""
    if not MODULES_AVAILABLE:
        print("❌ Cannot run tests - required modules not available")
        return
    
    print("🔍 Running Typography and Element Sizing Tests")
    print("=" * 60)
    
    # Create QApplication
    app = QApplication(sys.argv)
    
    # Test 1: Typography System Components
    print("\n📝 Testing Typography System Components...")
    typography_results = test_typography_system()
    
    print(f"  ✓ System Creation: {'✅' if typography_results['system_created'] else '❌'}")
    print(f"  ✓ Font Creation: {'✅' if typography_results['fonts_created'] else '❌'}")
    print(f"  ✓ Stylesheet Generation: {'✅' if typography_results['stylesheets_generated'] else '❌'}")
    print(f"  ✓ Scaling Functions: {'✅' if typography_results['scaling_working'] else '❌'}")
    
    if typography_results['errors']:
        print("  ❌ Errors found:")
        for error in typography_results['errors']:
            print(f"    - {error}")
    
    # Test 2: Create test window and apply fixes
    print("\n🎨 Testing Typography Fixes Application...")
    window = create_test_window()
    
    try:
        # Apply typography fixes
        fixer = TypographySizeFixer(window)
        fix_results = fixer.apply_comprehensive_fixes()
        
        if fix_results['success']:
            print(f"  ✅ Typography fixes applied successfully")
            print(f"  📊 Fixes applied: {len(fix_results['fixes_applied'])}")
            
            for fix in fix_results['fixes_applied'][:5]:  # Show first 5 fixes
                print(f"    - {fix}")
            if len(fix_results['fixes_applied']) > 5:
                print(f"    ... and {len(fix_results['fixes_applied']) - 5} more")
        else:
            print(f"  ❌ Typography fixes failed: {fix_results.get('error', 'Unknown error')}")
        
    except Exception as e:
        print(f"  ❌ Error applying fixes: {e}")
        fix_results = {'success': False}
    
    # Test 3: Font Size Compliance
    print("\n📏 Testing Font Size Compliance...")
    font_results = test_font_sizes(window)
    
    print(f"  ✅ Passed: {len(font_results['passed'])}")
    print(f"  ❌ Failed: {len(font_results['failed'])}")
    
    for failure in font_results['failed']:
        print(f"    - {failure}")
    
    # Test 4: Touch Target Compliance  
    print("\n👆 Testing Touch Target Compliance...")
    touch_results = test_touch_targets(window)
    
    print(f"  ✅ Passed: {len(touch_results['passed'])}")
    print(f"  ❌ Failed: {len(touch_results['failed'])}")
    
    for failure in touch_results['failed']:
        print(f"    - {failure}")
    
    # Test 5: Accessibility Report
    print("\n♿ Testing Accessibility Report Generation...")
    try:
        if fix_results.get('success'):
            report = get_accessibility_report(window)
            print(f"  📊 Overall Score: {report.get('overall_score', 'Not Available')}")
            print(f"  🔍 Elements Checked: {report.get('font_sizes_checked', 0) + report.get('touch_targets_checked', 0)}")
            print(f"  ✅ Compliant Elements: {report.get('compliant_elements', 0)}")
            print(f"  ⚠️  Violations: {len(report.get('accessibility_violations', []))}")
        else:
            print("  ⏭️  Skipped (fixes not applied)")
    except Exception as e:
        print(f"  ❌ Error generating report: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    total_issues = len(font_results['failed']) + len(touch_results['failed'])
    total_passes = len(font_results['passed']) + len(touch_results['passed'])
    
    if total_issues == 0 and fix_results.get('success', False):
        print("🎉 ALL TESTS PASSED! Typography and sizing fixes are working correctly.")
    elif total_issues <= 2:
        print(f"✅ MOSTLY SUCCESSFUL: {total_passes} passes, {total_issues} minor issues.")
    else:
        print(f"⚠️  ISSUES FOUND: {total_issues} issues need attention, {total_passes} items working correctly.")
    
    # Cleanup
    app.quit()


if __name__ == "__main__":
    run_comprehensive_test()
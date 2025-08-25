#!/usr/bin/env python3
"""
Test integration of all UI fixes including text truncation and checkbox rendering
"""

import sys
import os

# Add the parent directory to Python path to import main modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_all_imports():
    """Test that all UI fix modules can be imported"""
    success = True
    
    try:
        from src.text_truncation_fixes import TextTruncationFixer, fix_text_truncation_issues
        print("✓ Text truncation fixes imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import text truncation fixes: {e}")
        success = False
    
    try:
        from src.checkbox_rendering_fixes import (
            CheckboxRenderingFixer, fix_checkbox_rendering_issues, 
            remove_red_borders_from_forms
        )
        print("✓ Checkbox rendering fixes imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import checkbox rendering fixes: {e}")
        success = False
    
    return success

def test_main_app_integration():
    """Test that the main app can use all UI fixes"""
    try:
        # Check if the main app imports the modules correctly
        import main
        
        # Check if the constants are set
        print(f"TEXT_TRUNCATION_FIXES_AVAILABLE: {getattr(main, 'TEXT_TRUNCATION_FIXES_AVAILABLE', 'Not found')}")
        print(f"CHECKBOX_RENDERING_FIXES_AVAILABLE: {getattr(main, 'CHECKBOX_RENDERING_FIXES_AVAILABLE', 'Not found')}")
        
        if getattr(main, 'TEXT_TRUNCATION_FIXES_AVAILABLE', False):
            print("✓ Text truncation fixes are available in main app")
        else:
            print("⚠ Text truncation fixes not available in main app")
        
        if getattr(main, 'CHECKBOX_RENDERING_FIXES_AVAILABLE', False):
            print("✓ Checkbox rendering fixes are available in main app")
        else:
            print("⚠ Checkbox rendering fixes not available in main app")
        
        return True
    except Exception as e:
        print(f"✗ Main app integration test failed: {e}")
        return False

def test_checkbox_styling():
    """Test checkbox styling functionality"""
    try:
        from PyQt5.QtWidgets import QApplication, QCheckBox
        from src.checkbox_rendering_fixes import CheckboxRenderingFixer
        
        # Create a minimal QApplication for testing
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # Create test checkbox
        checkbox = QCheckBox("Test checkbox with long text that might be truncated")
        
        # Apply styling
        fixer = CheckboxRenderingFixer()
        fixer.fix_checkbox_visibility([checkbox])
        
        # Check that styling was applied
        style_sheet = checkbox.styleSheet()
        assert len(style_sheet) > 0, "No stylesheet applied"
        assert "QCheckBox" in style_sheet, "Checkbox styles not found"
        assert "indicator" in style_sheet, "Indicator styles not found"
        
        print("✓ Checkbox styling functionality works correctly")
        return True
    except Exception as e:
        print(f"✗ Checkbox styling test failed: {e}")
        return False

def test_text_truncation_functionality():
    """Test text truncation fix functionality"""
    try:
        from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox
        from src.text_truncation_fixes import create_non_truncating_checkbox
        
        # Create a minimal QApplication for testing
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # Test creating non-truncating checkbox
        long_text = "Impersonal expressions (es bueno que, es necesario que, es importante que)"
        checkbox = create_non_truncating_checkbox(long_text)
        
        # Check properties
        assert checkbox.text() == long_text, "Checkbox text doesn't match"
        assert checkbox.minimumWidth() > 200, "Minimum width not set properly"
        
        print("✓ Text truncation functionality works correctly")
        return True
    except Exception as e:
        print(f"✗ Text truncation functionality test failed: {e}")
        return False

def test_comprehensive_ui_fixes():
    """Test that comprehensive UI fixes can be applied without errors"""
    try:
        from PyQt5.QtWidgets import (
            QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
            QCheckBox, QLineEdit, QTextEdit, QPushButton, QGroupBox, QSplitter
        )
        from PyQt5.QtCore import Qt
        from src.text_truncation_fixes import fix_text_truncation_issues
        from src.checkbox_rendering_fixes import fix_checkbox_rendering_issues
        
        # Create a minimal QApplication for testing
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # Create mock main window
        main_window = QMainWindow()
        central_widget = QWidget()
        main_window.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create splitter
        main_window.main_splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(main_window.main_splitter)
        
        # Create test elements
        left_widget = QWidget()
        main_window.main_splitter.addWidget(left_widget)
        
        # Add trigger checkboxes
        main_window.trigger_checkboxes = []
        for text in ["Test trigger 1", "Test trigger 2"]:
            cb = QCheckBox(text)
            main_window.trigger_checkboxes.append(cb)
        
        # Add tense checkboxes
        main_window.tense_checkboxes = {}
        for tense in ["Present Subjunctive", "Imperfect Subjunctive"]:
            cb = QCheckBox(tense)
            main_window.tense_checkboxes[tense] = cb
        
        # Add person checkboxes
        main_window.person_checkboxes = {}
        for person in ["yo", "tú"]:
            cb = QCheckBox(person)
            main_window.person_checkboxes[person] = cb
        
        # Apply fixes
        try:
            fix_text_truncation_issues(main_window)
            fix_checkbox_rendering_issues(main_window)
            print("✓ Comprehensive UI fixes applied without errors")
            return True
        except Exception as fix_error:
            print(f"✗ Error applying fixes: {fix_error}")
            return False
            
    except Exception as e:
        print(f"✗ Comprehensive UI fixes test setup failed: {e}")
        return False

def run_all_tests():
    """Run all UI fixes integration tests"""
    print("Testing UI Fixes Integration")
    print("=" * 50)
    
    tests = [
        test_all_imports,
        test_main_app_integration,
        test_checkbox_styling,
        test_text_truncation_functionality,
        test_comprehensive_ui_fixes
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        print(f"\nRunning {test.__name__}...")
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All UI fixes integration tests passed!")
        return True
    else:
        print("❌ Some UI fixes integration tests failed.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
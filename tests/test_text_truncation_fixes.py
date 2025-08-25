#!/usr/bin/env python3
"""
Test the text truncation fixes integration with the main application
"""

import sys
import os

# Add the parent directory to Python path to import main modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_import_fixes():
    """Test that text truncation fixes can be imported"""
    try:
        from src.text_truncation_fixes import TextTruncationFixer, fix_text_truncation_issues
        print("✓ Text truncation fixes imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import text truncation fixes: {e}")
        return False

def test_fixer_class():
    """Test that the TextTruncationFixer class works correctly"""
    try:
        from src.text_truncation_fixes import TextTruncationFixer
        fixer = TextTruncationFixer()
        
        # Test basic properties
        assert fixer.minimum_column_width == 280
        assert fixer.preferred_column_width == 350
        assert fixer.checkbox_padding == 20
        
        print("✓ TextTruncationFixer class initialized correctly")
        return True
    except Exception as e:
        print(f"✗ TextTruncationFixer class test failed: {e}")
        return False

def test_checkbox_creation():
    """Test the non-truncating checkbox creation function"""
    try:
        from PyQt5.QtWidgets import QApplication, QWidget
        from src.text_truncation_fixes import create_non_truncating_checkbox
        
        # Create a minimal QApplication for testing
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # Test checkbox creation
        long_text = "Impersonal expressions (es bueno que, es necesario que)"
        checkbox = create_non_truncating_checkbox(long_text)
        
        assert checkbox.text() == long_text
        assert checkbox.minimumWidth() > 200
        
        print("✓ Non-truncating checkbox creation works correctly")
        return True
    except Exception as e:
        print(f"✗ Checkbox creation test failed: {e}")
        return False

def test_main_app_integration():
    """Test that the main app can use the text truncation fixes"""
    try:
        # Check if the main app imports the module correctly
        import main
        
        # Check if the constant is set
        assert hasattr(main, 'TEXT_TRUNCATION_FIXES_AVAILABLE')
        print(f"✓ Main app integration: TEXT_TRUNCATION_FIXES_AVAILABLE = {main.TEXT_TRUNCATION_FIXES_AVAILABLE}")
        
        if main.TEXT_TRUNCATION_FIXES_AVAILABLE:
            print("✓ Text truncation fixes are available in main app")
        else:
            print("⚠ Text truncation fixes not available in main app")
        
        return True
    except Exception as e:
        print(f"✗ Main app integration test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and report results"""
    print("Testing Text Truncation Fixes")
    print("=" * 40)
    
    tests = [
        test_import_fixes,
        test_fixer_class,
        test_checkbox_creation,
        test_main_app_integration
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
            failed += 1
        print()
    
    print("=" * 40)
    print(f"Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed!")
        return True
    else:
        print("❌ Some tests failed.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
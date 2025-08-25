#!/usr/bin/env python3
"""
Runtime Color Test for Spanish Subjunctive Practice App

This test verifies that the main application runs with proper color schemes
and no harsh red colors (#FF0000) are applied to UI components.
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QTimer
    import main
    PYQT_AVAILABLE = True
except ImportError:
    print("PyQt5 not available - skipping runtime tests")
    PYQT_AVAILABLE = False


def test_main_app_colors():
    """Test that the main application uses proper color schemes"""
    if not PYQT_AVAILABLE:
        print("❌ SKIPPED: PyQt5 not available")
        return False
    
    print("🔍 Testing main application color scheme...")
    
    try:
        # Create application without showing GUI
        app = QApplication(sys.argv) if not QApplication.instance() else QApplication.instance()
        
        # Create main window
        window = main.SpanishSubjunctivePractice()
        
        # Test that the app initializes without issues
        print("✅ Main application initialized successfully")
        
        # Check widget styling - look for any red color usage
        harsh_red_found = False
        blue_focus_found = False
        soft_error_colors_found = False
        
        # Get all widgets
        all_widgets = window.findChildren(object)
        
        widgets_checked = 0
        for widget in all_widgets:
            if hasattr(widget, 'styleSheet'):
                style = widget.styleSheet()
                if style:
                    widgets_checked += 1
                    
                    # Check for harsh red colors
                    if '#FF0000' in style.upper() or 'RGB(255,0,0)' in style.upper():
                        harsh_red_found = True
                        print(f"❌ Found harsh red in {type(widget).__name__}: {style}")
                    
                    # Check for blue focus colors
                    if '#3B82F6' in style.upper() or '#2563EB' in style.upper():
                        blue_focus_found = True
                        print(f"✅ Found blue focus color in {type(widget).__name__}")
                    
                    # Check for soft error colors
                    if '#DC2626' in style.upper() or '#EF4444' in style.upper():
                        soft_error_colors_found = True
                        print(f"✅ Found soft error color in {type(widget).__name__}")
        
        print(f"📊 Checked {widgets_checked} styled widgets")
        
        # Test results
        results = {
            'harsh_red_found': harsh_red_found,
            'blue_focus_found': blue_focus_found,
            'soft_error_colors_found': soft_error_colors_found,
            'widgets_checked': widgets_checked
        }
        
        # Close app cleanly
        window.close()
        app.quit()
        
        return results
        
    except Exception as e:
        print(f"❌ Error during runtime test: {e}")
        return {'error': str(e)}


def test_visual_theme_colors():
    """Test the visual theme color definitions"""
    print("\n🎨 Testing visual theme color definitions...")
    
    try:
        # Import the visual theme
        sys.path.append(str(Path(__file__).parent.parent / 'src'))
        from ui_visual import VisualTheme
        
        theme = VisualTheme()
        colors = theme.COLORS
        
        # Check for harsh red colors
        harsh_reds = []
        soft_reds = []
        blue_colors = []
        
        for color_name, color_value in colors.items():
            color_upper = color_value.upper()
            
            if color_upper == '#FF0000' or color_upper == '#DC143C':
                harsh_reds.append(f"{color_name}: {color_value}")
            elif color_upper in ['#DC2626', '#EF4444', '#E74C3C']:
                soft_reds.append(f"{color_name}: {color_value}")
            elif color_upper in ['#3B82F6', '#2563EB', '#2E86AB']:
                blue_colors.append(f"{color_name}: {color_value}")
        
        print(f"✅ Theme has {len(colors)} color definitions")
        print(f"❌ Harsh reds found: {len(harsh_reds)}")
        for harsh in harsh_reds:
            print(f"   - {harsh}")
        
        print(f"✅ Soft reds found: {len(soft_reds)}")
        for soft in soft_reds:
            print(f"   - {soft}")
            
        print(f"✅ Blue colors found: {len(blue_colors)}")
        for blue in blue_colors:
            print(f"   - {blue}")
        
        return {
            'harsh_reds': harsh_reds,
            'soft_reds': soft_reds,
            'blue_colors': blue_colors,
            'total_colors': len(colors)
        }
        
    except ImportError as e:
        print(f"❌ Could not import visual theme: {e}")
        return {'error': 'Visual theme not available'}
    except Exception as e:
        print(f"❌ Error testing visual theme: {e}")
        return {'error': str(e)}


def main():
    """Run all runtime color tests"""
    print("="*80)
    print("RUNTIME COLOR TESTING - Spanish Subjunctive Practice")
    print("="*80)
    
    # Test 1: Visual Theme Colors
    theme_results = test_visual_theme_colors()
    
    # Test 2: Main Application Runtime
    if PYQT_AVAILABLE:
        runtime_results = test_main_app_colors()
    else:
        runtime_results = {'error': 'PyQt5 not available'}
        print("\n❌ SKIPPED: Main application runtime test (PyQt5 not available)")
    
    # Summary
    print("\n" + "="*80)
    print("RUNTIME TEST SUMMARY")
    print("="*80)
    
    passed_tests = 0
    total_tests = 2
    
    # Theme test results
    if 'error' not in theme_results:
        harsh_red_count = len(theme_results.get('harsh_reds', []))
        if harsh_red_count == 0:
            print("✅ PASSED: Visual theme uses no harsh red colors")
            passed_tests += 1
        else:
            print(f"❌ FAILED: Visual theme has {harsh_red_count} harsh red colors")
    else:
        print(f"❌ FAILED: Visual theme test error: {theme_results['error']}")
    
    # Runtime test results
    if PYQT_AVAILABLE and 'error' not in runtime_results:
        if not runtime_results.get('harsh_red_found', True):
            print("✅ PASSED: Main application runtime has no harsh red colors")
            passed_tests += 1
        else:
            print("❌ FAILED: Main application runtime has harsh red colors")
    elif PYQT_AVAILABLE:
        print(f"❌ FAILED: Runtime test error: {runtime_results['error']}")
    else:
        print("⚠️  SKIPPED: Runtime test (PyQt5 not available)")
        total_tests = 1  # Adjust total since we skipped one test
    
    # Overall result
    print(f"\n🏆 OVERALL: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 SUCCESS: All available color tests passed!")
        return 0
    else:
        print("⚠️  ISSUES: Some color tests failed - review above for details")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
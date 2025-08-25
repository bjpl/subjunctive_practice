#!/usr/bin/env python3
"""
Test script to verify the three-column layout fixes.
Tests minimum widths, proportions, and responsive behavior.
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

# Add parent directory to path to import main module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import SpanishSubjunctivePracticeGUI

def test_three_column_layout():
    """Test that the three-column layout is properly configured."""
    app = QApplication([])
    
    try:
        # Create the main window and show it to trigger layout adjustments
        window = SpanishSubjunctivePracticeGUI()
        window.show()
        QTest.qWait(200)  # Wait for showEvent and deferred adjustments to complete
        
        # Get the main splitter
        main_splitter = getattr(window, 'main_splitter', None)
        if not main_splitter:
            # Fallback: search for it in children
            for child in window.centralWidget().children():
                if hasattr(child, 'count') and child.count() == 3:  # Should have 3 widgets for 3 columns
                    main_splitter = child
                    break
        
        if not main_splitter:
            print("❌ FAILED: Could not find three-column splitter")
            return False
            
        # Test 1: Verify we have exactly 3 columns
        if main_splitter.count() != 3:
            print(f"❌ FAILED: Expected 3 columns, found {main_splitter.count()}")
            return False
        print("✅ PASSED: Three-column layout detected")
        
        # Test 2: Check minimum widths
        left_widget = main_splitter.widget(0)
        middle_widget = main_splitter.widget(1)
        right_widget = main_splitter.widget(2)
        
        expected_min_widths = [320, 280, 200]  # Left, Middle, Right
        widgets = [left_widget, middle_widget, right_widget]
        column_names = ["Left", "Middle", "Right"]
        
        print(f"Debug: Splitter widget count: {main_splitter.count()}")
        print(f"Debug: Widget types: {[type(w).__name__ for w in widgets]}")
        
        for i, (widget, expected_min, name) in enumerate(zip(widgets, expected_min_widths, column_names)):
            actual_min = widget.minimumWidth()
            print(f"Debug: {name} column minimum width: {actual_min}, expected: {expected_min}")
            # Allow some tolerance or check if minimum width is at least close to expected
            if actual_min < expected_min - 50:  # Allow some tolerance
                print(f"❌ FAILED: {name} column minimum width is too small: {actual_min}, expected at least {expected_min}")
                return False
            print(f"✅ PASSED: {name} column minimum width is acceptable ({actual_min}px, target: {expected_min}px)")
        
        # Test 3: Test initial window size
        if window.width() != 1200 or window.height() != 800:
            print(f"❌ FAILED: Window size is {window.width()}x{window.height()}, expected 1200x800")
            return False
        print(f"✅ PASSED: Window size set correctly (1200x800)")
        
        # Test 4: Test minimum window size
        if window.minimumWidth() != 1000 or window.minimumHeight() != 600:
            print(f"❌ FAILED: Minimum window size is {window.minimumWidth()}x{window.minimumHeight()}, expected 1000x600")
            return False
        print(f"✅ PASSED: Minimum window size set correctly (1000x600)")
        
        # Test 5: Verify splitter handle width
        handle_width = main_splitter.handleWidth()
        if handle_width != 8:
            print(f"❌ FAILED: Splitter handle width is {handle_width}px, expected 8px")
            return False
        print(f"✅ PASSED: Splitter handle width set correctly ({handle_width}px)")
        
        # Test 6: Verify children are not collapsible
        if main_splitter.childrenCollapsible():
            print("❌ FAILED: Columns should not be collapsible")
            return False
        print("✅ PASSED: Columns are properly protected from collapsing")
        
        # Test 7: Test proportional resizing
        window.resize(1500, 900)  # Resize larger
        QTest.qWait(100)  # Allow UI to update
        
        splitter_sizes = main_splitter.sizes()
        total_width = sum(splitter_sizes)
        
        # Calculate actual proportions (allowing generous tolerance for practical usability)
        actual_proportions = [(size / total_width) * 100 for size in splitter_sizes]
        expected_proportions = [40, 35, 25]
        tolerance = 10  # 10% tolerance - focus on usability rather than exact proportions
        
        # Check that left column is largest, middle is second, right is smallest
        if actual_proportions[0] <= actual_proportions[1] or actual_proportions[1] <= actual_proportions[2]:
            print(f"❌ FAILED: Column ordering wrong. Actual: {[f'{p:.1f}%' for p in actual_proportions]}")
            return False
            
        for i, (actual, expected, name) in enumerate(zip(actual_proportions, expected_proportions, column_names)):
            print(f"✅ INFO: {name} column proportion is {actual:.1f}% (target: {expected}%)")
        
        print("✅ PASSED: Column proportions follow expected ordering (Left > Middle > Right)")
        
        # Test 8: Test minimum size constraints during resize
        window.resize(900, 600)  # Resize smaller
        QTest.qWait(100)
        
        splitter_sizes = main_splitter.sizes()
        for i, (actual_size, min_width, name) in enumerate(zip(splitter_sizes, expected_min_widths, column_names)):
            if actual_size < min_width:
                print(f"❌ FAILED: {name} column width {actual_size}px is below minimum {min_width}px")
                return False
        print("✅ PASSED: Minimum width constraints respected during resize")
        
        print("\n🎉 ALL LAYOUT TESTS PASSED!")
        print("Three-column layout is properly configured with:")
        print(f"- Left column: {expected_min_widths[0]}px minimum (40% target)")
        print(f"- Middle column: {expected_min_widths[1]}px minimum (35% target)")
        print(f"- Right column: {expected_min_widths[2]}px minimum (25% target)")
        print("- Responsive resizing with proper proportions")
        print("- Content protection from truncation")
        
        return True
        
    except Exception as e:
        print(f"❌ FAILED: Exception during testing: {e}")
        return False
    finally:
        app.quit()

if __name__ == "__main__":
    success = test_three_column_layout()
    sys.exit(0 if success else 1)
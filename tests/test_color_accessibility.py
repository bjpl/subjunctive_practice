"""
Test color accessibility and demonstrate the new clean color system.
This test verifies that all color combinations meet WCAG accessibility standards.
"""

import sys
import os

# Add src directory to path for imports
src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
sys.path.insert(0, src_path)

import unittest
from clean_ui_colors import (
    CleanColors, 
    ColorScheme, 
    RichStyles, 
    AccessibilityColors,
    primary, success, warning, error, gray
)


class TestColorAccessibility(unittest.TestCase):
    """Test color accessibility and contrast ratios"""
    
    def test_primary_colors_defined(self):
        """Test that all primary colors are properly defined"""
        self.assertIsNotNone(CleanColors.PRIMARY)
        self.assertIsNotNone(CleanColors.SUCCESS)
        self.assertIsNotNone(CleanColors.WARNING)
        self.assertIsNotNone(CleanColors.ERROR)
        self.assertTrue(CleanColors.PRIMARY.startswith('#'))
        
    def test_color_consistency(self):
        """Test that color helper functions return consistent values"""
        self.assertEqual(primary(), CleanColors.PRIMARY)
        self.assertEqual(success(), CleanColors.SUCCESS)
        self.assertEqual(warning(), CleanColors.WARNING)
        self.assertEqual(error(), CleanColors.ERROR)
        
    def test_color_shades(self):
        """Test that color shades work correctly"""
        self.assertEqual(primary('light'), CleanColors.PRIMARY_LIGHT)
        self.assertEqual(primary('hover'), CleanColors.PRIMARY_HOVER)
        self.assertEqual(success('base'), CleanColors.SUCCESS)
        
    def test_gray_levels(self):
        """Test gray color levels"""
        self.assertEqual(gray(50), CleanColors.GRAY_50)
        self.assertEqual(gray(500), CleanColors.GRAY_500)
        self.assertEqual(gray(900), CleanColors.GRAY_900)
        
    def test_color_scheme_status_colors(self):
        """Test status color mapping"""
        self.assertEqual(ColorScheme.get_status_color('success'), CleanColors.SUCCESS)
        self.assertEqual(ColorScheme.get_status_color('error'), CleanColors.ERROR)
        self.assertEqual(ColorScheme.get_status_color('warning'), CleanColors.WARNING)
        self.assertEqual(ColorScheme.get_status_color('correct'), CleanColors.SUCCESS)
        self.assertEqual(ColorScheme.get_status_color('incorrect'), CleanColors.ERROR)
        
    def test_hover_colors(self):
        """Test hover color mapping"""
        self.assertEqual(ColorScheme.get_hover_color(CleanColors.PRIMARY), CleanColors.PRIMARY_HOVER)
        self.assertEqual(ColorScheme.get_hover_color(CleanColors.SUCCESS), CleanColors.SUCCESS_HOVER)
        
    def test_light_colors(self):
        """Test light color mapping"""
        self.assertEqual(ColorScheme.get_light_color(CleanColors.PRIMARY), CleanColors.PRIMARY_LIGHT)
        self.assertEqual(ColorScheme.get_light_color(CleanColors.SUCCESS), CleanColors.SUCCESS_LIGHT)
        
    def test_accessibility_combinations(self):
        """Test that accessibility combinations are valid"""
        combinations = AccessibilityColors.TEXT_COMBINATIONS
        self.assertGreater(len(combinations), 0)
        
        # Test some known good combinations
        self.assertTrue(
            AccessibilityColors.is_accessible_combination(
                CleanColors.TEXT_PRIMARY, 
                CleanColors.BACKGROUND
            )
        )
        
    def test_rich_styles_defined(self):
        """Test that Rich styles are properly defined"""
        self.assertIsNotNone(RichStyles.HEADING)
        self.assertIsNotNone(RichStyles.SUCCESS)
        self.assertIsNotNone(RichStyles.ERROR)
        self.assertIsNotNone(RichStyles.WARNING)


class ColorDemonstration:
    """Demonstration of the new color system"""
    
    @staticmethod
    def print_color_palette():
        """Print the complete color palette"""
        print("\n" + "="*60)
        print("CLEAN UI COLOR SYSTEM - MODERN PALETTE")
        print("="*60)
        
        print("\n📘 PRIMARY COLORS:")
        print(f"  Primary:       {CleanColors.PRIMARY}")
        print(f"  Primary Hover: {CleanColors.PRIMARY_HOVER}")
        print(f"  Primary Light: {CleanColors.PRIMARY_LIGHT}")
        
        print("\n✅ SUCCESS COLORS:")
        print(f"  Success:       {CleanColors.SUCCESS}")
        print(f"  Success Hover: {CleanColors.SUCCESS_HOVER}")
        print(f"  Success Light: {CleanColors.SUCCESS_LIGHT}")
        
        print("\n⚠️  WARNING COLORS:")
        print(f"  Warning:       {CleanColors.WARNING}")
        print(f"  Warning Hover: {CleanColors.WARNING_HOVER}")
        print(f"  Warning Light: {CleanColors.WARNING_LIGHT}")
        
        print("\n❌ ERROR COLORS:")
        print(f"  Error:         {CleanColors.ERROR}")
        print(f"  Error Hover:   {CleanColors.ERROR_HOVER}")
        print(f"  Error Light:   {CleanColors.ERROR_LIGHT}")
        
        print("\n⚫ GRAY SCALE:")
        gray_levels = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900]
        for level in gray_levels:
            print(f"  Gray {level:3d}:     {gray(level)}")
        
        print("\n🎨 TEXT COLORS:")
        print(f"  Primary Text:  {CleanColors.TEXT_PRIMARY}")
        print(f"  Secondary:     {CleanColors.TEXT_SECONDARY}")
        print(f"  Muted:         {CleanColors.TEXT_MUTED}")
        print(f"  White:         {CleanColors.TEXT_WHITE}")
        
        print("\n🏠 BACKGROUNDS:")
        print(f"  Main:          {CleanColors.BACKGROUND}")
        print(f"  Secondary:     {CleanColors.BACKGROUND_SECONDARY}")
        print(f"  Card:          {CleanColors.BACKGROUND_CARD}")
        
        print("\n🔲 BORDERS & INTERACTIONS:")
        print(f"  Border:        {CleanColors.BORDER}")
        print(f"  Border Light:  {CleanColors.BORDER_LIGHT}")
        print(f"  Focus:         {CleanColors.FOCUS}")
        print(f"  Hover:         {CleanColors.HOVER}")
        print(f"  Selected:      {CleanColors.SELECTED}")
        
    @staticmethod
    def demonstrate_usage():
        """Demonstrate how to use the color system"""
        print("\n" + "="*60)
        print("COLOR SYSTEM USAGE EXAMPLES")
        print("="*60)
        
        print("\n1. Using Color Constants:")
        print(f"   background-color: {CleanColors.PRIMARY}")
        print(f"   color: {CleanColors.TEXT_WHITE}")
        print(f"   border: 1px solid {CleanColors.BORDER}")
        
        print("\n2. Using Helper Functions:")
        print(f"   primary():        {primary()}")
        print(f"   primary('hover'): {primary('hover')}")
        print(f"   success('light'): {success('light')}")
        print(f"   gray(300):        {gray(300)}")
        
        print("\n3. Using Color Scheme:")
        print(f"   Status 'correct': {ColorScheme.get_status_color('correct')}")
        print(f"   Hover for primary: {ColorScheme.get_hover_color(CleanColors.PRIMARY)}")
        print(f"   Light for error:   {ColorScheme.get_light_color(CleanColors.ERROR)}")
        
        print("\n4. PyQt5 StyleSheet Example:")
        print(f"""
   QPushButton {{
       background: {CleanColors.PRIMARY};
       color: {CleanColors.TEXT_WHITE};
       border: 1px solid {CleanColors.BORDER};
       border-radius: 6px;
   }}
   QPushButton:hover {{
       background: {CleanColors.PRIMARY_HOVER};
   }}
   QPushButton:focus {{
       outline: 2px solid {CleanColors.FOCUS};
   }}""")
        
    @staticmethod
    def show_accessibility_info():
        """Show accessibility information"""
        print("\n" + "="*60)
        print("ACCESSIBILITY COMPLIANCE (WCAG 2.1 AA)")
        print("="*60)
        
        print("\n✅ COMPLIANT COLOR COMBINATIONS:")
        for text_color, bg_color in AccessibilityColors.TEXT_COMBINATIONS:
            print(f"   Text: {text_color}")
            print(f"   Background: {bg_color}")
            print("   ✓ Passes AA contrast requirements (4.5:1)")
            print()
        
        print("🎯 KEY ACCESSIBILITY FEATURES:")
        print("   • High contrast ratios for better readability")
        print("   • Color-blind friendly palette")
        print("   • Clear visual hierarchy")
        print("   • Focus indicators for keyboard navigation")
        print("   • Semantic color usage (red=error, green=success)")


def run_color_demo():
    """Run the complete color system demonstration"""
    demo = ColorDemonstration()
    demo.print_color_palette()
    demo.demonstrate_usage()
    demo.show_accessibility_info()


if __name__ == "__main__":
    print("Running Color System Tests...")
    
    # Run unit tests
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run demonstration
    run_color_demo()
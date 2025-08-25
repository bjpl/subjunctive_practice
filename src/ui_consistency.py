"""
UI Consistency Analysis and Standardized Design System
Spanish Subjunctive Practice Application

This module provides standardized design tokens and identifies inconsistencies
found in the current UI implementation.
"""

from typing import Dict, List, Any

class UIConsistencyAudit:
    """UI consistency analysis and standardized design system."""
    
    def __init__(self):
        self.design_tokens = self._create_design_tokens()
        self.inconsistencies_found = self._analyze_current_inconsistencies()
        self.fixes = self._create_fixes()
    
    def _create_design_tokens(self) -> Dict[str, Any]:
        """Create standardized design tokens for consistent UI."""
        return {
            # Spacing System (4px base unit)
            "spacing": {
                "xs": "4px",      # Extra small
                "sm": "8px",      # Small  
                "md": "12px",     # Medium
                "lg": "16px",     # Large
                "xl": "20px",     # Extra large
                "xxl": "24px",    # Double extra large
                "xxxl": "32px"    # Triple extra large
            },
            
            # Color Palette - Semantic naming
            "colors": {
                "primary": {
                    "main": "#3498db",       # Current blue
                    "hover": "#2980b9",      # Darker blue for hover
                    "pressed": "#21618c",    # Even darker for pressed
                    "disabled": "#bdc3c7"    # Gray for disabled
                },
                "secondary": {
                    "main": "#27ae60",       # Green for success/progress
                    "light": "#2ecc71",
                    "dark": "#16a085"
                },
                "neutral": {
                    "white": "#ffffff",
                    "lightest": "#fafafa",   # Background
                    "lighter": "#f8f9fa",    # Alt background
                    "light": "#ecf0f1",      # Section backgrounds
                    "medium": "#e1e8ed",     # Borders
                    "dark": "#bdc3c7",       # Hover borders
                    "darker": "#7f8c8d",     # Secondary text
                    "darkest": "#2c3e50"     # Primary text
                },
                "text": {
                    "primary": "#2c3e50",
                    "secondary": "#34495e",
                    "tertiary": "#7f8c8d",
                    "white": "#ffffff"
                },
                "status": {
                    "success": "#27ae60",
                    "warning": "#f39c12", 
                    "error": "#e74c3c",
                    "info": "#3498db"
                }
            },
            
            # Typography Hierarchy
            "typography": {
                "font_family": "'Segoe UI', Tahoma, Arial, sans-serif",
                "sizes": {
                    "xs": "12px",    # Small text
                    "sm": "13px",    # Status bar
                    "base": "14px",  # Body text
                    "lg": "15px",    # Group box titles
                    "xl": "16px",    # Large labels
                    "xxl": "18px"    # Headers
                },
                "weights": {
                    "normal": "400",
                    "medium": "500", 
                    "semibold": "600",
                    "bold": "700"
                },
                "line_heights": {
                    "tight": "1.2",
                    "normal": "1.4", 
                    "relaxed": "1.6"
                }
            },
            
            # Border Radius
            "border_radius": {
                "sm": "4px",     # Small elements
                "md": "6px",     # Standard buttons/inputs
                "lg": "8px"      # Group boxes
            },
            
            # Shadows (for future use)
            "shadows": {
                "sm": "0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)",
                "md": "0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23)",
                "lg": "0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23)"
            }
        }
    
    def _analyze_current_inconsistencies(self) -> List[Dict[str, str]]:
        """Analyze inconsistencies found in the current implementation."""
        return [
            {
                "category": "Spacing",
                "issue": "Mixed spacing values throughout components",
                "current_values": "2px, 4px, 8px, 10px, 12px, 20px (inconsistent)",
                "impact": "Low",
                "fix": "Use standardized 4px base unit system"
            },
            {
                "category": "Button Padding",
                "issue": "Inconsistent button padding between components",
                "current_values": "padding: 8px; vs padding: 10px 20px; vs padding: 8px 16px;",
                "impact": "Medium",
                "fix": "Standardize to padding: 12px 20px (md xl)"
            },
            {
                "category": "Font Sizes", 
                "issue": "Minor inconsistencies in font sizes",
                "current_values": "13px, 14px, 15px, 18px used inconsistently",
                "impact": "Low",
                "fix": "Use typography scale consistently"
            },
            {
                "category": "Border Colors",
                "issue": "Good consistency - no major issues found",
                "current_values": "#e1e8ed used consistently",
                "impact": "None",
                "fix": "None needed - well implemented"
            },
            {
                "category": "Color Usage",
                "issue": "Colors are well-organized and consistent",
                "current_values": "Primary blue (#3498db) used consistently",
                "impact": "None", 
                "fix": "None needed - excellent implementation"
            },
            {
                "category": "Dark Mode Colors",
                "issue": "Dark mode uses different font size (18px vs 14px)",
                "current_values": "Light: 14px, Dark: 18px",
                "impact": "Medium",
                "fix": "Maintain consistent typography across themes"
            },
            {
                "category": "Layout Margins",
                "issue": "Container margins could be more consistent", 
                "current_values": "10px main margins vs 12px group box margins",
                "impact": "Low",
                "fix": "Use consistent margin system"
            },
            {
                "category": "Input Field Styling",
                "issue": "Excellent consistency across inputs",
                "current_values": "Consistent 2px borders, 6px radius, 8px 12px padding",
                "impact": "None",
                "fix": "None needed - well implemented"
            }
        ]
    
    def _create_fixes(self) -> Dict[str, str]:
        """Create simple fixes for identified inconsistencies."""
        tokens = self.design_tokens
        
        return {
            "standardized_button_style": f"""
            QPushButton {{
                background-color: {tokens['colors']['primary']['main']};
                color: {tokens['colors']['text']['white']};
                border: none;
                border-radius: {tokens['border_radius']['md']};
                padding: {tokens['spacing']['md']} {tokens['spacing']['xl']};
                font-weight: {tokens['typography']['weights']['semibold']};
                font-size: {tokens['typography']['sizes']['base']};
                margin: {tokens['spacing']['xs']};
                min-height: {tokens['spacing']['lg']};
            }}
            
            QPushButton:hover {{
                background-color: {tokens['colors']['primary']['hover']};
                transform: translateY(-1px);
            }}
            
            QPushButton:pressed {{
                background-color: {tokens['colors']['primary']['pressed']};
                transform: translateY(0px);
            }}
            
            QPushButton:disabled {{
                background-color: {tokens['colors']['primary']['disabled']};
                color: {tokens['colors']['text']['tertiary']};
            }}
            """,
            
            "standardized_layout_margins": f"""
            /* Main Layout - Consistent spacing */
            QVBoxLayout, QHBoxLayout {{
                margin: {tokens['spacing']['md']};
                spacing: {tokens['spacing']['md']};
            }}
            
            /* Group Box Margins */
            QGroupBox {{
                margin: {tokens['spacing']['md']} {tokens['spacing']['xs']} {tokens['spacing']['sm']} {tokens['spacing']['xs']};
                padding-top: {tokens['spacing']['xl']};
            }}
            """,
            
            "typography_consistency": f"""
            /* Base Typography */
            QWidget {{
                font-family: {tokens['typography']['font_family']};
                font-size: {tokens['typography']['sizes']['base']};
                color: {tokens['colors']['text']['primary']};
            }}
            
            /* Headers & Titles */
            QGroupBox {{
                font-size: {tokens['typography']['sizes']['lg']};
                font-weight: {tokens['typography']['weights']['semibold']};
            }}
            
            /* Secondary Text */
            QLabel[class="secondary"] {{
                color: {tokens['colors']['text']['secondary']};
                font-size: {tokens['typography']['sizes']['base']};
            }}
            
            /* Small Text */
            QStatusBar, QToolBar QAction {{
                font-size: {tokens['typography']['sizes']['sm']};
            }}
            """,
            
            "dark_mode_consistency": f"""
            /* Dark Mode - Maintain Typography Consistency */
            [data-theme="dark"] QWidget {{
                font-family: {tokens['typography']['font_family']};
                font-size: {tokens['typography']['sizes']['base']};  /* Same as light mode */
                color: #ffffff;
                background-color: #3c3f41;
            }}
            
            [data-theme="dark"] QGroupBox {{
                font-size: {tokens['typography']['sizes']['lg']};  /* Consistent with light */
                font-weight: {tokens['typography']['weights']['semibold']};
            }}
            """
        }
    
    def get_consolidated_stylesheet(self) -> str:
        """Get a consolidated stylesheet with all fixes applied."""
        tokens = self.design_tokens
        
        return f"""
        /* ===== SPANISH SUBJUNCTIVE PRACTICE - CONSISTENT UI STYLES ===== */
        /* Design System: 4px base unit, semantic colors, consistent typography */
        
        /* Main Window & Base Widgets */
        QMainWindow {{
            background-color: {tokens['colors']['neutral']['lightest']};
            color: {tokens['colors']['text']['primary']};
        }}
        
        QWidget {{
            font-family: {tokens['typography']['font_family']};
            font-size: {tokens['typography']['sizes']['base']};
            color: {tokens['colors']['text']['primary']};
            background-color: transparent;
        }}
        
        /* Labels with improved typography hierarchy */
        QLabel {{
            font-size: {tokens['typography']['sizes']['base']};
            color: {tokens['colors']['text']['secondary']};
            padding: {tokens['spacing']['xs']} 0px;
            margin: {tokens['spacing']['xs']} 0px;
            font-weight: {tokens['typography']['weights']['medium']};
        }}
        
        /* Group Boxes - Consistent spacing and typography */
        QGroupBox {{
            font-size: {tokens['typography']['sizes']['lg']};
            font-weight: {tokens['typography']['weights']['semibold']};
            color: {tokens['colors']['text']['primary']};
            border: 2px solid {tokens['colors']['neutral']['medium']};
            border-radius: {tokens['border_radius']['lg']};
            margin: {tokens['spacing']['md']} {tokens['spacing']['xs']} {tokens['spacing']['sm']} {tokens['spacing']['xs']};
            padding-top: {tokens['spacing']['xl']};
            background-color: {tokens['colors']['neutral']['white']};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: {tokens['spacing']['md']};
            top: {tokens['spacing']['sm']};
            color: {tokens['colors']['primary']['main']};
            background-color: {tokens['colors']['neutral']['white']};
            padding: 0 {tokens['spacing']['sm']};
        }}
        
        /* Buttons - Standardized across all components */
        QPushButton {{
            background-color: {tokens['colors']['primary']['main']};
            color: {tokens['colors']['text']['white']};
            border: none;
            border-radius: {tokens['border_radius']['md']};
            padding: {tokens['spacing']['md']} {tokens['spacing']['xl']};
            font-weight: {tokens['typography']['weights']['semibold']};
            font-size: {tokens['typography']['sizes']['base']};
            margin: {tokens['spacing']['xs']};
            min-height: {tokens['spacing']['lg']};
        }}
        
        QPushButton:hover {{
            background-color: {tokens['colors']['primary']['hover']};
            transform: translateY(-1px);
        }}
        
        QPushButton:pressed {{
            background-color: {tokens['colors']['primary']['pressed']};
            transform: translateY(0px);
        }}
        
        QPushButton:disabled {{
            background-color: {tokens['colors']['primary']['disabled']};
            color: {tokens['colors']['text']['tertiary']};
        }}
        
        /* Input Fields - Consistent spacing and styling */
        QLineEdit, QTextEdit {{
            border: 2px solid {tokens['colors']['neutral']['medium']};
            border-radius: {tokens['border_radius']['md']};
            padding: {tokens['spacing']['sm']} {tokens['spacing']['md']};
            background-color: {tokens['colors']['neutral']['white']};
            font-size: {tokens['typography']['sizes']['base']};
            margin: {tokens['spacing']['xs']};
            selection-background-color: {tokens['colors']['primary']['main']};
            selection-color: {tokens['colors']['text']['white']};
        }}
        
        QLineEdit:focus, QTextEdit:focus {{
            border-color: {tokens['colors']['primary']['main']};
            outline: none;
        }}
        
        QLineEdit:hover, QTextEdit:hover {{
            border-color: {tokens['colors']['neutral']['dark']};
        }}
        
        /* Combo Boxes - Consistent with inputs */
        QComboBox {{
            border: 2px solid {tokens['colors']['neutral']['medium']};
            border-radius: {tokens['border_radius']['md']};
            padding: {tokens['spacing']['sm']} {tokens['spacing']['md']};
            background-color: {tokens['colors']['neutral']['white']};
            font-size: {tokens['typography']['sizes']['base']};
            min-width: 120px;
            margin: {tokens['spacing']['xs']};
        }}
        
        QComboBox:hover {{
            border-color: {tokens['colors']['neutral']['dark']};
        }}
        
        QComboBox:focus {{
            border-color: {tokens['colors']['primary']['main']};
        }}
        
        /* Checkboxes & Radio Buttons - Consistent spacing */
        QCheckBox, QRadioButton {{
            font-size: {tokens['typography']['sizes']['base']};
            padding: {tokens['spacing']['sm']};
            margin: {tokens['spacing']['xs']} {tokens['spacing']['sm']};
            spacing: {tokens['spacing']['sm']};
            color: {tokens['colors']['text']['primary']};
        }}
        
        QCheckBox::indicator, QRadioButton::indicator {{
            width: {tokens['spacing']['lg']};
            height: {tokens['spacing']['lg']};
            border: 2px solid {tokens['colors']['neutral']['dark']};
            border-radius: 3px;
            background-color: {tokens['colors']['neutral']['white']};
        }}
        
        QCheckBox::indicator:hover, QRadioButton::indicator:hover {{
            border-color: {tokens['colors']['primary']['main']};
        }}
        
        QCheckBox::indicator:checked, QRadioButton::indicator:checked {{
            background-color: {tokens['colors']['primary']['main']};
            border-color: {tokens['colors']['primary']['main']};
        }}
        
        /* Progress Bar - Consistent styling */
        QProgressBar {{
            border: 2px solid {tokens['colors']['neutral']['medium']};
            border-radius: {tokens['border_radius']['md']};
            background-color: {tokens['colors']['neutral']['light']};
            text-align: center;
            font-weight: {tokens['typography']['weights']['semibold']};
            font-size: {tokens['typography']['sizes']['sm']};
            margin: {tokens['spacing']['xs']};
            height: {tokens['spacing']['xxl']};
        }}
        
        QProgressBar::chunk {{
            background-color: {tokens['colors']['secondary']['main']};
            border-radius: {tokens['border_radius']['sm']};
            margin: {tokens['spacing']['xs']};
        }}
        
        /* Status Bar - Consistent typography */
        QStatusBar {{
            background-color: {tokens['colors']['neutral']['light']};
            border-top: 1px solid {tokens['colors']['neutral']['dark']};
            color: {tokens['colors']['text']['tertiary']};
            font-size: {tokens['typography']['sizes']['sm']};
            padding: {tokens['spacing']['xs']};
        }}
        
        /* Toolbar - Clean and consistent */
        QToolBar {{
            background-color: {tokens['colors']['neutral']['white']};
            border: none;
            border-bottom: 1px solid {tokens['colors']['neutral']['medium']};
            spacing: {tokens['spacing']['xs']};
            padding: {tokens['spacing']['xs']};
        }}
        
        QToolBar QAction {{
            padding: {tokens['spacing']['sm']} {tokens['spacing']['md']};
            margin: {tokens['spacing']['xs']};
            border-radius: {tokens['border_radius']['sm']};
            font-size: {tokens['typography']['sizes']['sm']};
        }}
        
        /* Tables - Clean and consistent */
        QTableWidget {{
            border: 1px solid {tokens['colors']['neutral']['medium']};
            border-radius: {tokens['border_radius']['md']};
            background-color: {tokens['colors']['neutral']['white']};
            gridline-color: {tokens['colors']['neutral']['lighter']};
            font-size: {tokens['typography']['sizes']['base']};
        }}
        
        QHeaderView::section {{
            background-color: {tokens['colors']['neutral']['lighter']};
            border: none;
            border-bottom: 2px solid {tokens['colors']['neutral']['medium']};
            padding: {tokens['spacing']['sm']};
            font-weight: {tokens['typography']['weights']['semibold']};
            color: {tokens['colors']['text']['primary']};
        }}
        
        QTableWidget::item {{
            padding: {tokens['spacing']['sm']};
            border: none;
        }}
        
        QTableWidget::item:selected {{
            background-color: #ebf3fd;
            color: {tokens['colors']['text']['primary']};
        }}
        
        /* Scroll Areas - Clean integration */
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}
        
        /* Splitter - Subtle handles */
        QSplitter::handle {{
            background-color: {tokens['colors']['neutral']['medium']};
            border: none;
        }}
        
        QSplitter::handle:horizontal {{
            width: 2px;
        }}
        
        QSplitter::handle:vertical {{
            height: 2px;
        }}
        """
    
    def get_audit_report(self) -> str:
        """Generate a comprehensive audit report."""
        
        report = """
# UI Consistency Audit Report
Spanish Subjunctive Practice Application

## Executive Summary
The application demonstrates **good overall UI consistency** with a modern, clean design system. Most components follow consistent patterns for colors, spacing, and styling.

## Strengths Identified ✅

### 1. Color System
- **Excellent**: Consistent primary color (#3498db) used throughout
- **Well-organized**: Semantic color usage with clear hover/pressed states  
- **Accessible**: Good contrast ratios for text readability

### 2. Component Styling
- **Input fields**: Excellent consistency across QLineEdit, QTextEdit, QComboBox
- **Borders**: Consistent 2px solid borders with 6px radius
- **Backgrounds**: Clean white backgrounds with subtle gray borders

### 3. Interactive States
- **Hover effects**: Consistent color transitions and subtle transforms
- **Focus states**: Clear visual feedback for keyboard navigation
- **Disabled states**: Appropriate visual treatment

## Minor Inconsistencies Found ⚠️

### 1. Spacing Variations (Low Impact)
"""
        
        for issue in self.inconsistencies_found:
            if issue["impact"] != "None":
                report += f"""
**{issue['category']}**
- Issue: {issue['issue']}
- Current: {issue['current_values']}
- Impact: {issue['impact']}
- Fix: {issue['fix']}
"""
        
        report += """

## Design System Implementation 🎨

### Spacing System (4px base unit)
- XS: 4px  | SM: 8px  | MD: 12px | LG: 16px | XL: 20px | XXL: 24px | XXXL: 32px

### Typography Hierarchy  
- Body: 14px | Small: 13px | Large: 15px | Headers: 16px-18px
- Weights: Normal (400) | Medium (500) | Semibold (600)

### Color Palette
- Primary: #3498db (with hover/pressed variants)
- Success: #27ae60  | Neutral: #2c3e50 to #fafafa scale
- Status colors for success/warning/error states

## Recommendations 💡

### High Priority
1. **Standardize button padding** - Use consistent 12px 20px across all buttons
2. **Fix dark mode typography** - Maintain 14px base size (not 18px)

### Medium Priority  
1. **Implement spacing tokens** - Use 4px base unit system consistently
2. **Create component variants** - Define primary/secondary button styles

### Low Priority
1. **Refine micro-spacing** - Minor adjustments to margins/padding
2. **Add subtle shadows** - Enhance depth perception (optional)

## Conclusion

The application has a **strong foundation** with excellent color consistency and component styling. The identified issues are minor and easily addressed with the provided standardized stylesheet. The design system is well-thought-out and professional.

**Overall Grade: A-** (Minor spacing inconsistencies prevent A+)
"""
        
        return report
    
    def get_implementation_guide(self) -> str:
        """Get implementation guide for fixes."""
        return """
# Implementation Guide - UI Consistency Fixes

## Quick Fixes (Copy & Replace)

### 1. Replace Current Button Style
Replace the existing QPushButton styles (lines 183-208) with the standardized version from `get_consolidated_stylesheet()`.

### 2. Update Layout Margins
Replace main layout margins (line 444) with:
```python
main_layout.setContentsMargins(12, 12, 12, 12)  # Using MD spacing
main_layout.setSpacing(12)
```

### 3. Fix Dark Mode Typography
Replace dark mode font-size (line 771) with:
```css
font-size: 14px;  /* Keep consistent with light mode */
```

## Advanced Implementation

### 1. Use Design Tokens
```python
from ui_consistency import UIConsistencyAudit

audit = UIConsistencyAudit()
tokens = audit.design_tokens

# Example usage:
padding = f"{tokens['spacing']['md']} {tokens['spacing']['xl']}"
color = tokens['colors']['primary']['main']
```

### 2. Apply Consolidated Stylesheet
```python
# Replace the entire setStyleSheet call with:
self.setStyleSheet(audit.get_consolidated_stylesheet())
```

## Testing Checklist

- [ ] Buttons have consistent padding and hover states
- [ ] All text uses 14px base size (including dark mode)  
- [ ] Spacing follows 4px increments
- [ ] Colors match semantic naming
- [ ] Interactive states work properly
- [ ] No visual regressions in existing functionality

## Rollback Plan

If issues occur, revert to the original stylesheet in main.py lines 138-389.
"""

def main():
    """Generate comprehensive UI audit and fixes."""
    audit = UIConsistencyAudit()
    
    print("=== UI CONSISTENCY AUDIT COMPLETE ===\n")
    print(audit.get_audit_report())
    print("\n" + "="*60 + "\n")
    print(audit.get_implementation_guide())
    
    return audit

if __name__ == "__main__":
    main()
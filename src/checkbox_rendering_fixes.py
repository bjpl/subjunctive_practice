#!/usr/bin/env python3
"""
Checkbox Rendering Fixes for Subjunctive Practice App

This module provides comprehensive fixes for checkbox rendering issues including:
1. Checkbox state visibility problems
2. Red border styling on form elements
3. Consistent styling across all checkboxes
4. Proper contrast and accessibility
5. Visual feedback for checked/unchecked states
"""

from PyQt5.QtWidgets import (
    QWidget, QCheckBox, QRadioButton, QGroupBox, QLabel, QLineEdit,
    QTextEdit, QPushButton, QScrollArea, QApplication
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor
from typing import List, Dict, Optional, Union

class CheckboxRenderingFixer:
    """Handles checkbox rendering and form element styling fixes"""
    
    def __init__(self):
        self.primary_color = "#2563EB"  # Blue
        self.success_color = "#16A34A"  # Green  
        self.error_color = "#DC2626"    # Red
        self.text_color = "#1F2937"     # Dark gray
        self.bg_color = "#FFFFFF"       # White
        self.border_color = "#D1D5DB"   # Light gray
        self.hover_color = "#EFF6FF"    # Light blue
        
    def get_modern_checkbox_style(self) -> str:
        """
        Get modern checkbox styling that ensures visibility and proper rendering
        
        Returns:
            CSS string for checkbox styling
        """
        return f"""
            QCheckBox {{
                color: {self.text_color};
                font-weight: 500;
                font-size: 14px;
                padding: 8px 4px;
                spacing: 8px;
                background-color: transparent;
                border: none;
                outline: none;
            }}
            
            QCheckBox:hover {{
                background-color: {self.hover_color};
                border-radius: 4px;
            }}
            
            QCheckBox:disabled {{
                color: #9CA3AF;
            }}
            
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                margin-right: 6px;
                border-radius: 3px;
                border: 2px solid {self.border_color};
                background-color: {self.bg_color};
            }}
            
            QCheckBox::indicator:hover {{
                border-color: {self.primary_color};
                background-color: #F8FAFC;
            }}
            
            QCheckBox::indicator:checked {{
                background-color: {self.primary_color};
                border-color: {self.primary_color};
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEwIDNMNC41IDguNUwyIDYiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=);
            }}
            
            QCheckBox::indicator:checked:hover {{
                background-color: #1D4ED8;
                border-color: #1D4ED8;
            }}
            
            QCheckBox::indicator:checked:disabled {{
                background-color: #9CA3AF;
                border-color: #9CA3AF;
            }}
            
            QCheckBox::indicator:indeterminate {{
                background-color: {self.primary_color};
                border-color: {self.primary_color};
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGxpbmUgeDE9IjMiIHkxPSI2IiB4Mj0iOSIgeTI9IjYiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+Cjwvc3ZnPgo=);
            }}
        """
    
    def get_modern_radio_button_style(self) -> str:
        """
        Get modern radio button styling
        
        Returns:
            CSS string for radio button styling
        """
        return f"""
            QRadioButton {{
                color: {self.text_color};
                font-weight: 500;
                font-size: 14px;
                padding: 8px 4px;
                spacing: 8px;
                background-color: transparent;
                border: none;
                outline: none;
            }}
            
            QRadioButton:hover {{
                background-color: {self.hover_color};
                border-radius: 4px;
            }}
            
            QRadioButton:disabled {{
                color: #9CA3AF;
            }}
            
            QRadioButton::indicator {{
                width: 18px;
                height: 18px;
                margin-right: 6px;
                border-radius: 9px;
                border: 2px solid {self.border_color};
                background-color: {self.bg_color};
            }}
            
            QRadioButton::indicator:hover {{
                border-color: {self.primary_color};
                background-color: #F8FAFC;
            }}
            
            QRadioButton::indicator:checked {{
                background-color: {self.bg_color};
                border-color: {self.primary_color};
                background-image: radial-gradient(circle, {self.primary_color} 40%, transparent 45%);
            }}
            
            QRadioButton::indicator:checked:hover {{
                border-color: #1D4ED8;
                background-image: radial-gradient(circle, #1D4ED8 40%, transparent 45%);
            }}
            
            QRadioButton::indicator:checked:disabled {{
                border-color: #9CA3AF;
                background-image: radial-gradient(circle, #9CA3AF 40%, transparent 45%);
            }}
        """
    
    def get_form_element_styles(self) -> str:
        """
        Get styling for form elements to prevent red borders and ensure consistency
        
        Returns:
            CSS string for form elements
        """
        return f"""
            QLineEdit {{
                padding: 10px 12px;
                border: 2px solid {self.border_color};
                border-radius: 6px;
                font-size: 14px;
                background-color: {self.bg_color};
                color: {self.text_color};
                selection-background-color: {self.primary_color};
                selection-color: white;
            }}
            
            QLineEdit:focus {{
                border-color: {self.primary_color};
                outline: none;
                box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
            }}
            
            QLineEdit:hover {{
                border-color: #9CA3AF;
            }}
            
            QLineEdit:disabled {{
                background-color: #F9FAFB;
                color: #9CA3AF;
                border-color: #E5E7EB;
            }}
            
            QTextEdit {{
                padding: 10px 12px;
                border: 2px solid {self.border_color};
                border-radius: 6px;
                font-size: 14px;
                background-color: {self.bg_color};
                color: {self.text_color};
                selection-background-color: {self.primary_color};
                selection-color: white;
            }}
            
            QTextEdit:focus {{
                border-color: {self.primary_color};
                outline: none;
            }}
            
            QTextEdit:hover {{
                border-color: #9CA3AF;
            }}
            
            QTextEdit:disabled {{
                background-color: #F9FAFB;
                color: #9CA3AF;
                border-color: #E5E7EB;
            }}
            
            QPushButton {{
                background-color: {self.primary_color};
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 600;
                font-size: 14px;
                min-height: 20px;
            }}
            
            QPushButton:hover {{
                background-color: #1D4ED8;
            }}
            
            QPushButton:pressed {{
                background-color: #1E40AF;
            }}
            
            QPushButton:disabled {{
                background-color: #9CA3AF;
                color: #F9FAFB;
            }}
            
            QPushButton[objectName="secondary-button"] {{
                background-color: {self.bg_color};
                color: {self.text_color};
                border: 2px solid {self.border_color};
            }}
            
            QPushButton[objectName="secondary-button"]:hover {{
                background-color: #F9FAFB;
                border-color: {self.primary_color};
                color: {self.primary_color};
            }}
            
            QPushButton[objectName="secondary-button"]:pressed {{
                background-color: #F3F4F6;
            }}
        """
    
    def get_group_box_styles(self) -> str:
        """
        Get styling for group boxes to ensure proper appearance
        
        Returns:
            CSS string for group boxes
        """
        return f"""
            QGroupBox {{
                font-weight: 600;
                font-size: 16px;
                color: {self.text_color};
                border: 2px solid {self.border_color};
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 8px;
                padding-left: 4px;
                padding-right: 4px;
                padding-bottom: 8px;
                background-color: {self.bg_color};
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 12px;
                top: -8px;
                padding: 0 8px;
                background-color: {self.bg_color};
                color: {self.text_color};
            }}
        """
    
    def fix_checkbox_visibility(self, checkboxes: List[QCheckBox]) -> None:
        """
        Fix visibility and styling of checkboxes
        
        Args:
            checkboxes: List of QCheckBox widgets to fix
        """
        checkbox_style = self.get_modern_checkbox_style()
        
        for checkbox in checkboxes:
            if checkbox:
                checkbox.setStyleSheet(checkbox_style)
                # Ensure checkbox is properly sized
                checkbox.setMinimumHeight(32)
                # Force repaint to ensure changes are visible
                checkbox.repaint()
    
    def fix_radio_button_visibility(self, radio_buttons: List[QRadioButton]) -> None:
        """
        Fix visibility and styling of radio buttons
        
        Args:
            radio_buttons: List of QRadioButton widgets to fix
        """
        radio_style = self.get_modern_radio_button_style()
        
        for radio_button in radio_buttons:
            if radio_button:
                radio_button.setStyleSheet(radio_style)
                radio_button.setMinimumHeight(32)
                radio_button.repaint()
    
    def fix_form_element_styling(self, form_elements: List[QWidget]) -> None:
        """
        Fix styling of form elements to prevent red borders and ensure consistency
        
        Args:
            form_elements: List of form widgets (QLineEdit, QTextEdit, etc.) to fix
        """
        form_style = self.get_form_element_styles()
        
        for element in form_elements:
            if element:
                element.setStyleSheet(form_style)
                element.repaint()
    
    def fix_group_box_styling(self, group_boxes: List[QGroupBox]) -> None:
        """
        Fix group box styling for better appearance
        
        Args:
            group_boxes: List of QGroupBox widgets to fix
        """
        group_style = self.get_group_box_styles()
        
        for group_box in group_boxes:
            if group_box:
                group_box.setStyleSheet(group_style)
                group_box.repaint()
    
    def apply_comprehensive_fixes(self, app_window) -> None:
        """
        Apply comprehensive checkbox and form element fixes to the entire application
        
        Args:
            app_window: Main application window instance
        """
        try:
            # Fix trigger checkboxes (left column)
            if hasattr(app_window, 'trigger_checkboxes'):
                self.fix_checkbox_visibility(app_window.trigger_checkboxes)
                print("Fixed trigger checkboxes in left column")
            
            # Fix tense checkboxes (middle column)
            if hasattr(app_window, 'tense_checkboxes'):
                tense_checkboxes = list(app_window.tense_checkboxes.values())
                self.fix_checkbox_visibility(tense_checkboxes)
                print("Fixed tense checkboxes in middle column")
            
            # Fix person checkboxes (middle column)
            if hasattr(app_window, 'person_checkboxes'):
                person_checkboxes = list(app_window.person_checkboxes.values())
                self.fix_checkbox_visibility(person_checkboxes)
                print("Fixed person checkboxes in middle column")
            
            # Fix all QCheckBox widgets found in the application
            all_checkboxes = app_window.findChildren(QCheckBox)
            self.fix_checkbox_visibility(all_checkboxes)
            print(f"Fixed {len(all_checkboxes)} total checkboxes")
            
            # Fix all QRadioButton widgets
            all_radio_buttons = app_window.findChildren(QRadioButton)
            self.fix_radio_button_visibility(all_radio_buttons)
            print(f"Fixed {len(all_radio_buttons)} radio buttons")
            
            # Fix all form elements
            form_elements = []
            form_elements.extend(app_window.findChildren(QLineEdit))
            form_elements.extend(app_window.findChildren(QTextEdit))
            form_elements.extend(app_window.findChildren(QPushButton))
            
            self.fix_form_element_styling(form_elements)
            print(f"Fixed {len(form_elements)} form elements")
            
            # Fix all group boxes
            all_group_boxes = app_window.findChildren(QGroupBox)
            self.fix_group_box_styling(all_group_boxes)
            print(f"Fixed {len(all_group_boxes)} group boxes")
            
            print("Comprehensive checkbox and form element fixes applied successfully")
            
        except Exception as e:
            print(f"Error applying comprehensive fixes: {e}")

# Standalone functions for easy integration
def fix_checkbox_rendering_issues(app_window) -> None:
    """
    Convenience function to fix all checkbox rendering issues in the app
    
    Args:
        app_window: Main application window instance
    """
    fixer = CheckboxRenderingFixer()
    fixer.apply_comprehensive_fixes(app_window)

def apply_modern_checkbox_style(checkbox: QCheckBox) -> None:
    """
    Apply modern styling to a single checkbox
    
    Args:
        checkbox: QCheckBox widget to style
    """
    fixer = CheckboxRenderingFixer()
    fixer.fix_checkbox_visibility([checkbox])

def remove_red_borders_from_forms(app_window) -> None:
    """
    Remove red borders and fix styling of all form elements
    
    Args:
        app_window: Main application window instance
    """
    fixer = CheckboxRenderingFixer()
    
    # Find all form elements that might have red borders
    form_elements = []
    form_elements.extend(app_window.findChildren(QLineEdit))
    form_elements.extend(app_window.findChildren(QTextEdit))
    
    fixer.fix_form_element_styling(form_elements)
    print("Red borders removed from form elements")

# Test function
def test_checkbox_rendering_fixes():
    """Test the checkbox rendering fixes with sample data"""
    import sys
    
    app = QApplication(sys.argv)
    
    # Create test window
    widget = QWidget()
    layout = QVBoxLayout(widget)
    
    # Create test checkboxes
    test_checkboxes = []
    test_texts = [
        "Impersonal expressions (es bueno que, es necesario que)",
        "Wishes and desires (querer que, desear que)",
        "Doubt and denial (dudar que, no creer que)",
        "Present Subjunctive",
        "Imperfect Subjunctive (ra)"
    ]
    
    for text in test_texts:
        cb = QCheckBox(text)
        layout.addWidget(cb)
        test_checkboxes.append(cb)
    
    # Create test form elements
    line_edit = QLineEdit("Test input")
    layout.addWidget(line_edit)
    
    text_edit = QTextEdit("Test text area")
    layout.addWidget(text_edit)
    
    button = QPushButton("Test Button")
    layout.addWidget(button)
    
    # Apply fixes
    fixer = CheckboxRenderingFixer()
    fixer.fix_checkbox_visibility(test_checkboxes)
    fixer.fix_form_element_styling([line_edit, text_edit, button])
    
    widget.setWindowTitle("Checkbox Rendering Fixes Test")
    widget.resize(500, 400)
    widget.show()
    
    print("Test window created. Check that all checkboxes render properly and form elements look good.")
    return app.exec_()

if __name__ == "__main__":
    test_checkbox_rendering_fixes()
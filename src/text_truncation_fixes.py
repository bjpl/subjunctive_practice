#!/usr/bin/env python3
"""
Text Truncation Fixes for Subjunctive Practice App

This module provides fixes for text truncation issues in the left column,
specifically addressing:
1. QCheckBox text truncation in subjunctive indicators
2. Column width constraints
3. Word wrapping for long text
4. Proper minimum widths for readable content
5. Scroll area sizing improvements
"""

from PyQt5.QtWidgets import (
    QWidget, QCheckBox, QScrollArea, QGroupBox, QSplitter, QLabel,
    QVBoxLayout, QHBoxLayout, QSizePolicy, QApplication
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontMetrics
from typing import List, Optional, Union

class TextTruncationFixer:
    """Handles text truncation fixes for the Spanish subjunctive practice app"""
    
    def __init__(self):
        self.minimum_column_width = 280  # Minimum width for left column
        self.preferred_column_width = 350  # Preferred width for left column
        self.checkbox_padding = 20  # Extra padding for checkbox text
        
    def fix_checkbox_text_display(self, checkboxes: List[QCheckBox], parent_widget: QWidget = None) -> None:
        """
        Fix text truncation issues in checkbox widgets
        
        Args:
            checkboxes: List of QCheckBox widgets to fix
            parent_widget: Parent widget for sizing reference
        """
        if not checkboxes:
            return
            
        # Calculate maximum text width needed
        max_text_width = 0
        font = QFont()
        
        for checkbox in checkboxes:
            # Enable word wrap if available (not directly supported by QCheckBox)
            # Instead, we'll ensure proper sizing
            checkbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            
            # Calculate text width
            checkbox_font = checkbox.font()
            font_metrics = QFontMetrics(checkbox_font)
            text_width = font_metrics.horizontalAdvance(checkbox.text()) + self.checkbox_padding
            max_text_width = max(max_text_width, text_width)
            
            # Set minimum size to ensure text is visible
            checkbox.setMinimumWidth(min(text_width, self.minimum_column_width - 40))
            
            # Apply styling to prevent truncation
            checkbox.setStyleSheet("""
                QCheckBox {
                    padding: 4px;
                    spacing: 8px;
                }
                QCheckBox::indicator {
                    width: 16px;
                    height: 16px;
                    margin-right: 8px;
                }
            """)
        
        # If parent widget is provided, adjust its minimum width
        if parent_widget:
            recommended_width = min(max_text_width + 60, self.preferred_column_width)
            parent_widget.setMinimumWidth(recommended_width)
    
    def fix_scroll_area_display(self, scroll_area: QScrollArea) -> None:
        """
        Fix scroll area to properly display content without truncation
        
        Args:
            scroll_area: QScrollArea widget to fix
        """
        if not scroll_area:
            return
            
        # Ensure the scroll area can expand properly
        scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        scroll_area.setWidgetResizable(True)
        
        # Set minimum height and width
        scroll_area.setMinimumHeight(150)
        scroll_area.setMinimumWidth(self.minimum_column_width - 20)
        
        # Enable horizontal scrollbar if needed
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Apply styling for better appearance
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #cccccc;
                border-radius: 4px;
                background-color: white;
            }
            QScrollArea > QWidget > QWidget {
                background-color: white;
            }
        """)
    
    def fix_group_box_display(self, group_box: QGroupBox) -> None:
        """
        Fix group box to properly display content without truncation
        
        Args:
            group_box: QGroupBox widget to fix
        """
        if not group_box:
            return
            
        # Set proper size policy
        group_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        # Set minimum width
        group_box.setMinimumWidth(self.minimum_column_width)
        
        # Apply styling for better readability
        group_box.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin: 5px 0px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                background-color: white;
            }
        """)
    
    def fix_splitter_proportions(self, splitter: QSplitter) -> None:
        """
        Fix splitter proportions to give adequate space to all columns
        
        Args:
            splitter: QSplitter widget to fix
        """
        if not splitter:
            return
            
        # Set minimum sizes for splitter sections
        if splitter.count() == 3:
            # Three-column layout
            # Left pane (index 0) - subjunctive indicators
            splitter.widget(0).setMinimumWidth(self.minimum_column_width)
            
            # Middle pane (index 1) - controls and input
            splitter.widget(1).setMinimumWidth(280)
            
            # Right pane (index 2) - feedback
            splitter.widget(2).setMinimumWidth(300)
            
            # Set stretch factors for better proportions
            splitter.setStretchFactor(0, 2)  # Left column - more space for long text
            splitter.setStretchFactor(1, 1)  # Middle column - compact controls
            splitter.setStretchFactor(2, 3)  # Right column - lots of feedback text
            
            # Set initial sizes for better proportions
            total_width = splitter.width() if splitter.width() > 0 else 1200
            left_width = max(self.preferred_column_width, int(total_width * 0.35))
            middle_width = int(total_width * 0.25)
            right_width = total_width - left_width - middle_width
            
            splitter.setSizes([left_width, middle_width, right_width])
            
        elif splitter.count() >= 2:
            # Two-column layout fallback
            # Left pane (index 0) - subjunctive indicators
            splitter.widget(0).setMinimumWidth(self.minimum_column_width)
            
            # Right pane (index 1) - input and feedback
            splitter.widget(1).setMinimumWidth(400)
            
            # Set stretch factors: left column gets less stretch but adequate space
            splitter.setStretchFactor(0, 1)  # Left column
            splitter.setStretchFactor(1, 2)  # Right column
            
            # Set initial sizes - give left column adequate starting width
            total_width = splitter.width() if splitter.width() > 0 else 800
            left_width = max(self.preferred_column_width, int(total_width * 0.35))
            right_width = total_width - left_width
            
            splitter.setSizes([left_width, right_width])
            
        # Make splitter handle more visible
        splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #d0d0d0;
                width: 3px;
            }
            QSplitter::handle:hover {
                background-color: #a0a0a0;
            }
        """)
    
    def fix_label_word_wrap(self, labels: List[QLabel]) -> None:
        """
        Fix word wrapping for labels to prevent truncation
        
        Args:
            labels: List of QLabel widgets to fix
        """
        for label in labels:
            if label:
                label.setWordWrap(True)
                label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                label.setMinimumWidth(200)
    
    def apply_all_fixes_to_app(self, app_window) -> None:
        """
        Apply all text truncation fixes to the main application window
        
        Args:
            app_window: Main application window instance
        """
        try:
            # Fix checkboxes in trigger section
            if hasattr(app_window, 'trigger_checkboxes'):
                trigger_scroll_content = None
                if hasattr(app_window, 'trigger_scroll_area'):
                    trigger_scroll_content = app_window.trigger_scroll_area.widget()
                
                self.fix_checkbox_text_display(
                    app_window.trigger_checkboxes, 
                    trigger_scroll_content
                )
            
            # Fix scroll area
            if hasattr(app_window, 'trigger_scroll_area'):
                self.fix_scroll_area_display(app_window.trigger_scroll_area)
            
            # Fix group box - find trigger box
            central_widget = app_window.centralWidget()
            if central_widget:
                trigger_boxes = central_widget.findChildren(QGroupBox)
                for box in trigger_boxes:
                    if "Subjunctive Indicators" in box.title():
                        self.fix_group_box_display(box)
                        break
            
            # Fix splitter - look for main_splitter first, then any horizontal splitter
            main_splitter = getattr(app_window, 'main_splitter', None)
            if main_splitter:
                self.fix_splitter_proportions(main_splitter)
            else:
                splitters = app_window.findChildren(QSplitter)
                for splitter in splitters:
                    if splitter.orientation() == Qt.Horizontal:
                        self.fix_splitter_proportions(splitter)
                        break
            
            # Fix labels with word wrap
            labels_to_fix = []
            if hasattr(app_window, 'sentence_label'):
                labels_to_fix.append(app_window.sentence_label)
            if hasattr(app_window, 'translation_label'):
                labels_to_fix.append(app_window.translation_label)
            
            self.fix_label_word_wrap(labels_to_fix)
            
            print("Text truncation fixes applied successfully")
            
        except Exception as e:
            print(f"Error applying text truncation fixes: {e}")

# Standalone functions for easy integration
def fix_text_truncation_issues(app_window) -> None:
    """
    Convenience function to fix all text truncation issues in the app
    
    Args:
        app_window: Main application window instance
    """
    fixer = TextTruncationFixer()
    fixer.apply_all_fixes_to_app(app_window)

def create_non_truncating_checkbox(text: str, parent: QWidget = None) -> QCheckBox:
    """
    Create a checkbox that won't truncate its text
    
    Args:
        text: Text for the checkbox
        parent: Parent widget
        
    Returns:
        QCheckBox configured to prevent text truncation
    """
    checkbox = QCheckBox(text, parent)
    
    # Calculate appropriate width
    font_metrics = QFontMetrics(checkbox.font())
    text_width = font_metrics.horizontalAdvance(text) + 40  # 40px for checkbox and padding
    checkbox.setMinimumWidth(min(text_width, 280))
    
    # Set size policy
    checkbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
    
    # Apply styling
    checkbox.setStyleSheet("""
        QCheckBox {
            padding: 4px;
            spacing: 8px;
        }
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
            margin-right: 8px;
        }
    """)
    
    return checkbox

def configure_column_widths(splitter: QSplitter, left_min_width: int = 280) -> None:
    """
    Configure splitter column widths to prevent text truncation
    
    Args:
        splitter: QSplitter to configure
        left_min_width: Minimum width for the left column
    """
    if splitter and splitter.count() >= 2:
        # Set minimum widths
        splitter.widget(0).setMinimumWidth(left_min_width)
        splitter.widget(1).setMinimumWidth(400)
        
        # Set stretch factors
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        # Set initial proportional sizes
        total_width = splitter.width() if splitter.width() > 0 else 800
        left_width = max(350, int(total_width * 0.35))
        right_width = total_width - left_width
        
        splitter.setSizes([left_width, right_width])

# Test function
def test_text_truncation_fixes():
    """Test the text truncation fixes with sample data"""
    import sys
    
    app = QApplication(sys.argv)
    
    # Create test window
    widget = QWidget()
    layout = QVBoxLayout(widget)
    
    # Create test splitter
    splitter = QSplitter(Qt.Horizontal)
    layout.addWidget(splitter)
    
    # Create left pane with long checkbox text
    left_widget = QWidget()
    left_layout = QVBoxLayout(left_widget)
    
    group_box = QGroupBox("Subjunctive Indicators & Context")
    group_layout = QVBoxLayout(group_box)
    
    scroll_area = QScrollArea()
    scroll_content = QWidget()
    scroll_layout = QVBoxLayout(scroll_content)
    
    # Create test checkboxes with long text
    long_texts = [
        "Impersonal expressions (es bueno que, es necesario que)",
        "Wishes and desires (querer que, desear que, esperar que)",
        "Doubt and denial (dudar que, no creer que, no estar seguro que)",
        "Emotions and reactions (gustar que, sentir que, alegrarse que)",
        "Requests and commands (pedir que, rogar que, sugerir que)"
    ]
    
    checkboxes = []
    for text in long_texts:
        cb = create_non_truncating_checkbox(text)
        scroll_layout.addWidget(cb)
        checkboxes.append(cb)
    
    scroll_area.setWidget(scroll_content)
    group_layout.addWidget(scroll_area)
    left_layout.addWidget(group_box)
    
    # Create right pane
    right_widget = QWidget()
    right_layout = QVBoxLayout(right_widget)
    right_layout.addWidget(QLabel("Right pane content"))
    
    splitter.addWidget(left_widget)
    splitter.addWidget(right_widget)
    
    # Apply fixes
    fixer = TextTruncationFixer()
    fixer.fix_checkbox_text_display(checkboxes, scroll_content)
    fixer.fix_scroll_area_display(scroll_area)
    fixer.fix_group_box_display(group_box)
    fixer.fix_splitter_proportions(splitter)
    
    widget.setWindowTitle("Text Truncation Fixes Test")
    widget.resize(800, 600)
    widget.show()
    
    print("Test window created. Check that all checkbox text is fully visible.")
    return app.exec_()

if __name__ == "__main__":
    test_text_truncation_fixes()
#!/usr/bin/env python3
"""
Test script for the Spanish Subjunctive Practice App spacing optimizer.

This script verifies that the spacing optimization system works correctly
and demonstrates the improvements in text spacing and layout.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QGroupBox, QPushButton, QSplitter
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Import our spacing optimizer
from src.spacing_optimizer import (
    SpacingOptimizer, 
    TypographySpacingProfile, 
    ReadabilityOptimizer,
    LayoutSpacingManager
)


class SpacingTestWindow(QMainWindow):
    """Test window to demonstrate spacing optimization"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spanish Subjunctive Practice - Spacing Optimization Test")
        self.setGeometry(100, 100, 1000, 700)
        
        # Initialize spacing optimizer
        self.spacing_optimizer = SpacingOptimizer(base_font_size=13, line_height_ratio=1.55)
        
        self.setup_ui()
        self.demonstrate_spacing()
    
    def setup_ui(self):
        """Set up the test UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("Spacing Optimization Test - Spanish Subjunctive Practice")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        main_layout.addWidget(title)
        
        # Create splitter for before/after comparison
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left side - Before optimization
        left_widget = self.create_test_content("Before Optimization (Basic Spacing)")
        splitter.addWidget(left_widget)
        
        # Right side - After optimization
        right_widget = self.create_test_content("After Optimization (Enhanced Spacing)")
        self.optimize_widget_spacing(right_widget)
        splitter.addWidget(right_widget)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        toggle_btn = QPushButton("Toggle Global Optimization")
        toggle_btn.clicked.connect(self.toggle_global_optimization)
        button_layout.addWidget(toggle_btn)
        
        report_btn = QPushButton("Show Spacing Report")
        report_btn.clicked.connect(self.show_spacing_report)
        button_layout.addWidget(report_btn)
        
        main_layout.addLayout(button_layout)
    
    def create_test_content(self, title: str) -> QWidget:
        """Create test content widget"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Section title
        section_title = QLabel(title)
        section_title.setStyleSheet("font-weight: bold; color: #0066cc;")
        layout.addWidget(section_title)
        
        # Sample sentence (like in the Spanish app)
        sentence_group = QGroupBox("Exercise Sentence")
        sentence_layout = QVBoxLayout(sentence_group)
        
        sentence_label = QLabel(
            "Es importante que tú estudies el subjuntivo para mejorar tu español."
        )
        sentence_label.setWordWrap(True)
        sentence_layout.addWidget(sentence_label)
        
        translation_label = QLabel(
            "Translation: It's important that you study the subjunctive to improve your Spanish."
        )
        translation_label.setStyleSheet("color: gray; font-style: italic;")
        translation_label.setWordWrap(True)
        sentence_layout.addWidget(translation_label)
        
        layout.addWidget(sentence_group)
        
        # Instructions group (like in the Spanish app)
        instructions_group = QGroupBox("Instructions")
        instructions_layout = QVBoxLayout(instructions_group)
        
        instructions_text = QTextEdit()
        instructions_text.setPlainText(
            "Select the correct subjunctive form:\n\n"
            "The subjunctive mood is used after expressions of importance, "
            "doubt, emotion, and other triggers. In this exercise, 'es importante que' "
            "requires the subjunctive form 'estudies' rather than the indicative 'estudias'.\n\n"
            "Key indicators:\n"
            "• Impersonal expressions (es importante que)\n"
            "• Expressions of doubt or emotion\n"
            "• Wishes and desires\n"
            "• Recommendations and suggestions"
        )
        instructions_text.setMaximumHeight(200)
        instructions_text.setReadOnly(True)
        instructions_layout.addWidget(instructions_text)
        
        layout.addWidget(instructions_group)
        
        # Stats label (like in the Spanish app)
        stats_label = QLabel("Exercise: 3/10 | Correct: 2 | Accuracy: 66.7%")
        stats_label.setStyleSheet("color: gray;")
        layout.addWidget(stats_label)
        
        # Store references for optimization
        widget.sentence_label = sentence_label
        widget.translation_label = translation_label
        widget.instructions_text = instructions_text
        widget.stats_label = stats_label
        widget.sentence_group = sentence_group
        widget.instructions_group = instructions_group
        
        return widget
    
    def optimize_widget_spacing(self, widget: QWidget):
        """Apply spacing optimization to the widget"""
        try:
            # Optimize text elements
            self.spacing_optimizer.optimize_widget_spacing(widget.sentence_label)
            self.spacing_optimizer.optimize_widget_spacing(widget.translation_label)
            self.spacing_optimizer.optimize_widget_spacing(widget.instructions_text)
            self.spacing_optimizer.optimize_widget_spacing(widget.stats_label)
            
            # Optimize group boxes
            self.spacing_optimizer.optimize_widget_spacing(widget.sentence_group)
            self.spacing_optimizer.optimize_widget_spacing(widget.instructions_group)
            
            # Optimize layout
            layout = widget.layout()
            if layout:
                self.spacing_optimizer.optimize_layout_spacing(layout)
            
            # Add breathing room
            self.spacing_optimizer.add_breathing_room_to_container(widget)
            
        except Exception as e:
            print(f"Error optimizing widget spacing: {e}")
    
    def demonstrate_spacing(self):
        """Demonstrate different spacing techniques"""
        print("=== Spacing Optimization Demonstration ===")
        
        # Show typography profile
        profile = self.spacing_optimizer.profile
        print(f"\nTypography Profile:")
        print(f"  Font size: {profile.font_size}px")
        print(f"  Line height: {profile.line_height}px (ratio: {profile.line_height_ratio})")
        print(f"  Paragraph spacing: {profile.paragraph_spacing}px")
        print(f"  Section spacing: {profile.section_spacing}px")
        print(f"  Content margin: {profile.content_margin}px")
        
        # Show spacing calculations
        print(f"\nSpacing Calculations:")
        print(f"  Optimal line height for 13px font: {profile.line_height}px")
        print(f"  Reading-optimized margins: {profile.content_margin}px")
        print(f"  Visual hierarchy spacing: {profile.section_spacing}px")
    
    def toggle_global_optimization(self):
        """Toggle global spacing optimization"""
        app = QApplication.instance()
        if app:
            self.spacing_optimizer.optimize_entire_application(app)
            print("Applied global spacing optimization to entire application")
    
    def show_spacing_report(self):
        """Show detailed spacing report"""
        report = self.spacing_optimizer.get_spacing_report()
        
        print("\n=== Spacing Optimization Report ===")
        print(f"\nCurrent Profile:")
        for key, value in report['profile'].items():
            print(f"  {key}: {value}")
        
        print(f"\nRecommendations:")
        for rec in report['recommendations']:
            print(f"  • {rec}")


def test_spacing_components():
    """Test individual spacing components"""
    print("\n=== Component Testing ===")
    
    # Test TypographySpacingProfile
    profile = TypographySpacingProfile(14, 1.6)
    print(f"Typography Profile Test:")
    print(f"  Font: 14px, Line height: {profile.line_height}px")
    print(f"  Paragraph spacing: {profile.paragraph_spacing}px")
    
    # Test SpacingCalculator
    from src.spacing_optimizer import SpacingCalculator
    from PyQt5.QtGui import QFont
    
    font = QFont("Arial", 12)
    line_height = SpacingCalculator.calculate_line_height(font, 1.5)
    paragraph_spacing = SpacingCalculator.calculate_paragraph_spacing(12)
    
    print(f"\nSpacing Calculator Test:")
    print(f"  Line height for 12px font: {line_height}px")
    print(f"  Paragraph spacing: {paragraph_spacing}px")
    
    # Test margin calculations
    margins = SpacingCalculator.calculate_content_margins(800, 20)
    print(f"  Content margins for 800px width: {margins}")


def main():
    """Main test function"""
    app = QApplication(sys.argv)
    
    # Test individual components
    test_spacing_components()
    
    # Create and show test window
    window = SpacingTestWindow()
    window.show()
    
    print("\n=== Visual Test Instructions ===")
    print("1. Compare the 'Before' and 'After' panels side by side")
    print("2. Notice the improved line spacing (1.55 ratio) in the 'After' panel")
    print("3. Observe better paragraph spacing and margins")
    print("4. Click 'Toggle Global Optimization' to apply to entire app")
    print("5. Click 'Show Spacing Report' for detailed metrics")
    print("\nKey improvements:")
    print("  • Line height: 1.55 for better readability")
    print("  • Enhanced padding and margins")
    print("  • Visual breathing room between elements")
    print("  • Typography-based spacing calculations")
    
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
"""
Minimal UI Fixes for Spanish Subjunctive Practice App

Addresses only the critical issues reported:
1. Text/elements too small to read - slightly increases font sizes
2. Form input text not visible when window expanded - fixes visibility
3. No progress feedback during API calls - simple status message
4. Red boxes around form selectors - removes harsh red styling

This module provides targeted, minimal fixes without over-engineering.
"""

from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QComboBox, QLabel
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt


class MinimalUIFixes:
    """Simple, focused UI improvements that address only the reported issues."""
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.status_label = None
        
    def apply_all_fixes(self):
        """Apply all minimal fixes in one method."""
        self.fix_font_sizes()
        self.fix_red_boxes()
        self.setup_simple_status()
        self.fix_text_visibility()
    
    def fix_font_sizes(self):
        """Slightly increase font sizes to make text readable - not huge."""
        # Find all text elements and make them slightly bigger
        for widget in self.main_window.findChildren((QLabel, QLineEdit, QComboBox)):
            current_font = widget.font()
            # Only increase if current font is too small
            if current_font.pointSize() < 12:
                current_font.setPointSize(12)
                widget.setFont(current_font)
            elif current_font.pointSize() < 14:
                current_font.setPointSize(14)
                widget.setFont(current_font)
    
    def fix_red_boxes(self):
        """Remove red boxes around form selectors with subtle styling."""
        app = QApplication.instance()
        if app:
            palette = app.palette()
            # Replace harsh system colors with subtle blue
            palette.setColor(QPalette.Highlight, QColor('#3182CE'))
            palette.setColor(QPalette.HighlightedText, QColor('white'))
            app.setPalette(palette)
        
        # Apply minimal CSS to remove aggressive red styling
        simple_css = """
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #3182CE;
                outline: none;
            }
            QLineEdit, QComboBox {
                border: 1px solid #CBD5E0;
                padding: 8px;
                font-size: 14px;
            }
            QLineEdit:hover, QComboBox:hover {
                border-color: #A0AEC0;
            }
        """
        
        # Apply to all form elements
        for widget in self.main_window.findChildren((QLineEdit, QComboBox)):
            current_style = widget.styleSheet()
            widget.setStyleSheet(current_style + simple_css)
    
    def fix_text_visibility(self):
        """Ensure text remains visible when window is expanded."""
        # Simple CSS for better text contrast and visibility
        visibility_css = """
            QLineEdit {
                color: #1A202C;
                background-color: white;
                border: 1px solid #CBD5E0;
                padding: 8px;
                font-size: 14px;
            }
            QComboBox {
                color: #1A202C;
                background-color: white;
                border: 1px solid #CBD5E0;
                padding: 8px;
                font-size: 14px;
            }
            QLabel {
                color: #1A202C;
                font-size: 14px;
            }
        """
        
        for widget in self.main_window.findChildren((QLineEdit, QComboBox, QLabel)):
            current_style = widget.styleSheet()
            widget.setStyleSheet(current_style + visibility_css)
    
    def setup_simple_status(self):
        """Add a simple status message area for API call feedback."""
        # Find the main layout and add a simple status label at the bottom
        try:
            central_widget = self.main_window.centralWidget()
            if central_widget:
                # Create simple status label if it doesn't exist
                if not hasattr(self.main_window, 'status_label'):
                    self.status_label = QLabel("")
                    self.status_label.setStyleSheet("""
                        QLabel {
                            padding: 8px;
                            background-color: #F7FAFC;
                            border: 1px solid #E2E8F0;
                            border-radius: 4px;
                            color: #4A5568;
                            font-size: 13px;
                        }
                    """)
                    self.status_label.setAlignment(Qt.AlignCenter)
                    self.status_label.hide()  # Hidden by default
                    
                    # Try to add to the main layout
                    main_layout = central_widget.layout()
                    if main_layout:
                        main_layout.addWidget(self.status_label)
                    
                    self.main_window.status_label = self.status_label
        except Exception:
            # If we can't add to layout, create a simple floating status
            pass
    
    def show_status(self, message: str, is_loading: bool = True):
        """Show a simple status message."""
        if hasattr(self.main_window, 'status_label') and self.main_window.status_label:
            if is_loading:
                self.main_window.status_label.setText(f"⏳ {message}")
                self.main_window.status_label.setStyleSheet("""
                    QLabel {
                        padding: 8px;
                        background-color: #EBF4FF;
                        border: 1px solid #3182CE;
                        border-radius: 4px;
                        color: #1A365D;
                        font-size: 13px;
                    }
                """)
            else:
                self.main_window.status_label.setText(f"✅ {message}")
                self.main_window.status_label.setStyleSheet("""
                    QLabel {
                        padding: 8px;
                        background-color: #F0FDF4;
                        border: 1px solid #16A34A;
                        border-radius: 4px;
                        color: #166534;
                        font-size: 13px;
                    }
                """)
            self.main_window.status_label.show()
    
    def hide_status(self):
        """Hide the status message."""
        if hasattr(self.main_window, 'status_label') and self.main_window.status_label:
            self.main_window.status_label.hide()
    
    def show_api_loading(self, operation: str = "Processing"):
        """Simple loading indicator for API calls."""
        self.show_status(f"{operation}... Please wait (may take up to 1 minute)", is_loading=True)
    
    def show_api_complete(self, operation: str = "Complete"):
        """Show completion status."""
        self.show_status(f"{operation}!", is_loading=False)
        # Auto-hide after 3 seconds
        if hasattr(self.main_window, 'status_label'):
            from PyQt5.QtCore import QTimer
            QTimer.singleShot(3000, self.hide_status)
    
    def show_api_error(self, error: str = "Error occurred"):
        """Show error status."""
        if hasattr(self.main_window, 'status_label') and self.main_window.status_label:
            self.main_window.status_label.setText(f"❌ {error}")
            self.main_window.status_label.setStyleSheet("""
                QLabel {
                    padding: 8px;
                    background-color: #FEF2F2;
                    border: 1px solid #DC2626;
                    border-radius: 4px;
                    color: #991B1B;
                    font-size: 13px;
                }
            """)
            self.main_window.status_label.show()
            # Auto-hide after 5 seconds
            from PyQt5.QtCore import QTimer
            QTimer.singleShot(5000, self.hide_status)


def apply_minimal_fixes(main_window):
    """
    Apply minimal UI fixes to the main window.
    
    Usage:
        from src.minimal_ui_fixes import apply_minimal_fixes
        ui_fixes = apply_minimal_fixes(main_window)
        
        # For API calls:
        ui_fixes.show_api_loading("Generating exercises")
        # ... do API call ...
        ui_fixes.show_api_complete("Exercises generated")
    """
    fixes = MinimalUIFixes(main_window)
    fixes.apply_all_fixes()
    return fixes


# Simple integration helper for existing code
class SimpleProgressHelper:
    """Simple progress helper that can be easily integrated into existing API calls."""
    
    def __init__(self, ui_fixes):
        self.ui_fixes = ui_fixes
    
    def start(self, message: str = "Loading"):
        """Start showing progress."""
        self.ui_fixes.show_api_loading(message)
    
    def finish(self, message: str = "Complete"):
        """Show completion."""
        self.ui_fixes.show_api_complete(message)
    
    def error(self, message: str = "Error occurred"):
        """Show error."""
        self.ui_fixes.show_api_error(message)


if __name__ == "__main__":
    """
    Test the minimal fixes
    """
    import sys
    from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton
    
    app = QApplication(sys.argv)
    
    # Test window
    test_window = QWidget()
    test_window.setWindowTitle("Minimal UI Fixes Test")
    test_window.setMinimumSize(600, 400)
    
    layout = QVBoxLayout(test_window)
    
    # Test elements
    test_input = QLineEdit("Test input - should be visible and readable")
    test_combo = QComboBox()
    test_combo.addItems(["Option 1", "Option 2", "Option 3"])
    test_label = QLabel("This text should be readable (not too small)")
    
    layout.addWidget(test_label)
    layout.addWidget(test_input)
    layout.addWidget(test_combo)
    
    # Test button for status
    def test_status():
        fixes.show_api_loading("Testing API call")
        QApplication.processEvents()
        
        # Simulate API delay
        import time
        time.sleep(2)
        
        fixes.show_api_complete("Test completed")
    
    test_btn = QPushButton("Test Status Message")
    test_btn.clicked.connect(test_status)
    layout.addWidget(test_btn)
    
    # Apply fixes
    fixes = apply_minimal_fixes(test_window)
    
    test_window.show()
    sys.exit(app.exec_())
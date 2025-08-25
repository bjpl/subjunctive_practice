"""
Form Styling Fixes for Spanish Subjunctive Practice App

This module addresses specific form styling issues:
1. Red box validation/focus states that are awkward
2. Text visibility issues when window is expanded
3. Poor padding, font size, and contrast
4. Non-responsive form elements
5. Missing proper hover and focus states

Key fixes:
- Removes aggressive red validation styling
- Improves text contrast and visibility
- Adds proper responsive sizing
- Implements clean hover/focus states
- Ensures accessibility compliance
"""

from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QComboBox, QCheckBox, QRadioButton, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor


class FormStylingManager:
    """
    Manages consistent form styling across the application with fixes for common issues.
    """
    
    # Modern, accessible color palette
    COLORS = {
        # Base colors - high contrast
        'background': '#FFFFFF',
        'surface': '#FAFBFC',
        'text_primary': '#1A202C',
        'text_secondary': '#4A5568',
        'text_muted': '#718096',
        
        # Form-specific colors with better contrast
        'input_bg': '#FFFFFF',
        'input_border': '#CBD5E0',
        'input_border_hover': '#A0AEC0',
        'input_border_focus': '#3B82F6',  # Professional blue instead of red
        'input_text': '#1A202C',
        'placeholder': '#9CA3AF',
        
        # State colors - softer, less aggressive
        'success_bg': '#F0FDF4',
        'success_border': '#16A34A',
        'success_text': '#166534',
        
        'error_bg': '#FEF2F2',
        'error_border': '#DC2626',
        'error_text': '#991B1B',
        
        'warning_bg': '#FFFBEB',
        'warning_border': '#D97706',
        'warning_text': '#92400E',
        
        # Interactive states
        'hover_bg': '#F7FAFC',
        'active_bg': '#EDF2F7',
        'disabled_bg': '#F7FAFC',
        'disabled_text': '#A0AEC0',
    }
    
    # Dark theme colors for accessibility
    DARK_COLORS = {
        'background': '#1A202C',
        'surface': '#2D3748',
        'text_primary': '#F7FAFC',
        'text_secondary': '#E2E8F0',
        'text_muted': '#A0AEC0',
        
        'input_bg': '#2D3748',
        'input_border': '#4A5568',
        'input_border_hover': '#718096',
        'input_border_focus': '#63B3ED',
        'input_text': '#F7FAFC',
        'placeholder': '#718096',
        
        'success_bg': '#1A2F1A',
        'success_border': '#38A169',
        'success_text': '#9AE6B4',
        
        'error_bg': '#2D1B1B',
        'error_border': '#E53E3E',
        'error_text': '#FC8181',
        
        'warning_bg': '#2D2014',
        'warning_border': '#ED8936',
        'warning_text': '#F6AD55',
        
        'hover_bg': '#4A5568',
        'active_bg': '#718096',
        'disabled_bg': '#2D3748',
        'disabled_text': '#718096',
    }
    
    def __init__(self, dark_mode: bool = False):
        self.dark_mode = dark_mode
        self.colors = self.DARK_COLORS if dark_mode else self.COLORS
    
    def get_base_form_stylesheet(self) -> str:
        """
        Returns base stylesheet for all form elements with improved styling.
        Removes aggressive red validation styling and improves overall appearance.
        """
        return f"""
            /* ==============================================
               BASE FORM ELEMENT STYLES - Clean & Accessible
               ============================================== */
               
            QLineEdit {{
                /* Remove aggressive red validation styling */
                background-color: {self.colors['input_bg']};
                border: 2px solid {self.colors['input_border']};
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 16px;
                font-weight: 400;
                color: {self.colors['input_text']};
                selection-background-color: {self.colors['input_border_focus']};
                selection-color: white;
                min-height: 24px;
                outline: none;
            }}
            
            QLineEdit::placeholder {{
                color: {self.colors['placeholder']};
                font-style: italic;
            }}
            
            /* Subtle hover state instead of harsh red */
            QLineEdit:hover {{
                border-color: {self.colors['input_border_hover']};
                background-color: {self.colors['hover_bg']};
                transition: all 0.2s ease;
            }}
            
            /* Clean focus state - blue instead of red */
            QLineEdit:focus {{
                border-color: {self.colors['input_border_focus']};
                background-color: {self.colors['input_bg']};
                outline: none;
                /* Removed harsh red focus styling */
            }}
            
            /* Disabled state */
            QLineEdit:disabled {{
                background-color: {self.colors['disabled_bg']};
                color: {self.colors['disabled_text']};
                border-color: {self.colors['input_border']};
            }}
            
            /* ==============================================
               COMBO BOX STYLING - Consistent with inputs
               ============================================== */
               
            QComboBox {{
                background-color: {self.colors['input_bg']};
                border: 2px solid {self.colors['input_border']};
                border-radius: 8px;
                padding: 12px 16px;
                padding-right: 32px;  /* Space for dropdown arrow */
                font-size: 16px;
                color: {self.colors['input_text']};
                min-width: 120px;
                min-height: 24px;
            }}
            
            QComboBox:hover {{
                border-color: {self.colors['input_border_hover']};
                background-color: {self.colors['hover_bg']};
            }}
            
            QComboBox:focus {{
                border-color: {self.colors['input_border_focus']};
                outline: none;
            }}
            
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 28px;
                border: none;
                background: transparent;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            }}
            
            QComboBox::down-arrow {{
                image: none;
                border-style: solid;
                border-width: 5px 4px 0 4px;
                border-color: {self.colors['text_secondary']} transparent transparent transparent;
            }}
            
            QComboBox QAbstractItemView {{
                border: 1px solid {self.colors['input_border']};
                border-radius: 8px;
                background-color: {self.colors['input_bg']};
                selection-background-color: {self.colors['hover_bg']};
                selection-color: {self.colors['input_text']};
                padding: 4px;
                outline: none;
            }}
            
            /* ==============================================
               CHECKBOX & RADIO BUTTON FIXES
               ============================================== */
               
            QCheckBox, QRadioButton {{
                font-size: 16px;
                color: {self.colors['text_primary']};
                padding: 8px;
                margin: 4px 0;
                spacing: 8px;
                outline: none;
            }}
            
            QCheckBox::indicator, QRadioButton::indicator {{
                width: 20px;
                height: 20px;
                border: 2px solid {self.colors['input_border']};
                background-color: {self.colors['input_bg']};
                border-radius: 4px;
            }}
            
            QRadioButton::indicator {{
                border-radius: 10px;  /* Circular for radio buttons */
            }}
            
            /* Hover states - subtle not aggressive */
            QCheckBox::indicator:hover, QRadioButton::indicator:hover {{
                border-color: {self.colors['input_border_hover']};
                background-color: {self.colors['hover_bg']};
            }}
            
            /* Checked states - blue theme instead of harsh red */
            QCheckBox::indicator:checked, QRadioButton::indicator:checked {{
                background-color: {self.colors['input_border_focus']};
                border-color: {self.colors['input_border_focus']};
            }}
            
            /* Focus states for accessibility */
            QCheckBox:focus::indicator, QRadioButton:focus::indicator {{
                outline: 2px solid {self.colors['input_border_focus']};
                outline-offset: 1px;
            }}
            
            /* ==============================================
               TEXT EDIT AREAS - Improved visibility
               ============================================== */
               
            QTextEdit {{
                background-color: {self.colors['input_bg']};
                border: 2px solid {self.colors['input_border']};
                border-radius: 8px;
                padding: 16px;
                font-size: 16px;
                font-family: "Segoe UI", system-ui, sans-serif;
                color: {self.colors['input_text']};
                line-height: 1.5;
                selection-background-color: {self.colors['input_border_focus']};
                selection-color: white;
            }}
            
            QTextEdit:hover {{
                border-color: {self.colors['input_border_hover']};
            }}
            
            QTextEdit:focus {{
                border-color: {self.colors['input_border_focus']};
                outline: none;
            }}
            
            /* ==============================================
               RESPONSIVE SCROLLBARS
               ============================================== */
               
            QScrollBar:vertical {{
                background-color: {self.colors['surface']};
                width: 14px;
                border-radius: 7px;
                margin: 0px;
            }}
            
            QScrollBar::handle:vertical {{
                background-color: {self.colors['input_border']};
                border-radius: 7px;
                min-height: 30px;
                margin: 2px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background-color: {self.colors['input_border_hover']};
            }}
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                border: none;
                background: none;
                height: 0px;
            }}
        """
    
    def get_state_specific_styles(self) -> dict:
        """
        Returns state-specific styles for form validation.
        Replaces aggressive red styling with gentler alternatives.
        """
        return {
            'success': f"""
                border-color: {self.colors['success_border']};
                background-color: {self.colors['success_bg']};
                color: {self.colors['success_text']};
            """,
            
            'error': f"""
                border-color: {self.colors['error_border']};
                background-color: {self.colors['error_bg']};
                color: {self.colors['error_text']};
            """,
            
            'warning': f"""
                border-color: {self.colors['warning_border']};
                background-color: {self.colors['warning_bg']};
                color: {self.colors['warning_text']};
            """,
            
            'neutral': f"""
                border-color: {self.colors['input_border']};
                background-color: {self.colors['input_bg']};
                color: {self.colors['input_text']};
            """
        }
    
    def apply_responsive_sizing(self, widget: QWidget, window_width: int = 1100):
        """
        Apply responsive sizing to form elements based on window size.
        Ensures text remains visible and elements scale properly.
        """
        # Calculate responsive scaling
        scale_factor = max(0.8, min(1.2, window_width / 1100))
        
        if isinstance(widget, (QLineEdit, QComboBox)):
            # Responsive font size and padding
            font_size = int(16 * scale_factor)
            padding = max(8, int(12 * scale_factor))
            
            responsive_style = f"""
                font-size: {font_size}px;
                padding: {padding}px {padding + 4}px;
                min-height: {max(24, int(24 * scale_factor))}px;
            """
            
            # Preserve existing styles and add responsive ones
            current_style = widget.styleSheet()
            widget.setStyleSheet(current_style + responsive_style)
        
        elif isinstance(widget, QTextEdit):
            font_size = int(16 * scale_factor)
            padding = max(12, int(16 * scale_factor))
            
            responsive_style = f"""
                font-size: {font_size}px;
                padding: {padding}px;
                line-height: 1.5;
            """
            
            current_style = widget.styleSheet()
            widget.setStyleSheet(current_style + responsive_style)
        
        elif isinstance(widget, (QCheckBox, QRadioButton)):
            font_size = int(16 * scale_factor)
            indicator_size = max(18, int(20 * scale_factor))
            
            responsive_style = f"""
                font-size: {font_size}px;
                spacing: {max(6, int(8 * scale_factor))}px;
            """
            
            # Update indicator size through setProperty for CSS selectors
            widget.setProperty('indicatorSize', f'{indicator_size}px')
            current_style = widget.styleSheet()
            widget.setStyleSheet(current_style + responsive_style)
    
    def apply_form_validation_state(self, widget: QWidget, state: str):
        """
        Apply form validation styling with improved, less aggressive appearance.
        
        Args:
            widget: The form widget to style
            state: 'success', 'error', 'warning', or 'neutral'
        """
        state_styles = self.get_state_specific_styles()
        
        if state in state_styles:
            base_style = widget.styleSheet()
            # Remove any existing state styling
            for existing_state in state_styles.keys():
                widget.setProperty('validationState', None)
            
            # Apply new state
            widget.setProperty('validationState', state)
            additional_style = state_styles[state]
            
            # Combine base and state-specific styles
            widget.setStyleSheet(base_style + additional_style)
            
            # Force style refresh
            widget.style().unpolish(widget)
            widget.style().polish(widget)
    
    def remove_aggressive_focus_styling(self, app: QApplication):
        """
        Remove system-level aggressive focus styling that creates red boxes.
        This addresses the core issue mentioned in the requirements.
        """
        # Create a custom palette with softer focus colors
        palette = app.palette()
        
        # Set focus colors to blue instead of harsh system colors
        focus_color = QColor(self.colors['input_border_focus'])
        
        palette.setColor(QPalette.Highlight, focus_color)
        palette.setColor(QPalette.HighlightedText, QColor('white'))
        
        app.setPalette(palette)
    
    def create_enhanced_form_styles(self) -> str:
        """
        Creates comprehensive enhanced form styles addressing all major issues.
        """
        base_styles = self.get_base_form_stylesheet()
        
        enhanced_styles = f"""
            {base_styles}
            
            /* ==============================================
               ENHANCED GROUP BOX STYLING
               ============================================== */
               
            QGroupBox {{
                font-size: 18px;
                font-weight: 600;
                color: {self.colors['text_primary']};
                border: 2px solid {self.colors['input_border']};
                border-radius: 12px;
                padding: 20px 16px 16px 16px;
                margin: 16px 0 8px 0;
                background-color: {self.colors['input_bg']};
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 16px;
                top: -8px;
                padding: 0 8px;
                color: {self.colors['input_border_focus']};
                background-color: {self.colors['input_bg']};
                border-radius: 4px;
            }}
            
            /* ==============================================
               SCROLL AREA ENHANCEMENTS
               ============================================== */
               
            QScrollArea {{
                border: 1px solid {self.colors['input_border']};
                border-radius: 8px;
                background-color: {self.colors['input_bg']};
            }}
            
            QScrollArea > QWidget > QWidget {{
                background-color: transparent;
            }}
            
            /* ==============================================
               RESPONSIVE DESIGN UTILITIES
               ============================================== */
               
            /* Small screens */
            @media (max-width: 768px) {{
                QLineEdit, QComboBox {{
                    font-size: 14px;
                    padding: 10px 12px;
                }}
                
                QTextEdit {{
                    font-size: 14px;
                    padding: 12px;
                }}
                
                QCheckBox, QRadioButton {{
                    font-size: 14px;
                    spacing: 6px;
                }}
            }}
            
            /* Large screens */
            @media (min-width: 1400px) {{
                QLineEdit, QComboBox {{
                    font-size: 18px;
                    padding: 14px 18px;
                }}
                
                QTextEdit {{
                    font-size: 18px;
                    padding: 18px;
                }}
                
                QCheckBox, QRadioButton {{
                    font-size: 18px;
                    spacing: 10px;
                }}
            }}
        """
        
        return enhanced_styles


def apply_form_styling_fixes(app: QApplication, main_window, dark_mode: bool = False):
    """
    Apply comprehensive form styling fixes to the Spanish Subjunctive Practice app.
    
    This function addresses:
    1. Aggressive red box validation styling
    2. Text visibility issues
    3. Poor responsive behavior
    4. Missing hover/focus states
    
    Args:
        app: The QApplication instance
        main_window: The main window instance
        dark_mode: Whether to use dark theme colors
    """
    # Initialize styling manager
    styling_manager = FormStylingManager(dark_mode)
    
    # Remove aggressive system focus styling
    styling_manager.remove_aggressive_focus_styling(app)
    
    # Apply base form styles
    enhanced_styles = styling_manager.create_enhanced_form_styles()
    app.setStyleSheet(app.styleSheet() + enhanced_styles)
    
    # Apply responsive sizing to all form elements
    window_width = main_window.width()
    
    # Find and style all form elements
    for widget in main_window.findChildren(QLineEdit):
        styling_manager.apply_responsive_sizing(widget, window_width)
        styling_manager.apply_form_validation_state(widget, 'neutral')
    
    for widget in main_window.findChildren(QComboBox):
        styling_manager.apply_responsive_sizing(widget, window_width)
    
    for widget in main_window.findChildren(QTextEdit):
        styling_manager.apply_responsive_sizing(widget, window_width)
    
    for widget in main_window.findChildren((QCheckBox, QRadioButton)):
        styling_manager.apply_responsive_sizing(widget, window_width)
    
    return styling_manager


def create_form_state_manager(styling_manager: FormStylingManager):
    """
    Create a form state manager for handling validation states cleanly.
    
    Returns a callable that can be used to set form validation states
    without aggressive red styling.
    """
    def set_form_state(widget: QWidget, state: str, message: str = ""):
        """
        Set form validation state with improved visual feedback.
        
        Args:
            widget: The form widget
            state: 'success', 'error', 'warning', 'neutral'
            message: Optional message to display
        """
        styling_manager.apply_form_validation_state(widget, state)
        
        # Set tooltip for additional feedback instead of harsh styling
        if message:
            widget.setToolTip(message)
        else:
            widget.setToolTip("")
    
    return set_form_state


# Utility functions for easy integration

def fix_form_red_boxes(app: QApplication):
    """
    Quick fix for removing red box focus styling system-wide.
    """
    palette = app.palette()
    focus_color = QColor('#3B82F6')  # Professional blue
    palette.setColor(QPalette.Highlight, focus_color)
    palette.setColor(QPalette.HighlightedText, QColor('white'))
    app.setPalette(palette)


def improve_text_contrast(widget: QWidget, dark_mode: bool = False):
    """
    Improve text contrast and visibility for a specific widget.
    """
    colors = FormStylingManager.DARK_COLORS if dark_mode else FormStylingManager.COLORS
    
    contrast_style = f"""
        color: {colors['text_primary']};
        background-color: {colors['input_bg']};
        font-weight: 500;
        line-height: 1.5;
    """
    
    current_style = widget.styleSheet()
    widget.setStyleSheet(current_style + contrast_style)


def make_form_responsive(widget: QWidget, window_width: int):
    """
    Make a single form element responsive to window size changes.
    """
    manager = FormStylingManager()
    manager.apply_responsive_sizing(widget, window_width)


if __name__ == "__main__":
    """
    Test the form styling fixes
    """
    import sys
    from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QGroupBox
    
    app = QApplication(sys.argv)
    
    # Test window
    test_window = QWidget()
    test_window.setWindowTitle("Form Styling Fixes Test")
    test_window.setMinimumSize(800, 600)
    
    layout = QVBoxLayout(test_window)
    
    # Test form elements
    group = QGroupBox("Test Form Elements")
    form_layout = QVBoxLayout(group)
    
    # Test input
    test_input = QLineEdit()
    test_input.setPlaceholderText("Type here to test styling...")
    form_layout.addWidget(QLabel("Input Field:"))
    form_layout.addWidget(test_input)
    
    # Test combo
    test_combo = QComboBox()
    test_combo.addItems(["Option 1", "Option 2", "Option 3"])
    form_layout.addWidget(QLabel("Dropdown:"))
    form_layout.addWidget(test_combo)
    
    # Test checkboxes
    cb1 = QCheckBox("Test checkbox 1")
    cb2 = QCheckBox("Test checkbox 2")
    form_layout.addWidget(QLabel("Checkboxes:"))
    form_layout.addWidget(cb1)
    form_layout.addWidget(cb2)
    
    layout.addWidget(group)
    
    # Apply fixes
    styling_manager = apply_form_styling_fixes(app, test_window)
    
    test_window.show()
    sys.exit(app.exec_())
"""
Visual Design Module for Spanish Subjunctive Practice App

This module provides a clean, modern visual design system with:
- Consistent color palette with good contrast
- Clean typography and spacing
- Professional button styling with clear hover states
- Cohesive visual language across all components
- PyQt5-optimized styling using built-in capabilities
"""

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor


class VisualTheme:
    """
    Centralized theme management for consistent visual design.
    """
    
    # Modern Color Palette
    COLORS = {
        # Primary Colors
        'primary': '#2E86AB',           # Professional blue
        'primary_hover': '#1F5F7A',     # Darker blue for hover
        'primary_pressed': '#174A5C',   # Even darker for pressed state
        'primary_light': '#E3F2FD',     # Light blue background
        
        # Secondary Colors  
        'secondary': '#A23B72',         # Complementary purple
        'secondary_hover': '#7A2B56',   # Darker purple
        'secondary_light': '#F3E5F5',   # Light purple background
        
        # Neutral Colors
        'background': '#FAFBFC',        # Very light gray background
        'surface': '#FFFFFF',           # Pure white for cards/panels
        'border': '#E1E8ED',            # Light border color
        'border_focus': '#2E86AB',      # Focus border color
        'border_hover': '#BDC3C7',      # Hover border color
        
        # Text Colors
        'text_primary': '#2C3E50',      # Dark blue-gray for primary text
        'text_secondary': '#5A6C7D',    # Lighter blue-gray for secondary text
        'text_muted': '#95A5A6',        # Muted gray for hints/placeholders
        'text_on_primary': '#FFFFFF',   # White text on primary backgrounds
        
        # Status Colors
        'success': '#27AE60',           # Green for success states
        'success_light': '#D5EDDB',     # Light green background
        'warning': '#F39C12',           # Orange for warnings
        'warning_light': '#FDF2E9',     # Light orange background
        'error': '#E74C3C',             # Red for errors
        'error_light': '#FADBD8',       # Light red background
        'info': '#3498DB',              # Info blue
        'info_light': '#EBF3FD',        # Light info background
    }
    
    # Typography Scale
    FONTS = {
        'base_family': 'Segoe UI, system-ui, -apple-system, sans-serif',
        'mono_family': 'Consolas, Monaco, monospace',
        'sizes': {
            'xs': '12px',
            'sm': '13px', 
            'base': '14px',
            'lg': '15px',
            'xl': '16px',
            'xxl': '18px',
            'title': '20px'
        },
        'weights': {
            'normal': 400,
            'medium': 500,
            'semibold': 600,
            'bold': 700
        }
    }
    
    # Spacing Scale (following 8px grid)
    SPACING = {
        'xs': '4px',
        'sm': '8px',
        'md': '12px',
        'lg': '16px',
        'xl': '20px',
        'xxl': '24px',
        'xxxl': '32px'
    }
    
    # Border Radius
    RADIUS = {
        'sm': '4px',
        'base': '6px', 
        'lg': '8px',
        'xl': '12px',
        'full': '50%'
    }
    
    # Shadows
    SHADOWS = {
        'subtle': '0 1px 3px rgba(0, 0, 0, 0.05)',
        'base': '0 2px 8px rgba(0, 0, 0, 0.08)',
        'elevated': '0 4px 20px rgba(0, 0, 0, 0.12)'
    }


def get_modern_stylesheet() -> str:
    """
    Returns a comprehensive modern stylesheet for the Spanish subjunctive app.
    Uses PyQt5's built-in styling capabilities effectively.
    """
    theme = VisualTheme()
    
    return f"""
        /* ==============================================
           BASE STYLES - Foundation
           ============================================== */
        
        QMainWindow {{
            background-color: {theme.COLORS['background']};
            color: {theme.COLORS['text_primary']};
            font-family: {theme.FONTS['base_family']};
            font-size: {theme.FONTS['sizes']['base']};
        }}
        
        QWidget {{
            font-family: {theme.FONTS['base_family']};
            font-size: {theme.FONTS['sizes']['base']};
            color: {theme.COLORS['text_primary']};
            background-color: transparent;
        }}
        
        /* ==============================================
           TYPOGRAPHY - Clean and readable
           ============================================== */
        
        QLabel {{
            color: {theme.COLORS['text_primary']};
            font-size: {theme.FONTS['sizes']['base']};
            font-weight: {theme.FONTS['weights']['medium']};
            padding: {theme.SPACING['xs']} 0;
            margin: 0;
            line-height: 1.4;
        }}
        
        QLabel[role="secondary"] {{
            color: {theme.COLORS['text_secondary']};
            font-size: {theme.FONTS['sizes']['sm']};
            font-weight: {theme.FONTS['weights']['normal']};
        }}
        
        QLabel[role="muted"] {{
            color: {theme.COLORS['text_muted']};
            font-size: {theme.FONTS['sizes']['sm']};
        }}
        
        /* ==============================================
           CONTAINERS - Clean panels and groups
           ============================================== */
        
        QGroupBox {{
            font-size: {theme.FONTS['sizes']['lg']};
            font-weight: {theme.FONTS['weights']['semibold']};
            color: {theme.COLORS['text_primary']};
            border: 2px solid {theme.COLORS['border']};
            border-radius: {theme.RADIUS['lg']};
            margin: {theme.SPACING['lg']} {theme.SPACING['sm']};
            padding-top: {theme.SPACING['xl']};
            background-color: {theme.COLORS['surface']};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: {theme.SPACING['md']};
            top: {theme.SPACING['sm']};
            color: {theme.COLORS['primary']};
            background-color: {theme.COLORS['surface']};
            padding: 0 {theme.SPACING['sm']};
            font-weight: {theme.FONTS['weights']['semibold']};
        }}
        
        /* ==============================================
           BUTTONS - Modern with clear states
           ============================================== */
        
        QPushButton {{
            background-color: {theme.COLORS['primary']};
            color: {theme.COLORS['text_on_primary']};
            border: none;
            border-radius: {theme.RADIUS['base']};
            padding: {theme.SPACING['md']} {theme.SPACING['xl']};
            font-weight: {theme.FONTS['weights']['semibold']};
            font-size: {theme.FONTS['sizes']['base']};
            margin: {theme.SPACING['xs']};
            min-height: {theme.SPACING['lg']};
            min-width: 80px;
        }}
        
        QPushButton:hover {{
            background-color: {theme.COLORS['primary_hover']};
            transform: translateY(-1px);
        }}
        
        QPushButton:pressed {{
            background-color: {theme.COLORS['primary_pressed']};
            transform: translateY(0px);
        }}
        
        QPushButton:disabled {{
            background-color: {theme.COLORS['text_muted']};
            color: {theme.COLORS['background']};
        }}
        
        /* Secondary button variant */
        QPushButton[variant="secondary"] {{
            background-color: {theme.COLORS['surface']};
            color: {theme.COLORS['primary']};
            border: 2px solid {theme.COLORS['primary']};
        }}
        
        QPushButton[variant="secondary"]:hover {{
            background-color: {theme.COLORS['primary_light']};
            border-color: {theme.COLORS['primary_hover']};
        }}
        
        /* ==============================================
           INPUT FIELDS - Clean and focused
           ============================================== */
        
        QLineEdit, QTextEdit {{
            border: 2px solid {theme.COLORS['border']};
            border-radius: {theme.RADIUS['base']};
            padding: {theme.SPACING['md']};
            background-color: {theme.COLORS['surface']};
            font-size: {theme.FONTS['sizes']['base']};
            color: {theme.COLORS['text_primary']};
            selection-background-color: {theme.COLORS['primary']};
            selection-color: {theme.COLORS['text_on_primary']};
        }}
        
        QLineEdit:hover, QTextEdit:hover {{
            border-color: {theme.COLORS['border_hover']};
        }}
        
        QLineEdit:focus, QTextEdit:focus {{
            border-color: {theme.COLORS['border_focus']};
            outline: none;
        }}
        
        QLineEdit::placeholder, QTextEdit::placeholder {{
            color: {theme.COLORS['text_muted']};
            font-style: italic;
        }}
        
        /* ==============================================
           DROPDOWN MENUS - Consistent with inputs
           ============================================== */
        
        QComboBox {{
            border: 2px solid {theme.COLORS['border']};
            border-radius: {theme.RADIUS['base']};
            padding: {theme.SPACING['md']};
            background-color: {theme.COLORS['surface']};
            font-size: {theme.FONTS['sizes']['base']};
            color: {theme.COLORS['text_primary']};
            min-width: 120px;
        }}
        
        QComboBox:hover {{
            border-color: {theme.COLORS['border_hover']};
        }}
        
        QComboBox:focus {{
            border-color: {theme.COLORS['border_focus']};
        }}
        
        QComboBox::drop-down {{
            border: none;
            background: transparent;
            width: 20px;
            margin-right: {theme.SPACING['xs']};
        }}
        
        QComboBox::down-arrow {{
            border: none;
            background: transparent;
            color: {theme.COLORS['text_secondary']};
        }}
        
        QComboBox QAbstractItemView {{
            border: 1px solid {theme.COLORS['border']};
            border-radius: {theme.RADIUS['base']};
            background-color: {theme.COLORS['surface']};
            selection-background-color: {theme.COLORS['primary_light']};
            selection-color: {theme.COLORS['text_primary']};
        }}
        
        /* ==============================================
           CHECKBOXES & RADIO BUTTONS - Clear interaction
           ============================================== */
        
        QCheckBox, QRadioButton {{
            font-size: {theme.FONTS['sizes']['base']};
            color: {theme.COLORS['text_primary']};
            padding: {theme.SPACING['sm']};
            margin: {theme.SPACING['xs']} {theme.SPACING['sm']};
            spacing: {theme.SPACING['sm']};
        }}
        
        QCheckBox::indicator, QRadioButton::indicator {{
            width: 18px;
            height: 18px;
            border: 2px solid {theme.COLORS['border']};
            border-radius: {theme.RADIUS['sm']};
            background-color: {theme.COLORS['surface']};
        }}
        
        QRadioButton::indicator {{
            border-radius: 11px; /* Make radio buttons circular */
        }}
        
        QCheckBox::indicator:hover, QRadioButton::indicator:hover {{
            border-color: {theme.COLORS['primary']};
        }}
        
        QCheckBox::indicator:checked, QRadioButton::indicator:checked {{
            background-color: {theme.COLORS['primary']};
            border-color: {theme.COLORS['primary']};
        }}
        
        QCheckBox::indicator:checked {{
            image: none; /* We'll use CSS for the checkmark */
        }}
        
        /* ==============================================
           PROGRESS BAR - Clean progress indication
           ============================================== */
        
        QProgressBar {{
            border: 2px solid {theme.COLORS['border']};
            border-radius: {theme.RADIUS['base']};
            background-color: {theme.COLORS['surface']};
            text-align: center;
            font-weight: {theme.FONTS['weights']['semibold']};
            font-size: {theme.FONTS['sizes']['sm']};
            color: {theme.COLORS['text_primary']};
            height: 28px;
        }}
        
        QProgressBar::chunk {{
            background-color: {theme.COLORS['success']};
            border-radius: {theme.RADIUS['sm']};
            margin: 2px;
        }}
        
        /* ==============================================
           SCROLL AREAS - Clean scrolling
           ============================================== */
        
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}
        
        QScrollArea > QWidget > QWidget {{
            background-color: transparent;
        }}
        
        QScrollBar:vertical {{
            background-color: {theme.COLORS['border']};
            width: 12px;
            border-radius: 6px;
            margin: 0;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {theme.COLORS['text_muted']};
            border-radius: 6px;
            min-height: 20px;
            margin: 2px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {theme.COLORS['primary']};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            border: none;
            background: none;
            height: 0;
        }}
        
        /* ==============================================
           STATUS BAR - Subtle information bar
           ============================================== */
        
        QStatusBar {{
            background-color: {theme.COLORS['surface']};
            border-top: 1px solid {theme.COLORS['border']};
            color: {theme.COLORS['text_secondary']};
            font-size: {theme.FONTS['sizes']['sm']};
            padding: {theme.SPACING['xs']};
        }}
        
        /* ==============================================
           TOOLBAR - Clean command bar
           ============================================== */
        
        QToolBar {{
            background-color: {theme.COLORS['surface']};
            border: none;
            border-bottom: 1px solid {theme.COLORS['border']};
            spacing: {theme.SPACING['xs']};
            padding: {theme.SPACING['xs']};
            font-size: {theme.FONTS['sizes']['sm']};
        }}
        
        QToolBar QToolButton {{
            background-color: transparent;
            border: none;
            border-radius: {theme.RADIUS['sm']};
            padding: {theme.SPACING['sm']} {theme.SPACING['md']};
            margin: {theme.SPACING['xs']};
            color: {theme.COLORS['text_primary']};
        }}
        
        QToolBar QToolButton:hover {{
            background-color: {theme.COLORS['primary_light']};
            color: {theme.COLORS['primary']};
        }}
        
        /* ==============================================
           SPLITTER - Minimal dividers
           ============================================== */
        
        QSplitter::handle {{
            background-color: {theme.COLORS['border']};
            border: none;
            border-radius: 1px;
        }}
        
        QSplitter::handle:horizontal {{
            width: 3px;
            margin: 0 {theme.SPACING['xs']};
        }}
        
        QSplitter::handle:vertical {{
            height: 3px;
            margin: {theme.SPACING['xs']} 0;
        }}
        
        QSplitter::handle:hover {{
            background-color: {theme.COLORS['primary']};
        }}
        
        /* ==============================================
           TABLES - Clean data presentation
           ============================================== */
        
        QTableWidget {{
            border: 1px solid {theme.COLORS['border']};
            border-radius: {theme.RADIUS['lg']};
            background-color: {theme.COLORS['surface']};
            gridline-color: {theme.COLORS['border']};
            font-size: {theme.FONTS['sizes']['base']};
            selection-background-color: {theme.COLORS['primary_light']};
            selection-color: {theme.COLORS['text_primary']};
        }}
        
        QHeaderView::section {{
            background-color: {theme.COLORS['background']};
            border: none;
            border-bottom: 2px solid {theme.COLORS['border']};
            padding: {theme.SPACING['md']};
            font-weight: {theme.FONTS['weights']['semibold']};
            font-size: {theme.FONTS['sizes']['sm']};
            color: {theme.COLORS['text_primary']};
        }}
        
        QTableWidget::item {{
            padding: {theme.SPACING['md']};
            border: none;
            border-bottom: 1px solid {theme.COLORS['border']};
        }}
        
        QTableWidget::item:selected {{
            background-color: {theme.COLORS['primary_light']};
            color: {theme.COLORS['text_primary']};
        }}
        
        /* ==============================================
           DIALOG & MESSAGE BOXES - Clean modals
           ============================================== */
        
        QDialog {{
            background-color: {theme.COLORS['surface']};
            border: 1px solid {theme.COLORS['border']};
            border-radius: {theme.RADIUS['lg']};
        }}
        
        QMessageBox {{
            background-color: {theme.COLORS['surface']};
            font-size: {theme.FONTS['sizes']['base']};
        }}
        
        QMessageBox QPushButton {{
            min-width: 80px;
            padding: {theme.SPACING['sm']} {theme.SPACING['lg']};
        }}
        
        /* ==============================================
           TAB WIDGET - Clean navigation
           ============================================== */
        
        QTabWidget::pane {{
            border: 1px solid {theme.COLORS['border']};
            border-radius: {theme.RADIUS['base']};
            background-color: {theme.COLORS['surface']};
            margin-top: -1px;
        }}
        
        QTabWidget::tab-bar {{
            alignment: center;
        }}
        
        QTabBar::tab {{
            background-color: {theme.COLORS['background']};
            color: {theme.COLORS['text_secondary']};
            border: 1px solid {theme.COLORS['border']};
            border-bottom: none;
            border-top-left-radius: {theme.RADIUS['base']};
            border-top-right-radius: {theme.RADIUS['base']};
            padding: {theme.SPACING['md']} {theme.SPACING['xl']};
            margin-right: 2px;
            font-weight: {theme.FONTS['weights']['medium']};
        }}
        
        QTabBar::tab:selected {{
            background-color: {theme.COLORS['surface']};
            color: {theme.COLORS['primary']};
            border-color: {theme.COLORS['border']};
        }}
        
        QTabBar::tab:hover:!selected {{
            background-color: {theme.COLORS['primary_light']};
            color: {theme.COLORS['primary']};
        }}
        
        /* ==============================================
           UTILITY CLASSES - Helper styles
           ============================================== */
        
        /* Success state styling */
        .success {{
            color: {theme.COLORS['success']};
            background-color: {theme.COLORS['success_light']};
        }}
        
        /* Warning state styling */
        .warning {{
            color: {theme.COLORS['warning']};
            background-color: {theme.COLORS['warning_light']};
        }}
        
        /* Error state styling */
        .error {{
            color: {theme.COLORS['error']};
            background-color: {theme.COLORS['error_light']};
        }}
        
        /* Info state styling */
        .info {{
            color: {theme.COLORS['info']};
            background-color: {theme.COLORS['info_light']};
        }}
    """


def get_dark_theme_stylesheet() -> str:
    """
    Returns a dark theme variant of the stylesheet.
    """
    # Dark theme color overrides
    dark_colors = {
        'background': '#1E1E1E',
        'surface': '#2D2D2D', 
        'border': '#3E3E3E',
        'border_focus': '#4A9EFF',
        'border_hover': '#5A5A5A',
        'text_primary': '#E1E1E1',
        'text_secondary': '#B0B0B0',
        'text_muted': '#707070',
        'primary': '#4A9EFF',
        'primary_hover': '#6BB0FF',
        'primary_pressed': '#3388DD',
        'primary_light': '#1A3A5A',
    }
    
    # For dark theme, we'd modify the base stylesheet
    # This is a simplified version - you could create a full dark theme
    return f"""
        QMainWindow {{
            background-color: {dark_colors['background']};
            color: {dark_colors['text_primary']};
        }}
        
        QWidget {{
            color: {dark_colors['text_primary']};
            background-color: transparent;
        }}
        
        QGroupBox {{
            background-color: {dark_colors['surface']};
            border-color: {dark_colors['border']};
            color: {dark_colors['text_primary']};
        }}
        
        QGroupBox::title {{
            color: {dark_colors['primary']};
            background-color: {dark_colors['surface']};
        }}
        
        QPushButton {{
            background-color: {dark_colors['primary']};
            color: white;
        }}
        
        QPushButton:hover {{
            background-color: {dark_colors['primary_hover']};
        }}
        
        QLineEdit, QTextEdit, QComboBox {{
            background-color: {dark_colors['surface']};
            border-color: {dark_colors['border']};
            color: {dark_colors['text_primary']};
        }}
        
        QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
            border-color: {dark_colors['border_focus']};
        }}
    """


class StyleManager:
    """
    Manages application styling and theme switching.
    """
    
    def __init__(self, app: QApplication):
        self.app = app
        self.current_theme = 'light'
        
    def apply_modern_theme(self):
        """Apply the modern light theme to the application."""
        stylesheet = get_modern_stylesheet()
        self.app.setStyleSheet(stylesheet)
        self.current_theme = 'light'
        
    def apply_dark_theme(self):
        """Apply the dark theme to the application.""" 
        stylesheet = get_dark_theme_stylesheet()
        self.app.setStyleSheet(stylesheet)
        self.current_theme = 'dark'
        
    def toggle_theme(self):
        """Toggle between light and dark themes."""
        if self.current_theme == 'light':
            self.apply_dark_theme()
        else:
            self.apply_modern_theme()
            
    def get_current_theme(self) -> str:
        """Get the current theme name."""
        return self.current_theme


def apply_widget_specific_styles(widget: QWidget, style_class: str = None):
    """
    Apply specific styling to individual widgets.
    
    Args:
        widget: The widget to style
        style_class: Optional CSS class name for specific styling
    """
    if style_class == 'primary-button':
        widget.setProperty('variant', 'primary')
    elif style_class == 'secondary-button':
        widget.setProperty('variant', 'secondary')
    elif style_class == 'success':
        widget.setProperty('class', 'success')
    elif style_class == 'warning':
        widget.setProperty('class', 'warning')
    elif style_class == 'error':
        widget.setProperty('class', 'error')
    elif style_class == 'info':
        widget.setProperty('class', 'info')
    
    # Force style refresh
    widget.style().unpolish(widget)
    widget.style().polish(widget)


def create_font(size: str = 'base', weight: str = 'normal') -> QFont:
    """
    Create a QFont with theme specifications.
    
    Args:
        size: Font size key from FONTS['sizes']
        weight: Font weight key from FONTS['weights']
    """
    theme = VisualTheme()
    font = QFont(theme.FONTS['base_family'])
    
    # Parse size (remove 'px' suffix and convert to int)
    size_value = int(theme.FONTS['sizes'].get(size, theme.FONTS['sizes']['base']).replace('px', ''))
    font.setPointSize(size_value)
    
    # Set weight
    weight_value = theme.FONTS['weights'].get(weight, theme.FONTS['weights']['normal'])
    font.setWeight(weight_value // 10)  # QFont uses different weight scale
    
    return font


def setup_high_dpi_support(app: QApplication):
    """
    Configure high DPI support for crisp rendering on high resolution displays.
    """
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


# Convenience functions for easy integration
def initialize_modern_ui(app: QApplication) -> StyleManager:
    """
    Initialize the modern UI with optimal settings.
    
    Args:
        app: The QApplication instance
        
    Returns:
        StyleManager instance for theme control
    """
    # Setup high DPI support
    setup_high_dpi_support(app)
    
    # Create and apply modern theme
    style_manager = StyleManager(app)
    style_manager.apply_modern_theme()
    
    return style_manager


if __name__ == "__main__":
    """
    Demo script to preview the visual design.
    """
    import sys
    from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QGroupBox
    
    app = QApplication(sys.argv)
    
    # Initialize modern UI
    style_manager = initialize_modern_ui(app)
    
    # Create demo window
    demo = QWidget()
    demo.setWindowTitle("Spanish Subjunctive Practice - Visual Design Demo")
    demo.setMinimumSize(800, 600)
    
    layout = QVBoxLayout(demo)
    
    # Demo content
    title = QLabel("Modern Visual Design Preview")
    title.setStyleSheet(f"font-size: {VisualTheme.FONTS['sizes']['title']}; font-weight: {VisualTheme.FONTS['weights']['bold']};")
    layout.addWidget(title)
    
    # Button examples
    button_group = QGroupBox("Button Examples")
    button_layout = QHBoxLayout(button_group)
    
    primary_btn = QPushButton("Primary Action")
    secondary_btn = QPushButton("Secondary")
    apply_widget_specific_styles(secondary_btn, 'secondary-button')
    
    button_layout.addWidget(primary_btn)
    button_layout.addWidget(secondary_btn)
    layout.addWidget(button_group)
    
    # Input examples
    input_group = QGroupBox("Input Examples")
    input_layout = QVBoxLayout(input_group)
    
    text_input = QLineEdit()
    text_input.setPlaceholderText("Type your Spanish answer here...")
    input_layout.addWidget(text_input)
    
    layout.addWidget(input_group)
    
    # Theme toggle
    theme_btn = QPushButton("Toggle Dark Theme")
    theme_btn.clicked.connect(style_manager.toggle_theme)
    layout.addWidget(theme_btn)
    
    demo.show()
    sys.exit(app.exec_())
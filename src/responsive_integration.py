"""
Responsive Design Integration for Spanish Subjunctive Practice Application
=========================================================================

This module integrates the modern responsive design system with the existing
Spanish Subjunctive Practice application, providing seamless responsive
behavior while maintaining compatibility with the current codebase.

Features:
- Seamless integration with existing main.py application
- Responsive layout adaptation for all screen sizes
- Modern visual theme with smooth transitions
- Enhanced accessibility and touch-friendly interactions
- Performance-optimized responsive behavior
- Cross-platform compatibility
"""

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QScrollArea, QGroupBox, QLabel, QPushButton, QLineEdit,
    QTextEdit, QProgressBar, QComboBox, QCheckBox, QRadioButton,
    QButtonGroup, QStatusBar, QToolBar, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt, QSize, QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QFont, QFontMetrics, QPalette, QColor, QScreen
from typing import Dict, List, Tuple, Optional, Any
import logging

# Import our responsive design modules
try:
    from .modern_responsive_design import (
        ModernThemeManager, ResponsiveLayoutManager as BaseResponsiveLayoutManager,
        create_modern_responsive_app, apply_widget_variant, apply_widget_role, apply_widget_state
    )
    from .enhanced_responsive_layout import (
        ResponsiveCard, ResponsiveGrid, AdaptiveSplitter, ResponsiveContainer,
        ModernTabWidget, ResponsiveForm, ResponsiveLayoutManager
    )
except ImportError:
    # Handle relative imports
    try:
        from modern_responsive_design import (
            ModernThemeManager, ResponsiveLayoutManager as BaseResponsiveLayoutManager,
            create_modern_responsive_app, apply_widget_variant, apply_widget_role, apply_widget_state
        )
        from enhanced_responsive_layout import (
            ResponsiveCard, ResponsiveGrid, AdaptiveSplitter, ResponsiveContainer,
            ModernTabWidget, ResponsiveForm, ResponsiveLayoutManager
        )
    except ImportError as e:
        print(f"Warning: Could not import responsive design modules: {e}")
        # Define fallback classes
        class ModernThemeManager:
            def __init__(self, app): pass
            def apply_theme(self, theme=None): pass
            def toggle_theme(self): pass
            def get_current_theme(self): return 'light'
        
        class ResponsiveLayoutManager:
            def __init__(self, widget): pass
            def handle_resize(self, size): pass
        
        def create_modern_responsive_app(app, window): return None, None
        def apply_widget_variant(widget, variant): pass
        def apply_widget_role(widget, role): pass
        def apply_widget_state(widget, state): pass
        
        ResponsiveCard = QGroupBox
        ResponsiveGrid = QWidget
        AdaptiveSplitter = QSplitter
        ResponsiveContainer = QScrollArea
        ModernTabWidget = QWidget
        ResponsiveForm = QWidget

logger = logging.getLogger(__name__)


class ResponsiveSpanishApp:
    """
    Enhanced version of the Spanish Subjunctive Practice app with modern responsive design
    """
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.theme_manager = None
        self.layout_manager = None
        self.responsive_components = []
        self.original_methods = {}  # Store original method references
        
        # Initialize responsive design
        self._initialize_responsive_design()
    
    def _initialize_responsive_design(self):
        """Initialize the responsive design system"""
        try:
            app = QApplication.instance()
            if app:
                # Initialize modern responsive app
                self.theme_manager, self.layout_manager = create_modern_responsive_app(
                    app, self.main_window
                )
                
                if self.theme_manager and self.layout_manager:
                    logger.info("Modern responsive design system initialized successfully")
                else:
                    logger.warning("Failed to initialize responsive design system")
                    self._setup_fallback_responsive_design()
            else:
                logger.warning("No QApplication instance found")
                self._setup_fallback_responsive_design()
                
        except Exception as e:
            logger.error(f"Error initializing responsive design: {e}")
            self._setup_fallback_responsive_design()
    
    def _setup_fallback_responsive_design(self):
        """Setup basic responsive design as fallback"""
        app = QApplication.instance()
        if app:
            self.theme_manager = ModernThemeManager(app)
            self.layout_manager = ResponsiveLayoutManager(self.main_window)
    
    def enhance_existing_ui(self):
        """
        Enhance the existing UI with responsive design elements
        This method modifies the existing UI without breaking functionality
        """
        try:
            self._enhance_main_layout()
            self._enhance_widgets()
            self._setup_responsive_behavior()
            self._apply_modern_styling()
            logger.info("UI enhancement completed successfully")
        except Exception as e:
            logger.error(f"Error enhancing UI: {e}")
    
    def _enhance_main_layout(self):
        """Enhance the main layout with responsive components"""
        if not hasattr(self.main_window, 'centralWidget'):
            return
        
        central_widget = self.main_window.centralWidget()
        if not central_widget:
            return
        
        # Find the main splitter and enhance it
        splitters = central_widget.findChildren(QSplitter)
        for splitter in splitters:
            self._enhance_splitter(splitter)
    
    def _enhance_splitter(self, splitter: QSplitter):
        """Enhance a splitter with responsive behavior"""
        # Apply modern splitter styling
        splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #e2e8f0;
                border: none;
                border-radius: 2px;
            }
            
            QSplitter::handle:horizontal {
                width: 2px;
                margin: 0 4px;
            }
            
            QSplitter::handle:vertical {
                height: 2px;
                margin: 4px 0;
            }
            
            QSplitter::handle:hover {
                background-color: #3b82f6;
            }
        """)
        
        # Add responsive behavior
        self.responsive_components.append({
            'widget': splitter,
            'type': 'splitter',
            'adapt_function': self._adapt_splitter
        })
    
    def _enhance_widgets(self):
        """Enhance individual widgets with modern styling and responsive behavior"""
        if not hasattr(self.main_window, 'centralWidget'):
            return
            
        central_widget = self.main_window.centralWidget()
        if not central_widget:
            return
        
        # Enhance buttons
        buttons = central_widget.findChildren(QPushButton)
        for button in buttons:
            self._enhance_button(button)
        
        # Enhance input fields
        line_edits = central_widget.findChildren(QLineEdit)
        for line_edit in line_edits:
            self._enhance_input_field(line_edit)
        
        text_edits = central_widget.findChildren(QTextEdit)
        for text_edit in text_edits:
            self._enhance_text_area(text_edit)
        
        # Enhance labels
        labels = central_widget.findChildren(QLabel)
        for label in labels:
            self._enhance_label(label)
        
        # Enhance group boxes
        group_boxes = central_widget.findChildren(QGroupBox)
        for group_box in group_boxes:
            self._enhance_group_box(group_box)
        
        # Enhance progress bars
        progress_bars = central_widget.findChildren(QProgressBar)
        for progress_bar in progress_bars:
            self._enhance_progress_bar(progress_bar)
    
    def _enhance_button(self, button: QPushButton):
        """Enhance a button with modern styling"""
        # Determine button variant based on text/role
        button_text = button.text().lower()
        
        if any(word in button_text for word in ['submit', 'generate', 'next', 'start']):
            apply_widget_variant(button, 'primary')
        elif any(word in button_text for word in ['hint', 'help', 'show']):
            apply_widget_variant(button, 'outline')
        elif any(word in button_text for word in ['cancel', 'reset', 'clear']):
            apply_widget_variant(button, 'secondary')
        else:
            apply_widget_variant(button, 'secondary')
        
        # Add to responsive components
        self.responsive_components.append({
            'widget': button,
            'type': 'button',
            'adapt_function': self._adapt_button
        })
    
    def _enhance_input_field(self, input_field: QLineEdit):
        """Enhance an input field with modern styling"""
        input_field.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding: 12px 16px;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                background-color: #ffffff;
                color: #1f2937;
                selection-background-color: #dbeafe;
                selection-color: #1e40af;
            }
            
            QLineEdit:hover {
                border-color: #d1d5db;
            }
            
            QLineEdit:focus {
                border-color: #3b82f6;
                outline: none;
            }
            
            QLineEdit::placeholder {
                color: #9ca3af;
                font-style: italic;
            }
        """)
        
        # Add to responsive components
        self.responsive_components.append({
            'widget': input_field,
            'type': 'input',
            'adapt_function': self._adapt_input_field
        })
    
    def _enhance_text_area(self, text_area: QTextEdit):
        """Enhance a text area with modern styling"""
        text_area.setStyleSheet("""
            QTextEdit {
                font-size: 15px;
                line-height: 1.6;
                padding: 16px;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                background-color: #ffffff;
                color: #1f2937;
                selection-background-color: #dbeafe;
                selection-color: #1e40af;
            }
            
            QTextEdit:hover {
                border-color: #d1d5db;
            }
            
            QTextEdit:focus {
                border-color: #3b82f6;
            }
        """)
        
        self.responsive_components.append({
            'widget': text_area,
            'type': 'textarea',
            'adapt_function': self._adapt_text_area
        })
    
    def _enhance_label(self, label: QLabel):
        """Enhance a label with proper typography"""
        # Determine label role based on object name or text
        object_name = label.objectName().lower()
        text = label.text().lower()
        
        if any(word in object_name for word in ['sentence', 'exercise']):
            apply_widget_role(label, 'title')
        elif any(word in object_name for word in ['translation', 'context']):
            apply_widget_role(label, 'subtitle')
        elif any(word in object_name for word in ['stats', 'progress']):
            apply_widget_role(label, 'caption')
        else:
            apply_widget_role(label, 'body')
        
        self.responsive_components.append({
            'widget': label,
            'type': 'label',
            'adapt_function': self._adapt_label
        })
    
    def _enhance_group_box(self, group_box: QGroupBox):
        """Enhance a group box with modern card styling"""
        group_box.setStyleSheet("""
            QGroupBox {
                background-color: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
                padding: 20px;
                margin: 8px 0;
                font-weight: 600;
                font-size: 16px;
                color: #374151;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 16px;
                top: -12px;
                padding: 0 8px;
                background-color: #ffffff;
                color: #6366f1;
                font-weight: 600;
            }
        """)
        
        self.responsive_components.append({
            'widget': group_box,
            'type': 'groupbox',
            'adapt_function': self._adapt_group_box
        })
    
    def _enhance_progress_bar(self, progress_bar: QProgressBar):
        """Enhance a progress bar with modern styling"""
        progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 6px;
                background-color: #f3f4f6;
                text-align: center;
                font-weight: 500;
                font-size: 14px;
                color: #374151;
                height: 12px;
            }
            
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #3b82f6, stop:0.5 #1d4ed8, stop:1 #1e40af);
                border-radius: 6px;
                margin: 0;
            }
        """)
    
    def _setup_responsive_behavior(self):
        """Setup responsive behavior for the application"""
        # Connect to window resize events
        if hasattr(self.main_window, 'resizeEvent'):
            original_resize_event = self.main_window.resizeEvent
            
            def enhanced_resize_event(event):
                original_resize_event(event)
                self._handle_window_resize(event.size())
            
            self.main_window.resizeEvent = enhanced_resize_event
        
        # Setup initial responsive state
        self._handle_window_resize(self.main_window.size())
    
    def _handle_window_resize(self, size: QSize):
        """Handle window resize events and update responsive components"""
        width = size.width()
        
        # Update all responsive components
        for component in self.responsive_components:
            try:
                component['adapt_function'](component['widget'], width)
            except Exception as e:
                logger.error(f"Error adapting component {component['type']}: {e}")
        
        # Update layout manager if available
        if self.layout_manager:
            self.layout_manager.handle_resize(size)
    
    def _adapt_splitter(self, splitter: QSplitter, width: int):
        """Adapt splitter behavior for different screen sizes"""
        if width <= 768:  # Mobile breakpoint
            if splitter.orientation() != Qt.Vertical:
                splitter.setOrientation(Qt.Vertical)
                splitter.setSizes([60, 40])  # Content area gets more space
        else:
            if splitter.orientation() != Qt.Horizontal:
                splitter.setOrientation(Qt.Horizontal)
                if width <= 1024:
                    splitter.setSizes([65, 35])  # Tablet
                else:
                    splitter.setSizes([70, 30])  # Desktop
    
    def _adapt_button(self, button: QPushButton, width: int):
        """Adapt button styling for different screen sizes"""
        if width <= 576:  # Mobile
            button.setMinimumHeight(48)  # Larger touch targets
            button.setStyleSheet(button.styleSheet() + """
                QPushButton {
                    font-size: 16px;
                    padding: 14px 20px;
                    margin: 4px 2px;
                }
            """)
        else:
            button.setMinimumHeight(44)
            button.setStyleSheet(button.styleSheet() + """
                QPushButton {
                    font-size: 15px;
                    padding: 12px 20px;
                    margin: 4px;
                }
            """)
    
    def _adapt_input_field(self, input_field: QLineEdit, width: int):
        """Adapt input field styling for different screen sizes"""
        if width <= 576:  # Mobile
            input_field.setStyleSheet(input_field.styleSheet() + """
                QLineEdit {
                    font-size: 18px;
                    padding: 16px;
                    min-height: 48px;
                }
            """)
        else:
            input_field.setStyleSheet(input_field.styleSheet() + """
                QLineEdit {
                    font-size: 16px;
                    padding: 12px 16px;
                    min-height: 44px;
                }
            """)
    
    def _adapt_text_area(self, text_area: QTextEdit, width: int):
        """Adapt text area styling for different screen sizes"""
        if width <= 576:  # Mobile
            text_area.setStyleSheet(text_area.styleSheet() + """
                QTextEdit {
                    font-size: 16px;
                    line-height: 1.5;
                    padding: 16px;
                }
            """)
        else:
            text_area.setStyleSheet(text_area.styleSheet() + """
                QTextEdit {
                    font-size: 15px;
                    line-height: 1.6;
                    padding: 16px;
                }
            """)
    
    def _adapt_label(self, label: QLabel, width: int):
        """Adapt label typography for different screen sizes"""
        role = label.property('role') or 'body'
        
        font_sizes = {
            'xs': {'display': 28, 'title': 18, 'subtitle': 16, 'body': 14, 'caption': 12},
            'sm': {'display': 32, 'title': 20, 'subtitle': 17, 'body': 15, 'caption': 13},
            'md': {'display': 36, 'title': 24, 'subtitle': 18, 'body': 16, 'caption': 14},
            'lg': {'display': 42, 'title': 28, 'subtitle': 20, 'body': 17, 'caption': 15},
            'xl': {'display': 48, 'title': 32, 'subtitle': 22, 'body': 18, 'caption': 16}
        }
        
        # Determine breakpoint
        if width <= 576:
            bp = 'xs'
        elif width <= 768:
            bp = 'sm'
        elif width <= 992:
            bp = 'md'
        elif width <= 1200:
            bp = 'lg'
        else:
            bp = 'xl'
        
        font_size = font_sizes[bp].get(role, font_sizes[bp]['body'])
        
        font = label.font()
        font.setPointSize(font_size)
        label.setFont(font)
    
    def _adapt_group_box(self, group_box: QGroupBox, width: int):
        """Adapt group box styling for different screen sizes"""
        if width <= 576:  # Mobile
            group_box.setStyleSheet(group_box.styleSheet() + """
                QGroupBox {
                    margin: 4px 0;
                    padding: 16px;
                }
            """)
        else:
            group_box.setStyleSheet(group_box.styleSheet() + """
                QGroupBox {
                    margin: 8px 0;
                    padding: 20px;
                }
            """)
    
    def _apply_modern_styling(self):
        """Apply modern styling to the entire application"""
        if self.theme_manager:
            self.theme_manager.apply_theme('light')
        else:
            # Apply basic modern styling
            self._apply_basic_modern_styling()
    
    def _apply_basic_modern_styling(self):
        """Apply basic modern styling as fallback"""
        app = QApplication.instance()
        if app:
            app.setStyleSheet("""
                QMainWindow {
                    background-color: #f9fafb;
                    font-family: 'Segoe UI', 'SF Pro Display', -apple-system, sans-serif;
                }
                
                QWidget {
                    font-family: 'Segoe UI', 'SF Pro Display', -apple-system, sans-serif;
                    background-color: transparent;
                }
            """)
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        if self.theme_manager:
            self.theme_manager.toggle_theme()
            current_theme = self.theme_manager.get_current_theme()
            logger.info(f"Switched to {current_theme} theme")
            return current_theme
        return 'light'
    
    def get_current_theme(self) -> str:
        """Get the current theme"""
        if self.theme_manager:
            return self.theme_manager.get_current_theme()
        return 'light'
    
    def set_theme(self, theme: str):
        """Set a specific theme"""
        if self.theme_manager:
            self.theme_manager.apply_theme(theme)
            logger.info(f"Applied {theme} theme")


def integrate_responsive_design(main_window) -> ResponsiveSpanishApp:
    """
    Integrate responsive design with an existing Spanish Subjunctive Practice application
    
    Args:
        main_window: The existing main window instance
    
    Returns:
        ResponsiveSpanishApp: Enhanced app instance with responsive design
    """
    try:
        # Create the responsive app wrapper
        responsive_app = ResponsiveSpanishApp(main_window)
        
        # Enhance the existing UI
        responsive_app.enhance_existing_ui()
        
        logger.info("Successfully integrated responsive design with existing application")
        
        return responsive_app
        
    except Exception as e:
        logger.error(f"Failed to integrate responsive design: {e}")
        # Return a minimal responsive app that won't break existing functionality
        return ResponsiveSpanishApp(main_window)


# Utility functions for easy integration with main.py
def apply_responsive_enhancements(app_instance):
    """
    Apply responsive enhancements to an existing app instance
    This can be called from main.py after the UI is initialized
    
    Args:
        app_instance: The SpanishSubjunctivePracticeGUI instance
    """
    try:
        # Integrate responsive design
        responsive_app = integrate_responsive_design(app_instance)
        
        # Store reference in the app instance
        app_instance.responsive_app = responsive_app
        
        # Add toggle theme method to toolbar if it exists
        if hasattr(app_instance, 'createToolBar'):
            _add_responsive_toolbar_actions(app_instance)
        
        logger.info("Applied responsive enhancements to existing app")
        
        return responsive_app
        
    except Exception as e:
        logger.error(f"Error applying responsive enhancements: {e}")
        return None


def _add_responsive_toolbar_actions(app_instance):
    """Add responsive design actions to the toolbar"""
    try:
        from PyQt5.QtWidgets import QAction
        
        # Find the toolbar
        toolbars = app_instance.findChildren(QToolBar)
        if not toolbars:
            return
        
        toolbar = toolbars[0]
        
        # Add theme toggle action
        theme_action = QAction("🌓 Toggle Theme", app_instance)
        theme_action.setToolTip("Toggle between light and dark themes")
        
        def toggle_theme_action():
            if hasattr(app_instance, 'responsive_app'):
                theme = app_instance.responsive_app.toggle_theme()
                app_instance.updateStatus(f"Switched to {theme} theme")
        
        theme_action.triggered.connect(toggle_theme_action)
        toolbar.addAction(theme_action)
        
        logger.info("Added responsive design actions to toolbar")
        
    except Exception as e:
        logger.error(f"Error adding responsive toolbar actions: {e}")


if __name__ == "__main__":
    # Demo integration with a mock main window
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
    
    app = QApplication(sys.argv)
    
    # Create a mock main window similar to the Spanish practice app
    window = QMainWindow()
    central = QWidget()
    window.setCentralWidget(central)
    
    layout = QVBoxLayout(central)
    
    # Add mock content
    title = QLabel("Spanish Subjunctive Practice")
    title.setObjectName("sentence_label")
    
    content = QLabel("This is a mock exercise sentence that would appear here.")
    content.setObjectName("exercise_content")
    
    input_field = QLineEdit()
    input_field.setPlaceholderText("Type your answer here...")
    
    submit_btn = QPushButton("Submit Answer")
    hint_btn = QPushButton("Show Hint")
    
    layout.addWidget(title)
    layout.addWidget(content)
    layout.addWidget(input_field)
    layout.addWidget(submit_btn)
    layout.addWidget(hint_btn)
    
    # Integrate responsive design
    responsive_app = integrate_responsive_design(window)
    
    window.setWindowTitle("Responsive Design Integration Demo")
    window.resize(1000, 700)
    window.show()
    
    print("Responsive design integration demo running...")
    print(f"Current theme: {responsive_app.get_current_theme()}")
    print(f"Number of responsive components: {len(responsive_app.responsive_components)}")
    
    sys.exit(app.exec_())

"""
Enhanced Responsive Layout System for Spanish Subjunctive Practice
================================================================

This module provides advanced responsive layout components that work
seamlessly with the existing application architecture while providing
modern, adaptive user interfaces.

Features:
- Responsive grid system based on CSS Grid principles
- Adaptive containers that resize intelligently
- Modern card-based layouts with proper elevation
- Collapsible sections for space efficiency
- Touch-friendly interactions
- Smooth animations and transitions
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QSplitter,
    QScrollArea, QGroupBox, QLabel, QPushButton, QFrame,
    QSizePolicy, QSpacerItem, QStackedWidget, QTabWidget
)
from PyQt5.QtCore import (
    Qt, QSize, QTimer, pyqtSignal, QPropertyAnimation, 
    QEasingCurve, QParallelAnimationGroup, QSequentialAnimationGroup
)
from PyQt5.QtGui import QFont, QFontMetrics, QIcon
from typing import Dict, List, Tuple, Optional, Union, Any
import logging

logger = logging.getLogger(__name__)


class ResponsiveCard(QGroupBox):
    """
    A modern card component with responsive behavior and smooth animations
    """
    
    def __init__(self, title: str = "", collapsible: bool = False, parent=None):
        super().__init__(title, parent)
        self.collapsible = collapsible
        self.collapsed = False
        self._content_widget = None
        self._animation = None
        
        self.setup_ui()
        
        if self.collapsible:
            self.setup_collapse_functionality()
    
    def setup_ui(self):
        """Setup the card UI with modern styling"""
        self.setStyleSheet("""
            QGroupBox {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 20px;
                margin: 8px 0;
                font-weight: 500;
                font-size: 16px;
                color: #2d3748;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 16px;
                top: -12px;
                padding: 0 8px;
                background-color: #ffffff;
                color: #4a5568;
                font-weight: 600;
            }
        """)
        
        # Create content area
        self._content_widget = QWidget()
        self._layout = QVBoxLayout(self._content_widget)
        self._layout.setContentsMargins(0, 0, 0, 0)
        
        # Main layout for the card
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self._content_widget)
    
    def setup_collapse_functionality(self):
        """Setup collapsible functionality with smooth animation"""
        if not self.title():
            return
            
        # Create toggle button in title
        self.toggle_button = QPushButton("▼")
        self.toggle_button.setFixedSize(24, 24)
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                font-weight: bold;
                font-size: 12px;
                color: #718096;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #edf2f7;
                color: #4a5568;
            }
        """)
        self.toggle_button.clicked.connect(self.toggle_collapse)
        
        # Position toggle button (this is a limitation in PyQt5 - we'll use a workaround)
        self.setTitle(f"{self.title()} ")
    
    def add_content(self, widget: QWidget):
        """Add content to the card"""
        self._layout.addWidget(widget)
    
    def add_content_layout(self, layout):
        """Add a layout as content"""
        self._layout.addLayout(layout)
    
    def toggle_collapse(self):
        """Toggle the collapsed state with animation"""
        if not self.collapsible:
            return
            
        self.collapsed = not self.collapsed
        
        # Update button text
        if hasattr(self, 'toggle_button'):
            self.toggle_button.setText("▲" if self.collapsed else "▼")
        
        # Animate the collapse/expand
        self._animate_collapse()
    
    def _animate_collapse(self):
        """Animate the collapse/expand transition"""
        if self._animation:
            self._animation.stop()
        
        start_height = self._content_widget.height()
        end_height = 0 if self.collapsed else self._content_widget.sizeHint().height()
        
        self._animation = QPropertyAnimation(self._content_widget, b"maximumHeight")
        self._animation.setDuration(250)
        self._animation.setStartValue(start_height)
        self._animation.setEndValue(end_height)
        self._animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        if self.collapsed:
            self._animation.finished.connect(
                lambda: self._content_widget.setVisible(False)
            )
        else:
            self._content_widget.setVisible(True)
        
        self._animation.start()
    
    def set_variant(self, variant: str):
        """Set visual variant of the card"""
        if variant == "elevated":
            self.setStyleSheet(self.styleSheet() + """
                QGroupBox {
                    border: none;
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                              stop:0 #ffffff, stop:1 #fafafa);
                }
            """)
        elif variant == "outlined":
            self.setStyleSheet(self.styleSheet() + """
                QGroupBox {
                    border: 2px solid #e2e8f0;
                    background-color: transparent;
                }
            """)
        elif variant == "filled":
            self.setStyleSheet(self.styleSheet() + """
                QGroupBox {
                    border: none;
                    background-color: #f7fafc;
                }
            """)


class ResponsiveGrid(QWidget):
    """
    A responsive grid layout that adapts to different screen sizes
    """
    
    def __init__(self, columns: int = 2, parent=None):
        super().__init__(parent)
        self.default_columns = columns
        self.current_columns = columns
        self.items = []
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the grid layout"""
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(16)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
    
    def add_item(self, widget: QWidget, stretch: int = 1):
        """Add an item to the grid"""
        self.items.append({'widget': widget, 'stretch': stretch})
        self._relayout_items()
    
    def _relayout_items(self):
        """Re-layout all items based on current column count"""
        # Clear current layout
        for i in reversed(range(self.grid_layout.count())):
            item = self.grid_layout.takeAt(i)
            if item.widget():
                item.widget().setParent(None)
        
        # Re-add items in grid formation
        for index, item in enumerate(self.items):
            row = index // self.current_columns
            col = index % self.current_columns
            
            self.grid_layout.addWidget(
                item['widget'], 
                row, 
                col, 
                1, 
                item['stretch']
            )
    
    def set_columns(self, columns: int):
        """Set the number of columns and re-layout"""
        if columns != self.current_columns:
            self.current_columns = columns
            self._relayout_items()
    
    def adapt_to_width(self, width: int):
        """Adapt grid columns based on available width"""
        # Simple responsive logic
        if width < 600:
            new_columns = 1
        elif width < 900:
            new_columns = 2
        elif width < 1200:
            new_columns = 3
        else:
            new_columns = self.default_columns
        
        self.set_columns(new_columns)


class AdaptiveSplitter(QSplitter):
    """
    An enhanced splitter that adapts its orientation and behavior responsively
    """
    
    orientationChanged = pyqtSignal(Qt.Orientation)
    
    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super().__init__(orientation, parent)
        self.default_orientation = orientation
        self.mobile_threshold = 768
        self.tablet_threshold = 1024
        
        self.setup_styling()
    
    def setup_styling(self):
        """Setup modern splitter styling"""
        self.setStyleSheet("""
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
                background-color: #3182ce;
            }
        """)
        
        # Enable child widgets to be collapsed
        self.setChildrenCollapsible(True)
    
    def adapt_to_width(self, width: int):
        """Adapt splitter behavior based on width"""
        if width <= self.mobile_threshold:
            # Stack vertically on mobile
            new_orientation = Qt.Vertical
            self.setSizes([60, 40])  # Primary content gets more space
        elif width <= self.tablet_threshold:
            # Balanced layout on tablet
            new_orientation = self.default_orientation
            if new_orientation == Qt.Horizontal:
                self.setSizes([55, 45])
            else:
                self.setSizes([60, 40])
        else:
            # Desktop layout
            new_orientation = self.default_orientation
            if new_orientation == Qt.Horizontal:
                self.setSizes([70, 30])
            else:
                self.setSizes([65, 35])
        
        if self.orientation() != new_orientation:
            self.setOrientation(new_orientation)
            self.orientationChanged.emit(new_orientation)


class ResponsiveContainer(QScrollArea):
    """
    A responsive container that manages content overflow and spacing
    """
    
    def __init__(self, max_width: int = None, parent=None):
        super().__init__(parent)
        self.max_content_width = max_width
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the responsive container"""
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setFrameShape(QFrame.NoFrame)
        
        # Create content widget
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        
        self.setWidget(self.content_widget)
        
        # Setup responsive margins
        self.update_margins()
    
    def add_widget(self, widget: QWidget):
        """Add a widget to the container"""
        self.content_layout.addWidget(widget)
    
    def add_layout(self, layout):
        """Add a layout to the container"""
        self.content_layout.addLayout(layout)
    
    def update_margins(self):
        """Update margins based on container width"""
        if self.max_content_width and self.width() > self.max_content_width:
            # Center content with side margins
            side_margin = (self.width() - self.max_content_width) // 2
            self.content_layout.setContentsMargins(
                side_margin, 20, side_margin, 20
            )
        else:
            # Full width with standard margins
            width = self.width()
            if width < 600:
                margin = 16
            elif width < 900:
                margin = 20
            else:
                margin = 24
            
            self.content_layout.setContentsMargins(
                margin, margin, margin, margin
            )
    
    def resizeEvent(self, event):
        """Handle resize events to update margins"""
        super().resizeEvent(event)
        self.update_margins()


class ModernTabWidget(QTabWidget):
    """
    A modern tab widget with responsive behavior
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_styling()
    
    def setup_styling(self):
        """Setup modern tab styling"""
        self.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background-color: #ffffff;
                margin-top: -1px;
            }
            
            QTabWidget::tab-bar {
                alignment: left;
            }
            
            QTabBar::tab {
                background-color: transparent;
                color: #718096;
                border: none;
                border-bottom: 3px solid transparent;
                padding: 12px 20px;
                margin-right: 4px;
                font-weight: 500;
                font-size: 14px;
                min-width: 80px;
            }
            
            QTabBar::tab:selected {
                color: #3182ce;
                border-bottom-color: #3182ce;
                background-color: rgba(49, 130, 206, 0.05);
            }
            
            QTabBar::tab:hover:!selected {
                color: #4a5568;
                background-color: #f7fafc;
            }
        """)
        
        # Set tab position
        self.setTabPosition(QTabWidget.North)
    
    def adapt_to_width(self, width: int):
        """Adapt tab display based on width"""
        if width < 600:
            # Consider stacking tabs or using a different approach
            # For now, just ensure they fit
            self.tabBar().setExpanding(True)
        else:
            self.tabBar().setExpanding(False)


class ResponsiveForm(QWidget):
    """
    A responsive form layout that adapts field arrangements
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.form_items = []
        self.current_layout_mode = 'vertical'
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the form layout"""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(16)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
    
    def add_field(self, label: str, widget: QWidget, inline: bool = False):
        """Add a field to the form"""
        form_item = {
            'label': QLabel(label),
            'widget': widget,
            'inline': inline,
            'container': None
        }
        
        # Style the label
        form_item['label'].setStyleSheet("""
            QLabel {
                font-weight: 500;
                color: #374151;
                margin-bottom: 6px;
            }
        """)
        
        self.form_items.append(form_item)
        self._relayout_form()
    
    def _relayout_form(self):
        """Re-layout the form based on current mode"""
        # Clear current layout
        for item in self.form_items:
            if item['container']:
                item['container'].setParent(None)
        
        # Re-add items based on layout mode
        for item in self.form_items:
            if self.current_layout_mode == 'horizontal' and not item['inline']:
                # Create horizontal container for label and widget
                container = QWidget()
                layout = QHBoxLayout(container)
                layout.setContentsMargins(0, 0, 0, 0)
                
                # Set label width for alignment
                item['label'].setFixedWidth(120)
                
                layout.addWidget(item['label'])
                layout.addWidget(item['widget'], 1)
                
                item['container'] = container
                self.main_layout.addWidget(container)
            else:
                # Vertical layout
                container = QWidget()
                layout = QVBoxLayout(container)
                layout.setContentsMargins(0, 0, 0, 0)
                
                item['label'].setFixedWidth(16777215)  # Reset width
                
                layout.addWidget(item['label'])
                layout.addWidget(item['widget'])
                
                item['container'] = container
                self.main_layout.addWidget(container)
    
    def adapt_to_width(self, width: int):
        """Adapt form layout based on width"""
        new_mode = 'horizontal' if width > 800 else 'vertical'
        
        if new_mode != self.current_layout_mode:
            self.current_layout_mode = new_mode
            self._relayout_form()


class ResponsiveLayoutManager(QWidget):
    """
    Main layout manager that orchestrates responsive behavior
    """
    
    resized = pyqtSignal(QSize)
    breakpointChanged = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.responsive_components = []
        self.current_breakpoint = 'lg'
        self.breakpoints = {
            'xs': 0,
            'sm': 576, 
            'md': 768,
            'lg': 992,
            'xl': 1200,
            'xxl': 1400
        }
        
        # Debounce timer for resize events
        self.resize_timer = QTimer()
        self.resize_timer.timeout.connect(self._handle_resize)
        self.resize_timer.setSingleShot(True)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the main responsive layout"""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
    
    def add_responsive_component(self, component):
        """Add a responsive component to be managed"""
        self.responsive_components.append(component)
    
    def get_current_breakpoint(self, width: int) -> str:
        """Get current breakpoint based on width"""
        for bp_name in ['xxl', 'xl', 'lg', 'md', 'sm', 'xs']:
            if width >= self.breakpoints[bp_name]:
                return bp_name
        return 'xs'
    
    def schedule_resize(self, size: QSize):
        """Schedule a resize operation with debouncing"""
        self.pending_size = size
        self.resize_timer.start(100)
    
    def _handle_resize(self):
        """Handle the resize operation"""
        if not hasattr(self, 'pending_size'):
            return
        
        width = self.pending_size.width()
        new_breakpoint = self.get_current_breakpoint(width)
        
        # Update all responsive components
        for component in self.responsive_components:
            if hasattr(component, 'adapt_to_width'):
                try:
                    component.adapt_to_width(width)
                except Exception as e:
                    logger.error(f"Error adapting component {component}: {e}")
        
        # Emit signals if breakpoint changed
        if new_breakpoint != self.current_breakpoint:
            self.current_breakpoint = new_breakpoint
            self.breakpointChanged.emit(new_breakpoint)
            logger.info(f"Breakpoint changed to: {new_breakpoint}")
        
        self.resized.emit(self.pending_size)
    
    def resizeEvent(self, event):
        """Handle widget resize events"""
        super().resizeEvent(event)
        self.schedule_resize(event.size())


def create_responsive_layout_for_app(parent_widget: QWidget) -> ResponsiveLayoutManager:
    """
    Create and configure a responsive layout system for the Spanish practice app
    
    Args:
        parent_widget: The parent widget (usually the main window's central widget)
    
    Returns:
        ResponsiveLayoutManager: Configured layout manager
    """
    # Create the main responsive layout manager
    layout_manager = ResponsiveLayoutManager(parent_widget)
    
    # Create main content splitter
    main_splitter = AdaptiveSplitter(Qt.Horizontal)
    layout_manager.main_layout.addWidget(main_splitter)
    layout_manager.add_responsive_component(main_splitter)
    
    # Left panel - Exercise content
    left_panel = ResponsiveContainer(max_width=800)
    
    # Exercise display card
    exercise_card = ResponsiveCard("Current Exercise")
    exercise_card.set_variant("elevated")
    left_panel.add_widget(exercise_card)
    
    # Context card (collapsible)
    context_card = ResponsiveCard("Context & Scenario", collapsible=True)
    left_panel.add_widget(context_card)
    
    # Add left panel to splitter
    main_splitter.addWidget(left_panel)
    
    # Right panel - Controls and settings
    right_panel = ResponsiveContainer(max_width=400)
    
    # Settings form
    settings_form = ResponsiveForm()
    settings_card = ResponsiveCard("Settings")
    settings_card.add_content(settings_form)
    right_panel.add_widget(settings_card)
    
    # Add responsive components
    layout_manager.add_responsive_component(left_panel)
    layout_manager.add_responsive_component(right_panel)
    layout_manager.add_responsive_component(settings_form)
    
    # Feedback section with tabs
    feedback_tabs = ModernTabWidget()
    feedback_tabs.addTab(QLabel("Explanation"), "Explanation")
    feedback_tabs.addTab(QLabel("Grammar Rules"), "Rules")
    feedback_tabs.addTab(QLabel("Examples"), "Examples")
    layout_manager.add_responsive_component(feedback_tabs)
    
    feedback_card = ResponsiveCard("Feedback")
    feedback_card.add_content(feedback_tabs)
    right_panel.add_widget(feedback_card)
    
    # Add right panel to splitter
    main_splitter.addWidget(right_panel)
    
    # Set initial splitter sizes
    main_splitter.setSizes([700, 300])
    
    logger.info("Created responsive layout system for Spanish practice app")
    
    return layout_manager


if __name__ == "__main__":
    # Demo the responsive layout system
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow
    
    app = QApplication(sys.argv)
    
    # Create main window
    window = QMainWindow()
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    
    # Create responsive layout
    layout_manager = create_responsive_layout_for_app(central_widget)
    
    # Set up the layout
    main_layout = QVBoxLayout(central_widget)
    main_layout.addWidget(layout_manager)
    
    window.setWindowTitle("Enhanced Responsive Layout Demo")
    window.resize(1200, 800)
    window.show()
    
    print("Enhanced responsive layout demo running...")
    print(f"Current breakpoint: {layout_manager.current_breakpoint}")
    
    sys.exit(app.exec_())

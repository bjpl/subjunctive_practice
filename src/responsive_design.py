"""
Responsive Design Module for Spanish Subjunctive Practice
=========================================================

This module provides responsive design capabilities to ensure the application
works well across different window sizes and screen resolutions while
maintaining educational effectiveness.

Features:
- Dynamic layout adjustments based on window size
- Adaptive font sizes and spacing
- Collapsible sections for small screens
- Optimized content density
- Accessibility considerations
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QScrollArea,
    QSizePolicy, QSpacerItem, QFrame
)
from PyQt5.QtCore import Qt, QSize, QTimer, pyqtSignal, QRect
from PyQt5.QtGui import QFont, QFontMetrics, QScreen
from typing import Dict, List, Tuple, Optional
import logging


class ResponsiveManager:
    """
    Manages responsive behavior for the subjunctive practice application.
    Handles dynamic layout adjustments based on window size and screen resolution.
    """
    
    # Breakpoints for different layouts (width in pixels)
    BREAKPOINTS = {
        'mobile': 480,      # Very small screens (phones)
        'tablet': 768,      # Small tablets
        'small': 1024,      # Small desktops/large tablets
        'medium': 1280,     # Medium desktops
        'large': 1600,      # Large desktops
        'xlarge': 1920      # Extra large desktops
    }
    
    def __init__(self, widget: QWidget):
        self.widget = widget
        self.current_breakpoint = 'medium'
        self.previous_size = QSize()
        
        # Timer for debounced resize events
        self.resize_timer = QTimer()
        self.resize_timer.timeout.connect(self._handle_resize)
        self.resize_timer.setSingleShot(True)
        
        # Default configurations for each breakpoint
        self.configurations = self._initialize_configurations()
        
    def _initialize_configurations(self) -> Dict:
        """Initialize responsive configurations for different breakpoints"""
        return {
            'mobile': {
                'splitter_orientation': Qt.Vertical,
                'splitter_ratios': [60, 40],  # Content first, then controls
                'font_size_base': 12,
                'spacing': 4,
                'margins': (5, 5, 5, 5),
                'collapse_triggers': True,
                'collapse_verbs': True,
                'collapse_advanced': True,
                'compact_buttons': True,
                'show_icons': False
            },
            'tablet': {
                'splitter_orientation': Qt.Vertical,
                'splitter_ratios': [65, 35],
                'font_size_base': 13,
                'spacing': 6,
                'margins': (6, 6, 6, 6),
                'collapse_triggers': True,
                'collapse_verbs': True,
                'collapse_advanced': False,
                'compact_buttons': True,
                'show_icons': True
            },
            'small': {
                'splitter_orientation': Qt.Horizontal,
                'splitter_ratios': [70, 30],
                'font_size_base': 14,
                'spacing': 8,
                'margins': (8, 8, 8, 8),
                'collapse_triggers': True,
                'collapse_verbs': True,
                'collapse_advanced': False,
                'compact_buttons': False,
                'show_icons': True
            },
            'medium': {
                'splitter_orientation': Qt.Horizontal,
                'splitter_ratios': [70, 30],
                'font_size_base': 14,
                'spacing': 8,
                'margins': (10, 10, 10, 10),
                'collapse_triggers': False,
                'collapse_verbs': True,
                'collapse_advanced': False,
                'compact_buttons': False,
                'show_icons': True
            },
            'large': {
                'splitter_orientation': Qt.Horizontal,
                'splitter_ratios': [75, 25],
                'font_size_base': 15,
                'spacing': 10,
                'margins': (12, 12, 12, 12),
                'collapse_triggers': False,
                'collapse_verbs': False,
                'collapse_advanced': False,
                'compact_buttons': False,
                'show_icons': True
            },
            'xlarge': {
                'splitter_orientation': Qt.Horizontal,
                'splitter_ratios': [75, 25],
                'font_size_base': 16,
                'spacing': 12,
                'margins': (15, 15, 15, 15),
                'collapse_triggers': False,
                'collapse_verbs': False,
                'collapse_advanced': False,
                'compact_buttons': False,
                'show_icons': True
            }
        }
        
    def get_current_breakpoint(self, width: int) -> str:
        """Determine current breakpoint based on width"""
        if width <= self.BREAKPOINTS['mobile']:
            return 'mobile'
        elif width <= self.BREAKPOINTS['tablet']:
            return 'tablet'
        elif width <= self.BREAKPOINTS['small']:
            return 'small'
        elif width <= self.BREAKPOINTS['medium']:
            return 'medium'
        elif width <= self.BREAKPOINTS['large']:
            return 'large'
        else:
            return 'xlarge'
            
    def schedule_resize(self, size: QSize):
        """Schedule a resize operation (debounced)"""
        self.new_size = size
        self.resize_timer.start(150)  # 150ms delay
        
    def _handle_resize(self):
        """Handle the actual resize operation"""
        if hasattr(self, 'new_size'):
            self.apply_responsive_layout(self.new_size)
            
    def apply_responsive_layout(self, size: QSize):
        """Apply responsive layout based on current size"""
        width = size.width()
        height = size.height()
        
        # Determine breakpoint
        new_breakpoint = self.get_current_breakpoint(width)
        
        # Only apply changes if breakpoint changed or significant size change
        if (new_breakpoint != self.current_breakpoint or 
            abs(size.width() - self.previous_size.width()) > 50 or
            abs(size.height() - self.previous_size.height()) > 50):
            
            logging.info(f"Applying responsive layout: {new_breakpoint} ({width}x{height})")
            
            config = self.configurations[new_breakpoint]
            self._apply_configuration(config)
            
            self.current_breakpoint = new_breakpoint
            self.previous_size = size
            
    def _apply_configuration(self, config: Dict):
        """Apply a specific configuration to the widget"""
        try:
            # Apply font size changes
            self._update_font_sizes(config['font_size_base'])
            
            # Apply spacing and margins
            self._update_spacing_and_margins(config)
            
            # Apply layout-specific changes
            if hasattr(self.widget, 'main_splitter'):
                self._update_splitter_layout(config)
                
            # Apply collapsible section states
            self._update_collapsible_sections(config)
            
            # Apply button configurations
            self._update_button_configurations(config)
            
        except Exception as e:
            logging.error(f"Error applying responsive configuration: {e}")
            
    def _update_font_sizes(self, base_size: int):
        """Update font sizes throughout the application"""
        # Calculate font sizes for different elements
        font_sizes = {
            'title': base_size + 2,
            'body': base_size,
            'small': base_size - 1,
            'button': base_size,
            'input': base_size
        }
        
        # Apply font sizes to different widget types
        self._apply_font_to_widgets(self.widget, font_sizes)
        
    def _apply_font_to_widgets(self, widget: QWidget, font_sizes: Dict):
        """Recursively apply font sizes to widgets"""
        try:
            # Determine appropriate font size based on widget type
            widget_type = type(widget).__name__
            
            font_size = font_sizes.get('body')  # default
            
            if 'Label' in widget_type:
                if hasattr(widget, 'title') or 'title' in widget.objectName().lower():
                    font_size = font_sizes.get('title')
                else:
                    font_size = font_sizes.get('body')
            elif 'Button' in widget_type:
                font_size = font_sizes.get('button')
            elif any(x in widget_type for x in ['LineEdit', 'TextEdit', 'ComboBox']):
                font_size = font_sizes.get('input')
            elif any(x in widget_type for x in ['CheckBox', 'RadioButton']):
                font_size = font_sizes.get('small')
                
            if font_size:
                font = widget.font()
                font.setPointSize(font_size)
                widget.setFont(font)
                
            # Recursively apply to children
            for child in widget.findChildren(QWidget):
                if child.parent() == widget:  # Only direct children
                    self._apply_font_to_widgets(child, font_sizes)
                    
        except Exception as e:
            logging.debug(f"Font application error for {widget}: {e}")
            
    def _update_spacing_and_margins(self, config: Dict):
        """Update spacing and margins in layouts"""
        spacing = config['spacing']
        margins = config['margins']
        
        self._apply_layout_properties(self.widget, spacing, margins)
        
    def _apply_layout_properties(self, widget: QWidget, spacing: int, margins: Tuple[int, int, int, int]):
        """Apply spacing and margin properties to layouts"""
        if hasattr(widget, 'layout') and widget.layout():
            layout = widget.layout()
            layout.setSpacing(spacing)
            layout.setContentsMargins(*margins)
            
        # Apply to child widgets
        for child in widget.findChildren(QWidget):
            if hasattr(child, 'layout') and child.layout():
                layout = child.layout()
                layout.setSpacing(max(spacing - 2, 2))  # Slightly smaller for nested layouts
                
    def _update_splitter_layout(self, config: Dict):
        """Update splitter orientation and ratios"""
        if hasattr(self.widget, 'main_splitter'):
            splitter = self.widget.main_splitter
            
            # Update orientation
            orientation = config['splitter_orientation']
            if splitter.orientation() != orientation:
                splitter.setOrientation(orientation)
                
            # Update ratios
            ratios = config['splitter_ratios']
            total_size = splitter.width() if orientation == Qt.Horizontal else splitter.height()
            sizes = [int(total_size * ratio / 100) for ratio in ratios]
            splitter.setSizes(sizes)
            
    def _update_collapsible_sections(self, config: Dict):
        """Update collapsible section states"""
        collapsible_configs = {
            'collapse_triggers': 'trigger_card',
            'collapse_verbs': 'verb_card',
            'collapse_advanced': 'advanced_card'
        }
        
        for config_key, widget_name in collapsible_configs.items():
            should_collapse = config.get(config_key, False)
            
            # Find the collapsible widget
            widget = self._find_widget_by_name(widget_name)
            if widget and hasattr(widget, 'collapsed'):
                if should_collapse != widget.collapsed:
                    widget._on_toggle(not should_collapse)
                    
    def _update_button_configurations(self, config: Dict):
        """Update button configurations"""
        compact_buttons = config.get('compact_buttons', False)
        show_icons = config.get('show_icons', True)
        
        # Find all buttons and update their appearance
        from PyQt5.QtWidgets import QPushButton
        buttons = self.widget.findChildren(QPushButton)
        
        for button in buttons:
            if compact_buttons:
                button.setStyleSheet(button.styleSheet() + """
                    QPushButton {
                        padding: 4px 8px;
                        min-width: 60px;
                    }
                """)
            else:
                button.setStyleSheet(button.styleSheet() + """
                    QPushButton {
                        padding: 8px 16px;
                        min-width: 80px;
                    }
                """)
                
    def _find_widget_by_name(self, name: str) -> Optional[QWidget]:
        """Find a widget by its object name"""
        return self.widget.findChild(QWidget, name)


class ResponsiveOptimizedLayout(QWidget):
    """
    An enhanced version of the optimized layout with responsive capabilities
    """
    
    resized = pyqtSignal(QSize)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Initialize responsive manager
        self.responsive_manager = ResponsiveManager(self)
        
        # Connect resize signal
        self.resized.connect(self.responsive_manager.schedule_resize)
        
        # Setup the base layout (this would be your OptimizedSubjunctiveLayout)
        self._setup_base_layout()
        
    def _setup_base_layout(self):
        """Setup the base responsive layout"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create main splitter
        self.main_splitter = QSplitter(Qt.Horizontal)
        self.main_splitter.setObjectName("main_splitter")
        
        # Content area
        self.content_area = self._create_responsive_content_area()
        self.control_area = self._create_responsive_control_area()
        
        self.main_splitter.addWidget(self.content_area)
        self.main_splitter.addWidget(self.control_area)
        
        # Set initial sizes
        self.main_splitter.setSizes([700, 300])
        self.main_splitter.setStretchFactor(0, 7)
        self.main_splitter.setStretchFactor(1, 3)
        
        main_layout.addWidget(self.main_splitter)
        
        # Apply initial responsive layout
        QTimer.singleShot(100, self._apply_initial_layout)
        
    def _create_responsive_content_area(self) -> QWidget:
        """Create content area with responsive design considerations"""
        content_widget = QWidget()
        content_widget.setObjectName("content_area")
        
        layout = QVBoxLayout(content_widget)
        layout.setObjectName("content_layout")
        
        # Exercise display (responsive)
        from .optimized_layout import InformationCard
        self.exercise_card = InformationCard("Current Exercise")
        self.exercise_card.setObjectName("exercise_card")
        
        # Add responsive text that scales
        from PyQt5.QtWidgets import QLabel
        self.exercise_label = QLabel("Exercise content will appear here")
        self.exercise_label.setWordWrap(True)
        self.exercise_label.setObjectName("exercise_label")
        self.exercise_card.add_widget(self.exercise_label)
        
        layout.addWidget(self.exercise_card)
        
        # Add responsive progress section
        self.progress_card = InformationCard("Progress")
        self.progress_card.setObjectName("progress_card")
        layout.addWidget(self.progress_card)
        
        return content_widget
        
    def _create_responsive_control_area(self) -> QWidget:
        """Create control area with responsive design"""
        control_widget = QWidget()
        control_widget.setObjectName("control_area")
        
        layout = QVBoxLayout(control_widget)
        layout.setObjectName("control_layout")
        
        # Add collapsible sections
        from .optimized_layout import CollapsibleCard
        
        self.settings_card = CollapsibleCard("Settings")
        self.settings_card.setObjectName("settings_card")
        layout.addWidget(self.settings_card)
        
        self.trigger_card = CollapsibleCard("Triggers", collapsed=True)
        self.trigger_card.setObjectName("trigger_card")
        layout.addWidget(self.trigger_card)
        
        self.verb_card = CollapsibleCard("Specific Verbs", collapsed=True)
        self.verb_card.setObjectName("verb_card")
        layout.addWidget(self.verb_card)
        
        layout.addStretch()
        return control_widget
        
    def _apply_initial_layout(self):
        """Apply initial responsive layout based on current size"""
        self.responsive_manager.apply_responsive_layout(self.size())
        
    def resizeEvent(self, event):
        """Handle resize events"""
        super().resizeEvent(event)
        self.resized.emit(event.size())
        
    def get_optimal_size_for_content(self, content_length: int) -> QSize:
        """Calculate optimal size based on content length"""
        base_width = 1000
        base_height = 700
        
        # Adjust based on content length
        if content_length > 500:  # Long content
            base_width = 1200
            base_height = 800
        elif content_length < 200:  # Short content
            base_width = 900
            base_height = 600
            
        return QSize(base_width, base_height)
        
    def adapt_to_screen_dpi(self, dpi: float):
        """Adapt layout to screen DPI"""
        if dpi > 120:  # High DPI screen
            scale_factor = dpi / 96.0  # Standard DPI is 96
            
            # Scale fonts
            for widget in self.findChildren(QWidget):
                font = widget.font()
                current_size = font.pointSize()
                if current_size > 0:
                    font.setPointSize(int(current_size * scale_factor))
                    widget.setFont(font)
                    
            # Scale spacing
            for layout in self.findChildren(QVBoxLayout) + self.findChildren(QHBoxLayout):
                current_spacing = layout.spacing()
                layout.setSpacing(int(current_spacing * scale_factor))


def create_responsive_layout(parent=None) -> ResponsiveOptimizedLayout:
    """Factory function to create a responsive optimized layout"""
    layout = ResponsiveOptimizedLayout(parent)
    
    # Apply additional responsive enhancements
    layout.setMinimumSize(400, 300)  # Minimum usable size
    layout.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    
    return layout


def get_screen_info() -> Dict:
    """Get information about available screens"""
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication.instance()
    if not app:
        return {}
        
    screen_info = {}
    screens = app.screens()
    
    for i, screen in enumerate(screens):
        geometry = screen.geometry()
        screen_info[f'screen_{i}'] = {
            'size': (geometry.width(), geometry.height()),
            'dpi': screen.logicalDotsPerInch(),
            'device_pixel_ratio': screen.devicePixelRatio(),
            'name': screen.name(),
            'primary': screen == app.primaryScreen()
        }
        
    return screen_info


if __name__ == "__main__":
    # Demo of responsive design
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    # Show screen information
    screen_info = get_screen_info()
    print("Available screens:", screen_info)
    
    # Create responsive layout
    layout = create_responsive_layout()
    layout.setWindowTitle("Responsive Spanish Subjunctive Layout")
    layout.show()
    
    sys.exit(app.exec_())
"""
CSS Variables System and Micro-Interactions for PyQt5
====================================================

This module implements a CSS custom properties-like system for PyQt5,
allowing for consistent theming and easy style customization throughout
the application. It also includes smooth micro-interactions and transitions.

Features:
- CSS custom properties equivalent for PyQt5
- Dynamic theme switching with smooth transitions
- Micro-interactions and hover effects
- Performance-optimized style updates
- Cross-platform compatible animations
"""

from PyQt5.QtWidgets import (
    QWidget, QApplication, QLabel, QPushButton, QLineEdit, QTextEdit,
    QGroupBox, QProgressBar, QFrame, QGraphicsOpacityEffect
)
from PyQt5.QtCore import (
    QObject, QTimer, QPropertyAnimation, QEasingCurve, 
    QParallelAnimationGroup, QSequentialAnimationGroup, pyqtSignal,
    QAbstractAnimation, QVariantAnimation, Qt
)
from PyQt5.QtGui import QColor, QPalette, QFont
from typing import Dict, List, Tuple, Any, Optional, Union
import logging
import json
import math

logger = logging.getLogger(__name__)


class CSSVariableSystem:
    """
    A CSS custom properties-like system for PyQt5 applications
    Allows for centralized theme management and dynamic style updates
    """
    
    def __init__(self):
        self.variables = {}
        self.themes = {}
        self.current_theme = 'light'
        self.listeners = []  # Widgets that listen to variable changes
        
        self._initialize_default_variables()
        self._initialize_default_themes()
    
    def _initialize_default_variables(self):
        """Initialize default CSS variables"""
        self.variables = {
            # Color system
            '--color-primary': '#3b82f6',
            '--color-primary-light': '#93c5fd',
            '--color-primary-dark': '#1d4ed8',
            '--color-secondary': '#8b5cf6',
            '--color-accent': '#f59e0b',
            
            # Neutral colors
            '--color-white': '#ffffff',
            '--color-gray-50': '#f9fafb',
            '--color-gray-100': '#f3f4f6',
            '--color-gray-200': '#e5e7eb',
            '--color-gray-300': '#d1d5db',
            '--color-gray-400': '#9ca3af',
            '--color-gray-500': '#6b7280',
            '--color-gray-600': '#4b5563',
            '--color-gray-700': '#374151',
            '--color-gray-800': '#1f2937',
            '--color-gray-900': '#111827',
            
            # Semantic colors
            '--color-success': '#10b981',
            '--color-warning': '#f59e0b',
            '--color-error': '#ef4444',
            '--color-info': '#3b82f6',
            
            # Background colors
            '--bg-primary': '#ffffff',
            '--bg-secondary': '#f9fafb',
            '--bg-surface': '#ffffff',
            '--bg-overlay': 'rgba(0, 0, 0, 0.5)',
            
            # Text colors
            '--text-primary': '#111827',
            '--text-secondary': '#6b7280',
            '--text-muted': '#9ca3af',
            '--text-inverse': '#ffffff',
            
            # Border colors
            '--border-color': '#e5e7eb',
            '--border-focus': '#3b82f6',
            '--border-error': '#ef4444',
            
            # Typography
            '--font-family-sans': '"Inter", "SF Pro Display", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
            '--font-family-mono': '"JetBrains Mono", "SF Mono", Consolas, monospace',
            
            '--font-size-xs': '12px',
            '--font-size-sm': '14px',
            '--font-size-base': '16px',
            '--font-size-lg': '18px',
            '--font-size-xl': '20px',
            '--font-size-2xl': '24px',
            '--font-size-3xl': '30px',
            '--font-size-4xl': '36px',
            
            '--font-weight-normal': '400',
            '--font-weight-medium': '500',
            '--font-weight-semibold': '600',
            '--font-weight-bold': '700',
            
            '--line-height-tight': '1.25',
            '--line-height-normal': '1.5',
            '--line-height-relaxed': '1.625',
            
            # Spacing
            '--spacing-1': '4px',
            '--spacing-2': '8px',
            '--spacing-3': '12px',
            '--spacing-4': '16px',
            '--spacing-5': '20px',
            '--spacing-6': '24px',
            '--spacing-8': '32px',
            '--spacing-10': '40px',
            '--spacing-12': '48px',
            '--spacing-16': '64px',
            '--spacing-20': '80px',
            '--spacing-24': '96px',
            
            # Border radius
            '--radius-sm': '4px',
            '--radius-base': '6px',
            '--radius-md': '8px',
            '--radius-lg': '12px',
            '--radius-xl': '16px',
            '--radius-2xl': '24px',
            '--radius-full': '9999px',
            
            # Shadows
            '--shadow-sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
            '--shadow-base': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
            '--shadow-md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
            '--shadow-lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
            '--shadow-xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
            
            # Transitions
            '--transition-fast': '150ms',
            '--transition-normal': '250ms',
            '--transition-slow': '350ms',
            
            # Z-index
            '--z-dropdown': '1000',
            '--z-modal': '1050',
            '--z-tooltip': '1100',
        }
    
    def _initialize_default_themes(self):
        """Initialize default light and dark themes"""
        self.themes = {
            'light': {
                '--bg-primary': '#ffffff',
                '--bg-secondary': '#f9fafb',
                '--bg-surface': '#ffffff',
                '--text-primary': '#111827',
                '--text-secondary': '#6b7280',
                '--text-muted': '#9ca3af',
                '--border-color': '#e5e7eb',
            },
            'dark': {
                '--bg-primary': '#111827',
                '--bg-secondary': '#1f2937',
                '--bg-surface': '#374151',
                '--text-primary': '#f9fafb',
                '--text-secondary': '#d1d5db',
                '--text-muted': '#9ca3af',
                '--border-color': '#4b5563',
                '--color-primary': '#60a5fa',
                '--color-primary-light': '#93c5fd',
                '--color-primary-dark': '#3b82f6',
            },
            'high-contrast': {
                '--bg-primary': '#000000',
                '--bg-secondary': '#ffffff',
                '--text-primary': '#ffffff',
                '--text-secondary': '#ffffff',
                '--color-primary': '#00ff00',
                '--border-color': '#ffffff',
            }
        }
    
    def get_variable(self, name: str, fallback: str = None) -> str:
        """Get a CSS variable value"""
        return self.variables.get(name, fallback or '')
    
    def set_variable(self, name: str, value: str):
        """Set a CSS variable value and notify listeners"""
        old_value = self.variables.get(name)
        self.variables[name] = value
        
        if old_value != value:
            self._notify_variable_change(name, value, old_value)
    
    def set_variables(self, variables: Dict[str, str]):
        """Set multiple CSS variables at once"""
        changes = {}
        for name, value in variables.items():
            old_value = self.variables.get(name)
            self.variables[name] = value
            if old_value != value:
                changes[name] = {'new': value, 'old': old_value}
        
        if changes:
            self._notify_variables_change(changes)
    
    def apply_theme(self, theme_name: str):
        """Apply a theme by updating variables"""
        if theme_name not in self.themes:
            logger.warning(f"Theme '{theme_name}' not found")
            return False
        
        theme_variables = self.themes[theme_name]
        self.set_variables(theme_variables)
        self.current_theme = theme_name
        
        logger.info(f"Applied theme: {theme_name}")
        return True
    
    def create_theme(self, name: str, variables: Dict[str, str]):
        """Create a new theme"""
        self.themes[name] = variables.copy()
        logger.info(f"Created theme: {name}")
    
    def add_listener(self, widget, callback):
        """Add a widget listener for variable changes"""
        self.listeners.append({
            'widget': widget,
            'callback': callback
        })
    
    def remove_listener(self, widget):
        """Remove a widget listener"""
        self.listeners = [l for l in self.listeners if l['widget'] != widget]
    
    def _notify_variable_change(self, name: str, new_value: str, old_value: str):
        """Notify listeners of a variable change"""
        for listener in self.listeners:
            try:
                listener['callback'](name, new_value, old_value)
            except Exception as e:
                logger.error(f"Error notifying listener: {e}")
    
    def _notify_variables_change(self, changes: Dict[str, Dict[str, str]]):
        """Notify listeners of multiple variable changes"""
        for listener in self.listeners:
            try:
                listener['callback'](changes)
            except Exception as e:
                logger.error(f"Error notifying listener: {e}")
    
    def generate_stylesheet(self, template: str) -> str:
        """Generate a stylesheet by replacing CSS variable references"""
        stylesheet = template
        
        # Replace CSS variable references with actual values
        for var_name, var_value in self.variables.items():
            stylesheet = stylesheet.replace(f'var({var_name})', var_value)
        
        return stylesheet


class MicroInteractionManager:
    """
    Manages micro-interactions and smooth transitions for UI elements
    """
    
    def __init__(self):
        self.animations = {}
        self.animation_groups = {}
        
    def create_hover_effect(self, widget: QWidget, 
                           hover_properties: Dict[str, Any],
                           duration: int = 200) -> None:
        """Create a smooth hover effect for a widget"""
        
        def on_enter_event(event):
            self._animate_properties(widget, hover_properties, duration)
            # Call original event handler if it exists
            if hasattr(widget, '_original_enter_event'):
                widget._original_enter_event(event)
        
        def on_leave_event(event):
            # Animate back to original properties
            original_properties = getattr(widget, '_original_properties', {})
            if original_properties:
                self._animate_properties(widget, original_properties, duration)
            # Call original event handler if it exists
            if hasattr(widget, '_original_leave_event'):
                widget._original_leave_event(event)
        
        # Store original event handlers
        if hasattr(widget, 'enterEvent'):
            widget._original_enter_event = widget.enterEvent
        if hasattr(widget, 'leaveEvent'):
            widget._original_leave_event = widget.leaveEvent
        
        # Store original properties for restoration
        widget._original_properties = self._get_current_properties(widget, hover_properties.keys())
        
        # Set new event handlers
        widget.enterEvent = on_enter_event
        widget.leaveEvent = on_leave_event
    
    def create_press_effect(self, widget: QPushButton, 
                           press_properties: Dict[str, Any],
                           duration: int = 150) -> None:
        """Create a smooth press effect for a button"""
        
        def on_press_event(event):
            self._animate_properties(widget, press_properties, duration // 2)
            # Call original event handler if it exists
            if hasattr(widget, '_original_press_event'):
                widget._original_press_event(event)
        
        def on_release_event(event):
            # Animate back to original properties
            original_properties = getattr(widget, '_original_press_properties', {})
            if original_properties:
                self._animate_properties(widget, original_properties, duration)
            # Call original event handler if it exists
            if hasattr(widget, '_original_release_event'):
                widget._original_release_event(event)
        
        # Store original event handlers
        if hasattr(widget, 'mousePressEvent'):
            widget._original_press_event = widget.mousePressEvent
        if hasattr(widget, 'mouseReleaseEvent'):
            widget._original_release_event = widget.mouseReleaseEvent
        
        # Store original properties for restoration
        widget._original_press_properties = self._get_current_properties(widget, press_properties.keys())
        
        # Set new event handlers
        widget.mousePressEvent = on_press_event
        widget.mouseReleaseEvent = on_release_event
    
    def create_fade_transition(self, widget: QWidget, 
                              fade_in: bool = True,
                              duration: int = 300,
                              callback=None) -> QPropertyAnimation:
        """Create a fade in/out transition"""
        effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(effect)
        
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        
        if fade_in:
            animation.setStartValue(0.0)
            animation.setEndValue(1.0)
        else:
            animation.setStartValue(1.0)
            animation.setEndValue(0.0)
        
        animation.setEasingCurve(QEasingCurve.OutQuad)
        
        if callback:
            animation.finished.connect(callback)
        
        animation.start(QAbstractAnimation.DeleteWhenStopped)
        
        return animation
    
    def create_scale_animation(self, widget: QWidget,
                              start_scale: float = 0.8,
                              end_scale: float = 1.0,
                              duration: int = 250) -> QVariantAnimation:
        """Create a scale animation effect"""
        original_geometry = widget.geometry()
        
        def update_scale(scale):
            # Calculate new size based on scale
            new_width = int(original_geometry.width() * scale)
            new_height = int(original_geometry.height() * scale)
            
            # Calculate position to keep widget centered
            new_x = original_geometry.x() + (original_geometry.width() - new_width) // 2
            new_y = original_geometry.y() + (original_geometry.height() - new_height) // 2
            
            widget.setGeometry(new_x, new_y, new_width, new_height)
        
        animation = QVariantAnimation()
        animation.setStartValue(start_scale)
        animation.setEndValue(end_scale)
        animation.setDuration(duration)
        animation.setEasingCurve(QEasingCurve.OutBack)
        animation.valueChanged.connect(update_scale)
        
        animation.start(QAbstractAnimation.DeleteWhenStopped)
        
        return animation
    
    def create_slide_animation(self, widget: QWidget,
                              direction: str = 'up',
                              distance: int = 20,
                              duration: int = 300) -> QPropertyAnimation:
        """Create a slide animation effect"""
        original_pos = widget.pos()
        
        # Calculate start and end positions
        if direction == 'up':
            start_pos = original_pos.x(), original_pos.y() + distance
            end_pos = original_pos.x(), original_pos.y()
        elif direction == 'down':
            start_pos = original_pos.x(), original_pos.y() - distance
            end_pos = original_pos.x(), original_pos.y()
        elif direction == 'left':
            start_pos = original_pos.x() + distance, original_pos.y()
            end_pos = original_pos.x(), original_pos.y()
        elif direction == 'right':
            start_pos = original_pos.x() - distance, original_pos.y()
            end_pos = original_pos.x(), original_pos.y()
        else:
            start_pos = end_pos = original_pos.x(), original_pos.y()
        
        # Set initial position
        widget.move(*start_pos)
        
        # Create animation
        animation = QPropertyAnimation(widget, b"pos")
        animation.setDuration(duration)
        animation.setStartValue(widget.pos())
        animation.setEndValue(widget.pos().__class__(*end_pos))
        animation.setEasingCurve(QEasingCurve.OutQuad)
        
        animation.start(QAbstractAnimation.DeleteWhenStopped)
        
        return animation
    
    def _animate_properties(self, widget: QWidget, properties: Dict[str, Any], duration: int):
        """Animate multiple properties of a widget"""
        # This is a simplified version - in a full implementation,
        # you'd need to handle different property types appropriately
        
        # For now, we'll focus on common properties like geometry, opacity, etc.
        if 'geometry' in properties:
            animation = QPropertyAnimation(widget, b"geometry")
            animation.setDuration(duration)
            animation.setEndValue(properties['geometry'])
            animation.setEasingCurve(QEasingCurve.OutQuad)
            animation.start(QAbstractAnimation.DeleteWhenStopped)
        
        if 'opacity' in properties and widget.graphicsEffect():
            effect = widget.graphicsEffect()
            if isinstance(effect, QGraphicsOpacityEffect):
                animation = QPropertyAnimation(effect, b"opacity")
                animation.setDuration(duration)
                animation.setEndValue(properties['opacity'])
                animation.setEasingCurve(QEasingCurve.OutQuad)
                animation.start(QAbstractAnimation.DeleteWhenStopped)
    
    def _get_current_properties(self, widget: QWidget, property_names: List[str]) -> Dict[str, Any]:
        """Get current property values from a widget"""
        properties = {}
        
        for prop_name in property_names:
            if prop_name == 'geometry':
                properties[prop_name] = widget.geometry()
            elif prop_name == 'opacity' and widget.graphicsEffect():
                effect = widget.graphicsEffect()
                if isinstance(effect, QGraphicsOpacityEffect):
                    properties[prop_name] = effect.opacity()
            # Add more properties as needed
        
        return properties
    
    def create_sequential_animation(self, animations: List[QAbstractAnimation]) -> QSequentialAnimationGroup:
        """Create a sequential animation group"""
        group = QSequentialAnimationGroup()
        for animation in animations:
            group.addAnimation(animation)
        
        return group
    
    def create_parallel_animation(self, animations: List[QAbstractAnimation]) -> QParallelAnimationGroup:
        """Create a parallel animation group"""
        group = QParallelAnimationGroup()
        for animation in animations:
            group.addAnimation(animation)
        
        return group


class ResponsiveStyleManager:
    """
    Manages responsive styles using the CSS variable system
    """
    
    def __init__(self):
        self.css_vars = CSSVariableSystem()
        self.micro_interactions = MicroInteractionManager()
        self.responsive_styles = {}
        self.current_breakpoint = 'lg'
        
        self._initialize_responsive_styles()
    
    def _initialize_responsive_styles(self):
        """Initialize responsive style templates"""
        self.responsive_styles = {
            'button': {
                'base': """
                    QPushButton {
                        background-color: var(--color-primary);
                        color: var(--text-inverse);
                        border: none;
                        border-radius: var(--radius-md);
                        font-family: var(--font-family-sans);
                        font-size: var(--font-size-base);
                        font-weight: var(--font-weight-medium);
                        padding: var(--spacing-3) var(--spacing-6);
                        min-height: 44px;
                    }
                    QPushButton:hover {
                        background-color: var(--color-primary-dark);
                    }
                    QPushButton:pressed {
                        background-color: var(--color-primary-light);
                    }
                """,
                'xs': """
                    QPushButton {
                        font-size: var(--font-size-lg);
                        padding: var(--spacing-4) var(--spacing-6);
                        min-height: 48px;
                    }
                """
            },
            'input': {
                'base': """
                    QLineEdit {
                        background-color: var(--bg-surface);
                        color: var(--text-primary);
                        border: 2px solid var(--border-color);
                        border-radius: var(--radius-md);
                        font-family: var(--font-family-sans);
                        font-size: var(--font-size-base);
                        padding: var(--spacing-3) var(--spacing-4);
                    }
                    QLineEdit:focus {
                        border-color: var(--border-focus);
                    }
                    QLineEdit:hover {
                        border-color: var(--color-gray-300);
                    }
                """,
                'xs': """
                    QLineEdit {
                        font-size: var(--font-size-lg);
                        padding: var(--spacing-4);
                        min-height: 48px;
                    }
                """
            },
            'card': {
                'base': """
                    QGroupBox {
                        background-color: var(--bg-surface);
                        border: 1px solid var(--border-color);
                        border-radius: var(--radius-lg);
                        font-family: var(--font-family-sans);
                        font-size: var(--font-size-lg);
                        font-weight: var(--font-weight-semibold);
                        color: var(--text-primary);
                        padding: var(--spacing-6);
                        margin: var(--spacing-4) 0;
                    }
                    QGroupBox::title {
                        color: var(--color-primary);
                        background-color: var(--bg-surface);
                        padding: 0 var(--spacing-2);
                    }
                """,
                'xs': """
                    QGroupBox {
                        padding: var(--spacing-4);
                        margin: var(--spacing-2) 0;
                    }
                """
            }
        }
    
    def apply_responsive_styles(self, widget_type: str, widget: QWidget, breakpoint: str = None):
        """Apply responsive styles to a widget"""
        if widget_type not in self.responsive_styles:
            logger.warning(f"No styles defined for widget type: {widget_type}")
            return
        
        breakpoint = breakpoint or self.current_breakpoint
        styles = self.responsive_styles[widget_type]
        
        # Start with base styles
        stylesheet = styles.get('base', '')
        
        # Add breakpoint-specific styles
        if breakpoint in styles:
            stylesheet += '\n' + styles[breakpoint]
        
        # Generate final stylesheet with variable substitution
        final_stylesheet = self.css_vars.generate_stylesheet(stylesheet)
        
        # Apply to widget
        widget.setStyleSheet(final_stylesheet)
    
    def add_micro_interactions(self, widget: QWidget, widget_type: str = None):
        """Add micro-interactions to a widget"""
        if isinstance(widget, QPushButton):
            self._add_button_interactions(widget)
        elif isinstance(widget, (QLineEdit, QTextEdit)):
            self._add_input_interactions(widget)
        elif isinstance(widget, QGroupBox):
            self._add_card_interactions(widget)
    
    def _add_button_interactions(self, button: QPushButton):
        """Add micro-interactions to a button"""
        # Hover effect
        self.micro_interactions.create_hover_effect(
            button,
            {'opacity': 0.9},  # Simplified - would need more sophisticated property handling
            duration=200
        )
        
        # Press effect
        self.micro_interactions.create_press_effect(
            button,
            {'opacity': 0.8},
            duration=100
        )
    
    def _add_input_interactions(self, input_widget):
        """Add micro-interactions to input fields"""
        # Focus animation could be added here
        # For now, we'll add a subtle hover effect
        self.micro_interactions.create_hover_effect(
            input_widget,
            {'opacity': 1.0},  # Simplified
            duration=150
        )
    
    def _add_card_interactions(self, card: QGroupBox):
        """Add micro-interactions to cards"""
        # Subtle hover effect for cards
        self.micro_interactions.create_hover_effect(
            card,
            {'opacity': 0.98},  # Simplified
            duration=200
        )
    
    def set_breakpoint(self, breakpoint: str):
        """Set the current responsive breakpoint"""
        self.current_breakpoint = breakpoint
    
    def get_css_variables(self) -> CSSVariableSystem:
        """Get the CSS variables system"""
        return self.css_vars
    
    def get_micro_interactions(self) -> MicroInteractionManager:
        """Get the micro-interactions manager"""
        return self.micro_interactions


# Utility functions for easy integration
def create_responsive_style_manager() -> ResponsiveStyleManager:
    """Create and configure a responsive style manager"""
    return ResponsiveStyleManager()


def apply_enhanced_styling(widget: QWidget, widget_type: str, style_manager: ResponsiveStyleManager):
    """Apply enhanced styling with micro-interactions to a widget"""
    style_manager.apply_responsive_styles(widget_type, widget)
    style_manager.add_micro_interactions(widget, widget_type)


if __name__ == "__main__":
    # Demo the CSS variables system and micro-interactions
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
    
    app = QApplication(sys.argv)
    
    # Create main window
    window = QMainWindow()
    central = QWidget()
    window.setCentralWidget(central)
    
    layout = QVBoxLayout(central)
    
    # Create style manager
    style_manager = create_responsive_style_manager()
    
    # Create demo widgets
    button1 = QPushButton("Primary Button")
    button2 = QPushButton("Secondary Action")
    input_field = QLineEdit()
    input_field.setPlaceholderText("Type something here...")
    
    card = QGroupBox("Demo Card")
    card_layout = QVBoxLayout(card)
    card_layout.addWidget(QLabel("This is a demo card with modern styling"))
    
    # Apply enhanced styling
    apply_enhanced_styling(button1, 'button', style_manager)
    apply_enhanced_styling(button2, 'button', style_manager)
    apply_enhanced_styling(input_field, 'input', style_manager)
    apply_enhanced_styling(card, 'card', style_manager)
    
    # Add to layout
    layout.addWidget(button1)
    layout.addWidget(button2)
    layout.addWidget(input_field)
    layout.addWidget(card)
    
    # Theme toggle button
    theme_btn = QPushButton("Toggle Dark Theme")
    
    def toggle_theme():
        current = style_manager.css_vars.current_theme
        new_theme = 'dark' if current == 'light' else 'light'
        style_manager.css_vars.apply_theme(new_theme)
        
        # Re-apply styles to all widgets
        apply_enhanced_styling(button1, 'button', style_manager)
        apply_enhanced_styling(button2, 'button', style_manager)
        apply_enhanced_styling(input_field, 'input', style_manager)
        apply_enhanced_styling(card, 'card', style_manager)
        apply_enhanced_styling(theme_btn, 'button', style_manager)
    
    theme_btn.clicked.connect(toggle_theme)
    apply_enhanced_styling(theme_btn, 'button', style_manager)
    layout.addWidget(theme_btn)
    
    window.setWindowTitle("CSS Variables & Micro-Interactions Demo")
    window.resize(600, 500)
    window.show()
    
    print("CSS Variables and Micro-Interactions demo running...")
    print(f"Current theme: {style_manager.css_vars.current_theme}")
    print(f"Available themes: {list(style_manager.css_vars.themes.keys())}")
    
    sys.exit(app.exec_())

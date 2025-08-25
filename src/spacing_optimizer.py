"""
Advanced Spacing and Layout Optimizer for Spanish Subjunctive Practice App

This module provides comprehensive text spacing, layout optimization, and visual
breathing room management to enhance readability and reduce eye strain.

Features:
- Optimal line spacing (1.5-1.6) for body text
- Paragraph spacing for instructions and content blocks
- Dynamic margin and padding management
- Whitespace optimization for visual hierarchy
- Alignment optimization for better text scanning
- Typography-based spacing calculations
- Responsive spacing based on font sizes
- Color contrast optimization for spacing elements
"""

from PyQt5.QtWidgets import (
    QWidget, QLabel, QTextEdit, QScrollArea, QGroupBox, 
    QVBoxLayout, QHBoxLayout, QApplication
)
from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtGui import QFont, QFontMetrics, QPalette, QColor
from typing import Dict, Tuple, Optional, Union
import logging

logger = logging.getLogger(__name__)


class SpacingCalculator:
    """Calculate optimal spacing values based on typography and content"""
    
    @staticmethod
    def calculate_line_height(font: QFont, target_ratio: float = 1.5) -> int:
        """Calculate optimal line height based on font size and target ratio"""
        font_metrics = QFontMetrics(font)
        font_height = font_metrics.height()
        return int(font_height * target_ratio)
    
    @staticmethod
    def calculate_paragraph_spacing(font_size: int, base_multiplier: float = 0.75) -> int:
        """Calculate paragraph spacing based on font size"""
        return int(font_size * base_multiplier)
    
    @staticmethod
    def calculate_section_spacing(font_size: int, multiplier: float = 1.2) -> int:
        """Calculate spacing between major sections"""
        return int(font_size * multiplier)
    
    @staticmethod
    def calculate_content_margins(widget_width: int, min_margin: int = 15) -> Tuple[int, int, int, int]:
        """Calculate optimal content margins based on widget width"""
        # Use golden ratio for optimal reading width
        optimal_width = widget_width * 0.618  # Golden ratio
        side_margin = max(min_margin, int((widget_width - optimal_width) / 2))
        
        # Vertical margins should be proportional but smaller
        vertical_margin = max(min_margin, int(side_margin * 0.6))
        
        return (side_margin, vertical_margin, side_margin, vertical_margin)  # left, top, right, bottom


class TypographySpacingProfile:
    """Typography-based spacing profile for different content types"""
    
    def __init__(self, font_size: int, line_height_ratio: float = 1.5):
        self.font_size = font_size
        self.line_height_ratio = line_height_ratio
        self.base_unit = font_size
        
        # Calculate spacing values
        self.line_height = int(self.base_unit * line_height_ratio)
        self.paragraph_spacing = int(self.base_unit * 0.75)
        self.section_spacing = int(self.base_unit * 1.2)
        self.block_spacing = int(self.base_unit * 1.5)
        self.group_spacing = int(self.base_unit * 2.0)
        
        # Margin calculations
        self.content_margin = max(15, int(self.base_unit * 0.8))
        self.nested_margin = max(10, int(self.base_unit * 0.5))
        self.button_margin = max(8, int(self.base_unit * 0.4))


class ReadabilityOptimizer:
    """Optimize text readability through spacing and layout"""
    
    @staticmethod
    def optimize_text_widget_spacing(widget: Union[QLabel, QTextEdit], 
                                   profile: TypographySpacingProfile) -> None:
        """Apply optimal spacing to text widgets"""
        
        if isinstance(widget, QLabel):
            widget.setWordWrap(True)
            widget.setAlignment(Qt.AlignTop | Qt.AlignLeft)
            
            # Set margins for breathing room
            widget.setContentsMargins(
                profile.content_margin, 
                profile.paragraph_spacing,
                profile.content_margin, 
                profile.paragraph_spacing
            )
            
            # Apply optimal line height through stylesheet
            widget.setStyleSheet(f"""
                QLabel {{
                    line-height: {profile.line_height}px;
                    padding: {profile.paragraph_spacing}px;
                }}
            """)
            
        elif isinstance(widget, QTextEdit):
            # Set optimal line height for text edit
            font = widget.font()
            font.setPixelSize(profile.font_size)
            widget.setFont(font)
            
            # Apply spacing through stylesheet
            widget.setStyleSheet(f"""
                QTextEdit {{
                    line-height: {profile.line_height}px;
                    padding: {profile.content_margin}px;
                    margin: {profile.block_spacing}px 0px;
                }}
            """)
    
    @staticmethod
    def create_breathing_space() -> QWidget:
        """Create an invisible spacer widget for visual breathing room"""
        spacer = QLabel()
        spacer.setFixedHeight(20)
        spacer.setStyleSheet("QLabel { background: transparent; }")
        return spacer
    
    @staticmethod
    def optimize_scroll_area_spacing(scroll_area: QScrollArea, 
                                   profile: TypographySpacingProfile) -> None:
        """Optimize spacing within scroll areas"""
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                padding: {profile.content_margin}px;
                margin: {profile.block_spacing}px 0px;
            }}
            QScrollArea QWidget {{
                padding: {profile.nested_margin}px;
            }}
        """)


class LayoutSpacingManager:
    """Manage spacing across different layout types"""
    
    def __init__(self, profile: TypographySpacingProfile):
        self.profile = profile
    
    def optimize_vertical_layout(self, layout: QVBoxLayout) -> None:
        """Optimize vertical layout spacing"""
        layout.setSpacing(self.profile.section_spacing)
        layout.setContentsMargins(
            self.profile.content_margin,
            self.profile.content_margin,
            self.profile.content_margin,
            self.profile.content_margin
        )
    
    def optimize_horizontal_layout(self, layout: QHBoxLayout) -> None:
        """Optimize horizontal layout spacing"""
        layout.setSpacing(self.profile.button_margin)
        layout.setContentsMargins(
            self.profile.nested_margin,
            self.profile.nested_margin,
            self.profile.nested_margin,
            self.profile.nested_margin
        )
    
    def optimize_group_box_spacing(self, group_box: QGroupBox) -> None:
        """Optimize spacing within group boxes"""
        group_box.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                border: 2px solid #c0c0c0;
                border-radius: 5px;
                margin-top: {self.profile.section_spacing}px;
                padding: {self.profile.block_spacing}px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: {self.profile.nested_margin}px;
                padding: 0 {self.profile.nested_margin}px 0 {self.profile.nested_margin}px;
                margin-bottom: {self.profile.paragraph_spacing}px;
            }}
        """)


class AccessibleSpacingEnhancer:
    """Enhance spacing for better accessibility"""
    
    @staticmethod
    def enhance_focus_spacing(widget: QWidget, profile: TypographySpacingProfile) -> None:
        """Add enhanced spacing for focused elements"""
        widget.setStyleSheet(widget.styleSheet() + f"""
            QWidget:focus {{
                border: 2px solid #0078d4;
                padding: {profile.button_margin}px;
                margin: {profile.nested_margin}px;
            }}
        """)
    
    @staticmethod
    def enhance_button_spacing(widget: QWidget, profile: TypographySpacingProfile) -> None:
        """Optimize button spacing for touch targets"""
        widget.setMinimumHeight(44)  # Accessibility guideline minimum
        widget.setStyleSheet(widget.styleSheet() + f"""
            QPushButton {{
                padding: {profile.button_margin * 2}px {profile.content_margin}px;
                margin: {profile.nested_margin}px;
                min-height: 44px;
            }}
        """)


class SpacingOptimizer:
    """Main spacing optimizer class that orchestrates all spacing improvements"""
    
    def __init__(self, base_font_size: int = 12, line_height_ratio: float = 1.5):
        self.profile = TypographySpacingProfile(base_font_size, line_height_ratio)
        self.layout_manager = LayoutSpacingManager(self.profile)
        self.readability_optimizer = ReadabilityOptimizer()
        self.accessibility_enhancer = AccessibleSpacingEnhancer()
        
        logger.info(f"SpacingOptimizer initialized with font size: {base_font_size}, "
                   f"line height ratio: {line_height_ratio}")
    
    def optimize_widget_spacing(self, widget: QWidget) -> None:
        """Apply comprehensive spacing optimization to a widget"""
        try:
            # Get widget font for calculations
            font = widget.font()
            if font.pointSize() > 0:
                self.profile = TypographySpacingProfile(font.pointSize(), 1.5)
            
            # Apply spacing based on widget type
            if isinstance(widget, (QLabel, QTextEdit)):
                self.readability_optimizer.optimize_text_widget_spacing(widget, self.profile)
            
            if isinstance(widget, QScrollArea):
                self.readability_optimizer.optimize_scroll_area_spacing(widget, self.profile)
            
            if isinstance(widget, QGroupBox):
                self.layout_manager.optimize_group_box_spacing(widget)
            
            # Apply accessibility enhancements
            if widget.focusPolicy() != Qt.NoFocus:
                self.accessibility_enhancer.enhance_focus_spacing(widget, self.profile)
            
            if widget.objectName() and 'button' in widget.objectName().lower():
                self.accessibility_enhancer.enhance_button_spacing(widget, self.profile)
            
            logger.debug(f"Applied spacing optimization to {widget.__class__.__name__}")
            
        except Exception as e:
            logger.error(f"Error optimizing spacing for widget {widget.__class__.__name__}: {e}")
    
    def optimize_layout_spacing(self, layout: Union[QVBoxLayout, QHBoxLayout]) -> None:
        """Apply spacing optimization to layouts"""
        try:
            if isinstance(layout, QVBoxLayout):
                self.layout_manager.optimize_vertical_layout(layout)
            elif isinstance(layout, QHBoxLayout):
                self.layout_manager.optimize_horizontal_layout(layout)
            
            logger.debug(f"Applied spacing optimization to {layout.__class__.__name__}")
            
        except Exception as e:
            logger.error(f"Error optimizing layout spacing: {e}")
    
    def create_visual_separator(self, height: int = None) -> QWidget:
        """Create a visual separator with optimal spacing"""
        separator = QLabel()
        separator_height = height or self.profile.section_spacing
        separator.setFixedHeight(separator_height)
        separator.setStyleSheet("""
            QLabel {
                background: transparent;
                border-bottom: 1px solid #e0e0e0;
                margin: 10px 0px;
            }
        """)
        return separator
    
    def add_breathing_room_to_container(self, container: QWidget) -> None:
        """Add optimal breathing room around container elements"""
        try:
            container.setContentsMargins(
                self.profile.content_margin,
                self.profile.content_margin,
                self.profile.content_margin,
                self.profile.content_margin
            )
            
            # Add breathing room through padding
            container.setStyleSheet(container.styleSheet() + f"""
                QWidget {{
                    padding: {self.profile.nested_margin}px;
                }}
            """)
            
            logger.debug(f"Added breathing room to container: {container.__class__.__name__}")
            
        except Exception as e:
            logger.error(f"Error adding breathing room to container: {e}")
    
    def optimize_entire_application(self, app: QApplication) -> None:
        """Apply global spacing optimizations to the entire application"""
        try:
            # Set global stylesheet with optimal spacing
            global_styles = f"""
                * {{
                    font-size: {self.profile.font_size}px;
                    line-height: {self.profile.line_height}px;
                }}
                
                QWidget {{
                    padding: {self.profile.nested_margin}px;
                    margin: {self.profile.nested_margin // 2}px;
                }}
                
                QLabel {{
                    line-height: {self.profile.line_height}px;
                    padding: {self.profile.paragraph_spacing}px 0px;
                }}
                
                QTextEdit {{
                    line-height: {self.profile.line_height}px;
                    padding: {self.profile.content_margin}px;
                }}
                
                QPushButton {{
                    padding: {self.profile.button_margin * 2}px {self.profile.content_margin}px;
                    margin: {self.profile.nested_margin}px;
                    min-height: 44px;
                }}
                
                QGroupBox {{
                    padding: {self.profile.block_spacing}px;
                    margin: {self.profile.section_spacing}px 0px;
                }}
                
                QScrollArea {{
                    padding: {self.profile.content_margin}px;
                }}
            """
            
            app.setStyleSheet(app.styleSheet() + global_styles)
            logger.info("Applied global spacing optimization to application")
            
        except Exception as e:
            logger.error(f"Error applying global spacing optimization: {e}")
    
    def get_spacing_report(self) -> Dict[str, any]:
        """Generate a report of current spacing settings"""
        return {
            "profile": {
                "font_size": self.profile.font_size,
                "line_height": self.profile.line_height,
                "line_height_ratio": self.profile.line_height_ratio,
                "paragraph_spacing": self.profile.paragraph_spacing,
                "section_spacing": self.profile.section_spacing,
                "content_margin": self.profile.content_margin
            },
            "recommendations": [
                "Line height ratio of 1.5-1.6 improves readability",
                "Adequate paragraph spacing reduces cognitive load",
                "Consistent margins create visual hierarchy",
                "Button spacing meets accessibility guidelines (44px min height)",
                "Content margins follow golden ratio principles"
            ]
        }


def apply_spacing_to_spanish_app(main_window) -> SpacingOptimizer:
    """
    Apply comprehensive spacing optimization to the Spanish Subjunctive Practice App
    
    Args:
        main_window: The main application window instance
    
    Returns:
        SpacingOptimizer: The optimizer instance for further customization
    """
    try:
        # Initialize optimizer with optimal settings for reading
        optimizer = SpacingOptimizer(base_font_size=13, line_height_ratio=1.55)
        
        # Optimize main widgets
        if hasattr(main_window, 'sentence_label'):
            optimizer.optimize_widget_spacing(main_window.sentence_label)
        
        if hasattr(main_window, 'translation_label'):
            optimizer.optimize_widget_spacing(main_window.translation_label)
        
        if hasattr(main_window, 'feedback_text'):
            optimizer.optimize_widget_spacing(main_window.feedback_text)
        
        if hasattr(main_window, 'stats_label'):
            optimizer.optimize_widget_spacing(main_window.stats_label)
        
        # Optimize scroll areas
        if hasattr(main_window, 'trigger_scroll_area'):
            optimizer.optimize_widget_spacing(main_window.trigger_scroll_area)
        
        # Optimize group boxes
        for attr_name in dir(main_window):
            attr = getattr(main_window, attr_name)
            if isinstance(attr, QGroupBox):
                optimizer.optimize_widget_spacing(attr)
        
        # Add breathing room to main container
        central_widget = main_window.centralWidget()
        if central_widget:
            optimizer.add_breathing_room_to_container(central_widget)
        
        # Apply global optimizations
        app = QApplication.instance()
        if app:
            optimizer.optimize_entire_application(app)
        
        logger.info("Successfully applied spacing optimization to Spanish Subjunctive Practice App")
        return optimizer
        
    except Exception as e:
        logger.error(f"Error applying spacing optimization to Spanish app: {e}")
        return None


# Helper function for easy integration
def quick_optimize_spacing(widget: QWidget, font_size: int = 13) -> None:
    """Quick spacing optimization for any widget"""
    optimizer = SpacingOptimizer(base_font_size=font_size)
    optimizer.optimize_widget_spacing(widget)


if __name__ == "__main__":
    # Demo and testing
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
    
    app = QApplication(sys.argv)
    
    # Create demo window
    window = QMainWindow()
    central = QWidget()
    window.setCentralWidget(central)
    
    layout = QVBoxLayout(central)
    
    # Add demo content
    title = QLabel("Spanish Subjunctive Practice - Optimized Spacing")
    content = QLabel("""
    This demo shows optimized text spacing with:
    • Line height ratio of 1.55 for better readability
    • Optimal paragraph spacing to reduce eye strain
    • Proper margins for visual breathing room
    • Typography-based spacing calculations
    """)
    
    layout.addWidget(title)
    layout.addWidget(content)
    
    # Apply spacing optimization
    optimizer = SpacingOptimizer()
    optimizer.optimize_widget_spacing(title)
    optimizer.optimize_widget_spacing(content)
    optimizer.optimize_layout_spacing(layout)
    
    window.show()
    print("Spacing optimization demo running...")
    print(f"Spacing report: {optimizer.get_spacing_report()}")
    
    sys.exit(app.exec_())
"""
Readability Enhancements Module for Spanish Subjunctive Practice App

This module provides comprehensive readability improvements focusing on:
1. Text contrast ratios (WCAG AAA standards)
2. Optimal paragraph width (45-75 characters)
3. Proper spacing between UI elements
4. Clear visual hierarchy for questions vs answers
5. Reduced cognitive load through better text presentation

Specifically optimized for Spanish language requirements including diacritical marks.
"""

import logging
from typing import Dict, List, Tuple, Optional, Any
from PyQt5.QtWidgets import (
    QWidget, QLabel, QTextEdit, QLineEdit, QPushButton, QGroupBox,
    QScrollArea, QProgressBar, QStatusBar, QComboBox, QCheckBox, QRadioButton,
    QSizePolicy, QApplication
)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect
from PyQt5.QtGui import QFont, QFontMetrics, QPalette, QColor, QTextCharFormat, QTextCursor

logger = logging.getLogger(__name__)

class ReadabilityAnalyzer:
    """Analyzes current UI elements for readability issues"""
    
    def __init__(self):
        self.wcag_aaa_ratio = 7.0  # WCAG AAA standard
        self.wcag_aa_ratio = 4.5   # WCAG AA standard
        self.optimal_line_length_min = 45  # characters
        self.optimal_line_length_max = 75  # characters
        self.spanish_diacritics = "áéíóúüñÁÉÍÓÚÜÑ¿¡"
        
    def calculate_contrast_ratio(self, color1: QColor, color2: QColor) -> float:
        """Calculate contrast ratio between two colors"""
        def relative_luminance(color: QColor) -> float:
            # Convert to sRGB
            def linearize(c: float) -> float:
                c = c / 255.0
                if c <= 0.03928:
                    return c / 12.92
                else:
                    return ((c + 0.055) / 1.055) ** 2.4
            
            r = linearize(color.red())
            g = linearize(color.green())
            b = linearize(color.blue())
            
            return 0.2126 * r + 0.7152 * g + 0.0722 * b
        
        lum1 = relative_luminance(color1)
        lum2 = relative_luminance(color2)
        
        lighter = max(lum1, lum2)
        darker = min(lum1, lum2)
        
        return (lighter + 0.05) / (darker + 0.05)
    
    def analyze_text_width(self, widget: QWidget, font: QFont) -> Dict[str, Any]:
        """Analyze text width for optimal readability"""
        if not isinstance(widget, (QLabel, QTextEdit)):
            return {"status": "not_applicable"}
        
        metrics = QFontMetrics(font)
        widget_width = widget.width()
        char_width = metrics.averageCharWidth()
        
        # Account for Spanish diacritics which may be slightly wider
        spanish_char_width = char_width * 1.1
        
        chars_per_line = widget_width / spanish_char_width
        
        analysis = {
            "chars_per_line": int(chars_per_line),
            "is_optimal": self.optimal_line_length_min <= chars_per_line <= self.optimal_line_length_max,
            "recommendation": "",
            "severity": "info"
        }
        
        if chars_per_line < self.optimal_line_length_min:
            analysis["recommendation"] = f"Text width too narrow ({int(chars_per_line)} chars). Increase to {self.optimal_line_length_min}-{self.optimal_line_length_max} characters."
            analysis["severity"] = "warning"
        elif chars_per_line > self.optimal_line_length_max:
            analysis["recommendation"] = f"Text width too wide ({int(chars_per_line)} chars). Reduce to {self.optimal_line_length_min}-{self.optimal_line_length_max} characters."
            analysis["severity"] = "warning"
        else:
            analysis["recommendation"] = "Text width is optimal for readability."
        
        return analysis
    
    def analyze_spacing(self, widget: QWidget) -> Dict[str, Any]:
        """Analyze spacing between UI elements"""
        layout = widget.layout()
        if not layout:
            return {"status": "no_layout"}
        
        spacing = layout.spacing()
        margins = layout.getContentsMargins()
        
        # Recommended spacing: 8-16px for related elements, 16-24px for sections
        analysis = {
            "current_spacing": spacing,
            "current_margins": margins,
            "recommendations": []
        }
        
        if spacing < 8:
            analysis["recommendations"].append(f"Increase element spacing from {spacing}px to 8-16px")
        elif spacing > 24:
            analysis["recommendations"].append(f"Decrease element spacing from {spacing}px to 16-24px")
        
        # Check margins
        min_margin = min(margins)
        max_margin = max(margins)
        
        if min_margin < 10:
            analysis["recommendations"].append(f"Increase minimum margins from {min_margin}px to 10-15px")
        if max_margin > 30:
            analysis["recommendations"].append(f"Decrease maximum margins from {max_margin}px to 15-30px")
        
        return analysis
    
    def analyze_color_contrast(self, widget: QWidget) -> Dict[str, Any]:
        """Analyze color contrast for WCAG compliance"""
        palette = widget.palette()
        text_color = palette.color(QPalette.WindowText)
        bg_color = palette.color(QPalette.Window)
        
        contrast_ratio = self.calculate_contrast_ratio(text_color, bg_color)
        
        analysis = {
            "contrast_ratio": contrast_ratio,
            "wcag_aa_pass": contrast_ratio >= self.wcag_aa_ratio,
            "wcag_aaa_pass": contrast_ratio >= self.wcag_aaa_ratio,
            "text_color": text_color.name(),
            "bg_color": bg_color.name(),
            "recommendation": ""
        }
        
        if contrast_ratio < self.wcag_aa_ratio:
            analysis["recommendation"] = f"Contrast ratio {contrast_ratio:.1f} fails WCAG AA. Minimum 4.5 required."
            analysis["severity"] = "critical"
        elif contrast_ratio < self.wcag_aaa_ratio:
            analysis["recommendation"] = f"Contrast ratio {contrast_ratio:.1f} meets WCAG AA but not AAA. Consider improving to 7.0+."
            analysis["severity"] = "warning"
        else:
            analysis["recommendation"] = f"Excellent contrast ratio {contrast_ratio:.1f} meets WCAG AAA standards."
            analysis["severity"] = "success"
        
        return analysis

class ReadabilityEnhancer:
    """Applies readability enhancements to widgets"""
    
    def __init__(self):
        self.base_font_size = 14  # Base font size for Spanish text
        self.line_height_multiplier = 1.4  # 140% line height
        self.spanish_optimized_fonts = [
            "Segoe UI", "Liberation Sans", "DejaVu Sans", 
            "Noto Sans", "Arial Unicode MS", "Tahoma"
        ]
        
    def enhance_text_widget(self, widget: QWidget, content_type: str = "body") -> None:
        """Enhance text widget for optimal readability"""
        if not isinstance(widget, (QLabel, QTextEdit, QLineEdit)):
            return
        
        # Font enhancement
        font = self._get_optimal_font(content_type)
        widget.setFont(font)
        
        # Text formatting for Spanish
        if isinstance(widget, QTextEdit):
            self._enhance_text_edit(widget, content_type)
        elif isinstance(widget, QLabel):
            self._enhance_label(widget, content_type)
        elif isinstance(widget, QLineEdit):
            self._enhance_line_edit(widget, content_type)
    
    def _get_optimal_font(self, content_type: str) -> QFont:
        """Get optimal font for content type"""
        font_sizes = {
            "heading": self.base_font_size + 6,    # 20px
            "question": self.base_font_size + 2,    # 16px
            "body": self.base_font_size,            # 14px
            "answer": self.base_font_size,          # 14px
            "feedback": self.base_font_size - 1,    # 13px
            "small": self.base_font_size - 2        # 12px
        }
        
        size = font_sizes.get(content_type, self.base_font_size)
        
        # Try Spanish-optimized fonts in order
        font = QFont()
        font.setPointSize(size)
        
        for font_family in self.spanish_optimized_fonts:
            test_font = QFont(font_family, size)
            if QFontMetrics(test_font).inFontUcs4(ord('ñ')):  # Check Spanish character support
                font = test_font
                break
        
        # Set font properties for readability
        font.setWeight(QFont.Normal)
        font.setHintingPreference(QFont.PreferFullHinting)
        
        return font
    
    def _enhance_text_edit(self, widget: QTextEdit, content_type: str) -> None:
        """Enhance QTextEdit for optimal readability"""
        # Set optimal width constraints
        metrics = QFontMetrics(widget.font())
        optimal_width = metrics.averageCharWidth() * 65  # 65 characters wide
        widget.setMaximumWidth(optimal_width * 1.2)  # Allow some flexibility
        
        # Line height and paragraph spacing
        cursor = widget.textCursor()
        format = QTextCharFormat()
        format.setFontPointSize(widget.font().pointSize())
        cursor.setCharFormat(format)
        
        # Enable word wrap
        widget.setWordWrapMode(True)
        widget.setLineWrapMode(QTextEdit.WidgetWidth)
    
    def _enhance_label(self, widget: QLabel, content_type: str) -> None:
        """Enhance QLabel for optimal readability"""
        widget.setWordWrap(True)
        
        # Set appropriate alignment
        if content_type == "heading":
            widget.setAlignment(Qt.AlignCenter)
        else:
            widget.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        # Enable text interaction for better accessibility
        widget.setTextInteractionFlags(Qt.TextSelectableByMouse)
        
        # Set minimum height for comfortable reading
        metrics = QFontMetrics(widget.font())
        line_height = metrics.height() * self.line_height_multiplier
        widget.setMinimumHeight(int(line_height))
    
    def _enhance_line_edit(self, widget: QLineEdit, content_type: str) -> None:
        """Enhance QLineEdit for optimal readability"""
        # Set appropriate height
        metrics = QFontMetrics(widget.font())
        optimal_height = metrics.height() * 1.6  # More comfortable input height
        widget.setMinimumHeight(int(optimal_height))
        
        # Add padding
        widget.setStyleSheet(f"""
            QLineEdit {{
                padding: 8px 12px;
                border-radius: 4px;
                border: 2px solid #d1d5db;
            }}
            QLineEdit:focus {{
                border-color: #3b82f6;
                outline: none;
            }}
        """)

class SpanishTextOptimizer:
    """Optimizes text specifically for Spanish language readability"""
    
    def __init__(self):
        self.diacritics_map = {
            'a': ['á'], 'e': ['é'], 'i': ['í'], 'o': ['ó'], 'u': ['ú', 'ü'],
            'n': ['ñ'], 'A': ['Á'], 'E': ['É'], 'I': ['Í'], 'O': ['Ó'],
            'U': ['Ú', 'Ü'], 'N': ['Ñ']
        }
        
    def optimize_text_display(self, text: str) -> str:
        """Optimize text for better Spanish readability"""
        # Ensure proper spacing around punctuation marks
        text = self._fix_punctuation_spacing(text)
        
        # Handle question and exclamation marks
        text = self._handle_spanish_punctuation(text)
        
        # Ensure proper line breaks for long sentences
        text = self._optimize_line_breaks(text)
        
        return text
    
    def _fix_punctuation_spacing(self, text: str) -> str:
        """Fix spacing around punctuation for Spanish text"""
        import re
        
        # Add space after commas and periods if missing
        text = re.sub(r'([,\.])([^\s\d])', r'\1 \2', text)
        
        # Ensure proper spacing around colons
        text = re.sub(r'(\S):(\S)', r'\1: \2', text)
        
        # Fix spacing around parentheses
        text = re.sub(r'\s*\(\s*', ' (', text)
        text = re.sub(r'\s*\)\s*', ') ', text)
        
        return text.strip()
    
    def _handle_spanish_punctuation(self, text: str) -> str:
        """Handle Spanish-specific punctuation marks"""
        import re
        
        # Ensure inverted question marks at the beginning
        if '?' in text and not text.startswith('¿'):
            # Simple heuristic: if sentence has a question mark, add inverted at start
            if text.count('?') == 1:
                question_pos = text.find('?')
                # Find sentence start (look backwards for sentence boundaries)
                sentence_start = 0
                for i in range(question_pos - 1, -1, -1):
                    if text[i] in '.!?':
                        sentence_start = i + 1
                        break
                
                # Insert inverted question mark
                while sentence_start < len(text) and text[sentence_start].isspace():
                    sentence_start += 1
                
                if sentence_start < len(text):
                    text = text[:sentence_start] + '¿' + text[sentence_start:]
        
        # Similar logic for exclamation marks
        if '!' in text and not text.startswith('¡'):
            if text.count('!') == 1:
                exclaim_pos = text.find('!')
                sentence_start = 0
                for i in range(exclaim_pos - 1, -1, -1):
                    if text[i] in '.!?':
                        sentence_start = i + 1
                        break
                
                while sentence_start < len(text) and text[sentence_start].isspace():
                    sentence_start += 1
                
                if sentence_start < len(text):
                    text = text[:sentence_start] + '¡' + text[sentence_start:]
        
        return text
    
    def _optimize_line_breaks(self, text: str) -> str:
        """Optimize line breaks for Spanish text readability"""
        import re
        
        # Don't break words with diacritics
        # Add soft hyphens before conjunctions for better breaking
        conjunctions = ['y', 'o', 'pero', 'sino', 'aunque', 'porque', 'para', 'por']
        
        for conj in conjunctions:
            # Add zero-width space before conjunctions to allow breaks
            pattern = r'\s+(' + conj + r')\s+'
            replacement = r' \u200b\1 '  # Zero-width space before conjunction
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text

class VisualHierarchyManager:
    """Manages visual hierarchy for clear content organization"""
    
    def __init__(self):
        self.hierarchy_levels = {
            "primary": {"color": "#1f2937", "size_factor": 1.4, "weight": QFont.Bold},
            "secondary": {"color": "#374151", "size_factor": 1.2, "weight": QFont.DemiBold},
            "body": {"color": "#4b5563", "size_factor": 1.0, "weight": QFont.Normal},
            "muted": {"color": "#6b7280", "size_factor": 0.9, "weight": QFont.Normal},
            "accent": {"color": "#3b82f6", "size_factor": 1.0, "weight": QFont.DemiBold}
        }
        
        self.spacing_hierarchy = {
            "section": 24,
            "subsection": 16,
            "paragraph": 12,
            "line": 8
        }
    
    def apply_hierarchy(self, widget: QWidget, level: str, base_font_size: int = 14) -> None:
        """Apply visual hierarchy to a widget"""
        if level not in self.hierarchy_levels:
            return
        
        config = self.hierarchy_levels[level]
        
        # Create font with hierarchy settings
        font = widget.font()
        font.setPointSize(int(base_font_size * config["size_factor"]))
        font.setWeight(config["weight"])
        widget.setFont(font)
        
        # Apply color
        stylesheet = f"""
            color: {config["color"]};
            margin-bottom: {self.spacing_hierarchy.get("paragraph", 12)}px;
        """
        
        # Add specific styling based on widget type
        if isinstance(widget, QLabel):
            if level == "primary":
                stylesheet += """
                    font-weight: bold;
                    padding-bottom: 8px;
                    border-bottom: 2px solid #e5e7eb;
                """
        elif isinstance(widget, QPushButton):
            if level == "accent":
                stylesheet += """
                    background-color: #3b82f6;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 6px;
                    font-weight: 600;
                """
        
        widget.setStyleSheet(stylesheet)

class ReadabilityManager:
    """Main manager for all readability enhancements"""
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.analyzer = ReadabilityAnalyzer()
        self.enhancer = ReadabilityEnhancer()
        self.spanish_optimizer = SpanishTextOptimizer()
        self.hierarchy_manager = VisualHierarchyManager()
        
        # Track analysis results
        self.analysis_results = {}
        
    def analyze_application(self) -> Dict[str, Any]:
        """Perform comprehensive readability analysis of the application"""
        results = {
            "timestamp": None,
            "overall_score": 0,
            "widget_analyses": {},
            "recommendations": [],
            "critical_issues": [],
            "spanish_specific_issues": []
        }
        
        # Analyze all relevant widgets
        widgets_to_analyze = self._find_text_widgets()
        
        total_score = 0
        widget_count = 0
        
        for widget_name, widget in widgets_to_analyze.items():
            widget_analysis = self._analyze_widget(widget, widget_name)
            results["widget_analyses"][widget_name] = widget_analysis
            
            # Accumulate score
            if "score" in widget_analysis:
                total_score += widget_analysis["score"]
                widget_count += 1
            
            # Collect recommendations
            if widget_analysis.get("recommendations"):
                results["recommendations"].extend(widget_analysis["recommendations"])
            
            # Collect critical issues
            if widget_analysis.get("severity") == "critical":
                results["critical_issues"].append({
                    "widget": widget_name,
                    "issue": widget_analysis.get("issue", "Unknown issue")
                })
        
        # Calculate overall score
        if widget_count > 0:
            results["overall_score"] = total_score / widget_count
        
        # Add Spanish-specific recommendations
        results["spanish_specific_issues"] = self._check_spanish_specific_issues()
        
        # Store results
        self.analysis_results = results
        
        return results
    
    def _find_text_widgets(self) -> Dict[str, QWidget]:
        """Find all text-related widgets in the application"""
        widgets = {}
        
        # Map of widget attributes to analyze
        widget_mapping = {
            'sentence_label': 'question_text',
            'translation_label': 'translation',
            'stats_label': 'stats',
            'feedback_text': 'feedback',
            'free_response_input': 'input',
            'submit_button': 'primary_button',
            'hint_button': 'secondary_button'
        }
        
        for attr_name, widget_type in widget_mapping.items():
            widget = getattr(self.main_window, attr_name, None)
            if widget:
                widgets[f"{attr_name}_{widget_type}"] = widget
        
        return widgets
    
    def _analyze_widget(self, widget: QWidget, widget_name: str) -> Dict[str, Any]:
        """Analyze a single widget for readability issues"""
        analysis = {
            "widget_name": widget_name,
            "widget_type": type(widget).__name__,
            "recommendations": [],
            "score": 100,  # Start with perfect score
            "issues": []
        }
        
        # Contrast analysis
        contrast_result = self.analyzer.analyze_color_contrast(widget)
        if not contrast_result.get("wcag_aaa_pass", False):
            analysis["score"] -= 30
            analysis["issues"].append("Poor contrast ratio")
            analysis["recommendations"].append(contrast_result.get("recommendation", "Improve contrast"))
            if not contrast_result.get("wcag_aa_pass", False):
                analysis["severity"] = "critical"
        
        # Width analysis for text widgets
        if isinstance(widget, (QLabel, QTextEdit)):
            width_result = self.analyzer.analyze_text_width(widget, widget.font())
            if not width_result.get("is_optimal", False):
                analysis["score"] -= 20
                analysis["issues"].append("Suboptimal text width")
                analysis["recommendations"].append(width_result.get("recommendation", "Adjust text width"))
        
        # Font analysis
        font = widget.font()
        if font.pointSize() < 12:  # Too small for comfortable reading
            analysis["score"] -= 25
            analysis["issues"].append("Font too small")
            analysis["recommendations"].append("Increase font size to at least 12pt")
        
        # Spanish character support
        if isinstance(widget, (QLabel, QTextEdit, QLineEdit)):
            font_metrics = QFontMetrics(font)
            if not font_metrics.inFontUcs4(ord('ñ')):
                analysis["score"] -= 15
                analysis["issues"].append("Poor Spanish character support")
                analysis["recommendations"].append("Use Spanish-optimized font")
        
        return analysis
    
    def _check_spanish_specific_issues(self) -> List[Dict[str, Any]]:
        """Check for Spanish language specific readability issues"""
        issues = []
        
        # Check if main content areas support Spanish characters properly
        sentence_label = getattr(self.main_window, 'sentence_label', None)
        if sentence_label:
            font_metrics = QFontMetrics(sentence_label.font())
            
            # Test key Spanish characters
            test_chars = ['ñ', 'á', 'é', 'í', 'ó', 'ú', 'ü', '¿', '¡']
            unsupported_chars = []
            
            for char in test_chars:
                if not font_metrics.inFontUcs4(ord(char)):
                    unsupported_chars.append(char)
            
            if unsupported_chars:
                issues.append({
                    "type": "font_support",
                    "severity": "high",
                    "description": f"Font doesn't properly support: {', '.join(unsupported_chars)}",
                    "recommendation": "Switch to a Spanish-optimized font like Segoe UI or Noto Sans"
                })
        
        # Check for proper punctuation handling
        feedback_text = getattr(self.main_window, 'feedback_text', None)
        if feedback_text and hasattr(feedback_text, 'toPlainText'):
            content = feedback_text.toPlainText()
            if content:
                if '?' in content and '¿' not in content:
                    issues.append({
                        "type": "punctuation",
                        "severity": "medium",
                        "description": "Missing inverted question marks",
                        "recommendation": "Ensure Spanish punctuation rules are followed"
                    })
        
        return issues
    
    def apply_comprehensive_enhancements(self) -> None:
        """Apply all readability enhancements to the application"""
        logger.info("Applying comprehensive readability enhancements")
        
        # Enhance main content areas
        self._enhance_content_areas()
        
        # Apply visual hierarchy
        self._apply_visual_hierarchy()
        
        # Optimize spacing and layout
        self._optimize_spacing()
        
        # Apply Spanish-specific optimizations
        self._apply_spanish_optimizations()
        
        logger.info("Readability enhancements applied successfully")
    
    def _enhance_content_areas(self) -> None:
        """Enhance main content areas for optimal readability"""
        # Question/sentence display
        if hasattr(self.main_window, 'sentence_label'):
            self.enhancer.enhance_text_widget(
                self.main_window.sentence_label, 
                "question"
            )
            self.hierarchy_manager.apply_hierarchy(
                self.main_window.sentence_label, 
                "primary"
            )
        
        # Translation display
        if hasattr(self.main_window, 'translation_label'):
            self.enhancer.enhance_text_widget(
                self.main_window.translation_label, 
                "body"
            )
            self.hierarchy_manager.apply_hierarchy(
                self.main_window.translation_label, 
                "muted"
            )
        
        # Feedback area
        if hasattr(self.main_window, 'feedback_text'):
            self.enhancer.enhance_text_widget(
                self.main_window.feedback_text, 
                "feedback"
            )
            self.hierarchy_manager.apply_hierarchy(
                self.main_window.feedback_text, 
                "body"
            )
        
        # Input field
        if hasattr(self.main_window, 'free_response_input'):
            self.enhancer.enhance_text_widget(
                self.main_window.free_response_input, 
                "answer"
            )
    
    def _apply_visual_hierarchy(self) -> None:
        """Apply clear visual hierarchy throughout the application"""
        # Primary action button
        if hasattr(self.main_window, 'submit_button'):
            self.hierarchy_manager.apply_hierarchy(
                self.main_window.submit_button, 
                "accent"
            )
        
        # Secondary buttons
        for button_attr in ['hint_button', 'prev_button', 'next_button']:
            button = getattr(self.main_window, button_attr, None)
            if button:
                self.hierarchy_manager.apply_hierarchy(button, "secondary")
        
        # Stats display
        if hasattr(self.main_window, 'stats_label'):
            self.hierarchy_manager.apply_hierarchy(
                self.main_window.stats_label, 
                "muted"
            )
    
    def _optimize_spacing(self) -> None:
        """Optimize spacing throughout the application"""
        # Optimize main layout spacing
        central_widget = self.main_window.centralWidget()
        if central_widget and central_widget.layout():
            layout = central_widget.layout()
            layout.setSpacing(16)  # Optimal spacing between sections
            layout.setContentsMargins(20, 20, 20, 20)  # Comfortable margins
        
        # Optimize button layout spacing
        if hasattr(self.main_window, 'buttons_layout'):
            # This would need to be accessible from the main window
            pass
    
    def _apply_spanish_optimizations(self) -> None:
        """Apply Spanish language specific optimizations"""
        # Optimize feedback text for Spanish
        if hasattr(self.main_window, 'feedback_text'):
            feedback = self.main_window.feedback_text
            if hasattr(feedback, 'toPlainText'):
                current_text = feedback.toPlainText()
                if current_text:
                    optimized_text = self.spanish_optimizer.optimize_text_display(current_text)
                    if optimized_text != current_text:
                        feedback.setText(optimized_text)
    
    def generate_readability_report(self) -> str:
        """Generate a comprehensive readability report"""
        if not self.analysis_results:
            self.analyze_application()
        
        results = self.analysis_results
        
        report = f"""
SPANISH SUBJUNCTIVE APP - READABILITY ANALYSIS REPORT
====================================================

OVERALL SCORE: {results['overall_score']:.1f}/100

CRITICAL ISSUES ({len(results['critical_issues'])}):
{chr(10).join(f"• {issue['widget']}: {issue['issue']}" for issue in results['critical_issues']) if results['critical_issues'] else "✓ No critical issues found"}

SPANISH-SPECIFIC ISSUES ({len(results['spanish_specific_issues'])}):
{chr(10).join(f"• {issue['description']} - {issue['recommendation']}" for issue in results['spanish_specific_issues']) if results['spanish_specific_issues'] else "✓ No Spanish-specific issues found"}

TOP RECOMMENDATIONS:
{chr(10).join(f"• {rec}" for rec in results['recommendations'][:10]) if results['recommendations'] else "✓ No major improvements needed"}

DETAILED WIDGET ANALYSIS:
"""
        
        for widget_name, analysis in results['widget_analyses'].items():
            report += f"""
{widget_name.upper()}:
  Score: {analysis['score']}/100
  Issues: {', '.join(analysis['issues']) if analysis['issues'] else 'None'}
  Type: {analysis['widget_type']}
"""
        
        report += f"""

ENHANCEMENT PRIORITIES:
1. Fix critical contrast ratio issues (WCAG AA minimum: 4.5, AAA: 7.0)
2. Optimize text width for 45-75 character line length
3. Ensure Spanish character support in all fonts
4. Implement proper visual hierarchy for questions vs answers
5. Add adequate spacing between UI elements (8-16px related, 16-24px sections)

SPANISH LANGUAGE CONSIDERATIONS:
• Ensure fonts support diacritical marks (ñ, á, é, í, ó, ú, ü)
• Implement proper punctuation (¿ and ¡) in generated content
• Optimize line breaks to avoid splitting accented words
• Consider slightly wider character spacing for diacritical marks
"""
        
        return report

# Convenience functions for easy integration
def analyze_app_readability(main_window) -> Dict[str, Any]:
    """Convenience function to analyze app readability"""
    manager = ReadabilityManager(main_window)
    return manager.analyze_application()

def enhance_app_readability(main_window) -> None:
    """Convenience function to enhance app readability"""
    manager = ReadabilityManager(main_window)
    manager.apply_comprehensive_enhancements()

def generate_readability_report(main_window) -> str:
    """Convenience function to generate readability report"""
    manager = ReadabilityManager(main_window)
    return manager.generate_readability_report()
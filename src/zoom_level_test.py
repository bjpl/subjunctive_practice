"""
Zoom Level and Accessibility Testing Script

This script tests the typography fixes at different zoom levels and validates
that text remains readable and interactive elements remain usable across
various magnification levels.
"""

import sys
import os
from typing import Dict, List, Tuple

# Add the parent directory to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QPushButton, QLineEdit, QTextEdit, QGroupBox, QSlider,
        QCheckBox, QComboBox, QProgressBar
    )
    from PyQt5.QtCore import Qt, QTimer
    from PyQt5.QtGui import QFont, QFontMetrics
    
    from src.enhanced_typography_system import AccessibleTypography, create_accessible_typography_system
    from src.typography_size_fixes import apply_typography_size_fixes
    
    MODULES_AVAILABLE = True
    
except ImportError as e:
    print(f"Import error: {e}")
    MODULES_AVAILABLE = False


class ZoomTestWindow(QMainWindow):
    """Test window for validating zoom levels and accessibility."""
    
    def __init__(self):
        super().__init__()
        self.current_zoom = 1.0
        self.test_results = {}
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the test UI with various elements."""
        self.setWindowTitle("Zoom Level Accessibility Test")
        self.setGeometry(100, 100, 1000, 700)
        
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        
        # Title
        title = QLabel("Typography Zoom Level Test")
        title.setProperty('role', 'title')
        main_layout.addWidget(title)
        
        # Zoom controls
        zoom_group = QGroupBox("Zoom Level Controls")
        zoom_layout = QHBoxLayout(zoom_group)
        
        zoom_layout.addWidget(QLabel("Zoom:"))
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setRange(50, 300)  # 50% to 300%
        self.zoom_slider.setValue(100)
        self.zoom_slider.valueChanged.connect(self.on_zoom_changed)
        zoom_layout.addWidget(self.zoom_slider)
        
        self.zoom_label = QLabel("100%")
        zoom_layout.addWidget(self.zoom_label)
        
        main_layout.addWidget(zoom_group)
        
        # Test content
        content_group = QGroupBox("Test Content")
        content_layout = QVBoxLayout(content_group)
        
        # Spanish text samples
        self.spanish_text = QLabel("Es importante que practiques el subjuntivo con acentos: ñ, á, é, í, ó, ú.")
        self.spanish_text.setProperty('role', 'exercise')
        content_layout.addWidget(self.spanish_text)
        
        self.english_text = QLabel("It's important that you practice the subjunctive with accents.")
        self.english_text.setProperty('role', 'translation')
        content_layout.addWidget(self.english_text)
        
        # Interactive elements
        button_layout = QHBoxLayout()
        
        self.small_button = QPushButton("Small")
        self.normal_button = QPushButton("Normal Button")
        self.large_button = QPushButton("Large Primary")
        self.large_button.setProperty('role', 'primary')
        
        button_layout.addWidget(self.small_button)
        button_layout.addWidget(self.normal_button)
        button_layout.addWidget(self.large_button)
        content_layout.addLayout(button_layout)
        
        # Input field
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Test input field with placeholder text")
        content_layout.addWidget(self.input_field)
        
        # Dropdown
        self.dropdown = QComboBox()
        self.dropdown.addItems(["Option 1", "Option 2", "Option 3"])
        content_layout.addWidget(self.dropdown)
        
        # Checkbox
        self.checkbox = QCheckBox("Test checkbox with descriptive label")
        content_layout.addWidget(self.checkbox)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setValue(65)
        content_layout.addWidget(self.progress)
        
        main_layout.addWidget(content_group)
        
        # Test results area
        self.results_text = QTextEdit()
        self.results_text.setMinimumHeight(150)
        main_layout.addWidget(self.results_text)
        
        # Test buttons
        test_layout = QHBoxLayout()
        
        run_test_btn = QPushButton("Run Accessibility Test")
        run_test_btn.clicked.connect(self.run_accessibility_test)
        test_layout.addWidget(run_test_btn)
        
        zoom_test_btn = QPushButton("Run Zoom Test")
        zoom_test_btn.clicked.connect(self.run_zoom_test)
        test_layout.addWidget(zoom_test_btn)
        
        main_layout.addLayout(test_layout)
        
        # Store references for testing
        self.sentence_label = self.spanish_text
        self.translation_label = self.english_text
        self.submit_button = self.large_button
        self.free_response_input = self.input_field
    
    def on_zoom_changed(self, value):
        """Handle zoom level changes."""
        self.current_zoom = value / 100.0
        self.zoom_label.setText(f"{value}%")
        self.apply_zoom_scaling(self.current_zoom)
    
    def apply_zoom_scaling(self, zoom_factor):
        """Apply zoom scaling to all elements."""
        try:
            if hasattr(self, 'theme_manager') and self.theme_manager:
                # Set user font scale based on zoom
                self.theme_manager.set_user_font_scale(zoom_factor)
                
                # Log the change
                self.log_message(f"Applied zoom scaling: {zoom_factor:.1f}x ({zoom_factor * 100:.0f}%)")
            else:
                # Manual scaling fallback
                self._apply_manual_scaling(zoom_factor)
                
        except Exception as e:
            self.log_message(f"Error applying zoom scaling: {e}")
    
    def _apply_manual_scaling(self, zoom_factor):
        """Apply manual font scaling when theme manager is not available."""
        widgets = [
            self.spanish_text, self.english_text, self.small_button,
            self.normal_button, self.large_button, self.input_field,
            self.dropdown, self.checkbox
        ]
        
        for widget in widgets:
            if widget:
                font = widget.font()
                base_size = 16 if not hasattr(widget, '_original_font_size') else widget._original_font_size
                if not hasattr(widget, '_original_font_size'):
                    widget._original_font_size = base_size
                
                new_size = int(base_size * zoom_factor)
                font.setPixelSize(max(10, new_size))  # Minimum 10px
                widget.setFont(font)
    
    def run_accessibility_test(self):
        """Run accessibility compliance test at current zoom level."""
        self.log_message(f"\n🔍 Running Accessibility Test at {self.current_zoom * 100:.0f}% zoom...")
        
        results = {
            'font_sizes': [],
            'touch_targets': [],
            'readability': [],
            'issues': []
        }
        
        # Test font sizes
        labels = [self.spanish_text, self.english_text]
        for label in labels:
            font = label.font()
            size = font.pixelSize() if font.pixelSize() > 0 else font.pointSize() * 1.33
            
            min_required = 14 * self.current_zoom
            if size >= min_required:
                results['font_sizes'].append(f"✅ {label.objectName() or 'Label'}: {size:.0f}px (≥{min_required:.0f}px required)")
            else:
                results['issues'].append(f"❌ {label.objectName() or 'Label'}: {size:.0f}px (below {min_required:.0f}px)")
        
        # Test touch targets
        buttons = [self.small_button, self.normal_button, self.large_button]
        for button in buttons:
            size = button.size()
            min_required = 44 * self.current_zoom
            
            if size.width() >= min_required and size.height() >= min_required:
                results['touch_targets'].append(f"✅ {button.text()}: {size.width()}x{size.height()}px")
            else:
                results['issues'].append(f"❌ {button.text()}: {size.width()}x{size.height()}px (need {min_required:.0f}x{min_required:.0f}px)")
        
        # Test input field height
        input_height = self.input_field.height()
        min_input_height = 44 * self.current_zoom
        if input_height >= min_input_height:
            results['touch_targets'].append(f"✅ Input field: {input_height}px height")
        else:
            results['issues'].append(f"❌ Input field: {input_height}px (need {min_input_height:.0f}px)")
        
        # Test text readability
        spanish_font = self.spanish_text.font()
        metrics = QFontMetrics(spanish_font)
        line_height = metrics.height()
        font_size = spanish_font.pixelSize() if spanish_font.pixelSize() > 0 else spanish_font.pointSize() * 1.33
        
        line_height_ratio = line_height / font_size if font_size > 0 else 1.0
        if line_height_ratio >= 1.4:
            results['readability'].append(f"✅ Line height ratio: {line_height_ratio:.2f} (≥1.4 recommended)")
        else:
            results['issues'].append(f"❌ Line height ratio: {line_height_ratio:.2f} (should be ≥1.4)")
        
        # Display results
        self.display_test_results(results)
    
    def run_zoom_test(self):
        """Run comprehensive zoom level test."""
        self.log_message("\n🔍 Running Comprehensive Zoom Level Test...")
        
        zoom_levels = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0]
        results_summary = {}
        
        for zoom in zoom_levels:
            self.log_message(f"\nTesting at {zoom * 100:.0f}% zoom...")
            
            # Apply zoom
            self.zoom_slider.setValue(int(zoom * 100))
            self.apply_zoom_scaling(zoom)
            
            # Wait for UI to update
            QApplication.processEvents()
            
            # Test this zoom level
            zoom_results = self._test_zoom_level(zoom)
            results_summary[zoom] = zoom_results
            
            # Brief results
            if zoom_results['issues']:
                self.log_message(f"  ⚠️  {len(zoom_results['issues'])} issues found")
            else:
                self.log_message(f"  ✅ All tests passed")
        
        # Summary report
        self.log_message("\n" + "="*50)
        self.log_message("ZOOM LEVEL TEST SUMMARY")
        self.log_message("="*50)
        
        for zoom, results in results_summary.items():
            status = "✅ PASS" if not results['issues'] else f"⚠️  {len(results['issues'])} ISSUES"
            self.log_message(f"{zoom * 100:4.0f}%: {status}")
        
        # Find optimal range
        passing_zooms = [zoom for zoom, results in results_summary.items() if not results['issues']]
        if passing_zooms:
            min_zoom = min(passing_zooms) * 100
            max_zoom = max(passing_zooms) * 100
            self.log_message(f"\n✅ OPTIMAL ZOOM RANGE: {min_zoom:.0f}% - {max_zoom:.0f}%")
        else:
            self.log_message(f"\n❌ NO ZOOM LEVELS FULLY COMPLIANT")
    
    def _test_zoom_level(self, zoom_factor):
        """Test accessibility at a specific zoom level."""
        results = {
            'font_sizes_ok': True,
            'touch_targets_ok': True,
            'readability_ok': True,
            'issues': []
        }
        
        try:
            # Font size test
            font = self.spanish_text.font()
            size = font.pixelSize() if font.pixelSize() > 0 else font.pointSize() * 1.33
            min_size = 14 * zoom_factor
            
            if size < min_size:
                results['font_sizes_ok'] = False
                results['issues'].append(f"Font size {size:.0f}px below minimum {min_size:.0f}px")
            
            # Touch target test
            button_size = self.normal_button.size()
            min_touch = 44 * zoom_factor
            
            if button_size.width() < min_touch or button_size.height() < min_touch:
                results['touch_targets_ok'] = False
                results['issues'].append(f"Touch target {button_size.width()}x{button_size.height()}px below {min_touch:.0f}px")
            
            # Input field test
            input_height = self.input_field.height()
            if input_height < min_touch:
                results['touch_targets_ok'] = False
                results['issues'].append(f"Input height {input_height}px below {min_touch:.0f}px")
            
        except Exception as e:
            results['issues'].append(f"Test error: {e}")
        
        return results
    
    def display_test_results(self, results):
        """Display test results in the results area."""
        output = []
        
        if results['font_sizes']:
            output.append("📝 Font Size Tests:")
            output.extend(f"  {item}" for item in results['font_sizes'])
            output.append("")
        
        if results['touch_targets']:
            output.append("👆 Touch Target Tests:")
            output.extend(f"  {item}" for item in results['touch_targets'])
            output.append("")
        
        if results['readability']:
            output.append("📖 Readability Tests:")
            output.extend(f"  {item}" for item in results['readability'])
            output.append("")
        
        if results['issues']:
            output.append("⚠️ Issues Found:")
            output.extend(f"  {item}" for item in results['issues'])
            output.append("")
        
        if not results['issues']:
            output.append("🎉 All accessibility tests passed!")
        
        self.log_message("\n".join(output))
    
    def log_message(self, message):
        """Add message to results text area."""
        self.results_text.append(message)
        QApplication.processEvents()


def run_zoom_level_tests():
    """Run the zoom level testing application."""
    if not MODULES_AVAILABLE:
        print("❌ Cannot run zoom tests - required modules not available")
        return
    
    app = QApplication(sys.argv)
    
    # Create test window
    window = ZoomTestWindow()
    
    # Apply typography fixes
    try:
        result = apply_typography_size_fixes(window)
        if result['success']:
            window.theme_manager = result.get('theme_manager')
            window.log_message("✅ Typography fixes applied successfully")
            window.log_message(f"📊 Applied {len(result['fixes_applied'])} improvements")
        else:
            window.log_message(f"❌ Typography fixes failed: {result.get('error')}")
    except Exception as e:
        window.log_message(f"❌ Error applying fixes: {e}")
    
    # Initial message
    window.log_message("Typography and Zoom Level Testing Tool")
    window.log_message("="*50)
    window.log_message("Use the zoom slider to test different magnification levels.")
    window.log_message("Click 'Run Accessibility Test' to check current zoom level.")
    window.log_message("Click 'Run Zoom Test' for comprehensive testing.\n")
    
    window.show()
    
    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"Error during testing: {e}")


if __name__ == "__main__":
    run_zoom_level_tests()
"""
Font Manager Integration Example

This module demonstrates how to integrate the FontManager into the Spanish Subjunctive
Practice application and provides examples of best practices for font handling.
"""

import sys
import logging
from typing import Optional

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QSlider, QComboBox, QTextEdit, QGroupBox,
    QCheckBox, QSpinBox, QTabWidget, QScrollArea, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QFont, QPixmap, QPainter, QColor

from font_manager import FontManager, FontConfig, SpanishCharacterValidator

logger = logging.getLogger(__name__)


class FontIntegrationDemo(QMainWindow):
    """
    Demonstration of FontManager integration in a Spanish learning application
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Font Manager Integration Demo - Spanish Subjunctive Practice")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize font manager
        self.font_manager = FontManager(self)
        
        # Connect font change signals
        self.font_manager.fontChanged.connect(self.on_font_changed)
        self.font_manager.sizeChanged.connect(self.on_font_size_changed)
        
        # Spanish test content
        self.spanish_content = {
            'title': 'Práctica del Subjuntivo Español',
            'subtitle': '¡Aprende el subjuntivo de manera efectiva!',
            'sample_text': '''
                El subjuntivo es un modo verbal que expresa duda, deseo, emoción o situaciones hipotéticas.
                
                Ejemplos:
                • Quiero que tú vengas mañana. (deseo)
                • Es posible que llueva hoy. (duda)  
                • Me alegra que hayas llegado. (emoción)
                • Si tuviera dinero, viajaría. (hipótesis)
                
                Caracteres especiales: ñoño, güeña, árbol, corazón, niño, año
            ''',
            'exercise': 'Completa la oración: "Es importante que tú _____ (estudiar) español."',
            'feedback': '¡Excelente! La respuesta correcta es "estudies". El subjuntivo se usa después de expresiones de importancia.'
        }
        
        self.setup_ui()
        self.apply_fonts_to_ui()
    
    def setup_ui(self):
        """Set up the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Left panel: Font controls
        left_panel = self.create_font_control_panel()
        main_layout.addWidget(left_panel, 1)
        
        # Right panel: Content demonstration
        right_panel = self.create_content_panel()
        main_layout.addWidget(right_panel, 2)
        
        # Status bar for debug info
        self.statusBar().showMessage("Font Manager initialized successfully")
    
    def create_font_control_panel(self) -> QWidget:
        """Create the font control panel"""
        panel = QWidget()
        panel.setMaximumWidth(350)
        layout = QVBoxLayout(panel)
        
        # Font selection group
        font_group = QGroupBox("Font Selection")
        font_layout = QVBoxLayout(font_group)
        
        # Font family combo
        font_layout.addWidget(QLabel("Font Family:"))
        self.font_combo = QComboBox()
        available_fonts = self.font_manager.get_available_fonts()
        recommended_fonts = self.font_manager.get_recommended_fonts()
        
        # Add recommended fonts first
        self.font_combo.addItem("--- Recommended for Spanish ---")
        for font_name in recommended_fonts:
            self.font_combo.addItem(f"⭐ {font_name}")
        
        self.font_combo.addItem("--- All Available Fonts ---")
        for font_name in available_fonts:
            if font_name not in recommended_fonts:
                self.font_combo.addItem(font_name)
        
        self.font_combo.currentTextChanged.connect(self.on_font_family_changed)
        font_layout.addWidget(self.font_combo)
        
        # Font size controls
        font_layout.addWidget(QLabel("Base Font Size:"))
        size_layout = QHBoxLayout()
        
        self.size_spinbox = QSpinBox()
        self.size_spinbox.setRange(8, 32)
        self.size_spinbox.setValue(14)
        self.size_spinbox.valueChanged.connect(self.on_font_size_spinbox_changed)
        size_layout.addWidget(self.size_spinbox)
        
        self.size_slider = QSlider(Qt.Horizontal)
        self.size_slider.setRange(8, 32)
        self.size_slider.setValue(14)
        self.size_slider.valueChanged.connect(self.on_font_size_slider_changed)
        size_layout.addWidget(self.size_slider)
        
        font_layout.addLayout(size_layout)
        
        # DPI scaling info
        dpi_info = QLabel(f"DPI Scale: {self.font_manager.dpi_manager.get_dpi_scale():.2f}")\n        dpi_info.setStyleSheet("color: gray; font-size: 11px;")\n        font_layout.addWidget(dpi_info)\n        \n        layout.addWidget(font_group)\n        \n        # Spanish character test group\n        spanish_group = QGroupBox("Spanish Character Support")\n        spanish_layout = QVBoxLayout(spanish_group)\n        \n        self.character_test_label = QLabel("Testing...")\n        self.character_test_label.setWordWrap(True)\n        spanish_layout.addWidget(self.character_test_label)\n        \n        test_button = QPushButton("Test Current Font")\n        test_button.clicked.connect(self.test_spanish_characters)\n        spanish_layout.addWidget(test_button)\n        \n        layout.addWidget(spanish_group)\n        \n        # Debug info group\n        debug_group = QGroupBox("Debug Information")\n        debug_layout = QVBoxLayout(debug_group)\n        \n        self.debug_text = QTextEdit()\n        self.debug_text.setMaximumHeight(200)\n        self.debug_text.setReadOnly(True)\n        debug_layout.addWidget(self.debug_text)\n        \n        refresh_debug_btn = QPushButton("Refresh Debug Info")\n        refresh_debug_btn.clicked.connect(self.update_debug_info)\n        debug_layout.addWidget(refresh_debug_btn)\n        \n        layout.addWidget(debug_group)\n        \n        # Performance test\n        perf_group = QGroupBox("Performance Test")\n        perf_layout = QVBoxLayout(perf_group)\n        \n        perf_button = QPushButton("Run Font Performance Test")\n        perf_button.clicked.connect(self.run_performance_test)\n        perf_layout.addWidget(perf_button)\n        \n        self.perf_results = QLabel("No test results yet")\n        self.perf_results.setWordWrap(True)\n        perf_layout.addWidget(self.perf_results)\n        \n        layout.addWidget(perf_group)\n        \n        layout.addStretch()\n        \n        return panel\n    \n    def create_content_panel(self) -> QWidget:\n        """Create the content demonstration panel"""\n        panel = QWidget()\n        layout = QVBoxLayout(panel)\n        \n        # Create tabs for different content types\n        tabs = QTabWidget()\n        \n        # Text content tab\n        text_tab = self.create_text_content_tab()\n        tabs.addTab(text_tab, "Text Content")\n        \n        # Exercise simulation tab\n        exercise_tab = self.create_exercise_tab()\n        tabs.addTab(exercise_tab, "Exercise Simulation")\n        \n        # Font comparison tab\n        comparison_tab = self.create_font_comparison_tab()\n        tabs.addTab(comparison_tab, "Font Comparison")\n        \n        layout.addWidget(tabs)\n        \n        return panel\n    \n    def create_text_content_tab(self) -> QWidget:\n        """Create tab with text content for font testing"""\n        tab = QWidget()\n        layout = QVBoxLayout(tab)\n        \n        # Title\n        self.title_label = QLabel(self.spanish_content['title'])\n        layout.addWidget(self.title_label)\n        \n        # Subtitle\n        self.subtitle_label = QLabel(self.spanish_content['subtitle'])\n        layout.addWidget(self.subtitle_label)\n        \n        # Separator\n        layout.addWidget(QLabel("─" * 80))\n        \n        # Main content\n        self.content_text = QTextEdit()\n        self.content_text.setPlainText(self.spanish_content['sample_text'])\n        self.content_text.setMinimumHeight(400)\n        layout.addWidget(self.content_text)\n        \n        return tab\n    \n    def create_exercise_tab(self) -> QWidget:\n        """Create tab simulating exercise interface"""\n        tab = QWidget()\n        layout = QVBoxLayout(tab)\n        \n        # Exercise question\n        exercise_group = QGroupBox("Exercise")\n        exercise_layout = QVBoxLayout(exercise_group)\n        \n        self.exercise_label = QLabel(self.spanish_content['exercise'])\n        self.exercise_label.setWordWrap(True)\n        exercise_layout.addWidget(self.exercise_label)\n        \n        # Answer input simulation\n        answer_label = QLabel("Your answer:")\n        exercise_layout.addWidget(answer_label)\n        \n        from PyQt5.QtWidgets import QLineEdit\n        self.answer_input = QLineEdit()\n        self.answer_input.setPlaceholderText("Type your answer here...")\n        exercise_layout.addWidget(self.answer_input)\n        \n        layout.addWidget(exercise_group)\n        \n        # Feedback section\n        feedback_group = QGroupBox("Feedback")\n        feedback_layout = QVBoxLayout(feedback_group)\n        \n        self.feedback_label = QLabel(self.spanish_content['feedback'])\n        self.feedback_label.setWordWrap(True)\n        feedback_layout.addWidget(self.feedback_label)\n        \n        layout.addWidget(feedback_group)\n        \n        layout.addStretch()\n        \n        return tab\n    \n    def create_font_comparison_tab(self) -> QWidget:\n        """Create tab comparing different fonts"""\n        tab = QWidget()\n        layout = QVBoxLayout(tab)\n        \n        scroll_area = QScrollArea()\n        scroll_widget = QWidget()\n        scroll_layout = QVBoxLayout(scroll_widget)\n        \n        test_text = "¡Hola! ¿Cómo estás? Ñoño güeña años corazón"\n        \n        # Compare top 5 Spanish fonts\n        recommended_fonts = self.font_manager.get_recommended_fonts()[:5]\n        \n        for font_name in recommended_fonts:\n            # Get Spanish support info\n            support_info = self.font_manager.get_spanish_character_support(font_name)\n            \n            group = QGroupBox(f"{font_name} (Support: {support_info.quality_score:.1%})")\n            group_layout = QVBoxLayout(group)\n            \n            # Sample text with this font\n            sample_label = QLabel(test_text)\n            font = QFont(font_name, 14)\n            sample_label.setFont(font)\n            group_layout.addWidget(sample_label)\n            \n            # Support details\n            if support_info.missing_chars:\n                missing_label = QLabel(f"Missing: {', '.join(support_info.missing_chars)}")\n                missing_label.setStyleSheet("color: #DC2626; font-size: 11px;")\n                group_layout.addWidget(missing_label)\n            else:\n                complete_label = QLabel("✓ Complete Spanish support")\n                complete_label.setStyleSheet("color: green; font-size: 11px;")\n                group_layout.addWidget(complete_label)\n            \n            scroll_layout.addWidget(group)\n        \n        scroll_area.setWidget(scroll_widget)\n        layout.addWidget(scroll_area)\n        \n        return tab\n    \n    def apply_fonts_to_ui(self):\n        """Apply font manager fonts to UI elements"""\n        # Apply different font sizes to different UI elements\n        self.font_manager.apply_font_to_widget(self.title_label, 'extra_large', QFont.Bold)\n        self.font_manager.apply_font_to_widget(self.subtitle_label, 'large', QFont.Normal, True)\n        self.font_manager.apply_font_to_widget(self.content_text, 'normal')\n        self.font_manager.apply_font_to_widget(self.exercise_label, 'medium')\n        self.font_manager.apply_font_to_widget(self.feedback_label, 'normal')\n        \n        # Update debug info\n        self.update_debug_info()\n        self.test_spanish_characters()\n    \n    @pyqtSlot()\n    def on_font_changed(self):\n        """Handle font change signal"""\n        self.apply_fonts_to_ui()\n        self.statusBar().showMessage("Font changed successfully", 2000)\n    \n    @pyqtSlot(int)\n    def on_font_size_changed(self, size: int):\n        """Handle font size change signal"""\n        # Update spinbox and slider without triggering signals\n        self.size_spinbox.blockSignals(True)\n        self.size_slider.blockSignals(True)\n        \n        self.size_spinbox.setValue(size)\n        self.size_slider.setValue(size)\n        \n        self.size_spinbox.blockSignals(False)\n        self.size_slider.blockSignals(False)\n        \n        self.apply_fonts_to_ui()\n    \n    def on_font_family_changed(self, font_name: str):\n        """Handle font family selection change"""\n        if font_name.startswith("---") or font_name.startswith("⭐"):\n            font_name = font_name.replace("⭐ ", "").strip()\n        \n        if font_name in self.font_manager.get_available_fonts():\n            self.font_manager.set_font_family(font_name)\n            self.statusBar().showMessage(f"Font changed to {font_name}", 2000)\n    \n    def on_font_size_spinbox_changed(self, size: int):\n        """Handle font size spinbox change"""\n        self.size_slider.setValue(size)\n        self.font_manager.set_base_font_size(size)\n    \n    def on_font_size_slider_changed(self, size: int):\n        """Handle font size slider change"""\n        self.size_spinbox.setValue(size)\n        self.font_manager.set_base_font_size(size)\n    \n    def test_spanish_characters(self):\n        """Test Spanish character support in current font"""\n        config = self.font_manager.get_current_configuration()\n        if not config:\n            self.character_test_label.setText("No font configuration available")\n            return\n        \n        support_info = self.font_manager.get_spanish_character_support(config.family)\n        \n        if support_info.supports_spanish:\n            result_text = f"✓ {config.family} has complete Spanish support ({support_info.quality_score:.1%})"\n            self.character_test_label.setStyleSheet("color: green;")\n        else:\n            missing = ", ".join(support_info.missing_chars)\n            result_text = f"⚠ {config.family} missing: {missing} ({support_info.quality_score:.1%} support)"\n            self.character_test_label.setStyleSheet("color: orange;")\n        \n        self.character_test_label.setText(result_text)\n    \n    def update_debug_info(self):\n        """Update debug information display"""\n        debug_info = self.font_manager.get_debug_info()\n        \n        formatted_info = f\"\"\"\nCurrent Configuration:\n• Family: {debug_info['current_config']['family'] if debug_info['current_config'] else 'None'}\n• Size: {debug_info['current_config']['size'] if debug_info['current_config'] else 'None'}pt\n• DPI Scale: {debug_info['dpi_scale']:.2f}\n• System DPI: {debug_info['system_dpi']}\n\nSystem Information:\n• Platform: {debug_info['platform']}\n• Available Fonts: {debug_info['available_fonts_count']}\n• Spanish-optimized Fonts: {debug_info['spanish_fonts_count']}\n• Windows Features: {debug_info['windows_available']}\n\nPerformance:\n• Font Cache Size: {debug_info['font_cache_size']}\n• Metrics Cache Size: {debug_info['metrics_cache_size']}\n\nTop Spanish Fonts:\n{chr(10).join([f'• {name}: {score:.1%}' for name, score in debug_info['top_spanish_fonts']])}\n        \"\"\".strip()\n        \n        self.debug_text.setPlainText(formatted_info)\n    \n    def run_performance_test(self):\n        \"\"\"Run a performance test on font operations\"\"\"\n        import time\n        \n        self.perf_results.setText("Running performance test...")\n        QApplication.processEvents()\n        \n        # Test font creation performance\n        start_time = time.time()\n        test_fonts = []\n        \n        for i in range(100):\n            font = self.font_manager.get_font('normal')\n            metrics = self.font_manager.get_font_metrics(font)\n            test_fonts.append((font, metrics))\n        \n        creation_time = time.time() - start_time\n        \n        # Test Spanish character validation\n        start_time = time.time()\n        validator = SpanishCharacterValidator()\n        \n        test_results = []\n        for font_name in self.font_manager.get_recommended_fonts()[:10]:\n            result = validator.validate_spanish_support(QFont(font_name))\n            test_results.append(result)\n        \n        validation_time = time.time() - start_time\n        \n        # Display results\n        results_text = f\"\"\"\nPerformance Test Results:\n\n• Font Creation (100 fonts): {creation_time:.3f}s\n• Avg per font: {creation_time/100*1000:.2f}ms\n• Spanish Validation (10 fonts): {validation_time:.3f}s\n• Avg per validation: {validation_time/10*1000:.2f}ms\n\nCache Status:\n• Font cache size: {len(self.font_manager._font_cache)}\n• Metrics cache size: {len(self.font_manager._metrics_cache)}\n        \"\"\".strip()\n        \n        self.perf_results.setText(results_text)\n\n\ndef main():\n    \"\"\"Main function to run the font integration demo\"\"\"\n    # Set up logging\n    logging.basicConfig(\n        level=logging.INFO,\n        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'\n    )\n    \n    # Create application\n    app = QApplication(sys.argv)\n    \n    # Create and show demo window\n    demo = FontIntegrationDemo()\n    demo.show()\n    \n    # Run application\n    sys.exit(app.exec_())\n\n\nif __name__ == "__main__":\n    main()
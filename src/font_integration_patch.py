"""
Font Manager Integration Patch for Spanish Subjunctive Practice App

This module provides a simple way to integrate the FontManager into the existing
main.py application with minimal code changes.
"""

import logging
from typing import Optional

from PyQt5.QtWidgets import QMainWindow, QWidget, QAction, QDialog, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QLabel, QPushButton, QSlider, QComboBox, QGroupBox, QCheckBox
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QFont

from font_manager import FontManager

logger = logging.getLogger(__name__)


class FontSettingsDialog(QDialog):
    """
    Font settings dialog for the Spanish Subjunctive Practice app
    """
    
    def __init__(self, font_manager: FontManager, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.font_manager = font_manager
        self.setWindowTitle("Font Settings")
        self.setModal(True)
        self.setMinimumSize(500, 400)
        
        self.setup_ui()
        self.load_current_settings()
    
    def setup_ui(self):
        """Set up the dialog UI"""
        layout = QVBoxLayout(self)
        
        # Font family selection
        family_group = QGroupBox("Font Family")
        family_layout = QVBoxLayout(family_group)
        
        family_layout.addWidget(QLabel("Choose a font optimized for Spanish characters:"))
        
        self.family_combo = QComboBox()
        
        # Add recommended fonts first
        recommended_fonts = self.font_manager.get_recommended_fonts()
        self.family_combo.addItem("--- Recommended for Spanish ---")
        self.family_combo.insertSeparator(1)
        
        for font_name in recommended_fonts:
            support_info = self.font_manager.get_spanish_character_support(font_name)
            display_name = f"⭐ {font_name} ({support_info.quality_score:.0%} support)"
            self.family_combo.addItem(display_name, font_name)
        
        self.family_combo.insertSeparator(self.family_combo.count())
        self.family_combo.addItem("--- Other Available Fonts ---")
        self.family_combo.insertSeparator(self.family_combo.count())
        
        # Add other fonts
        all_fonts = self.font_manager.get_available_fonts()
        for font_name in all_fonts:
            if font_name not in recommended_fonts:
                self.family_combo.addItem(font_name, font_name)
        
        self.family_combo.currentIndexChanged.connect(self.on_font_family_changed)
        family_layout.addWidget(self.family_combo)
        
        # Font support indicator
        self.support_label = QLabel("")
        family_layout.addWidget(self.support_label)
        
        layout.addWidget(family_group)
        
        # Font size selection
        size_group = QGroupBox("Font Size")
        size_layout = QVBoxLayout(size_group)
        
        size_layout.addWidget(QLabel("Adjust the base font size:"))\n        \n        size_control_layout = QHBoxLayout()\n        \n        self.size_slider = QSlider(Qt.Horizontal)\n        self.size_slider.setRange(10, 24)\n        self.size_slider.setValue(14)\n        self.size_slider.valueChanged.connect(self.on_size_changed)\n        size_control_layout.addWidget(self.size_slider)\n        \n        self.size_label = QLabel("14pt")\n        self.size_label.setMinimumWidth(50)\n        size_control_layout.addWidget(self.size_label)\n        \n        size_layout.addLayout(size_control_layout)\n        \n        # DPI info\n        dpi_scale = self.font_manager.dpi_manager.get_dpi_scale()\n        dpi_info = QLabel(f"DPI Scaling: {dpi_scale:.1%} (System DPI: {self.font_manager.dpi_manager.system_dpi})")\n        dpi_info.setStyleSheet("color: gray; font-size: 11px;")\n        size_layout.addWidget(dpi_info)\n        \n        layout.addWidget(size_group)\n        \n        # Spanish character test\n        test_group = QGroupBox("Spanish Character Test")\n        test_layout = QVBoxLayout(test_group)\n        \n        test_text = "Sample: ¡Hola! ¿Cómo estás? Ñoño güeña años corazón"\n        self.test_label = QLabel(test_text)\n        self.test_label.setStyleSheet("border: 1px solid gray; padding: 10px; background: white;")\n        test_layout.addWidget(self.test_label)\n        \n        layout.addWidget(test_group)\n        \n        # Buttons\n        button_layout = QHBoxLayout()\n        \n        reset_button = QPushButton("Reset to Default")\n        reset_button.clicked.connect(self.reset_to_default)\n        button_layout.addWidget(reset_button)\n        \n        button_layout.addStretch()\n        \n        cancel_button = QPushButton("Cancel")\n        cancel_button.clicked.connect(self.reject)\n        button_layout.addWidget(cancel_button)\n        \n        ok_button = QPushButton("OK")\n        ok_button.clicked.connect(self.accept)\n        ok_button.setDefault(True)\n        button_layout.addWidget(ok_button)\n        \n        layout.addLayout(button_layout)\n    \n    def load_current_settings(self):\n        \"\"\"Load current font settings into the dialog\"\"\"\n        config = self.font_manager.get_current_configuration()\n        if not config:\n            return\n        \n        # Find and select current font family\n        for i in range(self.family_combo.count()):\n            if self.family_combo.itemData(i) == config.family:\n                self.family_combo.setCurrentIndex(i)\n                break\n        \n        # Set current size\n        self.size_slider.setValue(config.size)\n        self.size_label.setText(f"{config.size}pt")\n        \n        # Update test label\n        self.update_test_label()\n    \n    def on_font_family_changed(self, index: int):\n        \"\"\"Handle font family change\"\"\"\n        font_name = self.family_combo.itemData(index)\n        if not font_name:\n            return\n        \n        # Update support info\n        support_info = self.font_manager.get_spanish_character_support(font_name)\n        \n        if support_info.supports_spanish:\n            self.support_label.setText(f"✓ Complete Spanish support ({support_info.quality_score:.0%})")\n            self.support_label.setStyleSheet("color: green;")\n        else:\n            missing = ", ".join(support_info.missing_chars[:5])  # Show first 5\n            if len(support_info.missing_chars) > 5:\n                missing += "..."\n            self.support_label.setText(f"⚠ Missing characters: {missing} ({support_info.quality_score:.0%} support)")\n            self.support_label.setStyleSheet("color: orange;")\n        \n        self.update_test_label()\n    \n    def on_size_changed(self, size: int):\n        \"\"\"Handle font size change\"\"\"\n        self.size_label.setText(f"{size}pt")\n        self.update_test_label()\n    \n    def update_test_label(self):\n        \"\"\"Update the test label with current font settings\"\"\"\n        font_name = self.family_combo.currentData()\n        if not font_name:\n            return\n        \n        size = self.size_slider.value()\n        scaled_size = self.font_manager.dpi_manager.get_scaled_size(size)\n        \n        font = QFont(font_name, scaled_size)\n        self.test_label.setFont(font)\n    \n    def reset_to_default(self):\n        \"\"\"Reset to default font settings\"\"\"\n        # Get best Spanish font\n        recommended_fonts = self.font_manager.get_recommended_fonts()\n        if recommended_fonts:\n            best_font = recommended_fonts[0]\n            \n            # Find and select it\n            for i in range(self.family_combo.count()):\n                if self.family_combo.itemData(i) == best_font:\n                    self.family_combo.setCurrentIndex(i)\n                    break\n        \n        # Reset size\n        self.size_slider.setValue(14)\n    \n    def accept(self):\n        \"\"\"Apply settings and close dialog\"\"\"\n        font_name = self.family_combo.currentData()\n        size = self.size_slider.value()\n        \n        if font_name:\n            self.font_manager.set_font_family(font_name)\n        \n        self.font_manager.set_base_font_size(size)\n        \n        super().accept()\n\n\nclass FontIntegrationMixin:\n    \"\"\"\n    Mixin class to add font management capabilities to the main application window.\n    \n    Usage:\n        class SpanishSubjunctivePracticeGUI(FontIntegrationMixin, QMainWindow):\n            def __init__(self):\n                super().__init__()\n                # ... existing initialization code ...\n                self.initialize_font_manager()\n                self.apply_font_management()\n    \"\"\"\n    \n    def initialize_font_manager(self):\n        \"\"\"Initialize font manager and add to the main window\"\"\"\n        try:\n            self.font_manager = FontManager(self)\n            \n            # Connect font change signals\n            self.font_manager.fontChanged.connect(self.on_font_changed)\n            self.font_manager.sizeChanged.connect(self.on_font_size_changed)\n            \n            logger.info("Font manager initialized successfully")\n            \n        except Exception as e:\n            logger.error(f"Failed to initialize font manager: {e}")\n            self.font_manager = None\n    \n    def apply_font_management(self):\n        \"\"\"Apply font management to the UI elements\"\"\"\n        if not hasattr(self, 'font_manager') or not self.font_manager:\n            return\n        \n        try:\n            # Apply fonts to main UI elements if they exist\n            if hasattr(self, 'sentence_label'):\n                self.font_manager.apply_font_to_widget(self.sentence_label, 'large')\n            \n            if hasattr(self, 'translation_label'):\n                self.font_manager.apply_font_to_widget(self.translation_label, 'normal', QFont.Normal, True)\n            \n            if hasattr(self, 'feedback_text'):\n                self.font_manager.apply_font_to_widget(self.feedback_text, 'normal')\n            \n            if hasattr(self, 'free_response_input'):\n                self.font_manager.apply_font_to_widget(self.free_response_input, 'medium')\n            \n            # Apply to buttons\n            for attr_name in ['submit_button', 'next_button', 'prev_button', 'hint_button']:\n                if hasattr(self, attr_name):\n                    button = getattr(self, attr_name)\n                    self.font_manager.apply_font_to_widget(button, 'normal', QFont.DemiBold)\n            \n            logger.info("Font management applied to UI elements")\n            \n        except Exception as e:\n            logger.error(f"Error applying font management: {e}")\n    \n    def add_font_menu_actions(self):\n        \"\"\"Add font-related actions to the application menu/toolbar\"\"\"\n        if not hasattr(self, 'font_manager') or not self.font_manager:\n            return\n        \n        try:\n            # Add to existing toolbar if it exists\n            if hasattr(self, 'addToolBar'):\n                # Font settings action\n                font_settings_action = QAction("Font Settings", self)\n                font_settings_action.setToolTip("Configure font settings for better Spanish character display")\n                font_settings_action.triggered.connect(self.show_font_settings)\n                \n                # Find toolbar or create one\n                toolbars = self.findChildren(type(self.toolBar())) if hasattr(self, 'toolBar') else []\n                if toolbars:\n                    toolbars[0].addAction(font_settings_action)\n                else:\n                    # Create a new toolbar\n                    font_toolbar = self.addToolBar("Font")\n                    font_toolbar.addAction(font_settings_action)\n        \n        except Exception as e:\n            logger.error(f"Error adding font menu actions: {e}")\n    \n    def show_font_settings(self):\n        \"\"\"Show font settings dialog\"\"\"\n        if not hasattr(self, 'font_manager') or not self.font_manager:\n            return\n        \n        try:\n            dialog = FontSettingsDialog(self.font_manager, self)\n            if dialog.exec_() == QDialog.Accepted:\n                # Font settings were applied in the dialog\n                self.apply_font_management()  # Reapply to all UI elements\n                \n                if hasattr(self, 'updateStatus'):\n                    self.updateStatus("Font settings updated successfully")\n        \n        except Exception as e:\n            logger.error(f"Error showing font settings dialog: {e}")\n    \n    @pyqtSlot(QFont)\n    def on_font_changed(self, font: QFont):\n        \"\"\"Handle font change signal\"\"\"\n        # Reapply fonts to UI elements\n        self.apply_font_management()\n        \n        if hasattr(self, 'updateStatus'):\n            self.updateStatus(f"Font changed to {font.family()}")\n    \n    @pyqtSlot(int)\n    def on_font_size_changed(self, size: int):\n        \"\"\"Handle font size change signal\"\"\"\n        # Reapply fonts to UI elements\n        self.apply_font_management()\n        \n        if hasattr(self, 'updateStatus'):\n            self.updateStatus(f"Font size changed to {size}pt")\n\n\n# Example integration code for existing main.py\nINTEGRATION_EXAMPLE = '''\n# Add these imports to the top of main.py:\nfrom src.font_integration_patch import FontIntegrationMixin, FontSettingsDialog\n\n# Modify the class declaration:\nclass SpanishSubjunctivePracticeGUI(FontIntegrationMixin, QMainWindow):\n    def __init__(self) -> None:\n        super().__init__()\n        \n        # ... existing initialization code ...\n        \n        # Add font manager initialization after UI setup\n        self.initialize_font_manager()\n        self.apply_font_management()\n        self.add_font_menu_actions()\n\n# That\'s it! The font manager is now integrated.\n'''\n\n\nif __name__ == "__main__":\n    print("Font Integration Patch for Spanish Subjunctive Practice App")\n    print("=" * 60)\n    print()\n    print("To integrate the font manager into your existing application:")\n    print(INTEGRATION_EXAMPLE)\n    \n    # You can also run a simple test\n    import sys\n    from PyQt5.QtWidgets import QApplication\n    \n    app = QApplication(sys.argv)\n    \n    # Create a test window\n    class TestWindow(FontIntegrationMixin, QMainWindow):\n        def __init__(self):\n            super().__init__()\n            self.setWindowTitle("Font Integration Test")\n            \n            # Add a simple label for testing\n            self.sentence_label = QLabel("¡Hola! ¿Cómo estás? Ñoño güeña años")\n            self.setCentralWidget(self.sentence_label)\n            \n            # Initialize font management\n            self.initialize_font_manager()\n            self.apply_font_management()\n            self.add_font_menu_actions()\n    \n    window = TestWindow()\n    window.show()\n    \n    sys.exit(app.exec_())
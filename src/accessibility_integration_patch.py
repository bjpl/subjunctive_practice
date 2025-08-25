"""
Accessibility Integration Patch

This module patches the accessibility integration to fix the identified runtime errors:
1. Toolbar attribute error ('SpanishSubjunctivePracticeGUI' object has no attribute 'toolBar')
2. QCheckBox not defined error in accessibility startup check

Author: Claude Code
Date: 2025-08-25
"""

import logging
from typing import Optional, Any
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QApplication, QMessageBox, QCheckBox, 
    QAction, QToolBar, QDialog, QVBoxLayout, QLabel, QPushButton
)
from PyQt5.QtCore import QObject, QEvent, Qt

logger = logging.getLogger(__name__)


def patch_accessibility_integration():
    """Apply patches to fix accessibility integration issues"""
    
    try:
        # Import the original module
        from src import accessibility_integration
        
        # Patch the add_accessibility_menu_items function
        original_add_menu = getattr(accessibility_integration.AccessibilityIntegration, '_add_accessibility_menu_items', None)
        if original_add_menu:
            accessibility_integration.AccessibilityIntegration._add_accessibility_menu_items = safe_add_accessibility_menu_items
            logger.info("Patched _add_accessibility_menu_items method")
        
        # Patch the startup check function if it exists
        if hasattr(accessibility_integration, 'add_accessibility_startup_check'):
            original_startup = accessibility_integration.add_accessibility_startup_check
            accessibility_integration.add_accessibility_startup_check = safe_accessibility_startup_check
            logger.info("Patched add_accessibility_startup_check function")
        
        return True
        
    except ImportError:
        logger.warning("Accessibility integration module not found")
        return False
    except Exception as e:
        logger.error(f"Failed to patch accessibility integration: {e}")
        return False


def safe_add_accessibility_menu_items(self):
    """Safe version of _add_accessibility_menu_items with proper error handling"""
    try:
        # Safely get or create toolbar
        toolbar = get_or_create_toolbar(self.main_window)
        if not toolbar:
            logger.warning("No toolbar available for accessibility menu items")
            return
        
        # Add separator
        toolbar.addSeparator()
        
        # Create accessibility actions safely
        actions_data = [
            ("Accessibility Settings", "Configure accessibility options (Ctrl+Alt+A)", 
             "Ctrl+Alt+A", "show_accessibility_settings"),
            ("High Contrast", "Toggle high contrast mode (Ctrl+Alt+H)", 
             "Ctrl+Alt+H", "toggle_high_contrast"),
            ("Keyboard Help", "Show keyboard shortcuts (F1)", 
             "F1", "show_keyboard_help")
        ]
        
        for text, tooltip, shortcut, method_name in actions_data:
            try:
                action = QAction(text, self.main_window)
                action.setToolTip(tooltip)
                action.setShortcut(shortcut)
                
                # Connect to accessibility manager method if available
                if self.accessibility_manager and hasattr(self.accessibility_manager, method_name):
                    action.triggered.connect(getattr(self.accessibility_manager, method_name))
                
                toolbar.addAction(action)
                logger.debug(f"Added accessibility action: {text}")
                
            except Exception as e:
                logger.error(f"Failed to add accessibility action {text}: {e}")
        
        logger.info("Accessibility menu items added successfully")
        
    except Exception as e:
        logger.error(f"Error adding accessibility menu items: {e}")


def get_or_create_toolbar(main_window):
    """Safely get or create a toolbar for the main window"""
    try:
        # Check for existing toolbar using various common attribute names
        toolbar_attrs = ['toolbar', 'toolBar', 'main_toolbar', 'mainToolBar']
        
        for attr in toolbar_attrs:
            if hasattr(main_window, attr):
                toolbar = getattr(main_window, attr)
                if toolbar and hasattr(toolbar, 'addAction'):
                    return toolbar
        
        # Try to find existing toolbar in children
        toolbars = main_window.findChildren(QToolBar)
        if toolbars:
            return toolbars[0]
        
        # Create new toolbar as last resort
        toolbar = QToolBar("Accessibility Toolbar")
        main_window.addToolBar(toolbar)
        logger.info("Created new accessibility toolbar")
        return toolbar
        
    except Exception as e:
        logger.error(f"Failed to get or create toolbar: {e}")
        return None


def safe_accessibility_startup_check(main_window, accessibility_manager):
    """Safe version of accessibility startup check with proper imports"""
    try:
        # Ensure all required imports are available locally
        from PyQt5.QtWidgets import QCheckBox, QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox
        
        # Get or create settings manager
        settings_manager = getattr(accessibility_manager, 'settings', None)
        if not settings_manager:
            logger.warning("Settings manager not available for accessibility startup check")
            return
        
        # Check if intro should be shown
        if settings_manager.get("accessibility_intro_shown", False):
            return  # Already shown
        
        # Create and show intro dialog
        try:
            msg = QMessageBox(main_window)
            msg.setWindowTitle("Accessibility Features Available")
            msg.setIcon(QMessageBox.Information)
            msg.setText(
                "This application includes accessibility features:\n\n"
                "• High contrast themes\n"
                "• Keyboard navigation\n" 
                "• Screen reader support\n"
                "• Customizable font sizes\n\n"
                "Access settings through Ctrl+Alt+A or the toolbar."
            )
            msg.setStandardButtons(QMessageBox.Ok)
            
            # Add "Don't show again" checkbox safely
            dont_show_checkbox = QCheckBox("Don't show this message again")
            dont_show_checkbox.setAccessibleDescription("Check to skip this message on startup")
            msg.setCheckBox(dont_show_checkbox)
            
            msg.exec_()
            
            # Save preference
            if dont_show_checkbox.isChecked():
                settings_manager.set("accessibility_intro_shown", True)
                
            logger.info("Accessibility startup check completed")
            
        except Exception as dialog_error:
            logger.error(f"Error showing accessibility intro dialog: {dialog_error}")
        
        # Apply saved accessibility preferences
        try:
            if settings_manager.get("high_contrast", False):
                if hasattr(accessibility_manager, 'theme_manager'):
                    accessibility_manager.theme_manager.apply_theme(main_window, "high_contrast")
            
            # Announce ready status if enabled
            if settings_manager.get("auto_announce", True):
                if hasattr(accessibility_manager, 'announce'):
                    accessibility_manager.announce("Accessibility features ready")
                    
        except Exception as prefs_error:
            logger.error(f"Error applying accessibility preferences: {prefs_error}")
        
    except ImportError as import_error:
        logger.error(f"Failed to import required PyQt5 widgets for accessibility startup: {import_error}")
    except Exception as e:
        logger.error(f"Error in accessibility startup check: {e}")


def create_fallback_accessibility_manager():
    """Create a minimal fallback accessibility manager if the main one fails"""
    
    class FallbackAccessibilityManager:
        """Minimal fallback accessibility manager"""
        
        def __init__(self, main_window):
            self.main_window = main_window
            self.settings = {}
        
        def show_accessibility_settings(self):
            """Show basic accessibility info"""
            try:
                QMessageBox.information(
                    self.main_window,
                    "Accessibility Settings",
                    "Basic accessibility features are available.\n\n"
                    "Use keyboard navigation with Tab and Enter keys.\n"
                    "Screen reader support is enabled."
                )
            except Exception as e:
                logger.error(f"Error showing accessibility settings: {e}")
        
        def toggle_high_contrast(self):
            """Toggle basic high contrast"""
            try:
                current_style = self.main_window.styleSheet()
                if "background-color: #000000" in current_style:
                    # Switch to normal
                    self.main_window.setStyleSheet("")
                else:
                    # Switch to high contrast
                    self.main_window.setStyleSheet("""
                        QMainWindow, QWidget { 
                            background-color: #000000; 
                            color: #FFFFFF; 
                        }
                        QPushButton { 
                            background-color: #FFFFFF; 
                            color: #000000; 
                            border: 2px solid #FFFFFF;
                        }
                    """)
                logger.info("High contrast toggled")
            except Exception as e:
                logger.error(f"Error toggling high contrast: {e}")
        
        def show_keyboard_help(self):
            """Show keyboard shortcuts"""
            try:
                QMessageBox.information(
                    self.main_window,
                    "Keyboard Help",
                    "Keyboard Shortcuts:\n\n"
                    "Tab - Navigate between elements\n"
                    "Enter/Return - Submit answer\n"
                    "Left/Right Arrow - Previous/Next exercise\n"
                    "H - Show hint\n"
                    "Ctrl+Alt+A - Accessibility settings\n"
                    "Ctrl+Alt+H - High contrast mode\n"
                    "F1 - This help"
                )
            except Exception as e:
                logger.error(f"Error showing keyboard help: {e}")
    
    return FallbackAccessibilityManager


# Integration function for the main application
def integrate_patched_accessibility(main_window):
    """Integrate patched accessibility features into the main application"""
    try:
        # Apply patches first
        if not patch_accessibility_integration():
            logger.warning("Failed to apply accessibility patches, using fallback")
            fallback_manager_class = create_fallback_accessibility_manager()
            return fallback_manager_class(main_window)
        
        # Try to use the original integration
        try:
            from src.accessibility_integration import AccessibilityIntegration
            integration = AccessibilityIntegration(main_window)
            return integration.initialize()
        except Exception as e:
            logger.error(f"Failed to initialize patched accessibility: {e}")
            fallback_manager_class = create_fallback_accessibility_manager()
            return fallback_manager_class(main_window)
    
    except Exception as e:
        logger.error(f"Failed to integrate accessibility features: {e}")
        return None


if __name__ == "__main__":
    # Test the patches
    logging.basicConfig(level=logging.INFO)
    success = patch_accessibility_integration()
    print(f"Accessibility patches applied: {success}")
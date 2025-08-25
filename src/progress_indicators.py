"""
Progress Indicators Module for Spanish Subjunctive Practice App

This module provides comprehensive progress indicators for API calls including:
- Animated spinning indicators for indeterminate progress
- Progress bars for determinate operations  
- Loading overlays that disable UI during async operations
- Error state handling with user feedback
- Customizable loading messages and timeouts
"""

import sys
import time
from typing import Optional, Callable, Any
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QProgressBar, QFrame, QGraphicsOpacityEffect, QApplication
)
from PyQt5.QtCore import (
    Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect, 
    pyqtSignal, QObject, QThread, QMutex, QMutexLocker
)
from PyQt5.QtGui import QPainter, QPen, QColor, QFont, QPalette


class SpinnerWidget(QWidget):
    """
    Animated spinner widget for indeterminate progress indication.
    Features smooth rotation animation with customizable size and color.
    """
    
    def __init__(self, parent: Optional[QWidget] = None, size: int = 32, color: str = "#2E86AB"):
        super().__init__(parent)
        self.size = size
        self.color = QColor(color)
        self.angle = 0
        self.setFixedSize(size, size)
        
        # Animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate)
        self.timer.setInterval(50)  # 50ms for smooth animation
        
    def start_spinning(self):
        """Start the spinning animation"""
        self.timer.start()
        self.show()
        
    def stop_spinning(self):
        """Stop the spinning animation"""
        self.timer.stop()
        self.hide()
        
    def rotate(self):
        """Rotate the spinner by 10 degrees"""
        self.angle = (self.angle + 10) % 360
        self.update()
        
    def paintEvent(self, event):
        """Custom paint event to draw the spinner"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Set up the pen
        pen = QPen(self.color, 3)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        
        # Draw the spinner arc
        rect = QRect(3, 3, self.size - 6, self.size - 6)
        painter.drawArc(rect, self.angle * 16, 270 * 16)  # 270 degrees arc


class ProgressOverlay(QWidget):
    """
    Semi-transparent overlay widget that shows loading progress and disables interaction.
    Can display both indeterminate (spinner) and determinate (progress bar) progress.
    """
    
    cancelled = pyqtSignal()  # Signal emitted when user cancels operation
    
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 8px;
            }
        """)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(16)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Spinner widget
        self.spinner = SpinnerWidget(size=48, color="#2E86AB")
        spinner_layout = QHBoxLayout()
        spinner_layout.setAlignment(Qt.AlignCenter)
        spinner_layout.addWidget(self.spinner)
        layout.addLayout(spinner_layout)
        
        # Progress bar (initially hidden)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #E1E8ED;
                border-radius: 6px;
                background-color: #FFFFFF;
                text-align: center;
                font-weight: 600;
                font-size: 12px;
                color: #2C3E50;
                min-width: 200px;
                height: 24px;
            }
            QProgressBar::chunk {
                background-color: #27AE60;
                border-radius: 4px;
                margin: 2px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("Loading...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #2C3E50;
                font-size: 14px;
                font-weight: 500;
                background: transparent;
                padding: 8px;
            }
        """)
        layout.addWidget(self.status_label)
        
        # Cancel button (initially hidden)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setVisible(False)
        self.cancel_button.clicked.connect(self.cancelled.emit)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: 600;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
            QPushButton:pressed {
                background-color: #A93226;
            }
        """)
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        # Initially hidden
        self.hide()
        
    def show_indeterminate(self, message: str = "Loading...", show_cancel: bool = False):
        """Show indeterminate progress with spinner"""
        self.status_label.setText(message)
        self.spinner.setVisible(True)
        self.progress_bar.setVisible(False)
        self.cancel_button.setVisible(show_cancel)
        self.spinner.start_spinning()
        self.show()
        self.raise_()
        
    def show_determinate(self, message: str = "Processing...", max_value: int = 100, show_cancel: bool = False):
        """Show determinate progress with progress bar"""
        self.status_label.setText(message)
        self.spinner.setVisible(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(max_value)
        self.progress_bar.setValue(0)
        self.cancel_button.setVisible(show_cancel)
        self.show()
        self.raise_()
        
    def update_progress(self, value: int, message: str = None):
        """Update progress bar value and optionally message"""
        if self.progress_bar.isVisible():
            self.progress_bar.setValue(value)
        if message:
            self.status_label.setText(message)
            
    def hide_progress(self):
        """Hide the progress overlay"""
        if self.spinner.timer.isActive():
            self.spinner.stop_spinning()
        self.hide()
        
    def resizeEvent(self, event):
        """Ensure overlay covers the entire parent widget"""
        if self.parent():
            self.resize(self.parent().size())
        super().resizeEvent(event)


class LoadingButton(QPushButton):
    """
    Button that shows loading state with spinner when clicked.
    Automatically disables interaction during loading.
    """
    
    def __init__(self, text: str, loading_text: str = "Loading...", parent: Optional[QWidget] = None):
        super().__init__(text, parent)
        self.original_text = text
        self.loading_text = loading_text
        self.is_loading = False
        
        # Create spinner for button
        self.spinner = SpinnerWidget(size=16, color="#FFFFFF")
        self.spinner.setVisible(False)
        
        # Layout for button content
        self.setup_button_layout()
        
    def setup_button_layout(self):
        """Set up the button layout with text and spinner"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(6)
        layout.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(self.spinner)
        
        # Override button text with custom label for better control
        self.text_label = QLabel(self.original_text)
        self.text_label.setStyleSheet("background: transparent; color: inherit;")
        layout.addWidget(self.text_label)
        
        # Hide the button's default text
        self.setText("")
        
    def start_loading(self, message: str = None):
        """Start loading state"""
        if self.is_loading:
            return
            
        self.is_loading = True
        self.setEnabled(False)
        self.text_label.setText(message or self.loading_text)
        self.spinner.setVisible(True)
        self.spinner.start_spinning()
        
    def stop_loading(self):
        """Stop loading state"""
        if not self.is_loading:
            return
            
        self.is_loading = False
        self.setEnabled(True)
        self.text_label.setText(self.original_text)
        self.spinner.setVisible(False)
        self.spinner.stop_spinning()


class ProgressManager(QObject):
    """
    Centralized manager for all progress indicators in the application.
    Handles coordination between different UI components and loading states.
    """
    
    # Signals for progress updates
    progress_started = pyqtSignal(str, str)  # operation_id, message
    progress_updated = pyqtSignal(str, int, str)  # operation_id, value, message
    progress_finished = pyqtSignal(str, bool, str)  # operation_id, success, message
    
    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self.active_operations = {}
        self.mutex = QMutex()
        
    def start_operation(self, operation_id: str, message: str = "Loading...", 
                       determinate: bool = False, max_value: int = 100):
        """Start a new progress operation"""
        with QMutexLocker(self.mutex):
            self.active_operations[operation_id] = {
                'message': message,
                'determinate': determinate,
                'max_value': max_value,
                'current_value': 0,
                'start_time': time.time()
            }
        
        self.progress_started.emit(operation_id, message)
        
    def update_operation(self, operation_id: str, value: int = None, message: str = None):
        """Update progress for an operation"""
        with QMutexLocker(self.mutex):
            if operation_id not in self.active_operations:
                return
                
            op = self.active_operations[operation_id]
            if value is not None:
                op['current_value'] = value
            if message is not None:
                op['message'] = message
        
        self.progress_updated.emit(operation_id, value or 0, message or "")
        
    def finish_operation(self, operation_id: str, success: bool = True, message: str = None):
        """Finish a progress operation"""
        with QMutexLocker(self.mutex):
            if operation_id in self.active_operations:
                op = self.active_operations[operation_id]
                duration = time.time() - op['start_time']
                del self.active_operations[operation_id]
        
        final_message = message or ("Operation completed successfully" if success else "Operation failed")
        self.progress_finished.emit(operation_id, success, final_message)
        
    def cancel_operation(self, operation_id: str):
        """Cancel a progress operation"""
        self.finish_operation(operation_id, False, "Operation cancelled")
        
    def is_operation_active(self, operation_id: str) -> bool:
        """Check if an operation is currently active"""
        with QMutexLocker(self.mutex):
            return operation_id in self.active_operations


class ProgressAwareWorker(QThread):
    """
    Base class for worker threads that can report progress.
    Integrates with ProgressManager for centralized progress tracking.
    """
    
    progress_update = pyqtSignal(str, int, str)  # operation_id, progress, message
    operation_finished = pyqtSignal(str, bool, str, object)  # operation_id, success, message, result
    
    def __init__(self, operation_id: str, parent: Optional[QObject] = None):
        super().__init__(parent)
        self.operation_id = operation_id
        self.should_cancel = False
        
    def cancel(self):
        """Request cancellation of the operation"""
        self.should_cancel = True
        
    def emit_progress(self, progress: int, message: str = ""):
        """Emit progress update"""
        self.progress_update.emit(self.operation_id, progress, message)
        
    def emit_finished(self, success: bool, message: str = "", result: Any = None):
        """Emit operation finished"""
        self.operation_finished.emit(self.operation_id, success, message, result)


# Utility functions for common progress patterns
def create_api_loading_message(operation: str) -> str:
    """Create a user-friendly loading message for API operations"""
    messages = {
        'generating_exercises': 'Generating new exercises...',
        'checking_answer': 'Checking your answer...',
        'getting_hint': 'Getting hint...',
        'explaining_answer': 'Explaining the answer...',
        'generating_summary': 'Creating session summary...',
        'testing_api': 'Testing API connection...',
        'saving_progress': 'Saving your progress...',
        'loading_exercises': 'Loading exercises...'
    }
    return messages.get(operation, f'{operation.replace("_", " ").title()}...')


def create_error_message(operation: str, error: str) -> str:
    """Create a user-friendly error message"""
    base_messages = {
        'generating_exercises': 'Failed to generate exercises',
        'checking_answer': 'Could not check your answer',
        'getting_hint': 'Unable to get hint',
        'explaining_answer': 'Could not explain the answer',
        'generating_summary': 'Failed to create summary',
        'testing_api': 'API test failed',
        'saving_progress': 'Could not save progress',
        'loading_exercises': 'Failed to load exercises'
    }
    
    base_msg = base_messages.get(operation, f'{operation.replace("_", " ").title()} failed')
    
    # Add specific error details for common issues
    if 'connection' in error.lower() or 'timeout' in error.lower():
        return f"{base_msg} - Connection issue. Please check your internet connection."
    elif 'authentication' in error.lower() or 'api key' in error.lower():
        return f"{base_msg} - Authentication error. Please check your API key."
    elif 'rate limit' in error.lower():
        return f"{base_msg} - Rate limit exceeded. Please wait a moment and try again."
    else:
        return f"{base_msg} - {error}"


if __name__ == "__main__":
    """
    Demo application showing all progress indicator components.
    """
    import random
    
    app = QApplication(sys.argv)
    
    # Main demo window
    demo = QWidget()
    demo.setWindowTitle("Progress Indicators Demo")
    demo.setMinimumSize(600, 400)
    
    layout = QVBoxLayout(demo)
    
    # Title
    title = QLabel("Progress Indicators Demo")
    title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")
    title.setAlignment(Qt.AlignCenter)
    layout.addWidget(title)
    
    # Progress overlay (will be shown over the entire window)
    overlay = ProgressOverlay(demo)
    
    # Demo buttons
    button_layout = QHBoxLayout()
    
    # Spinner demo button
    def show_spinner_demo():
        overlay.show_indeterminate("Processing API request...", show_cancel=True)
        QTimer.singleShot(3000, overlay.hide_progress)  # Hide after 3 seconds
        
    spinner_btn = QPushButton("Show Spinner")
    spinner_btn.clicked.connect(show_spinner_demo)
    button_layout.addWidget(spinner_btn)
    
    # Progress bar demo button
    def show_progress_demo():
        overlay.show_determinate("Downloading exercises...", 100, show_cancel=True)
        
        # Simulate progress updates
        progress_timer = QTimer()
        progress_value = [0]
        
        def update_progress():
            progress_value[0] += random.randint(5, 15)
            if progress_value[0] >= 100:
                progress_value[0] = 100
                overlay.update_progress(100, "Download complete!")
                QTimer.singleShot(1000, overlay.hide_progress)
                progress_timer.stop()
            else:
                overlay.update_progress(progress_value[0], f"Downloading... {progress_value[0]}%")
                
        progress_timer.timeout.connect(update_progress)
        progress_timer.start(200)
        
    progress_btn = QPushButton("Show Progress Bar")
    progress_btn.clicked.connect(show_progress_demo)
    button_layout.addWidget(progress_btn)
    
    # Loading button demo
    loading_btn = LoadingButton("Submit Answer", "Checking Answer...")
    
    def simulate_loading():
        loading_btn.start_loading()
        QTimer.singleShot(2000, loading_btn.stop_loading)  # Stop after 2 seconds
        
    loading_btn.clicked.connect(simulate_loading)
    button_layout.addWidget(loading_btn)
    
    layout.addLayout(button_layout)
    
    # Status area
    status_area = QLabel("Click buttons to test progress indicators")
    status_area.setStyleSheet("""
        QLabel {
            background-color: #f5f5f5;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 20px;
            margin-top: 20px;
        }
    """)
    status_area.setAlignment(Qt.AlignCenter)
    layout.addWidget(status_area)
    
    # Handle overlay cancellation
    def handle_cancel():
        status_area.setText("Operation cancelled by user")
        overlay.hide_progress()
        
    overlay.cancelled.connect(handle_cancel)
    
    demo.show()
    sys.exit(app.exec_())
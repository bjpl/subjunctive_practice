"""
Test script for progress indicators in the Spanish Subjunctive Practice App.

This script provides comprehensive testing for:
- Progress overlay visibility and behavior
- Loading state management 
- Error handling and user feedback
- API call simulation with delays
- UI disable/enable during operations
"""

import sys
import time
import random
from typing import Optional
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QTextEdit, QGroupBox, QCheckBox, QMessageBox
)
from PyQt5.QtCore import QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QFont

# Import progress indicators
try:
    from progress_indicators import (
        ProgressOverlay, LoadingButton, ProgressManager, 
        create_api_loading_message, create_error_message
    )
    PROGRESS_AVAILABLE = True
except ImportError:
    print("Could not import progress indicators. Make sure progress_indicators.py is in the same directory.")
    PROGRESS_AVAILABLE = False
    sys.exit(1)


class MockGPTWorker(QObject):
    """Mock GPT worker that simulates API calls with delays and potential errors"""
    
    result_ready = pyqtSignal(str, bool)  # result, success
    
    def __init__(self, operation_type: str, simulate_error: bool = False, delay: float = 2.0):
        super().__init__()
        self.operation_type = operation_type
        self.simulate_error = simulate_error
        self.delay = delay
        
    def start(self):
        """Start the mock operation"""
        timer = QTimer(self)
        timer.singleShot(int(self.delay * 1000), self._complete_operation)
        
    def _complete_operation(self):
        """Complete the operation with either success or error"""
        if self.simulate_error:
            # Simulate different types of errors
            error_types = [
                "Connection timeout. Please check your internet connection and try again.",
                "Authentication failed. Please verify your OpenAI API key in the .env file.",
                "Rate limit exceeded. Please wait a moment and try again.",
                "API quota exceeded. Please check your OpenAI account billing.",
                "Service temporarily unavailable: Internal server error"
            ]
            result = random.choice(error_types)
            self.result_ready.emit(result, False)
        else:
            # Simulate successful responses based on operation type
            success_responses = {
                'generating_exercises': """[
                    {"context": "En la reunión", "sentence": "Es importante que todos ___ (llegar) a tiempo.", 
                     "answer": "lleguen", "choices": ["llegan", "lleguen", "llegaron", "llegarán"], 
                     "translation": "It's important that everyone arrives on time."}
                ]""",
                'checking_answer': "Muy bien. Usaste correctamente el subjuntivo después de 'es importante que'. Esta expresión siempre requiere subjuntivo porque expresa una valoración personal.",
                'getting_hint': "Piensa en la expresión 'es importante que'. ¿Qué modo verbal requiere normalmente?",
                'generating_summary': "Tu práctica del subjuntivo ha sido excelente hoy. Dominaste bien las expresiones de valoración y mostraste buen uso de los tiempos verbales.",
                'testing_api': "Connection successful"
            }
            result = success_responses.get(self.operation_type, "Operation completed successfully")
            self.result_ready.emit(result, True)


class ProgressIndicatorTestWindow(QMainWindow):
    """Main test window for progress indicators"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Progress Indicators Test - Spanish Subjunctive Practice")
        self.setMinimumSize(800, 600)
        
        # Initialize progress manager
        self.progress_manager = ProgressManager(self)
        self.progress_overlay = None
        
        # Track loading states
        self.loading_states = {
            'generating_exercises': False,
            'checking_answer': False,
            'getting_hint': False,
            'generating_summary': False,
            'testing_api': False
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Progress Indicators Test Suite")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)
        
        # Progress overlay (covers entire window)
        self.progress_overlay = ProgressOverlay(self)
        self.progress_overlay.cancelled.connect(self.handle_operation_cancelled)
        
        # Connect progress manager signals
        self.progress_manager.progress_started.connect(self.handle_progress_started)
        self.progress_manager.progress_updated.connect(self.handle_progress_updated)
        self.progress_manager.progress_finished.connect(self.handle_progress_finished)
        
        # Test sections
        self.create_basic_tests(layout)
        self.create_loading_button_tests(layout)
        self.create_error_simulation_tests(layout)
        self.create_concurrent_operations_tests(layout)
        
        # Status display
        self.create_status_display(layout)
        
    def create_basic_tests(self, layout):
        """Create basic progress indicator tests"""
        group = QGroupBox("Basic Progress Indicators")
        group_layout = QHBoxLayout(group)
        
        # Exercise generation test
        exercises_btn = QPushButton("Generate Exercises")
        exercises_btn.clicked.connect(lambda: self.test_operation('generating_exercises', 3.0))
        group_layout.addWidget(exercises_btn)
        
        # Answer checking test
        answer_btn = QPushButton("Check Answer")
        answer_btn.clicked.connect(lambda: self.test_operation('checking_answer', 1.5))
        group_layout.addWidget(answer_btn)
        
        # Hint test
        hint_btn = QPushButton("Get Hint")
        hint_btn.clicked.connect(lambda: self.test_operation('getting_hint', 1.0))
        group_layout.addWidget(hint_btn)
        
        layout.addWidget(group)
        
    def create_loading_button_tests(self, layout):
        """Create loading button tests"""
        group = QGroupBox("Loading Buttons")
        group_layout = QHBoxLayout(group)
        
        # Standard loading button
        self.loading_btn = LoadingButton("Submit Answer", "Checking...")
        self.loading_btn.clicked.connect(self.test_loading_button)
        group_layout.addWidget(self.loading_btn)
        
        # Another loading button
        self.hint_btn = LoadingButton("Get Hint", "Getting hint...")
        self.hint_btn.clicked.connect(lambda: self.test_loading_button_with_delay(self.hint_btn, 2.0))
        group_layout.addWidget(self.hint_btn)
        
        layout.addWidget(group)
        
    def create_error_simulation_tests(self, layout):
        """Create error simulation tests"""
        group = QGroupBox("Error Simulation")
        group_layout = QVBoxLayout(group)
        
        # Error type checkboxes
        checkbox_layout = QHBoxLayout()
        
        self.connection_error_cb = QCheckBox("Connection Error")
        self.auth_error_cb = QCheckBox("Auth Error")
        self.rate_limit_cb = QCheckBox("Rate Limit")
        self.server_error_cb = QCheckBox("Server Error")
        
        checkbox_layout.addWidget(self.connection_error_cb)
        checkbox_layout.addWidget(self.auth_error_cb)
        checkbox_layout.addWidget(self.rate_limit_cb)
        checkbox_layout.addWidget(self.server_error_cb)
        
        group_layout.addLayout(checkbox_layout)
        
        # Error test buttons
        error_btn_layout = QHBoxLayout()
        
        exercises_error_btn = QPushButton("Generate Exercises (Error)")
        exercises_error_btn.clicked.connect(lambda: self.test_operation('generating_exercises', 2.0, True))
        error_btn_layout.addWidget(exercises_error_btn)
        
        api_error_btn = QPushButton("Test API (Error)")
        api_error_btn.clicked.connect(lambda: self.test_operation('testing_api', 1.5, True))
        error_btn_layout.addWidget(api_error_btn)
        
        group_layout.addLayout(error_btn_layout)
        layout.addWidget(group)
        
    def create_concurrent_operations_tests(self, layout):
        """Create concurrent operations tests"""
        group = QGroupBox("Concurrent Operations")
        group_layout = QHBoxLayout(group)
        
        concurrent_btn = QPushButton("Multiple Operations")
        concurrent_btn.clicked.connect(self.test_concurrent_operations)
        group_layout.addWidget(concurrent_btn)
        
        cancel_all_btn = QPushButton("Cancel All")
        cancel_all_btn.clicked.connect(self.cancel_all_operations)
        group_layout.addWidget(cancel_all_btn)
        
        layout.addWidget(group)
        
    def create_status_display(self, layout):
        """Create status display area"""
        group = QGroupBox("Test Results")
        group_layout = QVBoxLayout(group)
        
        self.status_display = QTextEdit()
        self.status_display.setMaximumHeight(150)
        self.status_display.setReadOnly(True)
        self.status_display.append("Ready to test progress indicators...")
        group_layout.addWidget(self.status_display)
        
        clear_btn = QPushButton("Clear Log")
        clear_btn.clicked.connect(self.status_display.clear)
        group_layout.addWidget(clear_btn)
        
        layout.addWidget(group)
        
    def test_operation(self, operation_type: str, delay: float = 2.0, simulate_error: bool = False):
        """Test a single operation with progress indication"""
        if self.loading_states[operation_type]:
            self.log(f"⚠️ {operation_type} is already running")
            return
            
        self.loading_states[operation_type] = True
        
        # Start progress indication
        loading_msg = create_api_loading_message(operation_type)
        self.progress_manager.start_operation(operation_type, loading_msg)
        
        self.log(f"🚀 Starting {operation_type} (delay: {delay}s, error: {simulate_error})")
        
        # Create and start mock worker
        worker = MockGPTWorker(operation_type, simulate_error, delay)
        worker.result_ready.connect(lambda result, success: self.handle_mock_result(operation_type, result, success))
        worker.start()
        
    def test_loading_button(self):
        """Test loading button behavior"""
        if self.loading_btn.is_loading:
            return
            
        self.loading_btn.start_loading()
        self.log("🔄 Loading button started")
        
        # Stop loading after 2 seconds
        QTimer.singleShot(2000, lambda: [
            self.loading_btn.stop_loading(),
            self.log("✅ Loading button stopped")
        ])
        
    def test_loading_button_with_delay(self, button: LoadingButton, delay: float):
        """Test loading button with custom delay"""
        if button.is_loading:
            return
            
        button.start_loading()
        self.log(f"🔄 Loading button started ({delay}s)")
        
        QTimer.singleShot(int(delay * 1000), lambda: [
            button.stop_loading(),
            self.log("✅ Loading button stopped")
        ])
        
    def test_concurrent_operations(self):
        """Test multiple operations running concurrently"""
        self.log("🔀 Starting concurrent operations...")
        
        # Start multiple operations with different delays
        operations = [
            ('checking_answer', 1.0, False),
            ('getting_hint', 1.5, False),
            ('generating_summary', 2.5, False)
        ]
        
        for op_type, delay, error in operations:
            if not self.loading_states[op_type]:
                QTimer.singleShot(random.randint(0, 500), lambda t=op_type, d=delay, e=error: self.test_operation(t, d, e))
                
    def cancel_all_operations(self):
        """Cancel all running operations"""
        cancelled_count = 0
        for operation in list(self.loading_states.keys()):
            if self.loading_states[operation]:
                self.progress_manager.cancel_operation(operation)
                self.loading_states[operation] = False
                cancelled_count += 1
                
        self.log(f"⛔ Cancelled {cancelled_count} operations")
        
    def handle_mock_result(self, operation_type: str, result: str, success: bool):
        """Handle results from mock operations"""
        self.loading_states[operation_type] = False
        
        if success:
            self.progress_manager.finish_operation(operation_type, True, f"{operation_type} completed successfully")
            self.log(f"✅ {operation_type} succeeded")
        else:
            error_msg = create_error_message(operation_type, result)
            self.progress_manager.finish_operation(operation_type, False, error_msg)
            self.log(f"❌ {operation_type} failed: {result}")
            
    def handle_operation_cancelled(self):
        """Handle when user cancels an operation"""
        for operation in self.loading_states:
            if self.loading_states[operation]:
                self.progress_manager.cancel_operation(operation)
                self.loading_states[operation] = False
                
        self.log("🚫 Operation cancelled by user")
        
    def handle_progress_started(self, operation_id: str, message: str):
        """Handle progress start"""
        self.log(f"📈 Progress started: {operation_id} - {message}")
        
        if operation_id in ['generating_exercises', 'generating_summary']:
            self.progress_overlay.show_indeterminate(message, show_cancel=True)
        else:
            self.progress_overlay.show_indeterminate(message, show_cancel=False)
            
    def handle_progress_updated(self, operation_id: str, value: int, message: str):
        """Handle progress update"""
        if message:
            self.progress_overlay.update_progress(value, message)
            self.log(f"📊 Progress updated: {operation_id} - {message}")
            
    def handle_progress_finished(self, operation_id: str, success: bool, message: str):
        """Handle progress finish"""
        self.progress_overlay.hide_progress()
        
        status = "✅ Success" if success else "❌ Failed"
        self.log(f"🏁 Progress finished: {operation_id} - {status} - {message}")
        
    def log(self, message: str):
        """Add message to status display"""
        timestamp = time.strftime("%H:%M:%S")
        self.status_display.append(f"[{timestamp}] {message}")
        
        # Scroll to bottom
        cursor = self.status_display.textCursor()
        cursor.movePosition(cursor.End)
        self.status_display.setTextCursor(cursor)
        
    def resizeEvent(self, event):
        """Handle window resize to maintain progress overlay positioning"""
        super().resizeEvent(event)
        if self.progress_overlay:
            self.progress_overlay.resize(self.size())


def main():
    """Main function to run the test application"""
    app = QApplication(sys.argv)
    
    if not PROGRESS_AVAILABLE:
        QMessageBox.critical(None, "Import Error", 
                           "Could not import progress indicators module.\\n"
                           "Make sure progress_indicators.py is available.")
        return
        
    # Set application style
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f5f5f5;
        }
        QGroupBox {
            font-weight: bold;
            border: 2px solid #cccccc;
            border-radius: 5px;
            margin-top: 1ex;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 10px 0 10px;
        }
        QPushButton {
            background-color: #2E86AB;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: 500;
            min-width: 100px;
        }
        QPushButton:hover {
            background-color: #1F5F7A;
        }
        QPushButton:pressed {
            background-color: #174A5C;
        }
        QPushButton:disabled {
            background-color: #95A5A6;
        }
        QTextEdit {
            background-color: white;
            border: 1px solid #cccccc;
            border-radius: 4px;
            padding: 5px;
            font-family: Consolas, Monaco, monospace;
            font-size: 12px;
        }
        QCheckBox {
            spacing: 5px;
        }
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
        }
        QCheckBox::indicator:unchecked {
            border: 2px solid #cccccc;
            border-radius: 3px;
            background-color: white;
        }
        QCheckBox::indicator:checked {
            border: 2px solid #2E86AB;
            border-radius: 3px;
            background-color: #2E86AB;
        }
    """)
    
    # Create and show main window
    window = ProgressIndicatorTestWindow()
    window.show()
    
    # Add some initial log messages
    window.log("🎯 Progress Indicators Test Suite initialized")
    window.log("💡 Try different operations to test loading states")
    window.log("⚠️ Error simulation tests show how errors are handled")
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
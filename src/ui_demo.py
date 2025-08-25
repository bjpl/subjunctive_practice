"""
UI Interactions Demo

This script demonstrates the improved user interaction flow for the Spanish 
Subjunctive Practice app. It shows the before/after comparison and highlights
the key improvements.
"""

import sys
import os
from typing import List
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QGroupBox, QTabWidget, QSplitter,
    QMessageBox, QProgressBar, QFrame
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


class InteractionDemoWindow(QMainWindow):
    """
    Demonstrates the improved UI interactions for the Spanish subjunctive app.
    Shows side-by-side comparison of old vs new interaction flows.
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UI Interaction Improvements Demo - Spanish Subjunctive Practice")
        self.setGeometry(100, 100, 1200, 800)
        
        # Demo data
        self.demo_step = 0
        self.demo_steps = [
            {
                'title': '🎯 Setup Phase',
                'old_flow': 'User must manually check boxes, then click Generate',
                'new_flow': 'Smart validation, F5 shortcut, visual feedback for missing selections',
                'improvement': '• Keyboard shortcuts (F5)\n• Smart validation with helpful messages\n• Auto-focus on required fields'
            },
            {
                'title': '✍️ Practice Phase', 
                'old_flow': 'Type answer, click Submit button',
                'new_flow': 'Type answer, press Enter, immediate visual feedback',
                'improvement': '• Enter key to submit\n• Rich visual feedback with emojis\n• Auto-focus on input field\n• Smart answer validation'
            },
            {
                'title': '📖 Feedback Phase',
                'old_flow': 'Read feedback, click Next button',
                'new_flow': 'Read feedback, press → or auto-advance after delay',
                'improvement': '• Arrow keys for navigation\n• Optional auto-advance\n• Contextual feedback messages\n• Clear visual state indicators'
            },
            {
                'title': '🧭 Navigation',
                'old_flow': 'Click Previous/Next buttons only',
                'new_flow': 'Arrow keys, Home/End, Ctrl+G to jump, Tab to switch modes',
                'improvement': '• Arrow keys: ←/→\n• Home/End: First/Last exercise\n• Ctrl+G: Jump to specific exercise\n• Tab: Switch practice modes'
            },
            {
                'title': '⚙️ Settings & Modes',
                'old_flow': 'Navigate through menus and dropdowns',
                'new_flow': 'Quick keyboard shortcuts for all common actions',
                'improvement': '• Ctrl+T: Toggle translation\n• Ctrl+D: Toggle theme\n• Ctrl+R: Review mode\n• F1: Contextual help'
            }
        ]
        
        self.init_ui()
        self.setup_demo_timer()

    def init_ui(self):
        """Initialize the demo UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        
        # Title
        title_label = QLabel("UI Interaction Flow Improvements")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(len(self.demo_steps))
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("Demo Step %v of %m")
        main_layout.addWidget(self.progress_bar)
        
        # Main content splitter
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left side - Before/After comparison
        comparison_widget = self.create_comparison_widget()
        splitter.addWidget(comparison_widget)
        
        # Right side - Interaction demonstration
        demo_widget = self.create_demo_widget()
        splitter.addWidget(demo_widget)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        
        # Control buttons
        controls_layout = QHBoxLayout()
        
        self.prev_btn = QPushButton("← Previous Step")
        self.prev_btn.clicked.connect(self.prev_step)
        self.prev_btn.setEnabled(False)
        
        self.play_pause_btn = QPushButton("⏸️ Pause Demo")
        self.play_pause_btn.clicked.connect(self.toggle_demo)
        
        self.next_btn = QPushButton("Next Step →")
        self.next_btn.clicked.connect(self.next_step)
        
        self.reset_btn = QPushButton("🔄 Reset Demo")
        self.reset_btn.clicked.connect(self.reset_demo)
        
        controls_layout.addWidget(self.prev_btn)
        controls_layout.addWidget(self.play_pause_btn)
        controls_layout.addWidget(self.next_btn)
        controls_layout.addStretch()
        controls_layout.addWidget(self.reset_btn)
        
        main_layout.addLayout(controls_layout)
        
        # Initialize first step
        self.update_demo_display()

    def create_comparison_widget(self) -> QWidget:
        """Create the before/after comparison widget"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Comparison tabs
        tabs = QTabWidget()
        
        # Before tab
        before_tab = QWidget()
        before_layout = QVBoxLayout(before_tab)
        
        before_title = QLabel("❌ BEFORE: Traditional UI Flow")
        before_title.setStyleSheet("font-weight: bold; color: #e74c3c; padding: 10px; background: #fdf2f2; border-radius: 5px;")
        before_layout.addWidget(before_title)
        
        self.before_text = QTextEdit()
        self.before_text.setMaximumHeight(200)
        self.before_text.setStyleSheet("background: #fdf2f2; border: 1px solid #e74c3c;")
        before_layout.addWidget(self.before_text)
        
        tabs.addTab(before_tab, "Before")
        
        # After tab
        after_tab = QWidget()
        after_layout = QVBoxLayout(after_tab)
        
        after_title = QLabel("✅ AFTER: Streamlined Interactions")
        after_title.setStyleSheet("font-weight: bold; color: #27ae60; padding: 10px; background: #f2fdf4; border-radius: 5px;")
        after_layout.addWidget(after_title)
        
        self.after_text = QTextEdit()
        self.after_text.setMaximumHeight(200)
        self.after_text.setStyleSheet("background: #f2fdf4; border: 1px solid #27ae60;")
        after_layout.addWidget(self.after_text)
        
        tabs.addTab(after_tab, "After")
        
        layout.addWidget(tabs)
        
        # Improvements section
        improvements_group = QGroupBox("🚀 Key Improvements")
        improvements_layout = QVBoxLayout(improvements_group)
        
        self.improvements_text = QTextEdit()
        self.improvements_text.setMaximumHeight(150)
        self.improvements_text.setStyleSheet("background: #f8f9fa; border: 1px solid #3498db;")
        improvements_layout.addWidget(self.improvements_text)
        
        layout.addWidget(improvements_group)
        
        return widget

    def create_demo_widget(self) -> QWidget:
        """Create the interactive demonstration widget"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Demo title
        self.demo_title = QLabel("Current Demo Step")
        demo_title_font = QFont()
        demo_title_font.setPointSize(16)
        demo_title_font.setBold(True)
        self.demo_title.setFont(demo_title_font)
        self.demo_title.setAlignment(Qt.AlignCenter)
        self.demo_title.setStyleSheet("padding: 15px; background: #3498db; color: white; border-radius: 8px;")
        layout.addWidget(self.demo_title)
        
        # Keyboard shortcuts showcase
        shortcuts_group = QGroupBox("⌨️ Try These Keyboard Shortcuts")
        shortcuts_layout = QVBoxLayout(shortcuts_group)
        
        self.shortcuts_display = QLabel()
        self.shortcuts_display.setWordWrap(True)
        self.shortcuts_display.setStyleSheet("padding: 15px; background: #f8f9fa; border-radius: 5px; font-family: monospace;")
        shortcuts_layout.addWidget(self.shortcuts_display)
        
        layout.addWidget(shortcuts_group)
        
        # Interactive elements
        interactive_group = QGroupBox("🎮 Interactive Demo")
        interactive_layout = QVBoxLayout(interactive_group)
        
        # Simulated app elements
        self.demo_input = QLabel("Demo Input Field")
        self.demo_input.setStyleSheet("padding: 10px; border: 2px solid #3498db; background: white; border-radius: 5px;")
        interactive_layout.addWidget(self.demo_input)
        
        self.demo_feedback = QLabel("Feedback will appear here...")
        self.demo_feedback.setStyleSheet("padding: 10px; border: 1px solid #bdc3c7; background: #ecf0f1; border-radius: 5px;")
        interactive_layout.addWidget(self.demo_feedback)
        
        # Demo buttons
        demo_buttons_layout = QHBoxLayout()
        
        self.demo_submit = QPushButton("Submit (Enter)")
        self.demo_submit.clicked.connect(self.simulate_submit)
        
        self.demo_prev = QPushButton("← (Left)")
        self.demo_prev.clicked.connect(self.simulate_prev)
        
        self.demo_next = QPushButton("→ (Right)")
        self.demo_next.clicked.connect(self.simulate_next)
        
        demo_buttons_layout.addWidget(self.demo_submit)
        demo_buttons_layout.addWidget(self.demo_prev)
        demo_buttons_layout.addWidget(self.demo_next)
        
        interactive_layout.addLayout(demo_buttons_layout)
        
        layout.addWidget(interactive_group)
        
        # Statistics showcase
        stats_group = QGroupBox("📊 Enhanced Feedback")
        stats_layout = QVBoxLayout(stats_group)
        
        self.stats_display = QLabel("Session stats and achievements will appear here...")
        self.stats_display.setStyleSheet("padding: 10px; background: #fff3cd; border: 1px solid #ffc107; border-radius: 5px;")
        stats_layout.addWidget(self.stats_display)
        
        layout.addWidget(stats_group)
        
        return widget

    def setup_demo_timer(self):
        """Setup automatic demo progression"""
        self.demo_timer = QTimer()
        self.demo_timer.timeout.connect(self.next_step)
        self.demo_timer.start(5000)  # 5 seconds per step
        self.demo_running = True

    def update_demo_display(self):
        """Update the demo display for current step"""
        if self.demo_step >= len(self.demo_steps):
            self.demo_step = 0
        
        step_data = self.demo_steps[self.demo_step]
        
        # Update comparison
        self.before_text.setText(f"Old Flow:\n{step_data['old_flow']}\n\nProblems:\n• Manual clicking required\n• No keyboard shortcuts\n• Limited feedback\n• Slow workflow")
        self.after_text.setText(f"New Flow:\n{step_data['new_flow']}\n\nBenefits:\n• Intuitive keyboard shortcuts\n• Rich visual feedback\n• Smooth transitions\n• Faster workflow")
        self.improvements_text.setText(step_data['improvement'])
        
        # Update demo section
        self.demo_title.setText(step_data['title'])
        self.progress_bar.setValue(self.demo_step + 1)
        
        # Update shortcuts based on current step
        shortcuts = self.get_shortcuts_for_step(self.demo_step)
        self.shortcuts_display.setText(shortcuts)
        
        # Update demo feedback
        feedback_messages = [
            "🎯 Select options and press F5 to generate exercises",
            "✍️ Type your answer and press Enter to submit", 
            "📖 Read explanation, press → to continue",
            "🧭 Use ←/→ arrows, Home/End, or Ctrl+G to navigate",
            "⚙️ Use Ctrl+T, Ctrl+D, Ctrl+R for quick settings"
        ]
        self.demo_feedback.setText(feedback_messages[self.demo_step])
        
        # Update stats
        stats_messages = [
            "📊 Setup validation: Missing selections highlighted",
            "🎉 Correct! +1 point • Streak: 3 • Accuracy: 85%",
            "💡 Explanation provided • Hint available (H key)",
            "📍 Exercise 3/10 • Use G to jump to any exercise",
            "🌙 Dark theme active • Translation visible • Review mode ready"
        ]
        self.stats_display.setText(stats_messages[self.demo_step])
        
        # Update button states
        self.prev_btn.setEnabled(self.demo_step > 0)
        self.next_btn.setEnabled(self.demo_step < len(self.demo_steps) - 1)

    def get_shortcuts_for_step(self, step: int) -> str:
        """Get relevant shortcuts for demo step"""
        shortcuts_by_step = [
            # Setup
            "F5 or Ctrl+N: Generate exercises\nTab: Switch between sections\nEnter: Confirm selections",
            
            # Practice  
            "Enter: Submit answer\nH: Show hint\nSpace: Alternative submit\nCtrl+A: Select all text",
            
            # Feedback
            "→ or Right: Next exercise\n← or Left: Previous exercise\nEnter: Continue to next\nR: Review mode",
            
            # Navigation
            "Home: First exercise\nEnd: Last exercise\nCtrl+G: Jump to exercise\nPageUp/Down: Skip 5 exercises",
            
            # Settings
            "Ctrl+T: Toggle translation\nCtrl+D: Toggle theme\nCtrl+R: Review mode\nF1: Help\nCtrl+S: Stats"
        ]
        
        return shortcuts_by_step[step] if step < len(shortcuts_by_step) else "All shortcuts available!"

    # Demo controls
    def next_step(self):
        """Go to next demo step"""
        if self.demo_step < len(self.demo_steps) - 1:
            self.demo_step += 1
        else:
            self.demo_step = 0  # Loop back to beginning
        self.update_demo_display()

    def prev_step(self):
        """Go to previous demo step"""
        if self.demo_step > 0:
            self.demo_step -= 1
            self.update_demo_display()

    def toggle_demo(self):
        """Toggle auto demo progression"""
        if self.demo_running:
            self.demo_timer.stop()
            self.play_pause_btn.setText("▶️ Play Demo")
            self.demo_running = False
        else:
            self.demo_timer.start(5000)
            self.play_pause_btn.setText("⏸️ Pause Demo")
            self.demo_running = True

    def reset_demo(self):
        """Reset demo to beginning"""
        self.demo_step = 0
        self.update_demo_display()

    # Simulation methods
    def simulate_submit(self):
        """Simulate submit action"""
        self.demo_input.setText("✅ Answer submitted! (using Enter key)")
        self.demo_input.setStyleSheet("padding: 10px; border: 2px solid #27ae60; background: #f2fdf4; border-radius: 5px;")
        QTimer.singleShot(2000, self.reset_demo_input)

    def simulate_prev(self):
        """Simulate previous action"""
        self.demo_feedback.setText("⬅️ Moved to previous exercise (using Left arrow)")
        QTimer.singleShot(2000, self.reset_demo_feedback)

    def simulate_next(self):
        """Simulate next action"""
        self.demo_feedback.setText("➡️ Moved to next exercise (using Right arrow)")
        QTimer.singleShot(2000, self.reset_demo_feedback)

    def reset_demo_input(self):
        """Reset demo input appearance"""
        self.demo_input.setText("Demo Input Field")
        self.demo_input.setStyleSheet("padding: 10px; border: 2px solid #3498db; background: white; border-radius: 5px;")

    def reset_demo_feedback(self):
        """Reset demo feedback"""
        feedback_messages = [
            "🎯 Select options and press F5 to generate exercises",
            "✍️ Type your answer and press Enter to submit", 
            "📖 Read explanation, press → to continue",
            "🧭 Use ←/→ arrows, Home/End, or Ctrl+G to navigate",
            "⚙️ Use Ctrl+T, Ctrl+D, Ctrl+R for quick settings"
        ]
        self.demo_feedback.setText(feedback_messages[self.demo_step])


def main():
    """Run the UI interactions demo"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show demo window
    demo = InteractionDemoWindow()
    demo.show()
    
    # Show initial info
    QMessageBox.information(demo, "UI Interactions Demo", 
        "This demo shows the improved user interaction flow for the Spanish Subjunctive Practice app.\n\n"
        "• Watch the automatic progression or use controls\n"
        "• Compare Before/After in the tabs\n" 
        "• Try the simulated interactions\n"
        "• Press F1 anytime for keyboard shortcuts\n\n"
        "The demo will auto-advance every 5 seconds.")
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
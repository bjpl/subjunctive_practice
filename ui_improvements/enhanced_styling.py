# Enhanced Color Scheme and Typography for Spanish Subjunctive Practice

ENHANCED_LIGHT_THEME = """
/* Main Application Styling */
QMainWindow {
    background-color: #fafbfc;
    font-family: 'Segoe UI', 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Typography Hierarchy */
QLabel {
    color: #2c3e50;
    font-size: 16px;
    line-height: 1.5;
}

QLabel[role="title"] {
    font-size: 24px;
    font-weight: 600;
    color: #1a202c;
    margin-bottom: 16px;
}

QLabel[role="subtitle"] {
    font-size: 18px;
    font-weight: 500;
    color: #4a5568;
    margin-bottom: 12px;
}

QLabel[role="context"] {
    font-size: 16px;
    color: #718096;
    font-style: italic;
    background-color: #f7fafc;
    border-left: 4px solid #4299e1;
    padding: 12px 16px;
    border-radius: 4px;
    margin: 8px 0;
}

QLabel[role="exercise"] {
    font-size: 20px;
    font-weight: 500;
    color: #1a202c;
    background-color: #fff5f5;
    border: 2px solid #fed7d7;
    border-radius: 8px;
    padding: 20px;
    margin: 16px 0;
}

/* Enhanced Button Styling */
QPushButton {
    font-family: 'Segoe UI', sans-serif;
    font-size: 16px;
    font-weight: 500;
    padding: 12px 24px;
    border-radius: 8px;
    border: none;
    transition: all 0.2s ease;
}

QPushButton[role="primary"] {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                              stop:0 #4299e1, stop:1 #3182ce);
    color: white;
    min-height: 44px;
}

QPushButton[role="primary"]:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                              stop:0 #3182ce, stop:1 #2b6cb0);
    transform: translateY(-1px);
}

QPushButton[role="secondary"] {
    background-color: #edf2f7;
    color: #4a5568;
    border: 1px solid #cbd5e0;
}

QPushButton[role="secondary"]:hover {
    background-color: #e2e8f0;
    border-color: #a0aec0;
}

QPushButton[role="success"] {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                              stop:0 #48bb78, stop:1 #38a169);
    color: white;
}

QPushButton[role="danger"] {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                              stop:0 #f56565, stop:1 #e53e3e);
    color: white;
}

/* Input Field Enhancements */
QLineEdit {
    font-size: 18px;
    padding: 16px;
    border: 2px solid #e2e8f0;
    border-radius: 8px;
    background-color: #ffffff;
    selection-background-color: #bee3f8;
}

QLineEdit:focus {
    border-color: #4299e1;
    outline: none;
    box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1);
}

QLineEdit[state="correct"] {
    border-color: #48bb78;
    background-color: #f0fff4;
}

QLineEdit[state="incorrect"] {
    border-color: #f56565;
    background-color: #fffafa;
}

/* Group Box Styling */
QGroupBox {
    font-size: 18px;
    font-weight: 600;
    color: #2d3748;
    border: 2px solid #e2e8f0;
    border-radius: 12px;
    padding: 20px;
    margin: 16px 0;
    background-color: #ffffff;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 16px;
    padding: 0 8px;
    color: #4a5568;
}

/* Progress Bar Enhancement */
QProgressBar {
    border: 2px solid #e2e8f0;
    border-radius: 8px;
    background-color: #f7fafc;
    text-align: center;
    font-weight: 600;
    height: 32px;
    font-size: 14px;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                              stop:0 #48bb78, stop:0.5 #38a169, stop:1 #2f855a);
    border-radius: 6px;
    margin: 2px;
}

/* Multiple Choice Options */
QRadioButton {
    font-size: 16px;
    padding: 12px 16px;
    margin: 8px 0;
    border: 2px solid #e2e8f0;
    border-radius: 8px;
    background-color: #ffffff;
    color: #2d3748;
}

QRadioButton:hover {
    background-color: #f7fafc;
    border-color: #cbd5e0;
}

QRadioButton:checked {
    background-color: #ebf8ff;
    border-color: #4299e1;
    color: #2b6cb0;
}

/* Feedback Text Area */
QTextEdit {
    border: 2px solid #e2e8f0;
    border-radius: 8px;
    background-color: #ffffff;
    font-size: 16px;
    line-height: 1.6;
    padding: 16px;
}

QTextEdit[feedback="correct"] {
    border-color: #48bb78;
    background-color: #f0fff4;
}

QTextEdit[feedback="incorrect"] {
    border-color: #f56565;
    background-color: #fffafa;
}

/* Scrollbar Styling */
QScrollBar:vertical {
    background-color: #f7fafc;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #cbd5e0;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #a0aec0;
}
"""

ENHANCED_DARK_THEME = """
/* Dark Theme with Better Contrast */
QMainWindow {
    background-color: #1a202c;
    color: #e2e8f0;
    font-family: 'Segoe UI', 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
}

QLabel {
    color: #e2e8f0;
}

QLabel[role="title"] {
    color: #f7fafc;
    font-size: 24px;
    font-weight: 600;
}

QLabel[role="context"] {
    background-color: #2d3748;
    border-left: 4px solid #63b3ed;
    color: #cbd5e0;
}

QLabel[role="exercise"] {
    background-color: #2d3748;
    border: 2px solid #4a5568;
    color: #f7fafc;
}

QPushButton[role="primary"] {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                              stop:0 #4299e1, stop:1 #3182ce);
    color: white;
}

QGroupBox {
    border: 2px solid #4a5568;
    background-color: #2d3748;
    color: #e2e8f0;
}

QLineEdit {
    background-color: #2d3748;
    border: 2px solid #4a5568;
    color: #f7fafc;
}

QLineEdit:focus {
    border-color: #63b3ed;
}

QTextEdit {
    background-color: #2d3748;
    border: 2px solid #4a5568;
    color: #e2e8f0;
}

QRadioButton {
    background-color: #2d3748;
    border: 2px solid #4a5568;
    color: #e2e8f0;
}

QRadioButton:checked {
    background-color: #3c4043;
    border-color: #63b3ed;
    color: #90cdf4;
}
"""

# Success/Error State Colors
SUCCESS_COLORS = {
    'light': {'bg': '#f0fff4', 'border': '#48bb78', 'text': '#22543d'},
    'dark': {'bg': '#1a2f1a', 'border': '#48bb78', 'text': '#9ae6b4'}
}

ERROR_COLORS = {
    'light': {'bg': '#fffafa', 'border': '#f56565', 'text': '#742a2a'},
    'dark': {'bg': '#2d1b1b', 'border': '#f56565', 'text': '#fc8181'}
}

def apply_feedback_styling(widget, is_correct: bool, is_dark_mode: bool):
    """Apply visual feedback styling based on answer correctness"""
    theme = 'dark' if is_dark_mode else 'light'
    colors = SUCCESS_COLORS[theme] if is_correct else ERROR_COLORS[theme]
    
    style = f"""
    background-color: {colors['bg']};
    border: 2px solid {colors['border']};
    color: {colors['text']};
    """
    
    widget.setStyleSheet(widget.styleSheet() + style)
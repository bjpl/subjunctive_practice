# Improved Layout Design for Better Space Utilization

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

def create_optimized_layout(self):
    """Create a more efficient layout with better space utilization"""
    
    # Main container with improved proportions
    main_container = QWidget()
    main_layout = QVBoxLayout(main_container)
    main_layout.setSpacing(16)
    main_layout.setContentsMargins(20, 20, 20, 20)
    
    # Header section - compact and informative
    header_widget = self.create_header_section()
    main_layout.addWidget(header_widget)
    
    # Content area with 70-30 split instead of 50-50
    content_splitter = QSplitter(Qt.Horizontal)
    content_splitter.setSizes([700, 300])  # 70-30 ratio
    
    # Main exercise area (left - 70%)
    exercise_area = self.create_exercise_area()
    content_splitter.addWidget(exercise_area)
    
    # Controls and feedback area (right - 30%)
    controls_area = self.create_controls_area()
    content_splitter.addWidget(controls_area)
    
    main_layout.addWidget(content_splitter, 1)  # Takes remaining space
    
    # Footer with status and quick actions
    footer_widget = self.create_footer_section()
    main_layout.addWidget(footer_widget)
    
    return main_container

def create_header_section(self):
    """Compact header with essential information"""
    header = QWidget()
    header.setFixedHeight(80)
    header.setStyleSheet("""
        QWidget {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                      stop:0 #667eea, stop:1 #764ba2);
            border-radius: 12px;
            color: white;
        }
    """)
    
    layout = QHBoxLayout(header)
    layout.setContentsMargins(20, 15, 20, 15)
    
    # App title and mode indicator
    title_section = QVBoxLayout()
    title_label = QLabel("Spanish Subjunctive Practice")
    title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
    
    mode_label = QLabel("Traditional Mode")  # Dynamic based on current mode
    mode_label.setStyleSheet("font-size: 14px; color: rgba(255,255,255,0.8);")
    
    title_section.addWidget(title_label)
    title_section.addWidget(mode_label)
    layout.addLayout(title_section)
    
    layout.addStretch()
    
    # Quick stats in header
    stats_container = QHBoxLayout()
    
    progress_info = self.create_header_stat("Progress", "3/5")
    accuracy_info = self.create_header_stat("Accuracy", "80%")
    streak_info = self.create_header_stat("Streak", "5 days")
    
    stats_container.addWidget(progress_info)
    stats_container.addWidget(accuracy_info)
    stats_container.addWidget(streak_info)
    
    layout.addLayout(stats_container)
    
    return header

def create_header_stat(self, label: str, value: str):
    """Create a compact stat display for header"""
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setSpacing(2)
    layout.setContentsMargins(10, 5, 10, 5)
    
    value_label = QLabel(value)
    value_label.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
    value_label.setAlignment(Qt.AlignCenter)
    
    label_widget = QLabel(label)
    label_widget.setStyleSheet("font-size: 12px; color: rgba(255,255,255,0.8);")
    label_widget.setAlignment(Qt.AlignCenter)
    
    layout.addWidget(value_label)
    layout.addWidget(label_widget)
    
    return widget

def create_exercise_area(self):
    """Main exercise display area with optimized layout"""
    container = QScrollArea()
    container.setWidgetResizable(True)
    container.setFrameShape(QFrame.NoFrame)
    
    content_widget = QWidget()
    layout = QVBoxLayout(content_widget)
    layout.setSpacing(20)
    layout.setContentsMargins(20, 20, 20, 20)
    
    # Exercise header with number and difficulty
    exercise_header = QHBoxLayout()
    
    exercise_num = QLabel("Exercise 3 of 5")
    exercise_num.setStyleSheet("""
        font-size: 16px; 
        font-weight: bold; 
        color: #4a5568;
        background-color: #edf2f7;
        padding: 8px 16px;
        border-radius: 20px;
    """)
    
    difficulty_badge = QLabel("Intermediate")
    difficulty_badge.setStyleSheet("""
        font-size: 14px;
        color: #d69e2e;
        background-color: #faf089;
        padding: 6px 12px;
        border-radius: 12px;
        font-weight: 500;
    """)
    
    exercise_header.addWidget(exercise_num)
    exercise_header.addStretch()
    exercise_header.addWidget(difficulty_badge)
    layout.addLayout(exercise_header)
    
    # Context card (collapsible)
    context_card = self.create_collapsible_context()
    layout.addWidget(context_card)
    
    # Main sentence - prominent display
    sentence_container = QWidget()
    sentence_container.setStyleSheet("""
        QWidget {
            background-color: #fff3cd;
            border: 2px solid #ffeaa7;
            border-radius: 12px;
            padding: 20px;
        }
    """)
    
    sentence_layout = QVBoxLayout(sentence_container)
    
    self.sentence_label = QLabel()
    self.sentence_label.setStyleSheet("""
        font-size: 22px;
        font-weight: 500;
        color: #212529;
        line-height: 1.6;
    """)
    self.sentence_label.setWordWrap(True)
    sentence_layout.addWidget(self.sentence_label)
    
    # Translation toggle (inline)
    translation_layout = QHBoxLayout()
    translation_btn = QPushButton("Show Translation")
    translation_btn.setStyleSheet("""
        QPushButton {
            font-size: 14px;
            color: #6c757d;
            background: transparent;
            border: 1px solid #dee2e6;
            border-radius: 6px;
            padding: 6px 12px;
        }
        QPushButton:hover {
            background-color: #f8f9fa;
        }
    """)
    translation_layout.addStretch()
    translation_layout.addWidget(translation_btn)
    sentence_layout.addLayout(translation_layout)
    
    layout.addWidget(sentence_container)
    
    # Answer input area
    input_section = self.create_answer_input_section()
    layout.addWidget(input_section)
    
    layout.addStretch()
    container.setWidget(content_widget)
    
    return container

def create_collapsible_context(self):
    """Create a collapsible context section to save space"""
    container = QWidget()
    layout = QVBoxLayout(container)
    layout.setSpacing(0)
    layout.setContentsMargins(0, 0, 0, 0)
    
    # Header with toggle button
    header = QWidget()
    header.setStyleSheet("""
        QWidget {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px 8px 0 0;
            padding: 8px 16px;
        }
    """)
    
    header_layout = QHBoxLayout(header)
    context_title = QLabel("📋 Context & Scenario")
    context_title.setStyleSheet("font-weight: 500; color: #495057;")
    
    toggle_btn = QPushButton("▼")
    toggle_btn.setFixedSize(24, 24)
    toggle_btn.setStyleSheet("""
        QPushButton {
            border: none;
            background: transparent;
            font-weight: bold;
        }
    """)
    
    header_layout.addWidget(context_title)
    header_layout.addStretch()
    header_layout.addWidget(toggle_btn)
    
    # Collapsible content
    self.context_content = QLabel("Context will appear here...")
    self.context_content.setStyleSheet("""
        QLabel {
            background-color: #ffffff;
            border: 1px solid #dee2e6;
            border-top: none;
            border-radius: 0 0 8px 8px;
            padding: 16px;
            color: #6c757d;
            font-style: italic;
        }
    """)
    self.context_content.setWordWrap(True)
    
    layout.addWidget(header)
    layout.addWidget(self.context_content)
    
    # Toggle functionality
    def toggle_context():
        visible = self.context_content.isVisible()
        self.context_content.setVisible(not visible)
        toggle_btn.setText("▲" if not visible else "▼")
    
    toggle_btn.clicked.connect(toggle_context)
    
    return container

def create_answer_input_section(self):
    """Enhanced answer input with better visual feedback"""
    container = QGroupBox("Your Answer")
    container.setStyleSheet("""
        QGroupBox {
            font-size: 18px;
            font-weight: 600;
            color: #2d3748;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            padding: 20px;
        }
    """)
    
    layout = QVBoxLayout(container)
    
    # Input stack for different modes
    self.input_stack = QStackedWidget()
    
    # Free response page with enhanced styling
    free_page = QWidget()
    free_layout = QVBoxLayout(free_page)
    
    input_container = QWidget()
    input_container.setStyleSheet("""
        QWidget {
            background-color: white;
            border: 3px solid #e2e8f0;
            border-radius: 12px;
            padding: 4px;
        }
    """)
    
    input_layout = QHBoxLayout(input_container)
    input_layout.setContentsMargins(16, 8, 16, 8)
    
    self.free_response_input = QLineEdit()
    self.free_response_input.setStyleSheet("""
        QLineEdit {
            font-size: 20px;
            border: none;
            padding: 12px 0;
            background: transparent;
        }
        QLineEdit:focus {
            outline: none;
        }
    """)
    self.free_response_input.setPlaceholderText("Type your conjugation here...")
    
    # Voice input button (future feature)
    voice_btn = QPushButton("🎤")
    voice_btn.setFixedSize(40, 40)
    voice_btn.setStyleSheet("""
        QPushButton {
            border: none;
            border-radius: 20px;
            background-color: #f0f0f0;
            font-size: 16px;
        }
        QPushButton:hover {
            background-color: #e0e0e0;
        }
    """)
    
    input_layout.addWidget(self.free_response_input)
    input_layout.addWidget(voice_btn)
    
    free_layout.addWidget(input_container)
    self.input_stack.addWidget(free_page)
    
    # Multiple choice page with card-style options
    mc_page = QWidget()
    mc_layout = QVBoxLayout(mc_page)
    
    self.mc_container = QWidget()
    self.mc_grid = QGridLayout(self.mc_container)
    self.mc_grid.setSpacing(12)
    
    mc_layout.addWidget(self.mc_container)
    self.input_stack.addWidget(mc_page)
    
    layout.addWidget(self.input_stack)
    
    return container

def create_controls_area(self):
    """Compact controls area with better organization"""
    container = QScrollArea()
    container.setWidgetResizable(True)
    container.setFrameShape(QFrame.NoFrame)
    
    content = QWidget()
    layout = QVBoxLayout(content)
    layout.setSpacing(16)
    layout.setContentsMargins(16, 20, 16, 20)
    
    # Quick action buttons
    actions_group = QGroupBox("Actions")
    actions_layout = QGridLayout(actions_group)
    actions_layout.setSpacing(8)
    
    hint_btn = QPushButton("💡 Hint")
    submit_btn = QPushButton("✓ Submit")
    skip_btn = QPushButton("→ Skip")
    
    # Style action buttons consistently
    button_style = """
        QPushButton {
            padding: 12px;
            font-size: 14px;
            font-weight: 500;
            border-radius: 8px;
            min-height: 20px;
        }
    """
    
    hint_btn.setStyleSheet(button_style + """
        QPushButton {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
        }
        QPushButton:hover {
            background-color: #ffeaa7;
        }
    """)
    
    submit_btn.setStyleSheet(button_style + """
        QPushButton {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }
        QPushButton:hover {
            background-color: #c3e6cb;
        }
    """)
    
    actions_layout.addWidget(hint_btn, 0, 0)
    actions_layout.addWidget(submit_btn, 0, 1)
    actions_layout.addWidget(skip_btn, 1, 0, 1, 2)
    
    layout.addWidget(actions_group)
    
    # Feedback area - more compact
    feedback_group = QGroupBox("Feedback")
    feedback_layout = QVBoxLayout(feedback_group)
    
    self.feedback_text = QTextEdit()
    self.feedback_text.setMaximumHeight(200)
    self.feedback_text.setStyleSheet("""
        QTextEdit {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 12px;
            font-size: 14px;
        }
    """)
    feedback_layout.addWidget(self.feedback_text)
    
    layout.addWidget(feedback_group)
    
    # Navigation - compact
    nav_group = QGroupBox("Navigation")
    nav_layout = QHBoxLayout(nav_group)
    
    prev_btn = QPushButton("‹ Prev")
    next_btn = QPushButton("Next ›")
    
    nav_btn_style = """
        QPushButton {
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: 500;
        }
    """
    
    prev_btn.setStyleSheet(nav_btn_style)
    next_btn.setStyleSheet(nav_btn_style)
    
    nav_layout.addWidget(prev_btn)
    nav_layout.addWidget(next_btn)
    
    layout.addWidget(nav_group)
    
    layout.addStretch()
    
    container.setWidget(content)
    return container

def create_footer_section(self):
    """Footer with status and quick settings"""
    footer = QWidget()
    footer.setFixedHeight(50)
    footer.setStyleSheet("""
        QWidget {
            background-color: #f8f9fa;
            border-top: 1px solid #dee2e6;
        }
    """)
    
    layout = QHBoxLayout(footer)
    layout.setContentsMargins(20, 10, 20, 10)
    
    # Status message
    self.status_label = QLabel("Ready to practice")
    self.status_label.setStyleSheet("color: #6c757d; font-size: 14px;")
    
    layout.addWidget(self.status_label)
    layout.addStretch()
    
    # Quick toggle buttons
    theme_btn = QPushButton("🌙")
    theme_btn.setToolTip("Toggle Dark Mode")
    theme_btn.setFixedSize(30, 30)
    
    sound_btn = QPushButton("🔊")
    sound_btn.setToolTip("Toggle Sound")
    sound_btn.setFixedSize(30, 30)
    
    settings_btn = QPushButton("⚙️")
    settings_btn.setToolTip("Settings")
    settings_btn.setFixedSize(30, 30)
    
    for btn in [theme_btn, sound_btn, settings_btn]:
        btn.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 15px;
                background: transparent;
            }
            QPushButton:hover {
                background-color: rgba(0,0,0,0.1);
            }
        """)
    
    layout.addWidget(theme_btn)
    layout.addWidget(sound_btn)
    layout.addWidget(settings_btn)
    
    return footer
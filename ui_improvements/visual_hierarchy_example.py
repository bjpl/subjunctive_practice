# Visual Hierarchy Improvements - Content Prioritization

def create_improved_content_display(self):
    """Enhanced content layout with clear visual hierarchy"""
    
    # Main exercise display with improved typography
    exercise_container = QGroupBox()
    exercise_container.setStyleSheet("""
        QGroupBox {
            border: 2px solid #4A90E2;
            border-radius: 12px;
            padding: 20px;
            margin: 10px;
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                                      stop:0 #f8f9fa, stop:1 #ffffff);
        }
    """)
    
    exercise_layout = QVBoxLayout(exercise_container)
    
    # Exercise number with prominence
    self.exercise_number_label = QLabel()
    self.exercise_number_label.setStyleSheet("""
        QLabel {
            font-size: 14px;
            font-weight: bold;
            color: #6c757d;
            text-transform: uppercase;
            letter-spacing: 1px;
            padding: 5px 0;
        }
    """)
    exercise_layout.addWidget(self.exercise_number_label)
    
    # Context with distinct styling
    self.context_label = QLabel()
    self.context_label.setStyleSheet("""
        QLabel {
            font-size: 16px;
            color: #495057;
            font-style: italic;
            padding: 10px;
            background-color: #e9ecef;
            border-left: 4px solid #17a2b8;
            border-radius: 4px;
            margin-bottom: 15px;
        }
    """)
    self.context_label.setWordWrap(True)
    exercise_layout.addWidget(self.context_label)
    
    # Main sentence with primary emphasis
    self.sentence_label = QLabel()
    self.sentence_label.setStyleSheet("""
        QLabel {
            font-size: 20px;
            font-weight: 600;
            color: #212529;
            line-height: 1.6;
            padding: 15px;
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 8px;
        }
    """)
    self.sentence_label.setWordWrap(True)
    exercise_layout.addWidget(self.sentence_label)
    
    return exercise_container

def create_progress_card(self):
    """Consolidated progress indicator card"""
    progress_card = QGroupBox("Progress Overview")
    progress_card.setStyleSheet("""
        QGroupBox {
            font-size: 16px;
            font-weight: bold;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
        }
        QGroupBox::title {
            color: #495057;
            padding: 0 10px;
        }
    """)
    
    layout = QVBoxLayout(progress_card)
    
    # Main progress bar with enhanced styling
    self.main_progress = QProgressBar()
    self.main_progress.setStyleSheet("""
        QProgressBar {
            border: 2px solid #e9ecef;
            border-radius: 8px;
            background-color: #f8f9fa;
            text-align: center;
            font-weight: bold;
            height: 25px;
        }
        QProgressBar::chunk {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                      stop:0 #28a745, stop:1 #20c997);
            border-radius: 6px;
        }
    """)
    layout.addWidget(self.main_progress)
    
    # Statistics in a grid layout
    stats_container = QWidget()
    stats_layout = QGridLayout(stats_container)
    stats_layout.setSpacing(10)
    
    # Accuracy indicator
    self.accuracy_widget = self.create_stat_widget("Accuracy", "0%", "#28a745")
    stats_layout.addWidget(self.accuracy_widget, 0, 0)
    
    # Streak indicator
    self.streak_widget = self.create_stat_widget("Streak", "0 days", "#fd7e14")
    stats_layout.addWidget(self.streak_widget, 0, 1)
    
    # Hints used
    self.hints_widget = self.create_stat_widget("Hints Used", "0", "#6f42c1")
    stats_layout.addWidget(self.hints_widget, 1, 0)
    
    # Time elapsed
    self.time_widget = self.create_stat_widget("Time", "0m", "#17a2b8")
    stats_layout.addWidget(self.time_widget, 1, 1)
    
    layout.addWidget(stats_container)
    return progress_card

def create_stat_widget(self, title: str, value: str, color: str):
    """Create individual stat display widget"""
    widget = QWidget()
    widget.setStyleSheet(f"""
        QWidget {{
            background-color: {color}15;
            border: 1px solid {color}40;
            border-radius: 6px;
            padding: 8px;
        }}
    """)
    
    layout = QVBoxLayout(widget)
    layout.setSpacing(2)
    
    title_label = QLabel(title)
    title_label.setStyleSheet(f"""
        QLabel {{
            font-size: 12px;
            color: {color};
            font-weight: bold;
            text-transform: uppercase;
        }}
    """)
    title_label.setAlignment(Qt.AlignCenter)
    
    value_label = QLabel(value)
    value_label.setStyleSheet("""
        QLabel {
            font-size: 18px;
            font-weight: bold;
            color: #212529;
        }
    """)
    value_label.setAlignment(Qt.AlignCenter)
    
    layout.addWidget(title_label)
    layout.addWidget(value_label)
    
    return widget
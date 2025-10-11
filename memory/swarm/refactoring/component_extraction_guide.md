# Component Extraction Guide
## Spanish Subjunctive Practice MVC Refactoring

### Code Extraction Mappings

This guide provides specific line number mappings from the monolithic main.py to the new MVC components, enabling precise extraction of functionality while preserving all features.

## Model Layer Extractions

### UserModel (user_model.py)
**Source Lines: 432-444, 2058-2164, 3786-3859**

```python
# Extract from main.py lines 432-444
class UserModel(BaseModel):
    def __init__(self):
        # From: self.dark_mode = False (line 433)
        self.theme_preference = "light"
        
        # From: self.show_translation = False (line 434) 
        self.display_preferences = {
            "show_translation": False,
            "show_hints": True,
            "auto_generate": False
        }
        
        # From accessibility initialization (lines 3786-3859)
        self.accessibility_settings = {
            "screen_reader_support": False,
            "high_contrast": False,
            "large_fonts": False,
            "keyboard_navigation": True
        }
    
    # Extract from toggleTheme() lines 2058-2164
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        self.theme_preference = "dark" if self.theme_preference == "light" else "light"
        self.emit_change("theme_changed", self.theme_preference)
    
    # Extract from _initialize_enhanced_accessibility() lines 3786-3819
    def configure_accessibility(self, settings: dict):
        """Configure accessibility settings"""
        self.accessibility_settings.update(settings)
        self.emit_change("accessibility_changed", self.accessibility_settings)
```

### SessionModel (session_model.py)
**Source Lines: 416-431, 3184-3294, 3952-3976**

```python
# Extract from main.py lines 416-431
class SessionModel(BaseModel):
    def __init__(self):
        # From: self.exercises: List[dict] = [] (line 417)
        self.exercises = []
        
        # From: self.current_exercise: int = 0 (line 418)
        self.current_exercise_index = 0
        
        # From: self.responses: List[dict] = [] (line 421)
        self.responses = []
        
        # From: self.session_stats: Dict (lines 423-430)
        self.session_stats = {
            "total_attempts": 0,
            "correct_attempts": 0,
            "hints_used": 0,
            "session_start": datetime.now(),
            "tenses_practiced": set(),
            "persons_practiced": set()
        }
        
        # From: self.correct_count: int = 0 (line 420)
        self.performance_metrics = {
            "correct_count": 0,
            "total_count": 0,
            "accuracy_rate": 0.0,
            "streak_count": 0
        }
    
    # Extract from saveProgress() lines 3184-3194
    def save_progress(self, filename: str = None):
        """Save current session progress"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"session_{timestamp}.json"
        
        session_data = {
            "exercises": self.exercises,
            "responses": self.responses,
            "stats": self.session_stats,
            "metrics": self.performance_metrics
        }
        
        # Implementation from original lines 3184-3194
        with open(f"user_data/{filename}", 'w', encoding='utf-8') as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
        
        return filename
    
    # Extract from exportSession() lines 3294-3328
    def export_session(self, format_type: str = "csv"):
        """Export session data in specified format"""
        if format_type == "csv":
            # Implementation from lines 3304-3328
            return self._export_to_csv()
        elif format_type == "json":
            return self._export_to_json()
    
    # Extract from closeEvent() lines 3952-3976
    def save_session_log(self):
        """Save detailed session log"""
        try:
            with open("subjunctive_session_log.txt", "a", encoding="utf-8") as f:
                f.write("\n=== Subjunctive Session Log ===\n")
                for r in self.responses:
                    f.write(
                        f"Exercise {r['exercise_index']+1}\n"
                        f"  Sentence: {r['sentence']}\n"
                        f"  Translation: {r['translation']}\n"
                        f"  User answer: {r['user_answer']}\n"
                        f"  Correct: {r['correct']}\n"
                        f"  Explanation: {r['explanation']}\n\n"
                    )
                f.write("=== End of Session ===\n\n")
        except Exception as e:
            raise ModelException(f"Error writing session log: {e}")
```

### ExerciseModel (exercise_model.py)
**Source Lines: 2595-2796, 2848-2898**

```python
# Extract from exercise generation and management
class ExerciseModel(BaseModel):
    def __init__(self):
        self.current_exercise = None
        self.exercise_queue = []
        self.exercise_history = []
        self.generation_params = {}
        self.answer_state = {
            "user_answer": "",
            "is_correct": None,
            "explanation": "",
            "hints_used": 0
        }
    
    # Extract from generateNewExercise() lines 2595-2660
    def generate_exercise(self, triggers: list, tenses: list, persons: list):
        """Generate new exercise with given parameters"""
        if not triggers or not tenses or not persons:
            raise ModelException("Missing required selection parameters")
        
        self.generation_params = {
            "triggers": triggers,
            "tenses": tenses,
            "persons": persons,
            "timestamp": datetime.now()
        }
        
        # Core generation logic from lines 2595-2660
        # This would integrate with the TBLTService
        exercise_data = self._create_exercise_from_params()
        self.current_exercise = exercise_data
        self.emit_change("exercise_generated", exercise_data)
        
        return exercise_data
    
    # Extract from populateMultipleChoice() lines 2848-2867
    def create_multiple_choice_options(self, correct_answer: str):
        """Create multiple choice options for the exercise"""
        # Logic from lines 2848-2867
        choices = [correct_answer]
        # Add distractors based on conjugation patterns
        # Implementation details...
        return choices
    
    # Extract from getUserAnswer() and answer validation
    def validate_answer(self, user_answer: str):
        """Validate user's answer against correct answer"""
        correct_answer = self.current_exercise.get("correct_answer", "")
        is_correct = self._check_answer_correctness(user_answer, correct_answer)
        
        self.answer_state.update({
            "user_answer": user_answer,
            "is_correct": is_correct,
            "timestamp": datetime.now()
        })
        
        self.emit_change("answer_validated", self.answer_state)
        return is_correct
```

## View Layer Extractions

### MainWindow (main_window.py)
**Source Lines: 405-408, 518-614, 3921-3951**

```python
# Extract from main window initialization
class MainWindow(BaseView):
    def __init__(self):
        super().__init__()
        # From: self.setWindowTitle() and geometry (lines 405-408)
        self.setWindowTitle("Spanish Subjunctive Practice")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(1000, 600)
        
        # Initialize child panels
        self.selection_panel = None
        self.exercise_panel = None
        self.stats_panel = None
        self.main_splitter = None
        
        self._initial_column_setup_done = False
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the main window UI layout"""
        # Extract from initUI() lines 518-614
        self.create_central_widget()
        self.create_menu_bar()
        self.create_status_bar()
        self.create_toolbar()
    
    def create_central_widget(self):
        """Create the main splitter layout"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Three-column layout with splitter
        self.main_splitter = QSplitter(Qt.Horizontal)
        
        # Add panels (will be injected by controller)
        # self.main_splitter.addWidget(self.selection_panel)
        # self.main_splitter.addWidget(self.exercise_panel)  
        # self.main_splitter.addWidget(self.stats_panel)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(self.main_splitter)
    
    # Extract from showEvent() lines 3921-3930
    def showEvent(self, event):
        """Handle window show event"""
        super().showEvent(event)
        
        if not self._initial_column_setup_done:
            QTimer.singleShot(100, self._adjust_column_proportions)
            self._initial_column_setup_done = True
    
    # Extract from _adjust_column_proportions() lines 3932-3944
    def _adjust_column_proportions(self):
        """Set optimal column width proportions"""
        try:
            if hasattr(self, 'main_splitter'):
                total_width = self.main_splitter.width()
                if total_width > 100:
                    self.main_splitter.setSizes([
                        int(total_width * 0.40),  # 40% for left
                        int(total_width * 0.35),  # 35% for middle  
                        int(total_width * 0.25)   # 25% for right
                    ])
        except Exception as e:
            self.emit_error(f"Error adjusting column proportions: {e}")
```

### SelectionPanel (selection_panel.py)
**Source Lines: 665-826, 2328-2501**

```python
# Extract from control panel creation
class SelectionPanel(BaseView):
    def __init__(self):
        super().__init__()
        self.trigger_checkboxes = {}
        self.tense_checkboxes = {}
        self.person_checkboxes = {}
        
        self.setup_ui()
    
    def setup_ui(self):
        """Create the selection panel UI"""
        # Extract from createControlPanel() lines 665-826
        main_layout = QVBoxLayout(self)
        
        # Create trigger selection group
        self.create_trigger_group(main_layout)
        
        # Create tense selection group  
        self.create_tense_group(main_layout)
        
        # Create person selection group
        self.create_person_group(main_layout)
        
        # Create action buttons
        self.create_action_buttons(main_layout)
    
    def create_trigger_group(self, parent_layout):
        """Create trigger selection checkboxes"""
        trigger_group = QGroupBox("Subjunctive Triggers")
        trigger_layout = QVBoxLayout(trigger_group)
        
        # Extract checkbox creation logic from lines 665-750
        triggers = [
            "que", "ojalá", "es importante que", "dudo que",
            "no creo que", "cuando", "después de que", "hasta que"
        ]
        
        for trigger in triggers:
            checkbox = QCheckBox(trigger)
            checkbox.stateChanged.connect(
                lambda state, t=trigger: self.on_selection_changed(t, state)
            )
            self.trigger_checkboxes[trigger] = checkbox
            trigger_layout.addWidget(checkbox)
        
        parent_layout.addWidget(trigger_group)
    
    # Extract from getSelectedTriggers() lines 2328-2335
    def get_selected_triggers(self) -> list:
        """Get list of selected triggers"""
        return [
            trigger for trigger, checkbox in self.trigger_checkboxes.items()
            if checkbox.isChecked()
        ]
    
    # Extract from onSelectionChanged() lines 2379-2419  
    def on_selection_changed(self, item: str, state: int):
        """Handle selection change events"""
        is_checked = state == 2  # Qt.Checked
        
        # Emit selection changed signal
        self.emit_signal("selection_changed", {
            "item": item,
            "checked": is_checked,
            "current_selection": self.get_current_selection()
        })
    
    def get_current_selection(self) -> dict:
        """Get current selection state"""
        return {
            "triggers": self.get_selected_triggers(),
            "tenses": self.get_selected_tenses(),
            "persons": self.get_selected_persons()
        }
```

### ExercisePanel (exercise_panel.py)
**Source Lines: 827-984, 1093-1274**

```python
# Extract from practice area creation
class ExercisePanel(BaseView):
    def __init__(self):
        super().__init__()
        
        # UI components
        self.sentence_label = None
        self.translation_label = None
        self.answer_input = None
        self.multiple_choice_group = None
        self.navigation_buttons = {}
        
        # State
        self.current_mode = "fill_in_blank"  # or "multiple_choice"
        
        self.setup_ui()
    
    def setup_ui(self):
        """Create the exercise panel UI"""
        # Extract from createPracticeArea() lines 827-984
        main_layout = QVBoxLayout(self)
        
        # Exercise display area
        self.create_exercise_display(main_layout)
        
        # Answer input area (stacked widget for different modes)
        self.create_answer_input_area(main_layout)
        
        # Navigation buttons
        self.create_navigation_buttons(main_layout)
    
    def create_exercise_display(self, parent_layout):
        """Create sentence and translation display"""
        # Extract from lines 827-900
        exercise_group = QGroupBox("Current Exercise")
        exercise_layout = QVBoxLayout(exercise_group)
        
        # Sentence label with enhanced styling
        self.sentence_label = QLabel("Select triggers, tenses, and persons to begin.")
        self.sentence_label.setWordWrap(True)
        self.sentence_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
            }
        """)
        
        # Translation label (initially hidden)
        self.translation_label = QLabel("Translation will appear here")
        self.translation_label.setWordWrap(True)
        self.translation_label.setVisible(False)
        
        exercise_layout.addWidget(self.sentence_label)
        exercise_layout.addWidget(self.translation_label)
        parent_layout.addWidget(exercise_group)
    
    def create_answer_input_area(self, parent_layout):
        """Create answer input with mode switching"""
        # Extract from lines 901-984, 1093-1274
        answer_group = QGroupBox("Your Answer")
        answer_layout = QVBoxLayout(answer_group)
        
        # Stacked widget for different input modes
        self.answer_stack = QStackedWidget()
        
        # Fill-in-the-blank input
        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText("Enter your conjugation here...")
        self.answer_input.returnPressed.connect(
            lambda: self.emit_signal("submit_answer")
        )
        
        # Multiple choice buttons
        self.multiple_choice_widget = QWidget()
        self.multiple_choice_layout = QVBoxLayout(self.multiple_choice_widget)
        self.multiple_choice_group = QButtonGroup(self.multiple_choice_widget)
        
        self.answer_stack.addWidget(self.answer_input)
        self.answer_stack.addWidget(self.multiple_choice_widget)
        
        answer_layout.addWidget(self.answer_stack)
        parent_layout.addWidget(answer_group)
    
    # Extract from populateMultipleChoice() lines 2848-2867
    def populate_multiple_choice(self, choices: list):
        """Populate multiple choice options"""
        # Clear existing choices
        for button in self.multiple_choice_group.buttons():
            self.multiple_choice_group.removeButton(button)
            button.deleteLater()
        
        # Add new choices
        for i, choice in enumerate(choices):
            radio_button = QRadioButton(choice)
            self.multiple_choice_group.addButton(radio_button, i)
            self.multiple_choice_layout.addWidget(radio_button)
        
        # Switch to multiple choice mode
        self.answer_stack.setCurrentWidget(self.multiple_choice_widget)
        self.current_mode = "multiple_choice"
    
    def get_user_answer(self) -> str:
        """Get the user's current answer"""
        if self.current_mode == "fill_in_blank":
            return self.answer_input.text().strip()
        else:  # multiple_choice
            selected_button = self.multiple_choice_group.checkedButton()
            return selected_button.text() if selected_button else ""
    
    def update_exercise_display(self, exercise_data: dict):
        """Update the exercise display with new data"""
        sentence = exercise_data.get("sentence", "")
        translation = exercise_data.get("translation", "")
        
        self.sentence_label.setText(sentence)
        self.translation_label.setText(translation)
        
        # Clear previous answer
        self.answer_input.clear()
        
        # Reset to fill-in-blank mode by default
        self.answer_stack.setCurrentWidget(self.answer_input)
        self.current_mode = "fill_in_blank"
```

## Controller Layer Extractions

### ExerciseController (exercise_controller.py)
**Source Lines: 2595-3088, 2899-2982**

```python
# Extract from exercise management logic
class ExerciseController(BaseController):
    def __init__(self, exercise_model, exercise_view, api_controller):
        super().__init__()
        self.exercise_model = exercise_model
        self.exercise_view = exercise_view
        self.api_controller = api_controller
        
        # Services (injected)
        self.tblt_service = None
        self.conjugation_service = None
        
        self.setup_connections()
    
    def setup_connections(self):
        """Set up model-view connections"""
        # Connect model events
        self.exercise_model.connect("exercise_generated", self.on_exercise_generated)
        self.exercise_model.connect("answer_validated", self.on_answer_validated)
        
        # Connect view events
        self.exercise_view.connect("submit_answer", self.handle_submit_answer)
        self.exercise_view.connect("request_hint", self.handle_hint_request)
        self.exercise_view.connect("next_exercise", self.handle_next_exercise)
        self.exercise_view.connect("prev_exercise", self.handle_prev_exercise)
    
    # Extract from generateNewExercise() lines 2595-2660
    def generate_new_exercise(self, selection_data: dict):
        """Generate new exercise based on selection"""
        triggers = selection_data.get("triggers", [])
        tenses = selection_data.get("tenses", [])
        persons = selection_data.get("persons", [])
        
        if not all([triggers, tenses, persons]):
            self.emit_error("Please select triggers, tenses, and persons")
            return
        
        try:
            # Use the exercise model to generate
            exercise = self.exercise_model.generate_exercise(triggers, tenses, persons)
            return exercise
        except Exception as e:
            self.emit_error(f"Error generating exercise: {e}")
    
    # Extract from submitAnswer() lines 2899-2982  
    def handle_submit_answer(self):
        """Handle answer submission"""
        user_answer = self.exercise_view.get_user_answer()
        
        if not user_answer.strip():
            self.emit_error("Please enter an answer")
            return
        
        # Validate answer through model
        is_correct = self.exercise_model.validate_answer(user_answer)
        
        # Get exercise data for explanation generation
        exercise_data = self.exercise_model.current_exercise
        correct_answer = exercise_data.get("correct_answer", "")
        sentence = exercise_data.get("sentence", "")
        
        # Generate explanation asynchronously
        self.api_controller.generate_explanation(
            user_answer=user_answer,
            correct_answer=correct_answer,
            is_correct=is_correct,
            sentence=sentence,
            callback=self.on_explanation_received
        )
    
    def on_explanation_received(self, explanation: str):
        """Handle explanation from API"""
        # Update view with explanation
        self.exercise_view.show_explanation(explanation)
        
        # Update session stats through model
        self.exercise_model.record_answer_result(explanation)
    
    # Extract from provideHint() lines 3035-3068
    def handle_hint_request(self):
        """Handle hint request"""
        exercise_data = self.exercise_model.current_exercise
        
        if not exercise_data:
            self.emit_error("No exercise available for hint")
            return
        
        # Generate hint through API
        self.api_controller.generate_hint(
            sentence=exercise_data.get("sentence", ""),
            correct_answer=exercise_data.get("correct_answer", ""),
            callback=self.on_hint_received
        )
    
    def on_hint_received(self, hint: str):
        """Handle hint from API"""
        self.exercise_view.show_hint(hint)
        self.exercise_model.increment_hints_used()
    
    # Extract from nextExercise() lines 3088-3111
    def handle_next_exercise(self):
        """Move to next exercise"""
        if self.exercise_model.has_next_exercise():
            next_exercise = self.exercise_model.get_next_exercise()
            self.exercise_view.update_exercise_display(next_exercise)
        else:
            # Generate new exercise or show completion
            self.handle_exercise_completion()
    
    # Extract from prevExercise() lines 3112-3135
    def handle_prev_exercise(self):
        """Move to previous exercise"""
        if self.exercise_model.has_prev_exercise():
            prev_exercise = self.exercise_model.get_prev_exercise()
            self.exercise_view.update_exercise_display(prev_exercise)
        else:
            self.emit_error("No previous exercise available")
```

### ApiController (api_controller.py)
**Source Lines: 253-394, 2983-3088, 3673-3785**

```python
# Extract from API integration logic
class ApiController(BaseController):
    def __init__(self):
        super().__init__()
        self.client = None
        self.thread_pool = QThreadPool()
        self.request_queue = Queue()
        
        self.initialize_client()
    
    def initialize_client(self):
        """Initialize OpenAI client"""
        # Extract from API initialization (lines 114-140)
        try:
            load_dotenv()
            api_key = os.getenv('OPENAI_API_KEY')
            
            if not api_key:
                raise ApiException("OpenAI API key not found")
            
            self.client = OpenAI(api_key=api_key)
            
        except Exception as e:
            self.emit_error(f"Failed to initialize API client: {e}")
    
    # Extract from generateGPTExplanationAsync() lines 2983-3005
    def generate_explanation(self, user_answer: str, correct_answer: str, 
                           is_correct: bool, sentence: str, callback):
        """Generate explanation asynchronously"""
        prompt = self._create_explanation_prompt(
            user_answer, correct_answer, is_correct, sentence
        )
        
        # Use worker runnable (extracted from lines 253-394)
        worker = GPTWorkerRunnable(
            prompt=prompt,
            model="gpt-4",
            max_tokens=600,
            temperature=0.5
        )
        
        worker.signals.result.connect(callback)
        worker.signals.error.connect(self.handle_api_error)
        
        self.thread_pool.start(worker)
    
    def generate_hint(self, sentence: str, correct_answer: str, callback):
        """Generate hint asynchronously"""
        prompt = f"""
        Provide a helpful hint for this Spanish subjunctive exercise:
        Sentence: {sentence}
        
        Give a hint about which conjugation to use without revealing the answer.
        Focus on the trigger or grammatical rule that applies.
        """
        
        worker = GPTWorkerRunnable(
            prompt=prompt,
            model="gpt-4",
            max_tokens=300,
            temperature=0.7
        )
        
        worker.signals.result.connect(callback)
        worker.signals.error.connect(self.handle_api_error)
        
        self.thread_pool.start(worker)
    
    # Extract from testAPIConnection() lines 3673-3785
    def test_connection(self, callback):
        """Test API connection health"""
        test_prompt = "Respond with 'Connection successful' if you receive this."
        
        worker = GPTWorkerRunnable(
            prompt=test_prompt,
            model="gpt-3.5-turbo",
            max_tokens=50,
            temperature=0
        )
        
        worker.signals.result.connect(callback)
        worker.signals.error.connect(self.handle_api_error)
        
        self.thread_pool.start(worker)
    
    def handle_api_error(self, error_msg: str):
        """Handle API errors"""
        self.emit_error(f"API Error: {error_msg}")
```

## Service Layer Extractions

### TBLTService (tblt_service.py)
**Integration with tblt_scenarios.py**

```python
# Integrate existing TBLT functionality into service
class TBLTService(BaseService):
    def __init__(self):
        super().__init__()
        self.task_generator = TBLTTaskGenerator()
        self.spaced_repetition = SpacedRepetitionTracker()
        self.feedback_engine = None
    
    def generate_tblt_exercise(self, context_type: str, difficulty_level: str):
        """Generate TBLT-based exercise"""
        # Use existing TBLTTaskGenerator
        scenario = self.task_generator.generate_scenario(context_type)
        exercise = self.task_generator.create_exercise_from_scenario(
            scenario, difficulty_level
        )
        
        return exercise
    
    def get_pedagogical_feedback(self, response_data: dict):
        """Get pedagogical feedback for response"""
        # Use existing feedback system
        return get_pedagogical_feedback(
            response_data['user_answer'],
            response_data['correct_answer'],
            response_data['context']
        )
```

This extraction guide provides specific mappings for transforming the 4,010-line monolith into a clean MVC architecture while preserving all functionality. Each extraction maintains the original logic while improving organization and testability.
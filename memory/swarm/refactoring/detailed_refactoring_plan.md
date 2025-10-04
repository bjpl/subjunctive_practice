# Detailed MVC Refactoring Implementation Plan
## Spanish Subjunctive Practice Application

### Current Monolithic Analysis (4,010 lines)

#### Major Classes and Components Identified

**SpanishSubjunctivePracticeGUI (Main Class - Lines 395-3976)**
- **UI Initialization**: Lines 518-1274 (756 lines)
- **Event Handlers**: Lines 1275-2164 (889 lines)  
- **Exercise Logic**: Lines 2165-3332 (1,167 lines)
- **API Integration**: Lines 2983-3088 (105 lines)
- **Session Management**: Lines 3184-3294 (110 lines)
- **Statistics and Analytics**: Lines 3329-3539 (210 lines)
- **Accessibility Features**: Lines 3786-3910 (124 lines)

**Support Classes (Lines 194-394)**
- WorkerSignals (Lines 216-252)
- GPTWorkerRunnable (Lines 253-394)

#### External Dependencies Analysis
- **tblt_scenarios.py**: TBLT learning methodology implementation
- **conjugation_reference.py**: Grammar rules and conjugation patterns  
- **session_manager.py**: Session persistence and management
- **learning_analytics.py**: Progress tracking and analytics
- **src/**: 80+ supporting modules for UI, accessibility, and enhancements

### Detailed MVC Mapping

#### Model Layer Decomposition

**1. UserModel (from lines 432-444, 3786-3859)**
```python
class UserModel:
    # From: self.dark_mode, accessibility settings, preferences
    - user_preferences: dict
    - accessibility_settings: dict
    - theme_preferences: str
    - learning_goals: dict
    
    # Methods extracted from:
    # - toggleTheme() (lines 2058-2164)
    # - _initialize_enhanced_accessibility() (lines 3786-3819)
```

**2. SessionModel (from lines 416-431, 3184-3294)**
```python
class SessionModel:
    # From: self.responses, self.session_stats
    - current_session: dict
    - session_history: list
    - exercises_completed: int
    - correct_count: int
    
    # Methods extracted from:
    # - saveProgress() (lines 3184-3194)
    # - loadProgress() (lines 3195-3217) 
    # - resetProgress() (lines 3218-3241)
    # - exportSession() (lines 3294-3328)
```

**3. ExerciseModel (from lines 417-419, 2595-2796)**
```python
class ExerciseModel:
    # From: self.exercises, self.current_exercise
    - exercises: list
    - current_exercise_index: int
    - exercise_queue: list
    - exercise_state: dict
    
    # Methods extracted from:
    # - generateNewExercise() (lines 2595-2660)
    # - generateTBLTExercises() (lines 2661-2689)
    # - generateContrastExercises() (lines 2690-2716)
```

**4. ProgressModel (from learning_analytics.py integration)**
```python
class ProgressModel:
    # From: self.session_stats, streak tracking
    - streak_data: dict
    - error_patterns: dict
    - difficulty_progression: list
    - performance_metrics: dict
    
    # Methods extracted from:
    # - updateStats() (lines 2205-2262)
    # - check_daily_streak() (lines 2049-2057)
    # - showDetailedStats() (lines 3329-3358)
```

#### View Layer Decomposition

**1. MainWindow (from lines 518-614, 3921-3951)**
```python
class MainWindow(QMainWindow):
    # From: initUI() main window setup
    - window_geometry: tuple
    - splitter_layout: QSplitter
    - column_proportions: tuple
    
    # Methods extracted from:
    # - showEvent() (lines 3921-3930)
    # - resizeEvent() (lines 3946-3950)
    # - closeEvent() (lines 3952-3976)
```

**2. SelectionPanel (from lines 665-826)**
```python
class SelectionPanel(QWidget):
    # From: trigger/tense/person selection UI
    - trigger_checkboxes: dict
    - tense_checkboxes: dict
    - person_checkboxes: dict
    - selection_counts: dict
    
    # Methods extracted from:
    # - createControlPanel() (lines 665-826)
    # - onSelectionChanged() (lines 2379-2419)
    # - select_all_tenses() (lines 2428-2433)
```

**3. ExercisePanel (from lines 827-984, 1093-1274)**  
```python
class ExercisePanel(QWidget):
    # From: exercise display and interaction UI
    - sentence_label: QLabel
    - translation_label: QLabel
    - answer_input: QLineEdit
    - multiple_choice_group: QButtonGroup
    
    # Methods extracted from:
    # - createPracticeArea() (lines 827-984)
    # - populateMultipleChoice() (lines 2848-2867)
    # - getCurrentInputWidget() (lines 2885-2898)
```

**4. StatsPanel (from lines 615-664)**
```python  
class StatsPanel(QWidget):
    # From: statistics and progress display
    - progress_bar: QProgressBar
    - stats_labels: dict
    - streak_display: QLabel
    
    # Methods extracted from:
    # - createStatsPanel() (lines 615-664)
    # - updateExerciseCounter() (lines 2192-2204)
    # - updateStats() (lines 2205-2262)
```

#### Controller Layer Decomposition

**1. ApplicationController (from main application flow)**
```python
class ApplicationController:
    # Main application orchestration
    - model_registry: dict
    - view_registry: dict
    - event_bus: EventBus
    
    # Methods extracted from:
    # - Application initialization (lines 3979-4010)
    # - Theme switching coordination
    # - Global error handling
```

**2. ExerciseController (from lines 2595-3088)**
```python
class ExerciseController:
    # Exercise workflow management
    - exercise_generator: ExerciseService
    - answer_validator: AnswerValidator
    - hint_generator: HintService
    
    # Methods extracted from:
    # - generateNewExercise() (lines 2595-2660)
    # - submitAnswer() (lines 2899-2982)
    # - provideHint() (lines 3035-3068)
    # - nextExercise() (lines 3088-3111)
    # - prevExercise() (lines 3112-3135)
```

**3. SelectionController (from lines 2379-2501)**
```python
class SelectionController:
    # Selection state management
    - selection_validator: SelectionValidator
    - preset_manager: PresetManager
    
    # Methods extracted from:
    # - onSelectionChanged() (lines 2379-2419)
    # - autoGenerateIfReady() (lines 2420-2427)
    # - getSelectionSummary() (lines 2342-2378)
```

**4. ApiController (from lines 253-394, 2983-3088)**
```python
class ApiController:
    # External API management
    - openai_client: OpenAI
    - request_queue: Queue
    - rate_limiter: RateLimiter
    
    # Methods extracted from:
    # - GPTWorkerRunnable class (lines 253-394)
    # - generateGPTExplanationAsync() (lines 2983-3005)
    # - testAPIConnection() (lines 3673-3785)
```

### Service Layer Architecture

**1. TBLTService (integrating tblt_scenarios.py)**
```python
class TBLTService:
    # Task-based learning methodology
    - scenario_generator: ScenarioGenerator
    - context_builder: ContextBuilder
    - pedagogical_feedback: FeedbackEngine
```

**2. ConjugationService (integrating conjugation_reference.py)**
```python
class ConjugationService:
    # Grammar rule engine
    - conjugation_patterns: dict
    - stem_changes: dict
    - sequence_of_tenses: dict
```

**3. AnalyticsService (integrating learning_analytics.py)**
```python
class AnalyticsService:
    # Learning analytics and tracking
    - streak_tracker: StreakTracker
    - error_analyzer: ErrorAnalyzer
    - difficulty_adapter: AdaptiveDifficulty
```

### Migration Implementation Strategy

#### Phase 1: Foundation (Week 1-2)
**Extract Base Infrastructure**
```python
# 1. Create base classes
src/base/
├── base_model.py       # Common model functionality
├── base_view.py        # Common view patterns  
├── base_controller.py  # Controller interface
└── base_service.py     # Service patterns

# 2. Set up event system
src/events/
├── event_bus.py        # Central event coordination
├── model_events.py     # Model state change events
├── view_events.py      # UI interaction events
└── controller_events.py # Application flow events

# 3. Create dependency injection
src/di/
├── container.py        # DI container
├── providers.py        # Service providers
└── decorators.py       # DI decorators
```

#### Phase 2: Model Layer (Week 3-4)
**Extract Data Models**
```python
# Extract from lines 416-444, session management sections
class UserModel(BaseModel):
    def __init__(self):
        self.preferences = {}
        self.accessibility_settings = {}
        # ... extracted from main.py lines 432-444

class SessionModel(BaseModel): 
    def __init__(self):
        self.current_session = {}
        self.responses = []
        # ... extracted from main.py lines 416-431

class ExerciseModel(BaseModel):
    def __init__(self):
        self.exercises = []
        self.current_exercise = 0
        # ... extracted from main.py lines 417-419
```

#### Phase 3: View Layer (Week 5-6)
**Extract UI Components**
```python  
# Extract from lines 518-1274
class MainWindow(BaseView):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        # ... extracted from initUI() lines 518-614

class SelectionPanel(BaseView):
    def __init__(self):
        super().__init__()
        self.create_controls()
        # ... extracted from lines 665-826
```

#### Phase 4: Controller Layer (Week 7-8)  
**Extract Application Logic**
```python
# Extract from exercise management sections
class ExerciseController(BaseController):
    def __init__(self, exercise_model, exercise_view):
        self.model = exercise_model
        self.view = exercise_view
        # ... extracted from lines 2595-3088
```

#### Phase 5: Service Layer (Week 9-10)
**Extract Business Services**
```python
class TBLTService(BaseService):
    def __init__(self):
        self.scenario_generator = TBLTTaskGenerator()
        # ... integrate tblt_scenarios.py
```

#### Phase 6: Integration (Week 11-12)
**Wire Everything Together**
```python
# New slim main.py
def main():
    app = QApplication(sys.argv)
    
    # Initialize DI container
    container = DIContainer()
    container.register_services()
    
    # Create application
    app_controller = container.get(ApplicationController)
    app_controller.initialize()
    
    sys.exit(app.exec_())
```

### Testing Strategy

#### Unit Tests (90% coverage target)
```python
# Model tests
tests/models/
├── test_user_model.py
├── test_session_model.py
├── test_exercise_model.py
└── test_progress_model.py

# View tests (UI component testing)
tests/views/
├── test_main_window.py
├── test_selection_panel.py
└── test_exercise_panel.py

# Controller tests (business logic)
tests/controllers/
├── test_application_controller.py
├── test_exercise_controller.py
└── test_api_controller.py

# Service tests
tests/services/
├── test_tblt_service.py
├── test_conjugation_service.py
└── test_analytics_service.py
```

#### Integration Tests
```python
tests/integration/
├── test_exercise_workflow.py     # End-to-end exercise flow
├── test_session_persistence.py   # Save/load functionality
├── test_api_integration.py       # OpenAI API integration
└── test_accessibility_flow.py    # Accessibility features
```

### Risk Mitigation Strategies

#### Technical Risks
1. **Performance Regression**
   - Profile critical paths before refactoring
   - Benchmark after each phase
   - Maintain performance within 10% of baseline

2. **Breaking Changes**
   - Implement feature flags for gradual migration
   - Maintain backward compatibility during transition
   - Create comprehensive regression test suite

3. **Complex Dependencies**
   - Map all dependencies before extraction
   - Use dependency injection for loose coupling
   - Mock external dependencies in tests

#### Process Risks
1. **Scope Creep**
   - Stick to refactoring-only changes
   - Document any necessary improvements separately
   - Get approval for scope changes

2. **Timeline Pressure**
   - Implement in small, deliverable increments
   - Validate each phase independently
   - Maintain working application throughout

### Success Metrics

#### Code Quality Improvements
- **File Size**: No file > 500 lines (current: 4,010 lines)
- **Complexity**: Cyclomatic complexity < 10 per method
- **Coupling**: Reduce inter-component dependencies by 60%
- **Cohesion**: Increase intra-component cohesion by 40%

#### Architecture Quality
- **Separation of Concerns**: Clear MVC boundaries
- **Testability**: 90% unit test coverage achievable
- **Maintainability**: New features require changes in single layer
- **Extensibility**: New UI themes addable without logic changes

#### Functional Preservation
- **Feature Parity**: 100% feature preservation
- **Performance**: Within 10% of current performance
- **UI/UX**: Identical user experience
- **Data Migration**: Seamless user data preservation

This detailed plan provides a comprehensive roadmap for transforming the monolithic Spanish Subjunctive Practice application into a clean, maintainable MVC architecture while preserving all existing functionality and quality attributes.
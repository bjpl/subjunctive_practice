# Spanish Subjunctive Learning Core Modules Documentation

## Overview

This documentation covers the clean JavaScript modules extracted from the PyQt Spanish subjunctive learning application. The core system is designed to be framework-agnostic and can be integrated into web applications, Node.js applications, or any JavaScript environment.

## Architecture

The core system consists of five main modules:

```
src/core/
├── index.js           # Main orchestrating class and exports
├── conjugation.js     # Conjugation rules and verb processing  
├── exercises.js       # TBLT scenarios and exercise generation
├── progression.js     # Spaced repetition and adaptive difficulty
├── analytics.js       # Error analysis and performance tracking
└── session.js         # Session management and review queues
```

## Module Details

### 1. Conjugation Module (`conjugation.js`)

**Purpose**: Handles Spanish subjunctive conjugation rules, patterns, and validation.

**Key Classes**:
- `ConjugationEngine`: Main conjugation processor
- `ConjugationUtils`: Utility functions for verb analysis

**Key Constants**:
- `SUBJUNCTIVE_ENDINGS`: Regular conjugation patterns
- `COMMON_IRREGULAR_VERBS`: Irregular verb conjugations  
- `SUBJUNCTIVE_TRIGGERS`: Words/phrases that trigger subjunctive
- `STEM_CHANGING_PATTERNS`: Stem-changing verb patterns

**Example Usage**:
```javascript
import { ConjugationEngine } from './src/core/conjugation.js';

const engine = new ConjugationEngine();

// Conjugate a verb
const result = engine.conjugateRegularVerb('hablar', 'Present Subjunctive', 'yo');
console.log(result); // "hable"

// Validate a conjugation
const validation = engine.validateConjugation('hablar', 'Present Subjunctive', 'yo', 'hable');
console.log(validation.isCorrect); // true

// Get full conjugation table
const table = engine.getConjugationTable('ser', 'Present Subjunctive');
console.log(table); // { yo: 'sea', tú: 'seas', ... }
```

### 2. Exercise Generation Module (`exercises.js`)

**Purpose**: Generates TBLT (Task-Based Language Teaching) exercises and scenarios.

**Key Classes**:
- `TBLTTaskGenerator`: Creates communicative language tasks

**Key Constants**:
- `TBLT_SCENARIOS`: Real-world communicative scenarios
- `EXERCISE_TYPES`: Available exercise types
- `PEDAGOGICAL_FEEDBACK`: Feedback templates by level

**Example Usage**:
```javascript
import { TBLTTaskGenerator, EXERCISE_TYPES } from './src/core/exercises.js';

const generator = new TBLTTaskGenerator();

// Generate a conjugation exercise
const exercise = generator.generateConjugationExercise({
  verb: 'querer',
  tense: 'Present Subjunctive',
  person: 'yo'
});

// Generate a TBLT scenario
const scenario = generator.generateScenarioTask('Intermediate');

// Generate multiple choice
const multipleChoice = generator.generateMultipleChoiceExercise();

// Validate an answer
const validation = generator.validateExerciseAnswer(exercise, 'quiera');
```

### 3. Learning Progression Module (`progression.js`)

**Purpose**: Implements spaced repetition algorithms and adaptive difficulty adjustment.

**Key Classes**:
- `LearningProgressionManager`: Orchestrates all progression systems
- `SpacedRepetitionManager`: SM-2 algorithm implementation
- `AdaptiveDifficultyManager`: Dynamic difficulty adjustment
- `StreakTracker`: Practice streak motivation
- `AchievementManager`: Achievement system

**Example Usage**:
```javascript
import { LearningProgressionManager } from './src/core/progression.js';

const progression = new LearningProgressionManager();

// Record exercise completion
const result = progression.recordExerciseCompletion(
  exercise,     // exercise object
  true,         // correct answer
  5000,         // response time in ms
  'quiera'      // user answer
);

console.log(result.difficulty.adjusted); // true if difficulty changed
console.log(result.achievements);        // any new achievements earned
console.log(result.streak);             // streak information

// Get items due for review
const reviewItems = progression.getReviewItems();
```

### 4. Analytics Module (`analytics.js`)

**Purpose**: Analyzes learning patterns, errors, and provides intelligent feedback.

**Key Classes**:
- `ErrorAnalyzer`: Intelligent error categorization and analysis
- `PerformanceAnalyzer`: Learning trend analysis

**Key Constants**:
- `ERROR_CATEGORIES`: Types of errors that can be detected
- `LEARNING_PATTERNS`: User learning pattern classifications

**Example Usage**:
```javascript
import { ErrorAnalyzer, PerformanceAnalyzer } from './src/core/analytics.js';

const errorAnalyzer = new ErrorAnalyzer();
const performanceAnalyzer = new PerformanceAnalyzer();

// Analyze an error
const analysis = errorAnalyzer.analyzeError(
  'hablo',           // user's incorrect answer
  'hable',           // correct answer  
  {                  // context
    verb: 'hablar',
    tense: 'Present Subjunctive', 
    person: 'yo',
    trigger: 'quiero que'
  }
);

console.log(analysis.errorTypes);        // ['mood_confusion']
console.log(analysis.targetedSuggestion); // specific help

// Record session performance
performanceAnalyzer.recordSession({
  duration: 900000,      // 15 minutes
  exercisesCompleted: 12,
  correctAnswers: 10,
  accuracy: 83.3
});

// Get performance trends
const trends = performanceAnalyzer.getPerformanceTrends(30); // last 30 days
console.log(trends.trend); // 'improving', 'declining', or 'stable'
```

### 5. Session Management Module (`session.js`)

**Purpose**: Tracks learning sessions, manages review queues, and persists progress.

**Key Classes**:
- `SessionManager`: Session tracking and statistics
- `ReviewQueue`: Priority-based review queue management

**Example Usage**:
```javascript
import { SessionManager, ReviewQueue } from './src/core/session.js';

const sessionManager = new SessionManager();
const reviewQueue = new ReviewQueue();

// Add exercise result to session
sessionManager.addExerciseResult(
  exercise,      // exercise object
  'hable',       // user answer
  true,          // correct
  3000,          // response time
  null           // error analysis
);

// Get session statistics
const stats = sessionManager.getStatistics();
console.log(`Accuracy: ${stats.accuracy}%`);
console.log(`Items to review: ${stats.itemsToReview}`);

// Get review items
const reviewItems = sessionManager.getReviewItems(5);

// Complete session
const completedSession = sessionManager.completeSession();
```

## Main Orchestrator (`index.js`)

The `SpanishSubjunctiveCore` class orchestrates all modules and provides a high-level API:

```javascript
import SpanishSubjunctiveCore from './src/core/index.js';

// Initialize the learning system
const core = new SpanishSubjunctiveCore({
  defaultDifficulty: 'Intermediate',
  enableSpacedRepetition: true,
  enableAdaptiveDifficulty: true,
  autoSave: true
});

// Generate an exercise
const exercise = core.generateExercise();

// Submit an answer and get comprehensive feedback
const result = core.submitAnswer(exercise, 'hable', 3000);
console.log(result.feedback.message);
console.log(result.validation.isCorrect);
console.log(result.progressionUpdate);

// Get learning dashboard
const dashboard = core.getDashboard();
console.log(dashboard.session.accuracy);
console.log(dashboard.streak);
console.log(dashboard.achievements);

// Save progress
const saveData = core.save();
localStorage.setItem('spanish-subjunctive-progress', JSON.stringify(saveData));

// Load progress
const loadedData = JSON.parse(localStorage.getItem('spanish-subjunctive-progress'));
core.load(loadedData);
```

## Integration Examples

### Web Application Integration

```javascript
// Initialize the core system
const core = new SpanishSubjunctiveCore({
  autoSave: true,
  defaultDifficulty: 'Beginner'
});

// Load saved progress
const savedData = localStorage.getItem('subjunctive-progress');
if (savedData) {
  core.load(JSON.parse(savedData));
}

// Generate and display exercise
function newExercise() {
  const exercise = core.generateExercise();
  displayExercise(exercise);
  
  // Set up answer submission
  document.getElementById('submit-btn').onclick = () => {
    const userAnswer = document.getElementById('answer-input').value;
    const startTime = Date.now();
    
    const result = core.submitAnswer(exercise, userAnswer, Date.now() - startTime);
    displayFeedback(result);
    
    // Auto-save progress
    localStorage.setItem('subjunctive-progress', JSON.stringify(core.save()));
  };
}

// Display dashboard
function showDashboard() {
  const dashboard = core.getDashboard();
  updateUI(dashboard);
}
```

### Node.js API Integration

```javascript
import express from 'express';
import SpanishSubjunctiveCore from './src/core/index.js';

const app = express();
const userSessions = new Map();

app.post('/api/exercise/generate', (req, res) => {
  const userId = req.user.id;
  const core = getUserCore(userId);
  
  const exercise = core.generateExercise(req.body.options);
  res.json(exercise);
});

app.post('/api/exercise/submit', (req, res) => {
  const userId = req.user.id;
  const core = getUserCore(userId);
  
  const { exercise, userAnswer, responseTime } = req.body;
  const result = core.submitAnswer(exercise, userAnswer, responseTime);
  
  // Save progress to database
  saveUserProgress(userId, core.save());
  
  res.json(result);
});

app.get('/api/dashboard', (req, res) => {
  const userId = req.user.id;
  const core = getUserCore(userId);
  
  res.json(core.getDashboard());
});

function getUserCore(userId) {
  if (!userSessions.has(userId)) {
    const core = new SpanishSubjunctiveCore();
    const savedData = loadUserProgress(userId);
    if (savedData) {
      core.load(savedData);
    }
    userSessions.set(userId, core);
  }
  return userSessions.get(userId);
}
```

## Testing

Each module includes comprehensive error handling and can be tested independently:

```javascript
// Test conjugation engine
const engine = new ConjugationEngine();
console.assert(engine.conjugateRegularVerb('hablar', 'Present Subjunctive', 'yo') === 'hable');

// Test exercise generation
const generator = new TBLTTaskGenerator();
const exercise = generator.generateConjugationExercise();
console.assert(exercise.type === 'conjugation');

// Test progression system
const progression = new LearningProgressionManager();
const result = progression.recordExerciseCompletion({}, true, 1000, 'test');
console.assert(typeof result === 'object');
```

## Performance Considerations

- All modules are designed to be lightweight and fast
- Spaced repetition calculations are optimized for real-time use
- Error analysis uses heuristic patterns for quick categorization
- Session data can be exported/imported for persistence
- Memory usage is kept minimal with garbage collection-friendly patterns

## Extensibility

The modular design allows for easy extension:

- Add new exercise types by extending `TBLTTaskGenerator`
- Add new error analysis patterns in `ErrorAnalyzer`
- Customize difficulty parameters in `AdaptiveDifficultyManager`
- Add new achievement criteria in `AchievementManager`
- Extend conjugation rules for additional verb types

## Browser Compatibility

The core modules use modern JavaScript features but are compatible with:
- ES2018+ (async/await, object spread)
- Modern browsers (Chrome 60+, Firefox 55+, Safari 12+)
- Node.js 12+

For older browser support, transpile with Babel.

## Dependencies

The core modules have **no external dependencies** - they are pure JavaScript implementations that can run in any JavaScript environment.
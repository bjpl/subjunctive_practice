# React Frontend Architecture Design
## Spanish Subjunctive Practice App

*System Architecture Designer: Clean, Educational React Frontend*

---

## 📋 Architecture Decision Record (ADR)

### Context
Building a React frontend for Spanish Subjunctive Practice app that connects to a streamlined FastAPI backend (reduced from 70k to 2k lines). Need educational-focused, accessible, mobile-responsive architecture with minimal complexity.

### Decision
Adopt a **component-based, educational-first architecture** with:
- Maximum 8 core components
- Context API for state management
- Educational UX patterns
- WCAG 2.1 AA accessibility compliance

### Quality Attributes
- **Simplicity**: Focus on learning, not complexity
- **Performance**: Fast loading, responsive interactions
- **Accessibility**: WCAG 2.1 AA compliant
- **Maintainability**: Clean, documented code
- **Educational Effectiveness**: Learning-first design

---

## 🏗️ Component Hierarchy Diagram

```
App (Root)
├── Header
│   ├── Navigation
│   └── ProgressBar
├── Router
│   ├── PracticeScreen
│   │   ├── ExerciseCard
│   │   ├── AnswerForm
│   │   └── FeedbackPanel
│   ├── ProgressDashboard
│   │   ├── StatsWidget
│   │   └── StreakTracker
│   ├── ReferenceGuide
│   │   ├── ConjugationTable
│   │   └── TriggersList
│   └── SessionSetup
└── Footer
```

---

## 🧩 Core Components (8 Total)

### 1. **App** (Root Container)
**Responsibility**: Application shell, global state provision, routing
**Props**: None (root level)
**State**: Global app state via Context

```jsx
// Primary concerns:
- Session management
- Error boundaries  
- Theme provider
- Accessibility announcements
```

### 2. **ExerciseCard** (Practice Component)
**Responsibility**: Display contextualized Spanish exercises
**Props**: `exercise, onSubmit, loading`
**State**: User input, submission state

```jsx
// Key features:
- Context sentence display
- Subjunctive trigger highlighting
- Hint system for beginners
- Accessible form controls
```

### 3. **AnswerForm** (Input Component) 
**Responsibility**: Capture and validate user answers
**Props**: `onSubmit, disabled, placeholder`
**State**: Input value, validation

```jsx
// Educational features:
- Real-time input validation
- Visual feedback for errors
- Keyboard shortcuts (Enter to submit)
- Voice input support (future)
```

### 4. **FeedbackPanel** (Learning Component)
**Responsibility**: Provide immediate pedagogical feedback
**Props**: `feedback, correct, explanation, nextAction`
**State**: Display animation

```jsx
// Learning elements:
- Immediate correctness feedback
- Explanatory grammar notes
- Encouraging messaging
- Progress celebration
```

### 5. **ProgressDashboard** (Analytics Component)
**Responsibility**: Show learning progress and statistics
**Props**: `sessionData, achievements`
**State**: Chart animations

```jsx
// Motivational features:
- Daily streak tracking
- Mastery level indicators
- Error pattern analysis
- Goal progress visualization
```

### 6. **ReferenceGuide** (Educational Component)
**Responsibility**: Grammar reference and learning aids
**Props**: `currentTopic, searchQuery`
**State**: Active section, search results

```jsx
// Reference materials:
- Subjunctive triggers list
- Conjugation tables
- Grammar rules
- Usage examples
```

### 7. **Navigation** (UI Component)
**Responsibility**: App navigation and accessibility
**Props**: `currentPath, sessionActive`
**State**: Menu open/closed

```jsx
// Accessibility features:
- Skip links for screen readers
- Keyboard navigation
- Focus management
- High contrast support
```

### 8. **SessionSetup** (Configuration Component)
**Responsibility**: Configure practice sessions
**Props**: `onStart, savedPreferences`
**State**: Difficulty, category, goal settings

```jsx
// Customization options:
- Difficulty selection (1-5)
- Topic categories
- Session length goals
- Accessibility preferences
```

---

## 📊 State Management Strategy

### Context API Architecture

```jsx
// AppContext.js - Single source of truth
const AppContext = createContext({
  // Session Management  
  session: null,
  createSession: () => {},
  endSession: () => {},
  
  // Exercise State
  currentExercise: null,
  exerciseHistory: [],
  submitAnswer: () => {},
  
  // Progress Tracking
  progress: {},
  achievements: [],
  
  // UI State
  loading: false,
  error: null,
  theme: 'light'
});
```

### State Structure
```typescript
interface AppState {
  // User Session
  session: {
    id: string;
    startTime: Date;
    preferences: UserPreferences;
    streak: number;
  } | null;
  
  // Current Exercise
  currentExercise: {
    taskId: string;
    context: string;
    prompt: string;
    trigger: string;
    category: string;
    difficulty: number;
    hint?: string;
  } | null;
  
  // Progress Data
  progress: {
    totalCorrect: number;
    totalAttempts: number;
    currentStreak: number;
    masteryLevels: Record<string, number>;
  };
  
  // UI State
  ui: {
    loading: boolean;
    error: string | null;
    theme: 'light' | 'dark';
    highContrast: boolean;
  };
}
```

---

## 🛣️ Routing Structure

### Educational Flow Design
```jsx
// Routes focused on learning progression
const routes = [
  {
    path: '/',
    component: SessionSetup,
    title: 'Start Learning'
  },
  {
    path: '/practice',
    component: PracticeScreen,
    title: 'Practice Session',
    protected: true // Requires active session
  },
  {
    path: '/progress', 
    component: ProgressDashboard,
    title: 'Your Progress'
  },
  {
    path: '/reference',
    component: ReferenceGuide,
    title: 'Grammar Reference'
  },
  {
    path: '/accessibility',
    component: AccessibilitySettings,
    title: 'Accessibility Options'
  }
];
```

### Route Protection
- `/practice` requires active session
- Session timeout redirects to setup
- Progress persists across sessions
- Deep linking to specific exercises

---

## 🔌 API Integration Layer

### Service Architecture
```jsx
// api/spanishApi.js - Centralized API layer
class SpanishApi {
  constructor(baseUrl = 'http://localhost:8000') {
    this.baseUrl = baseUrl;
    this.session = null;
  }
  
  // Session Management
  async createSession(userId = null) {
    const response = await this.post('/api/session/create', { userId });
    this.session = response.data;
    return this.session;
  }
  
  // Exercise Generation  
  async generatePractice(difficulty = 2, category = null) {
    return this.get('/api/practice/generate', {
      difficulty,
      category,
      sessionId: this.session?.sessionId
    });
  }
  
  // Answer Submission
  async submitAnswer(taskId, answer, responseTime) {
    return this.post('/api/practice/submit', {
      taskId,
      sessionId: this.session.sessionId,
      answer,
      responseTime
    });
  }
  
  // Progress Tracking
  async getProgress() {
    return this.get(`/api/progress/${this.session.sessionId}`);
  }
  
  // Reference Data
  async getConjugation(verb, tense = 'present_subjunctive') {
    return this.get(`/api/conjugate/${verb}`, { tense });
  }
  
  // Error Handling with Retry Logic
  async request(method, url, data = null) {
    try {
      const response = await fetch(`${this.baseUrl}${url}`, {
        method,
        headers: {
          'Content-Type': 'application/json'
        },
        body: data ? JSON.stringify(data) : null
      });
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      // Educational error messages
      if (error.name === 'TypeError') {
        throw new Error('Connection problem. Check your internet and try again.');
      }
      throw error;
    }
  }
}

export default new SpanishApi();
```

### Error Handling Strategy
- Network errors: Friendly educational messages
- Validation errors: Inline form guidance  
- Server errors: Graceful degradation
- Offline support: Cached content access

---

## 📁 File Structure Recommendation

```
frontend/
├── public/
│   ├── index.html
│   ├── manifest.json          # PWA support
│   └── icons/                 # App icons
├── src/
│   ├── components/           # Core UI components
│   │   ├── common/
│   │   │   ├── Header.jsx
│   │   │   ├── Navigation.jsx
│   │   │   └── Footer.jsx
│   │   ├── practice/
│   │   │   ├── ExerciseCard.jsx
│   │   │   ├── AnswerForm.jsx
│   │   │   └── FeedbackPanel.jsx
│   │   ├── progress/
│   │   │   ├── ProgressDashboard.jsx
│   │   │   └── StatsWidget.jsx
│   │   └── reference/
│   │       ├── ReferenceGuide.jsx
│   │       └── ConjugationTable.jsx
│   ├── context/             # State management
│   │   ├── AppContext.jsx
│   │   └── useAppState.js
│   ├── services/            # API integration
│   │   ├── spanishApi.js
│   │   └── errorHandler.js
│   ├── hooks/               # Custom React hooks
│   │   ├── useExercise.js
│   │   ├── useProgress.js
│   │   └── useAccessibility.js
│   ├── styles/              # CSS modules
│   │   ├── globals.css
│   │   ├── themes.css
│   │   └── accessibility.css
│   ├── utils/               # Helper functions
│   │   ├── constants.js
│   │   └── validation.js
│   └── App.jsx
├── package.json
└── README.md
```

---

## ♿ Accessibility Implementation (WCAG 2.1 AA)

### Accessibility Requirements

#### **Level A Compliance**
- ✅ Alt text for all images
- ✅ Keyboard navigation support  
- ✅ Focus indicators
- ✅ Screen reader compatibility

#### **Level AA Compliance**
- ✅ Color contrast ratio ≥ 4.5:1
- ✅ Text resize up to 200% without loss of functionality
- ✅ No seizure-inducing content
- ✅ Page titles and headings

### Implementation Strategy
```jsx
// useAccessibility.js - Custom hook
export const useAccessibility = () => {
  const [preferences, setPreferences] = useState({
    highContrast: false,
    reduceMotion: false,
    fontSize: 'medium',
    screenReader: false
  });
  
  // Apply preferences to CSS custom properties
  useEffect(() => {
    document.documentElement.style.setProperty(
      '--font-scale', 
      preferences.fontSize === 'large' ? '1.25' : '1'
    );
    
    document.documentElement.classList.toggle(
      'high-contrast', 
      preferences.highContrast
    );
  }, [preferences]);
  
  return { preferences, setPreferences };
};
```

### Accessibility Features
- **Screen Reader Support**: Semantic HTML, ARIA labels
- **Keyboard Navigation**: Tab order, keyboard shortcuts
- **High Contrast Mode**: Alternative color schemes
- **Text Scaling**: Responsive typography
- **Motion Reduction**: Respects prefers-reduced-motion

---

## 📱 Mobile-Responsive Design

### Responsive Breakpoints
```css
/* Mobile-first CSS approach */
:root {
  --mobile: 320px;
  --tablet: 768px; 
  --desktop: 1024px;
  --large: 1200px;
}

/* Component-specific responsive design */
.exercise-card {
  padding: 1rem;
  margin: 0.5rem;
}

@media (min-width: 768px) {
  .exercise-card {
    padding: 2rem;
    margin: 1rem;
    max-width: 600px;
  }
}
```

### Touch-Friendly Design
- Minimum 44px touch targets
- Swipe gestures for navigation
- Large, accessible buttons
- Optimized keyboard for text input

---

## ⚡ Performance Considerations

### Optimization Strategy
```jsx
// Code splitting by route
const PracticeScreen = lazy(() => import('./components/PracticeScreen'));
const ProgressDashboard = lazy(() => import('./components/ProgressDashboard'));

// Memoization for expensive components
const ExerciseCard = memo(({ exercise, onSubmit }) => {
  // Component implementation
});

// Virtual scrolling for large lists
const VirtualizedConjugationTable = ({ verbs }) => {
  // Implementation with react-window
};
```

### Performance Targets
- First Contentful Paint: < 2 seconds
- Time to Interactive: < 3 seconds  
- Bundle size: < 200KB gzipped
- Accessibility performance: 100/100 Lighthouse score

---

## 🔒 Educational UX Patterns

### Learning-First Design Principles

#### **Immediate Feedback**
- Visual confirmation of correct answers
- Gentle correction for mistakes
- Explanatory grammar notes
- Encouraging progress messages

#### **Progressive Disclosure**
- Start with simple exercises
- Gradually introduce complexity
- Hide advanced features initially
- Contextual help when needed

#### **Motivation Systems**
- Daily streak tracking
- Achievement badges
- Progress celebrations
- Personal goal setting

#### **Error Recovery**
- Friendly error messages
- Suggestion for improvement
- Option to try again
- Learning from mistakes emphasis

---

## 🚀 Implementation Roadmap

### Phase 1: Core Architecture (Week 1-2)
- [ ] Set up React app with TypeScript
- [ ] Implement Context API state management
- [ ] Create basic component structure
- [ ] Set up API integration layer

### Phase 2: Practice Flow (Week 2-3)
- [ ] Build ExerciseCard component
- [ ] Implement AnswerForm with validation
- [ ] Create FeedbackPanel
- [ ] Add session management

### Phase 3: Progress & Reference (Week 3-4)
- [ ] Build ProgressDashboard
- [ ] Create ReferenceGuide
- [ ] Implement accessibility features
- [ ] Add mobile responsiveness

### Phase 4: Polish & Testing (Week 4-5)
- [ ] Comprehensive testing suite
- [ ] Accessibility audit
- [ ] Performance optimization
- [ ] User experience testing

---

## 📊 Success Metrics

### Educational Effectiveness
- **Completion Rate**: >80% of started sessions
- **Learning Retention**: Progress maintained across sessions  
- **Error Reduction**: Improvement in accuracy over time
- **Engagement**: Average session length >10 minutes

### Technical Performance
- **Accessibility**: WCAG 2.1 AA compliance
- **Performance**: Lighthouse score >90
- **Responsiveness**: Works on all device sizes
- **Reliability**: <1% error rate

### User Experience
- **Ease of Use**: Intuitive navigation
- **Visual Design**: Clean, educational aesthetics
- **Feedback Quality**: Clear, helpful messages
- **Motivational Elements**: Visible progress tracking

---

This architecture balances educational effectiveness with technical simplicity, ensuring that learners can focus on mastering Spanish subjunctive without fighting the interface. The component-based approach allows for easy maintenance and future enhancements while maintaining the core principle of "learning first, technology second."
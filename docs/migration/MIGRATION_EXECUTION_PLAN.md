# PyQt to Web Migration Execution Plan
## Spanish Subjunctive Practice Application

**Target Timeline:** 5 weeks  
**Migration Approach:** Incremental with parallel development  
**Risk Level:** Medium (well-structured existing codebase)

---

## Executive Summary

This plan outlines the systematic migration of the Spanish Subjunctive Practice application from PyQt5/6 to a modern web-based architecture using React. The existing codebase shows excellent separation of concerns with distinct business logic, UI components, and data management layers, making it well-suited for web migration.

### Current Architecture Analysis

**Strengths:**
- Clean separation between UI (PyQt) and business logic
- Modular design with specialized components (session_manager.py, learning_analytics.py)
- Comprehensive accessibility features already implemented
- Advanced UI enhancements and responsive design considerations
- Robust data persistence and user progress tracking

**Key Components Identified:**
- **Core Logic:** `tblt_scenarios.py`, `conjugation_reference.py`, `session_manager.py`, `learning_analytics.py`
- **UI Layer:** `main.py` (SpanishSubjunctivePracticeGUI), `ui_enhancements.py`, accessibility components
- **Data Management:** JSON-based persistence, user progress tracking
- **Accessibility:** WCAG 2.1 AA compliant features with comprehensive screen reader support

---

# Phase 1: Core Logic Extraction (Week 1)

## 1.1 Business Logic Analysis and Extraction

### Day 1-2: Core Logic Mapping
**Priority:** HIGH | **Estimated Time:** 16 hours | **Risk:** LOW

**Tasks:**
- [ ] **Extract TBLT Task Generation Engine**
  - Convert `TBLTTaskGenerator` class to JavaScript/TypeScript
  - Port subjunctive scenarios and context generation
  - Migrate spaced repetition algorithms
  
- [ ] **Extract Conjugation Reference System**
  - Port `STEM_CHANGING_PATTERNS` and `SEQUENCE_OF_TENSES` data
  - Convert conjugation validation logic
  - Migrate pedagogical feedback system

- [ ] **Extract Learning Analytics Engine**
  - Port `StreakTracker`, `ErrorAnalyzer`, `AdaptiveDifficulty` classes
  - Convert statistical analysis algorithms
  - Migrate practice goal tracking

**Deliverables:**
```javascript
// src/core/
├── tblt-engine.js           // Task generation and scenarios
├── conjugation-engine.js    // Conjugation rules and validation
├── analytics-engine.js      // Learning analytics and tracking
├── session-manager.js       // Session and progress management
└── constants.js             // App constants and configurations
```

**Dependencies:**
- None (pure logic extraction)

**Testing Checkpoints:**
- [ ] Unit tests for each extracted module pass
- [ ] Logic parity validation with Python implementation
- [ ] Performance benchmarks meet requirements (< 100ms response time)

### Day 3: Data Model Standardization
**Priority:** HIGH | **Estimated Time:** 8 hours | **Risk:** LOW

**Tasks:**
- [ ] **Define TypeScript Interfaces**
  ```typescript
  interface Exercise {
    id: string;
    sentence: string;
    translation: string;
    context: string;
    correctAnswer: string;
    difficulty: 'beginner' | 'intermediate' | 'advanced';
  }
  
  interface UserProgress {
    totalExercises: number;
    correctAnswers: number;
    currentStreak: number;
    masteredConcepts: string[];
  }
  
  interface SessionData {
    startTime: string;
    exercises: Exercise[];
    responses: UserResponse[];
    analytics: SessionAnalytics;
  }
  ```

- [ ] **Create Data Migration Utilities**
  - JSON format converter (Python → Web)
  - Data validation schemas
  - Migration scripts for existing user data

### Day 4-5: Storage Layer Implementation
**Priority:** HIGH | **Estimated Time:** 16 hours | **Risk:** MEDIUM

**Tasks:**
- [ ] **Local Storage Implementation**
  - Browser localStorage for session data
  - IndexedDB for complex data (progress history)
  - Data compression for large datasets

- [ ] **Cloud Storage Integration (Optional)**
  - Firebase/Supabase integration
  - User authentication system
  - Cross-device synchronization

**Deliverables:**
```javascript
// src/storage/
├── local-storage.js         // Browser storage management
├── cloud-storage.js         // Optional cloud integration
├── data-migration.js        // Data format conversion
└── storage-manager.js       // Unified storage interface
```

**Risk Mitigation:**
- Implement fallback mechanisms for storage failures
- Add data validation at storage boundaries
- Create data backup/restore functionality

---

# Phase 2: Web Development Setup (Week 2)

## 2.1 React Application Foundation

### Day 1-2: Project Initialization
**Priority:** HIGH | **Estimated Time:** 16 hours | **Risk:** LOW

**Tasks:**
- [ ] **Create React App with TypeScript**
  ```bash
  npx create-react-app spanish-subjunctive-web --template typescript
  cd spanish-subjunctive-web
  npm install @types/react @types/react-dom
  ```

- [ ] **Configure Development Environment**
  ```json
  // package.json additions
  {
    "dependencies": {
      "react": "^18.2.0",
      "react-dom": "^18.2.0",
      "typescript": "^4.9.0",
      "styled-components": "^5.3.0",
      "react-query": "^3.39.0",
      "react-router-dom": "^6.8.0",
      "framer-motion": "^10.0.0"
    },
    "devDependencies": {
      "@testing-library/react": "^13.4.0",
      "@testing-library/jest-dom": "^5.16.0",
      "jest": "^27.5.0",
      "eslint": "^8.0.0",
      "prettier": "^2.8.0"
    }
  }
  ```

- [ ] **Setup Build Tools and Configuration**
  - ESLint configuration for React/TypeScript
  - Prettier code formatting
  - Jest testing framework setup
  - Webpack configuration customization

### Day 3: Component Architecture Planning
**Priority:** HIGH | **Estimated Time:** 8 hours | **Risk:** LOW

**Tasks:**
- [ ] **Design Component Hierarchy**
  ```
  App
  ├── Layout
  │   ├── Header
  │   ├── Navigation
  │   └── Footer
  ├── ExerciseView
  │   ├── ExerciseCard
  │   ├── AnswerInput
  │   ├── FeedbackPanel
  │   └── ProgressIndicator
  ├── SettingsView
  │   ├── AccessibilitySettings
  │   ├── DifficultySettings
  │   └── ThemeSettings
  └── StatisticsView
      ├── ProgressCharts
      ├── StreakDisplay
      └── ErrorAnalysis
  ```

- [ ] **Define Component Interfaces**
  ```typescript
  interface ExerciseCardProps {
    exercise: Exercise;
    onSubmit: (answer: string) => void;
    showTranslation: boolean;
  }
  
  interface ProgressIndicatorProps {
    current: number;
    total: number;
    accuracy: number;
    streak: number;
  }
  ```

### Day 4-5: Core Infrastructure
**Priority:** HIGH | **Estimated Time:** 16 hours | **Risk:** MEDIUM

**Tasks:**
- [ ] **State Management Setup**
  - React Context for global state
  - Custom hooks for data fetching
  - State persistence middleware

- [ ] **Routing Configuration**
  - React Router setup
  - Protected routes for authenticated users
  - Deep linking support for exercises

- [ ] **Theme System Implementation**
  - CSS-in-JS with styled-components
  - Dark/light theme support
  - Accessibility-compliant color schemes

**Deliverables:**
```typescript
// src/
├── components/           // React components
├── hooks/               // Custom React hooks  
├── context/             // React Context providers
├── styles/              // Theme and styling
├── utils/               // Utility functions
├── types/               // TypeScript definitions
└── __tests__/           // Test files
```

---

# Phase 3: Component Migration (Week 3-4)

## 3.1 PyQt Widget to React Component Mapping

### Week 3, Day 1-3: Core Exercise Components
**Priority:** HIGH | **Estimated Time:** 24 hours | **Risk:** MEDIUM

**Component Mapping:**

| PyQt Widget | React Component | Implementation Notes |
|-------------|-----------------|---------------------|
| `QLabel` (sentence display) | `ExerciseCard` | Card-based design with typography |
| `QLineEdit` (answer input) | `AnswerInput` | Controlled input with validation |
| `QPushButton` (submit/nav) | `Button` | Styled button with loading states |
| `QProgressBar` | `ProgressIndicator` | SVG-based progress visualization |
| `QTextEdit` (feedback) | `FeedbackPanel` | Rich text display with animations |
| `QCheckBox` (settings) | `Checkbox` | Accessible form controls |
| `QComboBox` (dropdowns) | `Select` | Custom dropdown with search |

**Tasks:**
- [ ] **ExerciseCard Component**
  ```typescript
  const ExerciseCard: React.FC<ExerciseCardProps> = ({
    exercise,
    showContext,
    showTranslation
  }) => {
    return (
      <Card>
        {showContext && <ContextBadge>{exercise.context}</ContextBadge>}
        <ExerciseSentence>{exercise.sentence}</ExerciseSentence>
        {showTranslation && (
          <Translation>{exercise.translation}</Translation>
        )}
      </Card>
    );
  };
  ```

- [ ] **AnswerInput Component with Validation**
  ```typescript
  const AnswerInput: React.FC<AnswerInputProps> = ({
    onSubmit,
    disabled,
    placeholder
  }) => {
    const [value, setValue] = useState('');
    const [validationState, setValidationState] = useState('neutral');
    
    return (
      <InputContainer>
        <StyledInput
          value={value}
          onChange={setValue}
          state={validationState}
          placeholder={placeholder}
          disabled={disabled}
        />
        <SubmitButton onClick={() => onSubmit(value)}>
          Submit
        </SubmitButton>
      </InputContainer>
    );
  };
  ```

- [ ] **ProgressIndicator Component**
  ```typescript
  const ProgressIndicator: React.FC<ProgressProps> = ({
    current,
    total,
    accuracy,
    streak
  }) => {
    const percentage = (current / total) * 100;
    
    return (
      <ProgressContainer>
        <ProgressBar>
          <ProgressFill width={percentage} />
        </ProgressBar>
        <StatsGrid>
          <Stat label="Exercise" value={`${current}/${total}`} />
          <Stat label="Accuracy" value={`${accuracy.toFixed(1)}%`} />
          <Stat label="Streak" value={`${streak} days`} />
        </StatsGrid>
      </ProgressContainer>
    );
  };
  ```

### Week 3, Day 4-5: Advanced UI Components
**Priority:** MEDIUM | **Estimated Time:** 16 hours | **Risk:** MEDIUM

**Tasks:**
- [ ] **Settings Panel Migration**
  - Convert accessibility settings from PyQt dialog to React modal
  - Implement theme switching functionality
  - Add keyboard shortcut configuration

- [ ] **Statistics Dashboard**
  - Port learning analytics visualizations
  - Convert QChart widgets to Chart.js/D3.js
  - Implement responsive data tables

- [ ] **Navigation System**
  - Convert PyQt menu system to React navigation
  - Implement breadcrumb navigation
  - Add keyboard navigation support

### Week 4, Day 1-3: Responsive Design Implementation
**Priority:** HIGH | **Estimated Time:** 24 hours | **Risk:** LOW

**Tasks:**
- [ ] **Mobile-First Responsive Layout**
  ```css
  /* Base mobile styles */
  .exercise-card {
    padding: 1rem;
    margin: 0.5rem;
  }
  
  /* Tablet styles */
  @media (min-width: 768px) {
    .exercise-card {
      padding: 1.5rem;
      margin: 1rem;
    }
  }
  
  /* Desktop styles */
  @media (min-width: 1024px) {
    .exercise-card {
      padding: 2rem;
      margin: 1.5rem;
      max-width: 800px;
    }
  }
  ```

- [ ] **Touch-Friendly Interface Design**
  - Minimum 44px touch targets
  - Gesture support for navigation
  - Haptic feedback for mobile devices

- [ ] **Progressive Web App Features**
  - Service worker for offline functionality
  - App manifest for native-like experience
  - Push notifications for practice reminders

### Week 4, Day 4-5: Accessibility Implementation
**Priority:** HIGH | **Estimated Time:** 16 hours | **Risk:** LOW

**Tasks:**
- [ ] **Port WCAG 2.1 AA Features**
  - Screen reader compatibility with ARIA labels
  - Keyboard navigation patterns
  - High contrast mode support
  - Font scaling and text spacing

- [ ] **Enhanced Web Accessibility**
  ```typescript
  const AccessibleButton: React.FC<ButtonProps> = ({
    children,
    onClick,
    disabled,
    ariaLabel
  }) => {
    return (
      <button
        onClick={onClick}
        disabled={disabled}
        aria-label={ariaLabel}
        role="button"
        tabIndex={disabled ? -1 : 0}
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            onClick();
          }
        }}
      >
        {children}
      </button>
    );
  };
  ```

- [ ] **Focus Management System**
  - Focus trap for modals
  - Skip links for main content
  - Logical tab order throughout application

**Deliverables:**
```typescript
// src/components/
├── ui/
│   ├── Button.tsx
│   ├── Input.tsx
│   ├── Card.tsx
│   ├── Modal.tsx
│   └── ProgressBar.tsx
├── exercise/
│   ├── ExerciseCard.tsx
│   ├── AnswerInput.tsx
│   ├── FeedbackPanel.tsx
│   └── NavigationControls.tsx
├── settings/
│   ├── AccessibilitySettings.tsx
│   ├── ThemeSelector.tsx
│   └── DifficultySettings.tsx
└── statistics/
    ├── ProgressCharts.tsx
    ├── StreakDisplay.tsx
    └── ErrorAnalytics.tsx
```

---

# Phase 4: Feature Parity and Enhancement (Week 5)

## 4.1 Core Feature Implementation

### Day 1-2: Exercise Generation and Management
**Priority:** HIGH | **Estimated Time:** 16 hours | **Risk:** MEDIUM

**Tasks:**
- [ ] **Exercise Flow Implementation**
  ```typescript
  const useExerciseFlow = () => {
    const [currentExercise, setCurrentExercise] = useState<Exercise | null>(null);
    const [userProgress, setUserProgress] = useState<UserProgress>();
    
    const generateNextExercise = useCallback(async () => {
      const exercise = await tblEngine.generateExercise({
        difficulty: userProgress.currentLevel,
        contexts: userProgress.selectedContexts,
        excludeRecent: true
      });
      setCurrentExercise(exercise);
    }, [userProgress]);
    
    const submitAnswer = useCallback(async (answer: string) => {
      const result = await conjugationEngine.validateAnswer(
        currentExercise,
        answer
      );
      
      await analyticsEngine.recordResponse(currentExercise, answer, result);
      return result;
    }, [currentExercise]);
    
    return { currentExercise, generateNextExercise, submitAnswer };
  };
  ```

- [ ] **Spaced Repetition Integration**
  - Port spaced repetition algorithms
  - Implement review queue management
  - Add difficulty adaptation based on performance

- [ ] **Context-Aware Exercise Generation**
  - Implement TBLT methodology
  - Context-driven scenario generation
  - Adaptive difficulty progression

### Day 3: Data Persistence and Synchronization
**Priority:** HIGH | **Estimated Time:** 8 hours | **Risk:** MEDIUM

**Tasks:**
- [ ] **Offline-First Data Strategy**
  ```typescript
  const useOfflineSync = () => {
    const [isOnline, setIsOnline] = useState(navigator.onLine);
    const [syncQueue, setSyncQueue] = useState<SyncItem[]>([]);
    
    useEffect(() => {
      const syncPendingData = async () => {
        if (isOnline && syncQueue.length > 0) {
          try {
            await cloudStorage.batchSync(syncQueue);
            setSyncQueue([]);
          } catch (error) {
            console.error('Sync failed:', error);
          }
        }
      };
      
      syncPendingData();
    }, [isOnline, syncQueue]);
    
    return { isOnline, queueForSync: setSyncQueue };
  };
  ```

- [ ] **Cross-Device Data Synchronization**
  - User account management
  - Progress synchronization across devices
  - Conflict resolution strategies

### Day 4: Advanced Features
**Priority:** MEDIUM | **Estimated Time:** 8 hours | **Risk:** LOW

**Tasks:**
- [ ] **Enhanced Learning Analytics**
  - Real-time progress visualization
  - Learning pattern analysis
  - Personalized recommendations

- [ ] **Gamification Elements**
  - Achievement system
  - Learning streaks and badges
  - Social sharing features

- [ ] **Advanced Accessibility Features**
  - Voice recognition for answers
  - Text-to-speech for exercises
  - High contrast and large text modes

### Day 5: Performance Optimization and Testing
**Priority:** HIGH | **Estimated Time:** 8 hours | **Risk:** LOW

**Tasks:**
- [ ] **Performance Optimization**
  ```typescript
  // Code splitting for better loading
  const ExerciseView = React.lazy(() => import('./components/ExerciseView'));
  const SettingsView = React.lazy(() => import('./components/SettingsView'));
  
  // Memoization for expensive calculations
  const exerciseResults = useMemo(() => 
    analyticsEngine.calculateProgress(userResponses),
    [userResponses]
  );
  
  // Virtual scrolling for large datasets
  const VirtualizedExerciseList = React.memo(({ exercises }) => {
    return (
      <FixedSizeList
        height={600}
        itemCount={exercises.length}
        itemSize={100}
      >
        {ExerciseRow}
      </FixedSizeList>
    );
  });
  ```

- [ ] **Comprehensive Testing**
  - Unit tests for all components (>90% coverage)
  - Integration tests for user flows
  - Accessibility testing with automated tools
  - Performance testing and optimization

---

# Risk Analysis and Mitigation Strategies

## High-Risk Areas

### 1. Data Migration Complexity
**Risk Level:** HIGH  
**Impact:** Could lose user progress data

**Mitigation Strategies:**
- Create comprehensive data migration scripts with validation
- Implement rollback mechanisms for failed migrations
- Test migration with production-like data sets
- Provide data export/import functionality as backup

**Action Items:**
- [ ] Create data validation schemas
- [ ] Implement migration rollback procedures
- [ ] Test with large datasets (>10,000 exercises)
- [ ] Create user-friendly data export tools

### 2. Performance Degradation
**Risk Level:** MEDIUM  
**Impact:** Poor user experience, especially on mobile

**Mitigation Strategies:**
- Implement aggressive code splitting and lazy loading
- Use React.memo and useMemo for expensive operations  
- Virtual scrolling for large data sets
- Service worker caching strategies

**Action Items:**
- [ ] Establish performance budgets (< 2s load time)
- [ ] Implement performance monitoring
- [ ] Create performance testing suite
- [ ] Optimize bundle size (< 1MB initial load)

### 3. Accessibility Regression
**Risk Level:** MEDIUM  
**Impact:** Loss of WCAG 2.1 AA compliance

**Mitigation Strategies:**
- Port existing accessibility features methodically
- Implement automated accessibility testing
- Conduct user testing with assistive technology users
- Create accessibility checklist for each component

**Action Items:**
- [ ] Set up automated accessibility testing (axe-core)
- [ ] Create accessibility testing protocol
- [ ] Establish screen reader testing procedures
- [ ] Document keyboard navigation patterns

## Medium-Risk Areas

### 4. Cross-Browser Compatibility
**Risk Level:** MEDIUM  
**Impact:** Inconsistent experience across browsers

**Mitigation Strategies:**
- Use progressive enhancement principles
- Implement feature detection over browser detection
- Test on all major browsers regularly
- Use polyfills for newer features

### 5. Offline Functionality
**Risk Level:** MEDIUM  
**Impact:** App unusable without internet connection

**Mitigation Strategies:**
- Implement comprehensive service worker
- Cache critical resources and data
- Provide clear offline status indicators
- Design degraded offline experience

---

# Testing Checkpoints and Validation Criteria

## Phase 1 Checkpoints ✅

### Core Logic Validation
- [ ] **Unit Test Coverage:** >95% for all business logic modules
- [ ] **Performance Benchmarks:** 
  - Exercise generation: <100ms
  - Answer validation: <50ms
  - Analytics calculations: <200ms
- [ ] **Data Integrity:** All existing user data migrates successfully
- [ ] **Algorithm Parity:** JavaScript implementation matches Python behavior

### Success Criteria:
- All business logic functions work identically to PyQt version
- No data loss during migration process
- Performance meets or exceeds desktop application

## Phase 2 Checkpoints ✅

### Development Environment
- [ ] **Build Process:** Clean builds with zero warnings
- [ ] **Code Quality:** ESLint passes with zero errors
- [ ] **Type Safety:** TypeScript compilation with strict mode
- [ ] **Testing Setup:** All test suites run successfully

### Success Criteria:
- Development environment supports efficient iteration
- Code quality tools prevent regression
- Testing infrastructure enables confidence in changes

## Phase 3 Checkpoints ✅

### Component Migration
- [ ] **Visual Parity:** UI matches PyQt version on desktop
- [ ] **Responsive Design:** Works well on mobile (>768px width)
- [ ] **Accessibility:** WCAG 2.1 AA compliance verified
- [ ] **Performance:** Components render in <16ms (60fps)

### Success Criteria:
- Feature parity with PyQt version
- Enhanced mobile experience
- Improved accessibility over desktop version

## Phase 4 Checkpoints ✅

### Final Validation
- [ ] **User Acceptance Testing:** 5+ users complete full exercise session
- [ ] **Browser Testing:** Works in Chrome, Firefox, Safari, Edge
- [ ] **Performance:** Lighthouse score >90 in all categories
- [ ] **Accessibility:** Screen reader testing passes
- [ ] **Offline Testing:** Core features work without internet

### Success Criteria:
- Production-ready application
- User experience exceeds desktop version
- Deployment ready with monitoring

---

# Deployment Strategy

## Staging Environment
**Timeline:** End of Week 4

- Deploy to staging environment (Vercel/Netlify)
- Configure CI/CD pipeline
- Set up monitoring and error tracking
- Conduct user acceptance testing

## Production Deployment
**Timeline:** End of Week 5

- Deploy to production environment
- Configure CDN and caching
- Set up analytics and monitoring
- Create rollback procedures

## Post-Launch Support
**Timeline:** Week 6+

- Monitor performance and errors
- Collect user feedback
- Plan feature enhancements
- Maintain security updates

---

# Success Metrics

## Technical Metrics
- **Performance:** Page load <2s, component renders <16ms
- **Accessibility:** WCAG 2.1 AA compliance verified
- **Browser Support:** 95%+ compatibility score
- **Bundle Size:** <1MB initial, <500KB per route
- **Test Coverage:** >90% overall, >95% business logic

## User Experience Metrics
- **Task Completion Rate:** >95% (matching desktop version)
- **User Satisfaction:** >4.5/5 rating
- **Mobile Usage:** >40% of sessions
- **Session Duration:** Maintained or improved vs desktop
- **Error Rate:** <1% of user actions

## Business Metrics
- **User Retention:** Match or exceed desktop version
- **Feature Adoption:** >80% of users try new web features
- **Support Requests:** <5% increase during migration
- **Performance Complaints:** <2% of user feedback

---

# Appendices

## A. Technology Stack Summary

### Frontend
- **Framework:** React 18 with TypeScript
- **Styling:** Styled-components with CSS-in-JS
- **State Management:** React Context + Custom hooks
- **Routing:** React Router v6
- **Testing:** Jest + React Testing Library
- **Accessibility:** @axe-core/react for automated testing

### Backend/Storage
- **Local Storage:** Browser localStorage + IndexedDB
- **Cloud Storage:** Firebase/Supabase (optional)
- **Authentication:** Firebase Auth (if cloud storage used)

### DevOps
- **Bundling:** Create React App (Webpack)
- **Deployment:** Vercel or Netlify
- **CI/CD:** GitHub Actions
- **Monitoring:** Sentry for error tracking
- **Analytics:** Google Analytics 4

## B. File Structure Reference

```
spanish-subjunctive-web/
├── public/
│   ├── index.html
│   ├── manifest.json
│   └── sw.js
├── src/
│   ├── components/        # React components
│   ├── hooks/            # Custom hooks
│   ├── context/          # React context providers
│   ├── core/             # Business logic (migrated from Python)
│   ├── storage/          # Data persistence layer
│   ├── styles/           # Theming and global styles
│   ├── types/            # TypeScript definitions
│   ├── utils/            # Utility functions
│   └── __tests__/        # Test files
├── docs/                 # Documentation
├── scripts/              # Build and deployment scripts
└── package.json
```

## C. Migration Validation Checklist

### Pre-Migration
- [ ] Complete code audit of existing PyQt application
- [ ] Document all current features and behaviors
- [ ] Create comprehensive test suite for existing functionality
- [ ] Set up development environment and tooling

### During Migration
- [ ] Regular testing against original application
- [ ] Progressive feature validation
- [ ] Accessibility compliance verification
- [ ] Performance monitoring and optimization

### Post-Migration
- [ ] User acceptance testing with existing users
- [ ] Performance comparison with desktop version
- [ ] Accessibility testing with assistive technology users
- [ ] Cross-browser and cross-device validation

---

**Document Version:** 1.0  
**Last Updated:** 2025-08-27  
**Author:** Claude Code Assistant  
**Review Status:** Ready for Implementation
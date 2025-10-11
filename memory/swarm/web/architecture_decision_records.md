# Architecture Decision Records (ADR)
## Spanish Subjunctive Practice Web Migration

### Decision Overview
This document records the key architectural decisions made during the consolidation of 224+ PyQt desktop modules into 35 web-focused modules.

---

## ADR-001: Web Framework Selection

**Status**: Accepted  
**Date**: 2025-09-01  
**Deciders**: System Architecture Team

### Context
Need to select appropriate web frameworks for the Spanish Subjunctive Practice application migration from PyQt desktop to web.

### Decision
- **Backend**: FastAPI (Python)
- **Frontend**: React with TypeScript
- **Database**: PostgreSQL
- **Styling**: Tailwind CSS

### Rationale

#### FastAPI Selection
1. **Performance**: Superior performance compared to Django/Flask
2. **Type Safety**: Native Pydantic integration for data validation
3. **Documentation**: Automatic OpenAPI/Swagger documentation
4. **Async Support**: Built-in async/await support for better concurrency
5. **Python Familiarity**: Team expertise in Python ecosystem

#### React + TypeScript Selection
1. **Component Reusability**: Excellent for educational UI components
2. **Type Safety**: TypeScript catches errors at compile time
3. **Accessibility**: Rich ecosystem of a11y tools and patterns
4. **Performance**: Virtual DOM and React 18 concurrent features
5. **Developer Experience**: Excellent tooling and debugging support

#### PostgreSQL Selection
1. **ACID Compliance**: Essential for user progress data integrity
2. **JSON Support**: Flexible storage for exercise metadata
3. **Full-text Search**: Native support for Spanish content search
4. **Scaling**: Proven scalability for educational applications
5. **Analytics**: Rich query capabilities for learning analytics

#### Tailwind CSS Selection
1. **Consistency**: Utility-first approach ensures design consistency
2. **Accessibility**: Built-in accessibility considerations
3. **Performance**: Purged CSS reduces bundle size
4. **Responsive**: Mobile-first responsive design utilities
5. **Maintainability**: Less custom CSS to maintain

### Consequences

#### Positive
- Modern, maintainable codebase
- Superior performance compared to desktop app
- Enhanced accessibility and mobile support
- Automatic API documentation
- Strong type safety throughout stack

#### Negative
- Learning curve for team members unfamiliar with React/TypeScript
- Initial setup complexity higher than simpler frameworks
- Requires modern browser support (IE11 not supported)

### Compliance
- WCAG 2.1 AA compatibility maintained
- All desktop functionality preserved
- Performance targets: <2s initial load, <100ms interactions

---

## ADR-002: Module Consolidation Strategy

**Status**: Accepted  
**Date**: 2025-09-01  
**Deciders**: System Architecture Team

### Context
Need to consolidate 224 Python modules into 35 web modules while preserving all functionality and improving maintainability.

### Decision
Implement aggressive consolidation following these principles:
1. **Eliminate PyQt Dependencies**: Remove all 89 PyQt-related modules
2. **Consolidate UI Systems**: Merge 76 overlapping UI modules into 8 React components
3. **Modernize Testing**: Replace 31 desktop test modules with 5 web test suites
4. **Preserve Core Logic**: Maintain 12 core business logic modules with minimal changes
5. **Selective Example Adaptation**: Keep web-relevant examples, remove desktop-specific ones

### Rationale

#### PyQt Elimination (89 → 0 modules)
- **Reason**: Web application has no need for desktop UI framework
- **Impact**: 39.7% module reduction
- **Risk Mitigation**: All UI functionality recreated in React components

#### UI System Consolidation (76 → 8 modules)
- **Reason**: Multiple overlapping UI systems with similar functionality
- **Impact**: 89.5% reduction in UI modules
- **Benefits**: 
  - Single source of truth for UI patterns
  - Consistent accessibility implementation
  - Easier maintenance and updates
  - Better performance through optimized components

#### Core Logic Preservation (12 → 12 modules)
- **Reason**: Business logic is framework-agnostic and proven
- **Approach**: Port to JavaScript/TypeScript for frontend, keep Python for backend
- **Benefits**: Reduced risk, faster migration, preserved domain expertise

### Module Mapping Strategy

#### Backend Consolidation (89 desktop → 15 web modules)
```
PyQt Desktop Modules (89) → FastAPI Backend (15)
├── Core API Layer (5 modules)
│   ├── main.py (application entry)
│   ├── routes/ (4 route modules)
│   └── middleware.py
├── Business Logic (6 modules)
│   ├── conjugation_engine.py
│   ├── exercise_generator.py
│   ├── session_manager.py
│   ├── learning_analytics.py
│   ├── spaced_repetition.py
│   └── error_analyzer.py
└── Data Layer (4 modules)
    ├── database.py
    ├── user.py
    ├── exercise.py
    └── session.py
```

#### Frontend Consolidation (135 UI → 20 web modules)
```
PyQt UI Modules (135) → React Frontend (20)
├── Core Components (8 modules)
│   ├── ExerciseCard.tsx
│   ├── ProgressBar.tsx
│   ├── AnswerInput.tsx
│   ├── MultipleChoice.tsx
│   ├── FeedbackDisplay.tsx
│   ├── NavigationMenu.tsx
│   ├── LoadingState.tsx
│   └── ErrorBoundary.tsx
├── Feature Modules (7 modules)
│   ├── AuthProvider.tsx
│   ├── PracticeSession.tsx
│   ├── ExerciseFlow.tsx
│   ├── Dashboard.tsx
│   ├── ProgressDashboard.tsx
│   ├── AccessibilityProvider.tsx
│   └── UserProfile.tsx
└── Infrastructure (5 modules)
    ├── App.tsx
    ├── client.ts
    ├── useExercise.ts
    ├── helpers.ts
    └── global.css
```

### Consequences

#### Positive
- 84.4% reduction in module count (224 → 35)
- Simplified maintenance and debugging
- Single responsibility principle enforced
- Reduced cognitive load for developers
- Faster build and deployment times

#### Negative
- Larger individual modules may be harder to understand initially
- Risk of creating "god components" if not carefully managed
- Initial migration effort is substantial

### Mitigation Strategies
- Comprehensive documentation for each consolidated module
- Clear separation of concerns within larger components
- Thorough testing to ensure no functionality is lost
- Gradual rollout with extensive user testing

---

## ADR-003: Accessibility Implementation Strategy

**Status**: Accepted  
**Date**: 2025-09-01  
**Deciders**: System Architecture Team, Accessibility Expert

### Context
Must preserve and enhance accessibility features from desktop application while adapting to web standards (WCAG 2.1 AA compliance).

### Decision
Implement comprehensive web accessibility through:
1. **Centralized Accessibility Provider**: Single source for all a11y features
2. **ARIA-First Design**: Semantic HTML with comprehensive ARIA attributes
3. **Keyboard Navigation**: Full keyboard accessibility for all interactions
4. **Screen Reader Optimization**: Live regions and announcements
5. **Responsive Accessibility**: Touch-friendly design with appropriate target sizes

### Desktop → Web Accessibility Mapping

#### Desktop Features → Web Implementation
```
Desktop Accessibility → Web Accessibility
├── Qt Screen Reader Support → ARIA live regions + announcements
├── Qt Keyboard Navigation → Focus management + key handlers
├── Qt High Contrast → CSS custom properties + themes
├── Qt Font Scaling → Responsive typography system
├── Qt Focus Indicators → CSS focus rings + visible focus
├── Qt Tooltips → ARIA descriptions + hover states
└── Qt Shortcuts → Custom keyboard shortcuts
```

#### Implementation Details

**1. Visual Accessibility**
```typescript
// Desktop: Qt high contrast, font scaling
// Web: CSS custom properties, responsive design
const visualA11y = {
  highContrast: 'contrast(150%) brightness(120%)',
  fontSize: 'clamp(1rem, 2.5vw, 1.5rem)',
  focusRing: '3px solid #0066CC',
  colorContrast: '>= 4.5:1 ratio'
};
```

**2. Keyboard Navigation**
```typescript
// Desktop: Qt key events
// Web: Custom keyboard event handlers
const keyboardNav = {
  exerciseNavigation: ['Tab', 'Shift+Tab', 'Arrow keys'],
  shortcuts: ['Ctrl+K', 'Ctrl+R', 'Ctrl+T'],
  focusManagement: 'automatic focus on new exercises',
  skipLinks: 'skip to content, skip to navigation'
};
```

**3. Screen Reader Support**
```typescript
// Desktop: Qt accessibility API
// Web: ARIA + live regions
const screenReaderSupport = {
  announcements: 'aria-live="polite|assertive"',
  descriptions: 'aria-describedby for hints and explanations',
  labels: 'aria-label for all interactive elements',
  landmarks: 'nav, main, aside roles'
};
```

**4. Motor Accessibility**
```typescript
// Desktop: Qt click areas, drag/drop alternatives
// Web: Touch targets, gesture alternatives
const motorA11y = {
  touchTargets: 'minimum 44px × 44px',
  clickAreas: 'expanded clickable areas',
  alternatives: 'keyboard alternatives to all gestures',
  dwellClick: 'optional dwell click support'
};
```

### Configuration System
Centralized accessibility settings preserving desktop app preferences:
```json
{
  "visual": {
    "highContrast": false,
    "fontSize": 1.0,
    "reduceMotion": false,
    "darkMode": false
  },
  "keyboard": {
    "navigationEnabled": true,
    "shortcuts": { "submitAnswer": "Enter", "showHint": "H" },
    "skipLinks": true
  },
  "screenReader": {
    "announcements": true,
    "verbosity": "normal",
    "liveRegions": true
  },
  "motor": {
    "touchTargets": 44,
    "dwellClick": false,
    "gestureAlternatives": true
  }
}
```

### Consequences

#### Positive
- Enhanced accessibility beyond desktop app capabilities
- WCAG 2.1 AA compliance achieved
- Better mobile accessibility
- Consistent accessibility patterns across app
- Automated accessibility testing integration

#### Negative
- Increased initial development time
- More complex component implementations
- Additional testing requirements

### Testing Strategy
- Automated accessibility testing with axe-core
- Screen reader testing with NVDA, JAWS, VoiceOver
- Keyboard-only navigation testing
- Mobile accessibility testing
- User testing with accessibility community

---

## ADR-004: Data Migration and Persistence Strategy

**Status**: Accepted  
**Date**: 2025-09-01  
**Deciders**: System Architecture Team, Data Engineering

### Context
Need to migrate user data from desktop SQLite databases to web PostgreSQL while preserving all progress and settings.

### Decision
Implement comprehensive data migration with:
1. **Schema Evolution**: Modern relational design optimized for web
2. **Data Export/Import**: Tools for seamless user data migration
3. **Progressive Enhancement**: Graceful handling of missing data
4. **Backup Strategy**: Complete data protection during migration

### Migration Strategy

#### Desktop SQLite → Web PostgreSQL Schema Mapping
```sql
-- Desktop: Simple tables
users_old(id, username, settings_json)
progress_old(user_id, exercise_id, attempts, success_rate)

-- Web: Normalized relational design
users(id, email, full_name, created_at, ...)
user_preferences(user_id, key, value, ...)
sessions(id, user_id, started_at, completed_at, ...)
exercise_results(id, user_id, exercise_id, session_id, ...)
spaced_repetition(id, user_id, exercise_id, next_review, ...)
```

#### Data Preservation Strategy
```typescript
interface MigrationMapping {
  // Preserve all user progress
  exerciseResults: {
    accuracy: 'calculated from attempts/successes',
    streaks: 'reconstructed from session data',
    preferences: 'migrated from settings JSON'
  };
  
  // Enhance with new features
  spacedRepetition: {
    schedule: 'calculated from historical performance',
    ease_factor: 'derived from accuracy patterns',
    review_history: 'reconstructed from exercise results'
  };
  
  // Preserve accessibility settings
  accessibility: {
    settings: 'direct migration from desktop config',
    preferences: 'enhanced with web-specific options'
  };
}
```

### Migration Tools

#### Export Tool (Desktop App)
```python
class DesktopDataExporter:
    def export_user_data(self, user_id: int) -> Dict[str, Any]:
        return {
            'user_profile': self.export_profile(user_id),
            'exercise_history': self.export_exercise_results(user_id),
            'learning_progress': self.export_progress_data(user_id),
            'accessibility_settings': self.export_accessibility(user_id),
            'session_history': self.export_sessions(user_id)
        }
```

#### Import Tool (Web App)
```python
class WebDataImporter:
    async def import_user_data(self, export_data: Dict[str, Any]) -> User:
        async with self.db.begin():
            user = await self.create_user(export_data['user_profile'])
            await self.import_exercise_history(user.id, export_data['exercise_history'])
            await self.calculate_spaced_repetition_schedules(user.id)
            await self.import_accessibility_settings(user.id, export_data['accessibility_settings'])
            return user
```

### Consequences

#### Positive
- Zero data loss during migration
- Enhanced data relationships and analytics capabilities
- Improved query performance with proper indexing
- Better data integrity with foreign key constraints
- Scalable schema for multi-user web environment

#### Negative
- Complex migration process requiring careful testing
- Temporary data inconsistency during migration window
- Requires both old and new systems running during transition

### Rollback Plan
- Complete database backups before migration
- Parallel operation capability during transition
- Data validation tools to verify migration accuracy
- Rollback scripts to restore desktop functionality if needed

---

## ADR-005: Performance and Scalability Requirements

**Status**: Accepted  
**Date**: 2025-09-01  
**Deciders**: System Architecture Team, Performance Engineering

### Context
Web application must meet or exceed desktop application performance while supporting multiple concurrent users.

### Decision
Implement comprehensive performance optimization:
1. **Frontend Performance**: <2s initial load, <100ms interaction response
2. **Backend Performance**: <50ms API response time (95th percentile)
3. **Database Performance**: Optimized queries with proper indexing
4. **Caching Strategy**: Multi-level caching for exercise content
5. **Progressive Loading**: Lazy loading and code splitting

### Performance Targets

#### Frontend Performance Budget
```typescript
const performanceBudgets = {
  initialLoad: {
    firstContentfulPaint: '<1.5s',
    largestContentfulPaint: '<2s',
    cumulativeLayoutShift: '<0.1',
    firstInputDelay: '<100ms'
  },
  
  interactions: {
    exerciseTransition: '<100ms',
    answerValidation: '<50ms',
    feedbackDisplay: '<200ms',
    navigationChange: '<100ms'
  },
  
  bundles: {
    initialBundle: '<500KB gzipped',
    chunkSize: '<250KB per chunk',
    totalAssets: '<2MB for complete app'
  }
};
```

#### Backend Performance Targets
```python
performance_targets = {
    'api_response_times': {
        'exercise_generation': '<100ms',
        'answer_validation': '<50ms',
        'progress_analytics': '<200ms',
        'user_authentication': '<100ms'
    },
    
    'database_queries': {
        'simple_selects': '<10ms',
        'complex_analytics': '<100ms',
        'concurrent_users': '1000+ simultaneous'
    },
    
    'caching': {
        'exercise_cache_hit_rate': '>90%',
        'static_content_cache': '>95%',
        'api_response_cache': '>80%'
    }
}
```

### Optimization Strategies

#### 1. Frontend Optimization
```typescript
// Code splitting by route and feature
const PracticeSession = lazy(() => import('./features/practice/PracticeSession'));

// Progressive enhancement
const enhancedFeatures = {
  animations: 'reduced motion respected',
  images: 'lazy loaded with intersection observer',
  fonts: 'font-display: swap for faster rendering'
};

// Service worker for caching
const cachingStrategy = {
  exercises: 'cache-first with background update',
  api: 'network-first with fallback',
  static: 'cache-first with versioning'
};
```

#### 2. Backend Optimization
```python
# Database query optimization
class OptimizedQueries:
    @cached(ttl=300)  # 5 minute cache
    async def get_user_progress(self, user_id: int):
        # Optimized query with proper indexes
        return await self.db.execute(
            select(UserProgress)
            .options(selectinload(UserProgress.sessions))
            .where(UserProgress.user_id == user_id)
        )
    
    # Connection pooling
    engine = create_async_engine(
        DATABASE_URL,
        pool_size=20,
        max_overflow=30,
        pool_timeout=30
    )
```

#### 3. Caching Strategy
```python
# Multi-level caching
caching_strategy = {
    'browser': 'ServiceWorker + localStorage',
    'cdn': 'CloudFront with 1 year static cache',
    'application': 'Redis for session data',
    'database': 'Query result caching with invalidation'
}
```

### Monitoring and Metrics

#### Performance Monitoring
```typescript
// Real User Monitoring (RUM)
const performanceObserver = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    analytics.track('performance', {
      name: entry.name,
      duration: entry.duration,
      type: entry.entryType
    });
  }
});

// Core Web Vitals tracking
const vitalsObserver = new PerformanceObserver((list) => {
  list.getEntries().forEach((entry) => {
    if (entry.entryType === 'largest-contentful-paint') {
      analytics.track('lcp', entry.startTime);
    }
  });
});
```

#### Backend Monitoring
```python
# Application Performance Monitoring (APM)
@app.middleware("http")
async def performance_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    # Log slow requests
    if duration > 0.1:  # 100ms threshold
        logger.warning(f"Slow request: {request.url.path} took {duration:.2f}s")
    
    return response
```

### Consequences

#### Positive
- Superior performance compared to desktop application
- Scalable architecture supporting growth
- Excellent user experience across devices
- Comprehensive performance monitoring
- Optimized for both speed and efficiency

#### Negative
- Increased complexity in optimization implementation
- Additional monitoring and alerting infrastructure required
- Performance budgets may limit some feature implementations

### Success Criteria
- 95% of users experience <2s initial load time
- 99% of interactions complete in <100ms
- 99.9% uptime for production application
- Support for 1000+ concurrent users
- Lighthouse performance score >90

---

## Summary of Architectural Decisions

### Key Outcomes
1. **Technology Stack**: FastAPI + React + TypeScript + PostgreSQL
2. **Module Consolidation**: 224 → 35 modules (84.4% reduction)
3. **Accessibility**: WCAG 2.1 AA compliance with enhanced web features
4. **Performance**: <2s load time, <100ms interactions
5. **Data Migration**: Comprehensive tools for zero-loss migration

### Success Metrics
- **Maintainability**: 84% fewer modules to maintain
- **Performance**: 3x faster than desktop app
- **Accessibility**: 100% WCAG 2.1 AA compliance
- **Scalability**: Support for 1000+ concurrent users
- **User Experience**: Mobile-first responsive design

### Risk Mitigation
- Comprehensive testing strategy covering functionality and performance
- Gradual rollout with extensive user feedback
- Rollback capabilities at each migration stage
- Performance monitoring and alerting from day one
- Accessibility testing with real users throughout development

These architectural decisions provide a solid foundation for migrating the Spanish Subjunctive Practice application from a 224-module PyQt desktop application to a modern, scalable, accessible web application with only 35 modules while preserving all functionality and significantly enhancing the user experience.
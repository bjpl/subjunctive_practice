# Architecture Decision Records (ADRs)
## Spanish Subjunctive Practice Application Web Migration

**Date:** August 26, 2025  
**Author:** System Architecture Designer  
**Status:** Active

---

## ADR-001: Web Migration Technology Stack

### Status: **ACCEPTED**
### Date: 2025-08-26

### Context
The existing Spanish subjunctive practice application is built with PyQt5 and has grown to over 46,000 lines in the main file. We need to migrate to a web-based solution for better maintainability, cross-platform support, and modern user experience.

### Decision
We will use **FastAPI + React + TypeScript** as the primary technology stack.

**Backend**: FastAPI with Python
**Frontend**: React with TypeScript
**Database**: PostgreSQL (production) / SQLite (development)
**Styling**: Tailwind CSS with Headless UI

### Rationale

#### FastAPI for Backend
**Chosen over Django/Flask/Node.js**
- ✅ **Code Reuse**: Preserves existing Python learning algorithms
- ✅ **Performance**: AsyncIO support for concurrent operations
- ✅ **Type Safety**: Pydantic models with automatic validation
- ✅ **Documentation**: Auto-generated OpenAPI documentation
- ✅ **Modern**: Built-in support for WebSockets and modern web standards

#### React + TypeScript for Frontend
**Chosen over Vue.js/Angular/Vanilla JS**
- ✅ **Ecosystem**: Largest component library ecosystem
- ✅ **Accessibility**: Excellent a11y tooling and community support
- ✅ **Type Safety**: Strong TypeScript integration
- ✅ **Performance**: Mature optimization patterns and tools
- ✅ **Team Expertise**: Better long-term maintainability

#### Tailwind CSS for Styling
**Chosen over Material-UI/Bootstrap/Custom CSS**
- ✅ **Utility-First**: Faster development and consistent design
- ✅ **Customization**: Easy theme system for accessibility
- ✅ **Performance**: Purged CSS reduces bundle size
- ✅ **Responsive**: Mobile-first responsive design patterns

### Consequences
**Positive**:
- Modern development experience with hot reloading
- Strong typing reduces runtime errors
- Excellent tooling and debugging capabilities
- Large community and extensive documentation

**Negative**:
- Learning curve for React if team is unfamiliar
- More complex build process than simple static sites
- Requires modern browser support

**Risks**:
- Bundle size could be large without proper optimization
- SEO considerations if not properly handled with SSR

---

## ADR-002: Component Architecture Pattern

### Status: **ACCEPTED**
### Date: 2025-08-26

### Context
The current PyQt application has complex UI state management spread across multiple modules. We need a clear architecture for managing component state and data flow in the web version.

### Decision
We will implement a **Container/Presentation Component** pattern with **Redux Toolkit** for global state management.

### Architecture Pattern
```typescript
// Container Component (Smart)
const ExerciseContainer: React.FC = () => {
  const dispatch = useAppDispatch();
  const { currentExercise, isLoading } = useAppSelector(state => state.exercise);
  
  return (
    <ExercisePresentation
      exercise={currentExercise}
      isLoading={isLoading}
      onSubmit={(answer) => dispatch(submitAnswer(answer))}
    />
  );
};

// Presentation Component (Dumb)
interface ExercisePresentationProps {
  exercise: Exercise | null;
  isLoading: boolean;
  onSubmit: (answer: string) => void;
}

const ExercisePresentation: React.FC<ExercisePresentationProps> = ({
  exercise,
  isLoading,
  onSubmit
}) => {
  // Pure UI logic only
};
```

### Rationale
- **Separation of Concerns**: Business logic separate from presentation
- **Testability**: Easy to test both logic and UI independently
- **Reusability**: Presentation components can be reused in different contexts
- **Performance**: Easier to optimize with React.memo and selective re-renders

### State Management Structure
```typescript
interface RootState {
  exercise: ExerciseState;
  session: SessionState;
  user: UserState;
  ui: UIState;
}

interface ExerciseState {
  current: Exercise | null;
  history: Exercise[];
  isLoading: boolean;
  error: string | null;
}
```

### Consequences
**Positive**:
- Clear data flow and predictable state updates
- Easier debugging with Redux DevTools
- Component reusability and testability

**Negative**:
- More boilerplate code initially
- Learning curve for Redux concepts

---

## ADR-003: Accessibility Architecture

### Status: **ACCEPTED**
### Date: 2025-08-26

### Context
The existing PyQt application has extensive accessibility features (WCAG 2.1 AA compliant). The web version must maintain or exceed this accessibility level.

### Decision
We will implement a **multi-layered accessibility architecture** with automated testing and manual verification.

### Architecture Layers

#### 1. Component-Level Accessibility
```typescript
interface AccessibleComponentProps {
  'aria-label'?: string;
  'aria-describedby'?: string;
  role?: string;
  tabIndex?: number;
}

const AccessibleButton: React.FC<AccessibleComponentProps & ButtonProps> = ({
  children,
  onClick,
  disabled,
  'aria-label': ariaLabel,
  'aria-describedby': ariaDescribedby,
  ...props
}) => {
  return (
    <button
      aria-label={ariaLabel}
      aria-describedby={ariaDescribedby}
      disabled={disabled}
      onClick={onClick}
      className="focus-visible:ring-2 focus-visible:ring-blue-500"
      {...props}
    >
      {children}
    </button>
  );
};
```

#### 2. Focus Management System
```typescript
const FocusManagementContext = createContext({
  focusHistory: [],
  setFocus: (element: HTMLElement) => {},
  restoreFocus: () => {},
  trapFocus: (container: HTMLElement) => {}
});

const useFocusManagement = () => {
  const context = useContext(FocusManagementContext);
  if (!context) {
    throw new Error('useFocusManagement must be used within FocusManagementProvider');
  }
  return context;
};
```

#### 3. Screen Reader Announcements
```typescript
const AnnouncementService = {
  announce: (message: string, priority: 'polite' | 'assertive' = 'polite') => {
    const announcer = document.createElement('div');
    announcer.setAttribute('aria-live', priority);
    announcer.setAttribute('aria-atomic', 'true');
    announcer.className = 'sr-only';
    announcer.textContent = message;
    
    document.body.appendChild(announcer);
    setTimeout(() => document.body.removeChild(announcer), 1000);
  }
};
```

#### 4. Keyboard Navigation System
```typescript
const KeyboardNavigation = {
  shortcuts: new Map([
    ['Enter', 'submit-answer'],
    ['Escape', 'close-modal'],
    ['ArrowRight', 'next-exercise'],
    ['ArrowLeft', 'previous-exercise'],
    ['h', 'show-hint']
  ]),
  
  handleKeyDown: (event: KeyboardEvent, handlers: Record<string, () => void>) => {
    const action = KeyboardNavigation.shortcuts.get(event.key);
    if (action && handlers[action]) {
      event.preventDefault();
      handlers[action]();
    }
  }
};
```

### Testing Strategy
- **Automated**: Jest + React Testing Library + axe-core
- **Manual**: Screen reader testing (NVDA, JAWS, VoiceOver)
- **Continuous**: Lighthouse accessibility audits in CI/CD

### Consequences
**Positive**:
- Maintains excellent accessibility standards
- Automated testing prevents regressions
- Systematic approach ensures consistency

**Negative**:
- Additional development time for accessibility features
- Requires accessibility expertise on the team

---

## ADR-004: Responsive Design Strategy

### Status: **ACCEPTED**
### Date: 2025-08-26

### Context
The current desktop application needs to work well on various screen sizes, from mobile phones to large desktop monitors, while maintaining usability for language learning.

### Decision
We will implement a **mobile-first responsive design** with progressive enhancement for larger screens.

### Breakpoint Strategy
```css
/* Mobile First Approach */
.container {
  /* Mobile (default): 320px - 768px */
  padding: 1rem;
  font-size: 1rem;
}

@media (min-width: 768px) {
  /* Tablet: 768px - 1024px */
  .container {
    padding: 1.5rem;
    font-size: 1.125rem;
  }
}

@media (min-width: 1024px) {
  /* Desktop: 1024px+ */
  .container {
    padding: 2rem;
    font-size: 1.25rem;
    max-width: 1200px;
    margin: 0 auto;
  }
}
```

### Layout Patterns

#### 1. Exercise Display Layout
```typescript
const ExerciseLayout: React.FC = ({ children }) => (
  <div className="
    grid grid-cols-1 gap-4 p-4
    md:grid-cols-2 md:gap-6 md:p-6
    lg:grid-cols-3 lg:gap-8 lg:p-8
    max-w-7xl mx-auto
  ">
    {children}
  </div>
);
```

#### 2. Navigation Patterns
- **Mobile**: Bottom tab navigation
- **Tablet**: Side navigation drawer
- **Desktop**: Top navigation with sidebar

#### 3. Touch-Friendly Design
- Minimum 44px touch targets (WCAG AA)
- Swipe gestures for mobile navigation
- Hover states only on non-touch devices

### Consequences
**Positive**:
- Excellent user experience across all devices
- Better accessibility with larger touch targets
- Future-proof design as mobile usage increases

**Negative**:
- More complex CSS and testing requirements
- Potential performance considerations for complex layouts

---

## ADR-005: Progressive Web App (PWA) Implementation

### Status: **ACCEPTED**
### Date: 2025-08-26

### Context
Users need the ability to practice Spanish subjunctive conjugations offline, especially when traveling or in areas with poor internet connectivity.

### Decision
We will implement a **full Progressive Web App** with comprehensive offline capabilities.

### PWA Features

#### 1. Service Worker Architecture
```typescript
// sw.ts - Service Worker
const CACHE_NAME = 'subjunctive-practice-v1';
const EXERCISES_CACHE = 'exercises-v1';
const API_CACHE = 'api-responses-v1';

self.addEventListener('fetch', (event) => {
  if (event.request.url.includes('/api/exercises')) {
    event.respondWith(
      caches.open(EXERCISES_CACHE).then(cache => 
        cache.match(event.request).then(response => 
          response || fetch(event.request).then(fetchResponse => {
            cache.put(event.request, fetchResponse.clone());
            return fetchResponse;
          })
        )
      )
    );
  }
});
```

#### 2. Offline Data Strategy
- **Exercises**: Pre-cache 100 most common exercises
- **Progress**: Local storage with background sync
- **Settings**: Persist in IndexedDB
- **Images/Assets**: Cache-first strategy

#### 3. Background Sync
```typescript
// Background sync for progress updates
self.addEventListener('sync', (event) => {
  if (event.tag === 'background-sync-progress') {
    event.waitUntil(syncProgress());
  }
});

const syncProgress = async () => {
  const offlineProgress = await getOfflineProgress();
  if (offlineProgress.length > 0) {
    try {
      await fetch('/api/sync/progress', {
        method: 'POST',
        body: JSON.stringify(offlineProgress)
      });
      await clearOfflineProgress();
    } catch (error) {
      console.log('Sync failed, will retry later');
    }
  }
};
```

#### 4. App Shell Architecture
- Core UI components cached on first visit
- Dynamic content loaded and cached as needed
- Graceful degradation when offline

### Installation Strategy
- Web App Manifest for "Add to Home Screen"
- Install prompts after user engagement
- iOS Safari bookmark guidance

### Consequences
**Positive**:
- Full functionality when offline
- App-like experience on mobile devices
- Reduced server load through caching

**Negative**:
- Increased complexity in data synchronization
- More testing required for offline scenarios
- Storage management considerations

---

## ADR-006: Performance Architecture

### Status: **ACCEPTED**
### Date: 2025-08-26

### Context
The web application must perform as well as or better than the current desktop application, with fast loading times and smooth interactions.

### Decision
We will implement a **performance-first architecture** with code splitting, lazy loading, and optimized bundling.

### Performance Strategy

#### 1. Bundle Optimization
```typescript
// webpack.config.js
module.exports = {
  optimization: {
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          priority: 10
        },
        common: {
          minChunks: 2,
          priority: 5,
          reuseExistingChunk: true
        }
      }
    }
  }
};
```

#### 2. Component Lazy Loading
```typescript
const ExerciseModule = lazy(() => import('./ExerciseModule'));
const SettingsModule = lazy(() => import('./SettingsModule'));
const StatisticsModule = lazy(() => import('./StatisticsModule'));

const App: React.FC = () => (
  <Suspense fallback={<LoadingSpinner />}>
    <Routes>
      <Route path="/exercise" element={<ExerciseModule />} />
      <Route path="/settings" element={<SettingsModule />} />
      <Route path="/stats" element={<StatisticsModule />} />
    </Routes>
  </Suspense>
);
```

#### 3. Image Optimization
- WebP format with fallbacks
- Responsive images with srcset
- Lazy loading for below-the-fold images
- Optimized SVG icons

#### 4. API Performance
```typescript
// React Query for caching and background updates
const useExercises = (difficulty: string) => {
  return useQuery(
    ['exercises', difficulty],
    () => fetchExercises(difficulty),
    {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      refetchOnWindowFocus: false
    }
  );
};
```

### Performance Budgets
- **First Contentful Paint**: < 1.5s
- **Time to Interactive**: < 3.5s
- **Bundle Size**: < 250KB gzipped
- **Core Web Vitals**: All green scores

### Monitoring Strategy
- Real User Monitoring (RUM)
- Lighthouse CI in deployment pipeline
- Core Web Vitals tracking
- Performance regression alerts

### Consequences
**Positive**:
- Excellent user experience with fast loading
- Better SEO rankings from performance metrics
- Reduced server costs through efficient caching

**Negative**:
- More complex build and deployment process
- Additional monitoring and tooling requirements

---

## ADR-007: Data Migration and Compatibility

### Status: **ACCEPTED**
### Date: 2025-08-26

### Context
Existing users have progress data, settings, and preferences stored in the current PyQt application. This data must be preserved and accessible in the web version.

### Decision
We will implement a **dual-phase migration strategy** with data export/import capabilities and temporary compatibility mode.

### Migration Architecture

#### 1. Data Export from PyQt App
```python
# migration_exporter.py
class DataExporter:
    def export_user_data(self) -> Dict[str, Any]:
        return {
            'version': '1.0',
            'exported_at': datetime.now().isoformat(),
            'user_settings': self.export_settings(),
            'session_history': self.export_sessions(),
            'progress_data': self.export_progress(),
            'streak_data': self.export_streaks()
        }
    
    def export_to_file(self, filepath: str) -> bool:
        try:
            data = self.export_user_data()
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            logger.error(f"Export failed: {e}")
            return False
```

#### 2. Data Import in Web App
```typescript
// migration-service.ts
interface MigrationData {
  version: string;
  exported_at: string;
  user_settings: UserSettings;
  session_history: SessionData[];
  progress_data: ProgressData;
  streak_data: StreakData;
}

class MigrationService {
  async importUserData(file: File): Promise<boolean> {
    try {
      const text = await file.text();
      const data: MigrationData = JSON.parse(text);
      
      await this.validateMigrationData(data);
      await this.importSettings(data.user_settings);
      await this.importProgress(data.progress_data);
      await this.importSessions(data.session_history);
      
      return true;
    } catch (error) {
      console.error('Migration failed:', error);
      return false;
    }
  }
}
```

#### 3. Compatibility Mode
During transition period, support both:
- **Legacy Format**: PyQt data structures
- **Modern Format**: Web app optimized structures
- **Automatic Conversion**: Background migration of data formats

### Migration UI Flow
1. **Welcome Screen**: Option to import existing data
2. **File Upload**: Drag & drop migration file
3. **Validation**: Check data integrity and version
4. **Import Process**: Progress bar with detailed steps
5. **Verification**: Summary of imported data
6. **Cleanup**: Option to remove temporary files

### Backup Strategy
- Automatic backup before migration
- Version control for data schemas
- Rollback capabilities if migration fails

### Consequences
**Positive**:
- Seamless transition for existing users
- No data loss during migration
- Flexible approach supports future migrations

**Negative**:
- Additional development time for migration tools
- Complexity in supporting multiple data formats
- Potential edge cases in data conversion

---

## Summary of Architectural Decisions

| ADR | Decision | Status | Impact |
|-----|----------|--------|--------|
| ADR-001 | FastAPI + React + TypeScript Stack | Accepted | High - Core technology choices |
| ADR-002 | Container/Presentation Pattern | Accepted | Medium - Component architecture |
| ADR-003 | Multi-layered Accessibility | Accepted | High - User experience |
| ADR-004 | Mobile-first Responsive Design | Accepted | High - Cross-platform support |
| ADR-005 | Full Progressive Web App | Accepted | Medium - Offline capabilities |
| ADR-006 | Performance-first Architecture | Accepted | High - User experience |
| ADR-007 | Dual-phase Data Migration | Accepted | Medium - User retention |

## Review and Updates

These ADRs will be reviewed quarterly and updated as the project evolves. Any changes to accepted decisions must be documented with rationale and impact analysis.

**Next Review Date**: November 26, 2025
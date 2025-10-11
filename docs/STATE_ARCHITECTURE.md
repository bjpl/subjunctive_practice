# State Management Architecture

## Visual Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         React Components                         │
│  (Authentication, Exercise Practice, Progress, Settings, etc.)   │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ Uses Custom Hooks
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Custom Hooks Layer                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │ useAuth  │ │useExercise│ │useProgress│ │useSettings│         │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
│  ┌──────────┐ ┌──────────┐ ┌──────────────┐                    │
│  │ useToast │ │useSelector│ │useLocalStorage│                   │
│  └──────────┘ └──────────┘ └──────────────┘                    │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ Dispatches Actions / Queries
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Redux Store                              │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Redux Slices                          │  │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐│  │
│  │  │  Auth  │ │Exercise│ │Progress│ │   UI   │ │Settings││  │
│  │  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘│  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    RTK Query APIs                        │  │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐           │  │
│  │  │ authApi│ │exerApi │ │progApi │ │userApi │           │  │
│  │  └────────┘ └────────┘ └────────┘ └────────┘           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                     Middleware                           │  │
│  │  ┌────────┐ ┌────────┐ ┌────────┐                       │  │
│  │  │  RTK   │ │ Error  │ │ Logger │                       │  │
│  │  │ Query  │ │Handler │ │  (Dev) │                       │  │
│  │  └────────┘ └────────┘ └────────┘                       │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ API Requests
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Backend API Server                          │
│                   (FastAPI - Python)                             │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐              │
│  │  /auth  │ │/exercises│ │/progress│ │  /user  │              │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘              │
└─────────────────────────────────────────────────────────────────┘
                     │
                     │ Persists to
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Persistent Storage                           │
│  ┌──────────────┐              ┌──────────────┐                │
│  │ LocalStorage │              │  JSON Files  │                │
│  │  (Frontend)  │              │  (Backend)   │                │
│  └──────────────┘              └──────────────┘                │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Patterns

### 1. Authentication Flow

```
┌─────────┐     login()      ┌──────────┐    API Call    ┌──────────┐
│Component│ ─────────────────▶│ useAuth  │ ──────────────▶│ authApi  │
└─────────┘                   └──────────┘                └──────────┘
     ▲                             │                            │
     │                             │                            ▼
     │                             │                     ┌──────────┐
     │                             │                     │ Backend  │
     │                             │                     └──────────┘
     │                             │                            │
     │                             ▼                            │
     │                        ┌──────────┐                      │
     │                        │ authSlice│ ◀────────────────────┘
     │                        └──────────┘      Success
     │                             │
     │                             │ setCredentials()
     │                             ▼
     │                        ┌──────────┐
     │                        │  Store   │
     │                        └──────────┘
     │                             │
     │                             │ Persist
     │                             ▼
     │                        ┌──────────┐
     └────────────────────────│LocalStorage│
          Re-render           └──────────┘
```

### 2. Exercise Submission Flow

```
Component ──▶ useExercise ──▶ submitAnswer() ──▶ exerciseApi
                                                       │
                                                       ▼
                                                   Backend
                                                       │
                                                       ▼
Validation ◀── exerciseSlice ◀── setLastValidation() ◀─┘
    │
    ├──▶ If Correct ──▶ useProgress ──▶ trackCompletion() ──▶ progressSlice
    │
    └──▶ useToast ──▶ success/error message ──▶ uiSlice
```

### 3. State Selection Flow

```
Component ──▶ useAppSelector(selectAccuracyRate)
                      │
                      ▼
              Memoized Selector
                      │
                      ├──▶ Check Cache
                      │         │
                      │         ├─ Hit ──▶ Return Cached
                      │         │
                      │         └─ Miss ──▶ Compute
                      │                        │
                      ▼                        ▼
              Redux Store State ────▶ Calculate ──▶ Cache ──▶ Return
```

## State Persistence Strategy

### Persisted State
```
LocalStorage
├── auth (✓ Persisted)
│   ├── user
│   ├── accessToken
│   └── refreshToken
├── settings (✓ Persisted)
│   ├── notifications
│   ├── practice
│   ├── accessibility
│   └── language
└── ui (✓ Persisted)
    ├── theme
    └── sidebarOpen
```

### Non-Persisted State
```
Redux Store (Memory Only)
├── exercise (✗ Not Persisted)
│   └── Fetched fresh on load
├── progress (✗ Not Persisted)
│   └── Fetched from API
└── api (✗ Not Persisted)
    └── RTK Query cache
```

## Selector Memoization

### Example: Weak Areas Selector

```typescript
// Base selector
const selectStatsByType = (state) => state.progress.statistics?.by_type;

// Memoized derived selector
const selectWeakAreas = createSelector(
  [selectStatsByType],
  (byType) => {
    // Only recomputes when byType changes
    return Object.entries(byType)
      .filter(([_, stats]) => stats.accuracy < 70)
      .sort((a, b) => a.accuracy - b.accuracy);
  }
);

// Usage
const weakAreas = useAppSelector(selectWeakAreas);
// Re-renders ONLY when weakAreas actually changes
```

## Error Handling Flow

```
API Error ──▶ RTK Query ──▶ Error Middleware
                                  │
                                  ├──▶ 401 ──▶ logout() ──▶ authSlice
                                  │
                                  ├──▶ 403 ──▶ Toast "Access Denied"
                                  │
                                  ├──▶ 404 ──▶ Toast "Not Found"
                                  │
                                  ├──▶ 500 ──▶ Toast "Server Error"
                                  │
                                  └──▶ Network ──▶ Toast "Check Connection"
                                         │
                                         ▼
                                    uiSlice (addToast)
                                         │
                                         ▼
                                    Component Displays Toast
```

## Performance Optimization Strategies

### 1. Memoized Selectors
- Prevent unnecessary recalculations
- Cache computed values
- Only recompute when dependencies change

### 2. RTK Query Caching
- Automatic request deduplication
- Shared cache across components
- Configurable cache invalidation
- Background refetching

### 3. Code Splitting
- Lazy load slices
- Lazy load components
- Dynamic imports

### 4. Optimistic Updates
```typescript
const [updateProfile] = useUpdateProfileMutation();

// Optimistic update
updateProfile(newData, {
  optimisticUpdate: {
    update: (draft) => {
      draft.profile = newData;
    }
  }
});
```

## Type Safety Flow

```
Backend (Python)          Frontend (TypeScript)
─────────────            ─────────────────────

Pydantic Models    ──▶   TypeScript Types
    │                         │
    ▼                         ▼
UserResponse       ──▶   ApiUser interface
ExerciseResponse   ──▶   ApiExercise interface
ProgressResponse   ──▶   ApiProgress interface
    │                         │
    ▼                         ▼
API Endpoints      ──▶   RTK Query APIs
    │                         │
    ▼                         ▼
JSON Response      ──▶   Typed Response
    │                         │
    ▼                         ▼
                          Redux Store (Typed)
                              │
                              ▼
                          Selectors (Typed)
                              │
                              ▼
                          Components (Type-safe)
```

## Middleware Pipeline

```
Action Dispatched
      │
      ▼
┌──────────────┐
│ Logger       │ ──▶ Log action (dev only)
└──────────────┘
      │
      ▼
┌──────────────┐
│ RTK Query    │ ──▶ Handle API calls
└──────────────┘
      │
      ▼
┌──────────────┐
│ Error Handler│ ──▶ Handle errors, show toasts
└──────────────┘
      │
      ▼
┌──────────────┐
│ Reducers     │ ──▶ Update state
└──────────────┘
      │
      ▼
┌──────────────┐
│ Persist      │ ──▶ Save to localStorage
└──────────────┘
      │
      ▼
State Updated ──▶ Components Re-render
```

## Hook Composition Pattern

```typescript
// Complex hook built from simpler hooks
function useExercisePractice() {
  const { currentExercise, submitAnswer } = useExercise();
  const { trackCompletion } = useProgress();
  const { success, error } = useToast();
  const { settings } = useSettings();

  const handleSubmit = async () => {
    const validation = await submitAnswer();

    if (validation.is_correct) {
      success('Correct!');
      trackCompletion(true, validation.score);
    } else {
      error('Incorrect');
      trackCompletion(false, validation.score);
    }
  };

  return { currentExercise, handleSubmit };
}
```

## State Normalization

```typescript
// Normalized Exercise State
{
  exercises: {
    byId: {
      'ex1': { id: 'ex1', type: 'present', ... },
      'ex2': { id: 'ex2', type: 'imperfect', ... }
    },
    allIds: ['ex1', 'ex2'],
    currentId: 'ex1'
  }
}

// Benefits:
// - No duplication
// - Easy updates
// - Efficient lookups
// - Consistent data
```

## Best Practices Summary

1. **Always use hooks** - Never dispatch directly
2. **Use selectors** - For all state access
3. **Memoize expensive computations** - Use createSelector
4. **Handle errors globally** - Let middleware handle
5. **Type everything** - Full TypeScript coverage
6. **Test in isolation** - Hooks, selectors, reducers
7. **Keep slices focused** - Single responsibility
8. **Optimize re-renders** - Use memoization
9. **Persist wisely** - Only necessary state
10. **Monitor performance** - Use DevTools

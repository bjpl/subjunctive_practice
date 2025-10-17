# State Management Documentation

## Overview

This application uses **Redux Toolkit** and **RTK Query** for comprehensive state management, providing a robust, type-safe, and performant data flow architecture.

## Architecture

### Core Technologies

- **Redux Toolkit**: Modern Redux with reduced boilerplate
- **RTK Query**: Powerful data fetching and caching
- **Redux Persist**: State persistence to localStorage
- **Reselect**: Memoized selectors for performance
- **TypeScript**: Full type safety

## Directory Structure

```
frontend/src/
├── store/
│   ├── api/
│   │   ├── baseApi.ts          # Base RTK Query configuration
│   │   ├── authApi.ts          # Authentication endpoints
│   │   ├── exerciseApi.ts      # Exercise endpoints
│   │   ├── progressApi.ts      # Progress tracking endpoints
│   │   └── userApi.ts          # User profile endpoints
│   ├── slices/
│   │   ├── authSlice.ts        # Authentication state
│   │   ├── exerciseSlice.ts    # Exercise state
│   │   ├── progressSlice.ts    # Progress state
│   │   ├── uiSlice.ts          # UI state
│   │   └── settingsSlice.ts    # Settings state
│   ├── selectors/
│   │   ├── authSelectors.ts    # Auth selectors
│   │   ├── exerciseSelectors.ts # Exercise selectors
│   │   ├── progressSelectors.ts # Progress selectors
│   │   ├── uiSelectors.ts      # UI selectors
│   │   └── settingsSelectors.ts # Settings selectors
│   ├── middleware/
│   │   ├── errorMiddleware.ts  # Global error handling
│   │   └── loggerMiddleware.ts # Development logging
│   └── store.ts                # Store configuration
├── hooks/
│   ├── useAuth.ts              # Authentication hook
│   ├── useExercise.ts          # Exercise management hook
│   ├── useProgress.ts          # Progress tracking hook
│   ├── useSettings.ts          # Settings hook
│   ├── useToast.ts             # Toast notifications hook
│   └── useLocalStorage.ts      # LocalStorage hook
├── lib/
│   └── storage.ts              # Storage utilities
└── types/
    ├── index.ts                # Core types
    └── api.ts                  # API types
```

## Redux Slices

### 1. Auth Slice (`authSlice.ts`)

Manages authentication state and tokens.

**State:**
- `user`: Current user data
- `accessToken`: JWT access token
- `refreshToken`: JWT refresh token
- `isAuthenticated`: Authentication status
- `isLoading`: Loading state
- `error`: Error messages

**Actions:**
- `setCredentials`: Set user and tokens
- `updateTokens`: Update tokens after refresh
- `updateUser`: Update user data
- `logout`: Clear authentication state
- `setAuthLoading`: Set loading state
- `setAuthError`: Set error message

### 2. Exercise Slice (`exerciseSlice.ts`)

Manages exercise state and history.

**State:**
- `currentExercise`: Current exercise
- `exerciseHistory`: Exercise history (last 50)
- `currentAnswer`: User's current answer
- `isSubmitting`: Submission status
- `lastValidation`: Last answer validation
- `filters`: Exercise filters
- `availableTypes`: Available exercise types

**Actions:**
- `setCurrentExercise`: Set current exercise
- `setCurrentAnswer`: Update answer
- `addToHistory`: Add to history
- `updateFilters`: Update filters
- `setLastValidation`: Set validation result

### 3. Progress Slice (`progressSlice.ts`)

Tracks user progress and statistics.

**State:**
- `progress`: User progress metrics
- `statistics`: Detailed statistics
- `isLoading`: Loading state
- `error`: Error messages

**Actions:**
- `setProgress`: Set progress data
- `setStatistics`: Set statistics data
- `incrementExerciseCount`: Increment exercise count
- `incrementCorrectAnswers`: Increment correct answers
- `addExperiencePoints`: Add XP

### 4. UI Slice (`uiSlice.ts`)

Manages UI state and interactions.

**State:**
- `theme`: Theme (light/dark)
- `sidebarOpen`: Sidebar state
- `modals`: Modal states
- `toasts`: Toast notifications
- `isOnline`: Online status

**Actions:**
- `setTheme`: Set theme
- `toggleTheme`: Toggle theme
- `openModal/closeModal`: Control modals
- `addToast/removeToast`: Manage toasts

### 5. Settings Slice (`settingsSlice.ts`)

Manages user preferences and settings.

**State:**
- `settings`: User settings
  - `notifications`: Notification preferences
  - `practice`: Practice settings
  - `accessibility`: Accessibility options
  - `language`: Language preferences

**Actions:**
- `updateSettings`: Update all settings
- `updateNotificationSettings`: Update notifications
- `updatePracticeSettings`: Update practice settings
- `updateAccessibilitySettings`: Update accessibility
- `resetSettings`: Reset to defaults

## RTK Query APIs

### Auth API (`authApi.ts`)

**Endpoints:**
- `login`: User login
- `register`: User registration
- `refreshToken`: Refresh access token
- `getCurrentUser`: Get current user
- `logout`: Logout (client-side)

### Exercise API (`exerciseApi.ts`)

**Endpoints:**
- `getExercises`: Get exercises with filters
- `getExerciseById`: Get single exercise
- `submitAnswer`: Submit answer for validation
- `getExerciseTypes`: Get available types

### Progress API (`progressApi.ts`)

**Endpoints:**
- `getUserProgress`: Get user progress
- `getUserStatistics`: Get detailed statistics
- `resetProgress`: Reset progress (testing)

### User API (`userApi.ts`)

**Endpoints:**
- `getUserProfile`: Get user profile
- `updateSettings`: Update user settings
- `getSettings`: Get user settings
- `updateProfile`: Update user profile

## Custom Hooks

### useAuth()

```typescript
const {
  user,
  isAuthenticated,
  isLoading,
  login,
  register,
  logout,
  refreshAccessToken,
} = useAuth();
```

### useExercise()

```typescript
const {
  currentExercise,
  currentAnswer,
  lastValidation,
  updateAnswer,
  submitAnswer,
  getNextExercise,
} = useExercise();
```

### useProgress()

```typescript
const {
  progress,
  statistics,
  refreshProgress,
  trackExerciseCompletion,
} = useProgress();
```

### useSettings()

```typescript
const {
  settings,
  updateNotifications,
  updatePractice,
  updateAccessibility,
} = useSettings();
```

### useToast()

```typescript
const { success, error, info, warning } = useToast();

// Usage
success('Exercise completed!');
error('Failed to submit answer');
```

## Memoized Selectors

Selectors are memoized using `createSelector` from Reselect for optimal performance.

### Auth Selectors

```typescript
import { selectCurrentUser, selectIsAuthenticated } from '@/store/selectors';

const user = useAppSelector(selectCurrentUser);
const isAuth = useAppSelector(selectIsAuthenticated);
```

### Progress Selectors

```typescript
import {
  selectAccuracyRate,
  selectCurrentStreak,
  selectWeakAreas,
} from '@/store/selectors';

const accuracy = useAppSelector(selectAccuracyRate);
const streak = useAppSelector(selectCurrentStreak);
const weakAreas = useAppSelector(selectWeakAreas);
```

## Usage Examples

### 1. Authentication Flow

```typescript
import { useAuth } from '@/hooks';

function LoginForm() {
  const { login, isLoading, error } = useAuth();

  const handleLogin = async (credentials) => {
    try {
      await login(credentials);
      // User logged in, tokens stored
    } catch (err) {
      // Handle error
    }
  };

  return (
    // Form JSX
  );
}
```

### 2. Exercise Practice

```typescript
import { useExercise, useProgress, useToast } from '@/hooks';

function ExercisePage() {
  const {
    currentExercise,
    currentAnswer,
    updateAnswer,
    submitAnswer,
    getNextExercise,
  } = useExercise();

  const { trackExerciseCompletion } = useProgress();
  const { success, error } = useToast();

  const handleSubmit = async () => {
    try {
      const validation = await submitAnswer();

      if (validation.is_correct) {
        success('Correct! Well done!');
        trackExerciseCompletion(true, validation.score);
      } else {
        error('Incorrect. Try again!');
        trackExerciseCompletion(false, validation.score);
      }

      // Auto-advance to next exercise
      setTimeout(() => getNextExercise(), 2000);
    } catch (err) {
      error('Failed to submit answer');
    }
  };

  return (
    // Exercise UI
  );
}
```

### 3. Settings Management

```typescript
import { useSettings } from '@/hooks';

function SettingsPage() {
  const { settings, updatePractice, updateAccessibility } = useSettings();

  const handleDailyGoalChange = (goal: number) => {
    updatePractice({ dailyGoal: goal });
  };

  const handleFontSizeChange = (size: 'small' | 'medium' | 'large') => {
    updateAccessibility({ fontSize: size });
  };

  return (
    // Settings UI
  );
}
```

### 4. Progress Tracking

```typescript
import { useProgress } from '@/hooks';
import { selectWeakAreas, selectStrongAreas } from '@/store/selectors';

function ProgressDashboard() {
  const { progress, statistics } = useProgress();
  const weakAreas = useAppSelector(selectWeakAreas);
  const strongAreas = useAppSelector(selectStrongAreas);

  return (
    <div>
      <h2>Your Progress</h2>
      <p>Level: {progress?.level}</p>
      <p>XP: {progress?.experience_points}</p>
      <p>Accuracy: {progress?.accuracy_rate}%</p>
      <p>Streak: {progress?.current_streak} days</p>

      <h3>Areas to Improve</h3>
      {weakAreas.map(area => (
        <div key={area.type}>
          {area.type}: {area.accuracy}%
        </div>
      ))}
    </div>
  );
}
```

## Middleware

### Error Middleware

Automatically handles API errors:
- 401: Logout and show session expired message
- 403: Show access denied message
- 404: Show not found message
- 500: Show server error message
- Network errors: Show connection error

### Logger Middleware

Logs all actions in development mode for debugging.

## State Persistence

Redux Persist automatically saves state to localStorage:

**Persisted:**
- `auth`: User and tokens
- `settings`: User preferences
- `ui`: Theme and UI state

**Not Persisted:**
- `exercise`: Exercise state (fresh on reload)
- `progress`: Progress (fetched from API)
- `api`: RTK Query cache

## Performance Optimization

1. **Memoized Selectors**: Prevent unnecessary re-renders
2. **RTK Query Caching**: Automatic caching and invalidation
3. **Optimistic Updates**: Immediate UI updates
4. **Code Splitting**: Lazy load reducers
5. **DevTools**: Redux DevTools for debugging

## Best Practices

1. **Use Hooks**: Always use custom hooks instead of direct dispatch
2. **Type Safety**: Use TypeScript types for all state
3. **Selectors**: Use memoized selectors for derived state
4. **Error Handling**: Let error middleware handle API errors
5. **Persistence**: Only persist necessary state
6. **Testing**: Test hooks and selectors separately

## API Integration

Base URL: `http://localhost:8000/api/v1`

All authenticated requests automatically include:
- `Authorization: Bearer <token>` header
- Automatic token refresh on 401 errors

## Environment Variables

```env
REACT_APP_API_URL=http://localhost:8000/api/v1
```

## Troubleshooting

### State Not Persisting
- Check localStorage quota
- Verify persist configuration
- Clear browser cache

### API Errors
- Check network tab
- Verify token validity
- Check error middleware logs

### Performance Issues
- Use memoized selectors
- Check for unnecessary re-renders
- Use React DevTools Profiler

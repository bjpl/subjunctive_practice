/**
 * Example usage of state management hooks and selectors
 */

import React, { useEffect } from 'react';
import {
  useAuth,
  useExercise,
  useProgress,
  useSettings,
  useToast,
  useLocalStorage,
} from '../frontend/src/hooks';
import { useAppSelector } from '../frontend/src/hooks/useAppSelector';
import {
  selectCurrentUser,
  selectAccuracyRate,
  selectCurrentStreak,
  selectWeakAreas,
  selectTheme,
  selectDailyGoal,
} from '../frontend/src/store/selectors';

// Example 1: Authentication Component
export function AuthExample() {
  const { login, register, logout, isAuthenticated, isLoading, error } = useAuth();
  const user = useAppSelector(selectCurrentUser);

  const handleLogin = async () => {
    try {
      await login({
        username: 'testuser',
        password: 'password123',
      });
    } catch (err) {
      console.error('Login failed:', err);
    }
  };

  return (
    <div>
      {isAuthenticated ? (
        <div>
          <p>Welcome, {user?.username}!</p>
          <button onClick={logout}>Logout</button>
        </div>
      ) : (
        <button onClick={handleLogin} disabled={isLoading}>
          {isLoading ? 'Loading...' : 'Login'}
        </button>
      )}
      {error && <p className="error">{error}</p>}
    </div>
  );
}

// Example 2: Exercise Practice Component
export function ExercisePractice() {
  const {
    currentExercise,
    currentAnswer,
    lastValidation,
    updateAnswer,
    submitAnswer,
    getNextExercise,
    isSubmitting,
  } = useExercise();

  const { trackExerciseCompletion } = useProgress();
  const { success, error } = useToast();
  const { settings } = useSettings();

  useEffect(() => {
    // Load first exercise on mount
    if (!currentExercise) {
      getNextExercise();
    }
  }, [currentExercise, getNextExercise]);

  const handleSubmit = async () => {
    try {
      const validation = await submitAnswer();

      if (validation?.is_correct) {
        success('Correct! Excellent work!');
        trackExerciseCompletion(true, validation.score);

        // Auto-advance if enabled
        if (settings.practice.autoAdvance) {
          setTimeout(() => getNextExercise(), 2000);
        }
      } else {
        error(`Incorrect. The answer is: ${validation?.correct_answer}`);
        trackExerciseCompletion(false, validation?.score || 0);
      }
    } catch (err) {
      error('Failed to submit answer. Please try again.');
    }
  };

  if (!currentExercise) {
    return <div>Loading exercise...</div>;
  }

  return (
    <div className="exercise-container">
      <h2>Exercise #{currentExercise.id}</h2>
      <p className="prompt">{currentExercise.prompt}</p>

      <input
        type="text"
        value={currentAnswer}
        onChange={(e) => updateAnswer(e.target.value)}
        placeholder="Your answer..."
        disabled={isSubmitting}
      />

      <button onClick={handleSubmit} disabled={isSubmitting || !currentAnswer}>
        {isSubmitting ? 'Submitting...' : 'Submit'}
      </button>

      {lastValidation && (
        <div className={lastValidation.is_correct ? 'success' : 'error'}>
          <p>{lastValidation.feedback}</p>
          {settings.practice.showExplanations && lastValidation.explanation && (
            <p className="explanation">{lastValidation.explanation}</p>
          )}
        </div>
      )}

      {settings.practice.showHints && currentExercise.hints && (
        <div className="hints">
          <h4>Hints:</h4>
          <ul>
            {currentExercise.hints.map((hint, i) => (
              <li key={i}>{hint}</li>
            ))}
          </ul>
        </div>
      )}

      <button onClick={getNextExercise}>Skip to Next</button>
    </div>
  );
}

// Example 3: Progress Dashboard
export function ProgressDashboard() {
  const { progress, statistics, refreshProgress, refreshStatistics } = useProgress();
  const accuracy = useAppSelector(selectAccuracyRate);
  const streak = useAppSelector(selectCurrentStreak);
  const weakAreas = useAppSelector(selectWeakAreas);

  useEffect(() => {
    refreshProgress();
    refreshStatistics();
  }, [refreshProgress, refreshStatistics]);

  if (!progress) {
    return <div>Loading progress...</div>;
  }

  return (
    <div className="progress-dashboard">
      <h2>Your Progress</h2>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>Level</h3>
          <p className="stat-value">{progress.level}</p>
        </div>

        <div className="stat-card">
          <h3>Experience</h3>
          <p className="stat-value">{progress.experience_points} XP</p>
        </div>

        <div className="stat-card">
          <h3>Accuracy</h3>
          <p className="stat-value">{accuracy.toFixed(1)}%</p>
        </div>

        <div className="stat-card">
          <h3>Streak</h3>
          <p className="stat-value">{streak} days</p>
        </div>
      </div>

      <div className="exercises-summary">
        <h3>Exercises Completed</h3>
        <p>Total: {progress.total_exercises}</p>
        <p>Correct: {progress.correct_answers}</p>
        <p>Incorrect: {progress.incorrect_answers}</p>
      </div>

      {weakAreas.length > 0 && (
        <div className="weak-areas">
          <h3>Areas to Improve</h3>
          <ul>
            {weakAreas.map((area) => (
              <li key={area.type}>
                {area.type.replace('_', ' ')}: {area.accuracy.toFixed(1)}% accuracy
              </li>
            ))}
          </ul>
        </div>
      )}

      {statistics?.learning_insights && (
        <div className="insights">
          <h3>Learning Insights</h3>
          <ul>
            {statistics.learning_insights.map((insight, i) => (
              <li key={i}>{insight}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

// Example 4: Settings Panel
export function SettingsPanel() {
  const {
    settings,
    updateNotifications,
    updatePractice,
    updateAccessibility,
    updateLanguage,
    resetToDefaults,
  } = useSettings();

  const theme = useAppSelector(selectTheme);
  const dailyGoal = useAppSelector(selectDailyGoal);

  return (
    <div className="settings-panel">
      <h2>Settings</h2>

      <section>
        <h3>Notifications</h3>
        <label>
          <input
            type="checkbox"
            checked={settings.notifications.email}
            onChange={(e) =>
              updateNotifications({ email: e.target.checked })
            }
          />
          Email Notifications
        </label>
        <label>
          <input
            type="checkbox"
            checked={settings.notifications.streakReminders}
            onChange={(e) =>
              updateNotifications({ streakReminders: e.target.checked })
            }
          />
          Streak Reminders
        </label>
      </section>

      <section>
        <h3>Practice Settings</h3>
        <label>
          Daily Goal:
          <input
            type="number"
            value={dailyGoal}
            onChange={(e) =>
              updatePractice({ dailyGoal: parseInt(e.target.value) })
            }
            min="1"
            max="100"
          />
        </label>
        <label>
          <input
            type="checkbox"
            checked={settings.practice.autoAdvance}
            onChange={(e) =>
              updatePractice({ autoAdvance: e.target.checked })
            }
          />
          Auto-advance to next exercise
        </label>
        <label>
          <input
            type="checkbox"
            checked={settings.practice.showHints}
            onChange={(e) =>
              updatePractice({ showHints: e.target.checked })
            }
          />
          Show hints
        </label>
      </section>

      <section>
        <h3>Accessibility</h3>
        <label>
          Font Size:
          <select
            value={settings.accessibility.fontSize}
            onChange={(e) =>
              updateAccessibility({
                fontSize: e.target.value as 'small' | 'medium' | 'large',
              })
            }
          >
            <option value="small">Small</option>
            <option value="medium">Medium</option>
            <option value="large">Large</option>
          </select>
        </label>
        <label>
          <input
            type="checkbox"
            checked={settings.accessibility.highContrast}
            onChange={(e) =>
              updateAccessibility({ highContrast: e.target.checked })
            }
          />
          High Contrast
        </label>
        <label>
          <input
            type="checkbox"
            checked={settings.accessibility.reduceMotion}
            onChange={(e) =>
              updateAccessibility({ reduceMotion: e.target.checked })
            }
          />
          Reduce Motion
        </label>
      </section>

      <button onClick={resetToDefaults}>Reset to Defaults</button>
    </div>
  );
}

// Example 5: Toast Notifications
export function ToastExample() {
  const { success, error, info, warning } = useToast();

  return (
    <div className="toast-examples">
      <button onClick={() => success('Operation successful!')}>
        Show Success
      </button>
      <button onClick={() => error('Something went wrong!')}>
        Show Error
      </button>
      <button onClick={() => info('Here is some information')}>
        Show Info
      </button>
      <button onClick={() => warning('Warning: Check this!')}>
        Show Warning
      </button>
    </div>
  );
}

// Example 6: Local Storage Hook
export function LocalStorageExample() {
  const [savedExercises, setSavedExercises, removeSavedExercises] =
    useLocalStorage<string[]>('saved_exercises', []);

  const addExercise = (id: string) => {
    setSavedExercises([...savedExercises, id]);
  };

  const clearAll = () => {
    removeSavedExercises();
  };

  return (
    <div>
      <h3>Saved Exercises</h3>
      <ul>
        {savedExercises.map((id) => (
          <li key={id}>{id}</li>
        ))}
      </ul>
      <button onClick={() => addExercise(`ex-${Date.now()}`)}>
        Add Exercise
      </button>
      <button onClick={clearAll}>Clear All</button>
    </div>
  );
}

// Example 7: Complete Application
export function App() {
  const { isAuthenticated } = useAuth();
  const theme = useAppSelector(selectTheme);

  return (
    <div className={`app ${theme}`}>
      {!isAuthenticated ? (
        <AuthExample />
      ) : (
        <>
          <SettingsPanel />
          <ExercisePractice />
          <ProgressDashboard />
        </>
      )}
      <ToastExample />
    </div>
  );
}

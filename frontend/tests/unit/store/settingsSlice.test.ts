import settingsReducer, {
  updateUserPreferences,
  setTheme,
  setFontSize,
  setReducedMotion,
  setLanguage,
  setDifficulty,
  updateSessionSettings,
  setSessionDifficulty,
  setTimeLimit,
  setHintsEnabled,
  setFeedbackType,
  setExerciseCount,
  fetchSettingsStart,
  fetchSettingsSuccess,
  fetchSettingsFailure,
  clearError,
  resetSettings,
} from '@/store/slices/settingsSlice';
import type { UserPreferences, SessionSettings } from '@/types';

describe('settingsSlice', () => {
  describe('initial state', () => {
    it('should have correct initial state', () => {
      const state = settingsReducer(undefined, { type: 'unknown' });

      expect(state).toEqual({
        userPreferences: {
          theme: 'light',
          fontSize: 'medium',
          reducedMotion: false,
          language: 'en',
          difficulty: 'beginner',
        },
        sessionSettings: {
          difficulty: 'beginner',
          timeLimit: undefined,
          hintsEnabled: true,
          feedbackType: 'immediate',
          exerciseCount: 10,
        },
        isLoading: false,
        error: null,
      });
    });
  });

  describe('updateUserPreferences', () => {
    it('should update partial preferences', () => {
      const state = settingsReducer(
        undefined,
        updateUserPreferences({ theme: 'dark', fontSize: 'large' })
      );

      expect(state.userPreferences.theme).toBe('dark');
      expect(state.userPreferences.fontSize).toBe('large');
      expect(state.userPreferences.language).toBe('en'); // unchanged
    });

    it('should merge with existing preferences', () => {
      const initialState = settingsReducer(undefined, { type: 'unknown' });
      const state = settingsReducer(
        initialState,
        updateUserPreferences({ reducedMotion: true })
      );

      expect(state.userPreferences).toEqual({
        theme: 'light',
        fontSize: 'medium',
        reducedMotion: true,
        language: 'en',
        difficulty: 'beginner',
      });
    });
  });

  describe('setTheme', () => {
    it('should set theme to light', () => {
      const state = settingsReducer(undefined, setTheme('light'));
      expect(state.userPreferences.theme).toBe('light');
    });

    it('should set theme to dark', () => {
      const state = settingsReducer(undefined, setTheme('dark'));
      expect(state.userPreferences.theme).toBe('dark');
    });

    it('should set theme to high-contrast', () => {
      const state = settingsReducer(undefined, setTheme('high-contrast'));
      expect(state.userPreferences.theme).toBe('high-contrast');
    });
  });

  describe('setFontSize', () => {
    it('should set font size to small', () => {
      const state = settingsReducer(undefined, setFontSize('small'));
      expect(state.userPreferences.fontSize).toBe('small');
    });

    it('should set font size to xl', () => {
      const state = settingsReducer(undefined, setFontSize('xl'));
      expect(state.userPreferences.fontSize).toBe('xl');
    });
  });

  describe('setReducedMotion', () => {
    it('should enable reduced motion', () => {
      const state = settingsReducer(undefined, setReducedMotion(true));
      expect(state.userPreferences.reducedMotion).toBe(true);
    });

    it('should disable reduced motion', () => {
      const state = settingsReducer(undefined, setReducedMotion(false));
      expect(state.userPreferences.reducedMotion).toBe(false);
    });
  });

  describe('setLanguage', () => {
    it('should set language to English', () => {
      const state = settingsReducer(undefined, setLanguage('en'));
      expect(state.userPreferences.language).toBe('en');
    });

    it('should set language to Spanish', () => {
      const state = settingsReducer(undefined, setLanguage('es'));
      expect(state.userPreferences.language).toBe('es');
    });
  });

  describe('setDifficulty', () => {
    it('should set difficulty to beginner', () => {
      const state = settingsReducer(undefined, setDifficulty('beginner'));
      expect(state.userPreferences.difficulty).toBe('beginner');
    });

    it('should set difficulty to intermediate', () => {
      const state = settingsReducer(undefined, setDifficulty('intermediate'));
      expect(state.userPreferences.difficulty).toBe('intermediate');
    });

    it('should set difficulty to advanced', () => {
      const state = settingsReducer(undefined, setDifficulty('advanced'));
      expect(state.userPreferences.difficulty).toBe('advanced');
    });
  });

  describe('updateSessionSettings', () => {
    it('should update partial session settings', () => {
      const state = settingsReducer(
        undefined,
        updateSessionSettings({ difficulty: 'advanced', exerciseCount: 20 })
      );

      expect(state.sessionSettings.difficulty).toBe('advanced');
      expect(state.sessionSettings.exerciseCount).toBe(20);
      expect(state.sessionSettings.hintsEnabled).toBe(true); // unchanged
    });

    it('should merge with existing settings', () => {
      const initialState = settingsReducer(undefined, { type: 'unknown' });
      const state = settingsReducer(
        initialState,
        updateSessionSettings({ timeLimit: 60000 })
      );

      expect(state.sessionSettings).toEqual({
        difficulty: 'beginner',
        timeLimit: 60000,
        hintsEnabled: true,
        feedbackType: 'immediate',
        exerciseCount: 10,
      });
    });
  });

  describe('setSessionDifficulty', () => {
    it('should set session difficulty', () => {
      const state = settingsReducer(undefined, setSessionDifficulty('intermediate'));
      expect(state.sessionSettings.difficulty).toBe('intermediate');
    });
  });

  describe('setTimeLimit', () => {
    it('should set time limit', () => {
      const state = settingsReducer(undefined, setTimeLimit(30000));
      expect(state.sessionSettings.timeLimit).toBe(30000);
    });

    it('should allow undefined time limit', () => {
      const initialState = settingsReducer(undefined, setTimeLimit(60000));
      const state = settingsReducer(initialState, setTimeLimit(undefined));
      expect(state.sessionSettings.timeLimit).toBeUndefined();
    });
  });

  describe('setHintsEnabled', () => {
    it('should enable hints', () => {
      const state = settingsReducer(undefined, setHintsEnabled(true));
      expect(state.sessionSettings.hintsEnabled).toBe(true);
    });

    it('should disable hints', () => {
      const state = settingsReducer(undefined, setHintsEnabled(false));
      expect(state.sessionSettings.hintsEnabled).toBe(false);
    });
  });

  describe('setFeedbackType', () => {
    it('should set feedback type to immediate', () => {
      const state = settingsReducer(undefined, setFeedbackType('immediate'));
      expect(state.sessionSettings.feedbackType).toBe('immediate');
    });

    it('should set feedback type to end', () => {
      const state = settingsReducer(undefined, setFeedbackType('end'));
      expect(state.sessionSettings.feedbackType).toBe('end');
    });
  });

  describe('setExerciseCount', () => {
    it('should set exercise count', () => {
      const state = settingsReducer(undefined, setExerciseCount(25));
      expect(state.sessionSettings.exerciseCount).toBe(25);
    });

    it('should update from default', () => {
      const initialState = settingsReducer(undefined, { type: 'unknown' });
      expect(initialState.sessionSettings.exerciseCount).toBe(10);

      const state = settingsReducer(initialState, setExerciseCount(15));
      expect(state.sessionSettings.exerciseCount).toBe(15);
    });
  });

  describe('fetchSettingsStart', () => {
    it('should set loading state and clear errors', () => {
      const initialState = {
        ...settingsReducer(undefined, { type: 'unknown' }),
        error: 'previous error',
      };

      const state = settingsReducer(initialState, fetchSettingsStart());

      expect(state.isLoading).toBe(true);
      expect(state.error).toBeNull();
    });
  });

  describe('fetchSettingsSuccess', () => {
    it('should update user preferences', () => {
      const initialState = {
        ...settingsReducer(undefined, { type: 'unknown' }),
        isLoading: true,
      };

      const state = settingsReducer(
        initialState,
        fetchSettingsSuccess({
          userPreferences: { theme: 'dark', fontSize: 'large' },
        })
      );

      expect(state.isLoading).toBe(false);
      expect(state.userPreferences.theme).toBe('dark');
      expect(state.userPreferences.fontSize).toBe('large');
    });

    it('should update session settings', () => {
      const initialState = {
        ...settingsReducer(undefined, { type: 'unknown' }),
        isLoading: true,
      };

      const state = settingsReducer(
        initialState,
        fetchSettingsSuccess({
          sessionSettings: { difficulty: 'advanced', exerciseCount: 20 },
        })
      );

      expect(state.isLoading).toBe(false);
      expect(state.sessionSettings.difficulty).toBe('advanced');
      expect(state.sessionSettings.exerciseCount).toBe(20);
    });

    it('should update both preferences and settings', () => {
      const initialState = {
        ...settingsReducer(undefined, { type: 'unknown' }),
        isLoading: true,
      };

      const state = settingsReducer(
        initialState,
        fetchSettingsSuccess({
          userPreferences: { theme: 'dark' },
          sessionSettings: { difficulty: 'advanced' },
        })
      );

      expect(state.isLoading).toBe(false);
      expect(state.userPreferences.theme).toBe('dark');
      expect(state.sessionSettings.difficulty).toBe('advanced');
    });

    it('should merge with existing values', () => {
      const initialState = {
        ...settingsReducer(undefined, { type: 'unknown' }),
        isLoading: true,
      };

      const state = settingsReducer(
        initialState,
        fetchSettingsSuccess({
          userPreferences: { theme: 'dark' },
        })
      );

      expect(state.userPreferences.language).toBe('en'); // unchanged
      expect(state.userPreferences.difficulty).toBe('beginner'); // unchanged
    });
  });

  describe('fetchSettingsFailure', () => {
    it('should set error and stop loading', () => {
      const initialState = {
        ...settingsReducer(undefined, { type: 'unknown' }),
        isLoading: true,
      };

      const state = settingsReducer(
        initialState,
        fetchSettingsFailure('Failed to load settings')
      );

      expect(state.isLoading).toBe(false);
      expect(state.error).toBe('Failed to load settings');
    });
  });

  describe('clearError', () => {
    it('should clear error', () => {
      const initialState = {
        ...settingsReducer(undefined, { type: 'unknown' }),
        error: 'Some error',
      };

      const state = settingsReducer(initialState, clearError());

      expect(state.error).toBeNull();
    });
  });

  describe('resetSettings', () => {
    it('should reset to initial state', () => {
      const modifiedState = {
        userPreferences: {
          theme: 'dark' as const,
          fontSize: 'xl' as const,
          reducedMotion: true,
          language: 'es' as const,
          difficulty: 'advanced' as const,
        },
        sessionSettings: {
          difficulty: 'advanced' as const,
          timeLimit: 60000,
          hintsEnabled: false,
          feedbackType: 'end' as const,
          exerciseCount: 25,
        },
        isLoading: true,
        error: 'some error',
      };

      const state = settingsReducer(modifiedState, resetSettings());

      expect(state).toEqual({
        userPreferences: {
          theme: 'light',
          fontSize: 'medium',
          reducedMotion: false,
          language: 'en',
          difficulty: 'beginner',
        },
        sessionSettings: {
          difficulty: 'beginner',
          timeLimit: undefined,
          hintsEnabled: true,
          feedbackType: 'immediate',
          exerciseCount: 10,
        },
        isLoading: false,
        error: null,
      });
    });
  });
});

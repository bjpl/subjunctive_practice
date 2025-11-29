/**
 * User settings hook
 */

import { useCallback } from 'react';
import { useAppSelector } from './useAppSelector';
import { useAppDispatch } from './useAppDispatch';
import {
  updateUserPreferences,
  updateSessionSettings,
  resetSettings,
} from '../store/slices/settingsSlice';
import type { UserSettings } from '../types/api';

export const useSettings = () => {
  const dispatch = useAppDispatch();

  // Selectors
  const userPreferences = useAppSelector((state) => state.settings.userPreferences);
  const sessionSettings = useAppSelector((state) => state.settings.sessionSettings);
  const isLoading = useAppSelector((state) => state.settings.isLoading);
  const error = useAppSelector((state) => state.settings.error);

  // Update all settings
  const updateAllSettings = useCallback(
    (newSettings: Partial<UserSettings>) => {
      // Update user preferences and session settings from the new settings
      if (newSettings) {
        dispatch(updateUserPreferences(newSettings as any));
        dispatch(updateSessionSettings(newSettings as any));
      }
    },
    [dispatch]
  );

  // Update notification settings
  const updateNotifications = useCallback(
    (notifications: any) => {
      dispatch(updateUserPreferences(notifications));
    },
    [dispatch]
  );

  // Update practice settings
  const updatePractice = useCallback(
    (practice: any) => {
      dispatch(updateSessionSettings(practice));
    },
    [dispatch]
  );

  // Update accessibility settings
  const updateAccessibility = useCallback(
    (accessibility: any) => {
      dispatch(updateUserPreferences(accessibility));
    },
    [dispatch]
  );

  // Update language settings
  const updateLanguage = useCallback(
    (language: any) => {
      dispatch(updateUserPreferences(language));
    },
    [dispatch]
  );

  // Reset to defaults
  const resetToDefaults = useCallback(() => {
    dispatch(resetSettings());
  }, [dispatch]);

  // Map settingsSlice state to UserSettings structure
  const settings: UserSettings = {
    notifications: {
      email: false,
      push: false,
      streakReminders: false,
    },
    practice: {
      dailyGoal: sessionSettings.exerciseCount || 10,
      autoAdvance: true,
      showHints: sessionSettings.hintsEnabled,
      showExplanations: sessionSettings.feedbackType !== 'minimal',
    },
    accessibility: {
      fontSize: userPreferences.fontSize,
      highContrast: false,
      reduceMotion: userPreferences.reducedMotion,
    },
    language: {
      interface: userPreferences.language,
      practice: userPreferences.language,
    },
  };

  return {
    // State
    settings,
    userPreferences,
    sessionSettings,
    isLoading,
    error,

    // Actions
    updateAllSettings,
    updateNotifications,
    updatePractice,
    updateAccessibility,
    updateLanguage,
    resetToDefaults,
  };
};

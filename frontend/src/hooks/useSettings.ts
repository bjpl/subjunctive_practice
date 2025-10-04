/**
 * User settings hook
 */

import { useCallback } from 'react';
import { useAppSelector } from './useAppSelector';
import { useAppDispatch } from './useAppDispatch';
import {
  updateSettings,
  updateNotificationSettings,
  updatePracticeSettings,
  updateAccessibilitySettings,
  updateLanguageSettings,
  resetSettings,
} from '../store/slices/settingsSlice';
import type { UserSettings } from '../types/api';

export const useSettings = () => {
  const dispatch = useAppDispatch();

  // Selectors
  const settings = useAppSelector((state) => state.settings.settings);
  const isLoading = useAppSelector((state) => state.settings.isLoading);
  const error = useAppSelector((state) => state.settings.error);

  // Update all settings
  const updateAllSettings = useCallback(
    (newSettings: Partial<UserSettings>) => {
      dispatch(updateSettings(newSettings));
    },
    [dispatch]
  );

  // Update notification settings
  const updateNotifications = useCallback(
    (notifications: Partial<UserSettings['notifications']>) => {
      dispatch(updateNotificationSettings(notifications));
    },
    [dispatch]
  );

  // Update practice settings
  const updatePractice = useCallback(
    (practice: Partial<UserSettings['practice']>) => {
      dispatch(updatePracticeSettings(practice));
    },
    [dispatch]
  );

  // Update accessibility settings
  const updateAccessibility = useCallback(
    (accessibility: Partial<UserSettings['accessibility']>) => {
      dispatch(updateAccessibilitySettings(accessibility));
    },
    [dispatch]
  );

  // Update language settings
  const updateLanguage = useCallback(
    (language: Partial<UserSettings['language']>) => {
      dispatch(updateLanguageSettings(language));
    },
    [dispatch]
  );

  // Reset to defaults
  const resetToDefaults = useCallback(() => {
    dispatch(resetSettings());
  }, [dispatch]);

  return {
    // State
    settings,
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

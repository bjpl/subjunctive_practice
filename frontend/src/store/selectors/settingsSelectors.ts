/**
 * Memoized selectors for settings state
 */

import { createSelector } from '@reduxjs/toolkit';
import type { RootState } from '../store';

// Base selectors
const selectSettingsState = (state: RootState) => state.settings;

// Memoized selectors
export const selectSettings = createSelector(
  [selectSettingsState],
  (settings) => settings.settings
);

export const selectSettingsLoading = createSelector(
  [selectSettingsState],
  (settings) => settings.isLoading
);

export const selectSettingsError = createSelector(
  [selectSettingsState],
  (settings) => settings.error
);

// Notification settings
export const selectNotificationSettings = createSelector(
  [selectSettings],
  (settings) => settings.notifications
);

export const selectEmailNotifications = createSelector(
  [selectNotificationSettings],
  (notifications) => notifications.email
);

export const selectPushNotifications = createSelector(
  [selectNotificationSettings],
  (notifications) => notifications.push
);

export const selectStreakReminders = createSelector(
  [selectNotificationSettings],
  (notifications) => notifications.streakReminders
);

// Practice settings
export const selectPracticeSettings = createSelector(
  [selectSettings],
  (settings) => settings.practice
);

export const selectDailyGoal = createSelector(
  [selectPracticeSettings],
  (practice) => practice.dailyGoal
);

export const selectAutoAdvance = createSelector(
  [selectPracticeSettings],
  (practice) => practice.autoAdvance
);

export const selectShowHints = createSelector(
  [selectPracticeSettings],
  (practice) => practice.showHints
);

export const selectShowExplanations = createSelector(
  [selectPracticeSettings],
  (practice) => practice.showExplanations
);

// Accessibility settings
export const selectAccessibilitySettings = createSelector(
  [selectSettings],
  (settings) => settings.accessibility
);

export const selectFontSize = createSelector(
  [selectAccessibilitySettings],
  (accessibility) => accessibility.fontSize
);

export const selectHighContrast = createSelector(
  [selectAccessibilitySettings],
  (accessibility) => accessibility.highContrast
);

export const selectReduceMotion = createSelector(
  [selectAccessibilitySettings],
  (accessibility) => accessibility.reduceMotion
);

// Language settings
export const selectLanguageSettings = createSelector(
  [selectSettings],
  (settings) => settings.language
);

export const selectInterfaceLanguage = createSelector(
  [selectLanguageSettings],
  (language) => language.interface
);

export const selectPracticeLanguage = createSelector(
  [selectLanguageSettings],
  (language) => language.practice
);

// Font size CSS class
export const selectFontSizeClass = createSelector(
  [selectFontSize],
  (fontSize) => {
    const sizeMap = {
      small: 'text-sm',
      medium: 'text-base',
      large: 'text-lg',
    };
    return sizeMap[fontSize] || 'text-base';
  }
);

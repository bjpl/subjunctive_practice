/**
 * User settings state slice
 */

import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { SettingsState, UserSettings } from '../../types';
import { getStorageItem, setStorageItem, StorageKeys } from '../../lib/storage';

const defaultSettings: UserSettings = {
  notifications: {
    email: true,
    push: false,
    streakReminders: true,
  },
  practice: {
    dailyGoal: 10,
    autoAdvance: true,
    showHints: true,
    showExplanations: true,
  },
  accessibility: {
    fontSize: 'medium',
    highContrast: false,
    reduceMotion: false,
  },
  language: {
    interface: 'en',
    practice: 'es',
  },
};

const initialState: SettingsState = {
  settings: getStorageItem<UserSettings>(StorageKeys.SETTINGS, defaultSettings),
  isLoading: false,
  error: null,
};

const settingsSlice = createSlice({
  name: 'settings',
  initialState,
  reducers: {
    setSettings: (state, action: PayloadAction<UserSettings>) => {
      state.settings = action.payload;
      setStorageItem(StorageKeys.SETTINGS, action.payload);
      state.error = null;
    },

    updateSettings: (state, action: PayloadAction<Partial<UserSettings>>) => {
      state.settings = { ...state.settings, ...action.payload };
      setStorageItem(StorageKeys.SETTINGS, state.settings);
    },

    updateNotificationSettings: (
      state,
      action: PayloadAction<Partial<UserSettings['notifications']>>
    ) => {
      state.settings.notifications = {
        ...state.settings.notifications,
        ...action.payload,
      };
      setStorageItem(StorageKeys.SETTINGS, state.settings);
    },

    updatePracticeSettings: (
      state,
      action: PayloadAction<Partial<UserSettings['practice']>>
    ) => {
      state.settings.practice = {
        ...state.settings.practice,
        ...action.payload,
      };
      setStorageItem(StorageKeys.SETTINGS, state.settings);
    },

    updateAccessibilitySettings: (
      state,
      action: PayloadAction<Partial<UserSettings['accessibility']>>
    ) => {
      state.settings.accessibility = {
        ...state.settings.accessibility,
        ...action.payload,
      };
      setStorageItem(StorageKeys.SETTINGS, state.settings);
    },

    updateLanguageSettings: (
      state,
      action: PayloadAction<Partial<UserSettings['language']>>
    ) => {
      state.settings.language = {
        ...state.settings.language,
        ...action.payload,
      };
      setStorageItem(StorageKeys.SETTINGS, state.settings);
    },

    resetSettings: (state) => {
      state.settings = defaultSettings;
      setStorageItem(StorageKeys.SETTINGS, defaultSettings);
    },

    setSettingsLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },

    setSettingsError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
      state.isLoading = false;
    },

    clearSettingsError: (state) => {
      state.error = null;
    },
  },
});

export const {
  setSettings,
  updateSettings,
  updateNotificationSettings,
  updatePracticeSettings,
  updateAccessibilitySettings,
  updateLanguageSettings,
  resetSettings,
  setSettingsLoading,
  setSettingsError,
  clearSettingsError,
} = settingsSlice.actions;

export default settingsSlice.reducer;

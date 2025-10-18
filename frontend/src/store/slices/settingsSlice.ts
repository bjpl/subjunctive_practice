import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import type { UserPreferences, SessionSettings } from "@/types";

interface SettingsState {
  userPreferences: UserPreferences;
  sessionSettings: SessionSettings;
  isLoading: boolean;
  error: string | null;
}

const initialState: SettingsState = {
  userPreferences: {
    theme: "light",
    fontSize: "medium",
    reducedMotion: false,
    language: "en",
    difficulty: "beginner",
  },
  sessionSettings: {
    difficulty: "beginner",
    timeLimit: undefined,
    hintsEnabled: true,
    feedbackType: "immediate",
    exerciseCount: 10,
  },
  isLoading: false,
  error: null,
};

const settingsSlice = createSlice({
  name: "settings",
  initialState,
  reducers: {
    updateUserPreferences: (state, action: PayloadAction<Partial<UserPreferences>>) => {
      state.userPreferences = { ...state.userPreferences, ...action.payload };
    },
    setTheme: (state, action: PayloadAction<UserPreferences["theme"]>) => {
      state.userPreferences.theme = action.payload;
    },
    setFontSize: (state, action: PayloadAction<UserPreferences["fontSize"]>) => {
      state.userPreferences.fontSize = action.payload;
    },
    setReducedMotion: (state, action: PayloadAction<boolean>) => {
      state.userPreferences.reducedMotion = action.payload;
    },
    setLanguage: (state, action: PayloadAction<UserPreferences["language"]>) => {
      state.userPreferences.language = action.payload;
    },
    setDifficulty: (state, action: PayloadAction<UserPreferences["difficulty"]>) => {
      state.userPreferences.difficulty = action.payload;
    },
    updateSessionSettings: (state, action: PayloadAction<Partial<SessionSettings>>) => {
      state.sessionSettings = { ...state.sessionSettings, ...action.payload };
    },
    setSessionDifficulty: (state, action: PayloadAction<SessionSettings["difficulty"]>) => {
      state.sessionSettings.difficulty = action.payload;
    },
    setTimeLimit: (state, action: PayloadAction<number | undefined>) => {
      state.sessionSettings.timeLimit = action.payload;
    },
    setHintsEnabled: (state, action: PayloadAction<boolean>) => {
      state.sessionSettings.hintsEnabled = action.payload;
    },
    setFeedbackType: (state, action: PayloadAction<SessionSettings["feedbackType"]>) => {
      state.sessionSettings.feedbackType = action.payload;
    },
    setExerciseCount: (state, action: PayloadAction<number>) => {
      state.sessionSettings.exerciseCount = action.payload;
    },
    fetchSettingsStart: (state) => {
      state.isLoading = true;
      state.error = null;
    },
    fetchSettingsSuccess: (
      state,
      action: PayloadAction<{
        userPreferences?: Partial<UserPreferences>;
        sessionSettings?: Partial<SessionSettings>;
      }>
    ) => {
      state.isLoading = false;
      if (action.payload.userPreferences) {
        state.userPreferences = { ...state.userPreferences, ...action.payload.userPreferences };
      }
      if (action.payload.sessionSettings) {
        state.sessionSettings = { ...state.sessionSettings, ...action.payload.sessionSettings };
      }
    },
    fetchSettingsFailure: (state, action: PayloadAction<string>) => {
      state.isLoading = false;
      state.error = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },
    resetSettings: () => initialState,
  },
});

export const {
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
} = settingsSlice.actions;

export default settingsSlice.reducer;

/**
 * Progress tracking state slice
 */

import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { ProgressState, Progress, Statistics } from '../../types';

const initialState: ProgressState = {
  progress: null,
  statistics: null,
  isLoading: false,
  error: null,
};

const progressSlice = createSlice({
  name: 'progress',
  initialState,
  reducers: {
    setProgress: (state, action: PayloadAction<Progress>) => {
      state.progress = action.payload;
      state.error = null;
    },

    setStatistics: (state, action: PayloadAction<Statistics>) => {
      state.statistics = action.payload;
      state.error = null;
    },

    updateProgress: (state, action: PayloadAction<Partial<Progress>>) => {
      if (state.progress) {
        state.progress = { ...state.progress, ...action.payload };
      }
    },

    incrementExerciseCount: (state) => {
      if (state.progress) {
        state.progress.total_exercises += 1;
      }
    },

    incrementCorrectAnswers: (state) => {
      if (state.progress) {
        state.progress.correct_answers += 1;
        state.progress.accuracy_rate =
          (state.progress.correct_answers / state.progress.total_exercises) * 100;
      }
    },

    incrementIncorrectAnswers: (state) => {
      if (state.progress) {
        state.progress.incorrect_answers += 1;
        state.progress.accuracy_rate =
          (state.progress.correct_answers / state.progress.total_exercises) * 100;
      }
    },

    updateStreak: (state, action: PayloadAction<{ current: number; best: number }>) => {
      if (state.progress) {
        state.progress.current_streak = action.payload.current;
        state.progress.best_streak = action.payload.best;
      }
    },

    addExperiencePoints: (state, action: PayloadAction<number>) => {
      if (state.progress) {
        state.progress.experience_points += action.payload;
        // Calculate new level
        const newLevel = Math.min(
          10,
          Math.floor(Math.sqrt(state.progress.experience_points / 100)) + 1
        );
        state.progress.level = newLevel;
      }
    },

    setProgressLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },

    setProgressError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
      state.isLoading = false;
    },

    clearProgressError: (state) => {
      state.error = null;
    },

    resetProgress: (state) => {
      state.progress = null;
      state.statistics = null;
      state.error = null;
    },
  },
});

export const {
  setProgress,
  setStatistics,
  updateProgress,
  incrementExerciseCount,
  incrementCorrectAnswers,
  incrementIncorrectAnswers,
  updateStreak,
  addExperiencePoints,
  setProgressLoading,
  setProgressError,
  clearProgressError,
  resetProgress,
} = progressSlice.actions;

export default progressSlice.reducer;

/**
 * Exercise state slice
 */

import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { ExerciseState, Exercise, AnswerValidation, ExerciseFilters } from '../../types';
import { getStorageItem, setStorageItem, StorageKeys } from '../../lib/storage';

const initialState: ExerciseState = {
  currentExercise: getStorageItem<Exercise | null>(StorageKeys.LAST_EXERCISE, null),
  exerciseHistory: getStorageItem<Exercise[]>(StorageKeys.EXERCISE_HISTORY, []),
  currentAnswer: '',
  isSubmitting: false,
  lastValidation: null,
  filters: {
    limit: 10,
    random_order: true,
  },
  availableTypes: [],
  isLoading: false,
  error: null,
};

const exerciseSlice = createSlice({
  name: 'exercise',
  initialState,
  reducers: {
    setCurrentExercise: (state, action: PayloadAction<Exercise | null>) => {
      state.currentExercise = action.payload;
      if (action.payload) {
        setStorageItem(StorageKeys.LAST_EXERCISE, action.payload);
      }
    },

    setCurrentAnswer: (state, action: PayloadAction<string>) => {
      state.currentAnswer = action.payload;
    },

    clearCurrentAnswer: (state) => {
      state.currentAnswer = '';
    },

    addToHistory: (state, action: PayloadAction<Exercise>) => {
      state.exerciseHistory = [action.payload, ...state.exerciseHistory].slice(0, 50); // Keep last 50
      setStorageItem(StorageKeys.EXERCISE_HISTORY, state.exerciseHistory);
    },

    clearHistory: (state) => {
      state.exerciseHistory = [];
      setStorageItem(StorageKeys.EXERCISE_HISTORY, []);
    },

    setSubmitting: (state, action: PayloadAction<boolean>) => {
      state.isSubmitting = action.payload;
    },

    setLastValidation: (state, action: PayloadAction<AnswerValidation | null>) => {
      state.lastValidation = action.payload;
    },

    updateFilters: (state, action: PayloadAction<Partial<ExerciseFilters>>) => {
      state.filters = { ...state.filters, ...action.payload };
    },

    resetFilters: (state) => {
      state.filters = {
        limit: 10,
        random_order: true,
      };
    },

    setAvailableTypes: (state, action: PayloadAction<string[]>) => {
      state.availableTypes = action.payload;
    },

    setExerciseLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },

    setExerciseError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
      state.isLoading = false;
    },

    clearExerciseError: (state) => {
      state.error = null;
    },

    resetExerciseState: (state) => {
      state.currentExercise = null;
      state.currentAnswer = '';
      state.lastValidation = null;
      state.isSubmitting = false;
      state.error = null;
    },
  },
});

export const {
  setCurrentExercise,
  setCurrentAnswer,
  clearCurrentAnswer,
  addToHistory,
  clearHistory,
  setSubmitting,
  setLastValidation,
  updateFilters,
  resetFilters,
  setAvailableTypes,
  setExerciseLoading,
  setExerciseError,
  clearExerciseError,
  resetExerciseState,
} = exerciseSlice.actions;

export default exerciseSlice.reducer;

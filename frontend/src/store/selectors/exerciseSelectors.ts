/**
 * Memoized selectors for exercise state
 */

import { createSelector } from '@reduxjs/toolkit';
import type { RootState } from '../store';

// Base selectors
const selectExerciseState = (state: RootState) => state.exercise;

// Memoized selectors
export const selectCurrentExercise = createSelector(
  [selectExerciseState],
  (exercise) => exercise.currentExercise
);

export const selectCurrentAnswer = createSelector(
  [selectExerciseState],
  (exercise) => exercise.currentAnswer
);

export const selectExerciseHistory = createSelector(
  [selectExerciseState],
  (exercise) => exercise.exerciseHistory
);

export const selectLastValidation = createSelector(
  [selectExerciseState],
  (exercise) => exercise.lastValidation
);

export const selectExerciseFilters = createSelector(
  [selectExerciseState],
  (exercise) => exercise.filters
);

export const selectAvailableTypes = createSelector(
  [selectExerciseState],
  (exercise) => exercise.availableTypes
);

export const selectIsSubmitting = createSelector(
  [selectExerciseState],
  (exercise) => exercise.isSubmitting
);

export const selectExerciseLoading = createSelector(
  [selectExerciseState],
  (exercise) => exercise.isLoading
);

export const selectExerciseError = createSelector(
  [selectExerciseState],
  (exercise) => exercise.error
);

// Computed selectors
export const selectIsAnswerValid = createSelector(
  [selectCurrentAnswer],
  (answer) => answer.trim().length > 0
);

export const selectExerciseHistoryCount = createSelector(
  [selectExerciseHistory],
  (history) => history.length
);

export const selectLastCorrectAnswer = createSelector(
  [selectLastValidation],
  (validation) => validation?.is_correct ? validation.correct_answer : null
);

export const selectLastScore = createSelector(
  [selectLastValidation],
  (validation) => validation?.score || 0
);

export const selectFilteredExerciseTypes = createSelector(
  [selectAvailableTypes, selectExerciseFilters],
  (types, filters) => {
    if (filters.exercise_type) {
      return types.filter((type) => type === filters.exercise_type);
    }
    return types;
  }
);

export const selectExerciseDifficulty = createSelector(
  [selectCurrentExercise],
  (exercise) => exercise?.difficulty || 1
);

export const selectExerciseHints = createSelector(
  [selectCurrentExercise],
  (exercise) => exercise?.hints || []
);

export const selectExerciseTags = createSelector(
  [selectCurrentExercise],
  (exercise) => exercise?.tags || []
);

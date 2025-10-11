/**
 * Exercise management hook
 */

import { useCallback } from 'react';
import { useAppSelector } from './useAppSelector';
import { useAppDispatch } from './useAppDispatch';
import {
  setCurrentExercise,
  setCurrentAnswer,
  clearCurrentAnswer,
  addToHistory,
  updateFilters,
  resetFilters,
  setLastValidation,
  resetExerciseState,
} from '../store/slices/exerciseSlice';
import {
  useGetExercisesQuery,
  useGetExerciseByIdQuery,
  useSubmitAnswerMutation,
  useGetExerciseTypesQuery,
} from '../store/api/exerciseApi';
import type { ApiExercise, ExerciseFilters } from '../types/api';

export const useExercise = () => {
  const dispatch = useAppDispatch();

  // Selectors
  const currentExercise = useAppSelector((state) => state.exercise.currentExercise);
  const currentAnswer = useAppSelector((state) => state.exercise.currentAnswer);
  const exerciseHistory = useAppSelector((state) => state.exercise.exerciseHistory);
  const lastValidation = useAppSelector((state) => state.exercise.lastValidation);
  const filters = useAppSelector((state) => state.exercise.filters);
  const availableTypes = useAppSelector((state) => state.exercise.availableTypes);
  const isSubmitting = useAppSelector((state) => state.exercise.isSubmitting);

  // Queries
  const { data: exerciseList, isLoading: isLoadingExercises } = useGetExercisesQuery(filters);
  const { data: exerciseTypes } = useGetExerciseTypesQuery();

  // Mutations
  const [submitAnswerMutation, { isLoading: isSubmittingAnswer }] = useSubmitAnswerMutation();

  // Set current exercise
  const setExercise = useCallback(
    (exercise: ApiExercise | null) => {
      dispatch(setCurrentExercise(exercise));
    },
    [dispatch]
  );

  // Update answer
  const updateAnswer = useCallback(
    (answer: string) => {
      dispatch(setCurrentAnswer(answer));
    },
    [dispatch]
  );

  // Clear answer
  const clearAnswer = useCallback(() => {
    dispatch(clearCurrentAnswer());
  }, [dispatch]);

  // Submit answer
  const submitAnswer = useCallback(
    async (timeTaken?: number) => {
      if (!currentExercise || !currentAnswer) return null;

      try {
        const validation = await submitAnswerMutation({
          exercise_id: currentExercise.id,
          user_answer: currentAnswer,
          time_taken: timeTaken,
        }).unwrap();

        dispatch(setLastValidation(validation));
        dispatch(addToHistory(currentExercise));
        return validation;
      } catch (err) {
        throw err;
      }
    },
    [currentExercise, currentAnswer, submitAnswerMutation, dispatch]
  );

  // Update filters
  const setFilters = useCallback(
    (newFilters: Partial<ExerciseFilters>) => {
      dispatch(updateFilters(newFilters));
    },
    [dispatch]
  );

  // Reset filters
  const clearFilters = useCallback(() => {
    dispatch(resetFilters());
  }, [dispatch]);

  // Reset exercise state
  const resetExercise = useCallback(() => {
    dispatch(resetExerciseState());
  }, [dispatch]);

  // Get next exercise from list
  const getNextExercise = useCallback(() => {
    if (!exerciseList?.exercises.length) return null;

    // Filter out exercises already in history
    const availableExercises = exerciseList.exercises.filter(
      (ex) => !exerciseHistory.some((h) => h.id === ex.id)
    );

    if (availableExercises.length === 0) {
      // Reset history if all exercises completed
      return exerciseList.exercises[0];
    }

    const nextExercise = availableExercises[0];
    dispatch(setCurrentExercise(nextExercise));
    dispatch(clearCurrentAnswer());
    dispatch(setLastValidation(null));
    return nextExercise;
  }, [exerciseList, exerciseHistory, dispatch]);

  return {
    // State
    currentExercise,
    currentAnswer,
    exerciseHistory,
    lastValidation,
    filters,
    availableTypes: exerciseTypes || [],
    exerciseList,
    isLoading: isLoadingExercises,
    isSubmitting: isSubmitting || isSubmittingAnswer,

    // Actions
    setExercise,
    updateAnswer,
    clearAnswer,
    submitAnswer,
    setFilters,
    clearFilters,
    resetExercise,
    getNextExercise,
  };
};

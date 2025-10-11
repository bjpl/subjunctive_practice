/**
 * Progress tracking hook
 */

import { useCallback } from 'react';
import { useAppSelector } from './useAppSelector';
import { useAppDispatch } from './useAppDispatch';
import {
  setProgress,
  setStatistics,
  incrementExerciseCount,
  incrementCorrectAnswers,
  incrementIncorrectAnswers,
  addExperiencePoints,
  resetProgress,
} from '../store/slices/progressSlice';
import {
  useGetUserProgressQuery,
  useGetUserStatisticsQuery,
  useResetProgressMutation,
} from '../store/api/progressApi';

export const useProgress = () => {
  const dispatch = useAppDispatch();

  // Selectors
  const progress = useAppSelector((state) => state.progress.progress);
  const statistics = useAppSelector((state) => state.progress.statistics);
  const isLoading = useAppSelector((state) => state.progress.isLoading);
  const error = useAppSelector((state) => state.progress.error);

  // Queries
  const {
    data: progressData,
    isLoading: isLoadingProgress,
    refetch: refetchProgress,
  } = useGetUserProgressQuery();

  const {
    data: statisticsData,
    isLoading: isLoadingStatistics,
    refetch: refetchStatistics,
  } = useGetUserStatisticsQuery();

  // Mutations
  const [resetProgressMutation, { isLoading: isResetting }] = useResetProgressMutation();

  // Update progress from server
  const refreshProgress = useCallback(async () => {
    const result = await refetchProgress();
    if (result.data) {
      dispatch(setProgress(result.data));
    }
    return result;
  }, [refetchProgress, dispatch]);

  // Update statistics from server
  const refreshStatistics = useCallback(async () => {
    const result = await refetchStatistics();
    if (result.data) {
      dispatch(setStatistics(result.data));
    }
    return result;
  }, [refetchStatistics, dispatch]);

  // Track exercise completion
  const trackExerciseCompletion = useCallback(
    (isCorrect: boolean, score: number) => {
      dispatch(incrementExerciseCount());
      if (isCorrect) {
        dispatch(incrementCorrectAnswers());
        dispatch(addExperiencePoints(score));
      } else {
        dispatch(incrementIncorrectAnswers());
      }
    },
    [dispatch]
  );

  // Reset user progress
  const resetUserProgress = useCallback(async () => {
    try {
      await resetProgressMutation().unwrap();
      dispatch(resetProgress());
      await refreshProgress();
      await refreshStatistics();
    } catch (err) {
      throw err;
    }
  }, [resetProgressMutation, dispatch, refreshProgress, refreshStatistics]);

  return {
    // State
    progress: progress || progressData || null,
    statistics: statistics || statisticsData || null,
    isLoading: isLoading || isLoadingProgress || isLoadingStatistics || isResetting,
    error,

    // Actions
    refreshProgress,
    refreshStatistics,
    trackExerciseCompletion,
    resetUserProgress,
  };
};

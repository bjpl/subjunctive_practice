/**
 * Progress tracking hook
 */

import { useCallback } from 'react';
import { useAppSelector } from './useAppSelector';
import { useAppDispatch } from './useAppDispatch';
import {
  updateStatistics,
  resetProgressState,
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
    return result;
  }, [refetchProgress]);

  // Update statistics from server
  const refreshStatistics = useCallback(async () => {
    const result = await refetchStatistics();
    if (result.data) {
      dispatch(updateStatistics(result.data));
    }
    return result;
  }, [refetchStatistics, dispatch]);

  // Track exercise completion
  const trackExerciseCompletion = useCallback(
    (isCorrect: boolean, score: number) => {
      // Update statistics based on exercise completion
      if (statistics) {
        const updates: Partial<typeof statistics> = {
          overall_stats: {
            ...statistics.overall_stats,
            total_exercises: statistics.overall_stats.total_exercises + 1,
            correct_answers: isCorrect
              ? statistics.overall_stats.correct_answers + 1
              : statistics.overall_stats.correct_answers,
            average_score: ((statistics.overall_stats.average_score * statistics.overall_stats.total_exercises) + score) / (statistics.overall_stats.total_exercises + 1),
            accuracy_rate: isCorrect
              ? (statistics.overall_stats.correct_answers + 1) / (statistics.overall_stats.total_exercises + 1)
              : statistics.overall_stats.correct_answers / (statistics.overall_stats.total_exercises + 1),
          },
        };
        dispatch(updateStatistics(updates));
      }
    },
    [dispatch, statistics]
  );

  // Reset user progress
  const resetUserProgress = useCallback(async () => {
    try {
      await resetProgressMutation().unwrap();
      dispatch(resetProgressState());
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

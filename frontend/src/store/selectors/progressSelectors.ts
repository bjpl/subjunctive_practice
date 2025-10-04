/**
 * Memoized selectors for progress state
 */

import { createSelector } from '@reduxjs/toolkit';
import type { RootState } from '../store';

// Base selectors
const selectProgressState = (state: RootState) => state.progress;

// Memoized selectors
export const selectProgress = createSelector(
  [selectProgressState],
  (progress) => progress.progress
);

export const selectStatistics = createSelector(
  [selectProgressState],
  (progress) => progress.statistics
);

export const selectProgressLoading = createSelector(
  [selectProgressState],
  (progress) => progress.isLoading
);

export const selectProgressError = createSelector(
  [selectProgressState],
  (progress) => progress.error
);

// Progress metrics
export const selectTotalExercises = createSelector(
  [selectProgress],
  (progress) => progress?.total_exercises || 0
);

export const selectCorrectAnswers = createSelector(
  [selectProgress],
  (progress) => progress?.correct_answers || 0
);

export const selectIncorrectAnswers = createSelector(
  [selectProgress],
  (progress) => progress?.incorrect_answers || 0
);

export const selectAccuracyRate = createSelector(
  [selectProgress],
  (progress) => progress?.accuracy_rate || 0
);

export const selectCurrentStreak = createSelector(
  [selectProgress],
  (progress) => progress?.current_streak || 0
);

export const selectBestStreak = createSelector(
  [selectProgress],
  (progress) => progress?.best_streak || 0
);

export const selectUserLevel = createSelector(
  [selectProgress],
  (progress) => progress?.level || 1
);

export const selectExperiencePoints = createSelector(
  [selectProgress],
  (progress) => progress?.experience_points || 0
);

export const selectLastPracticeDate = createSelector(
  [selectProgress],
  (progress) => progress?.last_practice || null
);

// Computed selectors
export const selectNextLevelXP = createSelector(
  [selectUserLevel],
  (level) => Math.pow(level, 2) * 100
);

export const selectLevelProgress = createSelector(
  [selectExperiencePoints, selectNextLevelXP],
  (xp, nextLevelXP) => {
    const currentLevelXP = Math.pow(Math.floor(Math.sqrt(xp / 100)), 2) * 100;
    const progress = ((xp - currentLevelXP) / (nextLevelXP - currentLevelXP)) * 100;
    return Math.min(Math.max(progress, 0), 100);
  }
);

export const selectIsOnStreak = createSelector(
  [selectCurrentStreak],
  (streak) => streak > 0
);

export const selectStreakMessage = createSelector(
  [selectCurrentStreak, selectBestStreak],
  (current, best) => {
    if (current === 0) return 'Start your streak today!';
    if (current === 1) return '1 day streak - keep going!';
    if (current === best) return `${current} days - Personal best!`;
    return `${current} days streak - ${best - current} to beat your record!`;
  }
);

// Statistics selectors
export const selectOverallStats = createSelector(
  [selectStatistics],
  (stats) => stats?.overall_stats || null
);

export const selectStatsByType = createSelector(
  [selectStatistics],
  (stats) => stats?.by_type || {}
);

export const selectStatsByDifficulty = createSelector(
  [selectStatistics],
  (stats) => stats?.by_difficulty || {}
);

export const selectRecentPerformance = createSelector(
  [selectStatistics],
  (stats) => stats?.recent_performance || []
);

export const selectLearningInsights = createSelector(
  [selectStatistics],
  (stats) => stats?.learning_insights || []
);

export const selectPracticeCalendar = createSelector(
  [selectStatistics],
  (stats) => stats?.practice_calendar || []
);

// Weak areas selector
export const selectWeakAreas = createSelector(
  [selectStatsByType],
  (byType) => {
    return Object.entries(byType)
      .filter(([_, stats]) => stats.accuracy < 70 && stats.total >= 5)
      .map(([type, stats]) => ({
        type,
        accuracy: stats.accuracy,
        total: stats.total,
      }))
      .sort((a, b) => a.accuracy - b.accuracy);
  }
);

// Strong areas selector
export const selectStrongAreas = createSelector(
  [selectStatsByType],
  (byType) => {
    return Object.entries(byType)
      .filter(([_, stats]) => stats.accuracy >= 85 && stats.total >= 5)
      .map(([type, stats]) => ({
        type,
        accuracy: stats.accuracy,
        total: stats.total,
      }))
      .sort((a, b) => b.accuracy - a.accuracy);
  }
);

// Recent performance trend
export const selectRecentTrend = createSelector(
  [selectRecentPerformance],
  (recent) => {
    if (recent.length < 3) return 'neutral';
    const last5 = recent.slice(-5);
    const correct = last5.filter((r) => r.is_correct).length;
    if (correct >= 4) return 'improving';
    if (correct <= 1) return 'declining';
    return 'stable';
  }
);

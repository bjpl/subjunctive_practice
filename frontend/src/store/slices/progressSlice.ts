import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import type { Statistics, ProgressData, Achievement } from "@/types";

interface ProgressState {
  statistics: Statistics | null;
  progressHistory: ProgressData[];
  isLoading: boolean;
  error: string | null;
}

const initialState: ProgressState = {
  statistics: null,
  progressHistory: [],
  isLoading: false,
  error: null,
};

const progressSlice = createSlice({
  name: "progress",
  initialState,
  reducers: {
    fetchStatisticsStart: (state) => {
      state.isLoading = true;
      state.error = null;
    },
    fetchStatisticsSuccess: (state, action: PayloadAction<Statistics>) => {
      state.isLoading = false;
      state.statistics = action.payload;
    },
    fetchStatisticsFailure: (state, action: PayloadAction<string>) => {
      state.isLoading = false;
      state.error = action.payload;
    },
    updateStatistics: (state, action: PayloadAction<Partial<Statistics>>) => {
      if (state.statistics) {
        state.statistics = { ...state.statistics, ...action.payload };
      }
    },
    incrementStreak: (state) => {
      if (state.statistics) {
        state.statistics.currentStreak += 1;
        if (state.statistics.currentStreak > state.statistics.longestStreak) {
          state.statistics.longestStreak = state.statistics.currentStreak;
        }
      }
    },
    resetStreak: (state) => {
      if (state.statistics) {
        state.statistics.currentStreak = 0;
      }
    },
    addAchievement: (state, action: PayloadAction<Achievement>) => {
      if (state.statistics) {
        const existingIndex = state.statistics.achievements.findIndex(
          (a) => a.id === action.payload.id
        );
        if (existingIndex >= 0) {
          state.statistics.achievements[existingIndex] = action.payload;
        } else {
          state.statistics.achievements.push(action.payload);
        }
      }
    },
    updateAchievementProgress: (
      state,
      action: PayloadAction<{ id: string; progress: number }>
    ) => {
      if (state.statistics) {
        const achievement = state.statistics.achievements.find(
          (a) => a.id === action.payload.id
        );
        if (achievement) {
          achievement.progress = action.payload.progress;
          if (achievement.progress >= achievement.target && !achievement.unlockedAt) {
            achievement.unlockedAt = new Date();
          }
        }
      }
    },
    setProgressHistory: (state, action: PayloadAction<ProgressData[]>) => {
      state.progressHistory = action.payload;
    },
    addProgressData: (state, action: PayloadAction<ProgressData>) => {
      state.progressHistory.push(action.payload);
    },
    clearError: (state) => {
      state.error = null;
    },
    resetProgressState: () => initialState,
  },
});

export const {
  fetchStatisticsStart,
  fetchStatisticsSuccess,
  fetchStatisticsFailure,
  updateStatistics,
  incrementStreak,
  resetStreak,
  addAchievement,
  updateAchievementProgress,
  setProgressHistory,
  addProgressData,
  clearError,
  resetProgressState,
} = progressSlice.actions;

export default progressSlice.reducer;

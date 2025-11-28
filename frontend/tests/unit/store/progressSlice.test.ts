import progressReducer, {
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
} from '@/store/slices/progressSlice';
import type { Statistics, Achievement, ProgressData } from '@/types';

const mockAchievement: Achievement = {
  id: 'achievement-1',
  name: 'First Steps',
  description: 'Complete your first exercise',
  icon: '🎯',
  progress: 1,
  target: 1,
  unlockedAt: new Date('2024-01-01'),
};

const mockStatistics: Statistics = {
  totalExercises: 100,
  correctAnswers: 75,
  accuracy: 0.75,
  currentStreak: 5,
  longestStreak: 10,
  averageTimePerExercise: 45000,
  verbsMastered: ['hablar', 'ser', 'estar'],
  weakAreas: ['subjunctive-imperfect'],
  lastPracticeDate: new Date('2024-01-01'),
  totalPracticeTime: 3600000,
  level: 3,
  xp: 1500,
  achievements: [mockAchievement],
};

const mockProgressData: ProgressData = {
  date: new Date('2024-01-01'),
  exercisesCompleted: 10,
  accuracy: 0.8,
  timeSpent: 600000,
};

describe('progressSlice', () => {
  describe('initial state', () => {
    it('should have correct initial state', () => {
      const state = progressReducer(undefined, { type: 'unknown' });

      expect(state).toEqual({
        statistics: null,
        progressHistory: [],
        isLoading: false,
        error: null,
      });
    });
  });

  describe('fetchStatisticsStart', () => {
    it('should set loading state and clear errors', () => {
      const initialState = {
        statistics: null,
        progressHistory: [],
        isLoading: false,
        error: 'previous error',
      };

      const state = progressReducer(initialState, fetchStatisticsStart());

      expect(state.isLoading).toBe(true);
      expect(state.error).toBeNull();
    });
  });

  describe('fetchStatisticsSuccess', () => {
    it('should set statistics and stop loading', () => {
      const initialState = {
        statistics: null,
        progressHistory: [],
        isLoading: true,
        error: null,
      };

      const state = progressReducer(
        initialState,
        fetchStatisticsSuccess(mockStatistics)
      );

      expect(state.isLoading).toBe(false);
      expect(state.statistics).toEqual(mockStatistics);
    });

    it('should replace existing statistics', () => {
      const oldStats = { ...mockStatistics, totalExercises: 50 };
      const initialState = {
        statistics: oldStats,
        progressHistory: [],
        isLoading: true,
        error: null,
      };

      const state = progressReducer(
        initialState,
        fetchStatisticsSuccess(mockStatistics)
      );

      expect(state.statistics).toEqual(mockStatistics);
    });
  });

  describe('fetchStatisticsFailure', () => {
    it('should set error and stop loading', () => {
      const initialState = {
        statistics: null,
        progressHistory: [],
        isLoading: true,
        error: null,
      };

      const state = progressReducer(
        initialState,
        fetchStatisticsFailure('Network error')
      );

      expect(state.isLoading).toBe(false);
      expect(state.error).toBe('Network error');
    });
  });

  describe('updateStatistics', () => {
    it('should update partial statistics', () => {
      const initialState = {
        statistics: mockStatistics,
        progressHistory: [],
        isLoading: false,
        error: null,
      };

      const state = progressReducer(
        initialState,
        updateStatistics({ totalExercises: 150, accuracy: 0.85 })
      );

      expect(state.statistics?.totalExercises).toBe(150);
      expect(state.statistics?.accuracy).toBe(0.85);
      expect(state.statistics?.correctAnswers).toBe(75); // unchanged
    });

    it('should not update if statistics is null', () => {
      const state = progressReducer(
        undefined,
        updateStatistics({ totalExercises: 100 })
      );

      expect(state.statistics).toBeNull();
    });
  });

  describe('incrementStreak', () => {
    it('should increment current streak', () => {
      const initialState = {
        statistics: mockStatistics,
        progressHistory: [],
        isLoading: false,
        error: null,
      };

      const state = progressReducer(initialState, incrementStreak());

      expect(state.statistics?.currentStreak).toBe(6);
    });

    it('should update longest streak if current exceeds it', () => {
      const stats = { ...mockStatistics, currentStreak: 10, longestStreak: 10 };
      const initialState = {
        statistics: stats,
        progressHistory: [],
        isLoading: false,
        error: null,
      };

      const state = progressReducer(initialState, incrementStreak());

      expect(state.statistics?.currentStreak).toBe(11);
      expect(state.statistics?.longestStreak).toBe(11);
    });

    it('should not update longest streak if current is less', () => {
      const initialState = {
        statistics: mockStatistics,
        progressHistory: [],
        isLoading: false,
        error: null,
      };

      const state = progressReducer(initialState, incrementStreak());

      expect(state.statistics?.currentStreak).toBe(6);
      expect(state.statistics?.longestStreak).toBe(10); // unchanged
    });

    it('should handle null statistics', () => {
      const state = progressReducer(undefined, incrementStreak());

      expect(state.statistics).toBeNull();
    });
  });

  describe('resetStreak', () => {
    it('should reset current streak to 0', () => {
      const initialState = {
        statistics: mockStatistics,
        progressHistory: [],
        isLoading: false,
        error: null,
      };

      const state = progressReducer(initialState, resetStreak());

      expect(state.statistics?.currentStreak).toBe(0);
      expect(state.statistics?.longestStreak).toBe(10); // unchanged
    });

    it('should handle null statistics', () => {
      const state = progressReducer(undefined, resetStreak());

      expect(state.statistics).toBeNull();
    });
  });

  describe('addAchievement', () => {
    it('should add new achievement', () => {
      const newAchievement: Achievement = {
        id: 'achievement-2',
        name: 'Practice Master',
        description: 'Complete 100 exercises',
        icon: '🏆',
        progress: 100,
        target: 100,
        unlockedAt: new Date(),
      };

      const initialState = {
        statistics: mockStatistics,
        progressHistory: [],
        isLoading: false,
        error: null,
      };

      const state = progressReducer(initialState, addAchievement(newAchievement));

      expect(state.statistics?.achievements).toHaveLength(2);
      expect(state.statistics?.achievements[1]).toEqual(newAchievement);
    });

    it('should update existing achievement', () => {
      const updatedAchievement = { ...mockAchievement, progress: 2 };
      const initialState = {
        statistics: mockStatistics,
        progressHistory: [],
        isLoading: false,
        error: null,
      };

      const state = progressReducer(initialState, addAchievement(updatedAchievement));

      expect(state.statistics?.achievements).toHaveLength(1);
      expect(state.statistics?.achievements[0].progress).toBe(2);
    });

    it('should handle null statistics', () => {
      const state = progressReducer(undefined, addAchievement(mockAchievement));

      expect(state.statistics).toBeNull();
    });
  });

  describe('updateAchievementProgress', () => {
    it('should update achievement progress', () => {
      const initialState = {
        statistics: mockStatistics,
        progressHistory: [],
        isLoading: false,
        error: null,
      };

      const state = progressReducer(
        initialState,
        updateAchievementProgress({ id: 'achievement-1', progress: 5 })
      );

      expect(state.statistics?.achievements[0].progress).toBe(5);
    });

    it('should unlock achievement when progress reaches target', () => {
      const incompleteAchievement: Achievement = {
        ...mockAchievement,
        progress: 0,
        target: 5,
        unlockedAt: undefined,
      };

      const stats = {
        ...mockStatistics,
        achievements: [incompleteAchievement],
      };

      const initialState = {
        statistics: stats,
        progressHistory: [],
        isLoading: false,
        error: null,
      };

      const state = progressReducer(
        initialState,
        updateAchievementProgress({ id: 'achievement-1', progress: 5 })
      );

      expect(state.statistics?.achievements[0].progress).toBe(5);
      expect(state.statistics?.achievements[0].unlockedAt).toBeDefined();
    });

    it('should not unlock already unlocked achievement', () => {
      const initialState = {
        statistics: mockStatistics,
        progressHistory: [],
        isLoading: false,
        error: null,
      };

      const originalUnlockDate = mockStatistics.achievements[0].unlockedAt;

      const state = progressReducer(
        initialState,
        updateAchievementProgress({ id: 'achievement-1', progress: 2 })
      );

      expect(state.statistics?.achievements[0].unlockedAt).toEqual(originalUnlockDate);
    });

    it('should handle non-existent achievement', () => {
      const initialState = {
        statistics: mockStatistics,
        progressHistory: [],
        isLoading: false,
        error: null,
      };

      const state = progressReducer(
        initialState,
        updateAchievementProgress({ id: 'non-existent', progress: 5 })
      );

      expect(state.statistics?.achievements).toHaveLength(1);
    });

    it('should handle null statistics', () => {
      const state = progressReducer(
        undefined,
        updateAchievementProgress({ id: 'achievement-1', progress: 5 })
      );

      expect(state.statistics).toBeNull();
    });
  });

  describe('setProgressHistory', () => {
    it('should set progress history', () => {
      const history = [mockProgressData];
      const state = progressReducer(undefined, setProgressHistory(history));

      expect(state.progressHistory).toEqual(history);
    });

    it('should replace existing history', () => {
      const oldHistory = [{ ...mockProgressData, exercisesCompleted: 5 }];
      const newHistory = [mockProgressData];

      const initialState = {
        statistics: null,
        progressHistory: oldHistory,
        isLoading: false,
        error: null,
      };

      const state = progressReducer(initialState, setProgressHistory(newHistory));

      expect(state.progressHistory).toEqual(newHistory);
    });
  });

  describe('addProgressData', () => {
    it('should add progress data to history', () => {
      const state = progressReducer(undefined, addProgressData(mockProgressData));

      expect(state.progressHistory).toHaveLength(1);
      expect(state.progressHistory[0]).toEqual(mockProgressData);
    });

    it('should append to existing history', () => {
      const existingData = { ...mockProgressData, date: new Date('2023-12-31') };
      const initialState = {
        statistics: null,
        progressHistory: [existingData],
        isLoading: false,
        error: null,
      };

      const state = progressReducer(initialState, addProgressData(mockProgressData));

      expect(state.progressHistory).toHaveLength(2);
      expect(state.progressHistory[1]).toEqual(mockProgressData);
    });
  });

  describe('clearError', () => {
    it('should clear error', () => {
      const initialState = {
        statistics: null,
        progressHistory: [],
        isLoading: false,
        error: 'Some error',
      };

      const state = progressReducer(initialState, clearError());

      expect(state.error).toBeNull();
    });
  });

  describe('resetProgressState', () => {
    it('should reset to initial state', () => {
      const initialState = {
        statistics: mockStatistics,
        progressHistory: [mockProgressData],
        isLoading: true,
        error: 'some error',
      };

      const state = progressReducer(initialState, resetProgressState());

      expect(state).toEqual({
        statistics: null,
        progressHistory: [],
        isLoading: false,
        error: null,
      });
    });
  });
});

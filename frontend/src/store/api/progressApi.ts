/**
 * Progress tracking API endpoints
 */

import { baseApi } from './baseApi';
import type { ApiProgress, ApiStatistics } from '../../types/api';

export const progressApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    // Get user progress
    getUserProgress: builder.query<ApiProgress, void>({
      query: () => '/progress',
      providesTags: ['Progress'],
    }),

    // Get user statistics
    getUserStatistics: builder.query<ApiStatistics, void>({
      query: () => '/progress/statistics',
      providesTags: ['Statistics'],
    }),

    // Reset progress (for testing)
    resetProgress: builder.mutation<{ message: string; user_id: string }, void>({
      query: () => ({
        url: '/progress/reset',
        method: 'POST',
      }),
      invalidatesTags: ['Progress', 'Statistics'],
    }),
  }),
});

export const {
  useGetUserProgressQuery,
  useGetUserStatisticsQuery,
  useResetProgressMutation,
  useLazyGetUserProgressQuery,
  useLazyGetUserStatisticsQuery,
} = progressApi;

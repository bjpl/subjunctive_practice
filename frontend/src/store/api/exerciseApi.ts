/**
 * Exercise API endpoints
 */

import { baseApi } from './baseApi';
import type {
  ApiExercise,
  ExerciseListResponse,
  ExerciseAnswer,
  AnswerValidation,
  ExerciseFilters,
  CustomPracticeRequest,
  CustomPracticeResponse,
  AvailableVerbsResponse,
  SessionStartRequest,
  SessionStartResponse,
  SessionEndRequest,
  SessionEndResponse,
  DueReviewResponse,
  ReviewStatsResponse,
} from '@/types/api';

export const exerciseApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    // Get exercises with filters
    getExercises: builder.query<ExerciseListResponse, Partial<ExerciseFilters>>({
      query: (filters = {}) => {
        const params = new URLSearchParams();
        if (filters.difficulty) params.append('difficulty', filters.difficulty.toString());
        if (filters.exercise_type) params.append('exercise_type', filters.exercise_type);
        if (filters.tags && filters.tags.length > 0) {
          params.append('tags', filters.tags.join(','));
        }
        if (filters.limit) params.append('limit', filters.limit.toString());
        if (filters.random_order !== undefined) {
          params.append('random_order', filters.random_order.toString());
        }
        return `/exercises?${params.toString()}`;
      },
      providesTags: ['Exercise'],
    }),

    // Get single exercise by ID
    getExerciseById: builder.query<ApiExercise, string>({
      query: (id) => `/exercises/${id}`,
      providesTags: (_result, _error, id) => [{ type: 'Exercise', id }],
    }),

    // Submit answer
    submitAnswer: builder.mutation<AnswerValidation, ExerciseAnswer>({
      query: (answer) => ({
        url: '/exercises/submit',
        method: 'POST',
        body: answer,
      }),
      invalidatesTags: ['Progress', 'Statistics'],
    }),

    // Get available exercise types
    getExerciseTypes: builder.query<string[], void>({
      query: () => '/exercises/types/available',
    }),

    // Generate custom exercises
    generateCustomExercises: builder.mutation<CustomPracticeResponse, CustomPracticeRequest>({
      query: (config) => ({
        url: '/exercises/generate',
        method: 'POST',
        body: config,
      }),
    }),

    // Get available verbs for custom practice
    getAvailableVerbs: builder.query<AvailableVerbsResponse, void>({
      query: () => '/exercises/verbs/available',
    }),

    // Session management
    startSession: builder.mutation<SessionStartResponse, SessionStartRequest>({
      query: (request) => ({
        url: '/exercises/session/start',
        method: 'POST',
        body: request,
      }),
    }),

    endSession: builder.mutation<SessionEndResponse, SessionEndRequest>({
      query: (request) => ({
        url: '/exercises/session/end',
        method: 'POST',
        body: request,
      }),
      invalidatesTags: ['Progress', 'Statistics'],
    }),

    // Spaced repetition endpoints
    getDueReviews: builder.query<DueReviewResponse, { limit?: number }>({
      query: ({ limit = 10 }) => `/exercises/review/due?limit=${limit}`,
      providesTags: ['Exercise'],
    }),

    getReviewStats: builder.query<ReviewStatsResponse, void>({
      query: () => '/exercises/review/stats',
    }),
  }),
});

export const {
  useGetExercisesQuery,
  useGetExerciseByIdQuery,
  useSubmitAnswerMutation,
  useGetExerciseTypesQuery,
  useLazyGetExercisesQuery,
  useGenerateCustomExercisesMutation,
  useGetAvailableVerbsQuery,
  useStartSessionMutation,
  useEndSessionMutation,
  useGetDueReviewsQuery,
  useGetReviewStatsQuery,
} = exerciseApi;

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
  }),
});

export const {
  useGetExercisesQuery,
  useGetExerciseByIdQuery,
  useSubmitAnswerMutation,
  useGetExerciseTypesQuery,
  useLazyGetExercisesQuery,
} = exerciseApi;

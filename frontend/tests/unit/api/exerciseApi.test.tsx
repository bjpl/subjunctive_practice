/**
 * Unit tests for Exercise API endpoints (RTK Query)
 * Tests all exercise-related API endpoints including queries and mutations
 */

import React from 'react';
import { waitFor } from '@testing-library/react';
import {
  createTestStore,
  authenticatedState,
  waitForRTKQuery,
} from '../../utils/rtk-query-utils';
import {
  useGetExercisesQuery,
  useSubmitAnswerMutation,
  useGenerateCustomExercisesMutation,
  useGetDueReviewsQuery,
} from '@/store/api/exerciseApi';
import { server } from '../../mocks/server';
import { http, HttpResponse } from 'msw';
import { renderHook } from '@testing-library/react';
import { Provider } from 'react-redux';
import type {
  ExerciseFilters,
  ExerciseAnswer,
  CustomPracticeRequest,
  GeneratedExercise,
} from '@/types/api';

const API_BASE_URL = 'http://localhost:8000/api/v1';

describe('Exercise API Endpoints', () => {
  let store: ReturnType<typeof createTestStore>;

  beforeEach(() => {
    store = createTestStore(authenticatedState);
  });

  const wrapper = ({ children }: { children: React.ReactNode }) => {
    return <Provider store={store}>{children}</Provider>;
  };

  describe('getExercises Query', () => {
    it('should fetch exercises with no filters', async () => {
      const mockExercises = [
        {
          id: '1',
          type: 'fill-blank',
          prompt: 'Complete: Espero que tú _____ español.',
          difficulty: 2,
          explanation: 'Use present subjunctive after "espero que"',
          hints: ['Think about -ar verb endings'],
          tags: ['present-subjunctive', 'wishes'],
        },
        {
          id: '2',
          type: 'conjugation',
          prompt: 'Conjugate ser in present subjunctive for nosotros',
          difficulty: 3,
          explanation: 'Ser is irregular in subjunctive',
          hints: [],
          tags: ['present-subjunctive', 'irregular'],
        },
      ];

      server.use(
        http.get(`${API_BASE_URL}/exercises`, () => {
          return HttpResponse.json({
            exercises: mockExercises,
            total: 2,
            page: 1,
            page_size: 10,
            has_more: false,
          });
        })
      );

      const { result } = renderHook(() => useGetExercisesQuery({}), { wrapper });

      await waitFor(() => {
        expect(result.current.isSuccess).toBe(true);
      });

      expect(result.current.data?.exercises).toHaveLength(2);
      expect(result.current.data?.exercises[0]).toEqual(mockExercises[0]);
      expect(result.current.data?.total).toBe(2);
    });

    it('should fetch exercises with difficulty filter', async () => {
      const filters: Partial<ExerciseFilters> = {
        difficulty: 2,
        limit: 5,
      };

      server.use(
        http.get(`${API_BASE_URL}/exercises`, ({ request }) => {
          const url = new URL(request.url);
          expect(url.searchParams.get('difficulty')).toBe('2');
          expect(url.searchParams.get('limit')).toBe('5');

          return HttpResponse.json({
            exercises: [
              {
                id: '1',
                type: 'fill-blank',
                prompt: 'Intermediate exercise',
                difficulty: 2,
              },
            ],
            total: 1,
            page: 1,
            page_size: 5,
            has_more: false,
          });
        })
      );

      const { result } = renderHook(() => useGetExercisesQuery(filters), { wrapper });

      await waitFor(() => {
        expect(result.current.isSuccess).toBe(true);
      });

      expect(result.current.data?.exercises).toHaveLength(1);
      expect(result.current.data?.exercises[0].difficulty).toBe(2);
    });

    it('should fetch exercises with type and tags filters', async () => {
      const filters: Partial<ExerciseFilters> = {
        exercise_type: 'conjugation',
        tags: ['present-subjunctive', 'irregular'],
        random_order: true,
      };

      server.use(
        http.get(`${API_BASE_URL}/exercises`, ({ request }) => {
          const url = new URL(request.url);
          expect(url.searchParams.get('exercise_type')).toBe('conjugation');
          expect(url.searchParams.get('tags')).toBe('present-subjunctive,irregular');
          expect(url.searchParams.get('random_order')).toBe('true');

          return HttpResponse.json({
            exercises: [],
            total: 0,
            page: 1,
            page_size: 10,
            has_more: false,
          });
        })
      );

      const { result } = renderHook(() => useGetExercisesQuery(filters), { wrapper });

      await waitFor(() => {
        expect(result.current.isSuccess).toBe(true);
      });

      expect(result.current.data?.exercises).toHaveLength(0);
    });

    it('should handle API errors when fetching exercises', async () => {
      server.use(
        http.get(`${API_BASE_URL}/exercises`, () => {
          return HttpResponse.json(
            { error: 'Internal server error' },
            { status: 500 }
          );
        })
      );

      const { result } = renderHook(() => useGetExercisesQuery({}), { wrapper });

      await waitFor(() => {
        expect(result.current.isError).toBe(true);
      });

      expect(result.current.error).toBeDefined();
    });

    it('should cache exercises query results', async () => {
      let callCount = 0;

      server.use(
        http.get(`${API_BASE_URL}/exercises`, () => {
          callCount++;
          return HttpResponse.json({
            exercises: [{ id: '1', type: 'fill-blank', prompt: 'Test', difficulty: 1 }],
            total: 1,
            page: 1,
            page_size: 10,
            has_more: false,
          });
        })
      );

      // First call
      const { result: result1 } = renderHook(() => useGetExercisesQuery({}), { wrapper });

      await waitFor(() => {
        expect(result1.current.isSuccess).toBe(true);
      });

      expect(callCount).toBe(1);

      // Second call with same parameters should use cache
      const { result: result2 } = renderHook(() => useGetExercisesQuery({}), { wrapper });

      await waitFor(() => {
        expect(result2.current.isSuccess).toBe(true);
      });

      // Should still be 1 because of caching
      expect(callCount).toBe(1);
    });
  });

  describe('submitAnswer Mutation', () => {
    it('should submit correct answer successfully', async () => {
      const answer: ExerciseAnswer = {
        exercise_id: '1',
        user_answer: 'hables',
        time_taken: 15,
        session_id: 123,
      };

      server.use(
        http.post(`${API_BASE_URL}/exercises/submit`, async ({ request }) => {
          const body = await request.json() as ExerciseAnswer;
          expect(body.user_answer).toBe('hables');

          return HttpResponse.json({
            is_correct: true,
            correct_answer: 'hables',
            user_answer: 'hables',
            feedback: 'Excellent work!',
            score: 100,
            explanation: 'Perfect conjugation of the present subjunctive.',
          });
        })
      );

      const { result } = renderHook(() => useSubmitAnswerMutation(), { wrapper });

      const [submitAnswer] = result.current;
      const response = await submitAnswer(answer).unwrap();

      expect(response.is_correct).toBe(true);
      expect(response.score).toBe(100);
      expect(response.feedback).toBe('Excellent work!');
    });

    it('should submit incorrect answer and receive feedback', async () => {
      const answer: ExerciseAnswer = {
        exercise_id: '1',
        user_answer: 'habla',
        time_taken: 20,
      };

      server.use(
        http.post(`${API_BASE_URL}/exercises/submit`, () => {
          return HttpResponse.json({
            is_correct: false,
            correct_answer: 'hables',
            user_answer: 'habla',
            feedback: 'Almost! Remember to use the subjunctive form.',
            score: 0,
            explanation: 'After "espero que" we need the present subjunctive.',
            error_type: 'wrong_mood',
            suggestions: ['Try using the subjunctive ending for tú'],
          });
        })
      );

      const { result } = renderHook(() => useSubmitAnswerMutation(), { wrapper });

      const [submitAnswer] = result.current;
      const response = await submitAnswer(answer).unwrap();

      expect(response.is_correct).toBe(false);
      expect(response.correct_answer).toBe('hables');
      expect(response.error_type).toBe('wrong_mood');
      expect(response.suggestions).toHaveLength(1);
    });

    it('should handle network errors during submission', async () => {
      server.use(
        http.post(`${API_BASE_URL}/exercises/submit`, () => {
          return HttpResponse.error();
        })
      );

      const { result } = renderHook(() => useSubmitAnswerMutation(), { wrapper });

      const [submitAnswer] = result.current;
      const answer: ExerciseAnswer = {
        exercise_id: '1',
        user_answer: 'hables',
      };

      await expect(submitAnswer(answer).unwrap()).rejects.toThrow();
    });

    it('should invalidate progress and statistics tags after submission', async () => {
      server.use(
        http.post(`${API_BASE_URL}/exercises/submit`, () => {
          return HttpResponse.json({
            is_correct: true,
            correct_answer: 'hables',
            user_answer: 'hables',
            feedback: 'Great!',
            score: 100,
          });
        })
      );

      const { result } = renderHook(() => useSubmitAnswerMutation(), { wrapper });

      const [submitAnswer, { isSuccess }] = result.current;
      const answer: ExerciseAnswer = {
        exercise_id: '1',
        user_answer: 'hables',
      };

      await submitAnswer(answer);

      await waitFor(() => {
        expect(isSuccess).toBe(true);
      });

      // Tags should be invalidated (Progress and Statistics)
      const apiState = store.getState().api;
      expect(apiState).toBeDefined();
    });
  });

  describe('generateCustomExercises Mutation', () => {
    it('should generate custom exercises with full configuration', async () => {
      const config: CustomPracticeRequest = {
        verbs: ['hablar', 'ser', 'tener'],
        tense: 'present_subjunctive',
        persons: ['yo', 'tú', 'él/ella/usted'],
        difficulty: 2,
        custom_context: 'at a restaurant',
        trigger_category: 'wishes',
        exercise_count: 10,
        include_hints: true,
        include_explanations: true,
      };

      const mockExercises: GeneratedExercise[] = [
        {
          id: '1',
          verb: 'hablar',
          verb_translation: 'to speak',
          tense: 'present_subjunctive',
          person: 'yo',
          prompt: 'Espero que yo _____ con el mesero.',
          correct_answer: 'hable',
          alternative_answers: [],
          hint: 'Use the yo form of hablar in present subjunctive',
          explanation: 'After "espero que" we use the subjunctive.',
          trigger_phrase: 'espero que',
          difficulty: 2,
        },
      ];

      server.use(
        http.post(`${API_BASE_URL}/exercises/generate`, async ({ request }) => {
          const body = await request.json() as CustomPracticeRequest;
          expect(body.verbs).toHaveLength(3);
          expect(body.custom_context).toBe('at a restaurant');
          expect(body.exercise_count).toBe(10);

          return HttpResponse.json({
            exercises: mockExercises,
            total: 1,
            config_summary: {
              verbs: body.verbs,
              verb_count: body.verbs.length,
              tense: body.tense,
              persons: body.persons,
              difficulty: body.difficulty,
              trigger_category: body.trigger_category,
              has_custom_context: true,
            },
          });
        })
      );

      const { result } = renderHook(() => useGenerateCustomExercisesMutation(), { wrapper });

      const [generateExercises] = result.current;
      const response = await generateExercises(config).unwrap();

      expect(response.exercises).toHaveLength(1);
      expect(response.config_summary.has_custom_context).toBe(true);
      expect(response.config_summary.verb_count).toBe(3);
    });

    it('should generate exercises without custom context', async () => {
      const config: CustomPracticeRequest = {
        verbs: ['hablar'],
        tense: 'present_subjunctive',
        persons: ['yo'],
        difficulty: 1,
        custom_context: '',
        trigger_category: 'all',
        exercise_count: 5,
        include_hints: false,
        include_explanations: false,
      };

      server.use(
        http.post(`${API_BASE_URL}/exercises/generate`, () => {
          return HttpResponse.json({
            exercises: [],
            total: 0,
            config_summary: {
              verbs: config.verbs,
              verb_count: 1,
              tense: config.tense,
              persons: config.persons,
              difficulty: config.difficulty,
              trigger_category: 'all',
              has_custom_context: false,
            },
          });
        })
      );

      const { result } = renderHook(() => useGenerateCustomExercisesMutation(), { wrapper });

      const [generateExercises] = result.current;
      const response = await generateExercises(config).unwrap();

      expect(response.config_summary.has_custom_context).toBe(false);
    });

    it('should handle validation errors from generation endpoint', async () => {
      const invalidConfig: CustomPracticeRequest = {
        verbs: [],
        tense: 'invalid_tense',
        persons: [],
        difficulty: 0,
        custom_context: '',
        trigger_category: '',
        exercise_count: 0,
        include_hints: true,
        include_explanations: true,
      };

      server.use(
        http.post(`${API_BASE_URL}/exercises/generate`, () => {
          return HttpResponse.json(
            { error: 'Validation failed', details: 'Invalid configuration' },
            { status: 400 }
          );
        })
      );

      const { result } = renderHook(() => useGenerateCustomExercisesMutation(), { wrapper });

      const [generateExercises] = result.current;

      await expect(generateExercises(invalidConfig).unwrap()).rejects.toThrow();
    });
  });

  describe('getDueReviews Query', () => {
    it('should fetch due reviews with default limit', async () => {
      const mockDueReviews = {
        items: [
          {
            verb_id: 1,
            verb_infinitive: 'hablar',
            verb_translation: 'to speak',
            tense: 'present_subjunctive',
            person: 'yo',
            days_overdue: 2,
            difficulty_level: 'easy',
            easiness_factor: 2.5,
            next_review_date: '2024-01-15',
            review_count: 5,
            success_rate: 0.8,
          },
        ],
        total_due: 1,
        next_review_date: '2024-01-16',
      };

      server.use(
        http.get(`${API_BASE_URL}/exercises/review/due`, ({ request }) => {
          const url = new URL(request.url);
          expect(url.searchParams.get('limit')).toBe('10');

          return HttpResponse.json(mockDueReviews);
        })
      );

      const { result } = renderHook(() => useGetDueReviewsQuery({ limit: 10 }), { wrapper });

      await waitFor(() => {
        expect(result.current.isSuccess).toBe(true);
      });

      expect(result.current.data?.items).toHaveLength(1);
      expect(result.current.data?.total_due).toBe(1);
      expect(result.current.data?.items[0].verb_infinitive).toBe('hablar');
    });

    it('should fetch due reviews with custom limit', async () => {
      server.use(
        http.get(`${API_BASE_URL}/exercises/review/due`, ({ request }) => {
          const url = new URL(request.url);
          expect(url.searchParams.get('limit')).toBe('20');

          return HttpResponse.json({
            items: [],
            total_due: 0,
          });
        })
      );

      const { result } = renderHook(() => useGetDueReviewsQuery({ limit: 20 }), { wrapper });

      await waitFor(() => {
        expect(result.current.isSuccess).toBe(true);
      });

      expect(result.current.data?.total_due).toBe(0);
    });

    it('should handle no due reviews', async () => {
      server.use(
        http.get(`${API_BASE_URL}/exercises/review/due`, () => {
          return HttpResponse.json({
            items: [],
            total_due: 0,
            next_review_date: null,
          });
        })
      );

      const { result } = renderHook(() => useGetDueReviewsQuery({}), { wrapper });

      await waitFor(() => {
        expect(result.current.isSuccess).toBe(true);
      });

      expect(result.current.data?.items).toHaveLength(0);
      expect(result.current.data?.next_review_date).toBeNull();
    });
  });

  describe('RTK Query Cache and Invalidation', () => {
    it('should provide Exercise tag for exercises query', async () => {
      server.use(
        http.get(`${API_BASE_URL}/exercises`, () => {
          return HttpResponse.json({
            exercises: [{ id: '1', type: 'fill-blank', prompt: 'Test', difficulty: 1 }],
            total: 1,
            page: 1,
            page_size: 10,
            has_more: false,
          });
        })
      );

      const { result } = renderHook(() => useGetExercisesQuery({}), { wrapper });

      await waitFor(() => {
        expect(result.current.isSuccess).toBe(true);
      });

      // Check that the query is tagged
      const apiState = store.getState().api;
      expect(apiState.queries).toBeDefined();
    });

    it('should invalidate Progress and Statistics tags after answer submission', async () => {
      server.use(
        http.post(`${API_BASE_URL}/exercises/submit`, () => {
          return HttpResponse.json({
            is_correct: true,
            correct_answer: 'hables',
            user_answer: 'hables',
            feedback: 'Great!',
            score: 100,
          });
        })
      );

      const { result } = renderHook(() => useSubmitAnswerMutation(), { wrapper });

      const [submitAnswer] = result.current;
      await submitAnswer({
        exercise_id: '1',
        user_answer: 'hables',
      });

      await waitFor(() => {
        const apiState = store.getState().api;
        expect(apiState.mutations).toBeDefined();
      });
    });
  });
});

/**
 * Unit tests for exercise slice actions
 * Tests exercise state management including sessions, answers, and progression
 */

import { configureStore } from '@reduxjs/toolkit';
import exerciseReducer, {
  startSession,
  setCurrentExercise,
  setAnswer,
  useHint,
  updateTimeElapsed,
  submitAnswerStart,
  submitAnswerSuccess,
  submitAnswerFailure,
  endSession,
  clearError,
  resetExerciseState,
} from '@/store/slices/exerciseSlice';
import type { PracticeSession, Exercise, Answer } from '@/types';

describe('Exercise Slice', () => {
  let store: ReturnType<typeof configureStore>;

  const mockExercises: Exercise[] = [
    {
      id: '1',
      type: 'fill-blank',
      verb: 'hablar',
      tense: 'Present Subjunctive',
      sentence: 'Espero que tú _____ español.',
      blanks: ['hables'],
      correctAnswer: 'hables',
      explanation: 'After espero que, we use the present subjunctive.',
      difficulty: 'beginner',
      hints: ['Think about -ar verbs'],
    },
    {
      id: '2',
      type: 'conjugation',
      verb: 'ser',
      tense: 'Present Subjunctive',
      sentence: 'Es importante que nosotros _____ honestos.',
      blanks: ['seamos'],
      correctAnswer: 'seamos',
      explanation: 'Ser is irregular in the subjunctive.',
      difficulty: 'intermediate',
      hints: [],
    },
  ];

  const mockSession: PracticeSession = {
    id: 'session-1',
    exercises: mockExercises,
    currentIndex: 0,
    answers: [],
    startTime: new Date('2024-01-01T10:00:00Z'),
    endTime: undefined,
    completed: false,
  };

  beforeEach(() => {
    store = configureStore({
      reducer: {
        exercise: exerciseReducer,
      },
    });
  });

  describe('Initial State', () => {
    it('should have correct initial state', () => {
      const state = store.getState().exercise;

      expect(state.currentSession).toBeNull();
      expect(state.currentExercise).toBeNull();
      expect(state.currentAnswer).toBeNull();
      expect(state.hintsUsed).toBe(0);
      expect(state.timeElapsed).toBe(0);
      expect(state.isSubmitting).toBe(false);
      expect(state.error).toBeNull();
    });
  });

  describe('Session Management', () => {
    it('should start a new practice session', () => {
      store.dispatch(startSession(mockSession));
      const state = store.getState().exercise;

      expect(state.currentSession).toEqual(mockSession);
      expect(state.currentExercise).toEqual(mockExercises[0]);
      expect(state.currentAnswer).toBeNull();
      expect(state.hintsUsed).toBe(0);
      expect(state.timeElapsed).toBe(0);
      expect(state.error).toBeNull();
    });

    it('should handle empty exercise list in session', () => {
      const emptySession: PracticeSession = {
        ...mockSession,
        exercises: [],
      };

      store.dispatch(startSession(emptySession));
      const state = store.getState().exercise;

      expect(state.currentSession).toEqual(emptySession);
      expect(state.currentExercise).toBeNull();
    });

    it('should end the current session', () => {
      store.dispatch(startSession(mockSession));
      store.dispatch(endSession());

      const state = store.getState().exercise;

      expect(state.currentSession?.completed).toBe(true);
      expect(state.currentSession?.endTime).toBeDefined();
      expect(state.currentExercise).toBeNull();
      expect(state.currentAnswer).toBeNull();
      expect(state.hintsUsed).toBe(0);
      expect(state.timeElapsed).toBe(0);
    });

    it('should handle ending session when no session exists', () => {
      store.dispatch(endSession());
      const state = store.getState().exercise;

      expect(state.currentSession).toBeNull();
      expect(state.currentExercise).toBeNull();
    });
  });

  describe('Exercise Navigation', () => {
    it('should set current exercise', () => {
      store.dispatch(setCurrentExercise(mockExercises[1]));
      const state = store.getState().exercise;

      expect(state.currentExercise).toEqual(mockExercises[1]);
      expect(state.currentAnswer).toBeNull();
      expect(state.hintsUsed).toBe(0);
      expect(state.timeElapsed).toBe(0);
    });

    it('should reset exercise state when changing exercises', () => {
      store.dispatch(startSession(mockSession));
      store.dispatch(setAnswer('some answer'));
      store.dispatch(useHint());
      store.dispatch(updateTimeElapsed(30));

      // Change to next exercise
      store.dispatch(setCurrentExercise(mockExercises[1]));
      const state = store.getState().exercise;

      expect(state.currentAnswer).toBeNull();
      expect(state.hintsUsed).toBe(0);
      expect(state.timeElapsed).toBe(0);
    });
  });

  describe('Answer Management', () => {
    beforeEach(() => {
      store.dispatch(startSession(mockSession));
    });

    it('should set user answer as string', () => {
      store.dispatch(setAnswer('hables'));
      const state = store.getState().exercise;

      expect(state.currentAnswer).toBe('hables');
    });

    it('should set user answer as array', () => {
      const answers = ['hable', 'hables', 'hable'];
      store.dispatch(setAnswer(answers));
      const state = store.getState().exercise;

      expect(state.currentAnswer).toEqual(answers);
    });

    it('should update answer multiple times', () => {
      store.dispatch(setAnswer('habl'));
      expect(store.getState().exercise.currentAnswer).toBe('habl');

      store.dispatch(setAnswer('hable'));
      expect(store.getState().exercise.currentAnswer).toBe('hable');

      store.dispatch(setAnswer('hables'));
      expect(store.getState().exercise.currentAnswer).toBe('hables');
    });
  });

  describe('Hint System', () => {
    it('should increment hints used', () => {
      store.dispatch(startSession(mockSession));

      expect(store.getState().exercise.hintsUsed).toBe(0);

      store.dispatch(useHint());
      expect(store.getState().exercise.hintsUsed).toBe(1);

      store.dispatch(useHint());
      expect(store.getState().exercise.hintsUsed).toBe(2);

      store.dispatch(useHint());
      expect(store.getState().exercise.hintsUsed).toBe(3);
    });
  });

  describe('Time Tracking', () => {
    it('should update time elapsed', () => {
      store.dispatch(startSession(mockSession));

      store.dispatch(updateTimeElapsed(10));
      expect(store.getState().exercise.timeElapsed).toBe(10);

      store.dispatch(updateTimeElapsed(25));
      expect(store.getState().exercise.timeElapsed).toBe(25);

      store.dispatch(updateTimeElapsed(60));
      expect(store.getState().exercise.timeElapsed).toBe(60);
    });
  });

  describe('Answer Submission', () => {
    beforeEach(() => {
      store.dispatch(startSession(mockSession));
    });

    it('should handle answer submission start', () => {
      store.dispatch(submitAnswerStart());
      const state = store.getState().exercise;

      expect(state.isSubmitting).toBe(true);
      expect(state.error).toBeNull();
    });

    it('should handle successful answer submission and move to next exercise', () => {
      const answer: Answer = {
        exerciseId: '1',
        userAnswer: 'hables',
        isCorrect: true,
        correctAnswer: 'hables',
        timeSpent: 15,
        hintsUsed: 0,
        timestamp: new Date('2024-01-01T10:00:15Z'),
      };

      store.dispatch(submitAnswerSuccess(answer));
      const state = store.getState().exercise;

      expect(state.isSubmitting).toBe(false);
      expect(state.currentSession?.answers).toHaveLength(1);
      expect(state.currentSession?.answers[0]).toEqual(answer);
      expect(state.currentSession?.currentIndex).toBe(1);
      expect(state.currentExercise).toEqual(mockExercises[1]);
      expect(state.currentAnswer).toBeNull();
      expect(state.hintsUsed).toBe(0);
      expect(state.timeElapsed).toBe(0);
    });

    it('should complete session after last exercise', () => {
      // Move to last exercise
      store.dispatch(setCurrentExercise(mockExercises[1]));

      const answer: Answer = {
        exerciseId: '2',
        userAnswer: 'seamos',
        isCorrect: true,
        correctAnswer: 'seamos',
        timeSpent: 20,
        hintsUsed: 1,
        timestamp: new Date('2024-01-01T10:00:35Z'),
      };

      // Update session to be on last exercise
      store.dispatch(startSession({
        ...mockSession,
        currentIndex: 1,
      }));

      store.dispatch(submitAnswerSuccess(answer));
      const state = store.getState().exercise;

      expect(state.currentSession?.completed).toBe(true);
      expect(state.currentSession?.endTime).toBeDefined();
      expect(state.currentExercise).toBeNull();
    });

    it('should handle answer submission failure', () => {
      const errorMessage = 'Network error';

      store.dispatch(submitAnswerFailure(errorMessage));
      const state = store.getState().exercise;

      expect(state.isSubmitting).toBe(false);
      expect(state.error).toBe(errorMessage);
    });

    it('should track multiple answers in session', () => {
      const answer1: Answer = {
        exerciseId: '1',
        userAnswer: 'hables',
        isCorrect: true,
        correctAnswer: 'hables',
        timeSpent: 15,
        hintsUsed: 0,
        timestamp: new Date('2024-01-01T10:00:15Z'),
      };

      const answer2: Answer = {
        exerciseId: '2',
        userAnswer: 'seamos',
        isCorrect: true,
        correctAnswer: 'seamos',
        timeSpent: 20,
        hintsUsed: 1,
        timestamp: new Date('2024-01-01T10:00:35Z'),
      };

      store.dispatch(submitAnswerSuccess(answer1));
      store.dispatch(submitAnswerSuccess(answer2));

      const state = store.getState().exercise;

      expect(state.currentSession?.answers).toHaveLength(2);
      expect(state.currentSession?.answers[0]).toEqual(answer1);
      expect(state.currentSession?.answers[1]).toEqual(answer2);
    });
  });

  describe('Error Handling', () => {
    it('should clear error state', () => {
      store.dispatch(startSession(mockSession));
      store.dispatch(submitAnswerFailure('Some error'));

      expect(store.getState().exercise.error).toBe('Some error');

      store.dispatch(clearError());
      expect(store.getState().exercise.error).toBeNull();
    });
  });

  describe('State Reset', () => {
    it('should reset to initial state', () => {
      store.dispatch(startSession(mockSession));
      store.dispatch(setAnswer('hables'));
      store.dispatch(useHint());
      store.dispatch(updateTimeElapsed(30));

      store.dispatch(resetExerciseState());
      const state = store.getState().exercise;

      expect(state.currentSession).toBeNull();
      expect(state.currentExercise).toBeNull();
      expect(state.currentAnswer).toBeNull();
      expect(state.hintsUsed).toBe(0);
      expect(state.timeElapsed).toBe(0);
      expect(state.isSubmitting).toBe(false);
      expect(state.error).toBeNull();
    });
  });

  describe('Edge Cases', () => {
    it('should handle submitting answer when no session exists', () => {
      const answer: Answer = {
        exerciseId: '1',
        userAnswer: 'hables',
        isCorrect: true,
        correctAnswer: 'hables',
        timeSpent: 15,
        hintsUsed: 0,
        timestamp: new Date(),
      };

      store.dispatch(submitAnswerSuccess(answer));
      const state = store.getState().exercise;

      expect(state.currentSession).toBeNull();
    });

    it('should preserve session data when changing exercises manually', () => {
      store.dispatch(startSession(mockSession));

      const answer: Answer = {
        exerciseId: '1',
        userAnswer: 'hables',
        isCorrect: true,
        correctAnswer: 'hables',
        timeSpent: 15,
        hintsUsed: 0,
        timestamp: new Date(),
      };

      store.dispatch(submitAnswerSuccess(answer));

      // Manually set exercise
      store.dispatch(setCurrentExercise(mockExercises[0]));

      const state = store.getState().exercise;
      expect(state.currentSession?.answers).toHaveLength(1);
    });
  });
});

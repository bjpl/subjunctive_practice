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

const mockExercise: Exercise = {
  id: '1',
  type: 'fill-blank',
  verb: 'hablar',
  tense: 'Present Subjunctive',
  sentence: 'Espero que tú _____ español.',
  blanks: ['hables'],
  correctAnswer: 'hables',
  explanation: 'After espero que, we use the present subjunctive.',
  difficulty: 'beginner',
  hints: ['Think about the -ar verb conjugation'],
};

const mockSession: PracticeSession = {
  id: 'session-1',
  userId: 'user-1',
  startTime: new Date('2024-01-01T10:00:00Z'),
  exercises: [mockExercise],
  currentIndex: 0,
  answers: [],
  score: 0,
  completed: false,
  settings: {
    difficulty: 'beginner',
    hintsEnabled: true,
    feedbackType: 'immediate',
    exerciseCount: 10,
  },
};

const mockAnswer: Answer = {
  exerciseId: '1',
  userAnswer: 'hables',
  isCorrect: true,
  hintsUsed: 0,
  timeSpent: 15000,
  submittedAt: new Date('2024-01-01T10:00:15Z'),
};

describe('exerciseSlice', () => {
  describe('initial state', () => {
    it('should have correct initial state', () => {
      const state = exerciseReducer(undefined, { type: 'unknown' });

      expect(state).toEqual({
        currentSession: null,
        currentExercise: null,
        currentAnswer: null,
        hintsUsed: 0,
        timeElapsed: 0,
        isSubmitting: false,
        error: null,
      });
    });
  });

  describe('startSession', () => {
    it('should start a new session', () => {
      const state = exerciseReducer(undefined, startSession(mockSession));

      expect(state.currentSession).toEqual(mockSession);
      expect(state.currentExercise).toEqual(mockExercise);
      expect(state.currentAnswer).toBeNull();
      expect(state.hintsUsed).toBe(0);
      expect(state.timeElapsed).toBe(0);
      expect(state.error).toBeNull();
    });

    it('should handle session with no exercises', () => {
      const emptySession = { ...mockSession, exercises: [] };
      const state = exerciseReducer(undefined, startSession(emptySession));

      expect(state.currentSession).toEqual(emptySession);
      expect(state.currentExercise).toBeNull();
    });

    it('should reset previous session data', () => {
      const initialState = {
        currentSession: mockSession,
        currentExercise: mockExercise,
        currentAnswer: 'previous answer',
        hintsUsed: 3,
        timeElapsed: 5000,
        isSubmitting: false,
        error: 'previous error',
      };

      const state = exerciseReducer(initialState, startSession(mockSession));

      expect(state.hintsUsed).toBe(0);
      expect(state.timeElapsed).toBe(0);
      expect(state.currentAnswer).toBeNull();
      expect(state.error).toBeNull();
    });
  });

  describe('setCurrentExercise', () => {
    it('should set current exercise and reset related fields', () => {
      const initialState = {
        currentSession: mockSession,
        currentExercise: null,
        currentAnswer: 'old answer',
        hintsUsed: 2,
        timeElapsed: 3000,
        isSubmitting: false,
        error: null,
      };

      const state = exerciseReducer(initialState, setCurrentExercise(mockExercise));

      expect(state.currentExercise).toEqual(mockExercise);
      expect(state.currentAnswer).toBeNull();
      expect(state.hintsUsed).toBe(0);
      expect(state.timeElapsed).toBe(0);
    });
  });

  describe('setAnswer', () => {
    it('should set string answer', () => {
      const state = exerciseReducer(undefined, setAnswer('hables'));

      expect(state.currentAnswer).toBe('hables');
    });

    it('should set array answer', () => {
      const state = exerciseReducer(undefined, setAnswer(['hables', 'hable']));

      expect(state.currentAnswer).toEqual(['hables', 'hable']);
    });

    it('should update existing answer', () => {
      const initialState = {
        ...exerciseReducer(undefined, { type: 'unknown' }),
        currentAnswer: 'old answer',
      };

      const state = exerciseReducer(initialState, setAnswer('new answer'));

      expect(state.currentAnswer).toBe('new answer');
    });
  });

  describe('useHint', () => {
    it('should increment hints used', () => {
      let state = exerciseReducer(undefined, { type: 'unknown' });
      expect(state.hintsUsed).toBe(0);

      state = exerciseReducer(state, useHint());
      expect(state.hintsUsed).toBe(1);

      state = exerciseReducer(state, useHint());
      expect(state.hintsUsed).toBe(2);
    });
  });

  describe('updateTimeElapsed', () => {
    it('should update time elapsed', () => {
      const state = exerciseReducer(undefined, updateTimeElapsed(5000));

      expect(state.timeElapsed).toBe(5000);
    });

    it('should allow time to increase', () => {
      let state = exerciseReducer(undefined, updateTimeElapsed(1000));
      state = exerciseReducer(state, updateTimeElapsed(2000));

      expect(state.timeElapsed).toBe(2000);
    });
  });

  describe('submitAnswerStart', () => {
    it('should set submitting state', () => {
      const state = exerciseReducer(undefined, submitAnswerStart());

      expect(state.isSubmitting).toBe(true);
      expect(state.error).toBeNull();
    });

    it('should clear previous errors', () => {
      const initialState = {
        ...exerciseReducer(undefined, { type: 'unknown' }),
        error: 'previous error',
      };

      const state = exerciseReducer(initialState, submitAnswerStart());

      expect(state.error).toBeNull();
    });
  });

  describe('submitAnswerSuccess', () => {
    it('should add answer and move to next exercise', () => {
      const exercise2: Exercise = { ...mockExercise, id: '2' };
      const sessionWithMultiple = {
        ...mockSession,
        exercises: [mockExercise, exercise2],
      };

      const initialState = {
        ...exerciseReducer(undefined, { type: 'unknown' }),
        currentSession: sessionWithMultiple,
        currentExercise: mockExercise,
        isSubmitting: true,
      };

      const state = exerciseReducer(initialState, submitAnswerSuccess(mockAnswer));

      expect(state.isSubmitting).toBe(false);
      expect(state.currentSession?.answers).toHaveLength(1);
      expect(state.currentSession?.answers[0]).toEqual(mockAnswer);
      expect(state.currentSession?.currentIndex).toBe(1);
      expect(state.currentExercise).toEqual(exercise2);
      expect(state.currentAnswer).toBeNull();
      expect(state.hintsUsed).toBe(0);
      expect(state.timeElapsed).toBe(0);
    });

    it('should mark session as completed when no more exercises', () => {
      const initialState = {
        ...exerciseReducer(undefined, { type: 'unknown' }),
        currentSession: mockSession,
        currentExercise: mockExercise,
        isSubmitting: true,
      };

      const state = exerciseReducer(initialState, submitAnswerSuccess(mockAnswer));

      expect(state.isSubmitting).toBe(false);
      expect(state.currentSession?.completed).toBe(true);
      expect(state.currentSession?.endTime).toBeDefined();
      expect(state.currentExercise).toBeNull();
    });

    it('should handle null session gracefully', () => {
      const initialState = {
        ...exerciseReducer(undefined, { type: 'unknown' }),
        isSubmitting: true,
      };

      const state = exerciseReducer(initialState, submitAnswerSuccess(mockAnswer));

      expect(state.isSubmitting).toBe(false);
    });
  });

  describe('submitAnswerFailure', () => {
    it('should set error and stop submitting', () => {
      const initialState = {
        ...exerciseReducer(undefined, { type: 'unknown' }),
        isSubmitting: true,
      };

      const state = exerciseReducer(
        initialState,
        submitAnswerFailure('Network error')
      );

      expect(state.isSubmitting).toBe(false);
      expect(state.error).toBe('Network error');
    });
  });

  describe('endSession', () => {
    it('should mark session as completed and clear exercise data', () => {
      const initialState = {
        ...exerciseReducer(undefined, { type: 'unknown' }),
        currentSession: mockSession,
        currentExercise: mockExercise,
        currentAnswer: 'some answer',
        hintsUsed: 2,
        timeElapsed: 5000,
      };

      const state = exerciseReducer(initialState, endSession());

      expect(state.currentSession?.completed).toBe(true);
      expect(state.currentSession?.endTime).toBeDefined();
      expect(state.currentExercise).toBeNull();
      expect(state.currentAnswer).toBeNull();
      expect(state.hintsUsed).toBe(0);
      expect(state.timeElapsed).toBe(0);
    });

    it('should handle null session', () => {
      const state = exerciseReducer(undefined, endSession());

      expect(state.currentSession).toBeNull();
      expect(state.currentExercise).toBeNull();
    });
  });

  describe('clearError', () => {
    it('should clear error', () => {
      const initialState = {
        ...exerciseReducer(undefined, { type: 'unknown' }),
        error: 'Some error',
      };

      const state = exerciseReducer(initialState, clearError());

      expect(state.error).toBeNull();
    });
  });

  describe('resetExerciseState', () => {
    it('should reset to initial state', () => {
      const initialState = {
        currentSession: mockSession,
        currentExercise: mockExercise,
        currentAnswer: 'some answer',
        hintsUsed: 3,
        timeElapsed: 5000,
        isSubmitting: true,
        error: 'some error',
      };

      const state = exerciseReducer(initialState, resetExerciseState());

      expect(state).toEqual({
        currentSession: null,
        currentExercise: null,
        currentAnswer: null,
        hintsUsed: 0,
        timeElapsed: 0,
        isSubmitting: false,
        error: null,
      });
    });
  });
});

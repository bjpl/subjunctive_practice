import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import type { Exercise, PracticeSession, Answer } from "@/types";

interface ExerciseState {
  currentSession: PracticeSession | null;
  currentExercise: Exercise | null;
  currentAnswer: string | string[] | null;
  hintsUsed: number;
  timeElapsed: number;
  isSubmitting: boolean;
  error: string | null;
}

const initialState: ExerciseState = {
  currentSession: null,
  currentExercise: null,
  currentAnswer: null,
  hintsUsed: 0,
  timeElapsed: 0,
  isSubmitting: false,
  error: null,
};

const exerciseSlice = createSlice({
  name: "exercise",
  initialState,
  reducers: {
    startSession: (state, action: PayloadAction<PracticeSession>) => {
      state.currentSession = action.payload;
      state.currentExercise = action.payload.exercises[0] || null;
      state.currentAnswer = null;
      state.hintsUsed = 0;
      state.timeElapsed = 0;
      state.error = null;
    },
    setCurrentExercise: (state, action: PayloadAction<Exercise>) => {
      state.currentExercise = action.payload;
      state.currentAnswer = null;
      state.hintsUsed = 0;
      state.timeElapsed = 0;
    },
    setAnswer: (state, action: PayloadAction<string | string[]>) => {
      state.currentAnswer = action.payload;
    },
    useHint: (state) => {
      state.hintsUsed += 1;
    },
    updateTimeElapsed: (state, action: PayloadAction<number>) => {
      state.timeElapsed = action.payload;
    },
    submitAnswerStart: (state) => {
      state.isSubmitting = true;
      state.error = null;
    },
    submitAnswerSuccess: (state, action: PayloadAction<Answer>) => {
      state.isSubmitting = false;
      if (state.currentSession) {
        state.currentSession.answers.push(action.payload);
        const nextIndex = state.currentSession.currentIndex + 1;

        if (nextIndex < state.currentSession.exercises.length) {
          state.currentSession.currentIndex = nextIndex;
          state.currentExercise = state.currentSession.exercises[nextIndex];
          state.currentAnswer = null;
          state.hintsUsed = 0;
          state.timeElapsed = 0;
        } else {
          state.currentSession.completed = true;
          state.currentSession.endTime = new Date();
          state.currentExercise = null;
        }
      }
    },
    submitAnswerFailure: (state, action: PayloadAction<string>) => {
      state.isSubmitting = false;
      state.error = action.payload;
    },
    endSession: (state) => {
      if (state.currentSession) {
        state.currentSession.completed = true;
        state.currentSession.endTime = new Date();
      }
      state.currentExercise = null;
      state.currentAnswer = null;
      state.hintsUsed = 0;
      state.timeElapsed = 0;
    },
    clearError: (state) => {
      state.error = null;
    },
    resetExerciseState: () => initialState,
  },
});

export const {
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
} = exerciseSlice.actions;

export default exerciseSlice.reducer;

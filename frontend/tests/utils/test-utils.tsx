import React, { ReactElement } from 'react';
import { render, RenderOptions } from '@testing-library/react';
import { Provider } from 'react-redux';
import { configureStore, PreloadedState } from '@reduxjs/toolkit';
import authReducer from '@/store/slices/auth-slice';

// Mock store type
interface ExtendedRenderOptions extends Omit<RenderOptions, 'wrapper'> {
  preloadedState?: PreloadedState<RootState>;
  store?: ReturnType<typeof setupStore>;
}

// Create a test store
export function setupStore(preloadedState?: PreloadedState<RootState>) {
  return configureStore({
    reducer: {
      auth: authReducer,
    },
    preloadedState,
  });
}

export type RootState = ReturnType<ReturnType<typeof setupStore>['getState']>;
export type AppStore = ReturnType<typeof setupStore>;

// Custom render function with Redux provider
export function renderWithProviders(
  ui: ReactElement,
  {
    preloadedState = {},
    store = setupStore(preloadedState),
    ...renderOptions
  }: ExtendedRenderOptions = {}
) {
  function Wrapper({ children }: { children: React.ReactNode }) {
    return <Provider store={store}>{children}</Provider>;
  }

  return {
    store,
    ...render(ui, { wrapper: Wrapper, ...renderOptions }),
  };
}

// Mock user for testing
export const mockUser = {
  id: 1,
  email: 'test@example.com',
  username: 'testuser',
  createdAt: '2024-01-01T00:00:00.000Z',
};

// Mock authenticated state
export const mockAuthState = {
  auth: {
    user: mockUser,
    token: 'mock-token-123',
    isAuthenticated: true,
    isLoading: false,
    error: null,
  },
};

// Mock unauthenticated state
export const mockUnauthenticatedState = {
  auth: {
    user: null,
    token: null,
    isAuthenticated: false,
    isLoading: false,
    error: null,
  },
};

// Mock exercise data
export const mockExercise = {
  id: 1,
  verb: 'hablar',
  subject: 'yo',
  tense: 'present',
  difficulty: 'beginner',
  english: 'I speak',
  correctAnswer: 'hable',
};

// Mock session stats
export const mockSessionStats = {
  totalExercises: 150,
  correctAnswers: 120,
  accuracy: 80,
  currentStreak: 5,
  longestStreak: 12,
  totalPoints: 1200,
  level: 5,
};

// Helper to wait for API calls
export const waitForApiCall = (ms: number = 100) =>
  new Promise((resolve) => setTimeout(resolve, ms));

// Helper to fill form fields
export const fillFormField = async (
  container: HTMLElement,
  name: string,
  value: string
) => {
  const input = container.querySelector(`input[name="${name}"]`) as HTMLInputElement;
  if (input) {
    input.value = value;
    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.dispatchEvent(new Event('change', { bubbles: true }));
  }
};

// Re-export everything from React Testing Library
export * from '@testing-library/react';
export { default as userEvent } from '@testing-library/user-event';

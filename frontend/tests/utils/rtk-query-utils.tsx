import React, { ReactElement } from 'react';
import { render, RenderOptions } from '@testing-library/react';
import { Provider } from 'react-redux';
import { configureStore, PreloadedState } from '@reduxjs/toolkit';
import { setupListeners } from '@reduxjs/toolkit/query';
import authReducer from '@/store/slices/authSlice';
import exerciseReducer from '@/store/slices/exerciseSlice';
import progressReducer from '@/store/slices/progressSlice';
import uiReducer from '@/store/slices/uiSlice';
import settingsReducer from '@/store/slices/settingsSlice';
import { baseApi } from '@/store/api/baseApi';
import type { RootState } from '@/types/api';

/**
 * Create a test store with RTK Query support
 */
export function createTestStore(preloadedState?: PreloadedState<RootState>) {
  const store = configureStore({
    reducer: {
      auth: authReducer,
      exercise: exerciseReducer,
      progress: progressReducer,
      ui: uiReducer,
      settings: settingsReducer,
      [baseApi.reducerPath]: baseApi.reducer,
    },
    middleware: (getDefaultMiddleware) =>
      getDefaultMiddleware().concat(baseApi.middleware),
    preloadedState: preloadedState as any,
  });

  // Enable refetchOnFocus/refetchOnReconnect behaviors
  setupListeners(store.dispatch);

  return store;
}

export type TestStore = ReturnType<typeof createTestStore>;

interface ExtendedRenderOptions extends Omit<RenderOptions, 'wrapper'> {
  preloadedState?: PreloadedState<RootState>;
  store?: TestStore;
}

/**
 * Custom render function with Redux and RTK Query provider
 */
export function renderWithRTKQuery(
  ui: ReactElement,
  {
    preloadedState = {},
    store = createTestStore(preloadedState),
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

/**
 * Wait for RTK Query to finish all pending queries
 */
export async function waitForRTKQuery(store: TestStore, timeout = 2000) {
  const startTime = Date.now();

  while (Date.now() - startTime < timeout) {
    const state = store.getState();
    const queries = baseApi.util.selectInvalidatedBy(state, []);

    // Check if there are any pending queries
    const hasPendingQueries = Object.values(state[baseApi.reducerPath].queries).some(
      (query: any) => query?.status === 'pending'
    );

    const hasPendingMutations = Object.values(state[baseApi.reducerPath].mutations).some(
      (mutation: any) => mutation?.status === 'pending'
    );

    if (!hasPendingQueries && !hasPendingMutations) {
      return;
    }

    await new Promise(resolve => setTimeout(resolve, 50));
  }

  throw new Error('RTK Query requests did not complete within timeout');
}

/**
 * Mock authenticated user state
 */
export const mockAuthenticatedUser = {
  id: 1,
  username: 'testuser',
  email: 'test@example.com',
  full_name: 'Test User',
  role: 'user',
  is_active: true,
  is_verified: true,
  created_at: '2024-01-01T00:00:00Z',
  last_login: '2024-01-15T10:30:00Z',
};

/**
 * Mock authentication tokens
 */
export const mockTokens = {
  access_token: 'mock-access-token-123',
  refresh_token: 'mock-refresh-token-456',
  token_type: 'Bearer',
  expires_in: 3600,
};

/**
 * Preloaded authenticated state
 */
export const authenticatedState: Partial<RootState> = {
  auth: {
    user: mockAuthenticatedUser,
    accessToken: mockTokens.access_token,
    refreshToken: mockTokens.refresh_token,
    isAuthenticated: true,
    isLoading: false,
    error: null,
  },
};

/**
 * Preloaded unauthenticated state
 */
export const unauthenticatedState: Partial<RootState> = {
  auth: {
    user: null,
    accessToken: null,
    refreshToken: null,
    isAuthenticated: false,
    isLoading: false,
    error: null,
  },
};

// Re-export testing library utilities
export * from '@testing-library/react';
export { default as userEvent } from '@testing-library/user-event';

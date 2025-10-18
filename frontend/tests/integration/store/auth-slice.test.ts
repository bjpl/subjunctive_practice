import { configureStore } from '@reduxjs/toolkit';
import authReducer, { login, register, logout, clearError } from '@/store/slices/authSlice';
import { server } from '../../mocks/server';
import { http, HttpResponse } from 'msw';

// Mock the authApi to work with MSW
jest.mock('@/lib/api-client', () => ({
  authApi: {
    login: async (credentials: any) => {
      const response = await fetch('http://localhost:8000/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials),
      });
      if (!response.ok) {
        throw { response: { data: { detail: 'Invalid credentials' } } };
      }
      return response.json();
    },
    register: async (credentials: any) => {
      const response = await fetch('http://localhost:8000/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials),
      });
      if (!response.ok) {
        throw { response: { data: { detail: 'User already exists' } } };
      }
      return response.json();
    },
  },
}));

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

describe('Auth Slice', () => {
  let store: ReturnType<typeof configureStore>;

  beforeEach(() => {
    store = configureStore({
      reducer: {
        auth: authReducer,
      },
    });
  });

  describe('Initial State', () => {
    it('has correct initial state', () => {
      const state = store.getState().auth;
      expect(state).toEqual({
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      });
    });
  });

  describe('Reducers', () => {
    it('handles logout', () => {
      // Set authenticated state first
      store.dispatch({ type: 'auth/login/fulfilled', payload: { user: { id: 1 }, access_token: 'token' } });
      expect(store.getState().auth.isAuthenticated).toBe(true);

      // Logout
      store.dispatch(logout());
      const state = store.getState().auth;

      expect(state.user).toBeNull();
      expect(state.token).toBeNull();
      expect(state.isAuthenticated).toBe(false);
      expect(state.error).toBeNull();
    });

    it('handles clearError', () => {
      store.dispatch({ type: 'auth/login/rejected', payload: 'Error message' });
      expect(store.getState().auth.error).toBe('Error message');

      store.dispatch(clearError());
      expect(store.getState().auth.error).toBeNull();
    });
  });

  describe('Login Async Thunk', () => {
    it('handles successful login', async () => {
      const credentials = { email: 'test@example.com', password: 'password123' };
      const result = await store.dispatch(login(credentials));

      expect(result.type).toBe('auth/login/fulfilled');

      const state = store.getState().auth;
      expect(state.isAuthenticated).toBe(true);
      expect(state.user).toBeTruthy();
      expect(state.token).toBe('mock-token-123');
      expect(state.error).toBeNull();
      expect(state.isLoading).toBe(false);
    });

    it('handles login failure', async () => {
      const credentials = { email: 'wrong@example.com', password: 'wrongpass' };
      const result = await store.dispatch(login(credentials));

      expect(result.type).toBe('auth/login/rejected');

      const state = store.getState().auth;
      expect(state.isAuthenticated).toBe(false);
      expect(state.user).toBeNull();
      expect(state.token).toBeNull();
      expect(state.error).toBeTruthy();
      expect(state.isLoading).toBe(false);
    });

    it('sets loading state during login', async () => {
      const credentials = { email: 'test@example.com', password: 'password123' };
      const promise = store.dispatch(login(credentials));

      // Check loading state while pending
      expect(store.getState().auth.isLoading).toBe(true);

      await promise;

      // Check loading state after completion
      expect(store.getState().auth.isLoading).toBe(false);
    });
  });

  describe('Register Async Thunk', () => {
    it('handles successful registration', async () => {
      const credentials = {
        email: 'newuser@example.com',
        username: 'newuser',
        password: 'password123',
      };
      const result = await store.dispatch(register(credentials));

      expect(result.type).toBe('auth/register/fulfilled');

      const state = store.getState().auth;
      expect(state.isAuthenticated).toBe(true);
      expect(state.user).toBeTruthy();
      expect(state.user?.email).toBe('newuser@example.com');
      expect(state.token).toBe('mock-token-123');
      expect(state.error).toBeNull();
    });

    it('handles registration failure with existing user', async () => {
      const credentials = {
        email: 'existing@example.com',
        username: 'existing',
        password: 'password123',
      };
      const result = await store.dispatch(register(credentials));

      expect(result.type).toBe('auth/register/rejected');

      const state = store.getState().auth;
      expect(state.isAuthenticated).toBe(false);
      expect(state.error).toBeTruthy();
    });

    it('sets loading state during registration', async () => {
      const credentials = {
        email: 'test@example.com',
        username: 'test',
        password: 'password123',
      };
      const promise = store.dispatch(register(credentials));

      expect(store.getState().auth.isLoading).toBe(true);

      await promise;

      expect(store.getState().auth.isLoading).toBe(false);
    });
  });

  describe('Error Handling', () => {
    it('handles network errors during login', async () => {
      server.use(
        http.post(`${API_BASE_URL}/auth/login`, () => {
          return HttpResponse.error();
        })
      );

      const credentials = { email: 'test@example.com', password: 'password123' };
      const result = await store.dispatch(login(credentials));

      expect(result.type).toBe('auth/login/rejected');
      expect(store.getState().auth.error).toBeTruthy();
    });

    it('handles network errors during registration', async () => {
      server.use(
        http.post(`${API_BASE_URL}/auth/register`, () => {
          return HttpResponse.error();
        })
      );

      const credentials = {
        email: 'test@example.com',
        username: 'test',
        password: 'password123',
      };
      const result = await store.dispatch(register(credentials));

      expect(result.type).toBe('auth/register/rejected');
      expect(store.getState().auth.error).toBeTruthy();
    });
  });
});

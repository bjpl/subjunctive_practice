import { configureStore } from '@reduxjs/toolkit';
import authReducer, { login, register, logout, clearError } from '@/store/slices/auth-slice';
import { server } from '../../mocks/server';
import { http, HttpResponse } from 'msw';

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
      expect(state.error).toBe('Invalid credentials');
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
      expect(state.error).toBe('User already exists');
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

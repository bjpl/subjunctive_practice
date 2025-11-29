/**
 * Unit tests for useAuth hook
 * Tests authentication functionality including login, logout, registration, and token refresh
 */

import React from 'react';
import { renderHook, waitFor } from '@testing-library/react';
import { Provider } from 'react-redux';
import { useAuth } from '@/hooks/useAuth';
import {
  createTestStore,
  mockAuthenticatedUser,
  mockTokens,
  authenticatedState,
  unauthenticatedState
} from '../../utils/rtk-query-utils';
import { server } from '../../mocks/server';
import { http, HttpResponse } from 'msw';
import type { LoginCredentials, RegisterData } from '@/types/api';

const API_BASE_URL = 'http://localhost:8000/api';

describe('useAuth Hook', () => {
  let store: ReturnType<typeof createTestStore>;

  beforeEach(() => {
    store = createTestStore(unauthenticatedState);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  const wrapper = ({ children }: { children: React.ReactNode }) => {
    return <Provider store={store}>{children}</Provider>;
  };

  describe('Initial State', () => {
    it('should return unauthenticated state by default', () => {
      const { result } = renderHook(() => useAuth(), { wrapper });

      expect(result.current.user).toBeNull();
      expect(result.current.accessToken).toBeNull();
      expect(result.current.refreshToken).toBeNull();
      expect(result.current.isAuthenticated).toBe(false);
      expect(result.current.isLoading).toBe(false);
      expect(result.current.error).toBeNull();
    });

    it('should return authenticated state when user is logged in', () => {
      store = createTestStore(authenticatedState);
      const wrapper = ({ children }: { children: React.ReactNode }) => (
        <Provider store={store}>{children}</Provider>
      );

      const { result } = renderHook(() => useAuth(), { wrapper });

      expect(result.current.user).toEqual(mockAuthenticatedUser);
      expect(result.current.accessToken).toBe(mockTokens.access_token);
      expect(result.current.refreshToken).toBe(mockTokens.refresh_token);
      expect(result.current.isAuthenticated).toBe(true);
    });
  });

  describe('Login Functionality', () => {
    it('should successfully login with valid credentials', async () => {
      // Mock successful login
      server.use(
        http.post(`${API_BASE_URL}/auth/login`, () => {
          return HttpResponse.json(mockTokens);
        }),
        http.get(`${API_BASE_URL}/auth/me`, () => {
          return HttpResponse.json(mockAuthenticatedUser);
        })
      );

      const { result } = renderHook(() => useAuth(), { wrapper });

      const credentials: LoginCredentials = {
        username: 'testuser',
        password: 'password123',
      };

      await waitFor(async () => {
        const loginResult = await result.current.login(credentials);
        expect(loginResult.tokens).toEqual(mockTokens);
        expect(loginResult.user).toEqual(mockAuthenticatedUser);
      });

      // Verify state updated
      await waitFor(() => {
        expect(result.current.isAuthenticated).toBe(true);
        expect(result.current.user).toEqual(mockAuthenticatedUser);
        expect(result.current.accessToken).toBe(mockTokens.access_token);
      });
    });

    it('should handle login failure with invalid credentials', async () => {
      // Mock failed login
      server.use(
        http.post(`${API_BASE_URL}/auth/login`, () => {
          return HttpResponse.json(
            { detail: 'Invalid credentials' },
            { status: 401 }
          );
        })
      );

      const { result } = renderHook(() => useAuth(), { wrapper });

      const credentials: LoginCredentials = {
        username: 'wronguser',
        password: 'wrongpass',
      };

      await expect(result.current.login(credentials)).rejects.toThrow();

      // Verify state remains unauthenticated
      expect(result.current.isAuthenticated).toBe(false);
      expect(result.current.user).toBeNull();
    });

    it('should handle network errors during login', async () => {
      // Mock network error
      server.use(
        http.post(`${API_BASE_URL}/auth/login`, () => {
          return HttpResponse.error();
        })
      );

      const { result } = renderHook(() => useAuth(), { wrapper });

      const credentials: LoginCredentials = {
        username: 'testuser',
        password: 'password123',
      };

      await expect(result.current.login(credentials)).rejects.toThrow();
    });

    it('should handle failure to fetch user data after successful token retrieval', async () => {
      server.use(
        http.post(`${API_BASE_URL}/auth/login`, () => {
          return HttpResponse.json(mockTokens);
        }),
        http.get(`${API_BASE_URL}/auth/me`, () => {
          return HttpResponse.json(
            { detail: 'User not found' },
            { status: 404 }
          );
        })
      );

      const { result } = renderHook(() => useAuth(), { wrapper });

      const credentials: LoginCredentials = {
        username: 'testuser',
        password: 'password123',
      };

      await expect(result.current.login(credentials)).rejects.toThrow('Failed to fetch user data');
    });
  });

  describe('Logout Functionality', () => {
    it('should successfully logout and clear authentication state', async () => {
      // Start with authenticated state
      store = createTestStore(authenticatedState);
      const wrapper = ({ children }: { children: React.ReactNode }) => (
        <Provider store={store}>{children}</Provider>
      );

      const { result } = renderHook(() => useAuth(), { wrapper });

      // Verify initially authenticated
      expect(result.current.isAuthenticated).toBe(true);

      // Logout
      result.current.logout();

      // Verify state cleared
      await waitFor(() => {
        expect(result.current.isAuthenticated).toBe(false);
        expect(result.current.user).toBeNull();
        expect(result.current.accessToken).toBeNull();
        expect(result.current.refreshToken).toBeNull();
      });
    });
  });

  describe('Registration Functionality', () => {
    it('should successfully register a new user and auto-login', async () => {
      const registerData: RegisterData = {
        username: 'newuser',
        email: 'new@example.com',
        password: 'password123',
        full_name: 'New User',
      };

      server.use(
        http.post(`${API_BASE_URL}/auth/register`, () => {
          return HttpResponse.json({
            ...mockAuthenticatedUser,
            username: registerData.username,
            email: registerData.email,
          });
        }),
        http.post(`${API_BASE_URL}/auth/login`, () => {
          return HttpResponse.json(mockTokens);
        }),
        http.get(`${API_BASE_URL}/auth/me`, () => {
          return HttpResponse.json({
            ...mockAuthenticatedUser,
            username: registerData.username,
            email: registerData.email,
          });
        })
      );

      const { result } = renderHook(() => useAuth(), { wrapper });

      await waitFor(async () => {
        const registerResult = await result.current.register(registerData);
        expect(registerResult.user.username).toBe(registerData.username);
        expect(registerResult.user.email).toBe(registerData.email);
      });

      // Verify automatically logged in
      await waitFor(() => {
        expect(result.current.isAuthenticated).toBe(true);
        expect(result.current.user?.username).toBe(registerData.username);
      });
    });

    it('should handle registration failure with existing email', async () => {
      server.use(
        http.post(`${API_BASE_URL}/auth/register`, () => {
          return HttpResponse.json(
            { detail: 'Email already exists' },
            { status: 400 }
          );
        })
      );

      const { result } = renderHook(() => useAuth(), { wrapper });

      const registerData: RegisterData = {
        username: 'testuser',
        email: 'existing@example.com',
        password: 'password123',
      };

      await expect(result.current.register(registerData)).rejects.toThrow();
      expect(result.current.isAuthenticated).toBe(false);
    });
  });

  describe('Token Refresh Functionality', () => {
    it('should successfully refresh access token', async () => {
      const newTokens = {
        ...mockTokens,
        access_token: 'new-access-token-789',
      };

      server.use(
        http.post(`${API_BASE_URL}/auth/refresh`, () => {
          return HttpResponse.json(newTokens);
        })
      );

      // Start with authenticated state
      store = createTestStore(authenticatedState);
      const wrapper = ({ children }: { children: React.ReactNode }) => (
        <Provider store={store}>{children}</Provider>
      );

      const { result } = renderHook(() => useAuth(), { wrapper });

      await waitFor(async () => {
        const refreshedTokens = await result.current.refreshAccessToken();
        expect(refreshedTokens).toEqual(newTokens);
      });

      // Verify token updated in state
      await waitFor(() => {
        expect(result.current.accessToken).toBe(newTokens.access_token);
      });
    });

    it('should logout on token refresh failure', async () => {
      server.use(
        http.post(`${API_BASE_URL}/auth/refresh`, () => {
          return HttpResponse.json(
            { detail: 'Invalid refresh token' },
            { status: 401 }
          );
        })
      );

      // Start with authenticated state
      store = createTestStore(authenticatedState);
      const wrapper = ({ children }: { children: React.ReactNode }) => (
        <Provider store={store}>{children}</Provider>
      );

      const { result } = renderHook(() => useAuth(), { wrapper });

      await expect(result.current.refreshAccessToken()).rejects.toThrow();

      // Verify logged out
      await waitFor(() => {
        expect(result.current.isAuthenticated).toBe(false);
        expect(result.current.user).toBeNull();
      });
    });

    it('should return null when no refresh token available', async () => {
      const { result } = renderHook(() => useAuth(), { wrapper });

      const refreshResult = await result.current.refreshAccessToken();
      expect(refreshResult).toBeNull();
    });
  });

  describe('Error Handling', () => {
    it('should clear error state', () => {
      store = createTestStore({
        ...unauthenticatedState,
        auth: {
          ...unauthenticatedState.auth!,
          error: 'Some error occurred',
        },
      });

      const wrapper = ({ children }: { children: React.ReactNode }) => (
        <Provider store={store}>{children}</Provider>
      );

      const { result } = renderHook(() => useAuth(), { wrapper });

      expect(result.current.error).toBe('Some error occurred');

      result.current.clearError();

      waitFor(() => {
        expect(result.current.error).toBeNull();
      });
    });
  });

  describe('Loading States', () => {
    it('should show loading state during login', async () => {
      let resolveLogin: (value: any) => void;
      const loginPromise = new Promise((resolve) => {
        resolveLogin = resolve;
      });

      server.use(
        http.post(`${API_BASE_URL}/auth/login`, async () => {
          await loginPromise;
          return HttpResponse.json(mockTokens);
        }),
        http.get(`${API_BASE_URL}/auth/me`, () => {
          return HttpResponse.json(mockAuthenticatedUser);
        })
      );

      const { result } = renderHook(() => useAuth(), { wrapper });

      const loginAttempt = result.current.login({
        username: 'testuser',
        password: 'password123',
      });

      // Should be loading
      await waitFor(() => {
        expect(result.current.isLoading).toBe(true);
      });

      // Resolve the login
      resolveLogin!(undefined);
      await loginAttempt;

      // Should finish loading
      await waitFor(() => {
        expect(result.current.isLoading).toBe(false);
      });
    });
  });
});

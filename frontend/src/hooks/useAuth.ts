/**
 * Authentication state and actions hook
 */

import { useCallback } from 'react';
import { useAppSelector } from './useAppSelector';
import { useAppDispatch } from './useAppDispatch';
import {
  setCredentials,
  logout as logoutAction,
  clearError as clearAuthError,
} from '../store/slices/authSlice';
import {
  useLoginMutation,
  useRegisterMutation,
  useRefreshTokenMutation,
} from '../store/api/authApi';
import type { LoginCredentials, RegisterData, ApiUser, TokenResponse } from '../types/api';

export const useAuth = () => {
  const dispatch = useAppDispatch();

  // Selectors
  const user = useAppSelector((state) => state.auth.user);
  const accessToken = useAppSelector((state) => state.auth.accessToken);
  const refreshToken = useAppSelector((state) => state.auth.refreshToken);
  const isAuthenticated = useAppSelector((state) => state.auth.isAuthenticated);
  const error = useAppSelector((state) => state.auth.error);

  // Mutations
  const [loginMutation, { isLoading: isLoggingIn }] = useLoginMutation();
  const [registerMutation, { isLoading: isRegistering }] = useRegisterMutation();
  const [refreshMutation] = useRefreshTokenMutation();

  // Login
  const login = useCallback(
    async (credentials: LoginCredentials) => {
      try {
        // Step 1: Login to get tokens
        const tokens = await loginMutation(credentials).unwrap();

        // Step 2: Fetch user data using the new token
        const userResponse = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'}/auth/me`,
          {
            headers: {
              Authorization: `Bearer ${tokens.access_token}`,
            },
          }
        );

        if (!userResponse.ok) {
          throw new Error('Failed to fetch user data');
        }

        const user: ApiUser = await userResponse.json();

        // Step 3: Store both tokens and user in Redux state
        dispatch(setCredentials({ tokens, user }));

        return { tokens, user };
      } catch (err) {
        throw err;
      }
    },
    [loginMutation, dispatch]
  );

  // Register
  const register = useCallback(
    async (data: RegisterData) => {
      try {
        // Step 1: Register user (returns user object directly)
        const user = await registerMutation(data).unwrap();

        // Step 2: Automatically log in with the new credentials
        const loginResult = await login({
          username: data.username,
          password: data.password,
        });

        return loginResult;
      } catch (err) {
        throw err;
      }
    },
    [registerMutation, login]
  );

  // Logout
  const logout = useCallback(() => {
    dispatch(logoutAction());
  }, [dispatch]);

  // Refresh token
  const refreshAccessToken = useCallback(async () => {
    if (!refreshToken) return null;
    try {
      const tokens = await refreshMutation({ refresh_token: refreshToken }).unwrap();
      dispatch(setCredentials({ user: user!, tokens }));
      return tokens;
    } catch (err) {
      dispatch(logoutAction());
      throw err;
    }
  }, [refreshToken, refreshMutation, dispatch, user]);

  // Clear error
  const clearError = useCallback(() => {
    dispatch(clearAuthError());
  }, [dispatch]);

  return {
    // State
    user,
    accessToken,
    refreshToken,
    isAuthenticated,
    isLoading: isLoggingIn || isRegistering,
    error,

    // Actions
    login,
    register,
    logout,
    refreshAccessToken,
    clearError,
  };
};

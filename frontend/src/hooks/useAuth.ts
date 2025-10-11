/**
 * Authentication state and actions hook
 */

import { useCallback } from 'react';
import { useAppSelector } from './useAppSelector';
import { useAppDispatch } from './useAppDispatch';
import {
  setCredentials,
  logout as logoutAction,
  clearAuthError,
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
  const isLoading = useAppSelector((state) => state.auth.isLoading);
  const error = useAppSelector((state) => state.auth.error);

  // Mutations
  const [loginMutation, { isLoading: isLoggingIn }] = useLoginMutation();
  const [registerMutation, { isLoading: isRegistering }] = useRegisterMutation();
  const [refreshMutation] = useRefreshTokenMutation();

  // Login
  const login = useCallback(
    async (credentials: LoginCredentials) => {
      try {
        const tokens = await loginMutation(credentials).unwrap();
        // Get user data from token or make separate request
        const userData: ApiUser = {
          user_id: 'temp', // Will be updated by getCurrentUser
          username: credentials.username,
          email: '',
          created_at: new Date().toISOString(),
        };
        dispatch(setCredentials({ user: userData, tokens }));
        return tokens;
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
        const user = await registerMutation(data).unwrap();
        return user;
      } catch (err) {
        throw err;
      }
    },
    [registerMutation]
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
    isLoading: isLoading || isLoggingIn || isRegistering,
    error,

    // Actions
    login,
    register,
    logout,
    refreshAccessToken,
    clearError,
  };
};

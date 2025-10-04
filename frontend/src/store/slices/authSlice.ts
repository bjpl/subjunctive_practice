/**
 * Authentication state slice
 */

import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { AuthState, User, TokenResponse } from '../../types';
import { getStorageItem, setStorageItem, removeStorageItem, StorageKeys } from '../../lib/storage';

const initialState: AuthState = {
  user: getStorageItem<User | null>(StorageKeys.USER_DATA, null),
  accessToken: getStorageItem<string | null>(StorageKeys.AUTH_TOKEN, null),
  refreshToken: getStorageItem<string | null>(StorageKeys.REFRESH_TOKEN, null),
  isAuthenticated: !!getStorageItem<string | null>(StorageKeys.AUTH_TOKEN, null),
  isLoading: false,
  error: null,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    setCredentials: (
      state,
      action: PayloadAction<{ user: User; tokens: TokenResponse }>
    ) => {
      const { user, tokens } = action.payload;
      state.user = user;
      state.accessToken = tokens.access_token;
      state.refreshToken = tokens.refresh_token;
      state.isAuthenticated = true;
      state.error = null;

      // Persist to localStorage
      setStorageItem(StorageKeys.USER_DATA, user);
      setStorageItem(StorageKeys.AUTH_TOKEN, tokens.access_token);
      setStorageItem(StorageKeys.REFRESH_TOKEN, tokens.refresh_token);
    },

    updateTokens: (state, action: PayloadAction<TokenResponse>) => {
      state.accessToken = action.payload.access_token;
      state.refreshToken = action.payload.refresh_token;

      // Persist to localStorage
      setStorageItem(StorageKeys.AUTH_TOKEN, action.payload.access_token);
      setStorageItem(StorageKeys.REFRESH_TOKEN, action.payload.refresh_token);
    },

    updateUser: (state, action: PayloadAction<User>) => {
      state.user = action.payload;
      setStorageItem(StorageKeys.USER_DATA, action.payload);
    },

    setAuthLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },

    setAuthError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
      state.isLoading = false;
    },

    logout: (state) => {
      state.user = null;
      state.accessToken = null;
      state.refreshToken = null;
      state.isAuthenticated = false;
      state.error = null;

      // Clear from localStorage
      removeStorageItem(StorageKeys.USER_DATA);
      removeStorageItem(StorageKeys.AUTH_TOKEN);
      removeStorageItem(StorageKeys.REFRESH_TOKEN);
    },

    clearAuthError: (state) => {
      state.error = null;
    },
  },
});

export const {
  setCredentials,
  updateTokens,
  updateUser,
  setAuthLoading,
  setAuthError,
  logout,
  clearAuthError,
} = authSlice.actions;

export default authSlice.reducer;

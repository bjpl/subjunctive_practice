/**
 * Memoized selectors for authentication state
 */

import { createSelector } from '@reduxjs/toolkit';
import type { RootState } from '../store';

// Base selectors
const selectAuthState = (state: RootState) => state.auth;

// Memoized selectors
export const selectCurrentUser = createSelector(
  [selectAuthState],
  (auth) => auth.user
);

export const selectIsAuthenticated = createSelector(
  [selectAuthState],
  (auth) => auth.isAuthenticated
);

export const selectAccessToken = createSelector(
  [selectAuthState],
  (auth) => auth.accessToken
);

export const selectRefreshToken = createSelector(
  [selectAuthState],
  (auth) => auth.refreshToken
);

export const selectAuthLoading = createSelector(
  [selectAuthState],
  (auth) => auth.isLoading
);

export const selectAuthError = createSelector(
  [selectAuthState],
  (auth) => auth.error
);

export const selectUserEmail = createSelector(
  [selectCurrentUser],
  (user) => user?.email || null
);

export const selectUsername = createSelector(
  [selectCurrentUser],
  (user) => user?.username || null
);

export const selectUserFullName = createSelector(
  [selectCurrentUser],
  (user) => user?.full_name || null
);

export const selectHasValidToken = createSelector(
  [selectAccessToken, selectIsAuthenticated],
  (token, isAuth) => !!token && isAuth
);

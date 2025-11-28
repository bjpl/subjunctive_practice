import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { authApi } from "@/store/api/authApi";
import type { ApiUser, TokenResponse } from "@/types/api";

interface AuthState {
  user: ApiUser | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  error: string | null;
}

const initialState: AuthState = {
  user: null,
  accessToken: null,
  refreshToken: null,
  isAuthenticated: false,
  error: null,
};

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    setCredentials: (
      state,
      action: PayloadAction<{ tokens: TokenResponse; user: ApiUser }>
    ) => {
      state.accessToken = action.payload.tokens.access_token;
      state.refreshToken = action.payload.tokens.refresh_token;
      state.user = action.payload.user;
      state.isAuthenticated = true;
      state.error = null;
    },
    setTokens: (state, action: PayloadAction<TokenResponse>) => {
      state.accessToken = action.payload.access_token;
      state.refreshToken = action.payload.refresh_token;
      state.isAuthenticated = true;
      state.error = null;
    },
    setUser: (state, action: PayloadAction<ApiUser>) => {
      state.user = action.payload;
    },
    logout: (state) => {
      state.user = null;
      state.accessToken = null;
      state.refreshToken = null;
      state.isAuthenticated = false;
      state.error = null;
    },
    setError: (state, action: PayloadAction<string>) => {
      state.error = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Handle login success
      .addMatcher(
        authApi.endpoints.login.matchFulfilled,
        (state, action) => {
          state.accessToken = action.payload.access_token;
          state.refreshToken = action.payload.refresh_token;
          state.isAuthenticated = true;
          state.error = null;
        }
      )
      // Handle login error
      .addMatcher(
        authApi.endpoints.login.matchRejected,
        (state, action) => {
          state.error = action.error.message || "Login failed";
          state.isAuthenticated = false;
        }
      )
      // Handle getCurrentUser success
      .addMatcher(
        authApi.endpoints.getCurrentUser.matchFulfilled,
        (state, action) => {
          state.user = action.payload;
        }
      )
      // Handle getCurrentUser error
      .addMatcher(
        authApi.endpoints.getCurrentUser.matchRejected,
        (state) => {
          // If fetching user fails, clear auth state
          state.user = null;
          state.accessToken = null;
          state.refreshToken = null;
          state.isAuthenticated = false;
        }
      )
      // Handle register success
      .addMatcher(
        authApi.endpoints.register.matchFulfilled,
        (state, action) => {
          // Registration returns a user directly
          state.user = action.payload;
          state.error = null;
        }
      )
      // Handle register error
      .addMatcher(
        authApi.endpoints.register.matchRejected,
        (state, action) => {
          state.error = action.error.message || "Registration failed";
        }
      )
      // Handle logout
      .addMatcher(
        authApi.endpoints.logout.matchFulfilled,
        (state) => {
          state.user = null;
          state.accessToken = null;
          state.refreshToken = null;
          state.isAuthenticated = false;
          state.error = null;
        }
      )
      // Handle token refresh
      .addMatcher(
        authApi.endpoints.refreshToken.matchFulfilled,
        (state, action) => {
          state.accessToken = action.payload.access_token;
          state.refreshToken = action.payload.refresh_token;
        }
      );
  },
});

export const {
  setCredentials,
  setTokens,
  setUser,
  logout,
  setError,
  clearError,
} = authSlice.actions;

export default authSlice.reducer;

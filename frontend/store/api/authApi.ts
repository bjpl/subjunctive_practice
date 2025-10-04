/**
 * Authentication API endpoints
 */

import { baseApi } from './baseApi';
import type {
  ApiUser,
  LoginCredentials,
  RegisterData,
  TokenResponse,
} from '@/types/api';

export const authApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    // Login
    login: builder.mutation<TokenResponse, LoginCredentials>({
      query: (credentials) => ({
        url: '/auth/login',
        method: 'POST',
        body: credentials,
      }),
      invalidatesTags: ['User'],
    }),

    // Register
    register: builder.mutation<ApiUser, RegisterData>({
      query: (userData) => ({
        url: '/auth/register',
        method: 'POST',
        body: userData,
      }),
    }),

    // Refresh token
    refreshToken: builder.mutation<TokenResponse, { refresh_token: string }>({
      query: (body) => ({
        url: '/auth/refresh',
        method: 'POST',
        body,
      }),
    }),

    // Get current user
    getCurrentUser: builder.query<ApiUser, void>({
      query: () => '/auth/me',
      providesTags: ['User'],
    }),

    // Logout (client-side only, clears state)
    logout: builder.mutation<void, void>({
      queryFn: () => ({ data: undefined }),
      invalidatesTags: ['User', 'Progress', 'Statistics'],
    }),
  }),
});

export const {
  useLoginMutation,
  useRegisterMutation,
  useRefreshTokenMutation,
  useGetCurrentUserQuery,
  useLogoutMutation,
} = authApi;

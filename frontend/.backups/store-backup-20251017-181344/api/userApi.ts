/**
 * User profile and settings API endpoints
 */

import { baseApi } from './baseApi';
import type { ApiUser, UserSettings } from '@/types/api';

export const userApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    // Get user profile
    getUserProfile: builder.query<ApiUser, void>({
      query: () => '/auth/me',
      providesTags: ['User'],
    }),

    // Update user settings
    updateSettings: builder.mutation<UserSettings, Partial<UserSettings>>({
      query: (settings) => ({
        url: '/user/settings',
        method: 'PATCH',
        body: settings,
      }),
      invalidatesTags: ['Settings'],
    }),

    // Get user settings
    getSettings: builder.query<UserSettings, void>({
      query: () => '/user/settings',
      providesTags: ['Settings'],
    }),

    // Update user profile
    updateProfile: builder.mutation<ApiUser, Partial<ApiUser>>({
      query: (profile) => ({
        url: '/user/profile',
        method: 'PATCH',
        body: profile,
      }),
      invalidatesTags: ['User'],
    }),
  }),
});

export const {
  useGetUserProfileQuery,
  useUpdateSettingsMutation,
  useGetSettingsQuery,
  useUpdateProfileMutation,
  useLazyGetSettingsQuery,
} = userApi;

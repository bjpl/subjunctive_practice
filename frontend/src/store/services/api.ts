import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import type { RootState } from "../store";

const baseQuery = fetchBaseQuery({
  baseUrl: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api",
  prepareHeaders: (headers, { getState }) => {
    const token = (getState() as RootState).auth.accessToken;
    if (token) {
      headers.set("authorization", `Bearer ${token}`);
    }
    headers.set("Content-Type", "application/json");
    return headers;
  },
});

export const api = createApi({
  reducerPath: "api",
  baseQuery,
  tagTypes: ["User", "Exercise", "Progress", "Statistics"],
  endpoints: (builder) => ({
    // Example endpoint - will be expanded later
    getCurrentUser: builder.query({
      query: () => "/auth/me",
      providesTags: ["User"],
    }),
  }),
});

export const { useGetCurrentUserQuery } = api;

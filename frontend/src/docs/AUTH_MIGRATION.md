# Authentication Migration Guide

## Overview

The authentication system has been migrated from Axios-based async thunks to RTK Query for better consistency and automatic caching/refetching.

## Key Changes

### 1. Auth State Structure

**Before:**
```typescript
interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}
```

**After:**
```typescript
interface AuthState {
  user: ApiUser | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  error: string | null;
}
```

Note: `isLoading` is now managed by RTK Query hooks instead of global state.

### 2. User Type

**Before:**
```typescript
interface User {
  id: string;  // String ID
  // ...
}
```

**After:**
```typescript
interface ApiUser {
  id: number;  // Matches backend (numeric ID)
  username: string;
  email: string;
  full_name?: string;
  role: string;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  last_login?: string | null;
}
```

### 3. Login Flow

**Backend Response:**
```json
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

**Important:** Login returns ONLY tokens. User data must be fetched separately via `/auth/me`.

## Migration Examples

### Before (Async Thunks)

```typescript
import { useDispatch, useSelector } from 'react-redux';
import { login, register, logout } from '@/store/slices/authSlice';

const MyComponent = () => {
  const dispatch = useDispatch();
  const { user, isLoading, error } = useSelector((state) => state.auth);

  const handleLogin = async (credentials) => {
    await dispatch(login(credentials));
  };

  // ...
};
```

### After (RTK Query + Custom Hook)

```typescript
import { useAuth } from '@/hooks/useAuth';

const MyComponent = () => {
  const { user, isLoading, error, login, register, logout } = useAuth();

  const handleLogin = async (credentials) => {
    try {
      const { tokens, user } = await login(credentials);
      console.log('Login successful:', user);
    } catch (err) {
      console.error('Login failed:', err);
    }
  };

  // ...
};
```

## How It Works

### Login Process

1. **Call login mutation** → Returns `TokenResponse`
2. **Fetch user data** → Call `/auth/me` with access token
3. **Store in Redux** → Save both tokens and user data
4. **Automatic header injection** → baseApi automatically adds token to all requests

### Register Process

1. **Call register mutation** → Returns `ApiUser`
2. **Auto-login** → Automatically logs in with provided credentials
3. **Complete flow** → Returns both tokens and user data

### Logout Process

1. **Call logout mutation** → Clears API cache
2. **Clear Redux state** → Removes tokens and user data
3. **No backend call** → Logout is client-side only

## Using the useAuth Hook

```typescript
import { useAuth } from '@/hooks/useAuth';

const LoginPage = () => {
  const { login, isLoading, error } = useAuth();

  const handleSubmit = async (credentials) => {
    try {
      const result = await login(credentials);
      // Navigate to dashboard or home
    } catch (err) {
      // Handle error
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields */}
      <button type="submit" disabled={isLoading}>
        {isLoading ? 'Logging in...' : 'Login'}
      </button>
      {error && <div className="error">{error}</div>}
    </form>
  );
};
```

## Direct RTK Query Usage

If you need more control, use the RTK Query hooks directly:

```typescript
import {
  useLoginMutation,
  useGetCurrentUserQuery,
  useLogoutMutation,
} from '@/store/api/authApi';
import { useDispatch } from 'react-redux';
import { setCredentials, logout } from '@/store/slices/authSlice';

const MyComponent = () => {
  const dispatch = useDispatch();
  const [loginMutation] = useLoginMutation();
  const { data: user, isLoading } = useGetCurrentUserQuery();

  const handleLogin = async (credentials) => {
    // Step 1: Get tokens
    const tokens = await loginMutation(credentials).unwrap();

    // Step 2: Fetch user
    const userResponse = await fetch(`${API_URL}/auth/me`, {
      headers: { Authorization: `Bearer ${tokens.access_token}` },
    });
    const userData = await userResponse.json();

    // Step 3: Store in Redux
    dispatch(setCredentials({ tokens, user: userData }));
  };
};
```

## Token Refresh

```typescript
const { refreshAccessToken } = useAuth();

// Manually refresh token
const newTokens = await refreshAccessToken();
```

The baseApi automatically includes the access token in all requests via `prepareHeaders`.

## Protected Routes

```typescript
import { useAuth } from '@/hooks/useAuth';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) return <LoadingSpinner />;
  if (!isAuthenticated) return <Navigate to="/login" />;

  return children;
};
```

## API Endpoints

All authentication endpoints are defined in `src/store/api/authApi.ts`:

- `useLoginMutation()` - POST `/auth/login`
- `useRegisterMutation()` - POST `/auth/register`
- `useRefreshTokenMutation()` - POST `/auth/refresh`
- `useGetCurrentUserQuery()` - GET `/auth/me`
- `useLogoutMutation()` - Client-side only

## Common Issues

### Issue: "Cannot read property 'id' of null"

**Cause:** Trying to access `user.id` before user data is fetched.

**Solution:**
```typescript
const { user } = useAuth();

// Safe access
const userId = user?.id;

// Or conditional rendering
{user && <div>Welcome, {user.username}!</div>}
```

### Issue: "401 Unauthorized" on API calls

**Cause:** Token not being sent with requests.

**Solution:** Ensure you're using the RTK Query hooks from `src/store/api/`, not the deprecated Axios client.

### Issue: User ID type mismatch

**Cause:** Frontend expecting `string`, backend returns `number`.

**Solution:** Use `ApiUser` type from `@/types/api` instead of `User` from `@/types`.

## Deprecated Files

- `src/lib/api-client.ts` - Use RTK Query instead
- Old async thunks in authSlice - Removed in favor of RTK Query matchers

## Testing

```typescript
import { renderWithProviders } from '@/test-utils';
import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('login flow', async () => {
  const { store } = renderWithProviders(<LoginPage />);

  await userEvent.type(screen.getByLabelText(/username/i), 'testuser');
  await userEvent.type(screen.getByLabelText(/password/i), 'password123');
  await userEvent.click(screen.getByRole('button', { name: /login/i }));

  await waitFor(() => {
    expect(store.getState().auth.isAuthenticated).toBe(true);
    expect(store.getState().auth.user).toBeTruthy();
  });
});
```

## Additional Resources

- [RTK Query Documentation](https://redux-toolkit.js.org/rtk-query/overview)
- [Backend API Documentation](../../backend/docs/API.md)
- [Type Definitions](../types/api.ts)

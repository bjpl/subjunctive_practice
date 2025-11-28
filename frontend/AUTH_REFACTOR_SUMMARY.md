# Authentication Refactor Summary

## Overview
Migrated frontend authentication from Axios-based async thunks to RTK Query for better consistency, type safety, and automatic caching.

## Changes Made

### 1. Updated `src/store/slices/authSlice.ts`
**Removed:**
- Axios-based `createAsyncThunk` for login/register
- `isLoading` field from state (now handled by RTK Query hooks)
- Dependency on `@/lib/api-client.ts`

**Added:**
- RTK Query matchers for handling API responses
- New actions: `setCredentials`, `setTokens`, `setUser`, `setError`
- Support for both `accessToken` and `refreshToken`
- Proper `ApiUser` type (with `id: number` instead of `id: string`)

**State Structure:**
```typescript
interface AuthState {
  user: ApiUser | null;
  accessToken: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  error: string | null;
}
```

### 2. Updated `src/hooks/useAuth.ts`
**Fixed:**
- Login flow now fetches user data after receiving tokens
- Register flow automatically logs in after registration
- Removed reference to non-existent `state.auth.isLoading`
- Proper error handling with type safety

**Login Flow:**
1. Call login mutation → Get tokens
2. Fetch user data via `/auth/me` with access token
3. Store both tokens and user in Redux state
4. Return `{ tokens, user }` to caller

**Register Flow:**
1. Call register mutation → Get user object
2. Automatically call login with provided credentials
3. Complete login flow (fetch tokens + user)
4. Return login result

### 3. Updated `src/types/index.ts`
**Changed:**
- `User.id` from `string` to `number` to match backend
- Added comment to use `@/types/api.ts` for API-specific types

**Added:**
- `LoginCredentials` interface
- `RegisterData` interface
- `LoginResponse` interface (matches backend `TokenResponse`)

### 4. Deprecated `src/lib/api-client.ts`
- Added deprecation notice at top of file
- File kept for backward compatibility but should not be used
- Will be removed in future version

### 5. Created Documentation
**New Files:**
- `src/docs/AUTH_MIGRATION.md` - Comprehensive migration guide
- `AUTH_REFACTOR_SUMMARY.md` (this file) - Summary of changes

## Backend Integration

### Login Endpoint Response
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "expires_in": 86400
}
```
**Important:** Login returns ONLY tokens, not user data.

### Get Current User Endpoint
```
GET /auth/me
Authorization: Bearer {access_token}
```
**Returns:**
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "full_name": "Test User",
  "role": "user",
  "is_active": true,
  "is_verified": false,
  "created_at": "2025-11-27T10:00:00Z",
  "last_login": "2025-11-27T10:00:00Z"
}
```

## Type Alignment

### Frontend → Backend Mapping

| Frontend (ApiUser) | Backend (UserResponse) | Type |
|-------------------|------------------------|------|
| `id` | `id` | `number` |
| `username` | `username` | `string` |
| `email` | `email` | `string` |
| `full_name` | `full_name` | `string \| null` |
| `role` | `role` | `string` |
| `is_active` | `is_active` | `boolean` |
| `is_verified` | `is_verified` | `boolean` |
| `created_at` | `created_at` | `string` (ISO 8601) |
| `last_login` | `last_login` | `string \| null` |

### Token Types

| Frontend (TokenResponse) | Backend (Token) | Type |
|-------------------------|-----------------|------|
| `access_token` | `access_token` | `string` |
| `refresh_token` | `refresh_token` | `string` |
| `token_type` | `token_type` | `string` |
| `expires_in` | `expires_in` | `number` |

## Usage Examples

### Using the useAuth Hook (Recommended)

```typescript
import { useAuth } from '@/hooks/useAuth';

const LoginPage = () => {
  const { login, isLoading, error } = useAuth();

  const handleSubmit = async (credentials) => {
    try {
      const { tokens, user } = await login(credentials);
      console.log('Logged in as:', user.username);
      // Navigate to dashboard
    } catch (err) {
      console.error('Login failed:', err);
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

### Using RTK Query Directly

```typescript
import {
  useLoginMutation,
  useGetCurrentUserQuery,
} from '@/store/api/authApi';
import { useDispatch } from 'react-redux';
import { setCredentials } from '@/store/slices/authSlice';

const Component = () => {
  const dispatch = useDispatch();
  const [login] = useLoginMutation();

  const handleLogin = async (credentials) => {
    const tokens = await login(credentials).unwrap();
    // Fetch user separately
    const response = await fetch(`${API_URL}/auth/me`, {
      headers: { Authorization: `Bearer ${tokens.access_token}` },
    });
    const user = await response.json();
    dispatch(setCredentials({ tokens, user }));
  };
};
```

## Benefits

1. **Type Safety**: All API calls use properly typed interfaces matching backend
2. **Automatic Caching**: RTK Query handles caching, refetching, and cache invalidation
3. **Less Boilerplate**: No need to write try/catch for every API call
4. **Better DX**: Loading and error states managed automatically by hooks
5. **Consistency**: Same pattern used across all API endpoints
6. **Token Management**: Automatic injection of auth tokens via baseApi
7. **Optimistic Updates**: RTK Query supports optimistic updates out of the box

## Migration Checklist

- [x] Remove Axios async thunks from authSlice
- [x] Add RTK Query matchers to authSlice
- [x] Update AuthState interface (remove isLoading, add refreshToken)
- [x] Fix useAuth hook to handle two-step login flow
- [x] Update User type (id: string → id: number)
- [x] Add LoginCredentials and RegisterData types
- [x] Deprecate api-client.ts
- [x] Create migration documentation
- [x] Verify TypeScript compilation
- [ ] Update existing components to use new auth pattern
- [ ] Add integration tests for auth flow
- [ ] Remove api-client.ts after migration complete

## Next Steps

1. **Update Components**: Migrate all components using old auth pattern to useAuth hook
2. **Add Tests**: Create comprehensive tests for auth flows
3. **Token Refresh**: Implement automatic token refresh on 401 errors
4. **Persist Auth**: Add redux-persist for auth state
5. **Remove Deprecated Code**: Delete api-client.ts once all migrations complete

## Files Modified

```
frontend/
├── src/
│   ├── store/
│   │   ├── slices/
│   │   │   └── authSlice.ts ............... UPDATED (removed async thunks)
│   │   └── api/
│   │       ├── authApi.ts ................. EXISTS (RTK Query endpoints)
│   │       └── baseApi.ts ................. EXISTS (token injection)
│   ├── hooks/
│   │   └── useAuth.ts ..................... UPDATED (two-step login)
│   ├── types/
│   │   ├── index.ts ....................... UPDATED (User.id type)
│   │   └── api.ts ......................... EXISTS (API types)
│   ├── lib/
│   │   └── api-client.ts .................. DEPRECATED
│   └── docs/
│       └── AUTH_MIGRATION.md .............. NEW
└── AUTH_REFACTOR_SUMMARY.md ............... NEW (this file)
```

## Breaking Changes

### For Components Using Old Pattern

**Before:**
```typescript
import { login } from '@/store/slices/authSlice';
const dispatch = useDispatch();
await dispatch(login(credentials));
```

**After:**
```typescript
import { useAuth } from '@/hooks/useAuth';
const { login } = useAuth();
await login(credentials);
```

### For Type Imports

**Before:**
```typescript
import type { User } from '@/types';
const user: User = { id: '123', ... }; // String ID
```

**After:**
```typescript
import type { ApiUser } from '@/types/api';
const user: ApiUser = { id: 123, ... }; // Number ID
```

## Testing Recommendations

```typescript
// Test login flow
test('login fetches user after getting tokens', async () => {
  const { result } = renderHook(() => useAuth());

  await act(async () => {
    await result.current.login({
      username: 'test',
      password: 'password',
    });
  });

  expect(result.current.user).toBeTruthy();
  expect(result.current.accessToken).toBeTruthy();
  expect(result.current.isAuthenticated).toBe(true);
});

// Test register flow
test('register automatically logs in', async () => {
  const { result } = renderHook(() => useAuth());

  await act(async () => {
    await result.current.register({
      username: 'newuser',
      email: 'new@example.com',
      password: 'password',
    });
  });

  expect(result.current.isAuthenticated).toBe(true);
});
```

## Notes

- No TypeScript errors introduced by these changes
- Existing file casing issues (Button.tsx vs button.tsx) are unrelated
- All auth state properly synced between RTK Query and Redux slice
- BaseApi automatically injects auth token in all requests
- Token refresh not yet implemented (future enhancement)

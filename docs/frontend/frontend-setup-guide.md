# Frontend Setup Guide - Spanish Subjunctive Practice

## Complete Next.js 14+ Frontend Foundation

This document provides a comprehensive overview of the frontend setup and how to get started.

## Project Overview

A modern, production-ready React/Next.js frontend built with:

- **Next.js 14+** with App Router
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **Redux Toolkit** with RTK Query for state management
- **React Hook Form** + **Zod** for form validation
- **Radix UI** for accessible components
- **Axios** for HTTP requests

## File Structure

```
frontend/
├── app/                          # Next.js App Router
│   ├── auth/
│   │   └── login/
│   │       └── page.tsx         # Login page
│   ├── dashboard/
│   │   └── page.tsx             # Dashboard page
│   ├── layout.tsx               # Root layout with metadata
│   ├── page.tsx                 # Home page (redirects)
│   └── providers.tsx            # Redux Provider wrapper
│
├── components/
│   └── ui/                      # UI component library
│       ├── button.tsx           # Button component
│       ├── card.tsx             # Card components
│       ├── input.tsx            # Input component
│       ├── label.tsx            # Label component
│       ├── toast.tsx            # Toast notification
│       └── toaster.tsx          # Toast container
│
├── hooks/
│   ├── use-redux.ts             # Typed Redux hooks
│   └── use-toast.tsx            # Toast hook
│
├── lib/
│   ├── api-client.ts            # Axios client with interceptors
│   └── utils.ts                 # Utility functions
│
├── store/
│   ├── services/
│   │   └── api.ts               # RTK Query API service
│   ├── slices/
│   │   └── auth-slice.ts        # Authentication slice
│   └── store.ts                 # Redux store configuration
│
├── styles/
│   └── globals.css              # Global styles + Tailwind
│
├── types/
│   └── index.ts                 # TypeScript type definitions
│
├── .env.example                 # Environment variables template
├── .env.local                   # Local environment variables
├── .eslintrc.json              # ESLint configuration
├── .gitignore                  # Git ignore rules
├── .prettierrc                 # Prettier configuration
├── next.config.js              # Next.js configuration
├── package.json                # Dependencies and scripts
├── postcss.config.js           # PostCSS configuration
├── tailwind.config.ts          # Tailwind CSS configuration
└── tsconfig.json               # TypeScript configuration
```

## Installation Steps

### 1. Navigate to Frontend Directory

```bash
cd frontend
```

### 2. Install Dependencies

```bash
npm install
```

This will install all required dependencies:

**Core Dependencies:**
- next (^14.2.0)
- react (^18.3.0)
- react-dom (^18.3.0)

**State Management:**
- @reduxjs/toolkit (^2.2.0)
- react-redux (^9.1.0)
- redux-persist (^6.0.0)

**HTTP & API:**
- axios (^1.7.0)

**Forms & Validation:**
- react-hook-form (^7.51.0)
- zod (^3.23.0)
- @hookform/resolvers (^3.3.0)

**UI Components:**
- @radix-ui/react-* (various components)
- lucide-react (^0.445.0)
- class-variance-authority (^0.7.0)
- clsx (^2.1.0)
- tailwind-merge (^2.5.0)

**Dev Dependencies:**
- typescript (^5.4.0)
- tailwindcss (^3.4.0)
- tailwindcss-animate (^1.0.7)
- eslint (^8.57.0)
- prettier (^3.2.0)

### 3. Configure Environment Variables

The `.env.local` file is already created with default values:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_APP_NAME=Spanish Subjunctive Practice
NEXT_PUBLIC_APP_VERSION=1.0.0
NEXT_PUBLIC_ENABLE_ANALYTICS=false
NEXT_PUBLIC_ENABLE_DEBUG=true
```

**Update if needed:**
- Change `NEXT_PUBLIC_API_URL` to match your backend URL
- Enable analytics in production
- Disable debug mode in production

### 4. Start Development Server

```bash
npm run dev
```

The application will start at [http://localhost:3000](http://localhost:3000)

## Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server on port 3000 |
| `npm run build` | Build production bundle |
| `npm start` | Start production server |
| `npm run lint` | Run ESLint for code quality |
| `npm run format` | Format code with Prettier |
| `npm run type-check` | Run TypeScript type checking |

## Key Features Implemented

### 1. State Management (Redux Toolkit)

**Store Configuration** (`store/store.ts`):
- Redux Toolkit setup
- Redux Persist for localStorage
- RTK Query middleware
- Type-safe exports

**Auth Slice** (`store/slices/auth-slice.ts`):
- Login/register async thunks
- User state management
- Token management
- Error handling

**API Service** (`store/services/api.ts`):
- RTK Query base configuration
- Automatic token injection
- Cache management
- Tag-based invalidation

### 2. API Client (Axios)

**Features** (`lib/api-client.ts`):
- Centralized HTTP client
- Request/response interceptors
- Automatic token injection
- 401 error handling
- Type-safe methods
- Organized API endpoints:
  - `authApi` - Authentication
  - `exerciseApi` - Exercises
  - `progressApi` - Progress tracking

### 3. Type Safety (TypeScript)

**Complete Type Definitions** (`types/index.ts`):
- User types
- Authentication types
- Exercise types
- Progress types
- API response types
- Form data types
- Session types

**Path Aliases** (tsconfig.json):
```typescript
import { Button } from "@/components/ui/button";
import { useAppDispatch } from "@/hooks/use-redux";
import { authApi } from "@/lib/api-client";
```

### 4. Authentication Flow

**Login Page** (`app/auth/login/page.tsx`):
- Form validation with Zod
- Redux Toolkit async actions
- Error handling with toast notifications
- Loading states
- Redirect after login

**Protected Routes**:
- Dashboard checks authentication
- Automatic redirect to login
- Token persistence
- Auto-logout on 401

### 5. UI Component Library

**Radix UI Components**:
- Fully accessible
- Customizable with Tailwind
- Type-safe props
- Dark mode ready

**Components Available**:
- Button (with variants)
- Input (form fields)
- Label (form labels)
- Card (content containers)
- Toast (notifications)

### 6. Styling System

**Tailwind CSS Configuration**:
- Custom color palette
- Design tokens (CSS variables)
- Dark mode support
- Responsive utilities
- Animation system

**Utility Functions** (`lib/utils.ts`):
- `cn()` - Class name merger
- `formatDate()` - Date formatting
- `formatTime()` - Time formatting
- `calculateAccuracy()` - Score calculation
- `debounce()` / `throttle()` - Performance helpers

## Application Flow

### 1. Initial Load

```
app/layout.tsx (Root Layout)
  └── app/providers.tsx (Redux Provider)
      └── app/page.tsx (Home - redirects based on auth)
```

### 2. Authentication Flow

```
Not Authenticated:
  → Redirect to /auth/login
  → User enters credentials
  → Redux action: login()
  → API call to backend
  → Store token + user data
  → Redirect to /dashboard

Authenticated:
  → Redirect to /dashboard
  → Load user data
  → Display dashboard
```

### 3. API Request Flow

```
Component calls API
  → apiClient interceptor adds token
  → Request sent to backend
  → Response intercepted
  → If 401: Clear auth, redirect to login
  → If success: Return data
  → Redux state updated
  → Component re-renders
```

## Integration with Backend

### API Endpoints Expected

The frontend expects these backend endpoints:

**Authentication:**
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user

**Exercises:**
- `GET /api/exercises` - List exercises
- `GET /api/exercises/:id` - Get single exercise
- `POST /api/exercises/:id/submit` - Submit answer

**Progress:**
- `GET /api/progress` - User progress
- `GET /api/statistics` - User statistics

### Request/Response Format

**Login Request:**
```json
{
  "username": "user123",
  "password": "password123"
}
```

**Login Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "username": "user123",
    "email": "user@example.com"
  }
}
```

**Authenticated Requests:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

## Development Workflow

### 1. Creating a New Page

```tsx
// app/new-page/page.tsx
"use client";

import { useAppSelector } from "@/hooks/use-redux";

export default function NewPage() {
  const { user } = useAppSelector((state) => state.auth);

  return <div>New Page for {user?.username}</div>;
}
```

### 2. Adding a New API Endpoint

```typescript
// lib/api-client.ts
export const newApi = {
  getData: (): Promise<any> => apiClient.get("/new-endpoint"),
  postData: (data: any): Promise<any> => apiClient.post("/new-endpoint", data),
};
```

### 3. Creating a Redux Slice

```typescript
// store/slices/new-slice.ts
import { createSlice } from "@reduxjs/toolkit";

const newSlice = createSlice({
  name: "newFeature",
  initialState: {},
  reducers: {},
});

export default newSlice.reducer;
```

### 4. Adding to Store

```typescript
// store/store.ts
import newReducer from "./slices/new-slice";

const rootReducer = combineReducers({
  auth: authReducer,
  newFeature: newReducer, // Add here
  [api.reducerPath]: api.reducer,
});
```

## Next Steps

### Immediate:
1. Run `npm install` in the frontend directory
2. Verify `.env.local` has correct API URL
3. Start development server with `npm run dev`
4. Test login page at `http://localhost:3000/auth/login`

### Short-term:
1. Create exercise practice pages
2. Build progress tracking UI
3. Add statistics dashboard
4. Implement real-time feedback

### Future Enhancements:
1. Dark mode toggle
2. Internationalization (i18n)
3. Progressive Web App (PWA)
4. Performance monitoring
5. A/B testing framework
6. Analytics integration

## Troubleshooting

### Port Already in Use
```bash
# Use different port
npm run dev -- -p 3001
```

### Build Errors
```bash
# Clear cache and rebuild
rm -rf .next
npm run build
```

### Type Errors
```bash
# Run type check
npm run type-check
```

### Dependency Issues
```bash
# Clear and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Redux Toolkit](https://redux-toolkit.js.org/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [React Hook Form](https://react-hook-form.com/)
- [Radix UI](https://www.radix-ui.com/)
- [TypeScript](https://www.typescriptlang.org/docs/)

## Summary

The frontend is now fully configured with:

✅ Next.js 14+ with App Router
✅ TypeScript configuration
✅ Tailwind CSS styling
✅ Redux Toolkit state management
✅ RTK Query for API calls
✅ Axios HTTP client
✅ Authentication flow
✅ Form validation (Zod + React Hook Form)
✅ UI component library (Radix UI)
✅ Type-safe hooks and utilities
✅ Development tooling (ESLint, Prettier)
✅ Production-ready build setup

**Ready to start development!**

Run `npm install` and `npm run dev` to begin.

# Frontend-Backend Integration Guide

## Overview

This guide provides comprehensive instructions for integrating and deploying the Spanish Subjunctive Practice application, which consists of a FastAPI backend and Next.js frontend.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Browser                          │
│  ┌───────────────────────────────────────────────────────┐ │
│  │         Next.js Frontend (Port 3000)                   │ │
│  │  - React Components                                    │ │
│  │  - Redux Store (RTK Query)                            │ │
│  │  - Tailwind CSS                                       │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                          │
                          │ HTTP/REST API
                          │ (JWT Authentication)
                          ▼
┌─────────────────────────────────────────────────────────────┐
│         FastAPI Backend (Port 8000)                         │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  API Endpoints:                                        │ │
│  │  - /api/auth/*      (Authentication)                  │ │
│  │  - /api/exercises/* (Exercise CRUD)                   │ │
│  │  - /api/progress/*  (Progress tracking)               │ │
│  └───────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  Core Services:                                        │ │
│  │  - JWT Token Management                               │ │
│  │  - Password Hashing (bcrypt)                          │ │
│  │  - Exercise Validation                                │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              Storage Layer                                   │
│  - PostgreSQL (Production)                                  │
│  - SQLite (Development)                                     │
│  - JSON Files (Fallback)                                    │
│  - Redis (Optional caching)                                 │
└─────────────────────────────────────────────────────────────┘
```

## Complete Setup Guide

### Prerequisites

- **Node.js**: 18.x or higher
- **Python**: 3.10 or higher
- **PostgreSQL**: 14.x or higher (for production)
- **Redis**: 7.x or higher (optional)
- **Git**: Latest version

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd subjunctive_practice
```

### Step 2: Backend Setup

#### 2.1 Create Python Virtual Environment

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

#### 2.2 Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

#### 2.3 Configure Environment Variables

Create `.env` file in `backend/` directory:

```env
# Application Settings
APP_NAME="Spanish Subjunctive Practice API"
VERSION="1.0.0"
ENVIRONMENT="development"
DEBUG=true
LOG_LEVEL="INFO"

# API Configuration
API_V1_PREFIX="/api"
HOST="0.0.0.0"
PORT=8000

# Security
SECRET_KEY="your-secret-key-change-in-production-min-32-chars"
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
ALGORITHM="HS256"

# CORS Configuration
CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
CORS_ALLOW_CREDENTIALS=true

# Database (PostgreSQL for production)
DATABASE_URL="postgresql://user:password@localhost:5432/subjunctive_practice"

# Or SQLite for development
# DATABASE_URL="sqlite:///./subjunctive_practice.db"

# Redis (Optional)
REDIS_URL="redis://localhost:6379/0"

# OpenAI (Optional - for AI features)
OPENAI_API_KEY="your-openai-api-key"

# Email Settings (Optional)
SMTP_HOST="smtp.gmail.com"
SMTP_PORT=587
SMTP_USER="your-email@gmail.com"
SMTP_PASSWORD="your-app-password"
EMAILS_FROM_EMAIL="noreply@subjunctivepractice.com"

# Sentry (Optional - for error tracking)
SENTRY_DSN=""
```

#### 2.4 Initialize Database

```bash
# Create database tables
alembic upgrade head

# Seed initial data (verbs, exercises, achievements)
python scripts/init_db.py
```

#### 2.5 Start Backend Server

```bash
# Development mode (auto-reload)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or using the Makefile
make dev

# Production mode
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### 2.6 Verify Backend

Open browser to http://localhost:8000/api/docs

You should see the interactive API documentation (Swagger UI).

### Step 3: Frontend Setup

#### 3.1 Install Dependencies

```bash
cd ../frontend
npm install
```

#### 3.2 Configure Environment Variables

Create `.env.local` file in `frontend/` directory:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api

# Application Settings
NEXT_PUBLIC_APP_NAME="Spanish Subjunctive Practice"
NEXT_PUBLIC_APP_VERSION="1.0.0"

# Feature Flags
NEXT_PUBLIC_ENABLE_ANALYTICS=false
NEXT_PUBLIC_ENABLE_AI_FEATURES=false
```

#### 3.3 Start Frontend Server

```bash
# Development mode
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

#### 3.4 Verify Frontend

Open browser to http://localhost:3000

You should see the landing page.

## Integration Testing

### Test Authentication Flow

1. **Register a new user:**
   - Frontend: http://localhost:3000/auth/register
   - Backend endpoint: POST /api/auth/register

2. **Login:**
   - Frontend: http://localhost:3000/auth/login
   - Backend endpoint: POST /api/auth/login

3. **Access protected route:**
   - Frontend: http://localhost:3000/dashboard
   - Backend validates JWT token

### Test Exercise Flow

1. **Fetch exercises:**
   - Backend: GET /api/exercises?limit=10&random_order=true
   - Frontend displays exercises

2. **Submit answer:**
   - Backend: POST /api/exercises/submit
   - Frontend shows validation result

3. **View progress:**
   - Backend: GET /api/progress
   - Frontend displays statistics

## API Integration Details

### Authentication Headers

All authenticated requests must include:

```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

### Request/Response Flow

#### 1. User Registration

**Frontend Request:**
```typescript
const response = await axios.post('/api/auth/register', {
  username: 'testuser',
  email: 'test@example.com',
  password: 'SecurePass123',
  full_name: 'Test User'
});
```

**Backend Response:**
```json
{
  "user_id": "user_1_testuser",
  "username": "testuser",
  "email": "test@example.com",
  "full_name": "Test User",
  "created_at": "2025-10-02T10:00:00Z",
  "last_login": null
}
```

#### 2. User Login

**Frontend Request:**
```typescript
const response = await axios.post('/api/auth/login', {
  username: 'testuser',
  password: 'SecurePass123'
});
```

**Backend Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

#### 3. Fetch Exercises

**Frontend Request:**
```typescript
const response = await axios.get('/api/exercises', {
  params: {
    difficulty: 2,
    limit: 10,
    random_order: true
  },
  headers: {
    Authorization: `Bearer ${accessToken}`
  }
});
```

**Backend Response:**
```json
{
  "exercises": [
    {
      "id": "ex_001",
      "type": "present_subjunctive",
      "prompt": "Espero que tú _____ (hablar) español.",
      "difficulty": 2,
      "explanation": "Use present subjunctive after 'espero que'",
      "hints": ["The verb is 'hablar' (to speak)"],
      "tags": ["present_subjunctive", "regular_verbs"]
    }
  ],
  "total": 10,
  "page": 1,
  "page_size": 10,
  "has_more": false
}
```

#### 4. Submit Answer

**Frontend Request:**
```typescript
const response = await axios.post('/api/exercises/submit', {
  exercise_id: 'ex_001',
  user_answer: 'hables',
  time_taken: 15
}, {
  headers: {
    Authorization: `Bearer ${accessToken}`
  }
});
```

**Backend Response:**
```json
{
  "is_correct": true,
  "correct_answer": "hables",
  "user_answer": "hables",
  "feedback": "Excellent! Your answer is correct.",
  "explanation": "Use present subjunctive after 'espero que'",
  "score": 105,
  "alternative_answers": []
}
```

## State Management Integration

### Redux Store Setup

The frontend uses Redux Toolkit for state management:

```typescript
// Store structure
{
  auth: {
    user: User | null,
    accessToken: string | null,
    refreshToken: string | null,
    isAuthenticated: boolean
  },
  exercise: {
    currentExercise: Exercise | null,
    exerciseHistory: Exercise[],
    currentAnswer: string,
    lastValidation: Validation | null
  },
  progress: {
    progress: Progress | null,
    statistics: Statistics | null
  },
  ui: {
    theme: 'light' | 'dark',
    sidebarOpen: boolean,
    toasts: Toast[]
  },
  settings: {
    notifications: boolean,
    dailyGoal: number,
    autoAdvance: boolean
  }
}
```

### API Client Configuration

```typescript
// lib/api-client.ts
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Request interceptor: Add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = store.getState().auth.accessToken;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor: Handle errors
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Token expired, try refresh
      await store.dispatch(refreshAccessToken());
    }
    return Promise.reject(error);
  }
);
```

## Deployment

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access services
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
# PostgreSQL: localhost:5432
# Redis: localhost:6379
```

### Production Deployment

#### Backend (Railway/Render)

1. Set environment variables
2. Configure PostgreSQL database
3. Run migrations: `alembic upgrade head`
4. Start with Gunicorn: `gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker`

#### Frontend (Vercel/Netlify)

1. Set `NEXT_PUBLIC_API_URL` to production backend URL
2. Build: `npm run build`
3. Deploy build artifacts

## Environment-Specific Configuration

### Development

- Backend: SQLite database
- Frontend: Hot reload enabled
- CORS: Allow localhost origins
- Debug mode: Enabled

### Staging

- Backend: PostgreSQL database
- Frontend: Optimized build
- CORS: Allow staging domain
- Debug mode: Limited logging

### Production

- Backend: PostgreSQL with connection pooling
- Frontend: CDN-hosted static assets
- CORS: Allow production domain only
- Debug mode: Disabled
- HTTPS: Required
- Rate limiting: Enabled
- Monitoring: Sentry integration

## Health Checks

### Backend Health

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-02T10:00:00Z",
  "version": "1.0.0",
  "environment": "development",
  "database_connected": true,
  "redis_connected": false,
  "openai_configured": false
}
```

### Frontend Health

```bash
curl http://localhost:3000/api/health
```

## Common Integration Issues

### CORS Errors

**Problem:** Frontend cannot access backend API

**Solution:**
- Verify `CORS_ORIGINS` in backend `.env`
- Include `http://localhost:3000` in allowed origins
- Check browser console for specific CORS error

### Authentication Failures

**Problem:** 401 Unauthorized errors

**Solution:**
- Verify JWT token is being sent in headers
- Check token expiration
- Ensure `SECRET_KEY` matches between requests
- Verify user exists in database

### Database Connection Issues

**Problem:** Backend fails to connect to database

**Solution:**
- Verify `DATABASE_URL` format
- Check PostgreSQL is running
- Verify database exists
- Check user permissions

### Environment Variable Not Found

**Problem:** `NEXT_PUBLIC_API_URL` undefined

**Solution:**
- Ensure `.env.local` exists in frontend root
- Restart development server after adding env vars
- Verify variable name starts with `NEXT_PUBLIC_`

## Monitoring and Logging

### Backend Logs

```bash
# View logs
tail -f backend.log

# View with filtering
grep ERROR backend.log
```

### Frontend Logs

Check browser console:
- Redux actions and state changes
- API requests/responses
- Component render logs

## Next Steps

1. Review [API Documentation](./API_DOCUMENTATION.md)
2. Read [Component Guide](./COMPONENT_GUIDE.md)
3. Check [Troubleshooting Guide](./TROUBLESHOOTING.md)
4. See [Development Guide](./DEVELOPMENT.md)

## Support

For issues or questions:
1. Check troubleshooting guide
2. Review API documentation
3. Check GitHub issues
4. Contact development team

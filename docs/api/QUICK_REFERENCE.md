# FastAPI Backend - Quick Reference

## Base URL
```
http://localhost:8000/api
```

## Quick Start
```bash
# Start server
./scripts/start_backend.sh  # Linux/Mac
scripts\start_backend.bat   # Windows

# Or directly
python -m uvicorn backend.main:app --reload

# Access docs
http://localhost:8000/api/docs
```

---

## Endpoints Summary

### Authentication (No Auth Required)

```bash
# Register
POST /api/auth/register
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123",
  "full_name": "John Doe"
}

# Login
POST /api/auth/login
{
  "username": "johndoe",
  "password": "SecurePass123"
}
# Returns: { "access_token": "...", "refresh_token": "..." }

# Refresh Token
POST /api/auth/refresh
{
  "refresh_token": "your_refresh_token"
}
```

### Exercises (Auth Required)

```bash
# Get exercises
GET /api/exercises?difficulty=1&limit=10&random_order=true
Authorization: Bearer {token}

# Get specific exercise
GET /api/exercises/{exercise_id}
Authorization: Bearer {token}

# Submit answer
POST /api/exercises/submit
Authorization: Bearer {token}
{
  "exercise_id": "fallback_001",
  "user_answer": "estudies",
  "time_taken": 15
}

# Get available types
GET /api/exercises/types/available
Authorization: Bearer {token}
```

### Progress (Auth Required)

```bash
# Get progress summary
GET /api/progress
Authorization: Bearer {token}

# Get detailed statistics
GET /api/progress/statistics
Authorization: Bearer {token}

# Reset progress (testing)
POST /api/progress/reset
Authorization: Bearer {token}
```

### System

```bash
# Health check
GET /health

# Root info
GET /
```

---

## Authentication Flow

```
1. Register → POST /api/auth/register
2. Login    → POST /api/auth/login (get tokens)
3. Use API  → Add "Authorization: Bearer {access_token}" header
4. Refresh  → POST /api/auth/refresh (when token expires)
```

---

## Response Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created (registration) |
| 400 | Bad Request (invalid input) |
| 401 | Unauthorized (invalid/missing token) |
| 403 | Forbidden (inactive user) |
| 404 | Not Found (resource doesn't exist) |
| 429 | Too Many Requests (rate limit) |
| 500 | Internal Server Error |

---

## Common Headers

```bash
# Authentication
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Content Type
Content-Type: application/json

# Response Headers
X-Process-Time: 0.023
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 57
```

---

## Error Response Format

```json
{
  "error": "Error Type",
  "message": "Detailed error message",
  "details": {},
  "path": "/api/endpoint",
  "timestamp": "2025-10-02T12:00:00"
}
```

---

## Example Workflow

```bash
# 1. Register a user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "learner1",
    "email": "learner@example.com",
    "password": "Learn123!"
  }'

# 2. Login to get token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "learner1",
    "password": "Learn123!"
  }'

# 3. Save the access_token from response

# 4. Get exercises
curl http://localhost:8000/api/exercises?difficulty=1&limit=5 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# 5. Submit an answer
curl -X POST http://localhost:8000/api/exercises/submit \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "exercise_id": "fallback_001",
    "user_answer": "estudies",
    "time_taken": 12
  }'

# 6. Check progress
curl http://localhost:8000/api/progress \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Environment Variables (.env)

```env
# Required
JWT_SECRET_KEY=your-super-secret-key-here

# Optional
DEBUG=true
CORS_ORIGINS=http://localhost:3000,http://localhost:80
OPENAI_API_KEY=sk-...
RATE_LIMIT_PER_MINUTE=60
```

---

## File Structure

```
backend/
├── main.py              # Entry point
├── core/
│   ├── config.py       # Settings
│   ├── security.py     # JWT & passwords
│   └── middleware.py   # CORS, logging, etc.
├── api/routes/
│   ├── auth.py         # /auth/*
│   ├── exercises.py    # /exercises/*
│   └── progress.py     # /progress/*
└── models/
    └── schemas.py      # Pydantic models
```

---

## Key Features

✅ JWT authentication with refresh tokens
✅ Password hashing (bcrypt)
✅ Input validation (Pydantic)
✅ CORS support
✅ Rate limiting (60 req/min)
✅ Request logging
✅ Error handling
✅ Auto-generated docs
✅ Health checks
✅ Progress tracking
✅ Gamification (levels, XP, streaks)

---

## Testing Tips

1. Use Swagger UI: http://localhost:8000/api/docs
2. Click "Authorize" button to set token
3. Try endpoints interactively
4. View request/response schemas
5. See example values

---

## Common Issues

**"Could not validate credentials"**
→ Token expired or invalid. Login again.

**"Rate limit exceeded"**
→ Wait 60 seconds or reduce request rate.

**"Username already registered"**
→ Choose a different username.

**"Invalid username or password"**
→ Check credentials are correct.

---

## Support

- Full Docs: `docs/api/BACKEND_API.md`
- Summary: `docs/api/BACKEND_SUMMARY.md`
- Interactive Docs: http://localhost:8000/api/docs
- Health Check: http://localhost:8000/health

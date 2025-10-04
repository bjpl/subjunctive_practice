# FastAPI Backend API Documentation

## Overview

The Spanish Subjunctive Practice backend is built with FastAPI and provides a comprehensive REST API for user authentication, exercise management, and progress tracking.

## Base URL

```
http://localhost:8000/api
```

## API Documentation

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI Spec**: http://localhost:8000/api/openapi.json

## Quick Start

### 1. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### 2. Configure Environment

Create a `.env` file with the following settings:

```env
# Application Settings
ENVIRONMENT=development
DEBUG=true
VERSION=1.0.0

# Security Keys
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
SESSION_SECRET_KEY=your-super-secret-session-key-change-in-production

# CORS Settings
CORS_ORIGINS=http://localhost:3000,http://localhost:80

# Database (Optional)
DATABASE_URL=postgresql://user:password@localhost:5432/subjunctive_practice

# Redis (Optional)
REDIS_URL=redis://localhost:6379/0

# OpenAI (Optional)
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4o-mini
```

### 3. Start Server

```bash
# Using script (recommended)
./scripts/start_backend.sh   # Linux/Mac
scripts\start_backend.bat    # Windows

# Or directly with uvicorn
python -m uvicorn backend.main:app --reload
```

## Authentication

All endpoints except `/auth/register` and `/auth/login` require authentication.

### Register User

```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123",
  "full_name": "John Doe"
}
```

**Response:**
```json
{
  "user_id": "user_1_johndoe",
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "created_at": "2025-10-02T12:00:00",
  "last_login": null
}
```

### Login

```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "johndoe",
  "password": "SecurePass123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

### Refresh Token

```http
POST /api/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Get Current User

```http
GET /api/auth/me
Authorization: Bearer {access_token}
```

## Exercises

### Get Exercises

```http
GET /api/exercises?difficulty=1&limit=10&random_order=true
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `difficulty` (optional): Filter by difficulty (1-5)
- `exercise_type` (optional): Filter by type (e.g., "present_subjunctive")
- `limit` (optional): Number of exercises (default: 10, max: 50)
- `random_order` (optional): Randomize order (default: true)

**Response:**
```json
{
  "exercises": [
    {
      "id": "fallback_001",
      "type": "present_subjunctive",
      "prompt": "Espero que tú _____ (estudiar) mucho.",
      "difficulty": 1,
      "explanation": "Use present subjunctive after expressions of hope/wish.",
      "hints": [],
      "tags": []
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10,
  "has_more": false
}
```

### Get Single Exercise

```http
GET /api/exercises/{exercise_id}
Authorization: Bearer {access_token}
```

### Submit Answer

```http
POST /api/exercises/submit
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "exercise_id": "fallback_001",
  "user_answer": "estudies",
  "time_taken": 15
}
```

**Response:**
```json
{
  "is_correct": true,
  "correct_answer": "estudies",
  "user_answer": "estudies",
  "feedback": "Excellent! Your answer is correct.",
  "explanation": "Use present subjunctive after expressions of hope/wish.",
  "score": 100,
  "alternative_answers": []
}
```

### Get Available Exercise Types

```http
GET /api/exercises/types/available
Authorization: Bearer {access_token}
```

**Response:**
```json
[
  "present_subjunctive",
  "imperfect_subjunctive",
  "subjunctive_triggers"
]
```

## Progress & Statistics

### Get User Progress

```http
GET /api/progress
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "user_id": "user_1_johndoe",
  "total_exercises": 25,
  "correct_answers": 20,
  "incorrect_answers": 5,
  "accuracy_rate": 80.0,
  "current_streak": 3,
  "best_streak": 5,
  "last_practice": "2025-10-02T12:00:00",
  "level": 2,
  "experience_points": 250
}
```

### Get Detailed Statistics

```http
GET /api/progress/statistics
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "user_id": "user_1_johndoe",
  "overall_stats": {
    "total_exercises": 25,
    "correct_answers": 20,
    "accuracy_rate": 80.0,
    "average_score": 85.5
  },
  "by_type": {
    "present_subjunctive": {
      "total": 15,
      "correct": 12,
      "accuracy": 80.0
    },
    "imperfect_subjunctive": {
      "total": 10,
      "correct": 8,
      "accuracy": 80.0
    }
  },
  "by_difficulty": {
    "1": {"total": 10, "correct": 9, "accuracy": 90.0},
    "2": {"total": 15, "correct": 11, "accuracy": 73.33}
  },
  "recent_performance": [...],
  "learning_insights": [
    "Great progress! Keep practicing to reach mastery.",
    "Focus on 'imperfect subjunctive' - your accuracy is 73.3%"
  ],
  "practice_calendar": ["2025-10-01", "2025-10-02"]
}
```

### Reset Progress (Testing)

```http
POST /api/progress/reset
Authorization: Bearer {access_token}
```

## System Endpoints

### Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-02T12:00:00",
  "version": "1.0.0",
  "environment": "development",
  "database_connected": false,
  "redis_connected": false,
  "openai_configured": true
}
```

### Root

```http
GET /
```

## Error Responses

All errors follow a consistent format:

```json
{
  "error": "Error Type",
  "message": "Detailed error message",
  "details": {},
  "path": "/api/endpoint",
  "timestamp": "2025-10-02T12:00:00"
}
```

### Common Error Codes

- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded (60 req/min)
- `500 Internal Server Error`: Server error

## Rate Limiting

- **Limit**: 60 requests per minute per IP
- **Headers**:
  - `X-RateLimit-Limit`: Maximum requests allowed
  - `X-RateLimit-Remaining`: Remaining requests

## Security Features

1. **JWT Authentication**: Secure token-based authentication
2. **Password Hashing**: Bcrypt password hashing
3. **CORS Protection**: Configurable CORS policies
4. **Rate Limiting**: Per-IP rate limiting
5. **Input Validation**: Pydantic schema validation
6. **Error Handling**: Sanitized error messages

## Architecture

```
backend/
├── main.py                 # FastAPI application entry point
├── core/
│   ├── config.py          # Configuration management
│   ├── security.py        # JWT & password utilities
│   └── middleware.py      # Custom middleware
├── api/
│   └── routes/
│       ├── auth.py        # Authentication endpoints
│       ├── exercises.py   # Exercise endpoints
│       └── progress.py    # Progress tracking endpoints
├── models/
│   └── schemas.py         # Pydantic models
└── database/              # Database models (future)
```

## Testing

```bash
# Run tests
pytest backend/tests/

# With coverage
pytest --cov=backend backend/tests/

# Specific test file
pytest backend/tests/test_auth.py
```

## Development Tips

1. **Auto-reload**: Use `--reload` flag during development
2. **Debug Mode**: Set `DEBUG=true` in `.env`
3. **API Docs**: Access interactive docs at `/api/docs`
4. **Logging**: Check `backend.log` for detailed logs
5. **Test Users**: Use file-based storage for development

## Production Deployment

1. Update `.env` with production settings
2. Set strong `JWT_SECRET_KEY`
3. Configure PostgreSQL database
4. Enable Redis for caching
5. Set up reverse proxy (nginx)
6. Use process manager (systemd, supervisor)
7. Enable HTTPS
8. Configure monitoring (Sentry)

## Future Enhancements

- [ ] PostgreSQL database integration
- [ ] Redis caching layer
- [ ] OpenAI-powered exercise generation
- [ ] WebSocket support for real-time updates
- [ ] Advanced analytics and reporting
- [ ] Multi-language support
- [ ] OAuth2 social login
- [ ] Email verification
- [ ] Password reset flow
- [ ] Admin dashboard API

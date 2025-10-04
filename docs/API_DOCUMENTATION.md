# API Documentation

## Overview

This document provides comprehensive documentation for the Spanish Subjunctive Practice Backend API, including all endpoints, request/response formats, authentication, and usage examples.

## Base URL

```
Development: http://localhost:8000/api
Production: https://api.subjunctivepractice.com/api
```

## API Version

Current version: **v1.0.0**

All endpoints are prefixed with `/api` unless otherwise specified.

## Authentication

### Overview

The API uses **JWT (JSON Web Token)** based authentication with access and refresh tokens.

### Token Types

1. **Access Token**: Short-lived (30 minutes), used for API requests
2. **Refresh Token**: Long-lived (7 days), used to obtain new access tokens

### Authentication Flow

```
1. User registers/logs in
2. Backend returns access_token and refresh_token
3. Client includes access_token in Authorization header
4. When access_token expires, use refresh_token to get new tokens
5. When refresh_token expires, user must log in again
```

### Including Tokens

Include the access token in the Authorization header:

```http
Authorization: Bearer <access_token>
```

## Endpoints

### System Endpoints

#### Health Check

Check API health and service status.

**Endpoint:** `GET /health`

**Authentication:** Not required

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-02T10:00:00Z",
  "version": "1.0.0",
  "environment": "development",
  "database_connected": true,
  "redis_connected": false,
  "openai_configured": true
}
```

**Status Codes:**
- `200 OK`: API is healthy
- `503 Service Unavailable`: API is unhealthy

---

#### Root Endpoint

Get API information.

**Endpoint:** `GET /`

**Authentication:** Not required

**Response:**
```json
{
  "message": "Spanish Subjunctive Practice API",
  "version": "1.0.0",
  "docs": "/api/docs",
  "health": "/health",
  "environment": "development"
}
```

---

### Authentication Endpoints

#### Register User

Create a new user account.

**Endpoint:** `POST /api/auth/register`

**Authentication:** Not required

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePassword123",
  "full_name": "John Doe"
}
```

**Validation Rules:**
- `username`: 3-50 characters, alphanumeric, unique
- `email`: Valid email format, unique
- `password`: Minimum 8 characters, must contain letters and numbers
- `full_name`: Optional, max 100 characters

**Response:** `201 Created`
```json
{
  "user_id": "user_1_johndoe",
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "created_at": "2025-10-02T10:00:00Z",
  "last_login": null
}
```

**Error Responses:**
- `400 Bad Request`: Invalid input or user already exists
- `422 Unprocessable Entity`: Validation error

**Example:**
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePassword123",
    "full_name": "John Doe"
  }'
```

---

#### Login

Authenticate user and get tokens.

**Endpoint:** `POST /api/auth/login`

**Authentication:** Not required

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "SecurePassword123"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid credentials
- `403 Forbidden`: Account disabled

**Example:**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "SecurePassword123"
  }'
```

---

#### Refresh Token

Get new access token using refresh token.

**Endpoint:** `POST /api/auth/refresh`

**Authentication:** Not required (uses refresh token)

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or expired refresh token

**Example:**
```bash
curl -X POST http://localhost:8000/api/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

---

#### Get Current User

Get authenticated user information.

**Endpoint:** `GET /api/auth/me`

**Authentication:** Required

**Response:** `200 OK`
```json
{
  "user_id": "user_1_johndoe",
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "created_at": "2025-10-02T10:00:00Z",
  "last_login": "2025-10-02T12:00:00Z"
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: User not found

**Example:**
```bash
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer <access_token>"
```

---

### Exercise Endpoints

#### Get Exercises

Retrieve practice exercises with optional filtering.

**Endpoint:** `GET /api/exercises`

**Authentication:** Required

**Query Parameters:**
- `difficulty` (integer, optional): Filter by difficulty (1-5)
- `exercise_type` (string, optional): Filter by type (e.g., "present_subjunctive")
- `limit` (integer, optional): Number of exercises (1-50, default: 10)
- `random_order` (boolean, optional): Randomize order (default: true)

**Response:** `200 OK`
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
    },
    {
      "id": "ex_002",
      "type": "imperfect_subjunctive",
      "prompt": "Si yo _____ (ser) rico, viajaría mucho.",
      "difficulty": 3,
      "explanation": "Use imperfect subjunctive in hypothetical conditions",
      "hints": ["The verb is 'ser' (to be)", "Irregular conjugation"],
      "tags": ["imperfect_subjunctive", "irregular_verbs", "conditional"]
    }
  ],
  "total": 2,
  "page": 1,
  "page_size": 10,
  "has_more": false
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: No exercises available
- `422 Unprocessable Entity`: Invalid query parameters

**Example:**
```bash
curl -X GET "http://localhost:8000/api/exercises?difficulty=2&limit=5&random_order=true" \
  -H "Authorization: Bearer <access_token>"
```

---

#### Get Exercise by ID

Retrieve a specific exercise.

**Endpoint:** `GET /api/exercises/{exercise_id}`

**Authentication:** Required

**Path Parameters:**
- `exercise_id` (string, required): Exercise identifier

**Response:** `200 OK`
```json
{
  "id": "ex_001",
  "type": "present_subjunctive",
  "prompt": "Espero que tú _____ (hablar) español.",
  "difficulty": 2,
  "explanation": "Use present subjunctive after 'espero que'",
  "hints": ["The verb is 'hablar' (to speak)"],
  "tags": ["present_subjunctive", "regular_verbs"]
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: Exercise not found

**Example:**
```bash
curl -X GET http://localhost:8000/api/exercises/ex_001 \
  -H "Authorization: Bearer <access_token>"
```

---

#### Submit Answer

Submit answer for validation.

**Endpoint:** `POST /api/exercises/submit`

**Authentication:** Required

**Request Body:**
```json
{
  "exercise_id": "ex_001",
  "user_answer": "hables",
  "time_taken": 15
}
```

**Fields:**
- `exercise_id` (string, required): Exercise identifier
- `user_answer` (string, required): User's answer
- `time_taken` (integer, optional): Time in seconds

**Response:** `200 OK`
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

**Incorrect Answer Response:**
```json
{
  "is_correct": false,
  "correct_answer": "hables",
  "user_answer": "hablas",
  "feedback": "Not quite. The correct answer is 'hables'.",
  "explanation": "Use present subjunctive after 'espero que'",
  "score": 0,
  "alternative_answers": []
}
```

**Scoring:**
- Correct answer: 100 points
- Time bonus (< 10 seconds): +10 points
- Time bonus (< 20 seconds): +5 points
- Incorrect answer: 0 points

**Error Responses:**
- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: Exercise not found
- `422 Unprocessable Entity`: Invalid request body

**Example:**
```bash
curl -X POST http://localhost:8000/api/exercises/submit \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "exercise_id": "ex_001",
    "user_answer": "hables",
    "time_taken": 15
  }'
```

---

#### Get Exercise Types

Get list of available exercise types.

**Endpoint:** `GET /api/exercises/types/available`

**Authentication:** Required

**Response:** `200 OK`
```json
[
  "present_subjunctive",
  "imperfect_subjunctive",
  "present_perfect_subjunctive",
  "pluperfect_subjunctive"
]
```

**Error Responses:**
- `401 Unauthorized`: Invalid or missing token

**Example:**
```bash
curl -X GET http://localhost:8000/api/exercises/types/available \
  -H "Authorization: Bearer <access_token>"
```

---

### Progress Endpoints

#### Get User Progress

Retrieve user's learning progress and statistics.

**Endpoint:** `GET /api/progress`

**Authentication:** Required

**Response:** `200 OK`
```json
{
  "user_id": "user_1_johndoe",
  "level": 5,
  "experience_points": 2450,
  "total_exercises_completed": 125,
  "correct_answers": 98,
  "accuracy_rate": 78.4,
  "current_streak": 7,
  "longest_streak": 14,
  "last_practice_date": "2025-10-02T12:00:00Z",
  "next_level_xp": 3000,
  "progress_to_next_level": 81.67
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or missing token
- `404 Not Found`: Progress not found

**Example:**
```bash
curl -X GET http://localhost:8000/api/progress \
  -H "Authorization: Bearer <access_token>"
```

---

#### Get User Statistics

Get detailed learning statistics.

**Endpoint:** `GET /api/progress/statistics`

**Authentication:** Required

**Response:** `200 OK`
```json
{
  "overall": {
    "total_sessions": 45,
    "total_study_time_minutes": 675,
    "average_session_duration": 15,
    "verbs_mastered": 12,
    "verbs_learning": 8,
    "achievements_unlocked": 5
  },
  "by_type": [
    {
      "type": "present_subjunctive",
      "exercises_completed": 60,
      "correct_answers": 48,
      "accuracy": 80.0
    },
    {
      "type": "imperfect_subjunctive",
      "exercises_completed": 40,
      "correct_answers": 28,
      "accuracy": 70.0
    }
  ],
  "weekly": {
    "exercises_completed": 25,
    "accuracy": 76.0,
    "study_time_minutes": 180
  },
  "weak_areas": [
    {
      "type": "imperfect_subjunctive",
      "accuracy": 70.0,
      "suggestion": "Review irregular verb conjugations"
    }
  ],
  "strong_areas": [
    {
      "type": "present_subjunctive",
      "accuracy": 80.0
    }
  ]
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or missing token

**Example:**
```bash
curl -X GET http://localhost:8000/api/progress/statistics \
  -H "Authorization: Bearer <access_token>"
```

---

#### Get Achievements

Get user's unlocked achievements.

**Endpoint:** `GET /api/progress/achievements`

**Authentication:** Required

**Response:** `200 OK`
```json
{
  "achievements": [
    {
      "id": "ach_001",
      "name": "First Steps",
      "description": "Complete your first exercise",
      "category": "milestone",
      "icon_url": "/achievements/first-steps.png",
      "points": 10,
      "unlocked_at": "2025-09-15T10:00:00Z"
    },
    {
      "id": "ach_002",
      "name": "Week Warrior",
      "description": "Maintain a 7-day streak",
      "category": "streak",
      "icon_url": "/achievements/week-warrior.png",
      "points": 50,
      "unlocked_at": "2025-09-22T10:00:00Z"
    }
  ],
  "total_points": 60,
  "total_unlocked": 2
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or missing token

**Example:**
```bash
curl -X GET http://localhost:8000/api/progress/achievements \
  -H "Authorization: Bearer <access_token>"
```

---

## Error Handling

### Error Response Format

All errors follow a consistent format:

```json
{
  "error": "Error Type",
  "message": "Detailed error message",
  "path": "/api/endpoint",
  "timestamp": "2025-10-02T10:00:00Z"
}
```

### HTTP Status Codes

- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required or failed
- `403 Forbidden`: Access denied
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: Service temporarily unavailable

### Common Errors

#### Authentication Error
```json
{
  "error": "Unauthorized",
  "message": "Invalid or expired token",
  "path": "/api/exercises",
  "timestamp": "2025-10-02T10:00:00Z"
}
```

#### Validation Error
```json
{
  "error": "Validation Error",
  "message": "Username must be at least 3 characters",
  "path": "/api/auth/register",
  "timestamp": "2025-10-02T10:00:00Z"
}
```

#### Not Found Error
```json
{
  "error": "Not Found",
  "message": "Exercise ex_999 not found",
  "path": "/api/exercises/ex_999",
  "timestamp": "2025-10-02T10:00:00Z"
}
```

---

## Rate Limiting

The API implements rate limiting to prevent abuse:

- **Limit**: 60 requests per minute per IP address
- **Headers**: Rate limit info in response headers
  - `X-RateLimit-Limit`: Total allowed requests
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Time when limit resets

**Rate Limit Exceeded Response:**
```json
{
  "error": "Too Many Requests",
  "message": "Rate limit exceeded. Try again in 30 seconds.",
  "path": "/api/exercises",
  "timestamp": "2025-10-02T10:00:00Z"
}
```

---

## Pagination

Endpoints returning lists support pagination:

**Query Parameters:**
- `page` (integer): Page number (default: 1)
- `page_size` (integer): Items per page (default: 10, max: 50)

**Response Structure:**
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "page_size": 10,
  "has_more": true
}
```

---

## API Versioning

The API uses URL versioning:
- Current: `/api/v1/`
- Future: `/api/v2/`

---

## Interactive Documentation

Explore the API interactively:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/api/openapi.json

---

## SDK / Client Libraries

### JavaScript/TypeScript

```typescript
import axios from 'axios';

class SubjunctiveAPI {
  private client = axios.create({
    baseURL: 'http://localhost:8000/api',
    headers: { 'Content-Type': 'application/json' }
  });

  async login(username: string, password: string) {
    const response = await this.client.post('/auth/login', {
      username,
      password
    });
    return response.data;
  }

  async getExercises(difficulty?: number, limit = 10) {
    const response = await this.client.get('/exercises', {
      params: { difficulty, limit }
    });
    return response.data;
  }

  async submitAnswer(exerciseId: string, answer: string) {
    const response = await this.client.post('/exercises/submit', {
      exercise_id: exerciseId,
      user_answer: answer
    });
    return response.data;
  }
}
```

### Python

```python
import requests

class SubjunctiveAPI:
    def __init__(self, base_url='http://localhost:8000/api'):
        self.base_url = base_url
        self.token = None

    def login(self, username, password):
        response = requests.post(
            f'{self.base_url}/auth/login',
            json={'username': username, 'password': password}
        )
        data = response.json()
        self.token = data['access_token']
        return data

    def get_exercises(self, difficulty=None, limit=10):
        headers = {'Authorization': f'Bearer {self.token}'}
        params = {'limit': limit}
        if difficulty:
            params['difficulty'] = difficulty

        response = requests.get(
            f'{self.base_url}/exercises',
            headers=headers,
            params=params
        )
        return response.json()

    def submit_answer(self, exercise_id, answer):
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.post(
            f'{self.base_url}/exercises/submit',
            headers=headers,
            json={'exercise_id': exercise_id, 'user_answer': answer}
        )
        return response.json()
```

---

## Support

For API support and questions:
- Review [Integration Guide](./INTEGRATION_GUIDE.md)
- Check [Troubleshooting Guide](./TROUBLESHOOTING.md)
- GitHub Issues
- Developer documentation

# API Documentation

This directory contains comprehensive API documentation for the Spanish Subjunctive Practice application backend.

## 📚 Documentation Files

### OpenAPI Specification
- **File**: `openapi.yaml`
- **Standard**: OpenAPI 3.0.3
- **Format**: YAML (YAML Ain't Markup Language)

## 🚀 Quick Start

### View Interactive Documentation

Once the backend server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

### Using the OpenAPI Specification

1. **Import into Postman**:
   ```bash
   # In Postman: File > Import > Select openapi.yaml
   ```

2. **Generate API Client**:
   ```bash
   # Install OpenAPI Generator
   npm install @openapitools/openapi-generator-cli -g

   # Generate TypeScript client
   openapi-generator-cli generate \
     -i docs/api/openapi.yaml \
     -g typescript-fetch \
     -o src/api/generated

   # Generate Python client
   openapi-generator-cli generate \
     -i docs/api/openapi.yaml \
     -g python \
     -o backend/api_client
   ```

3. **Validate Specification**:
   ```bash
   # Install Swagger CLI
   npm install -g @apidevtools/swagger-cli

   # Validate the spec
   swagger-cli validate docs/api/openapi.yaml
   ```

## 📖 API Overview

### Base URLs
- **Development**: http://localhost:8000
- **Staging**: https://api.staging.subjunctivepractice.com
- **Production**: https://api.subjunctivepractice.com

### Authentication
All authenticated endpoints require a JWT Bearer token:

```bash
# Login to get token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'

# Use token in subsequent requests
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### API Sections

#### 1. Authentication (`/api/auth/*`)
User registration, login, profile management, and password reset.

**Key Endpoints**:
- `POST /api/auth/register` - Create new user account
- `POST /api/auth/login` - Authenticate and get tokens
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/me` - Get current user profile

#### 2. Spaced Repetition System (`/api/srs/*`)
Advanced SRS implementation with SM-2+ algorithm for optimal learning.

**Key Endpoints**:
- `POST /api/srs/items/{item_id}/review` - Submit practice review
- `GET /api/srs/due-items` - Get items ready for review
- `GET /api/srs/analytics/metrics` - Learning analytics
- `GET /api/srs/schedule/optimize` - AI-optimized scheduling

#### 3. AI-Powered Learning (`/api/ai/*`)
GPT-4 powered intelligent tutoring features.

**Key Endpoints**:
- `POST /api/ai/exercise/generate` - Create contextual exercises
- `POST /api/ai/error/analyze` - Intelligent error analysis
- `POST /api/ai/conversation/generate` - Natural dialogue creation
- `POST /api/ai/feedback/adaptive` - Personalized feedback

#### 4. Health & Monitoring (`/health`, `/api/health`)
System health checks and service monitoring.

## 🔐 Security

### JWT Authentication
- **Algorithm**: HS256
- **Access Token**: 30 minutes expiration
- **Refresh Token**: 7 days expiration

### Rate Limiting
- **Default**: 100 requests per minute per IP
- **Burst**: Up to 120 requests in spike scenarios

### CORS Configuration
Configured for cross-origin requests from approved domains:
- Development: `http://localhost:3000`
- Production: `https://subjunctivepractice.com`

## 📊 Response Format

### Success Response
```json
{
  "data": { ... },
  "message": "Success message",
  "timestamp": "2025-10-02T10:30:00Z"
}
```

### Error Response
```json
{
  "error": "Error description",
  "status_code": 400,
  "details": {
    "field": "error details"
  }
}
```

## 🧪 Testing the API

### Using cURL

```bash
# Register a new user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_user",
    "email": "test@example.com",
    "password": "SecurePass123!",
    "first_name": "Test",
    "last_name": "User"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_user",
    "password": "SecurePass123!"
  }'

# Get due items (requires token)
curl -X GET "http://localhost:8000/api/srs/due-items?limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Generate AI exercise
curl -X POST http://localhost:8000/api/ai/exercise/generate \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "difficulty": "intermediate",
    "tense": "present",
    "topic": "travel"
  }'
```

### Using Python Requests

```python
import requests

# Base URL
BASE_URL = "http://localhost:8000"

# Login
response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={
        "username": "test_user",
        "password": "SecurePass123!"
    }
)
tokens = response.json()["tokens"]
access_token = tokens["access_token"]

# Set headers for authenticated requests
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Get due items
due_items = requests.get(
    f"{BASE_URL}/api/srs/due-items",
    headers=headers,
    params={"limit": 20}
).json()

# Submit a review
review_response = requests.post(
    f"{BASE_URL}/api/srs/items/{item_id}/review",
    headers=headers,
    json={
        "quality": 5,
        "response_time_ms": 3500,
        "user_answer": "hable",
        "expected_answer": "hable"
    }
).json()
```

### Using JavaScript/TypeScript

```typescript
// Login function
async function login(username: string, password: string) {
  const response = await fetch('http://localhost:8000/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });

  const data = await response.json();
  return data.tokens.access_token;
}

// Get due items
async function getDueItems(token: string, limit: number = 20) {
  const response = await fetch(
    `http://localhost:8000/api/srs/due-items?limit=${limit}`,
    {
      headers: { 'Authorization': `Bearer ${token}` }
    }
  );

  return await response.json();
}

// Generate AI exercise
async function generateExercise(token: string, options: {
  difficulty: string,
  tense: string,
  topic?: string
}) {
  const response = await fetch(
    'http://localhost:8000/api/ai/exercise/generate',
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(options)
    }
  );

  return await response.json();
}
```

## 🛠️ Development Tools

### OpenAPI Tooling

1. **Swagger Editor**: https://editor.swagger.io/
   - Paste the YAML content to edit and validate

2. **Swagger UI**: http://localhost:8000/api/docs
   - Interactive API exploration in development mode

3. **ReDoc**: http://localhost:8000/api/redoc
   - Beautiful API reference documentation

### Client Generation

Generate type-safe API clients for various languages:

```bash
# TypeScript/JavaScript
openapi-generator-cli generate -i docs/api/openapi.yaml -g typescript-fetch -o src/api/client

# Python
openapi-generator-cli generate -i docs/api/openapi.yaml -g python -o backend/client

# Java
openapi-generator-cli generate -i docs/api/openapi.yaml -g java -o java-client

# Go
openapi-generator-cli generate -i docs/api/openapi.yaml -g go -o go-client
```

## 📈 API Versioning

Current version: **v1.0.0**

### Version Strategy
- **URL versioning**: All endpoints prefixed with `/api/`
- **Backward compatibility**: Maintained for at least 6 months
- **Deprecation notices**: Announced 3 months in advance
- **Breaking changes**: Only in major version updates

### Future Versions
When v2 is released:
- v1 endpoints: `/api/v1/*`
- v2 endpoints: `/api/v2/*`
- Unversioned `/api/*` routes to latest stable version

## 🔍 API Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request succeeded |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid input parameters |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource does not exist |
| 409 | Conflict | Resource already exists |
| 422 | Unprocessable Entity | Validation error |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | Service temporarily unavailable |

## 🌐 Environments

### Development
- **URL**: http://localhost:8000
- **Docs**: http://localhost:8000/api/docs
- **Features**: Debug mode, detailed errors, CORS enabled

### Staging
- **URL**: https://api.staging.subjunctivepractice.com
- **Features**: Production-like environment for testing

### Production
- **URL**: https://api.subjunctivepractice.com
- **Features**: Optimized performance, security hardened

## 📝 Changelog

### v1.0.0 (2025-10-02)
- Initial API release
- Authentication system with JWT
- Spaced Repetition System (SRS)
- AI-powered exercise generation
- Learning analytics
- OpenAPI 3.0.3 specification

## 🤝 Contributing

When updating the API:

1. Update `openapi.yaml` with new endpoints/schemas
2. Validate the specification: `swagger-cli validate docs/api/openapi.yaml`
3. Update this README with relevant changes
4. Test all endpoints thoroughly
5. Update client code generators if needed

## 📞 Support

- **Documentation**: https://docs.subjunctivepractice.com
- **API Issues**: https://github.com/subjunctive-practice/backend/issues
- **Email**: api-support@subjunctivepractice.com

## 📜 License

MIT License - See LICENSE file for details

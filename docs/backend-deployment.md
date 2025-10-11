# Backend Deployment Guide
Spanish Subjunctive Practice Application - FastAPI Backend

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Docker Deployment](#docker-deployment)
4. [Railway Deployment](#railway-deployment)
5. [Render Deployment](#render-deployment)
6. [Environment Configuration](#environment-configuration)
7. [Database Migration](#database-migration)
8. [Testing](#testing)
9. [Monitoring & Logging](#monitoring--logging)

---

## Prerequisites

### Required Software
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (for containerized deployment)
- Git

### Required API Keys
- OpenAI API Key (for AI features)
- Sentry DSN (optional, for error tracking)

---

## Local Development Setup

### 1. Clone and Navigate to Backend
```bash
cd backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
# Production dependencies
pip install -r requirements.txt

# Development dependencies
pip install -r requirements-dev.txt
```

### 4. Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# Update database credentials, API keys, etc.
```

### 5. Setup Database
```bash
# Start PostgreSQL and Redis (if not using Docker)
# Or use Docker Compose:
docker-compose up -d postgres redis

# Run database migrations
alembic upgrade head

# Optional: Seed database with sample data
python scripts/seed_db.py
```

### 6. Run Development Server
```bash
# Using uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Or using Makefile
make dev
```

### 7. Access API
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

---

## Docker Deployment

### Full Stack with Docker Compose

#### 1. Build and Start Services
```bash
# Build images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend
```

#### 2. Services Included
- **backend** - FastAPI application (port 8000)
- **postgres** - PostgreSQL database (port 5432)
- **redis** - Redis cache (port 6379)
- **pgadmin** - Database management UI (port 5050) [optional]
- **redis-commander** - Redis management UI (port 8081) [optional]

#### 3. Start Optional Services
```bash
# Start with management tools
docker-compose --profile tools up -d
```

#### 4. Database Migration
```bash
# Run migrations in container
docker-compose exec backend alembic upgrade head
```

#### 5. Stop Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: Deletes data)
docker-compose down -v
```

### Production Docker Build

```bash
# Build production image
docker build -t subjunctive-backend:latest --target production .

# Run production container
docker run -d \
  --name subjunctive-backend \
  -p 8000:8000 \
  --env-file .env \
  subjunctive-backend:latest
```

---

## Railway Deployment

### 1. Install Railway CLI
```bash
npm install -g @railway/cli

# Login to Railway
railway login
```

### 2. Initialize Project
```bash
# Create new Railway project
railway init

# Link to existing project
railway link
```

### 3. Add Services

#### Add PostgreSQL
```bash
railway add postgresql
```

#### Add Redis
```bash
railway add redis
```

### 4. Configure Environment Variables
```bash
# Set environment variables via CLI
railway variables set JWT_SECRET_KEY="your-secret-key"
railway variables set SESSION_SECRET_KEY="your-session-key"
railway variables set OPENAI_API_KEY="your-openai-key"
railway variables set CORS_ORIGINS="https://your-frontend-domain.com"

# Or set via Railway dashboard
# https://railway.app/dashboard
```

### 5. Deploy
```bash
# Deploy backend
railway up

# View logs
railway logs

# Open in browser
railway open
```

### 6. Custom Domain (Optional)
1. Go to Railway dashboard
2. Select your service
3. Navigate to Settings > Networking
4. Add custom domain

### 7. Environment Variables (Railway Dashboard)
Set these in the Railway dashboard:
- `DATABASE_URL` - Auto-populated by PostgreSQL plugin
- `REDIS_URL` - Auto-populated by Redis plugin
- `JWT_SECRET_KEY` - Generate secure random string
- `SESSION_SECRET_KEY` - Generate secure random string
- `OPENAI_API_KEY` - Your OpenAI API key
- `CORS_ORIGINS` - Your frontend domain
- `SENTRY_DSN` - Optional, for error tracking

---

## Render Deployment

### 1. Connect Repository
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Blueprint"
3. Connect your GitHub repository
4. Select the repository containing `render.yaml`

### 2. Configure Services
The `render.yaml` file automatically configures:
- Web Service (FastAPI backend)
- PostgreSQL Database
- Redis Cache

### 3. Set Environment Variables
In Render dashboard, set these secret variables:
- `JWT_SECRET_KEY` - Generate with: `openssl rand -hex 32`
- `SESSION_SECRET_KEY` - Generate with: `openssl rand -hex 32`
- `OPENAI_API_KEY` - Your OpenAI API key
- `SENTRY_DSN` - Optional, your Sentry DSN

### 4. Update CORS Origins
Update `CORS_ORIGINS` in `render.yaml` with your frontend URL:
```yaml
- key: CORS_ORIGINS
  value: https://your-frontend.onrender.com
```

### 5. Deploy
1. Render automatically deploys on git push to main branch
2. Monitor deployment in Render dashboard
3. View logs in real-time

### 6. Database Migration
```bash
# SSH into Render instance
# Run migrations
alembic upgrade head
```

### 7. Custom Domain (Optional)
1. Go to service settings in Render dashboard
2. Add custom domain
3. Configure DNS records as instructed

---

## Environment Configuration

### Required Variables
```bash
# Application
ENVIRONMENT=production
DEBUG=false
PORT=8000

# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host:port/db

# Redis
REDIS_URL=redis://host:port/db

# Security
JWT_SECRET_KEY=your-secret-key
SESSION_SECRET_KEY=your-session-key

# OpenAI
OPENAI_API_KEY=your-api-key

# CORS
CORS_ORIGINS=https://your-frontend.com
```

### Optional Variables
```bash
# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
SENTRY_DSN=your-sentry-dsn

# Email (if needed)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email
SMTP_PASSWORD=your-password

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60
```

### Generate Secure Keys
```bash
# JWT Secret Key
openssl rand -hex 32

# Session Secret Key
openssl rand -hex 32

# Or in Python
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Database Migration

### Create Migration
```bash
# Auto-generate migration from models
alembic revision --autogenerate -m "Description of changes"

# Create empty migration
alembic revision -m "Description of changes"
```

### Apply Migrations
```bash
# Upgrade to latest version
alembic upgrade head

# Upgrade to specific version
alembic upgrade <revision_id>

# Upgrade one version
alembic upgrade +1
```

### Rollback Migrations
```bash
# Downgrade one version
alembic downgrade -1

# Downgrade to specific version
alembic downgrade <revision_id>

# Downgrade to base (WARNING: Destroys all data)
alembic downgrade base
```

### View Migration History
```bash
# Show current version
alembic current

# Show migration history
alembic history

# Show migration details
alembic show <revision_id>
```

---

## Testing

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run specific test
pytest tests/test_api.py::test_health_check

# Run with verbose output
pytest -v -s
```

### Test Database
Tests use a separate test database configured in `pytest.ini`:
```bash
TEST_DATABASE_URL=postgresql+asyncpg://test:test@localhost:5432/test_db
```

---

## Monitoring & Logging

### View Logs

#### Local Development
```bash
# View application logs
tail -f logs/backend.log

# View uvicorn logs
# Logs print to console in development mode
```

#### Docker
```bash
# View container logs
docker-compose logs -f backend

# View last 100 lines
docker-compose logs --tail=100 backend
```

#### Railway
```bash
# View logs via CLI
railway logs

# Or view in Railway dashboard
```

#### Render
- View logs in Render dashboard
- Real-time log streaming available

### Health Checks

#### API Health Endpoint
```bash
curl http://localhost:8000/health

# Expected response:
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-10-02T12:00:00Z"
}
```

#### Database Health
```bash
curl http://localhost:8000/health/db
```

#### Redis Health
```bash
curl http://localhost:8000/health/redis
```

### Sentry Integration
If Sentry is configured:
1. Set `SENTRY_DSN` environment variable
2. Errors automatically reported to Sentry
3. View errors in Sentry dashboard

---

## Makefile Commands

Quick reference for common commands:

```bash
make help              # Show all available commands
make install           # Install production dependencies
make install-dev       # Install development dependencies
make dev              # Run development server
make test             # Run tests
make lint             # Run linters
make format           # Format code
make docker-up        # Start Docker containers
make docker-down      # Stop Docker containers
make db-upgrade       # Run database migrations
make clean            # Clean temporary files
```

---

## Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL is running
pg_isready -h localhost -p 5432

# Test database connection
psql -h localhost -U app_user -d subjunctive_practice
```

### Redis Connection Issues
```bash
# Check Redis is running
redis-cli ping

# Expected response: PONG
```

### Docker Issues
```bash
# Remove all containers and volumes
docker-compose down -v

# Rebuild images
docker-compose build --no-cache

# View container status
docker-compose ps
```

### Port Already in Use
```bash
# Find process using port 8000
# On Linux/macOS
lsof -i :8000

# On Windows
netstat -ano | findstr :8000

# Kill the process
kill -9 <PID>
```

---

## Security Best Practices

1. **Never commit `.env` files** - Use `.env.example` as template
2. **Use strong secret keys** - Generate with `openssl rand -hex 32`
3. **Enable HTTPS in production** - Use Railway/Render SSL
4. **Set secure CORS origins** - Only allow trusted domains
5. **Keep dependencies updated** - Regularly run `pip list --outdated`
6. **Use environment-specific configs** - Separate dev/staging/prod
7. **Enable rate limiting** - Prevent API abuse
8. **Monitor logs** - Set up Sentry for error tracking
9. **Regular backups** - Backup database regularly
10. **Use secrets management** - Railway/Render provide secret storage

---

## Support & Resources

- **API Documentation**: http://localhost:8000/docs
- **Railway Docs**: https://docs.railway.app
- **Render Docs**: https://render.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Alembic Docs**: https://alembic.sqlalchemy.org

---

## Quick Start Commands

```bash
# Local development
cp .env.example .env
pip install -r requirements-dev.txt
docker-compose up -d postgres redis
alembic upgrade head
make dev

# Docker deployment
docker-compose up -d

# Railway deployment
railway login
railway init
railway up

# Render deployment
# Push to main branch after connecting repository
```

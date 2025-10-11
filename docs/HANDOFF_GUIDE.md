# Team Handoff Guide

**Project**: Spanish Subjunctive Practice Application
**Version**: 1.0.0
**Handoff Date**: October 2025
**Status**: Production Ready

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Quick Start Guide](#quick-start-guide)
3. [System Architecture](#system-architecture)
4. [Development Environment](#development-environment)
5. [Codebase Navigation](#codebase-navigation)
6. [Common Tasks](#common-tasks)
7. [Deployment Procedures](#deployment-procedures)
8. [Maintenance and Operations](#maintenance-and-operations)
9. [Troubleshooting](#troubleshooting)
10. [Critical Information](#critical-information)

---

## Project Overview

### What This Application Does

The Spanish Subjunctive Practice Application is an educational platform that helps users learn Spanish subjunctive conjugations through:
- Interactive exercises with immediate feedback
- AI-powered explanations and grammar guidance
- Spaced repetition for optimal retention
- Personalized learning paths
- Comprehensive progress tracking

### Technology Stack Summary

**Frontend**: Next.js 14 + React 18 + TypeScript + Tailwind CSS
**Backend**: FastAPI + Python 3.11 + PostgreSQL + Redis
**Infrastructure**: Docker + Docker Compose
**Key Services**: OpenAI API for feedback generation

### Project Status

- All core features implemented and tested
- 85%+ test coverage across frontend and backend
- WCAG 2.1 AA accessibility compliance achieved
- Production deployment configurations ready
- Comprehensive documentation complete

---

## Quick Start Guide

### Prerequisites Checklist

Before you begin, ensure you have:

- [ ] Node.js 18.x or higher
- [ ] Python 3.11 or higher
- [ ] PostgreSQL 15 or higher
- [ ] Redis 7 or higher
- [ ] Git
- [ ] Docker and Docker Compose (optional but recommended)
- [ ] Code editor (VS Code recommended)
- [ ] OpenAI API key (for AI feedback features)

### Getting Started in 5 Minutes

#### Option 1: Docker (Recommended for Quick Start)

```bash
# Clone the repository
git clone <repository-url>
cd subjunctive_practice

# Create environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local

# Edit the .env files with your configuration
# Minimum required:
# - OPENAI_API_KEY in backend/.env
# - DATABASE_URL will be set by docker-compose
# - REDIS_URL will be set by docker-compose

# Start all services
docker-compose up --build

# Wait for services to start, then access:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

#### Option 2: Local Development

```bash
# Clone the repository
git clone <repository-url>
cd subjunctive_practice

# Backend Setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
cp .env.example .env
# Edit .env with your configuration
alembic upgrade head
uvicorn main:app --reload

# In a new terminal, Frontend Setup
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local with your configuration
npm run dev
```

### First Login

1. Navigate to http://localhost:3000
2. Click "Sign Up" to create a new account
3. Fill in email and password
4. Verify your account (if email is configured)
5. Start practicing!

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────┐
│   Next.js Frontend  │  Port 3000
│   (React + Redux)   │
└──────────┬──────────┘
           │ HTTP/REST
           ▼
┌─────────────────────┐
│  FastAPI Backend    │  Port 8000
│  (Python + Async)   │
└──────────┬──────────┘
           │
     ┌─────┴─────┬────────┐
     ▼           ▼        ▼
┌─────────┐  ┌──────┐  ┌────────┐
│PostgreSQL│  │Redis │  │ OpenAI │
│   DB     │  │Cache │  │  API   │
└─────────┘  └──────┘  └────────┘
```

### Key Components

**Frontend (Next.js)**
- App Router for routing and layouts
- Redux Toolkit for state management
- React Hook Form for form handling
- Radix UI for accessible components
- Tailwind CSS for styling

**Backend (FastAPI)**
- RESTful API with async support
- SQLAlchemy ORM with async driver
- Alembic for database migrations
- Redis for caching and sessions
- OpenAI integration for AI feedback

**Database (PostgreSQL)**
- User accounts and authentication
- Exercise content and metadata
- Progress tracking and analytics
- Spaced repetition scheduling

**Cache (Redis)**
- Session management
- API response caching
- Rate limiting
- Temporary data storage

---

## Development Environment

### IDE Setup (VS Code Recommended)

#### Recommended Extensions

**For Backend (Python)**
- Python (Microsoft)
- Pylance
- Ruff
- Black Formatter
- mypy

**For Frontend (TypeScript/React)**
- ESLint
- Prettier
- TypeScript and JavaScript Language Features
- Tailwind CSS IntelliSense
- ES7+ React/Redux/React-Native snippets

**General**
- GitLens
- Docker
- Thunder Client (for API testing)
- Better Comments

#### VS Code Settings

Create `.vscode/settings.json`:

```json
{
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

### Environment Variables

#### Backend (.env)

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/subjunctive_db

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-here  # Generate with: openssl rand -hex 32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI
OPENAI_API_KEY=sk-...your-key-here

# CORS
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com

# Environment
ENVIRONMENT=development
DEBUG=True

# Email (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-password

# Sentry (optional)
SENTRY_DSN=your-sentry-dsn
```

#### Frontend (.env.local)

```bash
# API
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# Environment
NEXT_PUBLIC_ENVIRONMENT=development

# Feature Flags (optional)
NEXT_PUBLIC_ENABLE_ANALYTICS=false
NEXT_PUBLIC_ENABLE_SENTRY=false
```

### Database Setup

#### Creating the Database

```bash
# PostgreSQL command line
createdb subjunctive_db

# Or via psql
psql -U postgres
CREATE DATABASE subjunctive_db;
\q
```

#### Running Migrations

```bash
cd backend

# Check current migration status
alembic current

# Apply all pending migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history

# Create new migration
alembic revision --autogenerate -m "Description of changes"
```

#### Seeding Data (Optional)

```bash
cd backend
python -c "from core.seed_data import seed_database; seed_database()"
```

---

## Codebase Navigation

### Backend Structure

```
backend/
├── api/                    # API layer
│   ├── routes/            # Endpoint definitions
│   │   ├── auth.py        # Authentication endpoints
│   │   ├── exercises.py   # Exercise CRUD and generation
│   │   ├── progress.py    # Progress tracking
│   │   └── feedback.py    # AI feedback endpoints
│   └── __init__.py
├── core/                  # Core configurations
│   ├── config.py          # Application settings
│   ├── database.py        # Database connection
│   ├── security.py        # Auth and security
│   ├── middleware.py      # Custom middleware
│   └── logging_config.py  # Logging setup
├── models/                # Database models
│   ├── user.py            # User model
│   ├── exercise.py        # Exercise model
│   ├── progress.py        # Progress model
│   └── schemas.py         # Shared schemas
├── services/              # Business logic
│   ├── conjugation.py     # Verb conjugation
│   ├── exercise_generator.py  # Exercise creation
│   ├── learning_algorithm.py  # Spaced repetition
│   └── feedback.py        # AI feedback generation
├── utils/                 # Utility functions
├── tests/                 # Test suite
├── alembic/              # Database migrations
└── main.py               # Application entry point
```

### Frontend Structure

```
frontend/
├── app/                   # Next.js app directory
│   ├── (app)/            # Protected routes
│   │   └── practice/     # Practice pages
│   ├── auth/             # Auth pages (login, register)
│   ├── dashboard/        # Main dashboard
│   ├── layout.tsx        # Root layout
│   ├── page.tsx          # Landing page
│   └── providers.tsx     # Redux + theme providers
├── components/           # React components
│   ├── practice/         # Exercise components
│   ├── progress/         # Progress tracking
│   ├── feedback/         # Feedback display
│   ├── accessibility/    # A11y features
│   ├── layout/           # Layout components
│   └── ui/               # Reusable UI components
├── hooks/                # Custom React hooks
├── lib/                  # Utility libraries
│   ├── api.ts           # API client
│   ├── utils.ts         # Helper functions
│   └── constants.ts     # App constants
├── store/                # Redux store
│   ├── slices/          # Redux slices
│   └── index.ts         # Store configuration
├── styles/               # Global styles
└── tests/                # Test suite
```

### Key Files to Know

**Backend Entry Points**
- `backend/main.py` - FastAPI application setup
- `backend/core/config.py` - All configuration
- `backend/api/routes/__init__.py` - Router registration

**Frontend Entry Points**
- `frontend/app/layout.tsx` - Root layout and providers
- `frontend/app/page.tsx` - Landing page
- `frontend/store/index.ts` - Redux configuration

**Configuration Files**
- `backend/pyproject.toml` - Python dependencies and tools
- `frontend/package.json` - Node dependencies
- `docker-compose.yml` - Docker orchestration
- `backend/alembic.ini` - Migration configuration

---

## Common Tasks

### Adding a New API Endpoint

1. **Define the route** in `backend/api/routes/`

```python
# backend/api/routes/your_feature.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/your-feature", tags=["your-feature"])

@router.get("/")
async def get_items(db: AsyncSession = Depends(get_db)):
    # Your logic here
    return {"items": []}
```

2. **Register the router** in `backend/api/routes/__init__.py`

```python
from api.routes import your_feature

def register_routes(app):
    app.include_router(your_feature.router)
```

3. **Add tests** in `backend/tests/test_your_feature.py`

4. **Update API documentation** in `docs/api/README.md`

### Adding a New Frontend Component

1. **Create component file** in `frontend/components/`

```typescript
// frontend/components/YourComponent.tsx
import { FC } from 'react';

interface YourComponentProps {
  // Props definition
}

export const YourComponent: FC<YourComponentProps> = ({ ...props }) => {
  return (
    <div>
      {/* Component JSX */}
    </div>
  );
};
```

2. **Add tests** in `frontend/tests/unit/components/`

3. **Export from index** if creating a group

```typescript
// frontend/components/index.ts
export { YourComponent } from './YourComponent';
```

### Running Tests

**Backend Tests**
```bash
cd backend

# All tests
pytest

# Specific file
pytest tests/test_exercises.py

# With coverage
pytest --cov=. --cov-report=html

# Watch mode
pytest-watch
```

**Frontend Tests**
```bash
cd frontend

# Unit tests
npm test

# Watch mode
npm run test:watch

# Coverage
npm run test:coverage

# E2E tests
npm run test:e2e

# Accessibility tests
npm run test:a11y
```

### Database Migrations

**Creating a Migration**
```bash
cd backend

# Auto-generate from model changes
alembic revision --autogenerate -m "Add new field to user"

# Manual migration
alembic revision -m "Custom migration"

# Edit the generated file in alembic/versions/
```

**Applying Migrations**
```bash
# Apply all pending
alembic upgrade head

# Apply specific
alembic upgrade +1

# Rollback
alembic downgrade -1
```

### Adding Dependencies

**Backend (Python)**
```bash
cd backend

# Add to requirements.txt
echo "new-package==1.0.0" >> requirements.txt

# Install
pip install -r requirements.txt

# For dev dependencies
echo "new-dev-package==1.0.0" >> requirements-dev.txt
```

**Frontend (Node)**
```bash
cd frontend

# Production dependency
npm install package-name

# Dev dependency
npm install --save-dev package-name

# Update package.json and package-lock.json
```

### Code Formatting

**Backend**
```bash
cd backend

# Format with Black
black .

# Sort imports
isort .

# Lint with Ruff
ruff check .

# Type check
mypy .

# All at once
black . && isort . && ruff check . && mypy .
```

**Frontend**
```bash
cd frontend

# Format with Prettier
npm run format

# Lint with ESLint
npm run lint

# Fix linting issues
npm run lint --fix

# Type check
npm run type-check

# All at once
npm run lint && npm run type-check && npm run format
```

---

## Deployment Procedures

### Pre-Deployment Checklist

- [ ] All tests passing
- [ ] Code linting and formatting complete
- [ ] Environment variables configured
- [ ] Database migrations ready
- [ ] Dependencies updated and locked
- [ ] Security review completed
- [ ] Performance testing done
- [ ] Monitoring configured
- [ ] Backup strategy in place

### Deployment to Railway (Backend)

1. **Install Railway CLI**
```bash
npm install -g @railway/cli
railway login
```

2. **Create Project**
```bash
cd backend
railway init
railway add postgresql
railway add redis
```

3. **Set Environment Variables**
```bash
railway variables set SECRET_KEY=your-secret
railway variables set OPENAI_API_KEY=your-key
# Set all required variables from .env
```

4. **Deploy**
```bash
railway up
```

### Deployment to Vercel (Frontend)

1. **Install Vercel CLI**
```bash
npm install -g vercel
vercel login
```

2. **Configure Project**
```bash
cd frontend
vercel init
```

3. **Set Environment Variables** (in Vercel dashboard or CLI)
```bash
vercel env add NEXT_PUBLIC_API_URL production
# Add all required environment variables
```

4. **Deploy**
```bash
vercel --prod
```

### Docker Deployment

**Build Images**
```bash
# Backend
docker build -t subjunctive-backend:latest ./backend

# Frontend
docker build -t subjunctive-frontend:latest ./frontend
```

**Run with Docker Compose**
```bash
docker-compose up -d
```

**View Logs**
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

**Stop Services**
```bash
docker-compose down
```

---

## Maintenance and Operations

### Daily Operations

**Monitor Application Health**
- Check application logs
- Review error rates in Sentry
- Monitor database performance
- Check Redis cache hit rates
- Review API response times

**User Support**
- Review user feedback
- Check support tickets
- Monitor user registration
- Review exercise completion rates

### Weekly Tasks

- [ ] Review and triage new issues
- [ ] Update dependencies (check for security updates)
- [ ] Review analytics and usage patterns
- [ ] Database backup verification
- [ ] Performance metrics review
- [ ] Security log review

### Monthly Tasks

- [ ] Dependency updates (major versions with testing)
- [ ] Security audit
- [ ] Performance optimization review
- [ ] Database cleanup and optimization
- [ ] Documentation updates
- [ ] Disaster recovery drill

### Monitoring and Alerts

**Application Monitoring** (Sentry configured)
- Error tracking
- Performance monitoring
- Release tracking
- User feedback

**Database Monitoring**
- Query performance
- Connection pool usage
- Table sizes
- Index usage

**Redis Monitoring**
- Memory usage
- Hit/miss rates
- Connection count
- Eviction rate

### Backup Procedures

**Database Backups**
```bash
# Automated daily backups (configure in production)
pg_dump -U user -d subjunctive_db > backup_$(date +%Y%m%d).sql

# Restore from backup
psql -U user -d subjunctive_db < backup_20251002.sql
```

**Redis Backups**
```bash
# Create snapshot
redis-cli SAVE

# Automated backups via configuration in redis.conf
save 900 1
save 300 10
save 60 10000
```

### Scaling Considerations

**Horizontal Scaling**
- Backend: Run multiple FastAPI instances behind load balancer
- Frontend: Next.js serverless functions auto-scale on Vercel
- Database: Read replicas for read-heavy operations
- Redis: Redis Cluster for distributed caching

**Vertical Scaling**
- Increase database resources as user base grows
- Adjust Redis memory allocation
- Monitor and adjust worker processes

---

## Troubleshooting

### Common Issues and Solutions

#### Backend Won't Start

**Issue**: Database connection error
```
Solution:
1. Check DATABASE_URL in .env
2. Verify PostgreSQL is running: pg_isready
3. Check database exists: psql -l
4. Verify credentials
```

**Issue**: Redis connection error
```
Solution:
1. Check REDIS_URL in .env
2. Verify Redis is running: redis-cli ping
3. Check Redis port (default 6379)
```

**Issue**: Import errors
```
Solution:
1. Activate virtual environment
2. Install dependencies: pip install -r requirements.txt
3. Check Python version: python --version (needs 3.11+)
```

#### Frontend Won't Start

**Issue**: Module not found errors
```
Solution:
1. Delete node_modules: rm -rf node_modules
2. Clear npm cache: npm cache clean --force
3. Reinstall: npm install
```

**Issue**: API connection errors
```
Solution:
1. Check NEXT_PUBLIC_API_URL in .env.local
2. Verify backend is running on correct port
3. Check CORS configuration in backend
```

**Issue**: Build errors
```
Solution:
1. Check TypeScript errors: npm run type-check
2. Fix linting issues: npm run lint --fix
3. Clear .next folder: rm -rf .next
4. Rebuild: npm run build
```

#### Database Issues

**Issue**: Migration conflicts
```
Solution:
1. Check current version: alembic current
2. View history: alembic history
3. Resolve conflicts manually
4. Or downgrade and re-apply: alembic downgrade -1 && alembic upgrade head
```

**Issue**: Slow queries
```
Solution:
1. Enable query logging in config
2. Identify slow queries
3. Add indexes where needed
4. Optimize query logic
```

#### Tests Failing

**Issue**: Backend tests fail
```
Solution:
1. Check test database configuration
2. Run migrations on test database
3. Verify fixtures are loading correctly
4. Check for environment-specific issues
```

**Issue**: Frontend tests fail
```
Solution:
1. Check jest.config.js configuration
2. Verify test setup in jest.setup.js
3. Check for missing test utilities
4. Clear jest cache: npm run test -- --clearCache
```

### Getting Help

**Documentation**
- Check `/docs` folder for detailed guides
- Review ADRs for architectural decisions
- Check API docs at `/docs` endpoint

**Logs**
- Backend logs: `backend/logs/`
- Frontend logs: Browser console + Vercel logs
- Database logs: PostgreSQL logs
- Application logs: Sentry dashboard

**Support Contacts**
- Technical Lead: [contact info]
- DevOps: [contact info]
- Database Admin: [contact info]

---

## Critical Information

### Security Considerations

**Secrets Management**
- NEVER commit .env files
- Use environment variables for all secrets
- Rotate SECRET_KEY periodically
- Rotate API keys regularly
- Use different keys for dev/staging/prod

**Access Control**
- Database credentials should be restricted
- Redis should require authentication
- API keys should have minimal required permissions
- Implement rate limiting on all endpoints

### Performance Considerations

**Database**
- Monitor connection pool usage
- Watch for N+1 query problems
- Use database indexes appropriately
- Regular vacuum and analyze operations

**Caching**
- Use Redis for frequently accessed data
- Implement cache invalidation strategy
- Monitor cache hit rates
- Set appropriate TTLs

**API**
- Implement pagination for list endpoints
- Use async operations where possible
- Monitor response times
- Implement request timeouts

### Known Limitations

1. **OpenAI API Rate Limits**: Monitor usage and implement backoff
2. **Database Connection Pool**: Limited to 20 connections by default
3. **Redis Memory**: 256MB default, monitor usage
4. **File Upload**: Not currently implemented
5. **Websockets**: Not implemented (polling used instead)

### Emergency Contacts

**Critical Issues (Production Down)**
- On-call Engineer: [phone/email]
- Backup: [phone/email]

**Infrastructure Issues**
- Hosting Support: [contact]
- Database Support: [contact]

**Third-Party Services**
- OpenAI Support: [contact]
- Sentry Support: [contact]

### Next Steps for New Team

1. **Week 1**: Environment setup and familiarization
   - Set up local development environment
   - Run the application locally
   - Review architecture documentation
   - Run tests and understand test coverage

2. **Week 2**: Codebase exploration
   - Make small bug fix or feature addition
   - Review and understand the deployment process
   - Familiarize with monitoring and logging

3. **Week 3**: Take ownership
   - Handle user feedback
   - Implement minor features
   - Participate in code reviews
   - Begin planning improvements

4. **Month 2+**: Enhancement and optimization
   - Implement roadmap features
   - Optimize performance
   - Enhance test coverage
   - Improve documentation

---

## Additional Resources

### Documentation
- [Architecture Overview](./architecture/system-overview.md)
- [API Documentation](./api/README.md)
- [Deployment Guide](./DEPLOYMENT_GUIDE.md)
- [Contributing Guidelines](./developer-portal/CONTRIBUTING.md)

### Tools and Utilities
- API Testing: http://localhost:8000/docs (Swagger UI)
- Database Client: pgAdmin or DBeaver
- Redis Client: RedisInsight or redis-cli
- API Client: Postman or Thunder Client

### Learning Resources
- FastAPI: https://fastapi.tiangolo.com/
- Next.js: https://nextjs.org/docs
- SQLAlchemy: https://docs.sqlalchemy.org/
- Redux Toolkit: https://redux-toolkit.js.org/

---

**Welcome to the team! We're excited to have you working on this project.**

For questions or clarification on any part of this handoff guide, please don't hesitate to reach out to the team.

**Last Updated**: October 2025
**Version**: 1.0

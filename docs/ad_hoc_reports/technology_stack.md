# Technology Stack Analysis
## Spanish Subjunctive Practice Application

**Generated:** 2025-10-12
**Project Path:** `C:/Users/brand/Development/Project_Workspace/active-development/language-learning/subjunctive_practice`
**Version:** 1.0.0
**Status:** Active Development

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Operating System & Infrastructure](#operating-system--infrastructure)
3. [Frontend Stack](#frontend-stack)
4. [Backend Stack](#backend-stack)
5. [Database & Data Layer](#database--data-layer)
6. [Caching & Message Queues](#caching--message-queues)
7. [Authentication & Security](#authentication--security)
8. [DevOps & CI/CD](#devops--cicd)
9. [Testing & Quality Assurance](#testing--quality-assurance)
10. [Monitoring & Logging](#monitoring--logging)
11. [External APIs & Integrations](#external-apis--integrations)
12. [Development Tools](#development-tools)
13. [Architecture Patterns](#architecture-patterns)
14. [Technology Decision Rationale](#technology-decision-rationale)

---

## Executive Summary

The Spanish Subjunctive Practice application is a modern, full-stack web application built with a clear separation between frontend and backend services. The architecture follows microservices principles with containerized deployment, comprehensive testing strategies, and automated CI/CD pipelines.

### Key Technology Choices

| Layer | Primary Technology | Version | Rationale |
|-------|-------------------|---------|-----------|
| **Frontend** | Next.js (React) | 14.2.0 | Server-side rendering, SEO, performance |
| **Backend** | FastAPI (Python) | 0.118.0 | High performance, async, auto-docs |
| **Database** | PostgreSQL | 15 (Alpine) | ACID compliance, relational integrity |
| **Cache** | Redis | 7 (Alpine) | Session management, performance |
| **Container** | Docker | Latest | Consistency, portability, scalability |
| **CI/CD** | GitHub Actions | N/A | Native integration, free for public repos |

---

## Operating System & Infrastructure

### Deployment Platform

| Component | Technology | Version | Notes |
|-----------|-----------|---------|-------|
| **Container Runtime** | Docker | Latest | Multi-stage builds for optimization |
| **Container Orchestration** | Docker Compose | 3.8 | Local development and small-scale deployment |
| **Base Images** | Alpine Linux | - | Minimal footprint, security-focused |
| **Backend Base** | Python:3.11-slim | 3.11 | Official Python image, Debian-based |
| **Frontend Base** | Node:18-alpine | 18 | Official Node.js image, Alpine-based |
| **Database Image** | postgres:15-alpine | 15 | Official PostgreSQL, optimized |
| **Cache Image** | redis:7-alpine | 7 | Official Redis, lightweight |

### Infrastructure Services

```yaml
Services Architecture:
├── Frontend Service (Node.js/Next.js)
│   └── Port: 3000
├── Backend Service (Python/FastAPI)
│   └── Port: 8000
├── Database Service (PostgreSQL)
│   └── Port: 5432 (exposed as 5433)
├── Cache Service (Redis)
│   └── Port: 6379 (exposed as 6380)
├── PgAdmin (Optional - Database Management)
│   └── Port: 5050
└── Redis Commander (Optional - Cache Management)
    └── Port: 8081
```

---

## Frontend Stack

### Core Framework

| Technology | Version | Purpose | Configuration |
|-----------|---------|---------|---------------|
| **Next.js** | ^14.2.0 | React framework with App Router | `next.config.js` |
| **React** | ^18.3.0 | UI library | React 18 with concurrent features |
| **React DOM** | ^18.3.0 | React renderer | - |
| **TypeScript** | ^5.4.0 | Type safety | Strict mode enabled |
| **Node.js** | 18+ | Runtime | LTS version |

**Architectural Notes:**
- Uses Next.js App Router (not Pages Router) for improved routing and layouts
- Server-side rendering (SSR) enabled for SEO optimization
- React Strict Mode enabled for development safety
- SWC compiler for faster builds and minification

### State Management

| Technology | Version | Purpose |
|-----------|---------|---------|
| **@reduxjs/toolkit** | ^2.2.0 | Global state management |
| **react-redux** | ^9.1.0 | React bindings for Redux |
| **redux-persist** | ^6.0.0 | State persistence to localStorage |
| **RTK Query** | (included) | Data fetching and caching |

**State Architecture:**
- Redux Toolkit for simplified Redux setup
- RTK Query for API integration with automatic caching
- Persistent state for user preferences and session data

### UI Components & Styling

| Technology | Version | Purpose |
|-----------|---------|---------|
| **Tailwind CSS** | ^3.4.18 | Utility-first CSS framework |
| **PostCSS** | ^8.4.0 | CSS processing |
| **Autoprefixer** | ^10.4.0 | CSS vendor prefixing |
| **tailwindcss-animate** | ^1.0.7 | Animation utilities |
| **Radix UI** | Various | Accessible component primitives |
| **Lucide React** | ^0.544.0 | Icon library (SVG icons) |
| **Framer Motion** | ^12.23.22 | Animation library |
| **class-variance-authority** | ^0.7.0 | Component variant management |
| **clsx** | ^2.1.0 | Conditional className utility |
| **tailwind-merge** | ^3.3.1 | Tailwind class merging |

**Radix UI Components:**
- `@radix-ui/react-alert-dialog` ^1.1.15
- `@radix-ui/react-dialog` ^1.0.5
- `@radix-ui/react-dropdown-menu` ^2.0.6
- `@radix-ui/react-label` ^2.0.2
- `@radix-ui/react-progress` ^1.0.3
- `@radix-ui/react-select` ^2.0.0
- `@radix-ui/react-slot` ^1.0.2
- `@radix-ui/react-toast` ^1.1.5
- `@radix-ui/react-tooltip` ^1.2.8

**Design System:**
- Custom color palette with HSL values
- Dark mode support via class strategy
- Responsive design with mobile-first approach
- Custom animations and transitions

### Forms & Validation

| Technology | Version | Purpose |
|-----------|---------|---------|
| **react-hook-form** | ^7.64.0 | Form state management |
| **@hookform/resolvers** | ^5.2.2 | Schema validation integration |
| **zod** | ^4.1.12 | Schema validation and type inference |

**Form Strategy:**
- Uncontrolled components for performance
- Schema-first validation with Zod
- Type-safe form handling

### Data Visualization

| Technology | Version | Purpose |
|-----------|---------|---------|
| **recharts** | ^3.2.1 | Charts and graphs for progress tracking |
| **date-fns** | ^4.1.0 | Date manipulation and formatting |

### HTTP & API

| Technology | Version | Purpose |
|-----------|---------|---------|
| **axios** | ^1.12.2 | HTTP client |
| **RTK Query** | (included) | API integration layer |

**API Strategy:**
- RTK Query for automatic caching and invalidation
- Axios for direct HTTP calls when needed
- API proxy via Next.js rewrites for CORS handling

### Gestures & Interactions

| Technology | Version | Purpose |
|-----------|---------|---------|
| **react-use-gesture** | ^9.1.3 | Touch and mouse gesture handling |

### Build Tools & Configuration

| Technology | Version | Purpose |
|-----------|---------|---------|
| **@next/swc-win32-x64-msvc** | Auto-installed | Platform-specific SWC compiler |
| **@tailwindcss/postcss** | ^4.1.14 | PostCSS plugin for Tailwind |

---

## Backend Stack

### Core Framework

| Technology | Version | Purpose | Configuration |
|-----------|---------|---------|---------------|
| **FastAPI** | 0.118.0 | Modern async web framework | `main.py` |
| **Python** | 3.10-3.12 | Programming language | 3.11 recommended |
| **Uvicorn[standard]** | 0.37.0 | ASGI server (development) | Auto-reload enabled |
| **Gunicorn** | 21.2.0 | WSGI/ASGI server (production) | 4 workers, Uvicorn worker class |

**Framework Features:**
- Async/await support throughout
- Automatic OpenAPI (Swagger) documentation
- Data validation with Pydantic
- Dependency injection system
- High performance (comparable to Node.js/Go)

### Data Validation & Settings

| Technology | Version | Purpose |
|-----------|---------|---------|
| **pydantic** | 2.11.10 | Data validation using Python type hints |
| **pydantic-settings** | 2.11.0 | Settings management from environment |

**Validation Strategy:**
- Schema-first API design
- Request/response models with Pydantic
- Automatic validation error responses
- Type safety throughout the application

### HTTP Clients

| Technology | Version | Purpose |
|-----------|---------|---------|
| **httpx** | 0.26.0 | Modern async HTTP client |
| **aiohttp** | 3.9.3 | Async HTTP client/server |

### Serialization & Performance

| Technology | Version | Purpose |
|-----------|---------|---------|
| **orjson** | 3.11.3 | Fast JSON serialization (C-based) |
| **pyyaml** | 6.0.1 | YAML parsing |

**Performance Optimization:**
- orjson for 2-3x faster JSON operations
- Custom serializers for complex types

### Middleware & CORS

| Technology | Version | Purpose |
|-----------|---------|---------|
| **python-dotenv** | 1.0.1 | Environment variable management |
| **python-multipart** | 0.0.9 | Multipart form data handling |

**CORS Configuration:**
- Configurable allowed origins
- Credentials support enabled
- Preflight request handling

### Email & Templating

| Technology | Version | Purpose |
|-----------|---------|---------|
| **aiosmtplib** | 3.0.1 | Async SMTP client |
| **jinja2** | 3.1.3 | Template engine |
| **email-validator** | 2.1.0 | Email address validation |

**Email Strategy:**
- Async email sending to avoid blocking
- Jinja2 templates for HTML emails
- Validation before sending

### Utilities

| Technology | Version | Purpose |
|-----------|---------|---------|
| **python-dateutil** | 2.9.0.post0 | Date/time utilities |
| **structlog** | 24.1.0 | Structured logging |

---

## Database & Data Layer

### Primary Database

| Technology | Version | Purpose | Configuration |
|-----------|---------|---------|---------------|
| **PostgreSQL** | 15 (Alpine) | Relational database | UTF8 encoding, en_US.UTF-8 locale |
| **SQLAlchemy** | 2.0.43 | Python SQL toolkit and ORM | Async mode enabled |
| **asyncpg** | 0.29.0 | Async PostgreSQL driver | Used by SQLAlchemy |
| **psycopg2-binary** | 2.9.9 | PostgreSQL adapter (sync fallback) | Binary distribution |

**Database Features:**
- ACID compliance for data integrity
- JSON/JSONB support for flexible data
- Full-text search capabilities
- Row-level security (RLS) capable
- Backup and point-in-time recovery

### Database Migrations

| Technology | Version | Purpose |
|-----------|---------|---------|
| **Alembic** | 1.13.1 | Database migration tool |
| **alembic-utils** | 0.8.8 | Utilities for complex migrations (dev) |

**Migration Strategy:**
- Auto-generation from SQLAlchemy models
- Version control for schema changes
- Rollback support
- Migration history tracking

### Database Schema Architecture

```
Key Tables:
├── users
│   ├── Authentication data
│   ├── Profile information
│   └── Preferences
├── exercises
│   ├── Exercise content
│   ├── Difficulty levels
│   └── Type classification
├── user_progress
│   ├── Exercise completions
│   ├── Scores and XP
│   └── Timestamps
├── achievements
│   ├── Badge definitions
│   └── User unlocks
└── sessions
    └── User session data
```

### Alternative Database (Development)

| Technology | Purpose | Notes |
|-----------|---------|-------|
| **SQLite** | Development/testing | Configured via DATABASE_URL |

**Use Cases:**
- Local development without PostgreSQL
- CI/CD testing pipelines
- Quick prototyping

---

## Caching & Message Queues

### Cache Layer

| Technology | Version | Purpose | Configuration |
|-----------|---------|---------|---------------|
| **Redis** | 7 (Alpine) | In-memory cache and session store | Append-only file (AOF) persistence |
| **redis** (Python client) | 5.0.1 | Python Redis client | Async support |
| **hiredis** | 2.3.2 | C-based Redis protocol parser | Performance optimization |

**Redis Use Cases:**
- Session management
- API response caching
- Rate limiting counters
- Temporary data storage
- Pub/sub for real-time features (future)

**Persistence Configuration:**
- AOF (Append-Only File) enabled
- Periodic snapshots
- Data directory volume mount

### Cache Strategy

```
Caching Layers:
├── L1: Browser Cache (HTTP headers)
├── L2: Redis Cache (API responses)
├── L3: Database Connection Pool
└── L4: PostgreSQL Query Cache
```

---

## Authentication & Security

### Authentication

| Technology | Version | Purpose |
|-----------|---------|---------|
| **python-jose[cryptography]** | 3.5.0 | JWT token generation and validation |
| **passlib[bcrypt]** | 1.7.4 | Password hashing framework |
| **bcrypt** | 4.1.2 | Bcrypt hashing algorithm |

**Authentication Flow:**
1. User credentials validated against database
2. Access token (30 min) and refresh token (7 days) issued
3. JWT tokens contain user ID and permissions
4. Token validation on protected endpoints
5. Token refresh mechanism for extended sessions

**Security Features:**
- JWT with RS256 or HS256 algorithms
- Bcrypt with configurable rounds (default: 12)
- Secure token storage (httpOnly cookies recommended)
- Token expiration and refresh flow
- Password complexity validation

### Security Headers & Middleware

| Layer | Implementation |
|-------|---------------|
| **CORS** | FastAPI CORSMiddleware |
| **Rate Limiting** | Custom middleware (60 req/min) |
| **Input Validation** | Pydantic schemas |
| **SQL Injection Protection** | SQLAlchemy parameterized queries |
| **XSS Protection** | Content Security Policy headers |

### Security Monitoring

| Technology | Version | Purpose |
|-----------|---------|---------|
| **Bandit** | Latest (dev) | Python security scanner |
| **TruffleHog** | Latest (CI) | Secrets detection in commits |

**Security Scanning:**
- Bandit runs on CI for vulnerability detection
- TruffleHog prevents secret commits
- GitHub Dependabot for dependency updates

---

## DevOps & CI/CD

### Containerization

| Technology | Version | Purpose | Configuration |
|-----------|---------|---------|---------------|
| **Docker** | Latest | Container platform | Multi-stage Dockerfiles |
| **Docker Compose** | 3.8 | Multi-container orchestration | `docker-compose.yml` |

**Backend Dockerfile Stages:**
1. **Base**: System dependencies, Python 3.11-slim
2. **Builder**: Virtual environment, Python packages
3. **Development**: Auto-reload, dev dependencies
4. **Production**: Non-root user, Gunicorn, health checks

**Frontend Dockerfile Stages:**
1. **Dependencies**: Node modules installation
2. **Builder**: Next.js build with optimizations
3. **Runner**: Minimal production image, non-root user

**Security Features:**
- Non-root users in production images
- Multi-stage builds for minimal image size
- Health checks for all services
- Read-only file systems where possible

### CI/CD Pipeline (GitHub Actions)

#### Backend CI Workflow

```yaml
Workflow: backend-ci.yml
Triggers: Push/PR to main, develop (backend changes)

Jobs:
├── test (Matrix: Python 3.10, 3.11, 3.12)
│   ├── Services: PostgreSQL 15, Redis 7
│   ├── Dependencies: pip cache, requirements install
│   ├── Database migrations: Alembic
│   ├── Tests: pytest with coverage
│   └── Artifacts: Coverage reports (HTML, XML, Codecov)
│
├── lint
│   ├── Black: Code formatting check
│   ├── isort: Import sorting check
│   ├── Flake8: Linting (E9, F63, F7, F82 errors)
│   ├── MyPy: Type checking
│   └── Pylint: Code analysis
│
├── security
│   ├── Bandit: Security vulnerability scanning
│   └── TruffleHog: Secret detection
│
└── build
    └── Docker image build (cache optimized)
```

#### Frontend CI Workflow

Similar structure with:
- Node.js version matrix
- ESLint, Prettier checks
- TypeScript compilation
- Jest unit tests
- Playwright E2E tests
- Lighthouse performance checks

#### Additional Workflows

| Workflow | Purpose | Triggers |
|----------|---------|----------|
| **pr-checks.yml** | Combined checks for PRs | Pull requests |
| **integration.yml** | Full stack integration tests | Nightly, manual |
| **security.yml** | Security scans and audits | Weekly, on-demand |
| **release.yml** | Version tagging and release | Tag push |
| **deploy-backend.yml** | Backend deployment | Main branch push |
| **deploy-frontend.yml** | Frontend deployment | Main branch push |

### Deployment Targets

**Backend:**
- Railway / Render / Heroku
- Docker containerized
- PostgreSQL managed service
- Redis managed service

**Frontend:**
- Vercel / Netlify
- Automatic builds on push
- Environment variable injection
- Preview deployments for PRs

---

## Testing & Quality Assurance

### Backend Testing

| Technology | Version | Purpose |
|-----------|---------|---------|
| **pytest** | 8.4.2 | Testing framework |
| **pytest-asyncio** | 0.23.5 | Async test support |
| **pytest-cov** | 4.1.0 | Coverage reporting |
| **pytest-mock** | 3.15.1 | Mocking utilities |
| **pytest-env** | 1.1.5 | Environment variable management |
| **faker** | 23.2.1 | Test data generation |

**Testing Strategy:**
```
Backend Tests:
├── Unit Tests (tests/unit/)
│   ├── Models
│   ├── Schemas
│   ├── Services
│   └── Utilities
│
├── Integration Tests (tests/integration/)
│   ├── API endpoints
│   ├── Database operations
│   ├── Authentication flow
│   └── External service mocks
│
└── API Tests (tests/api/)
    ├── Request/response validation
    ├── Error handling
    └── Edge cases
```

**Coverage Requirements:**
- Minimum 80% overall coverage
- Critical paths: 95%+ coverage
- HTML and XML reports generated

### Frontend Testing

| Technology | Version | Purpose |
|-----------|---------|---------|
| **Jest** | ^30.2.0 | JavaScript testing framework |
| **@testing-library/react** | ^16.3.0 | React testing utilities |
| **@testing-library/jest-dom** | ^6.9.1 | DOM matchers for Jest |
| **@testing-library/user-event** | ^14.6.1 | User interaction simulation |
| **jest-environment-jsdom** | ^30.2.0 | DOM environment for Jest |
| **jest-axe** | ^10.0.0 | Accessibility testing |
| **msw** | ^2.11.3 | API mocking |
| **next-router-mock** | ^1.0.2 | Next.js router mocking |

**Testing Strategy:**
```
Frontend Tests:
├── Unit Tests (components/__tests__/)
│   ├── Component rendering
│   ├── State management
│   ├── Utility functions
│   └── Hooks
│
├── Integration Tests (tests/integration/)
│   ├── User flows
│   ├── API integration (MSW)
│   ├── Form submissions
│   └── State persistence
│
├── Accessibility Tests (tests/accessibility/)
│   ├── jest-axe scans
│   ├── Keyboard navigation
│   └── Screen reader compatibility
│
└── E2E Tests (tests/e2e/)
    └── See Playwright section below
```

**Coverage Requirements:**
- Global: 70% (branches, functions, lines, statements)
- Critical components: 85%+

### End-to-End Testing

| Technology | Version | Purpose |
|-----------|---------|---------|
| **@playwright/test** | ^1.55.1 | Browser automation and E2E testing |

**Playwright Configuration:**
- Multiple browsers: Chromium, Firefox, WebKit
- Mobile viewports: Pixel 5, iPhone 12
- Branded browsers: Microsoft Edge, Google Chrome
- Video recording on failure
- Screenshot on failure
- Trace collection on retry
- HTML, JSON, and JUnit reporters

**E2E Test Coverage:**
- User authentication flows
- Exercise completion workflows
- Progress tracking updates
- Navigation and routing
- Responsive design validation
- Performance metrics

### Code Quality Tools (Backend)

| Technology | Version | Purpose |
|-----------|---------|---------|
| **black** | 24.2.0 | Code formatter (PEP 8) |
| **flake8** | 7.3.0 | Linting |
| **mypy** | 1.18.2 | Static type checking |
| **isort** | 5.13.2 | Import sorting |
| **pylint** | 3.0.3 | Code analysis |

**Quality Standards:**
- Black formatting (line length: 88)
- Flake8 max complexity: 10
- Type hints required (mypy)
- Import order: stdlib, third-party, local

### Code Quality Tools (Frontend)

| Technology | Version | Purpose |
|-----------|---------|---------|
| **ESLint** | ^8.57.0 | JavaScript/TypeScript linting |
| **eslint-config-next** | ^14.2.0 | Next.js ESLint config |
| **Prettier** | ^3.2.0 | Code formatter |
| **TypeScript** | ^5.4.0 | Static type checking |

**Quality Standards:**
- Prettier formatting (2-space indent)
- ESLint Airbnb + Next.js rules
- Strict TypeScript mode
- No console statements in production

### Type Checking (Backend)

| Technology | Version | Purpose |
|-----------|---------|---------|
| **types-redis** | 4.6.0.20240218 | Redis type stubs |
| **types-python-jose** | 3.3.4.20240106 | python-jose type stubs |
| **types-passlib** | 1.7.7.20250602 | passlib type stubs |
| **types-python-dateutil** | 2.9.0.20250822 | dateutil type stubs |

---

## Monitoring & Logging

### Application Monitoring

| Technology | Version | Purpose | Configuration |
|-----------|---------|---------|---------------|
| **Sentry SDK** | 1.40.3 | Error tracking and performance monitoring | FastAPI integration |
| **structlog** | 24.1.0 | Structured logging | JSON output format |

**Monitoring Features:**
- Real-time error tracking
- Performance monitoring
- User session tracking
- Breadcrumb trail for debugging
- Release tracking
- Environment-based sampling

### Logging Strategy

```
Log Levels:
├── DEBUG: Development verbose logging
├── INFO: General information, API requests
├── WARNING: Deprecations, non-critical issues
├── ERROR: Caught exceptions, validation errors
└── CRITICAL: System failures, data corruption

Log Format:
{
  "timestamp": "2025-10-12T10:30:00Z",
  "level": "INFO",
  "logger": "api.routes.auth",
  "message": "User login successful",
  "user_id": "123",
  "request_id": "abc-def-ghi",
  "duration_ms": 45
}
```

**Log Destinations:**
- Development: Console output
- Production: File logs + Sentry
- Volume mounts: `backend_logs:/app/logs`

### Health Checks

**Backend Health Check:**
```
Endpoint: GET /health
Checks:
├── Database connection
├── Redis connection
├── API responsiveness
└── Memory usage
```

**Frontend Health Check:**
```
Endpoint: GET /api/health
Checks:
├── Server responsiveness
└── API connectivity
```

**Docker Health Checks:**
- Interval: 30 seconds
- Timeout: 10 seconds
- Start period: 5-40 seconds
- Retries: 3

---

## External APIs & Integrations

### AI Integration

| Service | Technology | Version | Purpose |
|---------|-----------|---------|---------|
| **OpenAI API** | openai | 1.12.0 | AI-powered feedback and insights |

**Integration Features:**
- Model: GPT-4o-mini (configurable)
- Max tokens: 1000
- Temperature: 0.7
- Use cases:
  - Personalized learning recommendations
  - Exercise explanation generation
  - Adaptive difficulty suggestions
  - Grammar correction feedback

**Configuration:**
```env
OPENAI_API_KEY=your-key
OPENAI_MODEL=gpt-4o-mini
OPENAI_MAX_TOKENS=1000
OPENAI_TEMPERATURE=0.7
```

### Database Management UIs

| Tool | Image | Port | Purpose |
|------|-------|------|---------|
| **PgAdmin** | dpage/pgadmin4:latest | 5050 | PostgreSQL administration |
| **Redis Commander** | rediscommander/redis-commander:latest | 8081 | Redis key management |

**Access:**
- Optional tools (Docker profile: `tools`)
- Start with: `docker-compose --profile tools up`

---

## Development Tools

### Backend Development

| Technology | Version | Purpose |
|-----------|---------|---------|
| **ipython** | 8.21.0 | Enhanced Python REPL |
| **ipdb** | 0.13.13 | Python debugger |
| **watchdog** | 4.0.0 | File system monitoring |
| **httpie** | 3.2.2 | HTTP client for API testing |

**Development Workflow:**
- Hot reload with Uvicorn `--reload`
- Interactive debugging with ipdb
- API testing with httpie or Swagger UI

### Frontend Development

| Technology | Version | Purpose |
|-----------|---------|---------|
| **@types/node** | ^24.7.0 | Node.js type definitions |
| **@types/react** | ^18.3.0 | React type definitions |
| **@types/react-dom** | ^18.3.0 | React DOM type definitions |
| **@types/jest** | ^30.0.0 | Jest type definitions |

**Development Workflow:**
- Hot reload with Next.js Fast Refresh
- TypeScript type checking in IDE
- Browser DevTools for debugging

### Documentation

| Technology | Version | Purpose |
|-----------|---------|---------|
| **mkdocs** | 1.5.3 | Documentation generator |
| **mkdocs-material** | 9.5.9 | Material Design theme for MkDocs |

**Documentation Sites:**
- Backend: Auto-generated OpenAPI/Swagger at `/api/docs`
- Frontend: Component Storybook (planned)
- User docs: MkDocs static site

### Pre-commit Hooks

| Technology | Version | Purpose |
|-----------|---------|---------|
| **pre-commit** | 3.6.2 | Git pre-commit hook framework |

**Configured Hooks:**
- Code formatting (Black, Prettier)
- Linting (Flake8, ESLint)
- Type checking (MyPy, TypeScript)
- Test execution (pytest, Jest)
- Secret scanning

### Version Control

| Technology | Purpose |
|-----------|---------|
| **Git** | Version control |
| **GitHub** | Repository hosting |
| **Git LFS** | Large file storage (if needed) |

**Branching Strategy:**
- `main`: Production-ready code
- `develop`: Integration branch
- `feature/*`: Feature development
- `hotfix/*`: Production hotfixes

---

## Architecture Patterns

### Backend Patterns

**1. Clean Architecture**
```
Layers:
├── API Layer (routes/)
│   └── HTTP endpoints, request/response handling
├── Service Layer (services/)
│   └── Business logic, orchestration
├── Domain Layer (models/)
│   └── Entities, domain logic
├── Data Layer (models/, database access)
│   └── Database operations, repositories
└── Infrastructure (core/)
    └── Configuration, utilities, cross-cutting concerns
```

**2. Dependency Injection**
- FastAPI's dependency injection system
- Service dependencies injected at route level
- Database sessions managed as dependencies
- Authentication dependencies for protected routes

**3. Repository Pattern**
- Abstract database operations
- Testable data access layer
- Swap implementations (PostgreSQL, SQLite)

**4. Service Layer Pattern**
- Business logic separated from routes
- Reusable services across endpoints
- Transaction management in services

### Frontend Patterns

**1. Component Architecture**
```
Components:
├── Atomic Design
│   ├── Atoms (ui/): Buttons, Inputs, Labels
│   ├── Molecules (ui/): Form Groups, Cards
│   ├── Organisms (features/): Complete features
│   └── Templates (layout/): Page layouts
└── Smart/Presentational
    ├── Container components (with Redux)
    └── Presentational components (pure)
```

**2. State Management Patterns**
- Redux Toolkit slices for domain-specific state
- RTK Query for server state and caching
- Local component state for UI-only concerns
- Context API for theme/locale

**3. Data Fetching Strategy**
- RTK Query for automatic caching
- Optimistic updates for better UX
- Background refetching on focus
- Automatic retry on failure

**4. Routing Architecture**
- Next.js App Router
- File-based routing
- Nested layouts
- Dynamic routes with params

### API Design Patterns

**1. RESTful API**
- Resource-based URLs
- HTTP methods (GET, POST, PUT, DELETE)
- Status codes (200, 201, 400, 401, 404, 500)
- HATEOAS links (planned)

**2. API Versioning**
- URL-based: `/api/v1/...`
- Future-proof for breaking changes

**3. Error Handling**
```json
{
  "detail": "Human-readable message",
  "error_code": "VALIDATION_ERROR",
  "field_errors": {
    "email": ["Invalid email format"]
  }
}
```

**4. Pagination**
```
Query params:
- page: Page number (1-based)
- per_page: Items per page (default: 20, max: 100)
- sort: Sort field
- order: asc/desc
```

---

## Technology Decision Rationale

### Why FastAPI?

**Chosen:** FastAPI
**Alternatives Considered:** Django, Flask, Express.js (Node.js)

**Rationale:**
1. **Performance**: Near Node.js/Go performance (async/await)
2. **Modern Python**: Type hints, Python 3.10+ features
3. **Auto Documentation**: OpenAPI/Swagger out of the box
4. **Data Validation**: Pydantic integration
5. **Developer Experience**: Clear error messages, IDE support
6. **Ecosystem**: Rich Python data science/ML ecosystem for future features

### Why Next.js?

**Chosen:** Next.js 14 with App Router
**Alternatives Considered:** Create React App, Vite + React, Remix

**Rationale:**
1. **SEO**: Server-side rendering for better search visibility
2. **Performance**: Automatic code splitting, image optimization
3. **Developer Experience**: Fast Refresh, TypeScript support
4. **Routing**: File-based routing with layouts
5. **API Routes**: Built-in API layer (not used, but available)
6. **Deployment**: Vercel integration for easy deployment
7. **Community**: Large ecosystem, active development

### Why PostgreSQL?

**Chosen:** PostgreSQL 15
**Alternatives Considered:** MySQL, MongoDB, SQLite

**Rationale:**
1. **ACID Compliance**: Data integrity for user progress
2. **JSON Support**: Flexible data storage (JSONB)
3. **Full-Text Search**: Built-in text search for exercises
4. **Scalability**: Handles millions of rows efficiently
5. **Open Source**: No licensing costs
6. **Extensions**: PostGIS, pg_trgm for advanced features
7. **Mature**: Battle-tested, reliable

### Why Redis?

**Chosen:** Redis 7
**Alternatives Considered:** Memcached, in-memory caching only

**Rationale:**
1. **Performance**: Sub-millisecond latency
2. **Versatility**: Cache, session store, pub/sub
3. **Data Structures**: More than key-value (sets, sorted sets, hashes)
4. **Persistence**: AOF and RDB for durability
5. **Atomic Operations**: Perfect for rate limiting, counters
6. **Scalability**: Horizontal scaling with clustering

### Why Docker?

**Chosen:** Docker + Docker Compose
**Alternatives Considered:** Direct installation, Kubernetes (overkill)

**Rationale:**
1. **Consistency**: Same environment dev/staging/prod
2. **Isolation**: Service isolation, no dependency conflicts
3. **Portability**: Run anywhere (local, cloud, on-premise)
4. **Scalability**: Easy horizontal scaling
5. **CI/CD Integration**: Build once, deploy many times
6. **Developer Onboarding**: One command to start everything

### Why TypeScript?

**Chosen:** TypeScript 5.4 (strict mode)
**Alternatives Considered:** JavaScript only

**Rationale:**
1. **Type Safety**: Catch errors at compile time
2. **IDE Support**: Better autocomplete, refactoring
3. **Documentation**: Types as documentation
4. **Maintainability**: Easier to refactor large codebases
5. **Team Collaboration**: Clear contracts between components
6. **Ecosystem**: Most libraries have TypeScript support

### Why Tailwind CSS?

**Chosen:** Tailwind CSS 3.4
**Alternatives Considered:** CSS Modules, Styled Components, Material-UI

**Rationale:**
1. **Utility-First**: Rapid UI development
2. **Consistency**: Design system via configuration
3. **Performance**: Purge unused CSS in production
4. **Customization**: Fully customizable design tokens
5. **Dark Mode**: Built-in dark mode support
6. **Responsive**: Mobile-first responsive design
7. **No CSS Conflicts**: Utility classes avoid specificity issues

### Why GitHub Actions?

**Chosen:** GitHub Actions
**Alternatives Considered:** Jenkins, GitLab CI, CircleCI

**Rationale:**
1. **Integration**: Native GitHub integration
2. **Free Tier**: Generous free minutes for public/private repos
3. **Marketplace**: Large action marketplace
4. **Simplicity**: YAML configuration, easy to understand
5. **Matrix Builds**: Test multiple versions easily
6. **Artifacts**: Built-in artifact storage
7. **Secrets**: Secure secret management

---

## Version Summary

### Backend Core Dependencies

```
fastapi==0.118.0
uvicorn[standard]==0.37.0
python==3.11 (recommended: 3.10-3.12)
pydantic==2.11.10
sqlalchemy==2.0.43
alembic==1.13.1
postgresql==15-alpine
redis==7-alpine
gunicorn==21.2.0
```

### Frontend Core Dependencies

```
next==14.2.0
react==18.3.0
typescript==5.4.0
tailwindcss==3.4.18
@reduxjs/toolkit==2.2.0
node==18+ (alpine)
```

### Testing Frameworks

```
Backend:
- pytest==8.4.2
- pytest-cov==4.1.0

Frontend:
- jest==30.2.0
- @playwright/test==1.55.1
- @testing-library/react==16.3.0
```

### Infrastructure

```
docker==latest
docker-compose==3.8
github-actions (cloud)
```

---

## Future Technology Considerations

### Planned Additions

1. **GraphQL** (v1.2)
   - Apollo Server/Client
   - Federated schema
   - Real-time subscriptions

2. **WebSockets** (v1.1)
   - Socket.io or native WebSockets
   - Real-time progress updates
   - Multiplayer features

3. **CDN** (v1.1)
   - CloudFlare or AWS CloudFront
   - Static asset optimization
   - Global edge caching

4. **Message Queue** (v2.0)
   - RabbitMQ or AWS SQS
   - Background job processing
   - Email queue, report generation

5. **Search Engine** (v2.0)
   - Elasticsearch or Algolia
   - Full-text search optimization
   - Faceted search

6. **Object Storage** (v1.2)
   - AWS S3 or MinIO
   - User uploads
   - Audio files for pronunciation

7. **Analytics** (v1.1)
   - Mixpanel or Amplitude
   - User behavior tracking
   - A/B testing

---

## Conclusion

The Spanish Subjunctive Practice application leverages modern, battle-tested technologies to create a scalable, performant, and maintainable learning platform. The technology stack is designed with the following principles:

1. **Developer Experience**: Fast iteration, clear errors, type safety
2. **Performance**: Sub-second response times, optimized builds
3. **Scalability**: Horizontal scaling, caching, async operations
4. **Reliability**: Type checking, comprehensive tests, error monitoring
5. **Security**: Authentication, input validation, security scanning
6. **Maintainability**: Clean architecture, documentation, code quality tools

The stack supports current requirements while providing a foundation for future features such as mobile apps, real-time collaboration, and advanced AI-powered learning insights.

---

**Document Version:** 1.0
**Last Updated:** 2025-10-12
**Maintained By:** System Architecture Team
**Contact:** architecture@subjunctivepractice.com

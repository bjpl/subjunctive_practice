# Infrastructure Architecture

Comprehensive documentation of system architecture, network topology, and infrastructure components for the Spanish Subjunctive Practice Application.

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Diagrams](#architecture-diagrams)
3. [Infrastructure Components](#infrastructure-components)
4. [Network Topology](#network-topology)
5. [Data Flow](#data-flow)
6. [Security Architecture](#security-architecture)
7. [Scalability Design](#scalability-design)
8. [Technology Stack](#technology-stack)

---

## System Overview

### High-Level Architecture

The Spanish Subjunctive Practice Application follows a modern three-tier architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                         Client Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Web Browser │  │    Mobile    │  │     PWA      │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTPS
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Application Layer                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Next.js Frontend (Port 3000)            │  │
│  │  - React 18 + TypeScript                            │  │
│  │  - Server-Side Rendering                            │  │
│  │  - Static Site Generation                           │  │
│  └──────────────────────────────────────────────────────┘  │
│                            │                                │
│                            │ REST API                       │
│                            ▼                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │             FastAPI Backend (Port 8000)              │  │
│  │  - Python 3.11                                      │  │
│  │  - Async/Await Support                              │  │
│  │  - OpenAPI/Swagger Docs                             │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                         Data Layer                          │
│  ┌──────────────────┐        ┌──────────────────┐          │
│  │   PostgreSQL 15  │        │     Redis 7      │          │
│  │   (Port 5432)    │        │   (Port 6379)    │          │
│  │  - Primary Data  │        │  - Caching       │          │
│  │  - Relational    │        │  - Sessions      │          │
│  └──────────────────┘        └──────────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

### Design Principles

1. **Separation of Concerns**: Clear boundaries between presentation, business logic, and data layers
2. **Stateless Backend**: Enables horizontal scaling and load balancing
3. **API-First Design**: RESTful API can serve multiple clients
4. **Caching Strategy**: Multi-level caching for optimal performance
5. **Security by Design**: Authentication, authorization, and encryption at every layer

---

## Architecture Diagrams

### Component Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (Next.js)                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                      App Router                          │  │
│  │  - pages/                                                │  │
│  │  - layouts/                                              │  │
│  │  - routing logic                                         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           │                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   Component Layer                        │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐              │  │
│  │  │    UI    │  │ Features │  │  Layout  │              │  │
│  │  │ Components│  │Components│  │Components│              │  │
│  │  └──────────┘  └──────────┘  └──────────┘              │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           │                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   State Management                       │  │
│  │  - Redux Toolkit                                         │  │
│  │  - RTK Query (API state)                                 │  │
│  │  - Redux Persist                                         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           │                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    API Client Layer                      │  │
│  │  - Axios interceptors                                    │  │
│  │  - Token management                                      │  │
│  │  - Error handling                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       BACKEND (FastAPI)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    API Layer (Routes)                    │  │
│  │  - /auth      - Authentication endpoints                 │  │
│  │  - /exercises - Exercise management                      │  │
│  │  - /progress  - User progress tracking                   │  │
│  │  - /users     - User management                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           │                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  Middleware Layer                        │  │
│  │  - CORS handling                                         │  │
│  │  - Authentication (JWT)                                  │  │
│  │  - Rate limiting                                         │  │
│  │  - Request logging                                       │  │
│  │  - Error handling                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           │                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   Service Layer                          │  │
│  │  - Business logic                                        │  │
│  │  - Exercise generation                                   │  │
│  │  - Learning algorithms                                   │  │
│  │  - Feedback system                                       │  │
│  │  - OpenAI integration                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           │                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                     Data Layer                           │  │
│  │  - SQLAlchemy ORM                                        │  │
│  │  - Database models                                       │  │
│  │  - Query optimization                                    │  │
│  │  - Connection pooling                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                           │                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                     Cache Layer                          │  │
│  │  - Redis client                                          │  │
│  │  - Session storage                                       │  │
│  │  - Query caching                                         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Deployment Architecture

```
                          ┌─────────────────┐
                          │   CloudFlare    │
                          │   (CDN + SSL)   │
                          └────────┬────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
           ┌────────▼────────┐         ┌─────────▼────────┐
           │  Frontend CDN   │         │  Backend API     │
           │   (Vercel)      │         │  (Railway/Render)│
           │                 │         │                  │
           │  - Static files │         │  - App servers   │
           │  - Edge SSR     │         │  - Auto-scaling  │
           │  - Multi-region │         │  - Load balancer │
           └─────────────────┘         └─────────┬────────┘
                                                  │
                                    ┌─────────────┴─────────────┐
                                    │                           │
                          ┌─────────▼────────┐      ┌──────────▼──────────┐
                          │   PostgreSQL     │      │      Redis          │
                          │   - Primary DB   │      │   - Cache cluster   │
                          │   - Replicas     │      │   - Session store   │
                          │   - Auto backup  │      │   - Pub/Sub         │
                          └──────────────────┘      └─────────────────────┘
                                    │
                          ┌─────────▼────────┐
                          │  Backup Storage  │
                          │  (S3/Backblaze)  │
                          └──────────────────┘
```

---

## Infrastructure Components

### Frontend Infrastructure (Next.js)

#### Component Details

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Framework | Next.js 14+ | React framework with SSR/SSG |
| Language | TypeScript | Type-safe JavaScript |
| UI Library | React 18 | Component-based UI |
| Styling | Tailwind CSS | Utility-first CSS |
| State Management | Redux Toolkit | Centralized state |
| API Client | RTK Query | Data fetching & caching |
| Form Handling | React Hook Form | Form validation |
| Animations | Framer Motion | UI animations |
| Icons | Lucide React | Icon library |

#### Hosting Options

**Vercel (Recommended)**
- Automatic deployments from Git
- Edge network (global CDN)
- Serverless functions
- Preview deployments
- Analytics included

**Netlify (Alternative)**
- Git-based deployments
- Edge functions
- Split testing
- Form handling

**Self-Hosted**
- Node.js server
- Nginx reverse proxy
- PM2 process manager

### Backend Infrastructure (FastAPI)

#### Component Details

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Framework | FastAPI | High-performance API framework |
| Language | Python 3.11+ | Backend programming |
| ASGI Server | Uvicorn | Async server |
| Production Server | Gunicorn | Process manager |
| ORM | SQLAlchemy | Database abstraction |
| Migration Tool | Alembic | Database versioning |
| Validation | Pydantic | Data validation |
| Authentication | JWT + bcrypt | Secure auth |
| HTTP Client | httpx + aiohttp | External API calls |

#### Hosting Options

**Railway (Recommended for MVP)**
- Simple deployment
- Auto-scaling
- Built-in PostgreSQL & Redis
- Automatic HTTPS
- $5/month starting cost

**Render (Production-ready)**
- Docker support
- Auto-deploy from Git
- Health checks
- Database backups
- Free tier available

**AWS (Enterprise)**
- EC2 or ECS for compute
- RDS for database
- ElastiCache for Redis
- CloudFront CDN
- S3 for storage

### Database Infrastructure

#### PostgreSQL Configuration

```yaml
Version: 15.x
Configuration:
  max_connections: 100
  shared_buffers: 256MB
  effective_cache_size: 1GB
  work_mem: 4MB
  maintenance_work_mem: 64MB
  checkpoint_completion_target: 0.9
  wal_buffers: 16MB
  default_statistics_target: 100
  random_page_cost: 1.1
  effective_io_concurrency: 200

Indexes:
  - Users: email (unique), username (unique)
  - Exercises: type, difficulty, created_at
  - UserProgress: user_id + exercise_id (composite)
  - UserSessions: user_id, token (hash), expires_at
```

#### Redis Configuration

```yaml
Version: 7.x
Configuration:
  maxmemory: 256mb
  maxmemory-policy: allkeys-lru
  save: "900 1 300 10 60 10000"
  appendonly: yes
  appendfsync: everysec

Use Cases:
  - Session storage: 30 min TTL
  - Query caching: 1 hour TTL
  - Rate limiting: sliding window
  - Pub/Sub: real-time notifications
```

---

## Network Topology

### Production Network Architecture

```
                    Internet
                       │
                       ▼
            ┌──────────────────┐
            │   Load Balancer  │
            │   (HTTPS:443)    │
            └────────┬─────────┘
                     │
          ┌──────────┴──────────┐
          │                     │
    ┌─────▼─────┐        ┌─────▼─────┐
    │  App      │        │  App      │
    │  Server 1 │        │  Server 2 │
    │  (:8000)  │        │  (: 8000) │
    └─────┬─────┘        └─────┬─────┘
          │                     │
          └──────────┬──────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
    ┌────▼────┐            ┌─────▼─────┐
    │   DB    │            │   Redis   │
    │ Primary │            │  Cluster  │
    └────┬────┘            └───────────┘
         │
    ┌────▼────┐
    │   DB    │
    │ Replica │
    └─────────┘
```

### Network Security Zones

**DMZ (Demilitarized Zone)**
- Load balancer
- Web application firewall
- Rate limiting

**Application Zone**
- Application servers
- Internal API gateway
- Service mesh

**Data Zone**
- Database cluster
- Cache cluster
- Backup storage

### Firewall Rules

```yaml
Inbound Rules:
  - Port 443 (HTTPS): Allow from anywhere
  - Port 80 (HTTP): Redirect to 443
  - Port 8000: Block from internet, allow from LB
  - Port 5432: Block from internet, allow from app servers
  - Port 6379: Block from internet, allow from app servers
  - Port 22 (SSH): Allow from VPN only

Outbound Rules:
  - Port 443: Allow (HTTPS to external APIs)
  - Port 80: Allow (HTTP for package downloads)
  - Port 25/587: Allow (SMTP for emails)
  - All others: Block by default
```

---

## Data Flow

### User Authentication Flow

```
┌──────────┐                ┌──────────┐                ┌──────────┐
│          │                │          │                │          │
│  Client  │                │  Backend │                │ Database │
│          │                │          │                │          │
└────┬─────┘                └────┬─────┘                └────┬─────┘
     │                           │                           │
     │  POST /auth/login         │                           │
     │  (email, password)        │                           │
     ├──────────────────────────►│                           │
     │                           │  Query user by email      │
     │                           ├──────────────────────────►│
     │                           │                           │
     │                           │  User data                │
     │                           │◄──────────────────────────┤
     │                           │                           │
     │                           │  Verify password          │
     │                           │  (bcrypt)                 │
     │                           │                           │
     │                           │  Generate JWT tokens      │
     │                           │  - Access token (30min)   │
     │                           │  - Refresh token (7days)  │
     │                           │                           │
     │  200 OK                   │  Store session in Redis   │
     │  {tokens, user}           │  Key: session:{user_id}   │
     │◄──────────────────────────┤  TTL: 7 days             │
     │                           │                           │
     │  Store tokens in          │                           │
     │  localStorage/cookie      │                           │
     │                           │                           │
```

### Exercise Retrieval Flow

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│          │     │          │     │          │     │          │
│  Client  │     │  Backend │     │  Redis   │     │ Database │
│          │     │          │     │          │     │          │
└────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘
     │                │                │                │
     │  GET /exercises?type=fill-in    │                │
     │  Authorization: Bearer {token}  │                │
     ├────────────────►│                │                │
     │                │  Validate JWT  │                │
     │                │  token         │                │
     │                │                │                │
     │                │  Check cache   │                │
     │                ├───────────────►│                │
     │                │                │                │
     │                │  Cache miss    │                │
     │                │◄───────────────┤                │
     │                │                │                │
     │                │  Query exercises               │
     │                ├───────────────────────────────►│
     │                │                │                │
     │                │  Exercise data                 │
     │                │◄───────────────────────────────┤
     │                │                │                │
     │                │  Store in cache (TTL: 1h)      │
     │                ├───────────────►│                │
     │                │                │                │
     │  200 OK        │                │                │
     │  {exercises}   │                │                │
     │◄───────────────┤                │                │
     │                │                │                │
```

### Progress Update Flow

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│          │     │          │     │          │     │          │
│  Client  │     │  Backend │     │ Service  │     │ Database │
│          │     │          │     │  Layer   │     │          │
└────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘
     │                │                │                │
     │  POST /exercises/submit         │                │
     │  {exercise_id, answer}          │                │
     ├────────────────►│                │                │
     │                │  Validate      │                │
     │                │  answer        │                │
     │                ├───────────────►│                │
     │                │                │  Query         │
     │                │                │  exercise      │
     │                │                ├───────────────►│
     │                │                │                │
     │                │                │  Exercise data │
     │                │                │◄───────────────┤
     │                │                │                │
     │                │                │  Check answer  │
     │                │                │  Calculate XP  │
     │                │                │  Generate      │
     │                │                │  feedback      │
     │                │                │                │
     │                │  Result +      │  Update        │
     │                │  feedback      │  progress      │
     │                │◄───────────────┤───────────────►│
     │                │                │                │
     │                │                │  Update stats  │
     │                │                │  Update streak │
     │                │                │───────────────►│
     │                │                │                │
     │  200 OK        │                │                │
     │  {correct,     │                │                │
     │   xp_earned,   │                │                │
     │   feedback}    │                │                │
     │◄───────────────┤                │                │
     │                │                │                │
```

---

## Security Architecture

### Authentication & Authorization

#### JWT Token Structure

```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user_id",
    "email": "user@example.com",
    "type": "access",
    "exp": 1234567890,
    "iat": 1234567000,
    "jti": "unique_token_id"
  },
  "signature": "..."
}
```

#### Token Management

```
Access Token:
  - Lifetime: 30 minutes
  - Storage: Memory only (Redux state)
  - Transmitted: Authorization header

Refresh Token:
  - Lifetime: 7 days
  - Storage: HttpOnly cookie
  - Transmitted: Cookie
  - Rotation: New token on use
```

### Security Layers

```
┌─────────────────────────────────────────────────────────┐
│                     Layer 7: Application                │
│  - Input validation (Pydantic/Zod)                      │
│  - SQL injection prevention (SQLAlchemy)                │
│  - XSS protection (React auto-escaping)                 │
│  - CSRF tokens                                          │
└─────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────┐
│                  Layer 6: Authentication                │
│  - JWT with RS256 algorithm                             │
│  - Bcrypt password hashing (12 rounds)                  │
│  - Session management                                   │
│  - Rate limiting (60 req/min)                           │
└─────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────┐
│                    Layer 5: Transport                   │
│  - TLS 1.3                                              │
│  - HTTPS only (HSTS enabled)                            │
│  - Certificate pinning                                  │
└─────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────┐
│                    Layer 4: Network                     │
│  - Firewall rules                                       │
│  - DDoS protection (CloudFlare)                         │
│  - VPN for admin access                                 │
└─────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────┐
│                   Layer 3: Data                         │
│  - Encryption at rest (AES-256)                         │
│  - Encrypted backups                                    │
│  - Secure key management                                │
└─────────────────────────────────────────────────────────┘
```

### Security Headers

```python
# Backend (FastAPI)
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "geolocation=(), microphone=(), camera=()"
}
```

---

## Scalability Design

### Horizontal Scaling Strategy

```
                    Load Balancer
                         │
        ┌────────────────┼────────────────┐
        │                │                │
    Server 1         Server 2         Server 3
    (Active)         (Active)         (Standby)
        │                │                │
        └────────────────┴────────────────┘
                         │
                   Shared Database
                   Shared Redis
```

### Database Scaling

**Read Replicas**
```
                  ┌─────────────┐
                  │   Primary   │
                  │  (Write)    │
                  └──────┬──────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
    ┌─────▼─────┐  ┌─────▼─────┐  ┌─────▼─────┐
    │ Replica 1 │  │ Replica 2 │  │ Replica 3 │
    │  (Read)   │  │  (Read)   │  │  (Read)   │
    └───────────┘  └───────────┘  └───────────┘
```

### Caching Strategy

**Multi-Level Cache**

```
Level 1: Browser Cache
  - Static assets: 1 year
  - API responses: No cache or short TTL

Level 2: CDN Cache (CloudFlare/Vercel)
  - Static pages: 1 hour
  - API responses: No cache

Level 3: Redis Cache
  - User sessions: 30 min
  - Exercise queries: 1 hour
  - Static data: 24 hours

Level 4: Database Query Cache
  - Frequently accessed queries
  - Automatically invalidated on writes
```

### Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| API Response Time | < 100ms (p95) | New Relic |
| Page Load Time | < 2s (LCP) | Lighthouse |
| Time to Interactive | < 3s | Lighthouse |
| Database Query Time | < 50ms (p95) | pg_stat_statements |
| Cache Hit Rate | > 80% | Redis INFO |
| Uptime | 99.9% | UptimeRobot |

---

## Technology Stack

### Complete Stack Overview

```yaml
Frontend:
  Framework: Next.js 14.2
  Runtime: Node.js 18 LTS
  Language: TypeScript 5.4
  UI Library: React 18.3
  Styling: Tailwind CSS 3.4
  State: Redux Toolkit 2.2
  Forms: React Hook Form 7.51
  Validation: Zod 3.23
  Testing: Jest 30 + Playwright 1.55

Backend:
  Framework: FastAPI 0.109
  Runtime: Python 3.11
  Server: Gunicorn + Uvicorn
  ORM: SQLAlchemy 2.0
  Migrations: Alembic 1.13
  Auth: Python-JOSE + Passlib
  Validation: Pydantic 2.6
  Testing: Pytest

Database:
  Primary: PostgreSQL 15
  Cache: Redis 7

External Services:
  AI: OpenAI GPT-4
  Monitoring: Sentry
  Analytics: (Optional) Google Analytics
  Email: (Optional) SendGrid

DevOps:
  CI/CD: GitHub Actions
  Containers: Docker
  Orchestration: Docker Compose
  Hosting: Railway/Render/Vercel
  CDN: CloudFlare/Vercel Edge

Development Tools:
  Version Control: Git
  Code Quality: ESLint, Prettier, Black, Flake8
  Type Checking: TypeScript, MyPy
  Pre-commit: Husky, lint-staged
```

### Dependency Matrix

**Frontend Dependencies**
- Production: 52 packages
- Development: 25 packages
- Total bundle size: ~250KB (gzipped)

**Backend Dependencies**
- Production: 18 packages
- Development: 12 packages
- Docker image size: ~450MB

---

## Disaster Recovery Architecture

### Backup Strategy

```
Daily Backups:
  ┌─────────────┐
  │  PostgreSQL │
  │   Primary   │
  └──────┬──────┘
         │
         │ pg_dump (2 AM UTC)
         ▼
  ┌──────────────┐
  │ Backup Server│
  │  (S3/B2)     │
  │              │
  │ Retention:   │
  │ - 7 days     │
  │ - 4 weeks    │
  │ - 12 months  │
  └──────────────┘
```

### Failover Plan

**Database Failover**
1. Detect primary failure (health check)
2. Promote replica to primary
3. Update DNS/connection string
4. Restart application servers
5. Monitor for issues

**Application Failover**
1. Health check fails
2. Load balancer removes from pool
3. Traffic routes to healthy servers
4. Auto-scale if needed
5. Alert ops team

### Recovery Time Objectives (RTO)

| Component | RTO | RPO |
|-----------|-----|-----|
| Application | 5 minutes | 0 |
| Database | 15 minutes | 5 minutes |
| Redis | 1 minute | 15 minutes |
| Full System | 30 minutes | 5 minutes |

---

## Monitoring Points

```
Application Metrics:
  - Request rate
  - Response time
  - Error rate
  - Active users

System Metrics:
  - CPU usage
  - Memory usage
  - Disk I/O
  - Network I/O

Database Metrics:
  - Connection pool
  - Query performance
  - Replication lag
  - Disk usage

Business Metrics:
  - User registrations
  - Exercises completed
  - Average session time
  - Retention rate
```

---

This architecture is designed to be:
- **Scalable**: Can handle 10x growth without major changes
- **Resilient**: Multiple layers of redundancy
- **Secure**: Defense in depth security model
- **Maintainable**: Clear separation of concerns
- **Observable**: Comprehensive monitoring and logging

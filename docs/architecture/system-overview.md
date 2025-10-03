# System Architecture Overview
## Spanish Subjunctive Practice Application

**Last Updated:** October 2, 2025
**Version:** 1.0
**Status:** Active Development

---

## Table of Contents
1. [High-Level Architecture](#high-level-architecture)
2. [Technology Stack](#technology-stack)
3. [Module Dependency Map](#module-dependency-map)
4. [Data Flow Diagrams](#data-flow-diagrams)
5. [Deployment Architecture](#deployment-architecture)
6. [Security Architecture](#security-architecture)

---

## High-Level Architecture

### Multi-Platform Architecture

The application implements a **tri-platform architecture** supporting desktop, web, and API-first access:

```mermaid
graph TB
    subgraph "Client Layer"
        Desktop["Desktop UI<br/>(PyQt5/PyQt6)"]
        WebUI["Web Frontend<br/>(React/Next.js)"]
        MobileWeb["Mobile Web<br/>(Responsive)"]
    end

    subgraph "Application Layer"
        DesktopCore["Desktop Core<br/>(Python)"]
        APIGateway["API Gateway<br/>(FastAPI)"]
    end

    subgraph "Business Logic Layer"
        SharedCore["Shared Core<br/>(Python Modules)"]
        Conjugation["Conjugation Engine"]
        TBLT["TBLT Scenarios"]
        SRS["Spaced Repetition"]
        Analytics["Learning Analytics"]
    end

    subgraph "Service Layer"
        OpenAI["OpenAI Service"]
        Auth["Authentication"]
        Gamification["Gamification"]
        Progress["Progress Tracking"]
    end

    subgraph "Data Layer"
        PostgreSQL[(PostgreSQL<br/>Database)]
        Redis[(Redis<br/>Cache)]
        FileStore["File Storage"]
    end

    Desktop --> DesktopCore
    WebUI --> APIGateway
    MobileWeb --> APIGateway

    DesktopCore --> SharedCore
    APIGateway --> SharedCore

    SharedCore --> Conjugation
    SharedCore --> TBLT
    SharedCore --> SRS
    SharedCore --> Analytics

    Conjugation --> OpenAI
    TBLT --> Auth
    SRS --> Gamification
    Analytics --> Progress

    OpenAI --> PostgreSQL
    Auth --> PostgreSQL
    Gamification --> PostgreSQL
    Progress --> PostgreSQL

    SharedCore --> Redis
    Progress --> FileStore
```

### Layered Architecture Pattern

```mermaid
graph LR
    subgraph "Presentation Layer"
        UI1["Desktop UI"]
        UI2["Web UI"]
        UI3["API Docs"]
    end

    subgraph "Application Layer"
        App1["Desktop App"]
        App2["FastAPI"]
    end

    subgraph "Domain Layer"
        Dom1["Conjugation"]
        Dom2["Pedagogy"]
        Dom3["Assessment"]
    end

    subgraph "Infrastructure Layer"
        Inf1["Database"]
        Inf2["Cache"]
        Inf3["External APIs"]
    end

    UI1 --> App1
    UI2 --> App2
    UI3 --> App2

    App1 --> Dom1
    App1 --> Dom2
    App2 --> Dom1
    App2 --> Dom2
    App2 --> Dom3

    Dom1 --> Inf1
    Dom2 --> Inf2
    Dom3 --> Inf3
```

---

## Technology Stack

### Backend Technologies

```mermaid
graph TD
    subgraph "API Framework"
        FastAPI["FastAPI 0.104.1<br/>Python 3.11+"]
        Uvicorn["Uvicorn 0.24.0<br/>ASGI Server"]
        Pydantic["Pydantic 2.5.0<br/>Validation"]
    end

    subgraph "Data Persistence"
        SQLAlchemy["SQLAlchemy 2.0.23<br/>ORM"]
        Alembic["Alembic 1.13.1<br/>Migrations"]
        PostgreSQL["PostgreSQL 14+<br/>Primary Database"]
        Redis["Redis 5.0.1<br/>Caching & Sessions"]
    end

    subgraph "Authentication & Security"
        Jose["python-jose 3.3.0<br/>JWT Tokens"]
        Passlib["passlib 1.7.4<br/>Password Hashing"]
        Cryptography["cryptography<br/>TLS/SSL"]
    end

    subgraph "Async & Real-time"
        WebSockets["websockets 12.0<br/>Real-time Communication"]
        Celery["Celery 5.3.4<br/>Task Queue"]
        HTTPX["httpx 0.25.2<br/>Async HTTP Client"]
    end

    subgraph "External Services"
        OpenAI["OpenAI API<br/>GPT-4 Integration"]
        Sentry["Sentry<br/>Error Tracking"]
    end

    FastAPI --> Uvicorn
    FastAPI --> Pydantic
    FastAPI --> SQLAlchemy
    SQLAlchemy --> Alembic
    SQLAlchemy --> PostgreSQL
    FastAPI --> Redis
    FastAPI --> Jose
    FastAPI --> Passlib
    FastAPI --> WebSockets
    FastAPI --> Celery
    FastAPI --> HTTPX
    HTTPX --> OpenAI
    FastAPI --> Sentry
```

### Frontend Technologies

```mermaid
graph TD
    subgraph "Desktop Stack"
        PyQt["PyQt5/PyQt6<br/>UI Framework"]
        QtDesigner["Qt Designer<br/>UI Development"]
        Python["Python 3.11+<br/>Core Language"]
    end

    subgraph "Web Stack"
        React["React 18+<br/>UI Library"]
        NextJS["Next.js 13+<br/>Framework"]
        TypeScript["TypeScript<br/>Type Safety"]
        TailwindCSS["Tailwind CSS<br/>Styling"]
    end

    subgraph "Build & Deploy"
        Webpack["Webpack<br/>Bundler"]
        Vercel["Vercel<br/>Hosting"]
        Docker["Docker<br/>Containerization"]
    end

    PyQt --> Python
    QtDesigner --> PyQt

    React --> NextJS
    NextJS --> TypeScript
    NextJS --> TailwindCSS
    NextJS --> Webpack
    Webpack --> Vercel

    Python --> Docker
    NextJS --> Docker
```

### Development & Testing Stack

| Category | Technologies |
|----------|-------------|
| **Testing** | pytest 7.4.3, pytest-asyncio 0.21.1, pytest-mock 3.12.0 |
| **Code Quality** | black 23.11.0, isort 5.12.0, flake8 6.1.0, mypy 1.7.1 |
| **Documentation** | Sphinx, OpenAPI/Swagger, Mermaid |
| **Version Control** | Git, GitHub Actions |
| **Monitoring** | Prometheus, Grafana, Sentry |
| **CI/CD** | GitHub Actions, Docker, Docker Compose |

---

## Module Dependency Map

### Backend Module Dependencies

```mermaid
graph TB
    subgraph "API Layer"
        AuthRoutes["api/routes/auth.py"]
        ReviewRoutes["api/routes/review.py"]
        ScenarioRoutes["api/routes/scenarios.py"]
    end

    subgraph "Service Layer"
        OpenAIService["services/openai_service.py"]
        TBLTService["services/tblt_service.py"]
        SRSService["services/spaced_repetition.py"]
        GamificationService["services/gamification.py"]
    end

    subgraph "Core Infrastructure"
        Database["core/database.py"]
        Security["core/security.py"]
        RedisClient["core/redis_client.py"]
        Config["core/config.py"]
    end

    subgraph "Data Models"
        UserModel["models/user.py"]
        ScenarioModel["models/scenario.py"]
        ProgressModel["models/progress.py"]
        SRSModel["models/srs_models.py"]
        AIMemoryModel["models/ai_memory.py"]
    end

    subgraph "Middleware"
        SecurityMiddleware["middleware/security.py"]
        RateLimiter["middleware/rate_limiter.py"]
        ErrorHandler["middleware/error_handling.py"]
    end

    AuthRoutes --> OpenAIService
    AuthRoutes --> Security
    AuthRoutes --> UserModel

    ReviewRoutes --> SRSService
    ReviewRoutes --> ProgressModel

    ScenarioRoutes --> TBLTService
    ScenarioRoutes --> ScenarioModel

    OpenAIService --> Database
    OpenAIService --> RedisClient
    OpenAIService --> AIMemoryModel

    TBLTService --> Database
    TBLTService --> ScenarioModel

    SRSService --> Database
    SRSService --> GamificationService
    SRSService --> SRSModel

    GamificationService --> ProgressModel

    Database --> Config
    RedisClient --> Config
    Security --> Config

    SecurityMiddleware --> Security
    RateLimiter --> RedisClient
```

### Desktop Application Dependencies

```mermaid
graph TB
    subgraph "UI Components"
        MainWindow["main.py<br/>Main Window"]
        EnhancedMain["main_enhanced.py<br/>Enhanced Features"]
    end

    subgraph "Core Business Logic"
        ConjugationRef["core/conjugation_reference.py"]
        LearningAnalytics["core/learning_analytics.py"]
        SessionMgr["core/session_manager.py"]
        TBLTScenarios["core/tblt_scenarios.py"]
        SubjunctiveCore["core/subjunctive_comprehensive.py"]
    end

    subgraph "UI System"
        Accessibility["ui_system/accessibility/"]
        Typography["ui_system/typography/"]
        Layout["ui_system/layout/"]
        Colors["ui_system/colors/"]
    end

    subgraph "Integration Modules"
        ErrorAnalysis["advanced_error_analysis.py"]
        FeedbackSystem["enhanced_feedback_system.py"]
    end

    MainWindow --> ConjugationRef
    MainWindow --> SessionMgr
    MainWindow --> TBLTScenarios

    EnhancedMain --> SubjunctiveCore
    EnhancedMain --> LearningAnalytics
    EnhancedMain --> ErrorAnalysis
    EnhancedMain --> FeedbackSystem

    MainWindow --> Accessibility
    MainWindow --> Typography
    MainWindow --> Layout
    MainWindow --> Colors

    EnhancedMain --> Accessibility
    EnhancedMain --> Typography
```

### Cross-Platform Shared Dependencies

```mermaid
graph LR
    subgraph "Desktop"
        DesktopConjugation["Conjugation Logic"]
        DesktopTBLT["TBLT Implementation"]
        DesktopAnalytics["Analytics Engine"]
    end

    subgraph "Backend"
        BackendConjugation["Conjugation API"]
        BackendTBLT["TBLT Service"]
        BackendAnalytics["Analytics Service"]
    end

    subgraph "Shared Core (Target)"
        SharedConjugation["shared/conjugation/"]
        SharedPedagogy["shared/pedagogy/"]
        SharedModels["shared/models/"]
    end

    DesktopConjugation -.->|"Should Use"| SharedConjugation
    BackendConjugation -.->|"Should Use"| SharedConjugation

    DesktopTBLT -.->|"Should Use"| SharedPedagogy
    BackendTBLT -.->|"Should Use"| SharedPedagogy

    DesktopAnalytics -.->|"Should Use"| SharedModels
    BackendAnalytics -.->|"Should Use"| SharedModels

    style SharedConjugation fill:#f9f,stroke:#333,stroke-width:2px
    style SharedPedagogy fill:#f9f,stroke:#333,stroke-width:2px
    style SharedModels fill:#f9f,stroke:#333,stroke-width:2px
```

---

## Data Flow Diagrams

### User Authentication Flow

```mermaid
sequenceDiagram
    participant User
    participant WebUI
    participant APIGateway
    participant AuthService
    participant Database
    participant Redis

    User->>WebUI: Enter credentials
    WebUI->>APIGateway: POST /api/auth/login
    APIGateway->>AuthService: authenticate(credentials)
    AuthService->>Database: Query user by email
    Database-->>AuthService: User data
    AuthService->>AuthService: Verify password hash
    AuthService->>AuthService: Generate JWT token
    AuthService->>Redis: Store session data
    Redis-->>AuthService: Session ID
    AuthService-->>APIGateway: JWT + Session ID
    APIGateway-->>WebUI: Auth token
    WebUI-->>User: Redirect to dashboard
```

### Exercise Generation & Submission Flow

```mermaid
sequenceDiagram
    participant User
    participant UI
    participant SessionManager
    participant ConjugationEngine
    participant TBLTService
    participant OpenAI
    participant Database
    participant SRSService

    User->>UI: Request new exercise
    UI->>SessionManager: Get user progress
    SessionManager->>Database: Query user stats
    Database-->>SessionManager: Progress data
    SessionManager->>SRSService: Get next review items
    SRSService-->>SessionManager: Due cards

    SessionManager->>TBLTService: Generate scenario
    TBLTService->>ConjugationEngine: Get verb forms
    ConjugationEngine-->>TBLTService: Conjugation data
    TBLTService->>OpenAI: Generate context
    OpenAI-->>TBLTService: Contextual scenario
    TBLTService-->>UI: Exercise data

    UI-->>User: Display exercise
    User->>UI: Submit answer
    UI->>SessionManager: Validate answer
    SessionManager->>ConjugationEngine: Check correctness
    ConjugationEngine-->>SessionManager: Validation result
    SessionManager->>SRSService: Update card strength
    SRSService->>Database: Save progress
    Database-->>SRSService: Confirmation
    SessionManager-->>UI: Feedback & next exercise
    UI-->>User: Show results
```

### Real-time Progress Tracking

```mermaid
sequenceDiagram
    participant User
    participant WebSocket
    participant ProgressTracker
    participant Analytics
    participant Database
    participant Cache

    User->>WebSocket: Connect to session
    WebSocket->>ProgressTracker: Initialize tracking
    ProgressTracker->>Cache: Get cached stats
    Cache-->>ProgressTracker: Recent data

    loop Exercise Completion
        User->>WebSocket: Complete exercise
        WebSocket->>ProgressTracker: Record attempt
        ProgressTracker->>Analytics: Analyze performance
        Analytics->>Analytics: Calculate metrics
        Analytics->>Cache: Update cached stats
        Analytics->>Database: Persist progress (async)
        ProgressTracker-->>WebSocket: Updated stats
        WebSocket-->>User: Real-time feedback
    end

    ProgressTracker->>Database: Final sync
    Database-->>ProgressTracker: Confirmation
```

### AI-Enhanced Feedback Flow

```mermaid
sequenceDiagram
    participant User
    participant UI
    participant FeedbackSystem
    participant OpenAI
    participant ErrorAnalyzer
    participant Database

    User->>UI: Submit incorrect answer
    UI->>FeedbackSystem: Process error
    FeedbackSystem->>ErrorAnalyzer: Analyze mistake type
    ErrorAnalyzer-->>FeedbackSystem: Error classification

    FeedbackSystem->>Database: Query similar errors
    Database-->>FeedbackSystem: Historical patterns

    FeedbackSystem->>OpenAI: Generate personalized feedback
    Note over FeedbackSystem,OpenAI: Context: user level, error type,<br/>historical patterns
    OpenAI-->>FeedbackSystem: Tailored explanation

    FeedbackSystem->>Database: Log feedback interaction
    FeedbackSystem-->>UI: Display feedback
    UI-->>User: Show explanation + examples
```

---

## Deployment Architecture

### Production Deployment (Docker)

```mermaid
graph TB
    subgraph "Load Balancer"
        Nginx["Nginx<br/>Reverse Proxy + SSL"]
    end

    subgraph "Application Tier"
        API1["FastAPI Instance 1"]
        API2["FastAPI Instance 2"]
        API3["FastAPI Instance 3"]
        Worker1["Celery Worker 1"]
        Worker2["Celery Worker 2"]
    end

    subgraph "Data Tier"
        PostgresPrimary["PostgreSQL Primary"]
        PostgresReplica["PostgreSQL Replica"]
        RedisMain["Redis Primary"]
        RedisReplica["Redis Replica"]
    end

    subgraph "Storage & Monitoring"
        S3["S3 Storage<br/>User Files"]
        Prometheus["Prometheus<br/>Metrics"]
        Sentry["Sentry<br/>Error Tracking"]
    end

    Nginx --> API1
    Nginx --> API2
    Nginx --> API3

    API1 --> PostgresPrimary
    API2 --> PostgresPrimary
    API3 --> PostgresPrimary

    PostgresPrimary --> PostgresReplica

    API1 --> RedisMain
    API2 --> RedisMain
    API3 --> RedisMain

    RedisMain --> RedisReplica

    Worker1 --> PostgresPrimary
    Worker2 --> PostgresPrimary
    Worker1 --> RedisMain
    Worker2 --> RedisMain

    API1 --> S3
    API2 --> S3
    API3 --> S3

    API1 --> Prometheus
    API2 --> Prometheus
    API3 --> Prometheus

    API1 --> Sentry
    API2 --> Sentry
    API3 --> Sentry
```

### Container Architecture

```mermaid
graph LR
    subgraph "Docker Compose Services"
        Backend["backend<br/>FastAPI + Uvicorn"]
        Frontend["frontend<br/>Next.js"]
        DB["db<br/>PostgreSQL 14"]
        Cache["redis<br/>Redis 7"]
        Queue["celery<br/>Task Queue"]
        Beat["celery-beat<br/>Scheduler"]
        Monitor["prometheus<br/>Monitoring"]
    end

    subgraph "Shared Resources"
        Network["app-network<br/>Docker Network"]
        AppVolume["app-data<br/>Application Data"]
        DBVolume["db-data<br/>Database Data"]
        RedisVolume["redis-data<br/>Cache Data"]
    end

    Backend --- Network
    Frontend --- Network
    DB --- Network
    Cache --- Network
    Queue --- Network
    Beat --- Network
    Monitor --- Network

    Backend --- AppVolume
    DB --- DBVolume
    Cache --- RedisVolume
```

---

## Security Architecture

### Security Layers

```mermaid
graph TB
    subgraph "Network Security"
        Firewall["Firewall<br/>Port Restrictions"]
        SSL["SSL/TLS<br/>Encryption"]
        DDoS["DDoS Protection<br/>Rate Limiting"]
    end

    subgraph "Application Security"
        Auth["JWT Authentication"]
        RBAC["Role-Based Access Control"]
        InputVal["Input Validation<br/>(Pydantic)"]
        CORS["CORS Configuration"]
        CSP["Content Security Policy"]
    end

    subgraph "Data Security"
        Encryption["Data Encryption at Rest"]
        PasswordHash["Password Hashing<br/>(bcrypt)"]
        SQLProtection["SQL Injection Protection<br/>(SQLAlchemy ORM)"]
        APIKeys["Encrypted API Keys"]
    end

    subgraph "Monitoring & Auditing"
        Logging["Centralized Logging"]
        AuditTrail["Audit Trail"]
        Alerting["Security Alerting"]
        Scanner["Vulnerability Scanning"]
    end

    Firewall --> SSL
    SSL --> DDoS
    DDoS --> Auth

    Auth --> RBAC
    RBAC --> InputVal
    InputVal --> CORS
    CORS --> CSP

    CSP --> Encryption
    Encryption --> PasswordHash
    PasswordHash --> SQLProtection
    SQLProtection --> APIKeys

    APIKeys --> Logging
    Logging --> AuditTrail
    AuditTrail --> Alerting
    Alerting --> Scanner
```

### Authentication & Authorization Flow

```mermaid
graph LR
    Request["Incoming Request"] --> RateLimiter["Rate Limiter<br/>Middleware"]
    RateLimiter --> CORS["CORS<br/>Middleware"]
    CORS --> JWTVerify["JWT Verification"]

    JWTVerify -->|Valid Token| CheckPermissions["Check Permissions<br/>(RBAC)"]
    JWTVerify -->|Invalid/Missing| Return401["Return 401<br/>Unauthorized"]

    CheckPermissions -->|Authorized| ProcessRequest["Process Request"]
    CheckPermissions -->|Forbidden| Return403["Return 403<br/>Forbidden"]

    ProcessRequest --> LogAccess["Log Access"]
    LogAccess --> ExecuteAction["Execute Action"]
    ExecuteAction --> Response["Return Response"]

    Return401 --> Response
    Return403 --> Response
```

---

## Performance Optimization Architecture

### Caching Strategy

```mermaid
graph TB
    Request["Request"] --> L1["L1: Application Cache<br/>(In-Memory)"]
    L1 -->|Cache Miss| L2["L2: Redis Cache<br/>(Distributed)"]
    L2 -->|Cache Miss| DB["L3: Database<br/>(Persistent)"]

    DB -->|Result| UpdateL2["Update Redis"]
    UpdateL2 --> UpdateL1["Update App Cache"]
    UpdateL1 --> Response["Response"]

    L1 -->|Cache Hit| Response
    L2 -->|Cache Hit| UpdateL1
```

### Async Processing Architecture

```mermaid
graph LR
    subgraph "Synchronous Flow"
        API["API Endpoint"] --> QuickOps["Quick Operations<br/><200ms"]
        QuickOps --> SyncResponse["Immediate Response"]
    end

    subgraph "Asynchronous Flow"
        API2["API Endpoint"] --> Queue["Task Queue<br/>(Celery + Redis)"]
        Queue --> Worker["Background Worker"]
        Worker --> LongOps["Long Operations<br/>AI, Bulk Processing"]
        LongOps --> DB["Database"]
        DB --> Notify["WebSocket Notification"]
        Notify --> Client["Client Update"]
    end

    API2 --> AsyncResponse["Task ID Response"]
```

---

## Next Steps

1. Review [Architecture Decision Records](./architecture-decision-records/)
2. Consult [Component Catalog](./component-catalog.md)
3. Review [Refactoring Roadmap](/docs/analysis/comprehensive-codebase-analysis.md#10-refactoring-roadmap)
4. Explore [API Documentation](../api/) (when available)

---

**Document Metadata**
- **Created:** October 2, 2025
- **Authors:** Architecture Documentation Agent
- **Review Cycle:** Monthly
- **Related Documents:** ADR-001, ADR-002, ADR-003, Component Catalog

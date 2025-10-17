# Refactoring Roadmap - Spanish Subjunctive Practice

**Project:** Spanish Subjunctive Practice Application
**Version:** 1.0
**Date:** October 2, 2025
**Status:** Draft for Review

---

## Executive Summary

This roadmap provides a **practical, phased approach** to refactoring the Spanish Subjunctive Practice codebase. The plan is designed to deliver **incremental value** while minimizing risk and maintaining application stability throughout the transformation.

**Total Timeline:** 24 weeks (6 months)
**Total Estimated Effort:** 496 hours (12.4 weeks FTE)
**Expected ROI:** 3-6 months break-even, 40% productivity increase

---

## Phase 1: Foundation & Organization (Weeks 1-2)

### Goals
- Establish clear project structure
- Set up code quality infrastructure
- Create baseline metrics
- Enable team alignment

### Tasks

#### Week 1: Documentation & Standards

**1.1 Create Architecture Documentation**
- [ ] Document current architecture (using comprehensive analysis)
- [ ] Create directory structure specification
- [ ] Map all major components and their relationships
- [ ] Document data flows and integration points

**Files to Create:**
```
docs/
├── architecture/
│   ├── OVERVIEW.md
│   ├── DIRECTORY_STRUCTURE.md
│   ├── DATA_FLOW.md
│   └── INTEGRATION_MAP.md
└── standards/
    ├── CODING_STANDARDS.md
    ├── TESTING_GUIDELINES.md
    └── COMMIT_CONVENTIONS.md
```

**Estimated Effort:** 16 hours

**1.2 Set Up Code Quality Tools**
```bash
# Install pre-commit hooks
pip install pre-commit
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
  - repo: https://github.com/PyCQA/isort
    rev: 5.12.0
    hooks:
      - id: isort
  - repo: https://github.com/PyCQA/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
EOF

pre-commit install
```

**1.3 Configure Coverage and Quality Metrics**
```bash
# Setup pytest coverage
cat > .coveragerc << EOF
[run]
source = src,backend
omit = */tests/*,*/migrations/*

[report]
precision = 2
show_missing = True
skip_covered = False

[html]
directory = htmlcov
EOF

# Add coverage to CI/CD
# Update .github/workflows/test.yml
```

**1.4 Security Scanning Setup**
```bash
# Add security tools
pip install bandit safety
cat > .bandit << EOF
[bandit]
exclude = /tests/,/migrations/
EOF

# Add to CI/CD pipeline
```

**Estimated Effort:** 8 hours

#### Week 2: Baseline & Initial Cleanup

**2.1 Measure Baseline Metrics**
```bash
# Run coverage
pytest --cov=src --cov=backend --cov-report=html --cov-report=term > coverage_baseline.txt

# Run complexity analysis
radon cc src/ backend/ -a > complexity_baseline.txt

# Run code duplication
radon mi src/ backend/ > maintainability_baseline.txt

# Security scan
bandit -r backend/ src/ > security_baseline.txt
safety check > dependencies_baseline.txt
```

**2.2 .gitignore Cleanup**
```bash
# Ensure all sensitive files ignored
cat >> .gitignore << EOF
# Environment variables
.env*
!.env.example

# IDE
.vscode/
.idea/
*.swp
*.swo

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
ENV/
build/
dist/
*.egg-info/

# Testing
.coverage
htmlcov/
.pytest_cache/

# Logs
*.log
```

**2.3 Identify Quick Wins**
- Mark obviously deprecated files
- Remove commented-out code
- Fix import order with isort
- Format all code with black

**Estimated Effort:** 8 hours

### Deliverables

- [ ] Architecture documentation complete
- [ ] Code quality tools configured and running in CI/CD
- [ ] Baseline metrics documented
- [ ] .gitignore updated and verified
- [ ] Quick wins implemented

### Success Metrics
- All team members can locate any module within 2 minutes
- CI/CD pipeline includes quality gates
- Baseline metrics established for tracking improvement

---

## Phase 2: Consolidation & Cleanup (Weeks 3-6)

### Goals
- Reduce root-level file clutter
- Organize test suite
- Create initial UI system package
- Remove deprecated code

### Week 3-4: File Reorganization

**3.1 Move Root-Level Business Logic**
```bash
# Create backup
git checkout -b refactor/phase2-consolidation

# Move files to src/core/
mv session_manager.py src/core/
mv learning_analytics.py src/core/
mv tblt_scenarios.py src/core/
mv conjugation_reference.py src/core/
mv advanced_error_analysis.py src/core/utilities/
mv enhanced_feedback_system.py src/core/utilities/

# Update imports across codebase
# Use IDE refactoring or search-and-replace carefully
```

**3.2 Consolidate Main Entry Points**
```python
# Decide on canonical entry points
main.py - Desktop application (keep)
main_web.py - Web application (keep)
railway_main.py - Railway deployment (keep in deployment/)

# Remove or merge
main_enhanced.py - Features should be in main.py
```

**3.3 Create Deprecated Module**
```python
# src/deprecated/__init__.py
"""
Deprecated modules kept for backward compatibility.
Will be removed in version 2.0.

Migration guides available in docs/migration/
"""
import warnings

warnings.warn(
    "This module is deprecated. See docs/migration/ for alternatives.",
    DeprecationWarning,
    stacklevel=2
)
```

**Estimated Effort:** 24 hours

### Week 5: Test Suite Organization

**5.1 Move All Tests to /tests/**
```bash
# Find misplaced tests
find . -name "test_*.py" -not -path "./tests/*" -not -path "./node_modules/*"

# Move to appropriate test directory
mv src/test_*.py tests/unit/
mv examples/test_*.py tests/integration/
```

**5.2 Organize Test Directory**
```bash
tests/
├── unit/
│   ├── test_conjugation.py
│   ├── test_tblt.py
│   ├── test_analytics.py
│   └── ui/
│       ├── test_accessibility.py
│       ├── test_typography.py
│       └── test_layout.py
├── integration/
│   ├── test_desktop_app.py
│   ├── test_web_app.py
│   └── test_api_integration.py
├── e2e/
│   └── test_user_workflows.py
├── performance/
│   └── test_load.py
├── security/
│   └── test_security_compliance.py
└── fixtures/
    └── test_data.py
```

**5.3 Consolidate Duplicate Tests**
```python
# Example: Merge UI color tests
# Before:
# - test_ui_colors.py
# - test_color_accessibility.py
# - test_color_compliance_final.py

# After:
# tests/unit/ui/test_color_system.py
# - Comprehensive test coverage
# - Remove duplicates
```

**Estimated Effort:** 16 hours

### Week 6: Initial UI System Package

**6.1 Create UI System Structure**
```python
src/ui_system/
├── __init__.py
├── accessibility/
│   ├── __init__.py
│   ├── manager.py          # Consolidated from 6 files
│   ├── theme.py
│   ├── wcag_compliance.py
│   └── tests/
│       └── test_accessibility.py
├── typography/
│   ├── __init__.py
│   ├── font_manager.py     # Consolidated from 5 files
│   ├── system.py
│   ├── sizes.py
│   └── tests/
│       └── test_typography.py
├── layout/
│   ├── __init__.py
│   ├── responsive.py       # Consolidated from 8 files
│   ├── spacing.py
│   ├── grid.py
│   └── tests/
│       └── test_layout.py
└── colors/
    ├── __init__.py
    ├── system.py           # Consolidated from 4 files
    ├── contrast.py
    ├── themes.py
    └── tests/
        └── test_colors.py
```

**6.2 Consolidation Strategy**
```python
# For each UI subsystem:
# 1. Identify canonical implementation
# 2. Merge features from variants
# 3. Create comprehensive tests
# 4. Mark old files as deprecated
# 5. Update imports across codebase

# Example for accessibility:
# FROM:
# - accessibility_demo.py
# - accessibility_integration.py
# - accessibility_integration_patch.py
# - accessibility_manager.py
# - accessibility_theme_integration.py

# TO:
# src/ui_system/accessibility/manager.py (consolidated)
```

**Estimated Effort:** 32 hours

### Deliverables

- [ ] Root directory has <10 Python files
- [ ] All tests in /tests/ with clear organization
- [ ] UI system package created with tests
- [ ] Deprecated files marked or removed
- [ ] All imports updated and tested

### Success Metrics
- 50% reduction in root-level Python files
- All tests pass after reorganization
- Test coverage maintained or improved
- No regression in application functionality

---

## Phase 3: Shared Core Extraction (Weeks 7-12)

### Goals
- Create platform-agnostic business logic
- Eliminate desktop/web duplication
- Standardize service interfaces
- Improve testability

### Week 7-8: Shared Package Creation

**7.1 Create Shared Package Structure**
```python
shared/
├── __init__.py
├── conjugation/
│   ├── __init__.py
│   ├── engine.py           # Core conjugation logic
│   ├── reference.py        # Reference data
│   ├── validators.py       # Validation rules
│   └── tests/
│       ├── test_engine.py
│       └── test_validators.py
├── pedagogy/
│   ├── __init__.py
│   ├── tblt.py             # Task-Based Language Teaching
│   ├── srs.py              # Spaced Repetition System
│   ├── analytics.py        # Learning analytics
│   ├── assessment.py       # Assessment logic
│   └── tests/
│       ├── test_tblt.py
│       ├── test_srs.py
│       └── test_analytics.py
├── models/
│   ├── __init__.py
│   ├── user.py             # User data model
│   ├── exercise.py         # Exercise model
│   ├── session.py          # Session model
│   ├── progress.py         # Progress tracking
│   └── tests/
│       └── test_models.py
└── utils/
    ├── __init__.py
    ├── text_processing.py
    ├── validators.py
    └── tests/
        └── test_utils.py
```

**7.2 Extract Conjugation Engine**
```python
# shared/conjugation/engine.py
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class ConjugationRequest:
    """Request for verb conjugation."""
    verb: str
    tense: str
    mood: str
    person: str
    number: str

@dataclass
class ConjugationResult:
    """Result of conjugation."""
    conjugated: str
    stem: str
    ending: str
    is_irregular: bool
    notes: Optional[str] = None

class ConjugationEngine:
    """Platform-agnostic conjugation engine."""

    def __init__(self, reference_data: Dict):
        self._reference = reference_data
        self._irregular_verbs = self._load_irregular_verbs()

    def conjugate(self, request: ConjugationRequest) -> ConjugationResult:
        """Conjugate verb according to request parameters."""
        # Implementation from existing code
        # Extracted from desktop and backend versions
        pass

    def validate_conjugation(self, verb: str, conjugated: str,
                            context: ConjugationRequest) -> bool:
        """Validate a conjugation."""
        pass

    def get_suggestions(self, partial: str, context: ConjugationRequest) -> List[str]:
        """Get conjugation suggestions."""
        pass
```

**Estimated Effort:** 32 hours

### Week 9-10: Platform Adaptation Layers

**9.1 Desktop Adapter**
```python
# src/core/conjugation_adapter.py
from shared.conjugation.engine import ConjugationEngine, ConjugationRequest
from shared.conjugation.reference import get_reference_data

class DesktopConjugationService:
    """Desktop UI adapter for conjugation engine."""

    def __init__(self):
        self._engine = ConjugationEngine(get_reference_data())

    def conjugate_for_ui(self, verb: str, tense: str, mood: str,
                         person: str, number: str) -> dict:
        """Conjugate and format for UI display."""
        request = ConjugationRequest(
            verb=verb, tense=tense, mood=mood,
            person=person, number=number
        )
        result = self._engine.conjugate(request)

        # Format for PyQt UI
        return {
            'conjugated': result.conjugated,
            'stem': result.stem,
            'ending': result.ending,
            'is_irregular': result.is_irregular,
            'notes': result.notes or '',
            'html_formatted': self._format_for_display(result)
        }

    def _format_for_display(self, result) -> str:
        """Format result with HTML for UI display."""
        # Desktop-specific formatting
        pass
```

**9.2 Backend Adapter**
```python
# backend/services/conjugation_service.py
from shared.conjugation.engine import ConjugationEngine, ConjugationRequest
from backend.schemas.conjugation import ConjugationRequestSchema, ConjugationResponseSchema

class APIConjugationService:
    """API adapter for conjugation engine."""

    def __init__(self, engine: ConjugationEngine):
        self._engine = engine

    async def conjugate(self, request: ConjugationRequestSchema) -> ConjugationResponseSchema:
        """Conjugate verb for API response."""
        core_request = ConjugationRequest(
            verb=request.verb,
            tense=request.tense,
            mood=request.mood,
            person=request.person,
            number=request.number
        )

        result = self._engine.conjugate(core_request)

        return ConjugationResponseSchema(
            conjugated=result.conjugated,
            stem=result.stem,
            ending=result.ending,
            is_irregular=result.is_irregular,
            notes=result.notes,
            metadata={
                'request_id': request.request_id,
                'timestamp': datetime.utcnow()
            }
        )
```

**Estimated Effort:** 24 hours

### Week 11-12: Service Layer Standardization

**11.1 Base Service Pattern**
```python
# shared/services/base.py
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional
import logging

T = TypeVar('T')
R = TypeVar('R')

class BaseService(ABC, Generic[T, R]):
    """Base class for all services."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._initialize()

    @abstractmethod
    def _initialize(self):
        """Initialize service resources."""
        pass

    @abstractmethod
    async def process(self, input_data: T) -> R:
        """Process input and return result."""
        pass

    def _handle_error(self, error: Exception, context: dict):
        """Standardized error handling."""
        self.logger.error(f"Error in {self.__class__.__name__}",
                         exc_info=error, extra=context)
        # Metrics, notifications, etc.
```

**11.2 Implement for Core Services**
```python
# shared/services/conjugation_service.py
from .base import BaseService
from shared.conjugation.engine import ConjugationEngine

class ConjugationService(BaseService[ConjugationRequest, ConjugationResult]):
    """Shared conjugation service."""

    def _initialize(self):
        self._engine = ConjugationEngine(get_reference_data())
        self.logger.info("Conjugation service initialized")

    async def process(self, request: ConjugationRequest) -> ConjugationResult:
        try:
            return self._engine.conjugate(request)
        except Exception as e:
            self._handle_error(e, {'request': request})
            raise

# Similarly for:
# - LearningAnalyticsService
# - TBLTService
# - SpacedRepetitionService
# - AssessmentService
```

**Estimated Effort:** 24 hours

### Deliverables

- [ ] Shared package created with core business logic
- [ ] Platform adapters implemented for desktop and web
- [ ] Service layer standardized
- [ ] Tests migrated to shared package (>85% coverage)
- [ ] Both platforms using shared core

### Success Metrics
- Code duplication reduced to <5%
- Shared modules have >85% test coverage
- Both platforms pass full test suites
- No functionality regressions

---

## Phase 4: Performance & Developer Experience (Weeks 13-18)

### Goals
- Optimize application performance
- Improve developer productivity
- Add comprehensive monitoring
- Reduce technical debt interest

### Week 13-14: Async AI Integration

**13.1 Implement Async OpenAI Client**
```python
# shared/ai/openai_client.py
import asyncio
from typing import Optional, List
import openai
from openai import AsyncOpenAI

class AsyncOpenAIClient:
    """Async OpenAI client with retry and caching."""

    def __init__(self, api_key: str, cache_backend: Optional[object] = None):
        self.client = AsyncOpenAI(api_key=api_key)
        self.cache = cache_backend
        self._rate_limiter = RateLimiter(max_per_minute=60)

    async def get_explanation(self, context: str, question: str) -> str:
        """Get AI explanation with caching."""
        cache_key = self._generate_cache_key(context, question)

        # Check cache
        if self.cache:
            cached = await self.cache.get(cache_key)
            if cached:
                return cached

        # Rate limiting
        await self._rate_limiter.acquire()

        # Make request with retry
        explanation = await self._make_request_with_retry(context, question)

        # Cache result
        if self.cache:
            await self.cache.set(cache_key, explanation, ttl=3600)

        return explanation

    async def _make_request_with_retry(self, context: str,
                                       question: str,
                                       max_retries: int = 3) -> str:
        """Make OpenAI request with exponential backoff."""
        for attempt in range(max_retries):
            try:
                response = await self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": context},
                        {"role": "user", "content": question}
                    ],
                    temperature=0.7,
                    max_tokens=200
                )
                return response.choices[0].message.content
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

**13.2 Request Queuing**
```python
# shared/ai/request_queue.py
from asyncio import Queue, create_task
from typing import Callable, Awaitable

class AIRequestQueue:
    """Queue for AI requests with prioritization."""

    def __init__(self, client: AsyncOpenAIClient, max_concurrent: int = 5):
        self.client = client
        self.queue = Queue()
        self.max_concurrent = max_concurrent
        self._workers: List[Task] = []

    async def start(self):
        """Start queue workers."""
        self._workers = [
            create_task(self._worker(i))
            for i in range(self.max_concurrent)
        ]

    async def _worker(self, worker_id: int):
        """Process requests from queue."""
        while True:
            request, future = await self.queue.get()
            try:
                result = await self.client.get_explanation(
                    request.context,
                    request.question
                )
                future.set_result(result)
            except Exception as e:
                future.set_exception(e)
            finally:
                self.queue.task_done()

    async def submit(self, context: str, question: str) -> Awaitable[str]:
        """Submit request to queue."""
        future = asyncio.Future()
        await self.queue.put((Request(context, question), future))
        return future
```

**Estimated Effort:** 32 hours

### Week 15-16: Frontend Optimization

**15.1 Bundle Analysis**
```bash
# Install bundle analyzer
npm install --save-dev webpack-bundle-analyzer

# Update next.config.js
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

module.exports = {
  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.plugins.push(
        new BundleAnalyzerPlugin({
          analyzerMode: 'static',
          reportFilename: './bundle-report.html'
        })
      );
    }
    return config;
  }
};

# Run analysis
npm run build
# Review bundle-report.html
```

**15.2 Code Splitting & Lazy Loading**
```typescript
// Implement route-based code splitting
import dynamic from 'next/dynamic'

// Before:
import ExerciseComponent from '../components/Exercise'

// After:
const ExerciseComponent = dynamic(() => import('../components/Exercise'), {
  loading: () => <LoadingSpinner />,
  ssr: false  // If component doesn't need SSR
})

// Implement component lazy loading
const HeavyComponent = dynamic(
  () => import('../components/HeavyComponent'),
  { loading: () => <div>Loading...</div> }
)
```

**15.3 Remove Unused Dependencies**
```bash
# Analyze dependencies
npx depcheck

# Remove unused packages
npm uninstall [unused-package-1] [unused-package-2] ...

# Update package.json with exact versions for critical deps
# Use ranges for development dependencies
```

**Estimated Effort:** 24 hours

### Week 17-18: Monitoring & APM

**17.1 Application Performance Monitoring**
```python
# Add Sentry integration
pip install sentry-sdk

# backend/core/monitoring.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

def initialize_monitoring(dsn: str, environment: str):
    """Initialize APM and error tracking."""
    sentry_sdk.init(
        dsn=dsn,
        environment=environment,
        traces_sample_rate=1.0 if environment == "development" else 0.1,
        profiles_sample_rate=1.0 if environment == "development" else 0.1,
        integrations=[
            FastApiIntegration(),
            SqlalchemyIntegration(),
        ],
    )
```

**17.2 Custom Metrics**
```python
# backend/core/metrics.py
from prometheus_client import Counter, Histogram, Gauge
import time

# Define metrics
conjugation_requests = Counter(
    'conjugation_requests_total',
    'Total number of conjugation requests',
    ['status']
)

conjugation_duration = Histogram(
    'conjugation_duration_seconds',
    'Time spent processing conjugation'
)

active_sessions = Gauge(
    'active_sessions',
    'Number of active user sessions'
)

# Use in service
class ConjugationService:
    @conjugation_duration.time()
    async def conjugate(self, request):
        try:
            result = await self._process(request)
            conjugation_requests.labels(status='success').inc()
            return result
        except Exception as e:
            conjugation_requests.labels(status='error').inc()
            raise
```

**17.3 Logging Strategy**
```python
# shared/logging/config.py
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'INFO',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/app.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'json',
            'level': 'INFO',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file'],
    },
}

def configure_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
```

**Estimated Effort:** 28 hours

### Deliverables

- [ ] Async AI client implemented with caching
- [ ] Frontend bundle size reduced by >40%
- [ ] APM and error tracking configured
- [ ] Custom metrics implemented
- [ ] Structured logging deployed

### Success Metrics
- API response time <200ms (p95)
- Frontend initial load <2s
- Frontend bundle <500KB gzipped
- 100% error tracking coverage

---

## Phase 5: Advanced Features & Scaling (Weeks 19-24)

### Goals
- Evaluate microservices architecture
- Implement advanced monitoring
- Create ML/AI pipeline
- Document scaling strategy

### Week 19-20: Architecture Evaluation

**19.1 Microservices Assessment**
```markdown
# docs/architecture/microservices-evaluation.md

## Current Monolith Analysis

### Bounded Contexts Identified:
1. **User Management** (Auth, Profile, Preferences)
2. **Conjugation Service** (Verb conjugation, validation)
3. **Learning Service** (TBLT, SRS, Analytics)
4. **AI Service** (OpenAI integration, NLP)
5. **Content Service** (Exercises, scenarios, reference data)

### Decision Criteria:
- **Migrate to microservices if:**
  - User base >50K active users
  - Team size >10 developers
  - Deployment frequency >10x/day
  - Different scaling needs for services

- **Stay monolithic if:**
  - User base <50K
  - Team size <10
  - Current architecture performs adequately
  - Operational complexity is a concern

### Recommendation:
Implement **modular monolith** pattern:
- Maintain single deployment
- Enforce strict module boundaries
- Prepare for future extraction
- Use message bus for module communication
```

**19.2 Module Boundary Enforcement**
```python
# tools/architecture_test.py
import pytest
from pathlib import Path

ALLOWED_DEPENDENCIES = {
    'backend.services.conjugation': [
        'shared.conjugation',
        'shared.models',
        'backend.core.database'
    ],
    'backend.services.learning': [
        'shared.pedagogy',
        'shared.models',
        'backend.core.database',
        'backend.services.conjugation'  # Allowed dependency
    ],
    # ... other modules
}

def test_module_dependencies():
    """Ensure modules only import from allowed dependencies."""
    violations = []

    for module, allowed in ALLOWED_DEPENDENCIES.items():
        actual_imports = get_imports_for_module(module)
        for import_path in actual_imports:
            if not any(import_path.startswith(a) for a in allowed):
                violations.append(f"{module} imports {import_path}")

    assert not violations, f"Module boundary violations: {violations}"
```

**Estimated Effort:** 24 hours

### Week 21-22: A/B Testing Infrastructure

**21.1 Feature Flag System**
```python
# shared/feature_flags/manager.py
from typing import Dict, Any, Optional
import hashlib

class FeatureFlags:
    """Feature flag management with A/B testing support."""

    def __init__(self, config_backend):
        self._backend = config_backend
        self._cache = {}

    def is_enabled(self, flag_name: str, user_id: Optional[str] = None,
                   context: Optional[Dict] = None) -> bool:
        """Check if feature is enabled for user."""
        flag_config = self._get_flag_config(flag_name)

        if not flag_config:
            return False

        # Global enable/disable
        if not flag_config['enabled']:
            return False

        # Percentage rollout
        if 'percentage' in flag_config:
            return self._is_in_rollout_group(
                flag_name,
                user_id,
                flag_config['percentage']
            )

        # Targeted rollout
        if 'targets' in flag_config and user_id:
            return user_id in flag_config['targets']

        return flag_config.get('default', False)

    def _is_in_rollout_group(self, flag_name: str, user_id: str,
                             percentage: int) -> bool:
        """Determine if user is in rollout percentage."""
        hash_input = f"{flag_name}:{user_id}".encode()
        hash_value = int(hashlib.md5(hash_input).hexdigest(), 16)
        return (hash_value % 100) < percentage

    def get_variant(self, experiment_name: str, user_id: str) -> str:
        """Get A/B test variant for user."""
        experiment = self._get_experiment_config(experiment_name)
        if not experiment:
            return 'control'

        # Consistent variant assignment
        hash_input = f"{experiment_name}:{user_id}".encode()
        hash_value = int(hashlib.md5(hash_input).hexdigest(), 16)

        cumulative = 0
        for variant in experiment['variants']:
            cumulative += variant['percentage']
            if (hash_value % 100) < cumulative:
                return variant['name']

        return 'control'
```

**21.2 Experiment Tracking**
```python
# shared/experiments/tracker.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ExperimentEvent:
    """Event in an A/B test experiment."""
    experiment_name: str
    user_id: str
    variant: str
    event_type: str  # 'exposure', 'conversion', 'metric'
    value: Optional[float] = None
    metadata: Optional[dict] = None
    timestamp: datetime = datetime.utcnow()

class ExperimentTracker:
    """Track A/B test events and metrics."""

    def __init__(self, backend):
        self._backend = backend

    async def track_exposure(self, experiment_name: str, user_id: str, variant: str):
        """Track when user is exposed to experiment variant."""
        event = ExperimentEvent(
            experiment_name=experiment_name,
            user_id=user_id,
            variant=variant,
            event_type='exposure'
        )
        await self._backend.store_event(event)

    async def track_conversion(self, experiment_name: str, user_id: str,
                               variant: str, value: Optional[float] = None):
        """Track conversion event."""
        event = ExperimentEvent(
            experiment_name=experiment_name,
            user_id=user_id,
            variant=variant,
            event_type='conversion',
            value=value
        )
        await self._backend.store_event(event)
```

**Estimated Effort:** 28 hours

### Week 23-24: ML Pipeline & Documentation

**23.1 ML Model Versioning**
```python
# shared/ml/model_registry.py
from pathlib import Path
import joblib
from typing import Any, Optional
import hashlib

class ModelRegistry:
    """Registry for ML models with versioning."""

    def __init__(self, storage_path: Path):
        self._storage = storage_path
        self._storage.mkdir(parents=True, exist_ok=True)

    def save_model(self, model: Any, name: str, version: str,
                   metadata: dict) -> str:
        """Save model with version and metadata."""
        model_path = self._storage / name / version
        model_path.mkdir(parents=True, exist_ok=True)

        # Save model
        joblib.dump(model, model_path / 'model.pkl')

        # Save metadata
        metadata['version'] = version
        metadata['saved_at'] = datetime.utcnow().isoformat()
        metadata['model_hash'] = self._compute_hash(model)

        with open(model_path / 'metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)

        return str(model_path)

    def load_model(self, name: str, version: Optional[str] = None) -> Any:
        """Load model by name and version (latest if not specified)."""
        if version is None:
            version = self._get_latest_version(name)

        model_path = self._storage / name / version / 'model.pkl'
        return joblib.load(model_path)
```

**23.2 Scaling Documentation**
```markdown
# docs/architecture/scaling-strategy.md

## Horizontal Scaling Strategy

### Load Balancing
- **Tool:** Nginx or cloud load balancer
- **Method:** Round-robin with health checks
- **Session Affinity:** Not required (stateless API)

### Database Scaling
**Read Replicas:**
- Primary: Write operations
- Replicas (2+): Read operations
- Connection pooling: 20 connections per instance

**Partitioning Strategy:**
- Users: Partition by user_id hash
- Sessions: Partition by date
- Exercises: Not partitioned (relatively small)

### Caching Strategy
**Redis Cluster:**
- Session data: TTL 1 hour
- Conjugation results: TTL 24 hours
- User preferences: TTL 1 hour
- AI responses: TTL 1 week

### Auto-scaling Rules
**Backend API:**
- Scale up: CPU > 70% for 5 minutes
- Scale down: CPU < 30% for 15 minutes
- Min instances: 2
- Max instances: 20

**Database:**
- Scale up: Connection pool utilization > 80%
- Scale up: Query latency p95 > 100ms

### Cost Optimization
- Use spot instances for non-critical workloads
- Implement connection pooling
- Optimize database queries
- Implement aggressive caching
```

**Estimated Effort:** 28 hours

### Deliverables

- [ ] Microservices evaluation complete with decision
- [ ] Feature flag system implemented
- [ ] A/B testing infrastructure deployed
- [ ] ML model registry created
- [ ] Scaling strategy documented

### Success Metrics
- Architecture supports 100K+ users
- Feature flags enable rapid experimentation
- Model deployments versioned and tracked
- Scaling procedures documented and tested

---

## Risk Mitigation

### Testing Strategy for Each Phase

**Before Each Phase:**
1. Create feature branch
2. Full test suite baseline
3. Performance benchmarks
4. Security scan

**During Each Phase:**
1. Unit tests for all new code
2. Integration tests for changed interfaces
3. Regression tests for existing functionality
4. Code review by 2+ developers

**After Each Phase:**
1. Deploy to staging
2. Run full test suite
3. Performance comparison
4. Security scan
5. Staged production rollout
6. Monitor for 48 hours
7. Document lessons learned

### Rollback Procedures

**For Each Deployment:**
```bash
# Tag current production
git tag production-$(date +%Y%m%d-%H%M%S)

# Deploy new version
./scripts/deploy.sh

# If issues detected within 48 hours:
git checkout production-YYYYMMDD-HHMMSS
./scripts/deploy.sh --force

# Investigate issues
# Fix in development
# Re-deploy when ready
```

---

## Progress Tracking

### Weekly Checkpoints

**Every Friday:**
- Review completed tasks
- Update metrics dashboard
- Assess risks
- Adjust timeline if needed
- Document blockers

### Metrics Dashboard

```markdown
## Phase 2 Progress (Example)

### Completed (Week 3):
- [x] Moved 8/12 root files to src/core/
- [x] Created deprecated module
- [x] Updated 45% of imports
- [ ] Remaining: main_enhanced.py consolidation

### Metrics:
- Root Python files: 18 → 12 (33% reduction)
- Test coverage: 67% (maintained)
- Build time: 1.8 minutes (no change)
- No regressions detected

### Blockers:
- main_enhanced.py has features not in main.py
- Need product decision on which features to keep

### Next Week:
- Complete root file consolidation
- Begin test suite organization
- Set up test coverage reporting
```

---

## Resource Requirements

### Team Composition

**Recommended:**
- 1 Senior Developer (architecture decisions, code review)
- 2 Mid-level Developers (implementation)
- 1 QA Engineer (testing, validation)
- 1 DevOps Engineer (part-time, CI/CD, monitoring)

**Minimum:**
- 1 Senior Developer
- 1 Mid-level Developer

### Time Allocation

**Full Team (Recommended):**
- Total calendar time: 24 weeks
- Total effort: 496 hours
- With 4-person team: ~12 weeks calendar time

**Minimum Team:**
- Total calendar time: 24 weeks
- Total effort: 496 hours
- With 2-person team: ~25 weeks calendar time

### Budget Considerations

**Tool Costs (Annual):**
- APM (Sentry/DataDog): $300-$1,200
- CI/CD (GitHub Actions): $0-$500
- Monitoring (Prometheus/Grafana): $0 (self-hosted)
- Security scanning: $0 (open source tools)

**Infrastructure (Monthly):**
- Staging environment: $100-$200
- Testing infrastructure: $50-$100

**Total Estimated Cost:**
- Year 1: $1,000-$3,000
- Ongoing: $500-$1,500/year

---

## Conclusion

This roadmap provides a **systematic, low-risk approach** to refactoring the Spanish Subjunctive Practice codebase. By following the phased approach, the team can:

1. **Deliver continuous value** - Each phase provides tangible benefits
2. **Minimize risk** - Small, tested changes with rollback capability
3. **Maintain velocity** - Features can still be developed during refactoring
4. **Build technical excellence** - Establish practices for long-term success

### Next Steps

1. **Review this roadmap** with the development team
2. **Adjust timelines** based on team size and priorities
3. **Get stakeholder approval** for Phase 1-2
4. **Begin Phase 1** with documentation and tooling
5. **Schedule weekly reviews** to track progress

### Success Criteria

**At 6 months:**
- Code duplication <5%
- Test coverage >80%
- Developer onboarding <4 hours
- Deployment time <10 minutes
- Zero-downtime deployments
- Comprehensive monitoring

**Long-term:**
- 40% increase in development velocity
- 60% reduction in bugs
- Platform supports 100K+ users
- Team can ship features confidently

---

**Document Version:** 1.0
**Last Updated:** October 2, 2025
**Next Review:** After Phase 1 completion

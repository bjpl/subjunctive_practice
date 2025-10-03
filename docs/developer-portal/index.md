# Spanish Subjunctive Practice - Developer Portal

Welcome to the comprehensive developer documentation for the Spanish Subjunctive Practice application. This portal provides everything you need to understand, integrate, and extend the platform.

## Quick Links

### Getting Started
- [Quick Start Guide](./getting-started.md) - Get up and running in 5 minutes
- [Architecture Overview](./architecture.md) - Understand the system design
- [Installation Guide](./getting-started.md#installation) - Detailed setup instructions

### API & SDK Documentation
- [API Reference](./api-reference.md) - Complete REST API documentation
- [Python SDK Guide](./sdk-guides/python-sdk.md) - Python client library usage
- [TypeScript SDK Guide](./sdk-guides/typescript-sdk.md) - TypeScript/JavaScript integration
- [Core Modules](./sdk-guides/core-modules.md) - Framework-agnostic JavaScript core

### Learning Resources
- [Interactive Tutorials](./tutorials/README.md) - Step-by-step coding tutorials
- [Code Examples](./examples/README.md) - Ready-to-use code samples
- [Best Practices](./best-practices.md) - Development guidelines
- [Troubleshooting](./troubleshooting.md) - Common issues and solutions

### Contributing
- [Contribution Guide](./contributing.md) - How to contribute code
- [Code of Conduct](./code-of-conduct.md) - Community guidelines
- [Development Workflow](./best-practices.md#development-workflow) - Git and CI/CD practices

## Platform Overview

The Spanish Subjunctive Practice platform is a comprehensive language learning application built with:

- **Backend**: FastAPI (Python 3.8+) with PostgreSQL and Redis
- **Frontend**: React with TypeScript and modern UI components
- **Desktop**: PyQt5 with cross-platform support
- **Core Logic**: Framework-agnostic JavaScript modules for maximum reusability

### Key Features

- **Adaptive Learning**: Spaced repetition (SM-2 algorithm) with intelligent difficulty adjustment
- **TBLT Methodology**: Task-Based Language Teaching with real-world scenarios
- **Comprehensive Coverage**: All subjunctive tenses, triggers, and irregular verbs
- **Analytics Dashboard**: Detailed progress tracking and learning insights
- **Multi-Platform**: Web, desktop, and mobile-ready architecture

## Architecture Highlights

```
┌─────────────────────────────────────────────────────────────┐
│                      Client Applications                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   Web    │  │  Mobile  │  │ Desktop  │  │   API    │   │
│  │  React   │  │   PWA    │  │  PyQt5   │  │ Clients  │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
└───────┼─────────────┼─────────────┼─────────────┼──────────┘
        │             │             │             │
        └─────────────┴─────────────┴─────────────┘
                         │
        ┌────────────────┴────────────────┐
        │      REST API (FastAPI)          │
        │  - Authentication & Authorization │
        │  - Exercise Generation            │
        │  - Progress Tracking              │
        │  - Analytics & Reporting          │
        └────────┬────────────────┬─────────┘
                 │                │
        ┌────────┴─────┐   ┌──────┴────────┐
        │  PostgreSQL  │   │     Redis     │
        │  (Persistent)│   │   (Cache)     │
        └──────────────┘   └───────────────┘
                 │
        ┌────────┴────────────────────────┐
        │   Core Business Logic (JS)      │
        │  - Conjugation Engine            │
        │  - Exercise Generator            │
        │  - Spaced Repetition             │
        │  - Error Analysis                │
        └──────────────────────────────────┘
```

## Development Workflow

### 1. Environment Setup
```bash
# Clone repository
git clone <repository-url>
cd subjunctive_practice

# Install dependencies
npm install
pip install -r requirements.txt

# Setup pre-commit hooks
pre-commit install

# Configure environment
cp .env.example .env
# Edit .env with your configuration
```

### 2. Run Development Servers
```bash
# Backend API
npm run dev:backend

# Frontend web app
npm run dev:frontend

# Desktop application
python main.py
```

### 3. Testing
```bash
# All tests
npm test

# Specific test suites
npm run test:unit
npm run test:integration
npm run test:e2e

# Backend tests
npm run test:backend
```

## Common Use Cases

### Building a Custom Learning App
See [Tutorial: Building Your First Exercise](./tutorials/01-first-exercise.md)

### Integrating with Existing Platform
See [Integration Guide](./examples/integration-examples.md)

### Extending Exercise Types
See [Tutorial: Custom Exercise Types](./tutorials/03-custom-exercises.md)

### Adding Analytics Features
See [Analytics SDK Guide](./sdk-guides/analytics.md)

## API Quick Reference

### Generate Exercise
```http
POST /api/v1/exercises/generate
Content-Type: application/json
Authorization: Bearer <token>

{
  "difficulty": "intermediate",
  "tense": "present_subjunctive",
  "exercise_type": "conjugation",
  "count": 10
}
```

### Submit Answer
```http
POST /api/v1/exercises/submit
Content-Type: application/json
Authorization: Bearer <token>

{
  "exercise_id": "uuid",
  "user_answer": "hable",
  "response_time_ms": 3500
}
```

### Get Progress
```http
GET /api/v1/users/me/progress
Authorization: Bearer <token>
```

See [Complete API Reference](./api-reference.md) for full documentation.

## SDK Quick Examples

### Python
```python
from subjunctive_practice import SubjunctiveClient

client = SubjunctiveClient(api_key="your-key")

# Generate exercises
exercises = client.exercises.generate(
    difficulty="intermediate",
    count=10
)

# Submit answer
result = client.exercises.submit(
    exercise_id=exercises[0].id,
    answer="hable"
)
```

### TypeScript
```typescript
import { SubjunctiveCore } from '@subjunctive/core';

const core = new SubjunctiveCore({
  defaultDifficulty: 'intermediate',
  enableSpacedRepetition: true
});

// Generate exercise
const exercise = core.generateExercise();

// Submit answer
const result = core.submitAnswer(exercise, 'hable', 3500);
```

## Resources

### Documentation
- [Architecture Decision Records](../architecture/ARCHITECTURE_DECISION_RECORDS.md)
- [Database Schema](./architecture.md#database-schema)
- [API Specification (OpenAPI)](../../openapi_spec.json)

### Code Quality
- [Testing Strategy](../TESTING_STRATEGY.md)
- [Code Standards](../standards/README.md)
- [Performance Guidelines](./best-practices.md#performance)

### Deployment
- [Deployment Guide](../DEPLOYMENT_GUIDE.md)
- [Docker Setup](../DOCKER_DEPLOYMENT.md)
- [Production Checklist](../PRODUCTION_CHECKLIST.md)

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/subjunctive_practice/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/subjunctive_practice/discussions)
- **Email**: support@example.com

## License

This project is licensed under the MIT License. See the [LICENSE](../../LICENSE) file for details.

---

**Last Updated**: October 2, 2025
**Version**: 1.0.0
**Maintainers**: Development Team

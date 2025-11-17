# Spanish Subjunctive Practice

A full-stack web application for learning and mastering the Spanish subjunctive mood through interactive exercises, real-time validation, and gamified progress tracking.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Live Demo](#live-demo)
- [Technical Overview](#technical-overview)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Overview

This application provides a comprehensive learning environment for Spanish subjunctive mastery. Built with modern web technologies, it offers interactive exercises with instant feedback, personalized learning paths, and gamification elements to maintain engagement and track progress.

The system adapts to user performance, identifies weak areas, and provides targeted practice while maintaining detailed analytics on accuracy, completion rates, and learning progression.

## Features

### Core Functionality
- **Interactive Exercise System**: Multiple exercise types including fill-in-blank, conjugation, translation, multiple choice, and trigger identification
- **Real-time Validation**: Instant feedback with detailed explanations for every answer
- **Progress Tracking**: Comprehensive statistics, accuracy rates, and performance analytics
- **Adaptive Difficulty**: Dynamic difficulty adjustment based on user performance

### Learning Features
- **Gamification**: Experience points, level progression, achievement badges, and daily streaks
- **Personalized Learning**: Weak area identification and custom recommendations
- **Spaced Repetition**: Algorithm-driven exercise scheduling for optimal retention
- **Comprehensive Explanations**: Detailed grammar rules and usage examples

### Technical Features
- **Modern Stack**: FastAPI backend with Next.js 14+ frontend
- **Type Safety**: Full TypeScript implementation with strict mode
- **Authentication**: JWT-based auth with access and refresh tokens
- **Database**: PostgreSQL with SQLAlchemy ORM and Alembic migrations
- **API Documentation**: Auto-generated Swagger/OpenAPI documentation

## Live Demo

Technical demonstration available as a portfolio project showcasing:
- Full-stack architecture with separated concerns
- Modern web development practices
- Scalable database design
- Secure authentication implementation
- Responsive UI with accessibility features

## Technical Overview

### Architecture

**Backend (FastAPI)**
- Python 3.10+ with type hints and async/await patterns
- PostgreSQL database with connection pooling
- RESTful API design with comprehensive validation
- Environment-based configuration management
- Comprehensive error handling and logging

**Frontend (Next.js)**
- Next.js 14+ with App Router
- TypeScript strict mode with full type coverage
- Tailwind CSS for styling
- Redux Toolkit with RTK Query for state management
- React Hook Form with Zod validation
- Radix UI component primitives

**Key Technologies**
- Database: PostgreSQL 14+, SQLAlchemy, Alembic
- Authentication: JWT with refresh token rotation
- API: FastAPI with Pydantic validation
- Frontend: React 18, Next.js 14, TypeScript
- Styling: Tailwind CSS, Radix UI
- Testing: Pytest (backend), Jest (frontend)

## Installation

<details>
<summary>Installation Steps</summary>

### Prerequisites

- Node.js 18+ and npm
- Python 3.10+ and pip
- PostgreSQL 14+ (or SQLite for development)
- Git

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Initialize database
alembic upgrade head
python scripts/init_db.py

# Start backend server
uvicorn main:app --reload
```

Backend available at: `http://localhost:8000`
API Documentation: `http://localhost:8000/api/docs`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local
# Edit .env.local with API URL

# Start development server
npm run dev
```

Frontend available at: `http://localhost:3000`

</details>

## Usage

### For Portfolio Review

This project demonstrates:

**Architecture & Design**
- Clean separation of concerns
- RESTful API design principles
- Database schema optimization
- Component-based UI architecture

**Development Practices**
- Type-safe code throughout the stack
- Comprehensive error handling
- Environment-based configuration
- Migration-based database versioning

**User Experience**
- Responsive design for all screen sizes
- Accessible UI following WCAG guidelines
- Progressive enhancement approach
- Optimistic UI updates for better UX

### For Local Development

1. Register an account at `http://localhost:3000/auth/register`
2. Complete the onboarding flow
3. Access practice exercises from the dashboard
4. Track progress through the statistics page

## Project Structure

```
subjunctive_practice/
├── backend/                 # FastAPI backend
│   ├── alembic/            # Database migrations
│   ├── api/                # API endpoints and routes
│   ├── core/               # Core configuration and utilities
│   ├── models/             # SQLAlchemy database models
│   ├── schemas/            # Pydantic request/response schemas
│   ├── services/           # Business logic layer
│   ├── tests/              # Backend test suite
│   └── main.py             # Application entry point
├── frontend/                # Next.js frontend
│   ├── app/                # Next.js App Router pages
│   ├── components/         # React components
│   ├── hooks/              # Custom React hooks
│   ├── lib/                # Utility functions
│   ├── store/              # Redux state management
│   ├── types/              # TypeScript type definitions
│   └── tests/              # Frontend test suite
└── docs/                   # Documentation
    ├── API_DOCUMENTATION.md
    ├── DEVELOPMENT.md
    └── DEPLOYMENT_GUIDE.md
```

## Development

### Code Style

**Backend (Python)**
- PEP 8 style guide with Black formatting
- Type hints for all function signatures
- Docstrings for public functions and classes
- Pytest for testing with 80%+ coverage target

**Frontend (TypeScript)**
- Airbnb TypeScript style guide
- Prettier for code formatting
- Strict TypeScript configuration
- Props interfaces for all components
- Jest and React Testing Library for tests

### Testing

```bash
# Backend tests
cd backend
pytest                              # Run all tests
pytest --cov=backend               # With coverage
pytest tests/test_auth.py          # Specific test file

# Frontend tests
cd frontend
npm test                            # Run all tests
npm test -- --watch                # Watch mode
npm test -- --coverage             # With coverage
```

### Environment Configuration

<details>
<summary>Environment Variables</summary>

**Backend (.env)**
```env
# Application
APP_NAME="Spanish Subjunctive Practice API"
ENVIRONMENT="development"
DEBUG=true

# Security
SECRET_KEY="your-secret-key-min-32-chars"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL="postgresql://user:password@localhost:5432/subjunctive_practice"
# Or for development: DATABASE_URL="sqlite:///./dev.db"

# CORS
CORS_ORIGINS=["http://localhost:3000"]
```

**Frontend (.env.local)**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_APP_NAME="Spanish Subjunctive Practice"
```

</details>

### Available Scripts

**Backend**
```bash
uvicorn main:app --reload         # Development server
pytest --cov                       # Tests with coverage
alembic revision --autogenerate   # Create migration
alembic upgrade head              # Apply migrations
black backend/                    # Format code
```

**Frontend**
```bash
npm run dev                        # Development server
npm run build                      # Production build
npm test                           # Run tests
npm run lint                       # Lint code
npm run type-check                 # TypeScript check
```

## Contributing

Contributions welcome. Please follow these guidelines:

1. Fork the repository
2. Create a feature branch from `develop`
3. Follow existing code style and conventions
4. Add tests for new functionality
5. Ensure all tests pass
6. Update documentation as needed
7. Submit a pull request

**Commit Message Format**
```
<type>(<scope>): <description>

Examples:
feat(auth): add password reset functionality
fix(exercises): correct accent validation
docs(api): update endpoint documentation
```

## License

MIT License - See LICENSE file for details.

---

**Repository**: https://github.com/bjpl/subjunctive_practice
**Documentation**: See `/docs` directory for detailed guides

Built with FastAPI, Next.js, PostgreSQL, and modern web technologies.

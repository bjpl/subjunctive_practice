# Spanish Subjunctive Practice

A comprehensive web application for learning and mastering the Spanish subjunctive mood through interactive exercises, personalized feedback, and gamified progress tracking.

## Features

- **Interactive Exercise System**: Multiple exercise types including fill-in-blank, conjugation, translation, and trigger identification
- **Real-time Validation**: Instant feedback with detailed explanations for every answer
- **Progress Tracking**: Comprehensive statistics, accuracy rates, and performance analytics
- **Gamification**: Experience points, level progression, achievement badges, and daily streaks
- **Personalized Learning**: Adaptive difficulty, weak area identification, and custom recommendations
- **Modern Tech Stack**: FastAPI backend with Next.js frontend for optimal performance

## Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with Python 3.10+
- **Database**: PostgreSQL (production) / SQLite (development)
- **Authentication**: JWT-based with access and refresh tokens
- **API Documentation**: Auto-generated Swagger/OpenAPI docs
- **ORM**: SQLAlchemy with Alembic migrations

### Frontend (Next.js)
- **Framework**: Next.js 14+ with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Redux Toolkit with RTK Query
- **UI Components**: Radix UI primitives
- **Form Handling**: React Hook Form with Zod validation

## Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.10+ and pip
- **PostgreSQL** 14+ (or use SQLite for development)
- **Git**

### Installation

#### 1. Clone Repository

```bash
git clone <repository-url>
cd subjunctive_practice
```

#### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your configuration

# Initialize database
alembic upgrade head
python scripts/init_db.py

# Start backend server
uvicorn main:app --reload
```

Backend will be available at: http://localhost:8000
API Documentation: http://localhost:8000/api/docs

#### 3. Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install

# Copy environment template
cp .env.example .env.local
# Edit .env.local with your API URL

# Start frontend server
npm run dev
```

Frontend will be available at: http://localhost:3000

### First Steps

1. **Register an Account**
   - Navigate to http://localhost:3000/auth/register
   - Create a new user account

2. **Start Practicing**
   - Login with your credentials
   - Go to the Practice page
   - Start completing exercises

3. **Track Your Progress**
   - View your dashboard for statistics
   - Monitor your level and XP
   - Check your accuracy and streaks

## Project Structure

```
subjunctive_practice/
├── backend/                 # FastAPI backend
│   ├── alembic/            # Database migrations
│   ├── api/                # API endpoints
│   │   └── routes/         # Route modules
│   ├── core/               # Core functionality
│   ├── models/             # SQLAlchemy models
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic
│   ├── scripts/            # Utility scripts
│   ├── tests/              # Backend tests
│   ├── main.py             # Application entry point
│   └── requirements.txt    # Python dependencies
├── frontend/                # Next.js frontend
│   ├── app/                # Next.js App Router pages
│   ├── components/         # React components
│   │   ├── ui/            # Base UI components
│   │   ├── features/      # Feature components
│   │   └── layout/        # Layout components
│   ├── hooks/              # Custom React hooks
│   ├── lib/                # Utilities and helpers
│   ├── store/              # Redux store
│   │   ├── slices/        # Redux slices
│   │   └── services/      # RTK Query services
│   ├── styles/             # Global styles
│   ├── types/              # TypeScript definitions
│   └── package.json        # Node dependencies
└── docs/                   # Documentation
    ├── INTEGRATION_GUIDE.md     # Integration guide
    ├── API_DOCUMENTATION.md     # API reference
    ├── COMPONENT_GUIDE.md       # Component usage
    ├── TROUBLESHOOTING.md       # Common issues
    ├── USER_GUIDE.md            # User documentation
    └── DEVELOPMENT.md           # Developer guide
```

## Environment Configuration

### Backend (.env)

```env
# Application
APP_NAME="Spanish Subjunctive Practice API"
VERSION="1.0.0"
ENVIRONMENT="development"
DEBUG=true

# API
API_V1_PREFIX="/api"
HOST="0.0.0.0"
PORT=8000

# Security
SECRET_KEY="your-secret-key-min-32-chars"
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=["http://localhost:3000"]
CORS_ALLOW_CREDENTIALS=true

# Database
DATABASE_URL="postgresql://user:password@localhost:5432/subjunctive_practice"
# Or for development:
# DATABASE_URL="sqlite:///./dev.db"

# Optional
REDIS_URL="redis://localhost:6379/0"
OPENAI_API_KEY="your-openai-key"
```

### Frontend (.env.local)

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api

# Application
NEXT_PUBLIC_APP_NAME="Spanish Subjunctive Practice"
NEXT_PUBLIC_APP_VERSION="1.0.0"
```

## Available Scripts

### Backend

```bash
# Start development server
uvicorn main:app --reload

# Run tests
pytest

# Run tests with coverage
pytest --cov=backend --cov-report=html

# Create database migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Initialize/reset database
python scripts/init_db.py --reset

# Format code
black backend/

# Lint code
flake8 backend/
```

### Frontend

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run tests
npm test

# Run tests in watch mode
npm test -- --watch

# Lint code
npm run lint

# Format code
npm run format

# Type check
npm run type-check
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/me` - Get current user info

### Exercises
- `GET /api/exercises` - Get exercises (with filters)
- `GET /api/exercises/{id}` - Get specific exercise
- `POST /api/exercises/submit` - Submit answer for validation
- `GET /api/exercises/types/available` - Get available exercise types

### Progress
- `GET /api/progress` - Get user progress
- `GET /api/progress/statistics` - Get detailed statistics
- `GET /api/progress/achievements` - Get user achievements

### System
- `GET /health` - Health check
- `GET /api/docs` - Interactive API documentation

Full API documentation available at: http://localhost:8000/api/docs

## Technology Stack

### Backend Technologies
- **FastAPI**: Modern, fast web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **Alembic**: Database migration tool
- **Pydantic**: Data validation using Python type annotations
- **Passlib**: Password hashing with bcrypt
- **Python-Jose**: JWT token handling
- **Uvicorn**: ASGI server

### Frontend Technologies
- **Next.js**: React framework with App Router
- **React**: UI library
- **TypeScript**: Type-safe JavaScript
- **Redux Toolkit**: State management
- **RTK Query**: Data fetching and caching
- **React Hook Form**: Form handling
- **Zod**: Schema validation
- **Tailwind CSS**: Utility-first CSS framework
- **Radix UI**: Accessible component primitives
- **Axios**: HTTP client
- **Lucide React**: Icon library

## Development

### Code Style

**Backend (Python):**
- Follow PEP 8 style guide
- Use Black for formatting
- Type hints required
- Docstrings for all public functions

**Frontend (TypeScript):**
- Follow Airbnb TypeScript style guide
- Use Prettier for formatting
- Strict TypeScript mode
- Props interfaces for all components

### Testing

**Backend:**
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py

# Run with coverage report
pytest --cov=backend --cov-report=html
```

**Frontend:**
```bash
# Run all tests
npm test

# Run in watch mode
npm test -- --watch

# Generate coverage report
npm test -- --coverage
```

### Git Workflow

1. Create feature branch from `develop`
2. Make changes and commit using conventional commits
3. Push branch and create pull request
4. Wait for CI/CD checks and code review
5. Merge to `develop` after approval

**Commit Message Format:**
```
<type>(<scope>): <description>

Examples:
feat(auth): add password reset functionality
fix(exercises): correct validation for accents
docs(api): update endpoint documentation
```

## Deployment

### Docker

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access services
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
# Database: localhost:5432
```

### Production Deployment

#### Backend (Railway/Render/Heroku)
1. Set environment variables
2. Configure PostgreSQL database
3. Run migrations: `alembic upgrade head`
4. Start with Gunicorn: `gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker`

#### Frontend (Vercel/Netlify)
1. Connect GitHub repository
2. Set `NEXT_PUBLIC_API_URL` to production backend URL
3. Deploy with automatic builds on push

## Documentation

Comprehensive documentation is available in the `/docs` directory:

- **[Integration Guide](./docs/INTEGRATION_GUIDE.md)**: Complete setup and integration instructions
- **[API Documentation](./docs/API_DOCUMENTATION.md)**: Detailed API endpoint reference with examples
- **[Component Guide](./docs/COMPONENT_GUIDE.md)**: Frontend component usage and best practices
- **[Troubleshooting Guide](./docs/TROUBLESHOOTING.md)**: Common issues and solutions
- **[User Guide](./docs/USER_GUIDE.md)**: End-user documentation and feature explanations
- **[Development Guide](./docs/DEVELOPMENT.md)**: Developer workflow and coding standards
- **[Database Schema](./docs/DATABASE_SCHEMA.md)**: Database structure and relationships
- **[State Management](./docs/STATE_MANAGEMENT.md)**: Redux store architecture

## Key Features Explained

### Exercise System
- **Multiple Types**: Fill-in-blank, conjugation, translation, multiple choice, trigger identification
- **Difficulty Levels**: 1 (Easy) to 5 (Expert)
- **Instant Validation**: Real-time answer checking with detailed feedback
- **Hints**: Context-sensitive hints available for each exercise
- **Explanations**: Comprehensive explanations for correct answers

### Progress Tracking
- **Experience Points**: Earn XP for correct answers (100 base + time bonuses)
- **Level System**: 20 levels from beginner to master
- **Accuracy Tracking**: Overall and per-exercise-type accuracy rates
- **Streak System**: Track consecutive days of practice
- **Statistics**: Detailed analytics on performance and weak areas

### Gamification
- **Achievements**: Unlock badges for milestones, streaks, and mastery
- **Daily Goals**: Set and track daily exercise targets
- **Leaderboards**: Compare progress with other learners (coming soon)
- **Rewards**: Visual feedback and celebration for accomplishments

### Personalization
- **Adaptive Difficulty**: System suggests appropriate difficulty levels
- **Weak Area Identification**: Automatically identifies areas needing practice
- **Custom Settings**: Customize session length, notifications, and preferences
- **Progress Insights**: AI-powered recommendations (when OpenAI configured)

## Browser Support

- Chrome/Edge (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Mobile browsers (iOS Safari, Chrome Android)

## Performance

- **Backend**: Average response time < 100ms
- **Frontend**: First Contentful Paint < 1.5s
- **Lighthouse Score**: 90+ across all metrics
- **Accessibility**: WCAG 2.1 AA compliant

## Security

- **Authentication**: JWT with secure token rotation
- **Password Hashing**: bcrypt with configurable rounds
- **CORS**: Configurable allowed origins
- **Rate Limiting**: Prevent abuse (60 req/min per IP)
- **Input Validation**: Comprehensive validation on all inputs
- **SQL Injection Protection**: Parameterized queries via SQLAlchemy

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure:
- All tests pass
- Code follows style guidelines
- Documentation is updated
- Commits follow conventional commit format

## Troubleshooting

Common issues and solutions are documented in the [Troubleshooting Guide](./docs/TROUBLESHOOTING.md).

**Quick fixes:**

```bash
# Backend not starting
# Check if virtual environment is activated
# Verify all dependencies are installed
pip install -r requirements.txt

# Frontend build errors
# Clear cache and reinstall
rm -rf node_modules .next
npm install

# Database connection issues
# Verify DATABASE_URL in .env
# Check if PostgreSQL is running
# Try SQLite for quick testing
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions, issues, or feature requests:
- **Documentation**: Check the `/docs` directory
- **Issues**: Open a GitHub issue
- **Email**: support@subjunctivepractice.com
- **Community**: Join our Discord server

## Acknowledgments

- Spanish language experts who reviewed exercise content
- Open source community for amazing tools and libraries
- Beta testers for valuable feedback

## Roadmap

### Version 1.1 (Q1 2025)
- Mobile apps (iOS & Android)
- Audio pronunciation for exercises
- Spaced repetition algorithm improvements
- Custom exercise creation

### Version 1.2 (Q2 2025)
- Leaderboards and competitions
- Multiplayer practice mode
- Advanced AI-powered insights
- Teacher dashboard

### Version 2.0 (Q3 2025)
- Additional Spanish tenses
- Other Spanish grammar topics
- Expansion to other languages
- API for third-party integrations

## Project Status

**Current Version**: 1.0.0
**Status**: Active Development
**Last Updated**: October 2025

---

Made with ❤️ for Spanish language learners worldwide.

Happy learning! ¡Buena suerte!

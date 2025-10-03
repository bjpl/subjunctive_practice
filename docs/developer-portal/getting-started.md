# Getting Started Guide

Welcome! This guide will help you set up your development environment and build your first integration with the Spanish Subjunctive Practice platform.

## Prerequisites

Before you begin, ensure you have:

- **Node.js** 16+ and npm 8+
- **Python** 3.8+
- **PostgreSQL** 13+ (for backend development)
- **Redis** 6+ (optional, for caching)
- **Git** for version control

## Quick Start (5 Minutes)

### 1. Clone and Install

```bash
# Clone repository
git clone <repository-url>
cd subjunctive_practice

# Install all dependencies
npm install
pip install -r requirements.txt

# Install development tools
pip install -r requirements-test.txt
```

### 2. Environment Configuration

```bash
# Create environment file
cp .env.example .env

# Edit .env with your settings
nano .env
```

Minimum required configuration:
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/subjunctive_db

# Security
SECRET_KEY=your-secret-key-here

# Optional: OpenAI for AI-powered features
OPENAI_API_KEY=sk-...
```

### 3. Database Setup

```bash
# Create database
createdb subjunctive_db

# Run migrations
cd backend
alembic upgrade head

# Seed initial data (optional)
python database/seeds.py
```

### 4. Run Development Servers

```bash
# Terminal 1: Backend API
npm run dev:backend

# Terminal 2: Frontend (in new terminal)
npm run dev:frontend

# Terminal 3: Desktop app (optional, in new terminal)
python main.py
```

### 5. Verify Installation

Open your browser to:
- **Web App**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health

## Installation Methods

### Method 1: Automated Setup (Recommended)

```bash
# Run setup script
chmod +x scripts/setup-dev-tools.sh
./scripts/setup-dev-tools.sh
```

This script:
- Installs Node.js dependencies
- Installs Python dependencies
- Sets up pre-commit hooks
- Installs Playwright browsers
- Verifies TypeScript configuration
- Runs initial code quality checks
- Creates .env file from template

### Method 2: Docker Setup

```bash
# Build and start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

Services available:
- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

### Method 3: Manual Setup

#### Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-test.txt

# Setup database
alembic upgrade head
```

#### Frontend Setup

```bash
# Install dependencies
npm install

# Build TypeScript
npm run build

# Start dev server
npm run dev:frontend
```

## Your First Integration

### Example 1: Using the Core JavaScript Library

```javascript
import SpanishSubjunctiveCore from './src/core/index.js';

// Initialize
const core = new SpanishSubjunctiveCore({
  defaultDifficulty: 'Intermediate',
  enableSpacedRepetition: true,
  autoSave: true
});

// Generate an exercise
const exercise = core.generateExercise();
console.log(exercise);
// Output:
// {
//   id: "ex_123",
//   question: "Conjugate 'hablar' in Present Subjunctive for 'yo'",
//   verb: "hablar",
//   tense: "Present Subjunctive",
//   person: "yo",
//   trigger: "quiero que",
//   expectedAnswer: "hable"
// }

// Submit answer
const result = core.submitAnswer(exercise, 'hable', 3500);
console.log(result.validation.isCorrect);  // true
console.log(result.feedback.message);      // "¡Excelente! ..."

// Get learning dashboard
const dashboard = core.getDashboard();
console.log(`Accuracy: ${dashboard.session.accuracy}%`);
console.log(`Streak: ${dashboard.streak.current} days`);
```

### Example 2: Using the REST API

```javascript
// 1. Authenticate
const authResponse = await fetch('http://localhost:8000/api/v1/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  })
});
const { access_token } = await authResponse.json();

// 2. Generate exercises
const exercisesResponse = await fetch('http://localhost:8000/api/v1/exercises/generate', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${access_token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    difficulty: 'intermediate',
    tense: 'present_subjunctive',
    count: 10
  })
});
const exercises = await exercisesResponse.json();

// 3. Submit answer
const submitResponse = await fetch('http://localhost:8000/api/v1/exercises/submit', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${access_token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    exercise_id: exercises[0].id,
    user_answer: 'hable',
    response_time_ms: 3500
  })
});
const result = await submitResponse.json();

// 4. Get progress
const progressResponse = await fetch('http://localhost:8000/api/v1/users/me/progress', {
  headers: { 'Authorization': `Bearer ${access_token}` }
});
const progress = await progressResponse.json();
```

### Example 3: Python Backend Integration

```python
from subjunctive_practice.core import SubjunctiveCore

# Initialize core
core = SubjunctiveCore(
    default_difficulty='intermediate',
    enable_spaced_repetition=True
)

# Generate exercise
exercise = core.generate_exercise()
print(f"Question: {exercise.question}")
print(f"Verb: {exercise.verb}")

# Validate answer
is_correct, feedback = core.validate_answer(
    exercise=exercise,
    user_answer='hable'
)

print(f"Correct: {is_correct}")
print(f"Feedback: {feedback.message}")
```

## Development Workflow

### 1. Code Quality Tools

The project uses automated tools that run on every commit:

```bash
# Format all files
npm run format

# Lint code
npm run lint

# Type check TypeScript
npm run type-check

# Run all pre-commit hooks manually
pre-commit run --all-files
```

### 2. Testing

```bash
# Run all tests
npm test

# Run specific test suites
npm run test:unit           # Unit tests
npm run test:integration    # Integration tests
npm run test:e2e           # End-to-end tests
npm run test:backend       # Python backend tests

# Run with coverage
npm run test:coverage

# Watch mode
npm run test:watch
```

### 3. Database Migrations

```bash
# Create new migration
cd backend
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1

# View migration history
alembic history
```

### 4. Git Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit (pre-commit hooks run automatically)
git add .
git commit -m "Add new feature"

# Push and create pull request
git push origin feature/your-feature-name
```

## Project Structure

```
subjunctive_practice/
├── backend/                 # FastAPI backend
│   ├── api/                # API routes
│   ├── core/               # Core configuration
│   ├── database/           # Database models
│   └── services/           # Business logic
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   └── api/           # API client
│   └── public/            # Static assets
├── src/                    # Source code
│   ├── core/              # Core JavaScript modules
│   ├── desktop_app/       # PyQt5 desktop app
│   └── web/               # Web-specific code
├── tests/                  # Test files
│   ├── backend/           # Backend tests
│   └── web/               # Frontend tests
├── docs/                   # Documentation
│   └── developer-portal/  # This documentation
├── scripts/                # Utility scripts
├── config/                 # Configuration files
└── examples/               # Code examples
```

## Configuration Options

### Environment Variables

See [.env.example](../../.env.example) for all available options:

```env
# Application
ENVIRONMENT=development
DEBUG=true
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/db
DATABASE_ECHO=false
DATABASE_POOL_SIZE=10

# Security
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Optional Services
REDIS_URL=redis://localhost:6379/0
OPENAI_API_KEY=sk-...
```

### Application Configuration

Modify `backend/core/config.py` for advanced settings:

```python
class Settings(BaseSettings):
    # Spaced repetition settings
    default_ease_factor: float = 2.5
    minimum_interval_days: int = 1

    # Exercise generation
    default_exercise_count: int = 10
    max_exercise_count: int = 50

    # Performance
    rate_limit_requests: int = 100
    rate_limit_window: int = 60
```

## Next Steps

Now that you have everything set up:

1. **Learn the Architecture**: Read [Architecture Overview](./architecture.md)
2. **Explore the API**: Check out [API Reference](./api-reference.md)
3. **Try Tutorials**: Follow [Interactive Tutorials](./tutorials/README.md)
4. **See Examples**: Browse [Code Examples](./examples/README.md)
5. **Best Practices**: Review [Development Best Practices](./best-practices.md)

## Troubleshooting

Having issues? Check our [Troubleshooting Guide](./troubleshooting.md) for common problems and solutions.

### Common Issues

**Database connection errors**
```bash
# Check PostgreSQL is running
pg_isready -h localhost -p 5432

# Verify connection
psql -U user -d subjunctive_db -h localhost
```

**Port already in use**
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

**Import errors in Python**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Getting Help

- **Documentation**: Browse this developer portal
- **Issues**: Report bugs on GitHub Issues
- **Discussions**: Ask questions in GitHub Discussions
- **Email**: Contact support@example.com

---

**Next**: [Architecture Overview](./architecture.md) →

# Development Workflow Guide

## Overview

This guide provides comprehensive information for developers working on the Spanish Subjunctive Practice application.

## Table of Contents

1. [Development Setup](#development-setup)
2. [Project Structure](#project-structure)
3. [Development Workflow](#development-workflow)
4. [Coding Standards](#coding-standards)
5. [Testing Strategy](#testing-strategy)
6. [Git Workflow](#git-workflow)
7. [Adding New Features](#adding-new-features)
8. [Debugging](#debugging)

---

## Development Setup

### Prerequisites

- **Node.js** 18+ and npm/yarn
- **Python** 3.10+ and pip
- **PostgreSQL** 14+ (or SQLite for quick testing)
- **Git** for version control
- **VS Code** (recommended) or preferred IDE

### Initial Setup

```bash
# Clone repository
git clone <repository-url>
cd subjunctive_practice

# Setup backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
cp .env.example .env
# Edit .env with your settings
alembic upgrade head
python scripts/init_db.py

# Setup frontend
cd ../frontend
npm install
cp .env.example .env.local
# Edit .env.local

# Start development servers
# Terminal 1 - Backend
cd backend
uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### VS Code Setup

**Recommended Extensions:**
- Python (Microsoft)
- Pylance
- ESLint
- Prettier
- Tailwind CSS IntelliSense
- GitLens
- Thunder Client (API testing)

**Workspace Settings** (`.vscode/settings.json`):
```json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter"
  }
}
```

---

## Project Structure

### Backend Structure

```
backend/
├── alembic/                 # Database migrations
│   ├── versions/           # Migration scripts
│   └── env.py             # Alembic configuration
├── api/                    # API endpoints
│   └── routes/            # Route modules
│       ├── auth.py        # Authentication
│       ├── exercises.py   # Exercise CRUD
│       └── progress.py    # Progress tracking
├── core/                   # Core functionality
│   ├── config.py          # Settings and configuration
│   ├── security.py        # JWT and password handling
│   ├── middleware.py      # Custom middleware
│   └── database.py        # Database connection
├── models/                 # SQLAlchemy models
│   ├── user.py            # User models
│   ├── exercise.py        # Exercise models
│   └── progress.py        # Progress models
├── schemas/                # Pydantic schemas
│   ├── user.py            # User validation
│   ├── exercise.py        # Exercise validation
│   └── progress.py        # Progress validation
├── services/               # Business logic
│   ├── exercise_service.py
│   ├── progress_service.py
│   └── ai_service.py
├── utils/                  # Utilities
│   └── helpers.py         # Helper functions
├── scripts/                # Utility scripts
│   ├── init_db.py         # Database initialization
│   └── seed_data.py       # Seed data
├── tests/                  # Tests
│   ├── test_auth.py
│   ├── test_exercises.py
│   └── test_progress.py
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
└── pytest.ini             # Pytest configuration
```

### Frontend Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── auth/              # Auth pages
│   ├── dashboard/         # Dashboard
│   ├── practice/          # Practice interface
│   ├── progress/          # Progress pages
│   ├── settings/          # Settings
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   └── providers.tsx      # Redux provider
├── components/             # React components
│   ├── ui/                # Base UI components
│   ├── features/          # Feature components
│   ├── layout/            # Layout components
│   └── common/            # Shared components
├── hooks/                  # Custom hooks
│   ├── useAuth.ts
│   ├── useExercise.ts
│   └── useProgress.ts
├── lib/                    # Libraries
│   ├── api-client.ts      # API client
│   └── utils.ts           # Utilities
├── store/                  # Redux store
│   ├── slices/            # Redux slices
│   ├── services/          # RTK Query services
│   ├── selectors/         # Memoized selectors
│   └── store.ts           # Store config
├── styles/                 # Styles
│   └── globals.css        # Global styles
├── types/                  # TypeScript types
│   └── index.ts
├── public/                 # Static assets
├── package.json            # Dependencies
├── tsconfig.json           # TypeScript config
└── tailwind.config.ts      # Tailwind config
```

---

## Development Workflow

### Daily Development Routine

1. **Pull latest changes**
```bash
git pull origin main
```

2. **Create feature branch**
```bash
git checkout -b feature/your-feature-name
```

3. **Start development servers**
```bash
# Backend
cd backend && uvicorn main:app --reload

# Frontend
cd frontend && npm run dev
```

4. **Make changes and test**
```bash
# Run tests frequently
cd backend && pytest
cd frontend && npm test
```

5. **Commit changes**
```bash
git add .
git commit -m "feat: add new feature"
```

6. **Push and create PR**
```bash
git push origin feature/your-feature-name
# Create pull request on GitHub
```

### Hot Reload

**Backend:**
- Uvicorn auto-reloads on file changes
- Changes take effect immediately
- Check terminal for errors

**Frontend:**
- Next.js Fast Refresh
- Instant UI updates
- Preserves component state

### Environment Management

**Backend:**
```bash
# Development
ENVIRONMENT=development
DEBUG=true

# Staging
ENVIRONMENT=staging
DEBUG=false

# Production
ENVIRONMENT=production
DEBUG=false
```

**Frontend:**
```bash
# Development
.env.local

# Production
.env.production
```

---

## Coding Standards

### Python (Backend)

**Style Guide:** PEP 8

**Formatting:**
```bash
# Format with Black
black backend/

# Lint with Flake8
flake8 backend/

# Type check with mypy
mypy backend/
```

**Code Style:**
```python
# Good
def get_exercise_by_id(exercise_id: str) -> Optional[Exercise]:
    """
    Retrieve exercise by ID.

    Args:
        exercise_id: Unique exercise identifier

    Returns:
        Exercise object or None if not found
    """
    return db.query(Exercise).filter(Exercise.id == exercise_id).first()

# Docstrings
# Use Google-style docstrings
# Include type hints
# Document exceptions

# Naming
class ExerciseService:  # PascalCase for classes
    def calculate_score(self, is_correct: bool) -> int:  # snake_case for functions
        BASE_SCORE = 100  # UPPER_CASE for constants
        user_score = 0  # snake_case for variables
```

### TypeScript (Frontend)

**Style Guide:** Airbnb TypeScript

**Formatting:**
```bash
# Format with Prettier
npm run format

# Lint with ESLint
npm run lint

# Type check
npm run type-check
```

**Code Style:**
```typescript
// Good
interface ExerciseProps {
  exercise: Exercise;
  onSubmit: (answer: string) => void;
  isSubmitting?: boolean;
}

export function ExerciseCard({ exercise, onSubmit, isSubmitting = false }: ExerciseProps) {
  const [answer, setAnswer] = useState<string>('');

  const handleSubmit = async () => {
    await onSubmit(answer);
  };

  return (
    <Card>
      {/* Component JSX */}
    </Card>
  );
}

// Naming
// PascalCase for components, interfaces, types
// camelCase for variables, functions
// UPPER_CASE for constants
```

### Commit Messages

Follow **Conventional Commits**:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Build/tooling changes

**Examples:**
```bash
feat(auth): add password reset functionality
fix(exercises): correct validation for accented characters
docs(api): update endpoint documentation
refactor(progress): optimize statistics calculation
test(exercises): add unit tests for validation
```

---

## Testing Strategy

### Backend Testing (Pytest)

**Test Structure:**
```
tests/
├── conftest.py           # Shared fixtures
├── test_auth.py          # Authentication tests
├── test_exercises.py     # Exercise tests
├── test_progress.py      # Progress tests
└── test_integration.py   # Integration tests
```

**Running Tests:**
```bash
# All tests
pytest

# Specific file
pytest tests/test_auth.py

# Specific test
pytest tests/test_auth.py::test_user_registration

# With coverage
pytest --cov=backend --cov-report=html

# Verbose output
pytest -v

# Stop on first failure
pytest -x
```

**Example Test:**
```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_user_registration():
    """Test user can register successfully."""
    response = client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "SecurePass123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert "password" not in data

def test_login_success():
    """Test user can login with correct credentials."""
    # Setup: Register user
    client.post("/api/auth/register", json={...})

    # Test login
    response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "SecurePass123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
```

### Frontend Testing (Jest + React Testing Library)

**Test Structure:**
```
src/
├── components/
│   └── __tests__/
│       └── ExerciseCard.test.tsx
├── hooks/
│   └── __tests__/
│       └── useAuth.test.ts
└── store/
    └── __tests__/
        └── authSlice.test.ts
```

**Running Tests:**
```bash
# All tests
npm test

# Watch mode
npm test -- --watch

# Coverage
npm test -- --coverage

# Specific file
npm test ExerciseCard
```

**Example Test:**
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { ExerciseCard } from '../ExerciseCard';

describe('ExerciseCard', () => {
  const mockExercise = {
    id: 'ex_001',
    prompt: 'Test prompt',
    type: 'present_subjunctive',
    difficulty: 2
  };

  it('renders exercise prompt', () => {
    render(<ExerciseCard exercise={mockExercise} onSubmit={jest.fn()} />);
    expect(screen.getByText('Test prompt')).toBeInTheDocument();
  });

  it('calls onSubmit when answer submitted', async () => {
    const onSubmit = jest.fn();
    render(<ExerciseCard exercise={mockExercise} onSubmit={onSubmit} />);

    const input = screen.getByPlaceholderText('Enter your answer');
    const submitButton = screen.getByText('Submit');

    fireEvent.change(input, { target: { value: 'hable' } });
    fireEvent.click(submitButton);

    expect(onSubmit).toHaveBeenCalledWith('hable');
  });
});
```

---

## Git Workflow

### Branching Strategy

```
main                    # Production-ready code
├── develop            # Development branch
    ├── feature/*      # New features
    ├── fix/*          # Bug fixes
    ├── refactor/*     # Refactoring
    └── docs/*         # Documentation
```

### Workflow

```bash
# 1. Start new feature
git checkout develop
git pull origin develop
git checkout -b feature/add-leaderboard

# 2. Make changes
# ... code ...

# 3. Commit
git add .
git commit -m "feat(leaderboard): add user ranking system"

# 4. Push
git push origin feature/add-leaderboard

# 5. Create Pull Request
# On GitHub, create PR to merge into develop

# 6. After PR approved and merged
git checkout develop
git pull origin develop
git branch -d feature/add-leaderboard
```

### Pre-commit Hooks

**Setup:**
```bash
# Backend
cd backend
pre-commit install

# This runs before each commit:
# - Black formatting
# - Flake8 linting
# - Import sorting
# - Trailing whitespace removal
```

---

## Adding New Features

### Adding a New API Endpoint

**1. Create Pydantic Schema** (`backend/schemas/feature.py`):
```python
from pydantic import BaseModel

class FeatureCreate(BaseModel):
    name: str
    description: str

class FeatureResponse(BaseModel):
    id: str
    name: str
    description: str
    created_at: datetime
```

**2. Create Route** (`backend/api/routes/feature.py`):
```python
from fastapi import APIRouter, Depends
from ...schemas.feature import FeatureCreate, FeatureResponse

router = APIRouter(prefix="/features", tags=["Features"])

@router.post("", response_model=FeatureResponse)
async def create_feature(
    feature: FeatureCreate,
    current_user = Depends(get_current_active_user)
):
    # Implementation
    pass
```

**3. Register Router** (`backend/main.py`):
```python
from .api.routes import feature

app.include_router(feature.router, prefix="/api")
```

**4. Add Tests** (`backend/tests/test_feature.py`):
```python
def test_create_feature():
    response = client.post("/api/features", json={...})
    assert response.status_code == 201
```

### Adding a New Frontend Component

**1. Create Component** (`frontend/components/features/NewFeature.tsx`):
```typescript
interface NewFeatureProps {
  data: Data;
  onAction: () => void;
}

export function NewFeature({ data, onAction }: NewFeatureProps) {
  return (
    <div>
      {/* Component implementation */}
    </div>
  );
}
```

**2. Add to Page** (`frontend/app/page/page.tsx`):
```typescript
import { NewFeature } from '@/components/features/NewFeature';

export default function Page() {
  return <NewFeature data={data} onAction={handleAction} />;
}
```

**3. Add Tests** (`frontend/components/__tests__/NewFeature.test.tsx`):
```typescript
describe('NewFeature', () => {
  it('renders correctly', () => {
    render(<NewFeature data={mockData} onAction={jest.fn()} />);
    // Assertions
  });
});
```

---

## Debugging

### Backend Debugging

**VS Code Launch Configuration** (`.vscode/launch.json`):
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "main:app",
        "--reload"
      ],
      "jinja": true,
      "cwd": "${workspaceFolder}/backend"
    }
  ]
}
```

**Logging:**
```python
import logging

logger = logging.getLogger(__name__)

# Debug
logger.debug(f"Processing exercise: {exercise_id}")

# Info
logger.info(f"User {user_id} completed exercise")

# Warning
logger.warning(f"Unusual behavior detected: {details}")

# Error
logger.error(f"Failed to process: {error}", exc_info=True)
```

### Frontend Debugging

**Chrome DevTools:**
- F12 → Sources → Set breakpoints
- Console → View logs and errors
- Network → Inspect API calls
- Redux DevTools → View state changes

**React DevTools:**
- Install React DevTools extension
- Inspect component tree
- View props and state
- Profile performance

**Debugging Tips:**
```typescript
// Console debugging
console.log('Variable:', variable);
console.table(arrayOfObjects);
console.trace(); // Stack trace

// Debugger statement
function processData(data: any) {
  debugger; // Pauses execution here
  // ... code
}
```

---

## Useful Commands

### Backend

```bash
# Start server
uvicorn main:app --reload

# Run tests
pytest

# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Format code
black backend/

# Lint code
flake8 backend/

# Type check
mypy backend/
```

### Frontend

```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run tests
npm test

# Lint
npm run lint

# Format
npm run format

# Type check
npm run type-check
```

---

## Next Steps

- Review [Integration Guide](./INTEGRATION_GUIDE.md)
- Check [API Documentation](./API_DOCUMENTATION.md)
- Read [Testing Strategy](./TESTING_STRATEGY.md)
- See [Deployment Guide](./backend-deployment.md)

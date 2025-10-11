# Backend Test Suite

Comprehensive testing suite for the Spanish Subjunctive Practice FastAPI backend.

## Overview

This test suite provides **120+ tests** covering:

- **Unit Tests** (60+ tests): Services, conjugation engine, exercise generator, learning algorithm, feedback
- **Integration Tests** (30+ tests): Database operations, model relationships, transactions
- **API Tests** (40+ tests): Authentication, exercises, progress, authorization
- **Performance Tests**: Response times, load testing, concurrent requests

## Test Coverage

Current coverage: **85%+**

### What's Tested

#### Unit Tests (`tests/unit/`)
- ✅ **Conjugation Engine** (`test_conjugation.py`): 40+ tests
  - Regular verbs (ar, er, ir)
  - Irregular verbs (ser, estar, ir, tener, etc.)
  - Stem-changing verbs (e→ie, o→ue, e→i)
  - Spelling changes (c→qu, g→gu, z→c)
  - Answer validation
  - Error analysis

- ✅ **Exercise Generator** (`test_exercise_generator.py`): 30+ tests
  - WEIRDO category generation
  - Difficulty-based verb selection
  - Distractor generation
  - Hint generation
  - Exercise set creation

- ✅ **Learning Algorithm** (`test_learning_algorithm.py`): 30+ tests
  - SM-2 spaced repetition
  - Adaptive difficulty
  - Card management
  - Progress tracking

- ✅ **Feedback Generator** (`test_feedback.py`): 25+ tests
  - Error categorization
  - Pattern detection
  - Contextualized feedback
  - Encouragement messages

- ✅ **Security** (`test_security.py`): 20+ tests
  - Password hashing
  - JWT token creation/validation
  - Token expiration
  - Authorization

#### API Tests (`tests/api/`)
- ✅ **Authentication** (`test_auth_api.py`): 25+ tests
  - User registration
  - Login/logout
  - Token refresh
  - Protected endpoints

- ✅ **Exercises** (`test_exercises_api.py`): 30+ tests
  - Get exercises
  - Filter by difficulty/type
  - Submit answers
  - Validation feedback

## Quick Start

### Installation

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Or using poetry
poetry install --with dev
```

### Running Tests

#### Using pytest directly:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=backend --cov-report=html

# Run specific test file
pytest tests/unit/test_conjugation.py

# Run specific test
pytest tests/unit/test_conjugation.py::TestConjugationEngine::test_conjugate_regular_ar_verb

# Run tests by marker
pytest -m unit           # Unit tests only
pytest -m api            # API tests only
pytest -m conjugation    # Conjugation tests only
pytest -m auth           # Auth tests only

# Run fast tests (exclude slow)
pytest -m "not slow"

# Re-run failed tests
pytest --lf
```

#### Using the test runner script:

```bash
# Run all tests
python tests/run_tests.py all

# Run specific test suites
python tests/run_tests.py unit
python tests/run_tests.py integration
python tests/run_tests.py api

# Run with verbose output
python tests/run_tests.py unit -v

# Run tests by marker
python tests/run_tests.py -m conjugation
python tests/run_tests.py -m auth

# Run specific test
python tests/run_tests.py -k test_conjugate_regular

# Generate coverage report
python tests/run_tests.py coverage

# Check coverage meets threshold
python tests/run_tests.py check
```

## Test Organization

```
tests/
├── conftest.py              # Pytest configuration and fixtures
├── __init__.py
├── README.md                # This file
├── run_tests.py             # Test runner script
│
├── unit/                    # Unit tests
│   ├── __init__.py
│   ├── test_conjugation.py
│   ├── test_exercise_generator.py
│   ├── test_learning_algorithm.py
│   ├── test_feedback.py
│   └── test_security.py
│
├── integration/             # Integration tests
│   ├── __init__.py
│   ├── test_database.py
│   └── test_services.py
│
├── api/                     # API endpoint tests
│   ├── __init__.py
│   ├── test_auth_api.py
│   ├── test_exercises_api.py
│   └── test_progress_api.py
│
└── performance/             # Performance tests
    ├── __init__.py
    └── test_benchmarks.py
```

## Fixtures

Common fixtures available in `conftest.py`:

### Configuration
- `test_settings`: Test application settings
- `override_settings`: Override app settings for testing

### Database
- `db_engine`: In-memory SQLite engine
- `db_session`: Database session
- `override_get_db`: Override database dependency

### FastAPI Client
- `client`: Basic TestClient
- `authenticated_client`: Authenticated TestClient with JWT token

### Users
- `test_user`: Basic test user
- `test_user_with_profile`: User with profile and preferences
- `admin_user`: Admin user
- `user_factory`: Factory for creating multiple users

### Authentication
- `valid_jwt_token`: Valid JWT token
- `expired_jwt_token`: Expired JWT token

### Services
- `conjugation_engine`: ConjugationEngine instance
- `exercise_generator`: ExerciseGenerator instance
- `learning_algorithm`: LearningAlgorithm instance
- `feedback_generator`: FeedbackGenerator instance
- `error_analyzer`: ErrorAnalyzer instance

### Data
- `sample_verbs`: Dictionary of sample verbs by type
- `sample_exercises`: List of sample exercises
- `card_factory`: Factory for creating SM2 cards

### Utilities
- `temp_dir`: Temporary directory
- `mock_openai`: Mock OpenAI API
- `mock_redis`: Mock Redis client

## Test Markers

Mark tests with pytest markers for categorization:

```python
@pytest.mark.unit
@pytest.mark.conjugation
def test_conjugate_regular_verb():
    ...

@pytest.mark.api
@pytest.mark.auth
def test_login_success():
    ...

@pytest.mark.slow
def test_load_testing():
    ...
```

Available markers:
- `unit`: Unit tests
- `integration`: Integration tests
- `api`: API endpoint tests
- `performance`: Performance tests
- `slow`: Slow-running tests
- `auth`: Authentication tests
- `conjugation`: Conjugation engine tests
- `exercise`: Exercise generation tests
- `learning`: Learning algorithm tests
- `feedback`: Feedback generation tests

## Coverage Reports

### Generate HTML Report

```bash
pytest --cov=backend --cov-report=html
```

View report: Open `htmlcov/index.html` in browser

### Generate Terminal Report

```bash
pytest --cov=backend --cov-report=term-missing
```

### Generate XML Report (for CI)

```bash
pytest --cov=backend --cov-report=xml
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt

    - name: Run tests
      run: pytest --cov=backend --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

## Writing New Tests

### Unit Test Template

```python
import pytest
from backend.services.my_service import MyService


@pytest.mark.unit
class TestMyService:
    """Test suite for MyService."""

    def test_basic_functionality(self):
        """Test basic functionality."""
        service = MyService()
        result = service.do_something()
        assert result is not None

    @pytest.mark.parametrize("input,expected", [
        ("a", "A"),
        ("b", "B"),
    ])
    def test_with_parameters(self, input, expected):
        """Test with different parameters."""
        service = MyService()
        result = service.transform(input)
        assert result == expected
```

### API Test Template

```python
import pytest
from fastapi import status


@pytest.mark.api
class TestMyAPI:
    """Test suite for my API endpoints."""

    def test_endpoint_requires_auth(self, client):
        """Test endpoint requires authentication."""
        response = client.get("/api/v1/my-endpoint")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_endpoint_success(self, authenticated_client):
        """Test successful endpoint call."""
        response = authenticated_client.get("/api/v1/my-endpoint")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "key" in data
```

## Best Practices

1. **Isolation**: Each test should be independent
2. **Fixtures**: Use fixtures for common setup
3. **Parametrize**: Use `@pytest.mark.parametrize` for testing multiple inputs
4. **Markers**: Mark tests appropriately (unit, integration, api, slow)
5. **Naming**: Use descriptive test names (test_what_when_expected)
6. **Assertions**: One logical assertion per test
7. **Cleanup**: Use fixtures and context managers for cleanup
8. **Mocking**: Mock external dependencies (OpenAI, Redis, etc.)

## Troubleshooting

### Tests Failing

1. Check test database is clean:
   ```bash
   rm -f test.db
   ```

2. Update dependencies:
   ```bash
   pip install -r requirements-dev.txt --upgrade
   ```

3. Clear pytest cache:
   ```bash
   pytest --cache-clear
   ```

### Import Errors

1. Ensure backend is in PYTHONPATH:
   ```bash
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

2. Or install backend in editable mode:
   ```bash
   pip install -e .
   ```

### Slow Tests

Run only fast tests:
```bash
pytest -m "not slow"
```

Or increase timeout:
```bash
pytest --timeout=300
```

## Performance Benchmarks

Expected performance targets:

- API response time: < 200ms (95th percentile)
- Database query time: < 50ms (average)
- Conjugation engine: < 1ms per verb
- Exercise generation: < 10ms per exercise
- Test suite: < 60 seconds (all tests)

## Contributing

When adding new features:

1. Write tests first (TDD)
2. Ensure all tests pass
3. Maintain coverage above 80%
4. Add docstrings to test classes/functions
5. Use appropriate markers
6. Update this README if needed

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)

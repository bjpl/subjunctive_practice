# ADR-004: Testing Strategy

**Status:** Accepted
**Date:** 2024-Q4
**Decision Makers:** Full Development Team
**Last Updated:** October 2, 2025

---

## Context

The Spanish Subjunctive Practice application spans multiple platforms (desktop PyQt, web React/FastAPI) with complex business logic, AI integration, and real-time features. A comprehensive testing strategy is required to:

- Ensure correctness across all platforms
- Prevent regressions during refactoring
- Enable confident deployments
- Support Test-Driven Development (TDD)
- Validate AI-generated content
- Test accessibility compliance

### Testing Challenges

1. **Multi-Platform:** Desktop and web have different testing requirements
2. **Async Code:** FastAPI and OpenAI integration use async/await
3. **AI Integration:** OpenAI responses are non-deterministic
4. **UI Testing:** PyQt and React require different testing approaches
5. **Database:** Test isolation and fixtures needed
6. **Real-time Features:** WebSockets and live updates

---

## Decision

**We will implement a multi-layered testing strategy using pytest as the core framework, with platform-specific tools for UI testing, and comprehensive coverage targets for critical paths.**

### Testing Pyramid

```mermaid
graph TB
    subgraph "Testing Levels"
        E2E["End-to-End Tests<br/>10% of tests<br/>Critical user flows"]
        Integration["Integration Tests<br/>25% of tests<br/>API + DB + Services"]
        Unit["Unit Tests<br/>65% of tests<br/>Business logic + Utils"]
    end

    E2E --> Integration
    Integration --> Unit

    style E2E fill:#FFB6C1
    style Integration fill:#FFD700
    style Unit fill:#90EE90
```

---

## Testing Stack

### Core Framework

```python
# requirements-test.txt
pytest==7.4.3                # Core testing framework
pytest-asyncio==0.21.1       # Async test support
pytest-mock==3.12.0          # Mocking utilities
pytest-cov==4.1.0            # Coverage reporting
pytest-xdist==3.5.0          # Parallel test execution
```

### Backend Testing

```python
httpx==0.25.2                # Async HTTP client for API tests
faker==20.1.0                # Test data generation
factory-boy==3.3.0           # Model factories
freezegun==1.4.0             # Time mocking
```

### Frontend Testing (Web)

```javascript
// package.json
{
  "devDependencies": {
    "@testing-library/react": "^14.0.0",
    "@testing-library/jest-dom": "^6.1.5",
    "@testing-library/user-event": "^14.5.1",
    "vitest": "^1.0.4",
    "playwright": "^1.40.0"
  }
}
```

### Desktop Testing (PyQt)

```python
pytest-qt==4.2.0             # PyQt testing utilities
pytest-xvfb==3.0.0           # Headless display for CI
```

---

## Testing Architecture

### Directory Structure

```
tests/
├── backend/
│   ├── unit/
│   │   ├── test_conjugation_engine.py
│   │   ├── test_srs_algorithm.py
│   │   └── test_tblt_service.py
│   ├── integration/
│   │   ├── test_auth_flow.py
│   │   ├── test_exercise_api.py
│   │   └── test_openai_integration.py
│   └── e2e/
│       └── test_complete_session.py
├── desktop/
│   ├── unit/
│   │   ├── test_ui_components.py
│   │   └── test_session_manager.py
│   └── integration/
│       └── test_full_workflow.py
├── frontend/
│   ├── unit/
│   │   └── components/
│   ├── integration/
│   └── e2e/
│       └── playwright/
├── shared/
│   └── test_business_logic.py
├── fixtures/
│   ├── db_fixtures.py
│   ├── user_fixtures.py
│   └── exercise_fixtures.py
├── reports/
│   ├── coverage/
│   └── html/
└── conftest.py              # Shared pytest configuration
```

---

## Testing Strategies by Layer

### 1. Unit Tests (65% of tests)

**Goal:** Test individual functions and classes in isolation

**Backend Example:**

```python
# tests/backend/unit/test_srs_algorithm.py
import pytest
from datetime import datetime, timedelta
from backend.services.spaced_repetition import SRSService

class TestSRSAlgorithm:
    """Test spaced repetition system algorithm."""

    def test_initial_interval_calculation(self):
        """Test first review interval is 1 day."""
        srs = SRSService()
        interval = srs.calculate_next_interval(
            quality=5,  # Perfect recall
            previous_interval=0,
            repetitions=0
        )
        assert interval == timedelta(days=1)

    def test_interval_increases_on_success(self):
        """Test interval increases with successful reviews."""
        srs = SRSService()

        # First review (perfect)
        interval1 = srs.calculate_next_interval(5, 0, 0)

        # Second review (perfect)
        interval2 = srs.calculate_next_interval(5, interval1.days, 1)

        # Third review (perfect)
        interval3 = srs.calculate_next_interval(5, interval2.days, 2)

        assert interval1.days < interval2.days < interval3.days

    def test_interval_resets_on_failure(self):
        """Test interval resets on failed recall."""
        srs = SRSService()

        # Build up interval
        interval = srs.calculate_next_interval(5, 0, 0)
        interval = srs.calculate_next_interval(5, interval.days, 1)

        # Fail recall
        reset_interval = srs.calculate_next_interval(0, interval.days, 2)

        assert reset_interval == timedelta(days=1)
```

**Desktop Unit Test:**

```python
# tests/desktop/unit/test_ui_components.py
import pytest
from PyQt6.QtWidgets import QApplication
from src.ui_system.widgets.exercise_widget import ExerciseWidget

@pytest.fixture(scope="session")
def qapp():
    """Create QApplication for PyQt tests."""
    app = QApplication([])
    yield app
    app.quit()

def test_exercise_widget_displays_question(qapp):
    """Test exercise widget displays question text."""
    widget = ExerciseWidget()
    widget.set_exercise("Complete: Espero que tú _____ (hablar) español.")

    assert "Espero que tú" in widget.question_label.text()
    assert "hablar" in widget.question_label.text()

def test_exercise_widget_validates_answer(qapp):
    """Test answer validation logic."""
    widget = ExerciseWidget()
    widget.set_exercise("Espero que tú _____ (hablar).")

    # Correct answer
    result = widget.validate_answer("hables")
    assert result.is_correct is True

    # Incorrect answer
    result = widget.validate_answer("hablas")
    assert result.is_correct is False
```

---

### 2. Integration Tests (25% of tests)

**Goal:** Test interactions between components

**Backend API Integration:**

```python
# tests/backend/integration/test_exercise_api.py
import pytest
from httpx import AsyncClient
from backend.main import app
from backend.core.database import get_db
from tests.fixtures.user_fixtures import create_test_user

@pytest.mark.asyncio
async def test_create_and_retrieve_exercise(test_db):
    """Test exercise creation and retrieval flow."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create user and login
        user = await create_test_user(test_db, email="test@example.com")
        login_response = await client.post(
            "/api/auth/login",
            json={"email": "test@example.com", "password": "password123"}
        )
        token = login_response.json()["access_token"]

        # Create exercise
        create_response = await client.post(
            "/api/exercises",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "verb": "hablar",
                "tense": "present_subjunctive",
                "difficulty": "intermediate"
            }
        )
        assert create_response.status_code == 201
        exercise_id = create_response.json()["id"]

        # Retrieve exercise
        get_response = await client.get(
            f"/api/exercises/{exercise_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert get_response.status_code == 200
        exercise = get_response.json()
        assert exercise["verb"] == "hablar"
        assert exercise["tense"] == "present_subjunctive"
```

**OpenAI Integration Test:**

```python
# tests/backend/integration/test_openai_integration.py
import pytest
from backend.services.openai_service import OpenAIService

@pytest.mark.asyncio
async def test_openai_generates_contextual_scenario(mocker):
    """Test OpenAI generates appropriate TBLT scenario."""
    # Mock OpenAI API response
    mock_response = {
        "choices": [{
            "message": {
                "content": "En un restaurante, el mesero sugiere: 'Recomiendo que usted pruebe la paella.'"
            }
        }]
    }
    mocker.patch("openai.ChatCompletion.acreate", return_value=mock_response)

    service = OpenAIService()
    scenario = await service.generate_tblt_scenario(
        verb="probar",
        tense="present_subjunctive",
        context="restaurant"
    )

    assert "pruebe" in scenario.text.lower()
    assert "restaurant" in scenario.context.lower()
```

---

### 3. End-to-End Tests (10% of tests)

**Goal:** Test complete user workflows

**Web E2E Test (Playwright):**

```javascript
// tests/frontend/e2e/complete-session.spec.js
import { test, expect } from '@playwright/test';

test('complete exercise session', async ({ page }) => {
  // Navigate to app
  await page.goto('http://localhost:3000');

  // Login
  await page.fill('input[name="email"]', 'test@example.com');
  await page.fill('input[name="password"]', 'password123');
  await page.click('button[type="submit"]');

  // Wait for dashboard
  await expect(page.locator('h1')).toContainText('Dashboard');

  // Start exercise session
  await page.click('text=Start Practice');

  // Complete first exercise
  await expect(page.locator('.exercise-question')).toBeVisible();
  await page.fill('input[name="answer"]', 'hable');
  await page.click('button:has-text("Submit")');

  // Verify feedback
  await expect(page.locator('.feedback')).toContainText('Correct!');

  // Continue session
  await page.click('button:has-text("Next")');

  // Verify progress updated
  const progressText = await page.locator('.progress-counter').textContent();
  expect(progressText).toContain('1 / 10');
});
```

**Desktop E2E Test:**

```python
# tests/desktop/e2e/test_complete_workflow.py
import pytest
from pytestqt.qtbot import QtBot
from src.main import MainWindow

def test_complete_exercise_workflow(qtbot):
    """Test user can complete full exercise workflow."""
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()

    # Login
    window.login_widget.email_input.setText("test@example.com")
    window.login_widget.password_input.setText("password123")
    qtbot.mouseClick(window.login_widget.login_button, Qt.LeftButton)

    # Wait for dashboard
    qtbot.waitUntil(lambda: window.dashboard.isVisible(), timeout=2000)

    # Start practice session
    qtbot.mouseClick(window.dashboard.start_button, Qt.LeftButton)

    # Answer exercise
    qtbot.waitUntil(lambda: window.exercise_widget.isVisible())
    window.exercise_widget.answer_input.setText("hable")
    qtbot.mouseClick(window.exercise_widget.submit_button, Qt.LeftButton)

    # Verify feedback
    qtbot.waitUntil(lambda: "Correct" in window.exercise_widget.feedback_label.text())
```

---

## Special Testing Scenarios

### 1. AI/OpenAI Testing

**Strategy:** Use mocks for unit tests, real API calls for integration tests (rate-limited)

```python
# tests/backend/unit/test_openai_service.py
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_openai_handles_api_errors(mocker):
    """Test graceful handling of OpenAI API errors."""
    # Mock API to raise error
    mock_openai = mocker.patch("openai.ChatCompletion.acreate")
    mock_openai.side_effect = Exception("API rate limit exceeded")

    service = OpenAIService()

    with pytest.raises(Exception) as exc_info:
        await service.generate_feedback("Test input")

    assert "rate limit" in str(exc_info.value).lower()

# tests/backend/integration/test_openai_real.py
@pytest.mark.slow  # Mark as slow test
@pytest.mark.asyncio
async def test_openai_real_api_call():
    """Test actual OpenAI API call (rate-limited in CI)."""
    service = OpenAIService()
    response = await service.generate_feedback(
        "User wrote 'hablas' instead of 'hables'"
    )

    # Verify response structure
    assert len(response) > 0
    assert "subjunctive" in response.lower() or "subjuntivo" in response.lower()
```

### 2. Database Testing

**Strategy:** Use test database with transactions rolled back after each test

```python
# tests/conftest.py
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from backend.core.database import Base

@pytest.fixture(scope="function")
async def test_db():
    """Create test database session."""
    # Create test engine
    engine = create_async_engine("postgresql+asyncpg://test:test@localhost/test_db")

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create session
    async with AsyncSession(engine) as session:
        yield session
        await session.rollback()

    # Drop all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
```

### 3. Accessibility Testing

```python
# tests/desktop/test_accessibility.py
import pytest
from src.ui_system.accessibility.wcag_validator import WCAGValidator

def test_color_contrast_compliance():
    """Test all UI colors meet WCAG AA contrast requirements."""
    validator = WCAGValidator()

    # Test combinations
    results = validator.validate_all_color_combinations()

    failures = [r for r in results if not r.passes_wcag_aa]
    assert len(failures) == 0, f"WCAG failures: {failures}"

def test_keyboard_navigation():
    """Test all interactive elements are keyboard-accessible."""
    # Implementation
    pass
```

---

## Coverage Targets

### Overall Targets

| Component | Coverage Target | Current | Priority |
|-----------|----------------|---------|----------|
| **Backend Services** | 90% | TBD | Critical |
| **Backend API Routes** | 85% | TBD | Critical |
| **Desktop Core Logic** | 85% | TBD | High |
| **Desktop UI Components** | 70% | TBD | Medium |
| **Web Frontend Components** | 80% | TBD | High |
| **Shared Business Logic** | 95% | TBD | Critical |

### Measuring Coverage

```bash
# Backend coverage
pytest --cov=backend --cov-report=html --cov-report=term tests/backend/

# Desktop coverage
pytest --cov=src --cov-report=html --cov-report=term tests/desktop/

# Generate combined report
coverage combine
coverage html
```

---

## CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r backend/requirements.txt
          pip install -r requirements-test.txt
      - name: Run tests
        run: pytest tests/backend/ --cov --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: npm ci
      - name: Run tests
        run: npm test
      - name: Run E2E tests
        run: npx playwright test

  desktop-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y xvfb
          pip install -r requirements.txt
          pip install -r requirements-test.txt
      - name: Run tests
        run: xvfb-run pytest tests/desktop/ --cov
```

---

## Consequences

### Positive

1. **Confidence:** High test coverage enables fearless refactoring
2. **Quality:** Catch bugs before production
3. **Documentation:** Tests serve as usage examples
4. **Regression Prevention:** Automated testing prevents old bugs from returning
5. **Faster Development:** TDD improves design and reduces debugging time

### Negative

1. **Maintenance:** Tests require updates when requirements change
2. **Time Investment:** Writing tests takes time upfront
3. **False Positives:** Flaky tests can reduce trust in CI/CD
4. **Complexity:** Testing async, UI, and AI adds complexity

### Mitigation

- **Test Maintenance:** Refactor tests alongside production code
- **Fast Feedback:** Parallelize tests, use caching
- **Flaky Tests:** Quarantine and fix immediately
- **Complexity:** Invest in testing utilities and fixtures

---

## Related Decisions

- **ADR-001:** Dual Platform Strategy (tests must cover both)
- **ADR-002:** PyQt5/PyQt6 Compatibility (test both versions)
- **ADR-003:** FastAPI Backend (async testing required)

---

## References

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [Playwright Documentation](https://playwright.dev/)
- [React Testing Library](https://testing-library.com/react)

---

**Document History**
- **2024-Q4:** Testing strategy established
- **October 2, 2025:** Documented in ADR format
- **Next Review:** Quarterly or when coverage falls below targets

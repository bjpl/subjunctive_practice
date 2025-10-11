# Test Writing Guide

## Overview

This guide provides comprehensive patterns, best practices, and examples for writing effective tests in the Spanish Subjunctive Practice application. It covers unit tests, integration tests, E2E tests, and accessibility testing.

## Table of Contents

- [General Principles](#general-principles)
- [Backend Testing (pytest)](#backend-testing-pytest)
- [Frontend Testing (Jest)](#frontend-testing-jest)
- [E2E Testing (Playwright)](#e2e-testing-playwright)
- [Accessibility Testing](#accessibility-testing)
- [Test Data Management](#test-data-management)
- [Mocking Strategies](#mocking-strategies)
- [Best Practices](#best-practices)

## General Principles

### AAA Pattern (Arrange-Act-Assert)

```python
def test_conjugation_regular_verb():
    # Arrange - Set up test data
    engine = ConjugationEngine()
    verb = "hablar"
    tense = "present_subjunctive"
    person = "yo"

    # Act - Execute the function
    result = engine.conjugate(verb, tense, person)

    # Assert - Verify the outcome
    assert result.conjugation == "hable"
    assert not result.is_irregular
```

### GIVEN-WHEN-THEN Pattern

```python
def test_user_receives_xp_for_correct_answer():
    # GIVEN a user with 0 XP
    user = create_test_user(xp=0)
    exercise = create_test_exercise()

    # WHEN they submit a correct answer
    response = submit_answer(user.id, exercise.id, correct_answer=True)

    # THEN they receive 100 XP
    assert response.xp_earned == 100
    assert user.total_xp == 100
```

### Test Naming Conventions

**Good Test Names:**
```python
# Backend (pytest)
def test_regular_ar_verb_present_subjunctive_yo_form()
def test_invalid_verb_raises_value_error()
def test_api_returns_401_for_unauthorized_user()

# Frontend (Jest)
test('renders practice session with exercise data', () => {})
test('displays error message when API call fails', () => {})
test('submits answer and shows feedback on button click', () => {})
```

**Bad Test Names:**
```python
def test_1()  # Too vague
def test_conjugation()  # Not specific enough
def test_stuff_works()  # Unclear what's being tested
```

## Backend Testing (pytest)

### Unit Test Pattern

```python
# tests/test_conjugation_engine.py
import pytest
from backend.services.conjugation import ConjugationEngine

class TestConjugationEngine:
    """Test suite for ConjugationEngine"""

    @pytest.fixture
    def engine(self):
        """Create a fresh engine instance for each test"""
        return ConjugationEngine()

    def test_regular_ar_verb_present(self, engine):
        """Test regular -ar verb conjugation in present subjunctive"""
        # Arrange
        verb = "hablar"
        tense = "present_subjunctive"
        person = "yo"

        # Act
        result = engine.conjugate(verb, tense, person)

        # Assert
        assert result.conjugation == "hable"
        assert result.verb_type == "-ar"
        assert not result.is_irregular
        assert not result.is_stem_changing

    @pytest.mark.parametrize("verb,person,expected", [
        ("hablar", "yo", "hable"),
        ("hablar", "tú", "hables"),
        ("hablar", "él/ella/usted", "hable"),
        ("hablar", "nosotros/nosotras", "hablemos"),
        ("hablar", "vosotros/vosotras", "habléis"),
        ("hablar", "ellos/ellas/ustedes", "hablen"),
    ])
    def test_hablar_all_persons(self, engine, verb, person, expected):
        """Test all persons for hablar in present subjunctive"""
        result = engine.conjugate(verb, "present_subjunctive", person)
        assert result.conjugation == expected

    def test_invalid_verb_raises_error(self, engine):
        """Test that invalid verb raises appropriate error"""
        with pytest.raises(ValueError, match="Unknown verb"):
            engine.conjugate("invalidverb", "present_subjunctive", "yo")

    @pytest.mark.spanish_logic
    def test_stem_changing_verb_pattern(self, engine):
        """Test e→ie stem change is detected and applied correctly"""
        result = engine.conjugate("querer", "present_subjunctive", "yo")

        assert result.conjugation == "quiera"
        assert result.is_stem_changing
        assert result.stem_change_pattern == "e→ie"
        assert "stem change" in result.explanation.lower()
```

### API Integration Test Pattern

```python
# tests/test_api_endpoints.py
import pytest
from httpx import AsyncClient
from backend.main import app

@pytest.mark.asyncio
class TestExerciseAPI:
    """Test exercise API endpoints"""

    @pytest.fixture
    async def client(self):
        """Create async test client"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            yield client

    @pytest.fixture
    async def authenticated_client(self, client):
        """Create authenticated test client"""
        # Register and login test user
        await client.post("/api/auth/register", json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "SecurePass123!"
        })

        response = await client.post("/api/auth/login", json={
            "username": "testuser",
            "password": "SecurePass123!"
        })

        token = response.json()["access_token"]
        client.headers["Authorization"] = f"Bearer {token}"
        return client

    async def test_get_exercises_requires_auth(self, client):
        """Test that exercises endpoint requires authentication"""
        response = await client.get("/api/exercises")

        assert response.status_code == 401
        assert "not authenticated" in response.json()["detail"].lower()

    async def test_get_exercises_returns_list(self, authenticated_client):
        """Test getting exercises returns proper structure"""
        response = await authenticated_client.get("/api/exercises")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["exercises"], list)
        assert "total" in data
        assert "page" in data

    @pytest.mark.parametrize("difficulty,expected_count", [
        (1, 10),
        (3, 15),
        (5, 8),
    ])
    async def test_filter_by_difficulty(
        self, authenticated_client, difficulty, expected_count
    ):
        """Test filtering exercises by difficulty level"""
        response = await authenticated_client.get(
            f"/api/exercises?difficulty={difficulty}"
        )

        assert response.status_code == 200
        exercises = response.json()["exercises"]
        assert all(ex["difficulty"] == difficulty for ex in exercises)

    async def test_submit_answer_correct(self, authenticated_client):
        """Test submitting a correct answer"""
        # Get an exercise first
        response = await authenticated_client.get("/api/exercises")
        exercise = response.json()["exercises"][0]

        # Submit correct answer
        response = await authenticated_client.post(
            "/api/exercises/submit",
            json={
                "exercise_id": exercise["id"],
                "answer": exercise["correct_answer"],
            }
        )

        assert response.status_code == 200
        result = response.json()
        assert result["is_correct"] is True
        assert result["xp_earned"] > 0
        assert "explanation" in result
```

### Database Test Pattern

```python
# tests/test_database.py
import pytest
from sqlalchemy.orm import Session
from backend.models import User, Exercise, Progress
from backend.core.database import get_db

@pytest.fixture
def db_session():
    """Create a test database session"""
    # Use in-memory SQLite for tests
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from backend.models.base import Base

    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    yield session

    session.close()

def test_create_user(db_session):
    """Test creating a user in database"""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_pass"
    )

    db_session.add(user)
    db_session.commit()

    retrieved = db_session.query(User).filter_by(
        username="testuser"
    ).first()

    assert retrieved is not None
    assert retrieved.email == "test@example.com"

def test_user_progress_relationship(db_session):
    """Test user-progress relationship"""
    user = User(email="test@example.com", username="test")
    exercise = Exercise(
        verb="hablar",
        tense="present_subjunctive",
        person="yo"
    )

    db_session.add(user)
    db_session.add(exercise)
    db_session.commit()

    progress = Progress(
        user_id=user.id,
        exercise_id=exercise.id,
        is_correct=True,
        xp_earned=100
    )

    db_session.add(progress)
    db_session.commit()

    assert len(user.progress) == 1
    assert user.progress[0].xp_earned == 100
```

### Performance Test Pattern

```python
# tests/test_performance.py
import pytest
import time

@pytest.mark.performance
class TestPerformance:
    """Performance benchmark tests"""

    def test_conjugation_speed(self, benchmark):
        """Test conjugation engine performance"""
        engine = ConjugationEngine()

        def conjugate():
            return engine.conjugate("hablar", "present_subjunctive", "yo")

        # Benchmark should complete in < 10ms
        result = benchmark(conjugate)
        assert result.conjugation == "hable"

    def test_exercise_generation_speed(self, benchmark):
        """Test exercise generation performance"""
        generator = ExerciseGenerator()

        def generate():
            return generator.generate_exercise(
                difficulty=3,
                exercise_type="fill_in_blank"
            )

        # Should generate exercise in < 100ms
        result = benchmark(generate)
        assert result is not None

    @pytest.mark.slow
    def test_bulk_conjugation_performance(self):
        """Test bulk conjugation performance"""
        engine = ConjugationEngine()
        verbs = ["hablar", "comer", "vivir"] * 100

        start = time.time()

        for verb in verbs:
            engine.conjugate(verb, "present_subjunctive", "yo")

        duration = time.time() - start

        # Should process 300 conjugations in < 1 second
        assert duration < 1.0
```

## Frontend Testing (Jest)

### Component Test Pattern

```typescript
// components/PracticeSession.test.tsx
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { PracticeSession } from './PracticeSession'

describe('PracticeSession', () => {
  it('renders practice session with exercise', () => {
    // Arrange
    const mockExercise = {
      id: '1',
      verb: 'hablar',
      sentence: 'Quiero que tú ___ español.',
      correct_answer: 'hables',
    }

    // Act
    render(<PracticeSession exercise={mockExercise} />)

    // Assert
    expect(screen.getByText(/Quiero que tú/)).toBeInTheDocument()
    expect(screen.getByRole('textbox')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /submit/i })).toBeInTheDocument()
  })

  it('handles answer submission', async () => {
    const user = userEvent.setup()
    const mockSubmit = jest.fn()
    const mockExercise = {
      id: '1',
      sentence: 'Quiero que tú ___ español.',
    }

    render(
      <PracticeSession
        exercise={mockExercise}
        onSubmit={mockSubmit}
      />
    )

    // Type answer
    const input = screen.getByRole('textbox')
    await user.type(input, 'hables')

    // Submit
    const submitButton = screen.getByRole('button', { name: /submit/i })
    await user.click(submitButton)

    // Verify
    expect(mockSubmit).toHaveBeenCalledWith('hables')
  })

  it('displays feedback after submission', async () => {
    const user = userEvent.setup()

    render(<PracticeSession exercise={mockExercise} />)

    await user.type(screen.getByRole('textbox'), 'hables')
    await user.click(screen.getByRole('button', { name: /submit/i }))

    await waitFor(() => {
      expect(screen.getByText(/correct/i)).toBeInTheDocument()
    })
  })
})
```

### Hook Test Pattern

```typescript
// hooks/useExercises.test.ts
import { renderHook, waitFor } from '@testing-library/react'
import { useExercises } from './useExercises'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

describe('useExercises', () => {
  const createWrapper = () => {
    const queryClient = new QueryClient({
      defaultOptions: {
        queries: { retry: false },
      },
    })

    return ({ children }: { children: React.ReactNode }) => (
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    )
  }

  it('fetches exercises on mount', async () => {
    const { result } = renderHook(() => useExercises(), {
      wrapper: createWrapper(),
    })

    expect(result.current.isLoading).toBe(true)

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false)
      expect(result.current.data).toBeDefined()
    })
  })

  it('filters exercises by difficulty', async () => {
    const { result } = renderHook(
      () => useExercises({ difficulty: 3 }),
      { wrapper: createWrapper() }
    )

    await waitFor(() => {
      expect(result.current.data?.every(ex => ex.difficulty === 3)).toBe(true)
    })
  })
})
```

### Redux Test Pattern

```typescript
// store/slices/practice.test.ts
import practiceReducer, {
  startPractice,
  submitAnswer,
  selectCurrentExercise,
} from './practiceSlice'

describe('practice slice', () => {
  const initialState = {
    exercises: [],
    currentIndex: 0,
    score: 0,
    isLoading: false,
  }

  it('should handle startPractice', () => {
    const exercises = [{ id: '1' }, { id: '2' }]
    const actual = practiceReducer(
      initialState,
      startPractice(exercises)
    )

    expect(actual.exercises).toEqual(exercises)
    expect(actual.currentIndex).toBe(0)
  })

  it('should handle submitAnswer with correct answer', () => {
    const state = {
      ...initialState,
      exercises: [{ id: '1', correct_answer: 'hables' }],
    }

    const actual = practiceReducer(
      state,
      submitAnswer({ answer: 'hables', isCorrect: true })
    )

    expect(actual.score).toBe(100)
    expect(actual.currentIndex).toBe(1)
  })

  it('should select current exercise', () => {
    const state = {
      practice: {
        exercises: [{ id: '1' }, { id: '2' }],
        currentIndex: 0,
      },
    }

    const result = selectCurrentExercise(state)
    expect(result).toEqual({ id: '1' })
  })
})
```

### Snapshot Testing

```typescript
// components/ExerciseCard.test.tsx
import { render } from '@testing-library/react'
import { ExerciseCard } from './ExerciseCard'

describe('ExerciseCard', () => {
  it('matches snapshot', () => {
    const exercise = {
      id: '1',
      verb: 'hablar',
      sentence: 'Quiero que tú ___ español.',
      difficulty: 3,
    }

    const { container } = render(<ExerciseCard exercise={exercise} />)
    expect(container).toMatchSnapshot()
  })

  it('matches snapshot with different difficulty', () => {
    const exercise = {
      id: '1',
      verb: 'ser',
      sentence: 'Es importante que ___ puntual.',
      difficulty: 5,
    }

    const { container } = render(<ExerciseCard exercise={exercise} />)
    expect(container).toMatchSnapshot()
  })
})
```

## E2E Testing (Playwright)

### Basic E2E Test Pattern

```typescript
// tests/e2e/practice-session.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Practice Session', () => {
  test.beforeEach(async ({ page }) => {
    // Login
    await page.goto('/auth/login')
    await page.fill('[name="username"]', 'testuser')
    await page.fill('[name="password"]', 'TestPass123!')
    await page.click('button[type="submit"]')

    // Navigate to practice
    await page.goto('/practice')
  })

  test('should complete full practice session', async ({ page }) => {
    // Wait for exercise to load
    await expect(page.locator('.exercise-sentence')).toBeVisible()

    // Fill in answer
    await page.fill('[data-testid="answer-input"]', 'hables')

    // Submit
    await page.click('button:has-text("Submit")')

    // Verify feedback
    await expect(page.locator('.feedback')).toContainText('Correct')

    // Verify XP increase
    const xpBefore = await page.locator('.xp-display').textContent()
    await page.click('button:has-text("Next")')
    const xpAfter = await page.locator('.xp-display').textContent()

    expect(parseInt(xpAfter!)).toBeGreaterThan(parseInt(xpBefore!))
  })

  test('should handle incorrect answer', async ({ page }) => {
    await page.fill('[data-testid="answer-input"]', 'hablo')
    await page.click('button:has-text("Submit")')

    // Verify error feedback
    await expect(page.locator('.feedback')).toContainText('Incorrect')

    // Verify explanation is shown
    await expect(page.locator('.explanation')).toBeVisible()

    // Verify hint button appears
    await expect(page.locator('button:has-text("Hint")')).toBeVisible()
  })
})
```

### Mobile E2E Test Pattern

```typescript
// tests/e2e/mobile.spec.ts
import { test, expect, devices } from '@playwright/test'

test.use({
  ...devices['iPhone 12'],
})

test.describe('Mobile Practice', () => {
  test('should be responsive on mobile', async ({ page }) => {
    await page.goto('/practice')

    // Check mobile layout
    const menu = page.locator('[data-testid="mobile-menu"]')
    await expect(menu).toBeVisible()

    // Verify touch interactions
    await page.tap('[data-testid="answer-input"]')
    await expect(page.locator('[data-testid="answer-input"]')).toBeFocused()

    // Check viewport
    const viewport = page.viewportSize()
    expect(viewport?.width).toBeLessThan(500)
  })

  test('should handle swipe gestures', async ({ page }) => {
    await page.goto('/practice')

    // Swipe to next exercise
    const exercise = page.locator('.exercise-card')
    const box = await exercise.boundingBox()

    await page.mouse.move(box!.x + box!.width / 2, box!.y + box!.height / 2)
    await page.mouse.down()
    await page.mouse.move(box!.x - 200, box!.y + box!.height / 2)
    await page.mouse.up()

    // Verify navigation
    await expect(page.locator('.next-exercise')).toBeVisible()
  })
})
```

### Visual Regression Test Pattern

```typescript
// tests/e2e/visual.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Visual Regression', () => {
  test('practice page matches baseline', async ({ page }) => {
    await page.goto('/practice')

    // Wait for content to load
    await page.waitForSelector('.exercise-card')

    // Take screenshot
    await expect(page).toHaveScreenshot('practice-page.png', {
      fullPage: true,
      maxDiffPixels: 100,
    })
  })

  test('dark mode matches baseline', async ({ page }) => {
    await page.goto('/practice')

    // Enable dark mode
    await page.click('[data-testid="theme-toggle"]')

    // Wait for transition
    await page.waitForTimeout(300)

    // Compare
    await expect(page).toHaveScreenshot('practice-dark-mode.png')
  })
})
```

## Accessibility Testing

### Automated Accessibility Tests

```typescript
// tests/accessibility/practice-session.a11y.test.tsx
import { render } from '@testing-library/react'
import { axe, toHaveNoViolations } from 'jest-axe'
import { PracticeSession } from '@/components/PracticeSession'

expect.extend(toHaveNoViolations)

describe('PracticeSession Accessibility', () => {
  it('should have no accessibility violations', async () => {
    const { container } = render(<PracticeSession exercise={mockExercise} />)
    const results = await axe(container)

    expect(results).toHaveNoViolations()
  })

  it('should have proper ARIA labels', () => {
    render(<PracticeSession exercise={mockExercise} />)

    expect(screen.getByRole('textbox')).toHaveAttribute(
      'aria-label',
      'Enter your answer'
    )
    expect(screen.getByRole('button', { name: /submit/i })).toHaveAttribute(
      'aria-label',
      'Submit answer'
    )
  })

  it('should have proper heading hierarchy', () => {
    render(<PracticeSession exercise={mockExercise} />)

    const headings = screen.getAllByRole('heading')

    // Should start with h1
    expect(headings[0].tagName).toBe('H1')

    // Should not skip levels
    const levels = headings.map(h => parseInt(h.tagName[1]))
    levels.forEach((level, i) => {
      if (i > 0) {
        expect(level - levels[i - 1]).toBeLessThanOrEqual(1)
      }
    })
  })
})
```

### Keyboard Navigation Tests

```typescript
// tests/e2e/keyboard-navigation.spec.ts
import { test, expect } from '@playwright/test'

test.describe('Keyboard Navigation', () => {
  test('should navigate with Tab key', async ({ page }) => {
    await page.goto('/practice')

    // Tab to input
    await page.keyboard.press('Tab')
    await expect(page.locator('[data-testid="answer-input"]')).toBeFocused()

    // Tab to submit button
    await page.keyboard.press('Tab')
    await expect(page.locator('button:has-text("Submit")')).toBeFocused()

    // Tab to hint button
    await page.keyboard.press('Tab')
    await expect(page.locator('button:has-text("Hint")')).toBeFocused()
  })

  test('should submit with Enter key', async ({ page }) => {
    await page.goto('/practice')

    await page.fill('[data-testid="answer-input"]', 'hables')
    await page.keyboard.press('Enter')

    // Verify submission
    await expect(page.locator('.feedback')).toBeVisible()
  })

  test('should have visible focus indicators', async ({ page }) => {
    await page.goto('/practice')

    await page.keyboard.press('Tab')

    const focused = page.locator(':focus')
    const outline = await focused.evaluate(el =>
      window.getComputedStyle(el).outline
    )

    // Should have visible outline
    expect(outline).not.toBe('none')
  })
})
```

### Color Contrast Tests

```typescript
// tests/accessibility/color-contrast.test.ts
import { render } from '@testing-library/react'
import { getContrast } from 'polished'

describe('Color Contrast', () => {
  it('should meet WCAG AA standards', () => {
    render(<PracticeSession exercise={mockExercise} />)

    const button = screen.getByRole('button', { name: /submit/i })
    const styles = window.getComputedStyle(button)

    const foreground = styles.color
    const background = styles.backgroundColor

    const contrast = getContrast(foreground, background)

    // WCAG AA requires 4.5:1 for normal text
    expect(contrast).toBeGreaterThanOrEqual(4.5)
  })

  it('should have sufficient contrast in dark mode', () => {
    render(
      <ThemeProvider theme="dark">
        <PracticeSession exercise={mockExercise} />
      </ThemeProvider>
    )

    // Test dark mode contrasts
    const text = screen.getByText(/quiero que/i)
    const styles = window.getComputedStyle(text)
    const contrast = getContrast(styles.color, styles.backgroundColor)

    expect(contrast).toBeGreaterThanOrEqual(4.5)
  })
})
```

## Test Data Management

### Using Fixtures

```python
# tests/conftest.py
import pytest
from backend.models import User, Exercise
from backend.services.conjugation import ConjugationEngine

@pytest.fixture
def sample_exercises():
    """Provide sample exercise data"""
    return [
        {
            "verb": "hablar",
            "tense": "present_subjunctive",
            "person": "yo",
            "correct_answer": "hable",
        },
        {
            "verb": "comer",
            "tense": "present_subjunctive",
            "person": "tú",
            "correct_answer": "comas",
        },
    ]

@pytest.fixture
def test_user(db_session):
    """Create a test user"""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_pass",
        xp=0,
        level=1,
    )
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def authenticated_headers(test_user):
    """Generate authentication headers"""
    from backend.core.security import create_access_token

    token = create_access_token({"sub": test_user.username})
    return {"Authorization": f"Bearer {token}"}
```

### Using Factories

```python
# tests/factories.py
import factory
from backend.models import User, Exercise, Progress

class UserFactory(factory.Factory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    username = factory.Sequence(lambda n: f"user{n}")
    hashed_password = "hashed_pass"
    xp = factory.Faker('random_int', min=0, max=10000)
    level = factory.LazyAttribute(lambda obj: obj.xp // 1000 + 1)

class ExerciseFactory(factory.Factory):
    class Meta:
        model = Exercise

    verb = factory.Faker('random_element', elements=[
        'hablar', 'comer', 'vivir', 'ser', 'estar'
    ])
    tense = "present_subjunctive"
    person = factory.Faker('random_element', elements=[
        'yo', 'tú', 'él/ella/usted'
    ])
    difficulty = factory.Faker('random_int', min=1, max=5)

# Usage
def test_with_factory():
    user = UserFactory()
    exercises = ExerciseFactory.build_batch(5)

    assert len(exercises) == 5
    assert user.level >= 1
```

## Mocking Strategies

### Mocking External APIs

```python
# tests/test_openai_integration.py
import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_openai():
    """Mock OpenAI API calls"""
    with patch('openai.ChatCompletion.create') as mock:
        mock.return_value = MagicMock(
            choices=[
                MagicMock(
                    message=MagicMock(
                        content="El subjuntivo se usa para expresar duda o deseo."
                    )
                )
            ]
        )
        yield mock

def test_ai_explanation_generation(mock_openai):
    """Test AI-powered explanation generation"""
    from backend.services.ai import generate_explanation

    explanation = generate_explanation("hablar", "present_subjunctive")

    assert "subjuntivo" in explanation.lower()
    mock_openai.assert_called_once()
```

### Mocking Frontend APIs

```typescript
// __mocks__/api.ts
export const mockExercisesAPI = {
  getExercises: jest.fn().mockResolvedValue({
    exercises: [
      { id: '1', verb: 'hablar', sentence: 'Test sentence' }
    ],
    total: 1,
  }),

  submitAnswer: jest.fn().mockResolvedValue({
    is_correct: true,
    xp_earned: 100,
    explanation: 'Good job!',
  }),
}

// Usage in tests
import { mockExercisesAPI } from '__mocks__/api'

test('fetches exercises on mount', async () => {
  render(<PracticeSession />)

  await waitFor(() => {
    expect(mockExercisesAPI.getExercises).toHaveBeenCalled()
  })
})
```

### MSW (Mock Service Worker) Pattern

```typescript
// mocks/handlers.ts
import { rest } from 'msw'

export const handlers = [
  rest.get('/api/exercises', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        exercises: [
          { id: '1', verb: 'hablar', difficulty: 3 }
        ],
        total: 1,
      })
    )
  }),

  rest.post('/api/exercises/submit', (req, res, ctx) => {
    const { answer } = req.body as { answer: string }

    return res(
      ctx.status(200),
      ctx.json({
        is_correct: answer === 'hables',
        xp_earned: answer === 'hables' ? 100 : 0,
      })
    )
  }),
]

// tests/setup.ts
import { setupServer } from 'msw/node'
import { handlers } from './mocks/handlers'

export const server = setupServer(...handlers)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

## Best Practices

### Test Independence

```python
# ✅ Good - Each test is independent
def test_conjugation_hablar():
    engine = ConjugationEngine()
    result = engine.conjugate("hablar", "present_subjunctive", "yo")
    assert result.conjugation == "hable"

def test_conjugation_comer():
    engine = ConjugationEngine()
    result = engine.conjugate("comer", "present_subjunctive", "yo")
    assert result.conjugation == "coma"

# ❌ Bad - Tests depend on each other
class TestConjugation:
    def test_setup(self):
        self.engine = ConjugationEngine()

    def test_hablar(self):
        # Fails if test_setup didn't run
        result = self.engine.conjugate("hablar", "present_subjunctive", "yo")
        assert result.conjugation == "hable"
```

### Descriptive Assertions

```python
# ✅ Good - Clear assertion messages
def test_irregular_verb_detection():
    result = engine.conjugate("ser", "present_subjunctive", "yo")

    assert result.is_irregular, (
        f"Expected 'ser' to be marked as irregular, "
        f"but is_irregular was {result.is_irregular}"
    )

# ❌ Bad - No context on failure
def test_irregular_verb_detection():
    result = engine.conjugate("ser", "present_subjunctive", "yo")
    assert result.is_irregular
```

### Test Organization

```python
# ✅ Good - Grouped by feature
tests/
├── conjugation/
│   ├── test_regular_verbs.py
│   ├── test_irregular_verbs.py
│   └── test_stem_changing_verbs.py
├── api/
│   ├── test_auth_endpoints.py
│   ├── test_exercise_endpoints.py
│   └── test_progress_endpoints.py
└── integration/
    └── test_full_practice_flow.py

# ❌ Bad - Everything in one file
tests/
└── test_everything.py  # 2000+ lines
```

### Avoid Test Duplication

```python
# ✅ Good - Use parametrize for similar tests
@pytest.mark.parametrize("verb,expected", [
    ("hablar", "hable"),
    ("comer", "coma"),
    ("vivir", "viva"),
])
def test_regular_verbs_yo_form(verb, expected):
    result = engine.conjugate(verb, "present_subjunctive", "yo")
    assert result.conjugation == expected

# ❌ Bad - Duplicate test code
def test_hablar_yo():
    result = engine.conjugate("hablar", "present_subjunctive", "yo")
    assert result.conjugation == "hable"

def test_comer_yo():
    result = engine.conjugate("comer", "present_subjunctive", "yo")
    assert result.conjugation == "coma"

def test_vivir_yo():
    result = engine.conjugate("vivir", "present_subjunctive", "yo")
    assert result.conjugation == "viva"
```

### Test What Matters

```python
# ✅ Good - Test business logic
def test_correct_answer_increases_xp():
    user = create_test_user(xp=0)
    submit_correct_answer(user.id, exercise.id)

    assert user.xp == 100

# ❌ Bad - Test implementation details
def test_xp_calculation_uses_addition():
    # This tests HOW it works, not WHAT it does
    assert calculate_xp.__code__.co_code.find(BINARY_ADD) != -1
```

## Quick Reference

### Test Template (pytest)

```python
import pytest
from backend.services.your_module import YourClass

class TestYourFeature:
    """Test suite for YourFeature"""

    @pytest.fixture
    def setup(self):
        """Setup test data"""
        return YourClass()

    def test_basic_functionality(self, setup):
        """Test basic functionality"""
        # Arrange
        input_data = "test"

        # Act
        result = setup.method(input_data)

        # Assert
        assert result == expected_value

    @pytest.mark.parametrize("input,expected", [
        ("a", "A"),
        ("b", "B"),
    ])
    def test_with_parameters(self, setup, input, expected):
        """Test with multiple parameters"""
        assert setup.method(input) == expected
```

### Test Template (Jest)

```typescript
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { YourComponent } from './YourComponent'

describe('YourComponent', () => {
  it('renders correctly', () => {
    render(<YourComponent />)
    expect(screen.getByText('Expected Text')).toBeInTheDocument()
  })

  it('handles user interaction', async () => {
    const user = userEvent.setup()
    const mockHandler = jest.fn()

    render(<YourComponent onClick={mockHandler} />)

    await user.click(screen.getByRole('button'))

    expect(mockHandler).toHaveBeenCalled()
  })
})
```

### Test Template (Playwright)

```typescript
import { test, expect } from '@playwright/test'

test.describe('Feature Name', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/your-page')
  })

  test('should do something', async ({ page }) => {
    await page.click('[data-testid="button"]')
    await expect(page.locator('.result')).toBeVisible()
  })
})
```

---

For troubleshooting test failures, see [TEST_TROUBLESHOOTING.md](./TEST_TROUBLESHOOTING.md).

For running tests, see [TEST_EXECUTION_GUIDE.md](./TEST_EXECUTION_GUIDE.md).

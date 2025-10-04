# Test Execution Guide

## Overview

This guide provides comprehensive instructions for running all tests in the Spanish Subjunctive Practice application. It covers backend tests (pytest), frontend tests (Jest), end-to-end tests (Playwright), and accessibility testing.

## Table of Contents

- [Quick Start](#quick-start)
- [Backend Testing (pytest)](#backend-testing-pytest)
- [Frontend Testing (Jest)](#frontend-testing-jest)
- [End-to-End Testing (Playwright)](#end-to-end-testing-playwright)
- [Accessibility Testing](#accessibility-testing)
- [Coverage Reports](#coverage-reports)
- [CI/CD Integration](#cicd-integration)
- [Interpreting Results](#interpreting-results)

## Quick Start

### Run All Tests

```bash
# From project root
npm run test:all

# Or run individually
npm run test:backend
npm run test:frontend
npm run test:e2e
```

### Prerequisites

**Backend:**
- Python 3.10+
- Virtual environment activated
- Backend dependencies installed: `pip install -r backend/requirements.txt`
- Test dependencies: `pip install -r backend/requirements-dev.txt`

**Frontend:**
- Node.js 18+
- Dependencies installed: `npm install`

**E2E:**
- Playwright browsers installed: `npx playwright install`
- Backend and frontend servers running

## Backend Testing (pytest)

### Running Backend Tests

#### All Backend Tests

```bash
# From backend directory
cd backend
pytest

# From project root
npm run test:backend
```

#### Specific Test Files

```bash
# Test conjugation engine
pytest tests/test_conjugation_engine.py

# Test exercise generator
pytest tests/test_exercise_generator.py

# Test API endpoints
pytest tests/test_api_endpoints.py

# Test TBLT scenarios
pytest tests/test_tblt_scenarios.py
```

#### Test by Marker

```bash
# Run only unit tests
pytest -m unit

# Run integration tests
pytest -m integration

# Run API tests
pytest -m api

# Run Spanish logic tests
pytest -m spanish_logic

# Run accessibility tests
pytest -m accessibility

# Run performance tests
pytest -m performance
```

#### Verbose Output

```bash
# Show detailed output
pytest -v

# Show print statements
pytest -s

# Extra verbose with test names
pytest -vv
```

#### Run Specific Tests

```bash
# Single test function
pytest tests/test_conjugation_engine.py::TestConjugationEngine::test_regular_ar_verb_present

# Test class
pytest tests/test_conjugation_engine.py::TestConjugationEngine

# Pattern matching
pytest -k "conjugation"
pytest -k "regular_verb"
```

#### Parallel Execution

```bash
# Install pytest-xdist
pip install pytest-xdist

# Run tests in parallel (4 workers)
pytest -n 4

# Auto-detect CPU count
pytest -n auto
```

#### Watch Mode (Development)

```bash
# Install pytest-watch
pip install pytest-watch

# Watch for changes and re-run
ptw

# Watch specific directory
ptw tests/
```

### Backend Test Configuration

**pytest.ini (backend/pytest.ini):**

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    unit: Fast, isolated unit tests
    integration: Component integration tests
    api: API endpoint tests
    performance: Timing-sensitive tests
    accessibility: WCAG compliance tests
    spanish_logic: Spanish language rule tests
addopts =
    -v
    --strict-markers
    --tb=short
    --disable-warnings
filterwarnings =
    ignore::DeprecationWarning
```

### Backend Coverage

```bash
# Generate coverage report
pytest --cov=backend --cov-report=html

# Coverage with terminal output
pytest --cov=backend --cov-report=term-missing

# Coverage for specific module
pytest --cov=backend.services.conjugation

# Fail if coverage below threshold
pytest --cov=backend --cov-fail-under=80
```

### Backend Test Environment

**Test Database:**

```bash
# Set test database URL
export DATABASE_URL="sqlite:///./test.db"

# Or use .env.test
cp .env.example .env.test
# Edit DATABASE_URL in .env.test
pytest --envfile=.env.test
```

**Mock External Services:**

```python
# Use pytest fixtures in conftest.py
@pytest.fixture
def mock_openai():
    with patch('openai.ChatCompletion.create') as mock:
        mock.return_value = {...}
        yield mock
```

## Frontend Testing (Jest)

### Running Frontend Tests

#### All Frontend Tests

```bash
# From frontend directory
cd frontend
npm test

# From project root
npm run test:frontend
```

#### Watch Mode

```bash
# Interactive watch mode
npm test -- --watch

# Watch all tests
npm test -- --watchAll
```

#### Specific Test Files

```bash
# Single file
npm test -- PracticeSession.test.tsx

# Pattern matching
npm test -- --testNamePattern="Practice"
npm test -- --testPathPattern="components"
```

#### Update Snapshots

```bash
# Update all snapshots
npm test -- --updateSnapshot

# Interactive snapshot update
npm test -- --watch
# Then press 'u' to update snapshots
```

#### Coverage Reports

```bash
# Generate coverage report
npm test -- --coverage

# Coverage with threshold
npm test -- --coverage --coverageThreshold='{"global":{"branches":70,"functions":70,"lines":70,"statements":70}}'

# Watch with coverage
npm test -- --watch --coverage
```

### Frontend Test Configuration

**jest.config.js:**

```javascript
module.exports = {
  testEnvironment: 'jest-environment-jsdom',
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/$1',
  },
  collectCoverageFrom: [
    'app/**/*.{js,jsx,ts,tsx}',
    'components/**/*.{js,jsx,ts,tsx}',
    '!**/*.d.ts',
    '!**/node_modules/**',
  ],
  coverageThresholds: {
    global: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70,
    },
  },
}
```

### Frontend Test Scripts

**package.json:**

```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "test:ci": "jest --ci --coverage --maxWorkers=2",
    "test:update-snapshots": "jest --updateSnapshot"
  }
}
```

## End-to-End Testing (Playwright)

### Running E2E Tests

#### All E2E Tests

```bash
# From frontend directory
cd frontend
npx playwright test

# From project root
npm run test:e2e
```

#### Start Servers First

```bash
# Terminal 1: Start backend
cd backend
uvicorn main:app --reload

# Terminal 2: Start frontend
cd frontend
npm run dev

# Terminal 3: Run E2E tests
npx playwright test
```

#### Specific Browsers

```bash
# Chromium only
npx playwright test --project=chromium

# Firefox only
npx playwright test --project=firefox

# WebKit (Safari) only
npx playwright test --project=webkit

# Mobile Chrome
npx playwright test --project="Mobile Chrome"

# Multiple browsers
npx playwright test --project=chromium --project=firefox
```

#### Headed Mode (Visual)

```bash
# Run with browser visible
npx playwright test --headed

# Debug mode
npx playwright test --debug

# Specific test in debug
npx playwright test critical-user-journeys.spec.js --debug
```

#### Specific Tests

```bash
# Single test file
npx playwright test tests/e2e/critical-user-journeys.spec.js

# Pattern matching
npx playwright test -g "practice session"

# Single test
npx playwright test -g "should complete full practice session"
```

#### Parallel Execution

```bash
# Run in parallel (default)
npx playwright test

# Single worker (sequential)
npx playwright test --workers=1

# Specific worker count
npx playwright test --workers=4
```

### E2E Test Configuration

**playwright.config.ts:**

```typescript
export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['json', { outputFile: 'test-results.json' }],
  ],
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
  ],
})
```

### E2E Reports

```bash
# View HTML report
npx playwright show-report

# Generate report after test
npx playwright test --reporter=html

# JSON report
npx playwright test --reporter=json

# Multiple reporters
npx playwright test --reporter=html,json
```

### E2E Debugging

```bash
# Step through test
npx playwright test --debug

# UI Mode (interactive)
npx playwright test --ui

# Trace viewer
npx playwright show-trace trace.zip

# Generate trace
npx playwright test --trace on
```

## Accessibility Testing

### Automated Accessibility Tests

#### Backend Accessibility

```bash
# Run accessibility-marked tests
pytest -m accessibility

# Specific accessibility test
pytest tests/test_accessibility_compliance.py
```

#### Frontend Accessibility (jest-axe)

```bash
# Run component accessibility tests
npm test -- --testPathPattern="accessibility"

# Specific component
npm test -- components/PracticeSession.accessibility.test.tsx
```

#### E2E Accessibility (Playwright + axe)

```bash
# Run E2E accessibility tests
npx playwright test accessibility.spec.js

# With specific WCAG level
WCAG_LEVEL=AAA npx playwright test accessibility.spec.js
```

### Manual Accessibility Testing

**Keyboard Navigation:**
```bash
# Test keyboard navigation
npx playwright test --headed keyboard-navigation.spec.js
```

**Screen Reader Testing:**
- macOS: VoiceOver (Cmd + F5)
- Windows: NVDA (free) or JAWS
- Linux: Orca

**Color Contrast:**
```bash
# Run contrast tests
npm test -- color-contrast.test.tsx
```

## Coverage Reports

### Backend Coverage

```bash
# HTML report
pytest --cov=backend --cov-report=html
# Open: backend/htmlcov/index.html

# Terminal report
pytest --cov=backend --cov-report=term-missing

# XML report (for CI)
pytest --cov=backend --cov-report=xml

# Multiple formats
pytest --cov=backend --cov-report=html --cov-report=term --cov-report=xml
```

### Frontend Coverage

```bash
# HTML report
npm test -- --coverage
# Open: frontend/coverage/lcov-report/index.html

# JSON report
npm test -- --coverage --coverageReporters=json

# Text summary
npm test -- --coverage --coverageReporters=text-summary
```

### Combined Coverage

```bash
# Run all tests with coverage
npm run test:coverage:all

# This runs:
# 1. Backend coverage
# 2. Frontend coverage
# 3. Merges reports (if configured)
```

### Coverage Thresholds

**Backend (pytest.ini):**
```ini
[tool:pytest]
addopts =
    --cov=backend
    --cov-fail-under=80
```

**Frontend (jest.config.js):**
```javascript
coverageThresholds: {
  global: {
    branches: 70,
    functions: 70,
    lines: 70,
    statements: 70,
  },
}
```

## CI/CD Integration

### GitHub Actions Workflow

**.github/workflows/tests.yml:**

```yaml
name: Test Suite

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.10, 3.11]
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run tests
        run: |
          cd backend
          pytest --cov=backend --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 18
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      - name: Run tests
        run: |
          cd frontend
          npm test -- --ci --coverage

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node.js
        uses: actions/setup-node@v3
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
          npx playwright install --with-deps
      - name: Run E2E tests
        run: |
          cd frontend
          npx playwright test
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: frontend/playwright-report
```

### Pre-commit Hooks

**.pre-commit-config.yaml:**

```yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: bash -c 'cd backend && pytest'
        language: system
        pass_filenames: false
        always_run: true

      - id: jest
        name: jest
        entry: bash -c 'cd frontend && npm test -- --ci --bail'
        language: system
        pass_filenames: false
        always_run: true
```

## Interpreting Results

### pytest Output

```bash
# Example output
test_conjugation_engine.py::TestConjugationEngine::test_regular_ar_verb_present PASSED [10%]
test_conjugation_engine.py::TestConjugationEngine::test_regular_er_verb_present PASSED [20%]
test_conjugation_engine.py::TestConjugationEngine::test_irregular_ser_present PASSED [30%]

========================= 15 passed in 2.45s ==========================
```

**Understanding:**
- ✓ `PASSED`: Test succeeded
- ✗ `FAILED`: Test failed (shows assertion error)
- `s` or `SKIPPED`: Test skipped
- `x` or `XFAIL`: Expected to fail (marked with @pytest.mark.xfail)
- `X` or `XPASS`: Expected to fail but passed

### Jest Output

```bash
# Example output
PASS  components/PracticeSession.test.tsx
  ✓ renders practice session (45 ms)
  ✓ handles answer submission (23 ms)
  ✓ displays feedback correctly (18 ms)

Test Suites: 1 passed, 1 total
Tests:       3 passed, 3 total
Snapshots:   0 total
Time:        2.456 s
```

**Understanding:**
- ✓ Green checkmark: Test passed
- ✗ Red X: Test failed
- ○ Yellow circle: Test skipped
- Snapshot summary shows snapshot status

### Playwright Output

```bash
# Example output
Running 5 tests using 3 workers
  ✓ [chromium] › critical-user-journeys.spec.js:10:5 › should complete practice session (4.5s)
  ✓ [firefox] › critical-user-journeys.spec.js:10:5 › should complete practice session (5.1s)
  ✓ [webkit] › critical-user-journeys.spec.js:10:5 › should complete practice session (4.8s)

5 passed (14.4s)
```

**Understanding:**
- Browser name in brackets: Which browser ran the test
- Time in parentheses: Test duration
- Final summary shows pass/fail counts

### Coverage Reports

**Coverage Percentages:**
- **90-100%**: Excellent coverage
- **70-90%**: Good coverage
- **50-70%**: Acceptable for non-critical code
- **<50%**: Needs improvement

**Coverage Metrics:**
- **Lines**: Percentage of code lines executed
- **Branches**: Percentage of conditional paths taken
- **Functions**: Percentage of functions called
- **Statements**: Percentage of statements executed

## Performance Benchmarks

### Backend Performance

```bash
# Run performance tests
pytest -m performance

# With benchmarking
pytest --benchmark-only

# Generate benchmark report
pytest --benchmark-autosave --benchmark-name=baseline
```

### Frontend Performance

```bash
# Lighthouse CI
npm run lighthouse:ci

# Performance tests
npm test -- performance.test.ts
```

### E2E Performance

```bash
# With performance metrics
npx playwright test --reporter=html,json

# Trace with performance data
npx playwright test --trace on
```

## Troubleshooting

### Common Issues

**Backend:**
```bash
# Database locked
rm -f test.db*
pytest

# Import errors
pip install -e .
pytest

# Fixture errors
pytest --fixtures  # List available fixtures
```

**Frontend:**
```bash
# Clear cache
npm test -- --clearCache

# Update snapshots
npm test -- --updateSnapshot

# Module not found
rm -rf node_modules
npm install
```

**E2E:**
```bash
# Browser not installed
npx playwright install

# Server not running
# Check backend: curl http://localhost:8000/health
# Check frontend: curl http://localhost:3000

# Port already in use
lsof -ti:8000 | xargs kill -9  # Backend
lsof -ti:3000 | xargs kill -9  # Frontend
```

## Best Practices

### Running Tests

1. **Always run tests before committing**
2. **Use watch mode during development**
3. **Run full suite before PR**
4. **Check coverage after adding features**
5. **Use specific markers for faster feedback**

### Performance

1. **Parallelize when possible** (`pytest -n auto`)
2. **Use appropriate test markers** (run only what's needed)
3. **Mock external services** (faster, more reliable)
4. **Clean up test data** (prevent test pollution)

### Debugging

1. **Use verbose mode** (`-v`, `-vv`)
2. **Enable debug mode** (`--debug` for Playwright)
3. **Check traces** (Playwright trace viewer)
4. **Use breakpoints** (`import pdb; pdb.set_trace()`)

## Quick Reference

### Backend Commands
```bash
pytest                          # All tests
pytest -v                       # Verbose
pytest -m unit                  # Unit tests only
pytest -k "conjugation"        # Pattern match
pytest --cov=backend           # With coverage
pytest -n auto                 # Parallel
```

### Frontend Commands
```bash
npm test                        # All tests
npm test -- --watch            # Watch mode
npm test -- --coverage         # With coverage
npm test -- PracticeSession    # Specific file
npm test -- --updateSnapshot   # Update snapshots
```

### E2E Commands
```bash
npx playwright test            # All tests
npx playwright test --headed   # Visual mode
npx playwright test --debug    # Debug mode
npx playwright test --ui       # UI mode
npx playwright show-report     # View report
```

---

For troubleshooting specific test failures, see [TEST_TROUBLESHOOTING.md](./TEST_TROUBLESHOOTING.md).

For writing new tests, see [TEST_WRITING_GUIDE.md](./TEST_WRITING_GUIDE.md).

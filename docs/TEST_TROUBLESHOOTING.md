# Test Troubleshooting Guide

## Overview

This guide provides solutions to common testing issues, debugging techniques, and troubleshooting strategies for the Spanish Subjunctive Practice application.

## Table of Contents

- [Backend Test Issues](#backend-test-issues)
- [Frontend Test Issues](#frontend-test-issues)
- [E2E Test Issues](#e2e-test-issues)
- [CI/CD Issues](#cicd-issues)
- [Debugging Techniques](#debugging-techniques)
- [Performance Issues](#performance-issues)
- [Flaky Test Resolution](#flaky-test-resolution)

## Backend Test Issues

### Database Issues

#### Problem: Database Locked Error

```bash
sqlite3.OperationalError: database is locked
```

**Solutions:**

1. **Close all database connections:**
```python
# In conftest.py
@pytest.fixture(scope="function")
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
```

2. **Use separate test database:**
```bash
# Set test database
export DATABASE_URL="sqlite:///./test.db"

# Or in pytest.ini
[pytest]
env =
    DATABASE_URL=sqlite:///./test.db
```

3. **Clear test database before tests:**
```bash
# Remove old test database
rm -f test.db*

# Run tests
pytest
```

4. **Use in-memory database:**
```python
# conftest.py
@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
```

#### Problem: Migration Issues

```bash
alembic.util.exc.CommandError: Can't locate revision identified by 'abc123'
```

**Solutions:**

1. **Reset migrations:**
```bash
# Downgrade all
alembic downgrade base

# Re-run migrations
alembic upgrade head
```

2. **Clean migration history:**
```bash
# Delete migration files (backup first!)
rm backend/alembic/versions/*.py

# Regenerate migrations
alembic revision --autogenerate -m "initial"
alembic upgrade head
```

3. **Use test-specific migrations:**
```python
# In conftest.py
@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    from alembic import command
    from alembic.config import Config

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    yield
    command.downgrade(alembic_cfg, "base")
```

### Import Errors

#### Problem: Module Not Found

```bash
ModuleNotFoundError: No module named 'backend'
```

**Solutions:**

1. **Install package in editable mode:**
```bash
pip install -e .
```

2. **Add to PYTHONPATH:**
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest
```

3. **Fix import paths in conftest.py:**
```python
# conftest.py
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
```

4. **Use absolute imports:**
```python
# Instead of: from models import User
from backend.models.user import User
```

### Fixture Issues

#### Problem: Fixture Not Found

```bash
fixture 'db_session' not found
```

**Solutions:**

1. **Check conftest.py location:**
```bash
# Should be in tests/ directory
tests/
├── conftest.py  # ← Here
└── test_*.py
```

2. **Verify fixture is defined:**
```python
# conftest.py
import pytest

@pytest.fixture
def db_session():
    # Must have @pytest.fixture decorator
    pass
```

3. **Check scope issues:**
```python
# If using scope, ensure it's accessible
@pytest.fixture(scope="function")  # or "session", "module"
def db_session():
    pass
```

### Async Test Issues

#### Problem: Async Function Not Awaited

```bash
RuntimeWarning: coroutine 'test_api_endpoint' was never awaited
```

**Solutions:**

1. **Add pytest-asyncio marker:**
```python
import pytest

@pytest.mark.asyncio
async def test_api_endpoint():
    response = await client.get("/api/exercises")
    assert response.status_code == 200
```

2. **Install pytest-asyncio:**
```bash
pip install pytest-asyncio
```

3. **Configure in pytest.ini:**
```ini
[pytest]
asyncio_mode = auto
```

### Mock Issues

#### Problem: Mock Not Working

```python
# Mock isn't being called
mock_openai.assert_called()  # AssertionError
```

**Solutions:**

1. **Verify patch path:**
```python
# Patch where it's used, not where it's defined
# ✅ Correct
@patch('backend.services.ai.openai.ChatCompletion.create')

# ❌ Wrong
@patch('openai.ChatCompletion.create')
```

2. **Use correct context:**
```python
# Use 'with' for scoped mocking
with patch('module.function') as mock:
    mock.return_value = "test"
    result = function_under_test()
    mock.assert_called()
```

3. **Check import timing:**
```python
# Import AFTER patching
with patch('module.Class') as MockClass:
    from module import Class  # Import here
    obj = Class()
```

## Frontend Test Issues

### React Testing Library Issues

#### Problem: Element Not Found

```bash
TestingLibraryElementError: Unable to find element
```

**Solutions:**

1. **Wait for async content:**
```typescript
// Use waitFor
await waitFor(() => {
  expect(screen.getByText('Expected Text')).toBeInTheDocument()
})

// Or findBy (automatically waits)
const element = await screen.findByText('Expected Text')
```

2. **Check query method:**
```typescript
// getBy - throws if not found (use for assertions)
screen.getByRole('button')

// queryBy - returns null if not found (use for non-existence)
expect(screen.queryByText('Not Here')).not.toBeInTheDocument()

// findBy - async, waits for element
await screen.findByText('Async Content')
```

3. **Use correct role:**
```typescript
// Check actual role with logRoles
import { logRoles } from '@testing-library/react'

const { container } = render(<Component />)
logRoles(container)

// Then use correct role
screen.getByRole('textbox')  // input
screen.getByRole('button')   // button
```

4. **Add test IDs for complex queries:**
```typescript
// Component
<div data-testid="exercise-card">...</div>

// Test
screen.getByTestId('exercise-card')
```

#### Problem: State Updates Not Reflected

```typescript
// Test fails because state hasn't updated
fireEvent.click(button)
expect(screen.getByText('Updated')).toBeInTheDocument()  // Fails
```

**Solutions:**

1. **Use userEvent instead of fireEvent:**
```typescript
import userEvent from '@testing-library/user-event'

const user = userEvent.setup()
await user.click(button)
await waitFor(() => {
  expect(screen.getByText('Updated')).toBeInTheDocument()
})
```

2. **Wrap in act() if needed:**
```typescript
import { act } from '@testing-library/react'

await act(async () => {
  fireEvent.click(button)
})
```

3. **Wait for state updates:**
```typescript
await waitFor(() => {
  expect(screen.getByText('Updated')).toBeInTheDocument()
})
```

### Jest Configuration Issues

#### Problem: Module Not Found

```bash
Cannot find module '@/components/Button'
```

**Solutions:**

1. **Configure moduleNameMapper:**
```javascript
// jest.config.js
module.exports = {
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/$1',
    '^@/components/(.*)$': '<rootDir>/components/$1',
  },
}
```

2. **Check tsconfig paths:**
```json
// tsconfig.json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./*"],
      "@/components/*": ["./components/*"]
    }
  }
}
```

3. **Install required packages:**
```bash
npm install -D @types/jest @testing-library/jest-dom
```

#### Problem: CSS/Image Import Errors

```bash
SyntaxError: Unexpected token .classname
```

**Solutions:**

1. **Mock CSS modules:**
```javascript
// jest.config.js
module.exports = {
  moduleNameMapper: {
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
    '\\.(jpg|jpeg|png|gif|svg)$': '<rootDir>/__mocks__/fileMock.js',
  },
}
```

2. **Create file mock:**
```javascript
// __mocks__/fileMock.js
module.exports = 'test-file-stub'
```

### Snapshot Issues

#### Problem: Snapshot Mismatch

```bash
Snapshot name: `Component should render 1`
- Snapshot
+ Received
```

**Solutions:**

1. **Update snapshots if changes are intentional:**
```bash
npm test -- --updateSnapshot
# or press 'u' in watch mode
```

2. **Review snapshot diff carefully:**
```bash
# Run with verbose to see diff
npm test -- --verbose
```

3. **Use inline snapshots for small data:**
```typescript
expect(value).toMatchInlineSnapshot(`"expected"`)
```

4. **Make snapshots more specific:**
```typescript
// Instead of whole component
expect(container).toMatchSnapshot()

// Snapshot specific parts
expect(screen.getByRole('button')).toMatchSnapshot()
```

### Mock Service Worker (MSW) Issues

#### Problem: Handlers Not Working

```typescript
// API calls returning undefined
const data = await fetch('/api/exercises')  // undefined
```

**Solutions:**

1. **Verify server setup:**
```typescript
// tests/setup.ts
import { setupServer } from 'msw/node'
import { handlers } from './mocks/handlers'

const server = setupServer(...handlers)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

2. **Check handler path:**
```typescript
// handlers.ts
rest.get('/api/exercises', (req, res, ctx) => {
  // Use full path or baseURL
  return res(ctx.json({ exercises: [] }))
})
```

3. **Import setup file:**
```javascript
// jest.config.js
setupFilesAfterEnv: ['<rootDir>/tests/setup.ts']
```

## E2E Test Issues

### Playwright Issues

#### Problem: Browser Not Found

```bash
Error: browserType.launch: Executable doesn't exist
```

**Solutions:**

1. **Install browsers:**
```bash
npx playwright install

# Or specific browser
npx playwright install chromium
```

2. **Install system dependencies:**
```bash
# Ubuntu/Debian
npx playwright install-deps

# Or manually
sudo apt-get install libnss3 libatk1.0-0 libx11-xcb1
```

#### Problem: Timeout Waiting for Element

```bash
TimeoutError: Timeout 30000ms exceeded waiting for selector
```

**Solutions:**

1. **Increase timeout:**
```typescript
// For specific action
await page.waitForSelector('.element', { timeout: 60000 })

// For test
test('name', async ({ page }) => {
  test.setTimeout(60000)
  // ...
})

// Globally in config
export default defineConfig({
  timeout: 60000,
})
```

2. **Wait for network idle:**
```typescript
await page.goto('/practice', { waitUntil: 'networkidle' })
```

3. **Use better selectors:**
```typescript
// ❌ Fragile
await page.click('.btn-primary')

// ✅ Better
await page.click('button:has-text("Submit")')
await page.click('[data-testid="submit-button"]')
await page.click('button[type="submit"]')
```

4. **Debug with headed mode:**
```bash
npx playwright test --headed --debug
```

#### Problem: Server Not Running

```bash
Error: connect ECONNREFUSED 127.0.0.1:3000
```

**Solutions:**

1. **Use webServer config:**
```typescript
// playwright.config.ts
export default defineConfig({
  webServer: {
    command: 'npm run dev',
    port: 3000,
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },
})
```

2. **Start servers manually:**
```bash
# Terminal 1
cd backend && uvicorn main:app --reload

# Terminal 2
cd frontend && npm run dev

# Terminal 3
cd frontend && npx playwright test
```

3. **Check port availability:**
```bash
# Kill processes on port
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9
```

#### Problem: Flaky Screenshot Tests

```bash
Error: Screenshot comparison failed
```

**Solutions:**

1. **Add threshold:**
```typescript
await expect(page).toHaveScreenshot('name.png', {
  maxDiffPixels: 100,
  threshold: 0.2,
})
```

2. **Disable animations:**
```typescript
// playwright.config.ts
use: {
  animations: 'disabled',
}

// Or in test
await page.emulateMedia({ reducedMotion: 'reduce' })
```

3. **Wait for fonts to load:**
```typescript
await page.waitForLoadState('networkidle')
await page.waitForTimeout(500)  // Allow fonts to render
```

4. **Use consistent viewport:**
```typescript
// playwright.config.ts
use: {
  viewport: { width: 1280, height: 720 },
}
```

## CI/CD Issues

### GitHub Actions Issues

#### Problem: Tests Pass Locally But Fail in CI

**Solutions:**

1. **Check environment variables:**
```yaml
# .github/workflows/tests.yml
env:
  DATABASE_URL: sqlite:///./test.db
  NODE_ENV: test
```

2. **Use consistent Node/Python versions:**
```yaml
- uses: actions/setup-python@v4
  with:
    python-version: '3.10'  # Match local version

- uses: actions/setup-node@v3
  with:
    node-version: '18'  # Match local version
```

3. **Install system dependencies:**
```yaml
- name: Install dependencies
  run: |
    sudo apt-get update
    sudo apt-get install -y python3-dev postgresql-client
```

4. **Use caching:**
```yaml
- uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}

- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
```

#### Problem: Timeout in CI

```bash
Error: The operation was canceled.
```

**Solutions:**

1. **Increase timeout:**
```yaml
jobs:
  test:
    timeout-minutes: 30  # Default is 360
```

2. **Run tests in parallel:**
```bash
# pytest
pytest -n auto

# Playwright
npx playwright test --workers=2
```

3. **Split test jobs:**
```yaml
jobs:
  unit-tests:
    # ...
  integration-tests:
    # ...
  e2e-tests:
    # ...
```

### Docker Test Issues

#### Problem: Tests Fail in Docker

```bash
ERROR: Failed to build test environment
```

**Solutions:**

1. **Check Dockerfile test stage:**
```dockerfile
FROM python:3.10 as test
WORKDIR /app
COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt
COPY . .
RUN pytest
```

2. **Use docker-compose for tests:**
```yaml
# docker-compose.test.yml
version: '3.8'
services:
  test:
    build:
      context: .
      target: test
    environment:
      - DATABASE_URL=postgresql://test:test@db:5432/test
    depends_on:
      - db
  db:
    image: postgres:14
    environment:
      POSTGRES_DB: test
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
```

3. **Run tests in container:**
```bash
docker-compose -f docker-compose.test.yml run --rm test
```

## Debugging Techniques

### Backend Debugging

#### Using pdb

```python
def test_conjugation():
    engine = ConjugationEngine()

    # Add breakpoint
    import pdb; pdb.set_trace()

    result = engine.conjugate("hablar", "present_subjunctive", "yo")
    assert result.conjugation == "hable"
```

**pdb Commands:**
- `n` - Next line
- `s` - Step into function
- `c` - Continue execution
- `p variable` - Print variable
- `l` - List code
- `q` - Quit

#### Using pytest verbosity

```bash
# Show print statements
pytest -s

# Show full traceback
pytest --tb=long

# Show local variables in traceback
pytest --tb=short --showlocals

# Stop at first failure
pytest -x

# Show slowest tests
pytest --durations=10
```

#### Using logging

```python
import logging

def test_with_logging():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    logger.debug("Starting test")
    # ... test code ...
    logger.debug("Result: %s", result)
```

### Frontend Debugging

#### Using console.log in tests

```typescript
test('debug test', () => {
  render(<Component />)

  // Print DOM
  screen.debug()

  // Print specific element
  screen.debug(screen.getByRole('button'))

  // Custom logging
  console.log('State:', component.state)
})
```

#### Using React DevTools

```typescript
import { render } from '@testing-library/react'

test('debug with DevTools', () => {
  const { container } = render(<Component />)

  // Pause test (in headed mode)
  debugger

  // Inspect in DevTools
})
```

#### Using test-specific debug helpers

```typescript
import { logRoles, prettyDOM } from '@testing-library/react'

test('debug', () => {
  const { container } = render(<Component />)

  // Log all roles
  logRoles(container)

  // Pretty print DOM
  console.log(prettyDOM(container))
})
```

### E2E Debugging

#### Playwright Debug Mode

```bash
# Interactive debug mode
npx playwright test --debug

# Debug specific test
npx playwright test practice.spec.ts --debug

# Debug with headed browser
npx playwright test --headed --debug
```

#### Playwright Inspector

```typescript
// Add in test
await page.pause()  // Opens inspector

// Or use debug mode
npx playwright test --debug
```

#### Trace Viewer

```bash
# Record trace
npx playwright test --trace on

# View trace
npx playwright show-trace trace.zip
```

```typescript
// In test
test('with trace', async ({ page }) => {
  await page.tracing.start({ screenshots: true, snapshots: true })

  // ... test actions ...

  await page.tracing.stop({ path: 'trace.zip' })
})
```

## Performance Issues

### Slow Tests

#### Problem: Tests Take Too Long

**Solutions:**

1. **Run tests in parallel:**
```bash
# pytest
pytest -n auto  # Use all CPU cores
pytest -n 4     # Use 4 workers

# Jest
npm test -- --maxWorkers=4
```

2. **Use faster test database:**
```python
# Use in-memory SQLite instead of PostgreSQL
DATABASE_URL = "sqlite:///:memory:"
```

3. **Mock slow operations:**
```python
@patch('slow_module.slow_function')
def test_fast(mock_slow):
    mock_slow.return_value = "instant result"
    # ... test ...
```

4. **Skip slow tests in development:**
```python
@pytest.mark.slow
def test_comprehensive_integration():
    # ...

# Run without slow tests
pytest -m "not slow"
```

### Memory Issues

#### Problem: Tests Use Too Much Memory

**Solutions:**

1. **Clean up after tests:**
```python
@pytest.fixture
def db_session():
    session = create_session()
    yield session
    session.close()
    session.expunge_all()
```

2. **Use generators for large datasets:**
```python
@pytest.fixture
def large_dataset():
    # Instead of creating all at once
    for i in range(10000):
        yield create_item(i)
```

3. **Limit parallel workers:**
```bash
# Reduce memory by using fewer workers
pytest -n 2  # Instead of -n auto
```

## Flaky Test Resolution

### Identifying Flaky Tests

```bash
# Run test multiple times
pytest test_flaky.py --count=100

# Run until it fails
pytest test_flaky.py --maxfail=1 --count=100
```

### Common Causes & Solutions

#### 1. Race Conditions

```typescript
// ❌ Flaky - doesn't wait
test('flaky', () => {
  render(<AsyncComponent />)
  expect(screen.getByText('Loaded')).toBeInTheDocument()  // Might not be loaded yet
})

// ✅ Fixed - waits for element
test('fixed', async () => {
  render(<AsyncComponent />)
  await waitFor(() => {
    expect(screen.getByText('Loaded')).toBeInTheDocument()
  })
})
```

#### 2. Time-Dependent Tests

```python
# ❌ Flaky - depends on execution time
def test_flaky():
    start = datetime.now()
    do_work()
    assert (datetime.now() - start).seconds < 1  # Sometimes fails

# ✅ Fixed - mock time
@patch('module.datetime')
def test_fixed(mock_datetime):
    mock_datetime.now.return_value = datetime(2025, 1, 1)
    # ... test ...
```

#### 3. Non-Deterministic Behavior

```python
# ❌ Flaky - random order
def test_flaky():
    items = get_random_items()
    assert items[0] == "first"  # Order changes

# ✅ Fixed - sort or don't depend on order
def test_fixed():
    items = sorted(get_random_items())
    assert "expected_item" in items
```

#### 4. External Dependencies

```python
# ❌ Flaky - depends on external API
def test_flaky():
    response = requests.get("https://api.example.com")
    assert response.status_code == 200  # API might be down

# ✅ Fixed - mock external calls
@patch('requests.get')
def test_fixed(mock_get):
    mock_get.return_value.status_code = 200
    # ... test ...
```

## Quick Reference

### Common Error Solutions

| Error | Quick Fix |
|-------|-----------|
| Database locked | `rm -f test.db && pytest` |
| Module not found | `pip install -e .` |
| Fixture not found | Check `conftest.py` location |
| Element not found | Use `waitFor()` or `findBy*` |
| Snapshot mismatch | `npm test -- --updateSnapshot` |
| Browser not found | `npx playwright install` |
| Timeout in CI | Increase timeout, use caching |
| Flaky test | Add waits, mock time/randomness |

### Debugging Commands

```bash
# Backend
pytest -s --tb=long --showlocals  # Verbose debugging
pytest --pdb  # Drop into debugger on failure

# Frontend
npm test -- --verbose  # Show all output
npm test -- --watch  # Interactive mode

# E2E
npx playwright test --debug  # Debug mode
npx playwright test --headed  # Visual debugging
npx playwright show-trace trace.zip  # View trace
```

### Useful pytest Flags

```bash
-v              # Verbose
-vv             # Extra verbose
-s              # Show print statements
-x              # Stop at first failure
--pdb           # Debug on failure
--lf            # Run last failed
--ff            # Run failures first
-k "pattern"    # Run tests matching pattern
-m marker       # Run tests with marker
--durations=10  # Show slowest tests
```

### Useful Jest Flags

```bash
--watch         # Watch mode
--coverage      # Coverage report
--verbose       # Verbose output
--silent        # Suppress console
--bail          # Stop on first failure
--onlyFailures  # Re-run only failures
--clearCache    # Clear Jest cache
```

---

For test execution details, see [TEST_EXECUTION_GUIDE.md](./TEST_EXECUTION_GUIDE.md).

For writing tests, see [TEST_WRITING_GUIDE.md](./TEST_WRITING_GUIDE.md).

For QA procedures, see [QA_CHECKLIST.md](./QA_CHECKLIST.md).

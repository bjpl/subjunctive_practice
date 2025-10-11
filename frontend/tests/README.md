# Frontend Testing Suite

Comprehensive testing suite for the Subjunctive Practice Next.js frontend application.

## Table of Contents

- [Overview](#overview)
- [Test Structure](#test-structure)
- [Running Tests](#running-tests)
- [Test Types](#test-types)
- [Writing Tests](#writing-tests)
- [Coverage Reports](#coverage-reports)
- [CI/CD Integration](#cicd-integration)

## Overview

This testing suite includes:

- **45+ Unit Tests** for UI components and utilities
- **25+ Integration Tests** for Redux store, hooks, and API interactions
- **18+ E2E Tests** covering complete user workflows
- **15+ Accessibility Tests** ensuring WCAG compliance
- **Mock Service Worker (MSW)** for API mocking
- **Playwright** for end-to-end testing

**Target Coverage:** 75%+ code coverage

## Test Structure

```
tests/
├── unit/                    # Component and utility unit tests
│   ├── components/
│   │   └── ui/             # UI component tests
│   └── lib/                # Utility function tests
├── integration/            # Integration tests
│   ├── store/              # Redux store tests
│   └── hooks/              # Custom hooks tests
├── e2e/                    # End-to-end tests
│   ├── auth.spec.ts        # Authentication flows
│   ├── practice.spec.ts    # Practice session flows
│   ├── dashboard.spec.ts   # Dashboard interactions
│   ├── settings.spec.ts    # Settings management
│   └── responsive.spec.ts  # Responsive design tests
├── accessibility/          # Accessibility tests
│   ├── components.a11y.test.tsx
│   ├── keyboard-navigation.test.tsx
│   └── aria-labels.test.tsx
├── mocks/                  # Mock data and handlers
│   ├── handlers.ts         # MSW API handlers
│   ├── server.ts           # MSW server setup (Node)
│   └── browser.ts          # MSW worker setup (Browser)
└── utils/                  # Test utilities
    └── test-utils.tsx      # Custom render functions
```

## Running Tests

### Unit & Integration Tests (Jest)

```bash
# Run all unit and integration tests
npm test

# Run tests in watch mode
npm run test:watch

# Run with coverage report
npm run test:coverage

# Run only unit tests
npm run test:unit

# Run only integration tests
npm run test:integration

# Run only accessibility tests
npm run test:a11y
```

### E2E Tests (Playwright)

```bash
# Install Playwright browsers (first time only)
npm run playwright:install

# Run all E2E tests
npm run test:e2e

# Run E2E tests with UI mode
npm run test:e2e:ui

# Run E2E tests in headed mode (see browser)
npm run test:e2e:headed

# Debug E2E tests
npm run test:e2e:debug
```

### Run All Tests

```bash
# Run all tests (unit, integration, accessibility, and E2E)
npm run test:all
```

## Test Types

### Unit Tests

Testing individual components and functions in isolation.

**Examples:**
- Button component renders correctly
- Input component handles user input
- Card component applies proper styles
- Utility functions work as expected

**Location:** `tests/unit/`

### Integration Tests

Testing how different parts work together.

**Examples:**
- Redux store state management
- API calls with RTK Query
- Custom hooks behavior
- Form validation logic

**Location:** `tests/integration/`

### E2E Tests

Testing complete user workflows from start to finish.

**Examples:**
- User registration and login
- Complete practice session
- Dashboard navigation
- Settings updates
- Responsive behavior

**Location:** `tests/e2e/`

### Accessibility Tests

Ensuring the app is accessible to all users.

**Examples:**
- WCAG compliance with jest-axe
- Keyboard navigation
- Screen reader compatibility
- ARIA labels and roles
- Focus management

**Location:** `tests/accessibility/`

## Writing Tests

### Unit Test Example

```typescript
import { render, screen } from '@testing-library/react';
import { Button } from '@/components/ui/button';

describe('Button', () => {
  it('renders with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button')).toHaveTextContent('Click me');
  });
});
```

### Integration Test Example

```typescript
import { renderWithProviders } from '../utils/test-utils';
import { useAppSelector } from '@/hooks/use-redux';

describe('Redux Integration', () => {
  it('selects auth state', () => {
    const { result } = renderHook(
      () => useAppSelector(state => state.auth),
      { wrapper: ReduxProvider }
    );
    expect(result.current.isAuthenticated).toBe(false);
  });
});
```

### E2E Test Example

```typescript
import { test, expect } from '@playwright/test';

test('user can login', async ({ page }) => {
  await page.goto('/auth/login');
  await page.fill('input[name="email"]', 'test@example.com');
  await page.fill('input[name="password"]', 'password');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL(/dashboard/);
});
```

### Accessibility Test Example

```typescript
import { axe } from 'jest-axe';

describe('Accessibility', () => {
  it('has no violations', async () => {
    const { container } = render(<Button>Click</Button>);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

## Mock Service Worker (MSW)

API requests are mocked using MSW for consistent, fast testing.

### Adding New Endpoints

Edit `tests/mocks/handlers.ts`:

```typescript
export const handlers = [
  http.get('/api/new-endpoint', () => {
    return HttpResponse.json({ data: 'mock data' });
  }),
];
```

### Overriding Handlers in Tests

```typescript
import { server } from '../mocks/server';
import { http, HttpResponse } from 'msw';

test('handles error', async () => {
  server.use(
    http.get('/api/endpoint', () => {
      return HttpResponse.json({ error: 'Error' }, { status: 500 });
    })
  );
  // Test error handling
});
```

## Coverage Reports

Coverage reports are generated in the `coverage/` directory.

```bash
# Generate and view coverage
npm run test:coverage

# Open coverage report in browser
# coverage/lcov-report/index.html
```

**Coverage Thresholds:**
- Branches: 70%
- Functions: 70%
- Lines: 70%
- Statements: 70%

## CI/CD Integration

### GitHub Actions Example

```yaml
- name: Run Tests
  run: |
    npm run test:coverage
    npm run test:e2e

- name: Upload Coverage
  uses: codecov/codecov-action@v3
  with:
    files: ./coverage/lcov.info
```

### Pre-commit Hooks

Tests can be run automatically before commits:

```bash
# Install husky
npx husky install

# Add pre-commit hook
npx husky add .husky/pre-commit "npm run test:unit"
```

## Best Practices

1. **Test User Behavior:** Focus on how users interact with the app
2. **Avoid Implementation Details:** Test what users see, not internal state
3. **Use Semantic Queries:** Prefer `getByRole`, `getByLabelText` over `getByTestId`
4. **Mock External Dependencies:** Use MSW for API calls
5. **Keep Tests Isolated:** Each test should be independent
6. **Write Descriptive Test Names:** Clearly describe what is being tested
7. **Test Accessibility:** Include a11y tests for all components
8. **Maintain Test Data:** Keep mock data realistic and up-to-date

## Debugging Tests

### Jest Tests

```bash
# Debug with Chrome DevTools
node --inspect-brk node_modules/.bin/jest --runInBand

# Run specific test file
npm test -- Button.test.tsx

# Run tests matching pattern
npm test -- --testNamePattern="should render"
```

### Playwright Tests

```bash
# Run with debugger
npm run test:e2e:debug

# Run specific test file
npx playwright test tests/e2e/auth.spec.ts

# Generate trace for failed tests
npx playwright test --trace on
```

## Resources

- [Jest Documentation](https://jestjs.io/)
- [React Testing Library](https://testing-library.com/react)
- [Playwright Documentation](https://playwright.dev/)
- [MSW Documentation](https://mswjs.io/)
- [jest-axe Documentation](https://github.com/nickcolley/jest-axe)
- [WCAG Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

## Troubleshooting

### Tests Failing Locally

1. Clear jest cache: `npx jest --clearCache`
2. Reinstall dependencies: `rm -rf node_modules && npm install`
3. Update snapshots: `npm test -- -u`

### E2E Tests Failing

1. Update browsers: `npm run playwright:install`
2. Check server is running: Ensure dev server is available
3. Increase timeout: Add `timeout` in playwright.config.ts

### Coverage Not Meeting Threshold

1. Identify uncovered code: Check coverage report
2. Add missing tests
3. Update thresholds if appropriate

## Contributing

When adding new features:

1. Write tests first (TDD approach)
2. Ensure tests pass: `npm run test:all`
3. Check coverage: `npm run test:coverage`
4. Add E2E tests for user workflows
5. Include accessibility tests

---

**Questions?** Check the main project README or open an issue.

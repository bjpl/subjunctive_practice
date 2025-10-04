# Testing Quick Reference Guide

## Quick Start

```bash
# Install dependencies (if not already done)
npm install

# Install Playwright browsers
npm run playwright:install

# Run all tests
npm run test:all
```

## Common Commands

### Jest (Unit/Integration/A11y)

```bash
npm test                    # Run all Jest tests
npm run test:watch         # Run in watch mode
npm run test:coverage      # Run with coverage
npm run test:unit          # Unit tests only
npm run test:integration   # Integration tests only
npm run test:a11y          # Accessibility tests only
```

### Playwright (E2E)

```bash
npm run test:e2e           # Run all E2E tests
npm run test:e2e:ui        # Interactive UI mode
npm run test:e2e:headed    # See browser actions
npm run test:e2e:debug     # Debug mode
```

## Test File Locations

| Type | Location | Count |
|------|----------|-------|
| Unit Tests | `tests/unit/` | 5 files (45+ tests) |
| Integration Tests | `tests/integration/` | 3 files (25+ tests) |
| E2E Tests | `tests/e2e/` | 5 files (18+ scenarios) |
| Accessibility Tests | `tests/accessibility/` | 3 files (15+ tests) |
| **Total** | | **16 files, 103+ tests** |

## Test Categories

### UI Components (`tests/unit/components/ui/`)
- `Button.test.tsx` - 18 tests
- `Input.test.tsx` - 13 tests
- `Card.test.tsx` - 9 tests
- `Label.test.tsx` - 4 tests
- `Alert.test.tsx` - 4 tests

### Utils (`tests/unit/lib/`)
- `utils.test.ts` - 6 tests

### Redux Store (`tests/integration/store/`)
- `auth-slice.test.ts` - 15 tests

### Hooks (`tests/integration/hooks/`)
- `use-redux.test.tsx` - 5 tests
- `use-toast.test.tsx` - 5 tests

### E2E Scenarios (`tests/e2e/`)
- `auth.spec.ts` - Authentication flows (10 scenarios)
- `practice.spec.ts` - Practice sessions (17 scenarios)
- `dashboard.spec.ts` - Dashboard features (13 scenarios)
- `settings.spec.ts` - Settings management (8 scenarios)
- `responsive.spec.ts` - Responsive design (8 scenarios)

### Accessibility (`tests/accessibility/`)
- `components.a11y.test.tsx` - Component accessibility (8 tests)
- `keyboard-navigation.test.tsx` - Keyboard navigation (9 tests)
- `aria-labels.test.tsx` - ARIA compliance (9 tests)

## Coverage Targets

| Metric | Target | Current |
|--------|--------|---------|
| Branches | 70% | Run `npm run test:coverage` |
| Functions | 70% | Run `npm run test:coverage` |
| Lines | 70% | Run `npm run test:coverage` |
| Statements | 70% | Run `npm run test:coverage` |

## Writing New Tests

### 1. Component Test Template

```typescript
import { render, screen } from '@testing-library/react';
import { ComponentName } from '@/components/ComponentName';

describe('ComponentName', () => {
  it('should render correctly', () => {
    render(<ComponentName />);
    expect(screen.getByText('Expected Text')).toBeInTheDocument();
  });
});
```

### 2. Integration Test Template

```typescript
import { renderWithProviders } from '../utils/test-utils';
import { YourComponent } from '@/components/YourComponent';

describe('Integration Test', () => {
  it('should work with Redux', () => {
    const { store } = renderWithProviders(<YourComponent />);
    // Test component with store
  });
});
```

### 3. E2E Test Template

```typescript
import { test, expect } from '@playwright/test';

test.describe('Feature Name', () => {
  test('should do something', async ({ page }) => {
    await page.goto('/path');
    await page.click('button');
    await expect(page).toHaveURL(/expected-path/);
  });
});
```

### 4. Accessibility Test Template

```typescript
import { axe } from 'jest-axe';

describe('Accessibility', () => {
  it('should have no violations', async () => {
    const { container } = render(<Component />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

## Mock Service Worker (MSW)

### Using Existing Mocks

Mocks are automatically loaded from `tests/mocks/handlers.ts`.

Available endpoints:
- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/exercises`
- `POST /api/exercises/:id/submit`
- `GET /api/progress/stats`
- `GET /api/progress/history`
- `GET /api/progress/weak-areas`
- `GET /api/settings`
- `PATCH /api/settings`

### Override in Test

```typescript
import { server } from '../mocks/server';
import { http, HttpResponse } from 'msw';

test('error handling', async () => {
  server.use(
    http.get('/api/endpoint', () => {
      return HttpResponse.json({ error: 'Error' }, { status: 500 });
    })
  );
  // Test error scenario
});
```

## Debugging

### Jest Tests

```bash
# Debug specific test
node --inspect-brk node_modules/.bin/jest tests/unit/Button.test.tsx

# Run only one test
npm test -- -t "test name"

# Clear cache
npx jest --clearCache
```

### Playwright Tests

```bash
# Debug mode (pauses at breakpoints)
npm run test:e2e:debug

# Run specific file
npx playwright test tests/e2e/auth.spec.ts

# Run specific test
npx playwright test -g "user can login"

# Generate trace
npx playwright test --trace on
```

## CI/CD Integration

### GitHub Actions

```yaml
- name: Install Dependencies
  run: npm ci

- name: Install Playwright
  run: npm run playwright:install

- name: Run Tests
  run: npm run test:all

- name: Upload Coverage
  uses: codecov/codecov-action@v3
```

## Common Issues

### Issue: Tests pass locally but fail in CI
**Solution:** Ensure all dependencies are installed, check Node version

### Issue: MSW not mocking requests
**Solution:** Import `server` in jest.setup.js, check handler URLs

### Issue: Playwright tests timeout
**Solution:** Increase timeout in playwright.config.ts, check server is running

### Issue: Coverage not meeting threshold
**Solution:** Add tests for uncovered code, check coverage report

## Best Practices

1. **Test user behavior, not implementation**
2. **Use semantic queries** (`getByRole`, `getByLabelText`)
3. **Mock external dependencies** (API calls, timers)
4. **Keep tests isolated** (no shared state)
5. **Write descriptive test names**
6. **Include accessibility tests**
7. **Test edge cases and errors**
8. **Maintain realistic mock data**

## Resources

- Full Documentation: `tests/README.md`
- Test Utilities: `tests/utils/test-utils.tsx`
- Mock Handlers: `tests/mocks/handlers.ts`
- Jest Config: `jest.config.js`
- Playwright Config: `playwright.config.ts`

---

**Need Help?** Check `tests/README.md` or create an issue.

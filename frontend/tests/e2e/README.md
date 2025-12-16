# E2E Tests Documentation

This directory contains End-to-End (E2E) tests for the Subjunctive Practice application using Playwright.

## Directory Structure

```
tests/e2e/
├── accessibility.spec.ts     # Accessibility and ARIA tests
├── auth.spec.ts              # Authentication flow tests
├── dashboard.spec.ts         # Dashboard page tests
├── practice.spec.ts          # Practice session tests
├── responsive.spec.ts        # Responsive design tests
├── review.spec.ts            # Review page tests
├── settings.spec.ts          # Settings page tests
├── fixtures/                 # Reusable test fixtures
│   └── authenticated.ts      # Authenticated session fixture
└── utils/                    # Test utilities
    ├── auth-helpers.ts       # Authentication helper functions
    ├── test-data.ts          # Test data and constants
    ├── accessibility-helpers.ts  # Accessibility testing helpers
    ├── page-objects/         # Page Object Models
    │   ├── LoginPage.ts
    │   ├── DashboardPage.ts
    │   ├── PracticePage.ts
    │   └── index.ts
    └── index.ts
```

## Running Tests

### All Tests
```bash
npm run test:e2e
```

### Headed Mode (see browser)
```bash
npm run test:e2e:headed
```

### Debug Mode
```bash
npm run test:e2e:debug
```

### UI Mode (interactive)
```bash
npm run test:e2e:ui
```

### Specific Browser
```bash
npx playwright test --project=chromium
npx playwright test --project=firefox
npx playwright test --project=webkit
```

### Specific Test File
```bash
npx playwright test auth.spec.ts
npx playwright test accessibility.spec.ts
```

### Specific Test
```bash
npx playwright test -g "should successfully login"
```

## Test Utilities

### Authentication Helpers

Located in `utils/auth-helpers.ts`:

```typescript
import { loginAsTestUser, logout, registerUniqueUser } from './utils/auth-helpers';

// Login with test credentials
await loginAsTestUser(page);

// Logout
await logout(page);

// Register a new unique user
const user = await registerUniqueUser(page);
```

### Test Data

Located in `utils/test-data.ts`:

```typescript
import { testUsers, practiceSettings, routes } from './utils/test-data';

// Use predefined test users
await login(page, testUsers.default.email, testUsers.default.password);

// Use practice settings
await practicePage.startPracticeWithSettings(practiceSettings.quick);

// Navigate to routes
await page.goto(routes.dashboard);
```

### Page Objects

Located in `utils/page-objects/`:

```typescript
import { LoginPage, DashboardPage, PracticePage } from './utils/page-objects';

// Using LoginPage
const loginPage = new LoginPage(page);
await loginPage.goto();
await loginPage.login(email, password);

// Using DashboardPage
const dashboardPage = new DashboardPage(page);
await dashboardPage.goto();
const accuracy = await dashboardPage.getAccuracy();

// Using PracticePage
const practicePage = new PracticePage(page);
await practicePage.goto();
await practicePage.startPracticeWithSettings({ difficulty: 'intermediate', count: 5 });
```

### Fixtures

Located in `fixtures/authenticated.ts`:

```typescript
import { test, expect } from './fixtures/authenticated';

test.describe('Protected Routes', () => {
  // This test automatically runs with an authenticated session
  test('should access dashboard', async ({ authenticatedPage, page, dashboardPage }) => {
    await dashboardPage.goto();
    await dashboardPage.expectOnDashboard();
  });

  // Use page objects directly from fixtures
  test('should start practice', async ({ authenticatedPage, practicePage }) => {
    await practicePage.goto();
    await practicePage.startPractice();
  });
});
```

## Accessibility Testing

The `accessibility.spec.ts` file contains comprehensive accessibility tests:

- Keyboard navigation
- Screen reader support (ARIA labels, roles)
- Skip links
- Focus management
- Color contrast checks
- Form accessibility
- Semantic HTML
- Mobile accessibility
- Reduced motion support

### Running Accessibility Tests Only

```bash
npx playwright test accessibility.spec.ts
```

## Best Practices

### 1. Use Page Objects

```typescript
// ✅ Good - Using page object
const loginPage = new LoginPage(page);
await loginPage.login(email, password);

// ❌ Bad - Direct interaction
await page.fill('input[name="email"]', email);
await page.fill('input[name="password"]', password);
await page.click('button[type="submit"]');
```

### 2. Use Test Data

```typescript
// ✅ Good - Using test data
await loginPage.login(testUsers.default.email, testUsers.default.password);

// ❌ Bad - Hardcoded values
await loginPage.login('test@example.com', 'Password123!');
```

### 3. Use Helper Functions

```typescript
// ✅ Good - Using helper
await loginAsTestUser(page);

// ❌ Bad - Manual login in every test
await page.goto('/auth/login');
await page.fill('input[name="email"]', 'test@example.com');
// ... more code
```

### 4. Use Fixtures for Common Setup

```typescript
// ✅ Good - Using fixture
import { test } from './fixtures/authenticated';

test('my test', async ({ authenticatedPage, dashboardPage }) => {
  // Already logged in!
  await dashboardPage.goto();
});

// ❌ Bad - Manual setup in every test
test('my test', async ({ page }) => {
  await loginAsTestUser(page);
  await page.goto('/dashboard');
});
```

### 5. Use Meaningful Test IDs

Always prefer `data-testid` over complex selectors:

```typescript
// ✅ Good
await page.getByTestId('user-menu').click();

// ❌ Bad
await page.click('div.header > nav > div:nth-child(3) > button');
```

## Debugging Tests

### Visual Debugging

```bash
# Run tests in headed mode
npm run test:e2e:headed

# Run in debug mode with Playwright Inspector
npm run test:e2e:debug
```

### Screenshots and Videos

Tests automatically capture:
- Screenshots on failure
- Videos on retry
- Traces on first retry

Find them in:
- `test-results/` - Individual test artifacts
- `playwright-report/` - HTML report with all artifacts

### View Test Report

```bash
npx playwright show-report
```

## CI/CD Integration

The tests are configured for CI/CD:

- Retry failed tests 2 times
- Run tests serially in CI (workers: 1)
- Generate JUnit XML report for CI integration
- Generate JSON report for programmatic access

### Environment Variables

```bash
# Set base URL
PLAYWRIGHT_BASE_URL=http://localhost:3000

# Enable CI mode
CI=true
```

## Common Patterns

### Waiting for Elements

```typescript
// Wait for element to be visible
await page.waitForSelector('[data-testid="exercise-card"]');

// Wait for URL change
await page.waitForURL(/.*dashboard/);

// Wait for condition
await page.waitForFunction(() => localStorage.getItem('token') !== null);
```

### Working with Multiple Elements

```typescript
// Get all elements
const buttons = await page.locator('button').all();

// Iterate through elements
for (const button of buttons) {
  const text = await button.textContent();
  console.log(text);
}
```

### Testing Forms

```typescript
// Fill and submit
await page.fill('input[name="email"]', email);
await page.fill('input[name="password"]', password);
await page.click('button[type="submit"]');

// Check validation
await expect(page.getByText(/email.*required/i)).toBeVisible();
```

## Troubleshooting

### Tests Timing Out

Increase timeout in `playwright.config.ts`:

```typescript
timeout: 60 * 1000, // 60 seconds
```

### Flaky Tests

1. Add explicit waits
2. Use `waitForLoadState('networkidle')`
3. Increase retry count
4. Use `test.only()` to isolate

### Element Not Found

1. Check test-id exists in component
2. Wait for element to appear
3. Check if element is in viewport
4. Verify element is not hidden by CSS

## Contributing

When adding new tests:

1. Follow existing patterns
2. Use page objects for new pages
3. Add test data to `test-data.ts`
4. Document complex test scenarios
5. Ensure tests are independent
6. Clean up test data after tests

## Resources

- [Playwright Documentation](https://playwright.dev)
- [Best Practices](https://playwright.dev/docs/best-practices)
- [Selectors](https://playwright.dev/docs/selectors)
- [Assertions](https://playwright.dev/docs/test-assertions)

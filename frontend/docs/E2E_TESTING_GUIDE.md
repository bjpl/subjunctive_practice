# E2E Testing Guide

## Overview

This document provides a comprehensive guide to the Playwright E2E testing setup for the Subjunctive Practice application.

## Setup Complete ✅

The following components have been set up and configured:

### 1. Configuration Files

- ✅ **playwright.config.ts** - Enhanced with:
  - Timeout settings (30s per test, 10s for assertions)
  - Multiple reporters (HTML, JSON, JUnit, List)
  - Screenshot and video capture on failure
  - Browser matrix (Chromium, Firefox, WebKit, Mobile)
  - Dev server auto-start

### 2. Test Files (8 total)

- ✅ **auth.spec.ts** - Authentication flows (login, register, logout, protected routes)
- ✅ **dashboard.spec.ts** - Dashboard functionality (stats, charts, achievements)
- ✅ **practice.spec.ts** - Practice sessions (setup, exercises, completion)
- ✅ **accessibility.spec.ts** - **NEW** Comprehensive accessibility tests
- ✅ **responsive.spec.ts** - Responsive design tests
- ✅ **settings.spec.ts** - Settings page tests
- ✅ **review.spec.ts** - Review functionality tests
- ✅ **example-with-fixtures.spec.ts** - **NEW** Example demonstrating best practices

### 3. Test Utilities

#### Authentication Helpers (`utils/auth-helpers.ts`)
- `login(page, email, password)` - Login with credentials
- `loginAsTestUser(page)` - Login with default test user
- `register(page, email, username, password)` - Register new user
- `registerUniqueUser(page)` - Register with unique credentials
- `logout(page)` - Logout current user
- `isAuthenticated(page)` - Check authentication status
- `setupAuthenticatedSession(page)` - Setup for beforeEach hooks
- `clearAuth(page)` - Clear all auth data

#### Test Data (`utils/test-data.ts`)
- `testUsers` - Predefined test users
- `testExercises` - Sample exercise data
- `practiceSettings` - Practice configuration presets
- `userProgress` - Sample progress data
- `achievements` - Achievement definitions
- `mockSessionResults` - Session result data
- `errorMessages` - Expected error messages
- `routes` - Application routes
- Helper functions: `generateUniqueEmail()`, `createUniqueTestUser()`

#### Accessibility Helpers (`utils/accessibility-helpers.ts`)
- `hasAccessibleName(element)` - Check ARIA labels
- `checkHeadingHierarchy(page)` - Validate heading structure
- `checkForKeyboardTrap(page)` - Detect focus traps
- `isInTabOrder(element)` - Check tab navigation
- `checkColorContrast(element)` - Verify contrast ratios
- `getInteractiveElements(page)` - Find all interactive elements
- `hasSkipLinks(page)` - Check for skip navigation
- `checkFormLabels(page)` - Validate form accessibility
- `hasLiveRegion(page)` - Find ARIA live regions
- `modalTrapsFocus(page)` - Check modal focus management
- `hasFocusIndicator(element)` - Verify focus visibility
- `getLandmarks(page)` - Find semantic landmarks
- `checkTouchTargetSize(element)` - Validate touch targets (mobile)

### 4. Page Object Models

#### LoginPage (`utils/page-objects/LoginPage.ts`)
```typescript
const loginPage = new LoginPage(page);
await loginPage.goto();
await loginPage.login(email, password);
await loginPage.expectError(/invalid credentials/i);
```

Methods:
- `goto()` - Navigate to login page
- `login(email, password)` - Fill and submit login form
- `loginAndWait(email, password)` - Login and wait for redirect
- `togglePasswordVisibility()` - Show/hide password
- `isPasswordVisible()` - Check password visibility
- `getErrorMessage()` - Get current error message
- `expectError(message)` - Assert error is shown
- `expectOnLoginPage()` - Verify on login page
- `goToRegister()` - Navigate to registration

#### DashboardPage (`utils/page-objects/DashboardPage.ts`)
```typescript
const dashboardPage = new DashboardPage(page);
await dashboardPage.goto();
await dashboardPage.expectStatsVisible();
const accuracy = await dashboardPage.getAccuracy();
```

Methods:
- `goto()` - Navigate to dashboard
- `expectOnDashboard()` - Verify on dashboard
- `expectStatsVisible()` - Check stats are displayed
- `getTotalExercises()` - Get exercise count
- `getAccuracy()` - Get accuracy percentage
- `getCurrentStreak()` - Get streak count
- `getTotalPoints()` - Get total points
- `switchChartPeriod(period)` - Change chart timeframe
- `getWeakAreas()` - Get list of weak areas
- `practiceWeakArea(index)` - Start practice for weak area
- `getUnlockedAchievements()` - Count achievements
- `clickAchievement(index)` - Open achievement details
- `startPractice()` - Navigate to practice
- `viewProgress()` - Navigate to progress
- `logout()` - Logout user

#### PracticePage (`utils/page-objects/PracticePage.ts`)
```typescript
const practicePage = new PracticePage(page);
await practicePage.goto();
await practicePage.startPracticeWithSettings({
  difficulty: 'intermediate',
  count: 5
});
await practicePage.submitAnswer('hable');
```

Methods:
- `goto()` - Navigate to practice
- `expectOnPracticePage()` - Verify on practice page
- `selectDifficulty(level)` - Choose difficulty
- `selectTense(tense)` - Choose tense
- `setExerciseCount(count)` - Set number of exercises
- `startPractice()` - Begin practice session
- `startPracticeWithSettings(options)` - Start with config
- `submitAnswer(answer)` - Submit answer
- `submitAnswerWithEnter(answer)` - Submit with Enter key
- `skipExercise()` - Skip current exercise
- `goToNext()` - Move to next exercise
- `pauseSession()` - Pause practice
- `resumeSession()` - Resume practice
- `quitSession(confirm)` - Quit session
- `expectCorrectFeedback()` - Verify correct answer UI
- `expectIncorrectFeedback()` - Verify incorrect answer UI
- `getCurrentProgress()` - Get current/total exercises
- `getProgressPercentage()` - Get progress bar value
- `completeExercise(answer)` - Submit and move next
- `completeSession(answers)` - Complete full session
- `expectSessionComplete()` - Verify results shown
- `getFinalAccuracy()` - Get final accuracy
- `getFinalPoints()` - Get final points
- `startNewSession()` - Begin another session

### 5. Fixtures

#### Authenticated Fixture (`fixtures/authenticated.ts`)
```typescript
import { test, expect } from './fixtures/authenticated';

test('my test', async ({ authenticatedPage, dashboardPage }) => {
  // Already logged in!
  await dashboardPage.goto();
  await dashboardPage.expectOnDashboard();
});
```

Available fixtures:
- `authenticatedPage` - Auto-login before test
- `loginPage` - LoginPage instance
- `dashboardPage` - DashboardPage instance
- `practicePage` - PracticePage instance

### 6. Documentation

- ✅ **tests/e2e/README.md** - Comprehensive E2E testing guide
- ✅ **docs/E2E_TESTING_GUIDE.md** - This document

## Running Tests

### Installation

```bash
# Install Playwright browsers (one-time setup)
npm run playwright:install
```

### Basic Commands

```bash
# Run all E2E tests
npm run test:e2e

# Run with visible browser
npm run test:e2e:headed

# Interactive UI mode
npm run test:e2e:ui

# Debug mode with inspector
npm run test:e2e:debug

# Run all tests (unit + E2E)
npm run test:all
```

### Advanced Commands

```bash
# Run specific browser
npx playwright test --project=chromium
npx playwright test --project=firefox
npx playwright test --project=webkit

# Run specific file
npx playwright test auth.spec.ts
npx playwright test accessibility.spec.ts

# Run specific test
npx playwright test -g "should login successfully"

# Run in parallel
npx playwright test --workers=4

# Run in serial (one at a time)
npx playwright test --workers=1

# Update snapshots
npx playwright test --update-snapshots
```

### Reports

```bash
# View HTML report
npx playwright show-report

# Generated reports:
# - playwright-report/index.html (HTML)
# - playwright-report/results.json (JSON)
# - playwright-report/results.xml (JUnit)
```

## Test Examples

### Example 1: Basic Login Test

```typescript
import { test, expect } from '@playwright/test';
import { LoginPage } from './utils/page-objects';
import { testUsers } from './utils/test-data';

test('should login successfully', async ({ page }) => {
  const loginPage = new LoginPage(page);

  await loginPage.goto();
  await loginPage.login(testUsers.default.email, testUsers.default.password);

  await expect(page).toHaveURL(/.*dashboard/);
});
```

### Example 2: Using Authenticated Fixture

```typescript
import { test, expect } from './fixtures/authenticated';

test('should view dashboard stats', async ({ authenticatedPage, dashboardPage }) => {
  await dashboardPage.goto();

  const accuracy = await dashboardPage.getAccuracy();
  expect(accuracy).toBeGreaterThanOrEqual(0);
  expect(accuracy).toBeLessThanOrEqual(100);
});
```

### Example 3: Complete Practice Session

```typescript
import { test } from './fixtures/authenticated';

test('should complete practice session', async ({ authenticatedPage, practicePage }) => {
  await practicePage.goto();

  await practicePage.startPracticeWithSettings({
    difficulty: 'beginner',
    count: 3,
  });

  // Complete exercises
  const answers = ['hable', 'comas', 'viva'];
  await practicePage.completeSession(answers);

  // Verify results
  await practicePage.expectSessionComplete();

  const points = await practicePage.getFinalPoints();
  expect(points).toBeGreaterThan(0);
});
```

### Example 4: Accessibility Test

```typescript
import { test, expect } from '@playwright/test';
import { checkHeadingHierarchy } from './utils/accessibility-helpers';
import { loginAsTestUser } from './utils/auth-helpers';

test('should have proper heading hierarchy', async ({ page }) => {
  await loginAsTestUser(page);

  const result = await checkHeadingHierarchy(page);

  expect(result.valid).toBeTruthy();
  if (!result.valid) {
    console.log('Heading errors:', result.errors);
  }
});
```

## Best Practices

### 1. Always Use Page Objects

✅ **DO:**
```typescript
const loginPage = new LoginPage(page);
await loginPage.login(email, password);
```

❌ **DON'T:**
```typescript
await page.fill('input[name="email"]', email);
await page.click('button[type="submit"]');
```

### 2. Use Test Data Constants

✅ **DO:**
```typescript
import { testUsers } from './utils/test-data';
await loginPage.login(testUsers.default.email, testUsers.default.password);
```

❌ **DON'T:**
```typescript
await loginPage.login('test@example.com', 'password123');
```

### 3. Use Fixtures for Common Setup

✅ **DO:**
```typescript
import { test } from './fixtures/authenticated';

test('my test', async ({ authenticatedPage, dashboardPage }) => {
  // Already authenticated!
});
```

❌ **DON'T:**
```typescript
test.beforeEach(async ({ page }) => {
  await loginAsTestUser(page);
});
```

### 4. Use Semantic Selectors

✅ **DO:**
```typescript
await page.getByTestId('user-menu').click();
await page.getByRole('button', { name: 'Submit' }).click();
```

❌ **DON'T:**
```typescript
await page.click('div > nav > button:nth-child(3)');
```

### 5. Add Meaningful Assertions

✅ **DO:**
```typescript
await expect(page.getByTestId('error')).toContainText('Invalid credentials');
```

❌ **DON'T:**
```typescript
await page.waitForSelector('[role="alert"]');
// No assertion!
```

## Accessibility Testing

The E2E suite includes comprehensive accessibility tests covering:

### Keyboard Navigation
- ✅ Tab order through forms
- ✅ Arrow key navigation in menus
- ✅ Enter/Space for activation
- ✅ Escape to close modals
- ✅ Focus management on route changes

### Screen Reader Support
- ✅ ARIA labels on inputs
- ✅ Form validation announcements
- ✅ Heading hierarchy (h1-h6)
- ✅ Descriptive button labels
- ✅ Progress announcements
- ✅ Feedback announcements

### Focus Management
- ✅ Visible focus indicators
- ✅ Focus trap in modals
- ✅ Focus restoration after modal close
- ✅ Skip links

### Semantic HTML
- ✅ Landmark regions (main, nav, header)
- ✅ Proper list structures
- ✅ Form labels associated with inputs
- ✅ Required field indicators

### Mobile Accessibility
- ✅ Touch target sizes (44x44px minimum)
- ✅ Landscape orientation support
- ✅ Reduced motion support

## CI/CD Integration

### GitHub Actions Example

```yaml
name: E2E Tests

on: [push, pull_request]

jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps

      - name: Run E2E tests
        run: npm run test:e2e
        env:
          CI: true

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: playwright-report/
```

## Troubleshooting

### Tests Timeout

**Problem:** Tests hang or timeout

**Solutions:**
1. Increase timeout in config
2. Add explicit waits: `await page.waitForSelector()`
3. Check network requests: `await page.waitForLoadState('networkidle')`
4. Use `test.slow()` for known slow tests

### Flaky Tests

**Problem:** Tests fail intermittently

**Solutions:**
1. Add retry logic: `test.describe.configure({ retries: 2 })`
2. Wait for animations: `await page.waitForTimeout(300)`
3. Use auto-waiting: `await expect(element).toBeVisible()`
4. Check for race conditions

### Element Not Found

**Problem:** `Element not found` errors

**Solutions:**
1. Verify `data-testid` exists in component
2. Wait for element: `await element.waitFor()`
3. Check visibility: `await element.isVisible()`
4. Scroll into view: `await element.scrollIntoViewIfNeeded()`

### Authentication Issues

**Problem:** Tests can't authenticate

**Solutions:**
1. Check test user exists in database
2. Clear storage: `await clearAuth(page)`
3. Verify API is running: `curl http://localhost:3000/api/health`
4. Check network tab in headed mode

## File Structure Summary

```
frontend/
├── playwright.config.ts          # Enhanced configuration
├── package.json                  # Scripts defined
├── docs/
│   └── E2E_TESTING_GUIDE.md     # This guide
└── tests/
    └── e2e/
        ├── README.md             # Quick reference
        ├── *.spec.ts             # Test files (8)
        ├── fixtures/
        │   └── authenticated.ts  # Test fixtures
        └── utils/
            ├── auth-helpers.ts       # Auth utilities
            ├── test-data.ts          # Test data
            ├── accessibility-helpers.ts  # A11y utilities
            ├── index.ts              # Exports
            └── page-objects/
                ├── LoginPage.ts
                ├── DashboardPage.ts
                ├── PracticePage.ts
                └── index.ts
```

## NPM Scripts Summary

```json
{
  "test:e2e": "playwright test",
  "test:e2e:ui": "playwright test --ui",
  "test:e2e:headed": "playwright test --headed",
  "test:e2e:debug": "playwright test --debug",
  "test:all": "npm run test:coverage && npm run test:e2e",
  "playwright:install": "playwright install"
}
```

## Next Steps

1. ✅ Run `npm run playwright:install` to install browsers
2. ✅ Run `npm run test:e2e` to execute tests
3. ✅ Review test results in `playwright-report/`
4. ✅ Add custom tests following the patterns
5. ✅ Integrate into CI/CD pipeline

## Resources

- [Playwright Documentation](https://playwright.dev)
- [Test Generator](https://playwright.dev/docs/codegen)
- [Trace Viewer](https://playwright.dev/docs/trace-viewer)
- [Best Practices](https://playwright.dev/docs/best-practices)
- [Accessibility Testing](https://playwright.dev/docs/accessibility-testing)

## Support

For questions or issues:
1. Check the [tests/e2e/README.md](../tests/e2e/README.md)
2. Review example tests in `example-with-fixtures.spec.ts`
3. Consult Playwright documentation
4. Review test output and traces

---

**Last Updated:** December 2024
**Playwright Version:** 1.55.1
**Status:** ✅ Complete and Ready

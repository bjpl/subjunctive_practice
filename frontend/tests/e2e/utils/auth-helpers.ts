import { Page, expect } from '@playwright/test';

/**
 * Authentication helper functions for E2E tests
 */

export interface TestUser {
  email: string;
  username: string;
  password: string;
}

/**
 * Login with credentials
 */
export async function login(page: Page, email: string, password: string): Promise<void> {
  await page.goto('/auth/login');
  await page.fill('input[name="email"]', email);
  await page.fill('input[name="password"]', password);
  await page.click('button[type="submit"]');

  // Wait for redirect to dashboard
  await expect(page).toHaveURL(/.*dashboard/, { timeout: 10000 });
}

/**
 * Login with test user (default credentials)
 */
export async function loginAsTestUser(page: Page): Promise<void> {
  await login(page, 'test@example.com', 'Password123!');
}

/**
 * Register a new user
 */
export async function register(
  page: Page,
  email: string,
  username: string,
  password: string
): Promise<void> {
  await page.goto('/auth/register');
  await page.fill('input[name="email"]', email);
  await page.fill('input[name="username"]', username);
  await page.fill('input[name="password"]', password);
  await page.fill('input[name="confirmPassword"]', password);
  await page.click('button[type="submit"]');

  // Wait for successful registration
  await expect(page).toHaveURL(/.*dashboard/, { timeout: 10000 });
}

/**
 * Register a unique test user with timestamp
 */
export async function registerUniqueUser(page: Page): Promise<TestUser> {
  const timestamp = Date.now();
  const user: TestUser = {
    email: `test${timestamp}@example.com`,
    username: `user${timestamp}`,
    password: 'Password123!',
  };

  await register(page, user.email, user.username, user.password);
  return user;
}

/**
 * Logout current user
 */
export async function logout(page: Page): Promise<void> {
  // Open user menu
  await page.click('[data-testid="user-menu"]');

  // Click logout
  await page.click('text=Logout');

  // Verify redirected to login
  await expect(page).toHaveURL(/.*login/, { timeout: 5000 });
}

/**
 * Check if user is authenticated
 */
export async function isAuthenticated(page: Page): Promise<boolean> {
  try {
    // Check for user menu presence
    const userMenu = page.getByTestId('user-menu');
    await userMenu.waitFor({ state: 'visible', timeout: 3000 });
    return true;
  } catch {
    return false;
  }
}

/**
 * Navigate to a protected route and verify authentication
 */
export async function navigateToProtectedRoute(page: Page, route: string): Promise<void> {
  await page.goto(route);

  // Should either be on the route or redirected to login
  const url = page.url();
  const isOnRoute = url.includes(route);
  const isOnLogin = url.includes('/auth/login');

  expect(isOnRoute || isOnLogin).toBeTruthy();
}

/**
 * Setup authenticated session for tests
 * This can be used in test.beforeEach
 */
export async function setupAuthenticatedSession(page: Page): Promise<void> {
  await loginAsTestUser(page);

  // Verify we're logged in
  const authenticated = await isAuthenticated(page);
  expect(authenticated).toBeTruthy();
}

/**
 * Clear all authentication data
 */
export async function clearAuth(page: Page): Promise<void> {
  // Clear all cookies
  await page.context().clearCookies();

  // Clear local storage
  await page.evaluate(() => {
    localStorage.clear();
    sessionStorage.clear();
  });
}

/**
 * Wait for authentication to complete
 */
export async function waitForAuth(page: Page, timeout = 5000): Promise<void> {
  await page.waitForFunction(
    () => {
      // Check if auth token exists in localStorage
      const token = localStorage.getItem('authToken') || localStorage.getItem('token');
      return token !== null;
    },
    { timeout }
  );
}

/**
 * Get auth token from storage
 */
export async function getAuthToken(page: Page): Promise<string | null> {
  return await page.evaluate(() => {
    return localStorage.getItem('authToken') || localStorage.getItem('token');
  });
}

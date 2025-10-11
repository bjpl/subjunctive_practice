import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test.describe('User Registration', () => {
    test('should successfully register a new user', async ({ page }) => {
      await page.goto('/auth/register');

      // Fill registration form
      await page.fill('input[name="email"]', 'newuser@example.com');
      await page.fill('input[name="username"]', 'newuser');
      await page.fill('input[name="password"]', 'Password123!');
      await page.fill('input[name="confirmPassword"]', 'Password123!');

      // Submit form
      await page.click('button[type="submit"]');

      // Should redirect to dashboard after successful registration
      await expect(page).toHaveURL(/.*dashboard/);

      // Should show welcome message
      await expect(page.getByText(/welcome/i)).toBeVisible();
    });

    test('should show error for existing email', async ({ page }) => {
      await page.goto('/auth/register');

      await page.fill('input[name="email"]', 'existing@example.com');
      await page.fill('input[name="username"]', 'existing');
      await page.fill('input[name="password"]', 'Password123!');
      await page.fill('input[name="confirmPassword"]', 'Password123!');

      await page.click('button[type="submit"]');

      // Should show error message
      await expect(page.getByText(/already exists/i)).toBeVisible();

      // Should stay on registration page
      await expect(page).toHaveURL(/.*register/);
    });

    test('should validate password matching', async ({ page }) => {
      await page.goto('/auth/register');

      await page.fill('input[name="email"]', 'test@example.com');
      await page.fill('input[name="username"]', 'testuser');
      await page.fill('input[name="password"]', 'Password123!');
      await page.fill('input[name="confirmPassword"]', 'DifferentPassword!');

      await page.click('button[type="submit"]');

      // Should show password mismatch error
      await expect(page.getByText(/passwords.*match/i)).toBeVisible();
    });

    test('should validate required fields', async ({ page }) => {
      await page.goto('/auth/register');

      // Try to submit empty form
      await page.click('button[type="submit"]');

      // Should show validation errors
      await expect(page.getByText(/email.*required/i)).toBeVisible();
      await expect(page.getByText(/username.*required/i)).toBeVisible();
      await expect(page.getByText(/password.*required/i)).toBeVisible();
    });
  });

  test.describe('User Login', () => {
    test('should successfully login with valid credentials', async ({ page }) => {
      await page.goto('/auth/login');

      await page.fill('input[name="email"]', 'test@example.com');
      await page.fill('input[name="password"]', 'Password123!');

      await page.click('button[type="submit"]');

      // Should redirect to dashboard
      await expect(page).toHaveURL(/.*dashboard/);

      // Should show user menu
      await expect(page.getByTestId('user-menu')).toBeVisible();
    });

    test('should show error for invalid credentials', async ({ page }) => {
      await page.goto('/auth/login');

      await page.fill('input[name="email"]', 'wrong@example.com');
      await page.fill('input[name="password"]', 'wrongpassword');

      await page.click('button[type="submit"]');

      // Should show error message
      await expect(page.getByText(/invalid credentials/i)).toBeVisible();

      // Should stay on login page
      await expect(page).toHaveURL(/.*login/);
    });

    test('should validate required fields', async ({ page }) => {
      await page.goto('/auth/login');

      await page.click('button[type="submit"]');

      // Should show validation errors
      await expect(page.getByText(/email.*required/i)).toBeVisible();
      await expect(page.getByText(/password.*required/i)).toBeVisible();
    });

    test('should toggle password visibility', async ({ page }) => {
      await page.goto('/auth/login');

      const passwordInput = page.locator('input[name="password"]');
      const toggleButton = page.getByRole('button', { name: /show password/i });

      // Password should be hidden by default
      await expect(passwordInput).toHaveAttribute('type', 'password');

      // Click toggle to show password
      await toggleButton.click();
      await expect(passwordInput).toHaveAttribute('type', 'text');

      // Click toggle to hide password again
      await toggleButton.click();
      await expect(passwordInput).toHaveAttribute('type', 'password');
    });
  });

  test.describe('User Logout', () => {
    test('should successfully logout', async ({ page }) => {
      // Login first
      await page.goto('/auth/login');
      await page.fill('input[name="email"]', 'test@example.com');
      await page.fill('input[name="password"]', 'Password123!');
      await page.click('button[type="submit"]');

      await expect(page).toHaveURL(/.*dashboard/);

      // Logout
      await page.click('[data-testid="user-menu"]');
      await page.click('text=Logout');

      // Should redirect to login page
      await expect(page).toHaveURL(/.*login/);

      // Should not be able to access protected routes
      await page.goto('/dashboard');
      await expect(page).toHaveURL(/.*login/);
    });
  });

  test.describe('Protected Routes', () => {
    test('should redirect unauthenticated users to login', async ({ page }) => {
      await page.goto('/dashboard');
      await expect(page).toHaveURL(/.*login/);

      await page.goto('/practice');
      await expect(page).toHaveURL(/.*login/);

      await page.goto('/progress');
      await expect(page).toHaveURL(/.*login/);

      await page.goto('/settings');
      await expect(page).toHaveURL(/.*login/);
    });

    test('should allow authenticated users to access protected routes', async ({ page }) => {
      // Login first
      await page.goto('/auth/login');
      await page.fill('input[name="email"]', 'test@example.com');
      await page.fill('input[name="password"]', 'Password123!');
      await page.click('button[type="submit"]');

      // Should be able to access protected routes
      await page.goto('/dashboard');
      await expect(page).toHaveURL(/.*dashboard/);

      await page.goto('/practice');
      await expect(page).toHaveURL(/.*practice/);

      await page.goto('/progress');
      await expect(page).toHaveURL(/.*progress/);

      await page.goto('/settings');
      await expect(page).toHaveURL(/.*settings/);
    });
  });
});

import { test, expect } from '@playwright/test';

test.describe('Settings Page', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/auth/login');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'Password123!');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/.*dashboard/);

    // Navigate to settings
    await page.goto('/settings');
  });

  test.describe('Profile Settings', () => {
    test('should display current user information', async ({ page }) => {
      await expect(page.getByTestId('user-email')).toBeVisible();
      await expect(page.getByTestId('user-username')).toBeVisible();
    });

    test('should allow updating username', async ({ page }) => {
      const newUsername = 'newusername' + Date.now();

      await page.fill('input[name="username"]', newUsername);
      await page.click('button:has-text("Save Changes")');

      // Should show success message
      await expect(page.getByText(/saved successfully/i)).toBeVisible();
    });
  });

  test.describe('Practice Settings', () => {
    test('should allow changing daily goal', async ({ page }) => {
      await page.fill('input[name="dailyGoal"]', '30');
      await page.click('button:has-text("Save")');

      await expect(page.getByText(/settings updated/i)).toBeVisible();
    });

    test('should allow selecting default difficulty', async ({ page }) => {
      await page.click('[data-testid="difficulty-select"]');
      await page.click('text=Advanced');

      await page.click('button:has-text("Save")');

      await expect(page.getByText(/settings updated/i)).toBeVisible();
    });

    test('should allow selecting preferred tenses', async ({ page }) => {
      await page.click('[data-testid="tense-checkbox-present"]');
      await page.click('[data-testid="tense-checkbox-imperfect"]');

      await page.click('button:has-text("Save")');

      await expect(page.getByText(/settings updated/i)).toBeVisible();
    });
  });

  test.describe('Notification Settings', () => {
    test('should toggle notifications on/off', async ({ page }) => {
      const toggle = page.getByTestId('notifications-toggle');

      const initialState = await toggle.isChecked();

      await toggle.click();

      expect(await toggle.isChecked()).toBe(!initialState);
    });

    test('should save notification preferences', async ({ page }) => {
      await page.click('[data-testid="notifications-toggle"]');
      await page.click('button:has-text("Save")');

      await expect(page.getByText(/settings updated/i)).toBeVisible();
    });
  });

  test.describe('Theme Settings', () => {
    test('should allow switching between light and dark mode', async ({ page }) => {
      await page.click('[data-testid="theme-toggle"]');

      // Check if dark mode is applied
      const html = page.locator('html');
      const theme = await html.getAttribute('class');

      expect(theme).toContain('dark');
    });
  });

  test.describe('Data Management', () => {
    test('should show statistics export option', async ({ page }) => {
      await expect(page.getByRole('button', { name: /export data/i })).toBeVisible();
    });

    test('should confirm before resetting progress', async ({ page }) => {
      await page.click('button:has-text("Reset Progress")');

      // Should show confirmation dialog
      await expect(page.getByText(/are you sure/i)).toBeVisible();

      // Cancel reset
      await page.click('button:has-text("Cancel")');

      // Dialog should close
      await expect(page.getByText(/are you sure/i)).not.toBeVisible();
    });
  });

  test.describe('Account Management', () => {
    test('should allow changing password', async ({ page }) => {
      await page.fill('input[name="currentPassword"]', 'Password123!');
      await page.fill('input[name="newPassword"]', 'NewPassword123!');
      await page.fill('input[name="confirmPassword"]', 'NewPassword123!');

      await page.click('button:has-text("Change Password")');

      await expect(page.getByText(/password.*updated/i)).toBeVisible();
    });

    test('should validate password requirements', async ({ page }) => {
      await page.fill('input[name="currentPassword"]', 'Password123!');
      await page.fill('input[name="newPassword"]', 'weak');
      await page.fill('input[name="confirmPassword"]', 'weak');

      await page.click('button:has-text("Change Password")');

      // Should show validation error
      await expect(page.getByText(/password.*8 characters/i)).toBeVisible();
    });
  });
});

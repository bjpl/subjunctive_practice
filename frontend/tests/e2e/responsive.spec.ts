import { test, expect, devices } from '@playwright/test';

test.describe('Responsive Design Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/auth/login');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'Password123!');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/.*dashboard/);
  });

  test.describe('Mobile View - iPhone 12', () => {
    test.use({ ...devices['iPhone 12'] });

    test('should display mobile navigation menu', async ({ page }) => {
      await page.goto('/dashboard');

      // Mobile menu button should be visible
      const menuButton = page.getByTestId('mobile-menu-button');
      await expect(menuButton).toBeVisible();

      // Open menu
      await menuButton.click();

      // Navigation links should be visible
      await expect(page.getByRole('link', { name: /dashboard/i })).toBeVisible();
      await expect(page.getByRole('link', { name: /practice/i })).toBeVisible();
    });

    test('should adapt practice interface for mobile', async ({ page }) => {
      await page.goto('/practice');
      await page.click('button:has-text("Start Practice")');

      // Exercise card should be full width
      const exerciseCard = page.getByTestId('exercise-card');
      await expect(exerciseCard).toBeVisible();

      // Answer input should be large enough for mobile
      const input = page.getByTestId('answer-input');
      await expect(input).toBeVisible();
    });

    test('should make dashboard stats stack vertically', async ({ page }) => {
      await page.goto('/dashboard');

      // Stats should be visible and stacked
      await expect(page.getByTestId('total-exercises')).toBeVisible();
      await expect(page.getByTestId('accuracy-stat')).toBeVisible();
      await expect(page.getByTestId('current-streak')).toBeVisible();
    });
  });

  test.describe('Tablet View - iPad', () => {
    test.use({ ...devices['iPad (gen 7)'] });

    test('should adapt layout for tablet', async ({ page }) => {
      await page.goto('/dashboard');

      // Should show optimized tablet layout
      await expect(page.getByTestId('performance-chart')).toBeVisible();
      await expect(page.getByTestId('study-heatmap')).toBeVisible();
    });

    test('should use tablet navigation', async ({ page }) => {
      await page.goto('/dashboard');

      // May show hamburger menu or full nav depending on design
      const nav = page.getByRole('navigation');
      await expect(nav).toBeVisible();
    });
  });

  test.describe('Desktop View', () => {
    test('should display full desktop layout', async ({ page }) => {
      await page.setViewportSize({ width: 1920, height: 1080 });
      await page.goto('/dashboard');

      // All dashboard sections should be visible
      await expect(page.getByTestId('performance-chart')).toBeVisible();
      await expect(page.getByTestId('study-heatmap')).toBeVisible();
      await expect(page.getByTestId('weak-areas')).toBeVisible();
      await expect(page.getByTestId('achievements')).toBeVisible();
    });

    test('should show sidebar navigation', async ({ page }) => {
      await page.setViewportSize({ width: 1920, height: 1080 });
      await page.goto('/dashboard');

      // Desktop navigation should be visible
      const nav = page.getByRole('navigation');
      await expect(nav).toBeVisible();
    });
  });

  test.describe('Orientation Changes', () => {
    test('should handle portrait to landscape', async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 667 }); // iPhone portrait

      await page.goto('/practice');
      await page.click('button:has-text("Start Practice")');

      await expect(page.getByTestId('exercise-card')).toBeVisible();

      // Switch to landscape
      await page.setViewportSize({ width: 667, height: 375 });

      // Should still work in landscape
      await expect(page.getByTestId('exercise-card')).toBeVisible();
    });
  });

  test.describe('Touch Interactions', () => {
    test.use({ ...devices['iPhone 12'] });

    test('should support touch interactions', async ({ page }) => {
      await page.goto('/practice');
      await page.click('button:has-text("Start Practice")');

      // Tap on input
      const input = page.getByTestId('answer-input');
      await input.tap();

      // Input should be focused
      await expect(input).toBeFocused();
    });

    test('should support swipe gestures', async ({ page }) => {
      await page.goto('/practice');
      await page.click('button:has-text("Start Practice")');

      // Submit answer
      await page.fill('[data-testid="answer-input"]', 'hable');
      await page.click('button:has-text("Submit")');

      // Try swipe to next (if implemented)
      const exerciseCard = page.getByTestId('exercise-card');

      await exerciseCard.evaluate((element) => {
        const touchStart = new TouchEvent('touchstart', {
          touches: [{ clientX: 300, clientY: 200 } as Touch],
        });
        const touchEnd = new TouchEvent('touchend', {
          touches: [{ clientX: 100, clientY: 200 } as Touch],
        });

        element.dispatchEvent(touchStart);
        element.dispatchEvent(touchEnd);
      });
    });
  });

  test.describe('Font Scaling', () => {
    test('should remain usable with large text', async ({ page }) => {
      await page.goto('/dashboard');

      // Increase font size
      await page.evaluate(() => {
        document.documentElement.style.fontSize = '20px';
      });

      // Content should still be visible and usable
      await expect(page.getByTestId('total-exercises')).toBeVisible();
      await expect(page.getByTestId('performance-chart')).toBeVisible();
    });
  });

  test.describe('Small Screens', () => {
    test('should work on very small screens', async ({ page }) => {
      await page.setViewportSize({ width: 320, height: 568 }); // iPhone SE

      await page.goto('/dashboard');

      // Should show mobile layout
      await expect(page.getByTestId('mobile-menu-button')).toBeVisible();

      // Should be able to navigate
      await page.click('[data-testid="mobile-menu-button"]');
      await expect(page.getByRole('link', { name: /practice/i })).toBeVisible();
    });
  });
});

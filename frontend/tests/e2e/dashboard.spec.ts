import { test, expect } from '@playwright/test';

test.describe('Dashboard', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/auth/login');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'Password123!');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/.*dashboard/);
  });

  test.describe('Overview Statistics', () => {
    test('should display user statistics', async ({ page }) => {
      await expect(page.getByTestId('total-exercises')).toBeVisible();
      await expect(page.getByTestId('accuracy-stat')).toBeVisible();
      await expect(page.getByTestId('current-streak')).toBeVisible();
      await expect(page.getByTestId('total-points')).toBeVisible();
    });

    test('should show correct statistics values', async ({ page }) => {
      // Check that stats contain numbers
      const totalExercises = page.getByTestId('total-exercises');
      await expect(totalExercises).toContainText(/\d+/);

      const accuracy = page.getByTestId('accuracy-stat');
      await expect(accuracy).toContainText(/\d+%/);

      const streak = page.getByTestId('current-streak');
      await expect(streak).toContainText(/\d+/);
    });

    test('should display progress level', async ({ page }) => {
      await expect(page.getByTestId('user-level')).toBeVisible();
      await expect(page.getByTestId('level-progress')).toBeVisible();
    });
  });

  test.describe('Performance Chart', () => {
    test('should display performance chart', async ({ page }) => {
      await expect(page.getByTestId('performance-chart')).toBeVisible();
    });

    test('should allow switching chart time periods', async ({ page }) => {
      // Switch to weekly view
      await page.click('[data-testid="chart-period-week"]');
      await expect(page.getByTestId('performance-chart')).toBeVisible();

      // Switch to monthly view
      await page.click('[data-testid="chart-period-month"]');
      await expect(page.getByTestId('performance-chart')).toBeVisible();

      // Switch to all-time view
      await page.click('[data-testid="chart-period-all"]');
      await expect(page.getByTestId('performance-chart')).toBeVisible();
    });

    test('should show chart tooltips on hover', async ({ page }) => {
      const chart = page.getByTestId('performance-chart');

      // Hover over chart element
      await chart.hover();

      // Tooltip should appear (implementation dependent)
      // This is a basic check - adjust based on actual implementation
      await expect(page.locator('[role="tooltip"]').first()).toBeVisible({ timeout: 5000 });
    });
  });

  test.describe('Study Heatmap', () => {
    test('should display study heatmap', async ({ page }) => {
      await expect(page.getByTestId('study-heatmap')).toBeVisible();
    });

    test('should show activity for different days', async ({ page }) => {
      const heatmap = page.getByTestId('study-heatmap');

      // Should contain calendar cells
      const cells = heatmap.locator('[data-cell]');
      await expect(cells.first()).toBeVisible();
    });

    test('should show day details on hover', async ({ page }) => {
      const heatmap = page.getByTestId('study-heatmap');
      const firstCell = heatmap.locator('[data-cell]').first();

      await firstCell.hover();

      // Should show tooltip with day details
      await expect(page.getByTestId('heatmap-tooltip')).toBeVisible({ timeout: 3000 });
    });
  });

  test.describe('Weak Areas Analysis', () => {
    test('should display weak areas section', async ({ page }) => {
      await expect(page.getByTestId('weak-areas')).toBeVisible();
    });

    test('should show specific weak tenses', async ({ page }) => {
      const weakAreas = page.getByTestId('weak-areas');

      // Should list weak areas
      await expect(weakAreas.getByTestId('weak-area-item').first()).toBeVisible();
    });

    test('should provide practice link for weak areas', async ({ page }) => {
      const weakAreas = page.getByTestId('weak-areas');
      const practiceButton = weakAreas.getByRole('button', { name: /practice/i }).first();

      await expect(practiceButton).toBeVisible();

      // Click should navigate to practice with filters
      await practiceButton.click();
      await expect(page).toHaveURL(/.*practice/);
    });
  });

  test.describe('Achievements', () => {
    test('should display achievements section', async ({ page }) => {
      await expect(page.getByTestId('achievements')).toBeVisible();
    });

    test('should show unlocked achievements', async ({ page }) => {
      const achievements = page.getByTestId('achievements');
      const unlockedBadges = achievements.locator('[data-unlocked="true"]');

      await expect(unlockedBadges.first()).toBeVisible();
    });

    test('should show locked achievements', async ({ page }) => {
      const achievements = page.getByTestId('achievements');
      const lockedBadges = achievements.locator('[data-unlocked="false"]');

      await expect(lockedBadges.first()).toBeVisible();
    });

    test('should show achievement details on click', async ({ page }) => {
      const achievements = page.getByTestId('achievements');
      const firstBadge = achievements.locator('[data-achievement]').first();

      await firstBadge.click();

      // Should show achievement details modal
      await expect(page.getByRole('dialog')).toBeVisible();
      await expect(page.getByTestId('achievement-description')).toBeVisible();
    });
  });

  test.describe('Quick Actions', () => {
    test('should have quick action buttons', async ({ page }) => {
      await expect(page.getByRole('button', { name: /start practice/i })).toBeVisible();
      await expect(page.getByRole('link', { name: /view progress/i })).toBeVisible();
    });

    test('should navigate to practice from quick action', async ({ page }) => {
      await page.click('button:has-text("Start Practice")');
      await expect(page).toHaveURL(/.*practice/);
    });

    test('should navigate to progress from quick action', async ({ page }) => {
      await page.click('a:has-text("View Progress")');
      await expect(page).toHaveURL(/.*progress/);
    });
  });

  test.describe('Recent Activity', () => {
    test('should display recent sessions', async ({ page }) => {
      await expect(page.getByTestId('recent-sessions')).toBeVisible();
    });

    test('should show session details', async ({ page }) => {
      const sessions = page.getByTestId('recent-sessions');
      const firstSession = sessions.locator('[data-session]').first();

      await expect(firstSession).toBeVisible();

      // Should show session stats
      await expect(firstSession.getByTestId('session-date')).toBeVisible();
      await expect(firstSession.getByTestId('session-exercises')).toBeVisible();
      await expect(firstSession.getByTestId('session-accuracy')).toBeVisible();
    });
  });

  test.describe('Responsive Design', () => {
    test('should be responsive on mobile', async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 667 });

      // Dashboard should still be visible and usable
      await expect(page.getByTestId('total-exercises')).toBeVisible();
      await expect(page.getByTestId('performance-chart')).toBeVisible();
    });

    test('should be responsive on tablet', async ({ page }) => {
      await page.setViewportSize({ width: 768, height: 1024 });

      // Dashboard should adapt to tablet layout
      await expect(page.getByTestId('total-exercises')).toBeVisible();
      await expect(page.getByTestId('performance-chart')).toBeVisible();
    });
  });

  test.describe('Data Refresh', () => {
    test('should update stats after completing practice', async ({ page }) => {
      // Note initial stats
      const initialPoints = await page.getByTestId('total-points').textContent();

      // Complete a practice session
      await page.goto('/practice');
      await page.fill('input[name="exerciseCount"]', '1');
      await page.click('button:has-text("Start Practice")');

      await page.fill('[data-testid="answer-input"]', 'hable');
      await page.click('button:has-text("Submit")');
      await page.click('button:has-text("Next")');

      // Return to dashboard
      await page.goto('/dashboard');

      // Stats should be updated
      const updatedPoints = await page.getByTestId('total-points').textContent();
      expect(updatedPoints).not.toBe(initialPoints);
    });
  });
});

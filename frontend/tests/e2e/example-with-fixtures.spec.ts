import { test, expect } from './fixtures/authenticated';

/**
 * Example test file showing how to use fixtures and page objects
 * This file demonstrates best practices for E2E testing
 */

test.describe('Example: Using Fixtures and Page Objects', () => {
  test('should use authenticated page fixture', async ({ authenticatedPage, page }) => {
    // The authenticatedPage fixture automatically logs in
    // We can now navigate directly to protected routes

    await page.goto('/dashboard');
    await expect(page).toHaveURL(/.*dashboard/);

    // User should be logged in
    const userMenu = page.getByTestId('user-menu');
    await expect(userMenu).toBeVisible();
  });

  test('should use dashboard page object', async ({ authenticatedPage, dashboardPage }) => {
    // Navigate using page object
    await dashboardPage.goto();

    // Use page object methods
    await dashboardPage.expectStatsVisible();

    // Get statistics using page object
    const totalExercises = await dashboardPage.getTotalExercises();
    expect(totalExercises).toBeGreaterThanOrEqual(0);

    const accuracy = await dashboardPage.getAccuracy();
    expect(accuracy).toBeGreaterThanOrEqual(0);
    expect(accuracy).toBeLessThanOrEqual(100);
  });

  test('should use practice page object', async ({ authenticatedPage, practicePage }) => {
    // Navigate to practice page
    await practicePage.goto();

    // Start practice with custom settings
    await practicePage.startPracticeWithSettings({
      difficulty: 'intermediate',
      count: 3,
    });

    // Verify exercise card is visible
    await expect(practicePage.exerciseCard).toBeVisible();
    await expect(practicePage.answerInput).toBeVisible();

    // Submit an answer
    await practicePage.submitAnswer('hable');

    // Check for feedback
    const hasFeedback = await Promise.race([
      practicePage.correctIcon.isVisible().catch(() => false),
      practicePage.incorrectIcon.isVisible().catch(() => false),
    ]);

    expect(hasFeedback).toBeTruthy();
  });

  test('should use login page object without authentication', async ({ loginPage, page }) => {
    // This test doesn't use authenticatedPage, so it starts logged out

    // Navigate to login
    await loginPage.goto();

    // Check we're on login page
    await loginPage.expectOnLoginPage();

    // Try login with invalid credentials
    await loginPage.login('invalid@example.com', 'wrongpassword');

    // Should show error
    const error = await loginPage.getErrorMessage();
    expect(error).toBeTruthy();
  });

  test.describe('Combined workflow example', () => {
    test('should complete a full practice session', async ({ authenticatedPage, practicePage }) => {
      // Start practice
      await practicePage.goto();
      await practicePage.startPracticeWithSettings({
        difficulty: 'beginner',
        count: 2,
      });

      // Complete first exercise
      await practicePage.submitAnswer('hable');
      await practicePage.goToNext();

      // Complete second exercise
      await practicePage.submitAnswer('comas');
      await practicePage.goToNext();

      // Should show results
      await practicePage.expectSessionComplete();

      // Verify results exist
      const finalPoints = await practicePage.getFinalPoints();
      expect(finalPoints).toBeGreaterThanOrEqual(0);
    });

    test('should navigate between pages', async ({
      authenticatedPage,
      dashboardPage,
      practicePage,
    }) => {
      // Start on dashboard
      await dashboardPage.goto();
      await dashboardPage.expectOnDashboard();

      // Navigate to practice
      await dashboardPage.startPractice();
      await practicePage.expectOnPracticePage();

      // Go back to dashboard (using browser)
      await dashboardPage.goto();
      await dashboardPage.expectOnDashboard();
    });
  });
});

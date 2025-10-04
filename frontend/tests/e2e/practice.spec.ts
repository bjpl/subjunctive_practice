import { test, expect } from '@playwright/test';

test.describe('Practice Session Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/auth/login');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'Password123!');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/.*dashboard/);
  });

  test.describe('Starting Practice', () => {
    test('should start a practice session with default settings', async ({ page }) => {
      await page.goto('/practice');

      // Click start practice button
      await page.click('button:has-text("Start Practice")');

      // Should show first exercise
      await expect(page.getByTestId('exercise-card')).toBeVisible();
      await expect(page.getByTestId('exercise-prompt')).toBeVisible();
      await expect(page.getByTestId('answer-input')).toBeVisible();
    });

    test('should allow selecting difficulty level', async ({ page }) => {
      await page.goto('/practice');

      // Select difficulty
      await page.click('[data-testid="difficulty-select"]');
      await page.click('text=Intermediate');

      await page.click('button:has-text("Start Practice")');

      // Should show exercises of selected difficulty
      await expect(page.getByTestId('exercise-card')).toBeVisible();
    });

    test('should allow selecting specific tenses', async ({ page }) => {
      await page.goto('/practice');

      // Select tense
      await page.click('[data-testid="tense-select"]');
      await page.click('text=Present');

      await page.click('button:has-text("Start Practice")');

      // Should show exercises of selected tense
      await expect(page.getByTestId('exercise-card')).toBeVisible();
    });

    test('should set custom number of exercises', async ({ page }) => {
      await page.goto('/practice');

      // Set exercise count
      await page.fill('input[name="exerciseCount"]', '15');

      await page.click('button:has-text("Start Practice")');

      // Should show progress indicator with correct total
      await expect(page.getByText(/1.*\/.*15/)).toBeVisible();
    });
  });

  test.describe('Answering Exercises', () => {
    test('should submit correct answer and show feedback', async ({ page }) => {
      await page.goto('/practice');
      await page.click('button:has-text("Start Practice")');

      // Wait for exercise to load
      await page.waitForSelector('[data-testid="answer-input"]');

      // Submit correct answer
      await page.fill('[data-testid="answer-input"]', 'hable');
      await page.click('button:has-text("Submit")');

      // Should show correct feedback
      await expect(page.getByText(/correct/i)).toBeVisible();
      await expect(page.getByTestId('correct-icon')).toBeVisible();

      // Should show points earned
      await expect(page.getByText(/\+10.*points/i)).toBeVisible();
    });

    test('should submit incorrect answer and show explanation', async ({ page }) => {
      await page.goto('/practice');
      await page.click('button:has-text("Start Practice")');

      await page.waitForSelector('[data-testid="answer-input"]');

      // Submit incorrect answer
      await page.fill('[data-testid="answer-input"]', 'hablo');
      await page.click('button:has-text("Submit")');

      // Should show incorrect feedback
      await expect(page.getByText(/incorrect/i)).toBeVisible();
      await expect(page.getByTestId('incorrect-icon')).toBeVisible();

      // Should show correct answer
      await expect(page.getByText(/correct answer.*hable/i)).toBeVisible();

      // Should show explanation
      await expect(page.getByTestId('explanation')).toBeVisible();
    });

    test('should prevent empty submissions', async ({ page }) => {
      await page.goto('/practice');
      await page.click('button:has-text("Start Practice")');

      await page.waitForSelector('[data-testid="answer-input"]');

      // Try to submit empty answer
      const submitButton = page.getByRole('button', { name: /submit/i });

      // Button should be disabled
      await expect(submitButton).toBeDisabled();
    });

    test('should move to next exercise after submission', async ({ page }) => {
      await page.goto('/practice');
      await page.click('button:has-text("Start Practice")');

      await page.waitForSelector('[data-testid="answer-input"]');

      // Submit first answer
      await page.fill('[data-testid="answer-input"]', 'hable');
      await page.click('button:has-text("Submit")');

      // Click next button
      await page.click('button:has-text("Next")');

      // Should show next exercise
      await expect(page.getByText(/2.*\/.*10/)).toBeVisible();

      // Answer input should be cleared
      await expect(page.getByTestId('answer-input')).toHaveValue('');
    });
  });

  test.describe('Practice Session Navigation', () => {
    test('should show progress throughout session', async ({ page }) => {
      await page.goto('/practice');
      await page.click('button:has-text("Start Practice")');

      // Check initial progress
      await expect(page.getByText(/1.*\/.*10/)).toBeVisible();
      await expect(page.getByTestId('progress-bar')).toHaveAttribute('value', '0');

      // Complete first exercise
      await page.fill('[data-testid="answer-input"]', 'hable');
      await page.click('button:has-text("Submit")');
      await page.click('button:has-text("Next")');

      // Check updated progress
      await expect(page.getByText(/2.*\/.*10/)).toBeVisible();
      await expect(page.getByTestId('progress-bar')).toHaveAttribute('value', '10');
    });

    test('should allow skipping exercises', async ({ page }) => {
      await page.goto('/practice');
      await page.click('button:has-text("Start Practice")');

      await page.waitForSelector('[data-testid="answer-input"]');

      // Click skip button
      await page.click('button:has-text("Skip")');

      // Should move to next exercise
      await expect(page.getByText(/2.*\/.*10/)).toBeVisible();
    });

    test('should allow pausing and resuming session', async ({ page }) => {
      await page.goto('/practice');
      await page.click('button:has-text("Start Practice")');

      await page.waitForSelector('[data-testid="answer-input"]');

      // Pause session
      await page.click('button:has-text("Pause")');

      // Should show pause dialog
      await expect(page.getByText(/session paused/i)).toBeVisible();

      // Resume session
      await page.click('button:has-text("Resume")');

      // Should continue from same exercise
      await expect(page.getByText(/1.*\/.*10/)).toBeVisible();
    });

    test('should confirm before quitting session', async ({ page }) => {
      await page.goto('/practice');
      await page.click('button:has-text("Start Practice")');

      await page.waitForSelector('[data-testid="answer-input"]');

      // Try to quit
      await page.click('button:has-text("Quit")');

      // Should show confirmation dialog
      await expect(page.getByText(/quit.*session/i)).toBeVisible();

      // Cancel quit
      await page.click('button:has-text("Cancel")');

      // Should stay in session
      await expect(page.getByTestId('exercise-card')).toBeVisible();

      // Quit for real
      await page.click('button:has-text("Quit")');
      await page.click('button:has-text("Confirm")');

      // Should return to practice setup
      await expect(page.getByText(/start practice/i)).toBeVisible();
    });
  });

  test.describe('Session Completion', () => {
    test('should show results after completing all exercises', async ({ page }) => {
      await page.goto('/practice');

      // Start with just 2 exercises for faster testing
      await page.fill('input[name="exerciseCount"]', '2');
      await page.click('button:has-text("Start Practice")');

      // Complete first exercise
      await page.fill('[data-testid="answer-input"]', 'hable');
      await page.click('button:has-text("Submit")');
      await page.click('button:has-text("Next")');

      // Complete second exercise
      await page.fill('[data-testid="answer-input"]', 'comas');
      await page.click('button:has-text("Submit")');
      await page.click('button:has-text("Next")');

      // Should show results page
      await expect(page.getByText(/session complete/i)).toBeVisible();
      await expect(page.getByTestId('final-score')).toBeVisible();
      await expect(page.getByTestId('accuracy-stat')).toBeVisible();
      await expect(page.getByTestId('points-earned')).toBeVisible();
    });

    test('should display session statistics', async ({ page }) => {
      await page.goto('/practice');

      await page.fill('input[name="exerciseCount"]', '2');
      await page.click('button:has-text("Start Practice")');

      // Complete session
      await page.fill('[data-testid="answer-input"]', 'hable');
      await page.click('button:has-text("Submit")');
      await page.click('button:has-text("Next")');

      await page.fill('[data-testid="answer-input"]', 'comas');
      await page.click('button:has-text("Submit")');
      await page.click('button:has-text("Next")');

      // Check statistics
      await expect(page.getByText(/2.*\/.*2/)).toBeVisible(); // Exercises completed
      await expect(page.getByText(/100%/)).toBeVisible(); // Accuracy
      await expect(page.getByText(/20.*points/i)).toBeVisible(); // Points earned
    });

    test('should allow starting new session from results', async ({ page }) => {
      await page.goto('/practice');

      await page.fill('input[name="exerciseCount"]', '2');
      await page.click('button:has-text("Start Practice")');

      // Complete session quickly
      await page.fill('[data-testid="answer-input"]', 'hable');
      await page.click('button:has-text("Submit")');
      await page.click('button:has-text("Next")');

      await page.fill('[data-testid="answer-input"]', 'comas');
      await page.click('button:has-text("Submit")');
      await page.click('button:has-text("Next")');

      // Start new session
      await page.click('button:has-text("Practice Again")');

      // Should return to practice setup
      await expect(page.getByText(/start practice/i)).toBeVisible();
    });
  });

  test.describe('Keyboard Shortcuts', () => {
    test('should submit answer with Enter key', async ({ page }) => {
      await page.goto('/practice');
      await page.click('button:has-text("Start Practice")');

      await page.waitForSelector('[data-testid="answer-input"]');

      // Type answer and press Enter
      await page.fill('[data-testid="answer-input"]', 'hable');
      await page.press('[data-testid="answer-input"]', 'Enter');

      // Should show feedback
      await expect(page.getByText(/correct/i)).toBeVisible();
    });

    test('should navigate with keyboard shortcuts', async ({ page }) => {
      await page.goto('/practice');
      await page.click('button:has-text("Start Practice")');

      await page.waitForSelector('[data-testid="answer-input"]');

      // Submit with Enter
      await page.fill('[data-testid="answer-input"]', 'hable');
      await page.press('[data-testid="answer-input"]', 'Enter');

      // Move to next with keyboard shortcut
      await page.keyboard.press('n');

      // Should show next exercise
      await expect(page.getByText(/2.*\/.*10/)).toBeVisible();
    });
  });
});

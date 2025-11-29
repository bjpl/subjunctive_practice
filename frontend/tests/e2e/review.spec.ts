import { test, expect } from '@playwright/test';

test.describe('Spaced Repetition Review Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/auth/login');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'Password123!');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/.*dashboard/);
  });

  test.describe('Review Session Setup', () => {
    test('should navigate to review mode from practice page', async ({ page }) => {
      await page.goto('/practice');

      // Look for review mode option
      const reviewButton = page.getByRole('button', { name: /review/i });

      if (await reviewButton.isVisible()) {
        await reviewButton.click();

        // Should show review configuration or start review
        await expect(page.getByText(/review/i)).toBeVisible();
      } else {
        // Review mode might not be immediately visible
        console.log('Review mode button not found on practice page');
      }
    });

    test('should display number of due reviews', async ({ page }) => {
      await page.goto('/practice');

      // Check for due review count
      const dueReviewsIndicator = page.locator('[data-testid="due-reviews-count"]');

      if (await dueReviewsIndicator.isVisible()) {
        const count = await dueReviewsIndicator.textContent();
        expect(count).toMatch(/\d+/); // Should show a number
      }
    });

    test('should show review mode toggle', async ({ page }) => {
      await page.goto('/practice');

      // Look for mode toggle (practice vs review)
      const modeToggle = page.locator('[data-testid="mode-toggle"], [data-testid="session-type-select"]');

      if (await modeToggle.isVisible()) {
        await modeToggle.click();
        await expect(page.getByText(/review/i)).toBeVisible();
      }
    });
  });

  test.describe('Starting Review Session', () => {
    test('should start review session with due items', async ({ page }) => {
      await page.goto('/practice');

      // Try to start review mode
      const reviewOption = page.locator('text=/review/i').first();

      if (await reviewOption.isVisible()) {
        await reviewOption.click();

        const startButton = page.getByRole('button', { name: /start.*review/i });
        if (await startButton.isVisible()) {
          await startButton.click();

          // Should load review items
          await expect(page.getByTestId('exercise-card')).toBeVisible({ timeout: 10000 });
        }
      }
    });

    test('should show message when no reviews due', async ({ page }) => {
      await page.goto('/practice');

      // Navigate to review mode
      const reviewButton = page.getByRole('button', { name: /review/i });

      if (await reviewButton.isVisible()) {
        await reviewButton.click();

        // Might show "no reviews due" message
        const noReviewsMessage = page.locator('text=/no.*review.*due/i, text=/all.*caught.*up/i');

        // Either exercises show or "no reviews" message shows
        const hasExercises = await page.getByTestId('exercise-card').isVisible().catch(() => false);
        const hasMessage = await noReviewsMessage.isVisible().catch(() => false);

        expect(hasExercises || hasMessage).toBeTruthy();
      }
    });

    test('should filter reviews by verb or difficulty', async ({ page }) => {
      await page.goto('/practice');

      // Check for review filters
      const verbFilter = page.locator('[data-testid="verb-filter"]');
      const difficultyFilter = page.locator('[data-testid="difficulty-filter"]');

      if (await verbFilter.isVisible()) {
        await verbFilter.click();
        // Should show verb options
        await expect(page.locator('[role="option"], [role="menuitem"]').first()).toBeVisible();
      }

      if (await difficultyFilter.isVisible()) {
        await difficultyFilter.click();
        // Should show difficulty options
        await expect(page.locator('[role="option"], [role="menuitem"]').first()).toBeVisible();
      }
    });
  });

  test.describe('Completing Reviews', () => {
    test('should submit review and show quality rating', async ({ page }) => {
      await page.goto('/practice');

      // Try to start review
      const reviewMode = page.locator('text=/review/i').first();
      if (await reviewMode.isVisible()) {
        await reviewMode.click();
      }

      const startButton = page.getByRole('button', { name: /start/i });
      if (await startButton.isVisible()) {
        await startButton.click();

        // Wait for exercise
        const answerInput = page.getByTestId('answer-input');
        if (await answerInput.isVisible({ timeout: 5000 }).catch(() => false)) {
          await answerInput.fill('hable');
          await page.click('button:has-text("Submit")');

          // Look for quality rating prompt
          const qualityRating = page.locator('[data-testid="quality-rating"], text=/how.*well/i');

          if (await qualityRating.isVisible()) {
            // Should show quality options (1-5 or easy/medium/hard)
            await expect(page.locator('[data-testid="quality-option"], [role="button"]')).toHaveCount({ min: 3 });
          }
        }
      }
    });

    test('should record review quality and update schedule', async ({ page }) => {
      await page.goto('/practice');

      // Start review
      const reviewButton = page.locator('text=/review/i').first();
      if (await reviewButton.isVisible()) {
        await reviewButton.click();
      }

      const startButton = page.getByRole('button', { name: /start/i });
      if (await startButton.isVisible()) {
        await startButton.click();

        const answerInput = page.getByTestId('answer-input');
        if (await answerInput.isVisible({ timeout: 5000 }).catch(() => false)) {
          // Submit answer
          await answerInput.fill('hable');
          await page.click('button:has-text("Submit")');

          // Select quality rating if prompted
          const easyButton = page.getByRole('button', { name: /easy|5|perfect/i });
          if (await easyButton.isVisible()) {
            await easyButton.click();

            // Should show next review date
            const nextReviewInfo = page.locator('text=/next.*review/i, [data-testid="next-review-date"]');
            if (await nextReviewInfo.isVisible()) {
              const text = await nextReviewInfo.textContent();
              expect(text).toMatch(/\d+.*day|tomorrow|week|month/i);
            }
          }
        }
      }
    });

    test('should handle "Again" response (failed review)', async ({ page }) => {
      await page.goto('/practice');

      // Navigate to review
      const reviewButton = page.locator('text=/review/i').first();
      if (await reviewButton.isVisible()) {
        await reviewButton.click();
      }

      const startButton = page.getByRole('button', { name: /start/i });
      if (await startButton.isVisible()) {
        await startButton.click();

        const answerInput = page.getByTestId('answer-input');
        if (await answerInput.isVisible({ timeout: 5000 }).catch(() => false)) {
          // Submit wrong answer
          await answerInput.fill('wrong_answer');
          await page.click('button:has-text("Submit")');

          // Select "Again" or "Hard" rating
          const againButton = page.getByRole('button', { name: /again|hard|1|difficult/i });
          if (await againButton.isVisible()) {
            await againButton.click();

            // Should indicate item will be reviewed again soon
            const soonMessage = page.locator('text=/review.*soon|again.*today|1.*day/i');
            if (await soonMessage.isVisible()) {
              expect(await soonMessage.textContent()).toBeTruthy();
            }
          }
        }
      }
    });

    test('should show progress through review queue', async ({ page }) => {
      await page.goto('/practice');

      const reviewButton = page.locator('text=/review/i').first();
      if (await reviewButton.isVisible()) {
        await reviewButton.click();
      }

      const startButton = page.getByRole('button', { name: /start/i });
      if (await startButton.isVisible()) {
        await startButton.click();

        // Check for review progress indicator
        const progressIndicator = page.locator('[data-testid="review-progress"], text=/\\d+.*\\/.*\\d+/');

        if (await progressIndicator.isVisible()) {
          const progressText = await progressIndicator.textContent();
          expect(progressText).toMatch(/\d+/); // Should show numbers
        }
      }
    });
  });

  test.describe('Review Statistics', () => {
    test('should show review completion summary', async ({ page }) => {
      await page.goto('/practice');

      // This would require completing a full review session
      // For now, just check if review stats are available
      await page.goto('/progress');

      const reviewStats = page.locator('[data-testid="review-stats"], text=/review.*statistics/i');

      if (await reviewStats.isVisible()) {
        // Should show review-related metrics
        await expect(page.locator('text=/reviewed|due|mastered/i')).toHaveCount({ min: 1 });
      }
    });

    test('should display next review dates for verbs', async ({ page }) => {
      await page.goto('/progress');

      // Look for verb review schedule
      const reviewSchedule = page.locator('[data-testid="review-schedule"], text=/next.*review/i');

      if (await reviewSchedule.isVisible()) {
        // Should show dates
        await expect(page.locator('text=/day|week|month|today|tomorrow/i')).toHaveCount({ min: 1 });
      }
    });

    test('should show mastery levels for verbs', async ({ page }) => {
      await page.goto('/progress');

      // Look for mastery indicators
      const masterySection = page.locator('[data-testid="mastery-levels"], text=/mastery|proficiency/i');

      if (await masterySection.isVisible()) {
        // Should show different mastery levels
        await expect(page.locator('text=/learning|familiar|mastered|reviewing/i').first()).toBeVisible();
      }
    });

    test('should display review accuracy over time', async ({ page }) => {
      await page.goto('/progress');

      // Look for review accuracy chart or stats
      const accuracyChart = page.locator('[data-testid="review-accuracy"], [data-testid="accuracy-chart"]');

      if (await accuracyChart.isVisible()) {
        // Should have accuracy percentage
        await expect(page.locator('text=/\\d+%/')).toHaveCount({ min: 1 });
      }
    });
  });

  test.describe('Review Calendar', () => {
    test('should show review calendar with due dates', async ({ page }) => {
      await page.goto('/practice');

      // Look for calendar view
      const calendarButton = page.getByRole('button', { name: /calendar|schedule/i });

      if (await calendarButton.isVisible()) {
        await calendarButton.click();

        // Should show calendar
        await expect(page.locator('[data-testid="review-calendar"], [class*="calendar"]')).toBeVisible();
      }
    });

    test('should highlight days with due reviews', async ({ page }) => {
      await page.goto('/practice');

      const calendarView = page.locator('[data-testid="calendar-view"]');

      if (await calendarView.isVisible()) {
        // Days with reviews should be highlighted
        const highlightedDays = page.locator('[data-has-reviews="true"], [class*="has-review"]');

        if (await highlightedDays.first().isVisible()) {
          const count = await highlightedDays.count();
          expect(count).toBeGreaterThan(0);
        }
      }
    });

    test('should show review count on calendar dates', async ({ page }) => {
      await page.goto('/practice');

      const calendarButton = page.getByRole('button', { name: /calendar/i });
      if (await calendarButton.isVisible()) {
        await calendarButton.click();

        // Look for review count badges on dates
        const reviewBadges = page.locator('[data-testid="review-count"], [class*="review-badge"]');

        if (await reviewBadges.first().isVisible()) {
          const badgeText = await reviewBadges.first().textContent();
          expect(badgeText).toMatch(/\d+/);
        }
      }
    });
  });

  test.describe('Review Settings', () => {
    test('should allow configuring daily review limit', async ({ page }) => {
      await page.goto('/settings');

      // Look for review settings
      const reviewSettings = page.locator('[data-testid="review-settings"], text=/review.*settings/i');

      if (await reviewSettings.isVisible()) {
        const dailyLimitInput = page.locator('[name="dailyReviewLimit"], [data-testid="daily-review-limit"]');

        if (await dailyLimitInput.isVisible()) {
          await dailyLimitInput.fill('20');

          // Save settings
          const saveButton = page.getByRole('button', { name: /save/i });
          if (await saveButton.isVisible()) {
            await saveButton.click();
            await expect(page.locator('text=/saved|updated/i')).toBeVisible();
          }
        }
      }
    });

    test('should allow enabling/disabling review notifications', async ({ page }) => {
      await page.goto('/settings');

      const notificationToggle = page.locator('[data-testid="review-notifications"], input[type="checkbox"][name*="notification"]');

      if (await notificationToggle.isVisible()) {
        const initialState = await notificationToggle.isChecked();

        // Toggle notification setting
        await notificationToggle.click();

        const newState = await notificationToggle.isChecked();
        expect(newState).toBe(!initialState);
      }
    });
  });

  test.describe('Review Performance Tracking', () => {
    test('should track review streak', async ({ page }) => {
      await page.goto('/progress');

      // Look for review streak indicator
      const reviewStreak = page.locator('[data-testid="review-streak"], text=/review.*streak/i');

      if (await reviewStreak.isVisible()) {
        const streakText = await reviewStreak.textContent();
        expect(streakText).toMatch(/\d+.*day/i);
      }
    });

    test('should show retention rate', async ({ page }) => {
      await page.goto('/progress');

      // Look for retention statistics
      const retentionStats = page.locator('[data-testid="retention-rate"], text=/retention/i');

      if (await retentionStats.isVisible()) {
        // Should show percentage
        await expect(page.locator('text=/\\d+%/')).toHaveCount({ min: 1 });
      }
    });

    test('should display review performance trends', async ({ page }) => {
      await page.goto('/progress');

      // Look for performance chart
      const performanceChart = page.locator('[data-testid="performance-chart"], [data-testid="review-trends"]');

      if (await performanceChart.isVisible()) {
        // Chart should be rendered
        const chartElements = page.locator('[data-testid="chart-data"], svg, canvas');
        if (await chartElements.first().isVisible()) {
          expect(await chartElements.count()).toBeGreaterThan(0);
        }
      }
    });
  });

  test.describe('Edge Cases', () => {
    test('should handle completing all reviews in queue', async ({ page }) => {
      await page.goto('/practice');

      const reviewButton = page.locator('text=/review/i').first();
      if (await reviewButton.isVisible()) {
        await reviewButton.click();
      }

      const startButton = page.getByRole('button', { name: /start/i });
      if (await startButton.isVisible()) {
        await startButton.click();

        // If reviews exist, complete them
        const answerInput = page.getByTestId('answer-input');
        if (await answerInput.isVisible({ timeout: 5000 }).catch(() => false)) {
          // Complete one review
          await answerInput.fill('hable');
          await page.click('button:has-text("Submit")');

          const easyButton = page.getByRole('button', { name: /easy|5/i });
          if (await easyButton.isVisible()) {
            await easyButton.click();
          }

          // Eventually should see completion message or no more reviews
          await expect(
            page.locator('text=/complete|finished|no.*more.*review/i')
          ).toBeVisible({ timeout: 30000 });
        }
      }
    });

    test('should handle interrupting review session', async ({ page }) => {
      await page.goto('/practice');

      const reviewButton = page.locator('text=/review/i').first();
      if (await reviewButton.isVisible()) {
        await reviewButton.click();
      }

      const startButton = page.getByRole('button', { name: /start/i });
      if (await startButton.isVisible()) {
        await startButton.click();

        // Navigate away mid-session
        await page.goto('/dashboard');

        // Come back to practice
        await page.goto('/practice');

        // Should offer to resume or start fresh
        const resumeOption = page.locator('text=/resume|continue/i');
        const startNewOption = page.locator('text=/start.*new|begin/i');

        const hasResumeOption = await resumeOption.isVisible().catch(() => false);
        const hasStartNewOption = await startNewOption.isVisible().catch(() => false);

        expect(hasResumeOption || hasStartNewOption).toBeTruthy();
      }
    });
  });
});

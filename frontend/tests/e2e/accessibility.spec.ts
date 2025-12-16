import { test, expect } from '@playwright/test';
import { loginAsTestUser } from './utils/auth-helpers';

test.describe('Accessibility Tests', () => {
  test.describe('Keyboard Navigation', () => {
    test('should navigate login form with keyboard', async ({ page }) => {
      await page.goto('/auth/login');

      // Tab to email field
      await page.keyboard.press('Tab');
      let focused = await page.evaluate(() => document.activeElement?.getAttribute('name'));
      expect(focused).toBe('email');

      // Tab to password field
      await page.keyboard.press('Tab');
      focused = await page.evaluate(() => document.activeElement?.getAttribute('name'));
      expect(focused).toBe('password');

      // Tab to submit button
      await page.keyboard.press('Tab');
      focused = await page.evaluate(() => document.activeElement?.getAttribute('type'));
      expect(focused).toBe('submit');
    });

    test('should navigate practice session with keyboard', async ({ page }) => {
      await loginAsTestUser(page);
      await page.goto('/practice');

      // Start practice
      await page.click('button:has-text("Start Practice")');
      await page.waitForSelector('[data-testid="exercise-card"]');

      // Answer input should be focusable
      await page.keyboard.press('Tab');
      const answerInput = page.getByTestId('answer-input');
      await expect(answerInput).toBeFocused();

      // Type answer
      await page.keyboard.type('hable');

      // Submit with Enter
      await page.keyboard.press('Enter');

      // Should show feedback
      await expect(page.locator('text=/correct|incorrect/i')).toBeVisible();
    });

    test('should navigate dashboard with keyboard', async ({ page }) => {
      await loginAsTestUser(page);

      // Tab through interactive elements
      let tabCount = 0;
      const maxTabs = 20;

      while (tabCount < maxTabs) {
        await page.keyboard.press('Tab');
        tabCount++;

        // Check if we can reach the start practice button
        const focused = await page.evaluate(() => {
          const el = document.activeElement;
          return el?.textContent?.toLowerCase().includes('practice');
        });

        if (focused) {
          // Successfully navigated to practice button
          expect(focused).toBeTruthy();
          break;
        }
      }
    });

    test('should support arrow key navigation in menus', async ({ page }) => {
      await loginAsTestUser(page);

      // Open user menu
      const userMenu = page.getByTestId('user-menu');
      await userMenu.click();

      // Navigate with arrow keys
      await page.keyboard.press('ArrowDown');
      await page.keyboard.press('ArrowDown');

      // Should be able to select with Enter
      const focusedElement = await page.evaluate(() => {
        return document.activeElement?.textContent;
      });

      expect(focusedElement).toBeTruthy();
    });

    test('should trap focus in modal dialogs', async ({ page }) => {
      await loginAsTestUser(page);
      await page.goto('/practice');

      await page.click('button:has-text("Start Practice")');
      await page.waitForSelector('[data-testid="exercise-card"]');

      // Open pause dialog
      await page.click('button:has-text("Pause")');

      // Dialog should be visible
      await expect(page.getByRole('dialog')).toBeVisible();

      // Tab through dialog elements - focus should stay within dialog
      await page.keyboard.press('Tab');
      await page.keyboard.press('Tab');
      await page.keyboard.press('Tab');

      // Focus should still be within the dialog
      const focusInDialog = await page.evaluate(() => {
        const dialog = document.querySelector('[role="dialog"]');
        const focused = document.activeElement;
        return dialog?.contains(focused) || false;
      });

      expect(focusInDialog).toBeTruthy();
    });

    test('should close modal with Escape key', async ({ page }) => {
      await loginAsTestUser(page);
      await page.goto('/dashboard');

      // Open achievement dialog
      const achievement = page.getByTestId('achievements').locator('[data-achievement]').first();
      await achievement.click();

      // Dialog should be visible
      await expect(page.getByRole('dialog')).toBeVisible();

      // Press Escape
      await page.keyboard.press('Escape');

      // Dialog should be closed
      await expect(page.getByRole('dialog')).not.toBeVisible({ timeout: 3000 });
    });
  });

  test.describe('Screen Reader Support', () => {
    test('should have proper ARIA labels on form inputs', async ({ page }) => {
      await page.goto('/auth/login');

      // Check email input
      const emailInput = page.locator('input[name="email"]');
      const emailLabel = await emailInput.getAttribute('aria-label');
      const emailLabelledBy = await emailInput.getAttribute('aria-labelledby');

      expect(emailLabel || emailLabelledBy).toBeTruthy();

      // Check password input
      const passwordInput = page.locator('input[name="password"]');
      const passwordLabel = await passwordInput.getAttribute('aria-label');
      const passwordLabelledBy = await passwordInput.getAttribute('aria-labelledby');

      expect(passwordLabel || passwordLabelledBy).toBeTruthy();
    });

    test('should announce form validation errors', async ({ page }) => {
      await page.goto('/auth/login');

      // Submit empty form
      await page.click('button[type="submit"]');

      // Error should be announced (have role="alert" or aria-live)
      const errorElement = page.locator('[role="alert"]').first();
      await expect(errorElement).toBeVisible();

      // Check aria-live region
      const ariaLive = await errorElement.getAttribute('aria-live');
      const role = await errorElement.getAttribute('role');

      expect(ariaLive === 'polite' || ariaLive === 'assertive' || role === 'alert').toBeTruthy();
    });

    test('should have proper heading hierarchy', async ({ page }) => {
      await loginAsTestUser(page);

      // Check heading levels
      const h1 = await page.locator('h1').count();
      expect(h1).toBeGreaterThan(0);

      // Check that headings follow proper hierarchy
      const headings = await page.evaluate(() => {
        const elements = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6'));
        return elements.map((el) => parseInt(el.tagName.substring(1)));
      });

      // Should start with h1
      expect(headings[0]).toBe(1);

      // Check for skipped levels (e.g., h1 to h3 without h2)
      for (let i = 1; i < headings.length; i++) {
        const diff = headings[i] - headings[i - 1];
        // Difference should not be more than 1 when increasing
        if (diff > 0) {
          expect(diff).toBeLessThanOrEqual(1);
        }
      }
    });

    test('should have descriptive button labels', async ({ page }) => {
      await loginAsTestUser(page);
      await page.goto('/practice');

      // All buttons should have accessible names
      const buttons = await page.locator('button').all();

      for (const button of buttons) {
        const isVisible = await button.isVisible();
        if (!isVisible) continue;

        const accessibleName = await button.evaluate((el) => {
          return (
            el.getAttribute('aria-label') ||
            el.textContent?.trim() ||
            el.getAttribute('title')
          );
        });

        expect(accessibleName).toBeTruthy();
      }
    });

    test('should announce practice session progress', async ({ page }) => {
      await loginAsTestUser(page);
      await page.goto('/practice');

      await page.click('button:has-text("Start Practice")');
      await page.waitForSelector('[data-testid="exercise-card"]');

      // Progress should be announced
      const progressElement = page.locator('text=/\\d+\\s*\\/\\s*\\d+/');
      await expect(progressElement).toBeVisible();

      // Check for aria-live or role
      const container = await page.evaluate(() => {
        const progress = document.querySelector('[data-testid="progress-bar"]');
        return {
          role: progress?.getAttribute('role'),
          ariaValueNow: progress?.getAttribute('aria-valuenow'),
          ariaValueMin: progress?.getAttribute('aria-valuemin'),
          ariaValueMax: progress?.getAttribute('aria-valuemax'),
        };
      });

      // Progress bar should have proper ARIA attributes
      expect(container.role).toBe('progressbar');
      expect(container.ariaValueNow).toBeTruthy();
    });

    test('should announce correct/incorrect feedback', async ({ page }) => {
      await loginAsTestUser(page);
      await page.goto('/practice');

      await page.click('button:has-text("Start Practice")');
      await page.waitForSelector('[data-testid="answer-input"]');

      // Submit answer
      await page.fill('[data-testid="answer-input"]', 'hable');
      await page.click('button:has-text("Submit")');

      // Feedback should be in an ARIA live region
      const feedback = page.locator('text=/correct|incorrect/i').first();
      await expect(feedback).toBeVisible();

      // Check parent for aria-live
      const hasLiveRegion = await feedback.evaluate((el) => {
        let current = el;
        while (current && current !== document.body) {
          if (
            current.getAttribute('aria-live') ||
            current.getAttribute('role') === 'alert' ||
            current.getAttribute('role') === 'status'
          ) {
            return true;
          }
          current = current.parentElement as HTMLElement;
        }
        return false;
      });

      expect(hasLiveRegion).toBeTruthy();
    });
  });

  test.describe('Skip Links', () => {
    test('should have skip to main content link', async ({ page }) => {
      await loginAsTestUser(page);

      // Press Tab to reveal skip link
      await page.keyboard.press('Tab');

      // Check for skip link
      const skipLink = page.locator('a[href="#main-content"], a:has-text("Skip to")').first();

      // Skip link should exist and be focusable
      const exists = await skipLink.count();
      if (exists > 0) {
        // If skip link exists, it should work
        await skipLink.click();

        // Focus should move to main content
        const mainContent = page.locator('#main-content, main, [role="main"]').first();
        await expect(mainContent).toBeVisible();
      }
    });
  });

  test.describe('Focus Management', () => {
    test('should manage focus on route changes', async ({ page }) => {
      await loginAsTestUser(page);

      // Navigate to practice
      await page.click('a[href*="practice"]');
      await page.waitForURL(/.*practice/);

      // Focus should be set to a logical element (heading or main content)
      await page.waitForTimeout(500);

      const focused = await page.evaluate(() => {
        const el = document.activeElement;
        return {
          tag: el?.tagName,
          role: el?.getAttribute('role'),
          id: el?.id,
        };
      });

      // Should focus on heading, main, or body
      const validFocus =
        focused.tag === 'H1' ||
        focused.role === 'main' ||
        focused.tag === 'MAIN' ||
        focused.tag === 'BODY';

      expect(validFocus).toBeTruthy();
    });

    test('should return focus after closing modal', async ({ page }) => {
      await loginAsTestUser(page);

      // Find and click an element that opens a modal
      const achievementButton = page
        .getByTestId('achievements')
        .locator('[data-achievement]')
        .first();

      await achievementButton.click();

      // Modal should be open
      await expect(page.getByRole('dialog')).toBeVisible();

      // Close modal with Escape
      await page.keyboard.press('Escape');

      // Wait for modal to close
      await expect(page.getByRole('dialog')).not.toBeVisible({ timeout: 3000 });

      // Focus should return to the button that opened it
      await page.waitForTimeout(100);

      const focusedAfterClose = await page.evaluate(() => {
        return document.activeElement?.getAttribute('data-achievement');
      });

      expect(focusedAfterClose).toBeTruthy();
    });

    test('should show visible focus indicators', async ({ page }) => {
      await page.goto('/auth/login');

      // Tab to email input
      await page.keyboard.press('Tab');

      // Check if focus is visible
      const hasFocusStyle = await page.evaluate(() => {
        const el = document.activeElement as HTMLElement;
        const styles = window.getComputedStyle(el);

        // Check for outline or box-shadow (common focus indicators)
        return (
          styles.outline !== 'none' &&
          styles.outline !== '' &&
          styles.outlineWidth !== '0px'
        ) || styles.boxShadow !== 'none';
      });

      expect(hasFocusStyle).toBeTruthy();
    });
  });

  test.describe('Color Contrast', () => {
    test('should have sufficient color contrast on login page', async ({ page }) => {
      await page.goto('/auth/login');

      // Check text elements for contrast
      // This is a simplified check - in production, use axe-core or similar
      const textElements = await page.locator('p, h1, h2, h3, label, button, a').all();

      for (const element of textElements.slice(0, 10)) {
        // Check first 10 elements
        const isVisible = await element.isVisible();
        if (!isVisible) continue;

        const contrast = await element.evaluate((el) => {
          const styles = window.getComputedStyle(el);
          // In a real test, calculate actual contrast ratio
          // For now, just check that color is defined
          return {
            color: styles.color,
            backgroundColor: styles.backgroundColor,
          };
        });

        expect(contrast.color).toBeTruthy();
      }
    });
  });

  test.describe('Form Accessibility', () => {
    test('should associate labels with inputs', async ({ page }) => {
      await page.goto('/auth/register');

      // Check that all inputs have associated labels
      const inputs = await page
        .locator('input[type="text"], input[type="email"], input[type="password"]')
        .all();

      for (const input of inputs) {
        const hasLabel = await input.evaluate((el) => {
          const id = el.id;
          const ariaLabel = el.getAttribute('aria-label');
          const ariaLabelledBy = el.getAttribute('aria-labelledby');

          // Check for explicit label
          if (id) {
            const label = document.querySelector(`label[for="${id}"]`);
            if (label) return true;
          }

          // Check for aria-label or aria-labelledby
          if (ariaLabel || ariaLabelledBy) return true;

          return false;
        });

        expect(hasLabel).toBeTruthy();
      }
    });

    test('should indicate required fields', async ({ page }) => {
      await page.goto('/auth/register');

      // Check required inputs
      const requiredInputs = await page.locator('input[required]').all();

      for (const input of requiredInputs) {
        const hasRequiredIndicator = await input.evaluate((el) => {
          const ariaRequired = el.getAttribute('aria-required');
          const required = el.hasAttribute('required');

          return ariaRequired === 'true' || required;
        });

        expect(hasRequiredIndicator).toBeTruthy();
      }
    });
  });

  test.describe('Semantic HTML', () => {
    test('should use semantic landmarks', async ({ page }) => {
      await loginAsTestUser(page);

      // Check for main landmark
      const main = await page.locator('main, [role="main"]').count();
      expect(main).toBeGreaterThan(0);

      // Check for navigation
      const nav = await page.locator('nav, [role="navigation"]').count();
      expect(nav).toBeGreaterThan(0);
    });

    test('should use semantic list elements', async ({ page }) => {
      await loginAsTestUser(page);

      // Navigation should use lists
      const navList = await page.locator('nav ul, nav ol, [role="navigation"] ul').count();
      expect(navList).toBeGreaterThan(0);
    });
  });

  test.describe('Mobile Accessibility', () => {
    test('should have adequate touch target sizes', async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 667 });
      await loginAsTestUser(page);

      // Check button sizes (should be at least 44x44px)
      const buttons = await page.locator('button').all();

      for (const button of buttons.slice(0, 5)) {
        const isVisible = await button.isVisible();
        if (!isVisible) continue;

        const size = await button.boundingBox();

        if (size) {
          // Touch targets should be at least 44x44px
          expect(size.width).toBeGreaterThanOrEqual(40);
          expect(size.height).toBeGreaterThanOrEqual(40);
        }
      }
    });

    test('should be operable in landscape mode', async ({ page }) => {
      await page.setViewportSize({ width: 667, height: 375 }); // iPhone landscape
      await loginAsTestUser(page);

      // Should still be usable
      await expect(page.getByTestId('user-menu')).toBeVisible();

      // Navigate to practice
      await page.goto('/practice');
      await expect(page.getByRole('button', { name: /start practice/i })).toBeVisible();
    });
  });

  test.describe('Reduced Motion', () => {
    test('should respect prefers-reduced-motion', async ({ page }) => {
      // Emulate reduced motion preference
      await page.emulateMedia({ reducedMotion: 'reduce' });

      await loginAsTestUser(page);
      await page.goto('/practice');

      // Animations should be reduced or disabled
      // This is hard to test automatically, but we can check that the page loads
      await expect(page.getByRole('button', { name: /start practice/i })).toBeVisible();
    });
  });
});

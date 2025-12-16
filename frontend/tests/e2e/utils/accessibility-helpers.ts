import { Page, expect } from '@playwright/test';

/**
 * Accessibility helper functions for E2E tests
 */

/**
 * Check if element has proper ARIA label
 */
export async function hasAccessibleName(element: any): Promise<boolean> {
  const accessibleName = await element.evaluate((el: HTMLElement) => {
    return (
      el.getAttribute('aria-label') ||
      el.textContent?.trim() ||
      el.getAttribute('title') ||
      el.getAttribute('aria-labelledby')
    );
  });

  return !!accessibleName;
}

/**
 * Check heading hierarchy
 */
export async function checkHeadingHierarchy(page: Page): Promise<{ valid: boolean; errors: string[] }> {
  const headings = await page.evaluate(() => {
    const elements = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6'));
    return elements.map((el) => ({
      level: parseInt(el.tagName.substring(1)),
      text: el.textContent?.trim() || '',
    }));
  });

  const errors: string[] = [];

  // Should have at least one h1
  const h1Count = headings.filter((h) => h.level === 1).length;
  if (h1Count === 0) {
    errors.push('No h1 heading found');
  } else if (h1Count > 1) {
    errors.push(`Multiple h1 headings found (${h1Count})`);
  }

  // Check for skipped levels
  for (let i = 1; i < headings.length; i++) {
    const diff = headings[i].level - headings[i - 1].level;
    if (diff > 1) {
      errors.push(
        `Skipped heading level: ${headings[i - 1].level} to ${headings[i].level} ("${headings[i].text}")`
      );
    }
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}

/**
 * Check for keyboard traps
 */
export async function checkForKeyboardTrap(page: Page, maxTabs = 50): Promise<boolean> {
  const initialElement = await page.evaluate(() => document.activeElement?.tagName);

  for (let i = 0; i < maxTabs; i++) {
    await page.keyboard.press('Tab');
    await page.waitForTimeout(50);

    const currentElement = await page.evaluate(() => document.activeElement?.tagName);

    // If we've returned to body or initial element, we've completed the cycle
    if (currentElement === 'BODY' && i > 5) {
      return false; // No trap, successfully cycled through
    }
  }

  // If we tabbed through maxTabs elements and didn't return to body,
  // there might be a keyboard trap
  return true;
}

/**
 * Check if element is in tab order
 */
export async function isInTabOrder(element: any): Promise<boolean> {
  return await element.evaluate((el: HTMLElement) => {
    const tabindex = el.getAttribute('tabindex');

    // Elements with tabindex="-1" are not in tab order
    if (tabindex === '-1') return false;

    // Check if element is focusable
    const focusableElements = [
      'a[href]',
      'button',
      'input',
      'select',
      'textarea',
      '[tabindex]',
    ];

    const isFocusable = focusableElements.some((selector) => {
      try {
        return el.matches(selector);
      } catch {
        return false;
      }
    });

    return isFocusable;
  });
}

/**
 * Check color contrast (simplified version)
 */
export async function checkColorContrast(element: any): Promise<{
  color: string;
  backgroundColor: string;
  hasContrast: boolean;
}> {
  return await element.evaluate((el: HTMLElement) => {
    const styles = window.getComputedStyle(el);
    const color = styles.color;
    const backgroundColor = styles.backgroundColor;

    // Simplified check - in production use a proper contrast ratio calculator
    const hasContrast = color !== backgroundColor && color !== 'rgba(0, 0, 0, 0)';

    return {
      color,
      backgroundColor,
      hasContrast,
    };
  });
}

/**
 * Get all interactive elements on page
 */
export async function getInteractiveElements(page: Page) {
  return await page.locator('button, a, input, select, textarea, [role="button"]').all();
}

/**
 * Check if page has skip links
 */
export async function hasSkipLinks(page: Page): Promise<boolean> {
  const skipLinks = await page
    .locator('a[href^="#"], a:has-text("Skip to")')
    .first()
    .count();
  return skipLinks > 0;
}

/**
 * Check for proper form labels
 */
export async function checkFormLabels(page: Page): Promise<{ total: number; labeled: number; unlabeled: string[] }> {
  return await page.evaluate(() => {
    const inputs = Array.from(
      document.querySelectorAll('input, select, textarea')
    ) as HTMLElement[];

    let labeled = 0;
    const unlabeled: string[] = [];

    inputs.forEach((input) => {
      const id = input.id;
      const ariaLabel = input.getAttribute('aria-label');
      const ariaLabelledBy = input.getAttribute('aria-labelledby');
      const type = input.getAttribute('type');

      // Skip hidden inputs
      if (type === 'hidden') return;

      let hasLabel = false;

      // Check for explicit label
      if (id) {
        const label = document.querySelector(`label[for="${id}"]`);
        if (label) hasLabel = true;
      }

      // Check for aria-label or aria-labelledby
      if (ariaLabel || ariaLabelledBy) hasLabel = true;

      if (hasLabel) {
        labeled++;
      } else {
        unlabeled.push(
          `${input.tagName}${type ? `[type="${type}"]` : ''}${id ? `#${id}` : ''}`
        );
      }
    });

    return {
      total: inputs.length,
      labeled,
      unlabeled,
    };
  });
}

/**
 * Check for ARIA live regions
 */
export async function hasLiveRegion(page: Page): Promise<boolean> {
  const liveRegions = await page.locator('[aria-live], [role="alert"], [role="status"]').count();
  return liveRegions > 0;
}

/**
 * Check if modal traps focus
 */
export async function modalTrapsFocus(page: Page): Promise<boolean> {
  const dialog = page.getByRole('dialog');
  const isVisible = await dialog.isVisible();

  if (!isVisible) return false;

  // Tab multiple times
  for (let i = 0; i < 10; i++) {
    await page.keyboard.press('Tab');
    await page.waitForTimeout(50);
  }

  // Check if focus is still within dialog
  return await page.evaluate(() => {
    const dialog = document.querySelector('[role="dialog"]');
    const focused = document.activeElement;
    return dialog ? dialog.contains(focused) : false;
  });
}

/**
 * Check for focus visible indicators
 */
export async function hasFocusIndicator(element: any): Promise<boolean> {
  return await element.evaluate((el: HTMLElement) => {
    const styles = window.getComputedStyle(el);

    // Check for outline
    const hasOutline =
      styles.outline !== 'none' &&
      styles.outline !== '' &&
      styles.outlineWidth !== '0px';

    // Check for box-shadow
    const hasBoxShadow = styles.boxShadow !== 'none' && styles.boxShadow !== '';

    return hasOutline || hasBoxShadow;
  });
}

/**
 * Get landmark regions
 */
export async function getLandmarks(page: Page): Promise<string[]> {
  return await page.evaluate(() => {
    const landmarks = Array.from(
      document.querySelectorAll(
        'main, nav, aside, header, footer, [role="main"], [role="navigation"], [role="complementary"], [role="banner"], [role="contentinfo"]'
      )
    );

    return landmarks.map((el) => {
      const role = el.getAttribute('role') || el.tagName.toLowerCase();
      const label = el.getAttribute('aria-label');
      return label ? `${role} (${label})` : role;
    });
  });
}

/**
 * Check touch target size (for mobile)
 */
export async function checkTouchTargetSize(
  element: any,
  minWidth = 44,
  minHeight = 44
): Promise<{ width: number; height: number; meetsRequirement: boolean }> {
  const box = await element.boundingBox();

  if (!box) {
    return { width: 0, height: 0, meetsRequirement: false };
  }

  return {
    width: box.width,
    height: box.height,
    meetsRequirement: box.width >= minWidth && box.height >= minHeight,
  };
}

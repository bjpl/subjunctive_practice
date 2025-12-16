import { test as base } from '@playwright/test';
import { loginAsTestUser } from '../utils/auth-helpers';
import { LoginPage, DashboardPage, PracticePage } from '../utils/page-objects';

/**
 * Playwright fixtures for authenticated sessions and page objects
 */

type TestFixtures = {
  authenticatedPage: void;
  loginPage: LoginPage;
  dashboardPage: DashboardPage;
  practicePage: PracticePage;
};

/**
 * Extended test with custom fixtures
 */
export const test = base.extend<TestFixtures>({
  /**
   * Fixture that automatically logs in before each test
   */
  authenticatedPage: async ({ page }, use) => {
    await loginAsTestUser(page);
    await use();
  },

  /**
   * Login page object
   */
  loginPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await use(loginPage);
  },

  /**
   * Dashboard page object
   */
  dashboardPage: async ({ page }, use) => {
    const dashboardPage = new DashboardPage(page);
    await use(dashboardPage);
  },

  /**
   * Practice page object
   */
  practicePage: async ({ page }, use) => {
    const practicePage = new PracticePage(page);
    await use(practicePage);
  },
});

export { expect } from '@playwright/test';

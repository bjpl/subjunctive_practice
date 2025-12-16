import { Page, Locator, expect } from '@playwright/test';

/**
 * Page Object Model for Login Page
 */
export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly registerLink: Locator;
  readonly forgotPasswordLink: Locator;
  readonly passwordToggle: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.locator('input[name="email"]');
    this.passwordInput = page.locator('input[name="password"]');
    this.submitButton = page.locator('button[type="submit"]');
    this.registerLink = page.getByRole('link', { name: /register|sign up/i });
    this.forgotPasswordLink = page.getByRole('link', { name: /forgot password/i });
    this.passwordToggle = page.getByRole('button', { name: /show password|hide password/i });
    this.errorMessage = page.locator('[role="alert"]').first();
  }

  async goto() {
    await this.page.goto('/auth/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async loginAndWait(email: string, password: string) {
    await this.login(email, password);
    await this.page.waitForURL(/.*dashboard/, { timeout: 10000 });
  }

  async togglePasswordVisibility() {
    await this.passwordToggle.click();
  }

  async isPasswordVisible(): Promise<boolean> {
    const type = await this.passwordInput.getAttribute('type');
    return type === 'text';
  }

  async getErrorMessage(): Promise<string | null> {
    try {
      await this.errorMessage.waitFor({ state: 'visible', timeout: 3000 });
      return await this.errorMessage.textContent();
    } catch {
      return null;
    }
  }

  async expectError(message: string | RegExp) {
    await expect(this.errorMessage).toBeVisible();
    if (typeof message === 'string') {
      await expect(this.errorMessage).toContainText(message);
    } else {
      await expect(this.errorMessage).toContainText(message);
    }
  }

  async expectOnLoginPage() {
    await expect(this.page).toHaveURL(/.*login/);
  }

  async goToRegister() {
    await this.registerLink.click();
    await this.page.waitForURL(/.*register/);
  }
}

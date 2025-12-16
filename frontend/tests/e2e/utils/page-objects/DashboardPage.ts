import { Page, Locator, expect } from '@playwright/test';

/**
 * Page Object Model for Dashboard Page
 */
export class DashboardPage {
  readonly page: Page;

  // Stats
  readonly totalExercises: Locator;
  readonly accuracyStat: Locator;
  readonly currentStreak: Locator;
  readonly totalPoints: Locator;
  readonly userLevel: Locator;
  readonly levelProgress: Locator;

  // Charts
  readonly performanceChart: Locator;
  readonly studyHeatmap: Locator;

  // Sections
  readonly weakAreas: Locator;
  readonly achievements: Locator;
  readonly recentSessions: Locator;

  // Actions
  readonly startPracticeButton: Locator;
  readonly viewProgressLink: Locator;

  // Navigation
  readonly userMenu: Locator;

  constructor(page: Page) {
    this.page = page;

    // Stats
    this.totalExercises = page.getByTestId('total-exercises');
    this.accuracyStat = page.getByTestId('accuracy-stat');
    this.currentStreak = page.getByTestId('current-streak');
    this.totalPoints = page.getByTestId('total-points');
    this.userLevel = page.getByTestId('user-level');
    this.levelProgress = page.getByTestId('level-progress');

    // Charts
    this.performanceChart = page.getByTestId('performance-chart');
    this.studyHeatmap = page.getByTestId('study-heatmap');

    // Sections
    this.weakAreas = page.getByTestId('weak-areas');
    this.achievements = page.getByTestId('achievements');
    this.recentSessions = page.getByTestId('recent-sessions');

    // Actions
    this.startPracticeButton = page.getByRole('button', { name: /start practice/i });
    this.viewProgressLink = page.getByRole('link', { name: /view progress/i });

    // Navigation
    this.userMenu = page.getByTestId('user-menu');
  }

  async goto() {
    await this.page.goto('/dashboard');
  }

  async expectOnDashboard() {
    await expect(this.page).toHaveURL(/.*dashboard/);
  }

  async expectStatsVisible() {
    await expect(this.totalExercises).toBeVisible();
    await expect(this.accuracyStat).toBeVisible();
    await expect(this.currentStreak).toBeVisible();
    await expect(this.totalPoints).toBeVisible();
  }

  async getTotalExercises(): Promise<number> {
    const text = await this.totalExercises.textContent();
    return parseInt(text?.match(/\d+/)?.[0] || '0');
  }

  async getAccuracy(): Promise<number> {
    const text = await this.accuracyStat.textContent();
    return parseInt(text?.match(/\d+/)?.[0] || '0');
  }

  async getCurrentStreak(): Promise<number> {
    const text = await this.currentStreak.textContent();
    return parseInt(text?.match(/\d+/)?.[0] || '0');
  }

  async getTotalPoints(): Promise<number> {
    const text = await this.totalPoints.textContent();
    return parseInt(text?.match(/\d+/)?.[0] || '0');
  }

  async switchChartPeriod(period: 'week' | 'month' | 'all') {
    await this.page.click(`[data-testid="chart-period-${period}"]`);
  }

  async getWeakAreas(): Promise<string[]> {
    const items = await this.weakAreas.locator('[data-testid="weak-area-item"]').all();
    const areas: string[] = [];

    for (const item of items) {
      const text = await item.textContent();
      if (text) areas.push(text.trim());
    }

    return areas;
  }

  async practiceWeakArea(index: number = 0) {
    const practiceButtons = this.weakAreas.getByRole('button', { name: /practice/i });
    await practiceButtons.nth(index).click();
  }

  async getUnlockedAchievements(): Promise<number> {
    const unlocked = await this.achievements.locator('[data-unlocked="true"]').count();
    return unlocked;
  }

  async clickAchievement(index: number = 0) {
    const achievements = this.achievements.locator('[data-achievement]');
    await achievements.nth(index).click();
  }

  async startPractice() {
    await this.startPracticeButton.click();
    await this.page.waitForURL(/.*practice/);
  }

  async viewProgress() {
    await this.viewProgressLink.click();
    await this.page.waitForURL(/.*progress/);
  }

  async logout() {
    await this.userMenu.click();
    await this.page.click('text=Logout');
    await this.page.waitForURL(/.*login/);
  }
}

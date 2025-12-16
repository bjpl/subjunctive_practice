import { Page, Locator, expect } from '@playwright/test';

/**
 * Page Object Model for Practice Page
 */
export class PracticePage {
  readonly page: Page;

  // Setup
  readonly difficultySelect: Locator;
  readonly tenseSelect: Locator;
  readonly exerciseCountInput: Locator;
  readonly startButton: Locator;

  // Exercise
  readonly exerciseCard: Locator;
  readonly exercisePrompt: Locator;
  readonly answerInput: Locator;
  readonly submitButton: Locator;
  readonly skipButton: Locator;
  readonly nextButton: Locator;
  readonly pauseButton: Locator;
  readonly quitButton: Locator;

  // Feedback
  readonly correctIcon: Locator;
  readonly incorrectIcon: Locator;
  readonly explanation: Locator;
  readonly pointsEarned: Locator;

  // Progress
  readonly progressBar: Locator;
  readonly progressText: Locator;

  // Results
  readonly finalScore: Locator;
  readonly accuracyResult: Locator;
  readonly pointsResult: Locator;
  readonly practiceAgainButton: Locator;

  constructor(page: Page) {
    this.page = page;

    // Setup
    this.difficultySelect = page.getByTestId('difficulty-select');
    this.tenseSelect = page.getByTestId('tense-select');
    this.exerciseCountInput = page.locator('input[name="exerciseCount"]');
    this.startButton = page.getByRole('button', { name: /start practice/i });

    // Exercise
    this.exerciseCard = page.getByTestId('exercise-card');
    this.exercisePrompt = page.getByTestId('exercise-prompt');
    this.answerInput = page.getByTestId('answer-input');
    this.submitButton = page.getByRole('button', { name: /submit/i });
    this.skipButton = page.getByRole('button', { name: /skip/i });
    this.nextButton = page.getByRole('button', { name: /next/i });
    this.pauseButton = page.getByRole('button', { name: /pause/i });
    this.quitButton = page.getByRole('button', { name: /quit/i });

    // Feedback
    this.correctIcon = page.getByTestId('correct-icon');
    this.incorrectIcon = page.getByTestId('incorrect-icon');
    this.explanation = page.getByTestId('explanation');
    this.pointsEarned = page.locator('text=/\\+\\d+.*points/i');

    // Progress
    this.progressBar = page.getByTestId('progress-bar');
    this.progressText = page.locator('text=/\\d+\\s*\\/\\s*\\d+/');

    // Results
    this.finalScore = page.getByTestId('final-score');
    this.accuracyResult = page.getByTestId('accuracy-stat');
    this.pointsResult = page.getByTestId('points-earned');
    this.practiceAgainButton = page.getByRole('button', { name: /practice again/i });
  }

  async goto() {
    await this.page.goto('/practice');
  }

  async expectOnPracticePage() {
    await expect(this.page).toHaveURL(/.*practice/);
  }

  async selectDifficulty(difficulty: 'beginner' | 'intermediate' | 'advanced') {
    await this.difficultySelect.click();
    await this.page.click(`text=${difficulty}`);
  }

  async selectTense(tense: string) {
    await this.tenseSelect.click();
    await this.page.click(`text=${tense}`);
  }

  async setExerciseCount(count: number) {
    await this.exerciseCountInput.fill(count.toString());
  }

  async startPractice() {
    await this.startButton.click();
    await this.exerciseCard.waitFor({ state: 'visible' });
  }

  async startPracticeWithSettings(options: {
    difficulty?: 'beginner' | 'intermediate' | 'advanced';
    tense?: string;
    count?: number;
  }) {
    if (options.difficulty) {
      await this.selectDifficulty(options.difficulty);
    }
    if (options.tense) {
      await this.selectTense(options.tense);
    }
    if (options.count) {
      await this.setExerciseCount(options.count);
    }
    await this.startPractice();
  }

  async submitAnswer(answer: string) {
    await this.answerInput.fill(answer);
    await this.submitButton.click();
  }

  async submitAnswerWithEnter(answer: string) {
    await this.answerInput.fill(answer);
    await this.answerInput.press('Enter');
  }

  async skipExercise() {
    await this.skipButton.click();
  }

  async goToNext() {
    await this.nextButton.click();
  }

  async pauseSession() {
    await this.pauseButton.click();
  }

  async resumeSession() {
    await this.page.click('button:has-text("Resume")');
  }

  async quitSession(confirm: boolean = true) {
    await this.quitButton.click();

    if (confirm) {
      await this.page.click('button:has-text("Confirm")');
    } else {
      await this.page.click('button:has-text("Cancel")');
    }
  }

  async expectCorrectFeedback() {
    await expect(this.correctIcon).toBeVisible();
    await expect(this.page.getByText(/correct/i)).toBeVisible();
  }

  async expectIncorrectFeedback() {
    await expect(this.incorrectIcon).toBeVisible();
    await expect(this.page.getByText(/incorrect/i)).toBeVisible();
  }

  async getCurrentProgress(): Promise<{ current: number; total: number }> {
    const text = await this.progressText.textContent();
    const match = text?.match(/(\d+)\s*\/\s*(\d+)/);

    if (!match) {
      return { current: 0, total: 0 };
    }

    return {
      current: parseInt(match[1]),
      total: parseInt(match[2]),
    };
  }

  async getProgressPercentage(): Promise<number> {
    const value = await this.progressBar.getAttribute('value');
    return parseInt(value || '0');
  }

  async completeExercise(answer: string) {
    await this.submitAnswer(answer);
    await this.goToNext();
  }

  async completeSession(answers: string[]) {
    for (const answer of answers) {
      await this.submitAnswer(answer);

      // Wait for feedback
      await this.page.waitForTimeout(500);

      // Check if this is the last exercise
      const progress = await this.getCurrentProgress();
      if (progress.current < progress.total) {
        await this.goToNext();
      } else {
        // Last exercise - click next to see results
        await this.goToNext();
        break;
      }
    }
  }

  async expectSessionComplete() {
    await expect(this.page.getByText(/session complete/i)).toBeVisible();
    await expect(this.finalScore).toBeVisible();
  }

  async getFinalAccuracy(): Promise<number> {
    const text = await this.accuracyResult.textContent();
    return parseInt(text?.match(/\d+/)?.[0] || '0');
  }

  async getFinalPoints(): Promise<number> {
    const text = await this.pointsResult.textContent();
    return parseInt(text?.match(/\d+/)?.[0] || '0');
  }

  async startNewSession() {
    await this.practiceAgainButton.click();
    await expect(this.startButton).toBeVisible();
  }
}

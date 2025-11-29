/**
 * Unit tests for PracticeConfig component
 * Tests practice configuration UI, form validation, and configuration submission
 */

import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { PracticeConfig, type PracticeConfigOptions } from '@/components/practice/PracticeConfig';

describe('PracticeConfig Component', () => {
  const mockOnStartPractice = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  const defaultProps = {
    onStartPractice: mockOnStartPractice,
    isLoading: false,
  };

  describe('Initial Render', () => {
    it('should render all configuration sections', () => {
      render(<PracticeConfig {...defaultProps} />);

      expect(screen.getByText('Configure Your Practice Session')).toBeInTheDocument();
      expect(screen.getByText('Select Verbs to Practice')).toBeInTheDocument();
      expect(screen.getByText('Situation / Theme (Optional)')).toBeInTheDocument();
      expect(screen.getByText('Subjunctive Tense')).toBeInTheDocument();
      expect(screen.getByText('Trigger Category (WEIRDO)')).toBeInTheDocument();
      expect(screen.getByText('Grammatical Persons')).toBeInTheDocument();
      expect(screen.getByText('Difficulty Level')).toBeInTheDocument();
      expect(screen.getByText('Number of Exercises')).toBeInTheDocument();
    });

    it('should have default values selected', () => {
      render(<PracticeConfig {...defaultProps} />);

      // Default persons should be selected
      const yoButton = screen.getByRole('button', { name: 'yo' });
      const tuButton = screen.getByRole('button', { name: 'tú' });
      const elButton = screen.getByRole('button', { name: 'él/ella/usted' });

      expect(yoButton).toHaveClass(/default|primary/);
      expect(tuButton).toHaveClass(/default|primary/);
      expect(elButton).toHaveClass(/default|primary/);

      // Hints and explanations should be enabled
      expect(screen.getByText('Hints Enabled')).toBeInTheDocument();
      expect(screen.getByText('Explanations Enabled')).toBeInTheDocument();
    });

    it('should show start practice button', () => {
      render(<PracticeConfig {...defaultProps} />);

      const startButton = screen.getByRole('button', { name: /start practice session/i });
      expect(startButton).toBeInTheDocument();
      expect(startButton).not.toBeDisabled();
    });
  });

  describe('Verb Selection', () => {
    it('should open verb selection popover', async () => {
      const user = userEvent.setup();
      render(<PracticeConfig {...defaultProps} />);

      const verbButton = screen.getByRole('button', {
        name: /click to select verbs/i,
      });

      await user.click(verbButton);

      // Popover should show search input
      await waitFor(() => {
        expect(screen.getByPlaceholderText('Search verbs...')).toBeInTheDocument();
      });
    });

    it('should select and deselect verbs', async () => {
      const user = userEvent.setup();
      render(<PracticeConfig {...defaultProps} />);

      // Open verb popover
      const verbButton = screen.getByRole('button', {
        name: /click to select verbs/i,
      });
      await user.click(verbButton);

      // Wait for popover to open
      await waitFor(() => {
        expect(screen.getByPlaceholderText('Search verbs...')).toBeInTheDocument();
      });

      // Select "hablar"
      const hablarOption = screen.getByText('hablar');
      await user.click(hablarOption);

      // Verify button text updated
      await waitFor(() => {
        expect(screen.getByText('1 verb selected')).toBeInTheDocument();
      });

      // Click again to deselect
      await user.click(hablarOption);

      await waitFor(() => {
        expect(screen.getByText(/click to select verbs/i)).toBeInTheDocument();
      });
    });

    it('should filter verbs by search query', async () => {
      const user = userEvent.setup();
      render(<PracticeConfig {...defaultProps} />);

      // Open verb popover
      const verbButton = screen.getByRole('button', {
        name: /click to select verbs/i,
      });
      await user.click(verbButton);

      const searchInput = await screen.findByPlaceholderText('Search verbs...');

      // Search for "hab"
      await user.type(searchInput, 'hab');

      await waitFor(() => {
        expect(screen.getByText('hablar')).toBeInTheDocument();
        expect(screen.queryByText('comer')).not.toBeInTheDocument();
      });
    });

    it('should display selected verbs as badges', async () => {
      const user = userEvent.setup();
      render(<PracticeConfig {...defaultProps} />);

      // Open and select a verb
      const verbButton = screen.getByRole('button', {
        name: /click to select verbs/i,
      });
      await user.click(verbButton);

      const hablarOption = await screen.findByText('hablar');
      await user.click(hablarOption);

      // Close popover and check for badge
      await user.click(verbButton);

      await waitFor(() => {
        const badges = screen.getAllByText('hablar');
        expect(badges.length).toBeGreaterThan(0);
      });
    });

    it('should clear all selected verbs', async () => {
      const user = userEvent.setup();
      render(<PracticeConfig {...defaultProps} />);

      // Select multiple verbs
      const verbButton = screen.getByRole('button', {
        name: /click to select verbs/i,
      });
      await user.click(verbButton);

      const hablarOption = await screen.findByText('hablar');
      await user.click(hablarOption);

      const comerOption = screen.getByText('comer');
      await user.click(comerOption);

      await waitFor(() => {
        expect(screen.getByText('2 verbs selected')).toBeInTheDocument();
      });

      // Click clear selection
      const clearButton = screen.getByRole('button', { name: /clear selection/i });
      await user.click(clearButton);

      await waitFor(() => {
        expect(screen.getByText(/click to select verbs/i)).toBeInTheDocument();
      });
    });
  });

  describe('Theme/Context Selection', () => {
    it('should allow custom context input', async () => {
      const user = userEvent.setup();
      render(<PracticeConfig {...defaultProps} />);

      const contextInput = screen.getByPlaceholderText(/e.g., at a restaurant/i);

      await user.type(contextInput, 'traveling abroad');

      expect(contextInput).toHaveValue('traveling abroad');
      await waitFor(() => {
        expect(screen.getByText(/Exercises will be themed around/i)).toBeInTheDocument();
      });
    });

    it('should select quick theme suggestions', async () => {
      const user = userEvent.setup();
      render(<PracticeConfig {...defaultProps} />);

      const restaurantButton = screen.getByRole('button', { name: 'at a restaurant' });
      await user.click(restaurantButton);

      const contextInput = screen.getByPlaceholderText(/e.g., at a restaurant/i);
      expect(contextInput).toHaveValue('at a restaurant');
    });

    it('should toggle theme suggestion off', async () => {
      const user = userEvent.setup();
      render(<PracticeConfig {...defaultProps} />);

      const travelButton = screen.getByRole('button', { name: 'travel' });

      // Select
      await user.click(travelButton);
      const contextInput = screen.getByPlaceholderText(/e.g., at a restaurant/i);
      expect(contextInput).toHaveValue('travel');

      // Deselect
      await user.click(travelButton);
      expect(contextInput).toHaveValue('');
    });
  });

  describe('Person Selection', () => {
    it('should toggle person selection', async () => {
      const user = userEvent.setup();
      render(<PracticeConfig {...defaultProps} />);

      const nosotrosButton = screen.getByRole('button', { name: 'nosotros' });

      // Should start deselected
      expect(nosotrosButton).toHaveClass(/outline/);

      // Select
      await user.click(nosotrosButton);
      await waitFor(() => {
        expect(nosotrosButton).toHaveClass(/default|primary/);
      });

      // Deselect
      await user.click(nosotrosButton);
      await waitFor(() => {
        expect(nosotrosButton).toHaveClass(/outline/);
      });
    });

    it('should allow selecting all persons', async () => {
      const user = userEvent.setup();
      render(<PracticeConfig {...defaultProps} />);

      const persons = ['yo', 'tú', 'él/ella/usted', 'nosotros', 'vosotros', 'ellos/ustedes'];

      for (const person of persons.slice(3)) {
        // First 3 are already selected
        const button = screen.getByRole('button', { name: person });
        await user.click(button);
      }

      // All should be selected
      persons.forEach((person) => {
        const button = screen.getByRole('button', { name: person });
        expect(button).toHaveClass(/default|primary/);
      });
    });
  });

  describe('Options Configuration', () => {
    it('should toggle hints', async () => {
      const user = userEvent.setup();
      render(<PracticeConfig {...defaultProps} />);

      const hintsButton = screen.getByRole('button', { name: /hints enabled/i });

      await user.click(hintsButton);
      await waitFor(() => {
        expect(screen.getByText('Hints Disabled')).toBeInTheDocument();
      });

      await user.click(hintsButton);
      await waitFor(() => {
        expect(screen.getByText('Hints Enabled')).toBeInTheDocument();
      });
    });

    it('should toggle explanations', async () => {
      const user = userEvent.setup();
      render(<PracticeConfig {...defaultProps} />);

      const explanationsButton = screen.getByRole('button', { name: /explanations enabled/i });

      await user.click(explanationsButton);
      await waitFor(() => {
        expect(screen.getByText('Explanations Disabled')).toBeInTheDocument();
      });
    });
  });

  describe('Form Submission', () => {
    it('should submit configuration with default values', async () => {
      const user = userEvent.setup();
      render(<PracticeConfig {...defaultProps} />);

      const startButton = screen.getByRole('button', { name: /start practice session/i });
      await user.click(startButton);

      expect(mockOnStartPractice).toHaveBeenCalledTimes(1);

      const config: PracticeConfigOptions = mockOnStartPractice.mock.calls[0][0];

      // Should use all verbs when none selected
      expect(config.verbs.length).toBeGreaterThan(0);
      expect(config.tense).toBe('present_subjunctive');
      expect(config.persons).toEqual(['yo', 'tú', 'él/ella/usted']);
      expect(config.difficulty).toBe(2);
      expect(config.customContext).toBe('');
      expect(config.exerciseCount).toBe(10);
      expect(config.includeHints).toBe(true);
      expect(config.includeExplanations).toBe(true);
    });

    it('should submit configuration with custom selections', async () => {
      const user = userEvent.setup();
      render(<PracticeConfig {...defaultProps} />);

      // Select specific verbs
      const verbButton = screen.getByRole('button', { name: /click to select verbs/i });
      await user.click(verbButton);

      const hablarOption = await screen.findByText('hablar');
      await user.click(hablarOption);

      // Set custom context
      const contextInput = screen.getByPlaceholderText(/e.g., at a restaurant/i);
      await user.type(contextInput, 'job interview');

      // Click start
      const startButton = screen.getByRole('button', { name: /start practice session/i });
      await user.click(startButton);

      expect(mockOnStartPractice).toHaveBeenCalled();

      const config: PracticeConfigOptions = mockOnStartPractice.mock.calls[0][0];
      expect(config.verbs).toEqual(['hablar']);
      expect(config.customContext).toBe('job interview');
    });

    it('should be disabled when no persons selected', async () => {
      const user = userEvent.setup();
      render(<PracticeConfig {...defaultProps} />);

      // Deselect all default persons
      const yoButton = screen.getByRole('button', { name: 'yo' });
      const tuButton = screen.getByRole('button', { name: 'tú' });
      const elButton = screen.getByRole('button', { name: 'él/ella/usted' });

      await user.click(yoButton);
      await user.click(tuButton);
      await user.click(elButton);

      const startButton = screen.getByRole('button', { name: /start practice session/i });

      await waitFor(() => {
        expect(startButton).toBeDisabled();
      });
    });

    it('should show loading state', () => {
      render(<PracticeConfig onStartPractice={mockOnStartPractice} isLoading={true} />);

      const startButton = screen.getByRole('button', { name: /generating exercises/i });
      expect(startButton).toBeDisabled();
      expect(screen.getByText('Generating exercises...')).toBeInTheDocument();
    });
  });

  describe('Accessibility', () => {
    it('should have proper labels for form elements', () => {
      render(<PracticeConfig {...defaultProps} />);

      expect(screen.getByText('Select Verbs to Practice')).toBeInTheDocument();
      expect(screen.getByText('Situation / Theme (Optional)')).toBeInTheDocument();
      expect(screen.getByText('Subjunctive Tense')).toBeInTheDocument();
      expect(screen.getByText('Grammatical Persons')).toBeInTheDocument();
      expect(screen.getByText('Difficulty Level')).toBeInTheDocument();
      expect(screen.getByText('Number of Exercises')).toBeInTheDocument();
    });

    it('should have accessible button roles', () => {
      render(<PracticeConfig {...defaultProps} />);

      const buttons = screen.getAllByRole('button');
      expect(buttons.length).toBeGreaterThan(0);

      buttons.forEach((button) => {
        expect(button).toBeInTheDocument();
      });
    });
  });
});

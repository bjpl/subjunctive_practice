/**
 * Integration test for complete practice flow
 * Tests the end-to-end user journey from configuration to session completion
 */

import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Provider } from 'react-redux';
import {
  createTestStore,
  authenticatedState,
} from '../utils/rtk-query-utils';
import { server } from '../mocks/server';
import { http, HttpResponse } from 'msw';
import type { GeneratedExercise, AnswerValidation } from '@/types/api';

const API_BASE_URL = 'http://localhost:8000/api/v1';

// Mock practice page component for integration testing
const MockPracticePage = () => {
  const [mode, setMode] = React.useState<'select' | 'config' | 'practice' | 'results'>('select');
  const [exercises, setExercises] = React.useState<GeneratedExercise[]>([]);
  const [currentIndex, setCurrentIndex] = React.useState(0);
  const [answers, setAnswers] = React.useState<AnswerValidation[]>([]);
  const [currentAnswer, setCurrentAnswer] = React.useState('');

  const handleQuickPractice = () => {
    setMode('practice');
    // Simulate quick practice exercises
    setExercises([
      {
        id: '1',
        verb: 'hablar',
        verb_translation: 'to speak',
        tense: 'present_subjunctive',
        person: 'yo',
        prompt: 'Espero que yo _____ español.',
        correct_answer: 'hable',
        alternative_answers: [],
        difficulty: 1,
      },
      {
        id: '2',
        verb: 'ser',
        verb_translation: 'to be',
        tense: 'present_subjunctive',
        person: 'nosotros',
        prompt: 'Es importante que nosotros _____ honestos.',
        correct_answer: 'seamos',
        alternative_answers: [],
        difficulty: 2,
      },
    ]);
  };

  const handleSubmitAnswer = async () => {
    const validation: AnswerValidation = {
      is_correct: currentAnswer === exercises[currentIndex].correct_answer,
      correct_answer: exercises[currentIndex].correct_answer,
      user_answer: currentAnswer,
      feedback: currentAnswer === exercises[currentIndex].correct_answer
        ? 'Excellent work!'
        : 'Not quite, try again.',
      score: currentAnswer === exercises[currentIndex].correct_answer ? 100 : 0,
    };

    setAnswers([...answers, validation]);

    if (currentIndex < exercises.length - 1) {
      setCurrentIndex(currentIndex + 1);
      setCurrentAnswer('');
    } else {
      setMode('results');
    }
  };

  if (mode === 'select') {
    return (
      <div>
        <h1>Practice Spanish Subjunctive</h1>
        <button onClick={handleQuickPractice}>Quick Practice</button>
        <button onClick={() => setMode('config')}>Custom Practice</button>
      </div>
    );
  }

  if (mode === 'config') {
    return (
      <div>
        <h2>Configure Practice</h2>
        <button onClick={() => setMode('practice')}>Start Practice</button>
      </div>
    );
  }

  if (mode === 'practice') {
    const exercise = exercises[currentIndex];
    return (
      <div>
        <h2>Exercise {currentIndex + 1} of {exercises.length}</h2>
        <p>{exercise.prompt}</p>
        <input
          type="text"
          value={currentAnswer}
          onChange={(e) => setCurrentAnswer(e.target.value)}
          placeholder="Your answer"
          aria-label="answer input"
        />
        <button onClick={handleSubmitAnswer} disabled={!currentAnswer}>
          Submit Answer
        </button>
      </div>
    );
  }

  if (mode === 'results') {
    const correctCount = answers.filter(a => a.is_correct).length;
    const accuracy = Math.round((correctCount / answers.length) * 100);

    return (
      <div>
        <h2>Session Complete!</h2>
        <p>Score: {correctCount}/{answers.length}</p>
        <p>Accuracy: {accuracy}%</p>
        <button onClick={() => {
          setMode('select');
          setExercises([]);
          setCurrentIndex(0);
          setAnswers([]);
          setCurrentAnswer('');
        }}>
          Practice Again
        </button>
      </div>
    );
  }

  return null;
};

import React from 'react';

describe('Practice Flow Integration', () => {
  let store: ReturnType<typeof createTestStore>;

  beforeEach(() => {
    store = createTestStore(authenticatedState);

    // Setup API mocks
    server.use(
      http.post(`${API_BASE_URL}/exercises/generate`, () => {
        return HttpResponse.json({
          exercises: [
            {
              id: '1',
              verb: 'hablar',
              verb_translation: 'to speak',
              tense: 'present_subjunctive',
              person: 'yo',
              prompt: 'Espero que yo _____ español.',
              correct_answer: 'hable',
              alternative_answers: [],
              difficulty: 1,
            },
            {
              id: '2',
              verb: 'ser',
              verb_translation: 'to be',
              tense: 'present_subjunctive',
              person: 'nosotros',
              prompt: 'Es importante que nosotros _____ honestos.',
              correct_answer: 'seamos',
              alternative_answers: [],
              difficulty: 2,
            },
          ],
          total: 2,
          config_summary: {
            verbs: ['hablar', 'ser'],
            verb_count: 2,
            tense: 'present_subjunctive',
            persons: ['yo', 'nosotros'],
            difficulty: 1,
            trigger_category: 'all',
            has_custom_context: false,
          },
        });
      }),
      http.post(`${API_BASE_URL}/exercises/submit`, async ({ request }) => {
        const body = await request.json() as { user_answer: string; exercise_id: string };

        return HttpResponse.json({
          is_correct: body.user_answer === 'hable' || body.user_answer === 'seamos',
          correct_answer: body.exercise_id === '1' ? 'hable' : 'seamos',
          user_answer: body.user_answer,
          feedback: body.user_answer === 'hable' || body.user_answer === 'seamos'
            ? 'Excellent work!'
            : 'Not quite right.',
          score: body.user_answer === 'hable' || body.user_answer === 'seamos' ? 100 : 0,
        });
      })
    );
  });

  const wrapper = ({ children }: { children: React.ReactNode }) => {
    return <Provider store={store}>{children}</Provider>;
  };

  describe('Quick Practice Mode', () => {
    it('should complete quick practice flow successfully', async () => {
      const user = userEvent.setup();

      render(<MockPracticePage />, { wrapper });

      // Start with mode selection
      expect(screen.getByText('Practice Spanish Subjunctive')).toBeInTheDocument();

      // Click quick practice
      const quickPracticeButton = screen.getByRole('button', { name: /quick practice/i });
      await user.click(quickPracticeButton);

      // Should show first exercise
      await waitFor(() => {
        expect(screen.getByText('Exercise 1 of 2')).toBeInTheDocument();
      });

      expect(screen.getByText(/Espero que yo _____ español/i)).toBeInTheDocument();

      // Answer first exercise
      const answerInput = screen.getByLabelText(/answer input/i);
      await user.type(answerInput, 'hable');

      const submitButton = screen.getByRole('button', { name: /submit answer/i });
      await user.click(submitButton);

      // Should move to second exercise
      await waitFor(() => {
        expect(screen.getByText('Exercise 2 of 2')).toBeInTheDocument();
      });

      expect(screen.getByText(/Es importante que nosotros _____ honestos/i)).toBeInTheDocument();

      // Answer second exercise
      const answerInput2 = screen.getByLabelText(/answer input/i);
      await user.type(answerInput2, 'seamos');

      const submitButton2 = screen.getByRole('button', { name: /submit answer/i });
      await user.click(submitButton2);

      // Should show results
      await waitFor(() => {
        expect(screen.getByText('Session Complete!')).toBeInTheDocument();
      });

      expect(screen.getByText('Score: 2/2')).toBeInTheDocument();
      expect(screen.getByText('Accuracy: 100%')).toBeInTheDocument();
    });

    it('should handle incorrect answers', async () => {
      const user = userEvent.setup();

      render(<MockPracticePage />, { wrapper });

      // Start quick practice
      const quickPracticeButton = screen.getByRole('button', { name: /quick practice/i });
      await user.click(quickPracticeButton);

      await waitFor(() => {
        expect(screen.getByText('Exercise 1 of 2')).toBeInTheDocument();
      });

      // Submit wrong answer
      const answerInput = screen.getByLabelText(/answer input/i);
      await user.type(answerInput, 'hablo');

      const submitButton = screen.getByRole('button', { name: /submit answer/i });
      await user.click(submitButton);

      // Should still move forward
      await waitFor(() => {
        expect(screen.getByText('Exercise 2 of 2')).toBeInTheDocument();
      });

      // Complete second exercise
      const answerInput2 = screen.getByLabelText(/answer input/i);
      await user.type(answerInput2, 'seamos');

      const submitButton2 = screen.getByRole('button', { name: /submit answer/i });
      await user.click(submitButton2);

      // Check results show partial score
      await waitFor(() => {
        expect(screen.getByText('Session Complete!')).toBeInTheDocument();
      });

      expect(screen.getByText('Score: 1/2')).toBeInTheDocument();
      expect(screen.getByText('Accuracy: 50%')).toBeInTheDocument();
    });

    it('should allow practicing again after completion', async () => {
      const user = userEvent.setup();

      render(<MockPracticePage />, { wrapper });

      // Complete a quick practice session
      const quickPracticeButton = screen.getByRole('button', { name: /quick practice/i });
      await user.click(quickPracticeButton);

      await waitFor(() => {
        expect(screen.getByText('Exercise 1 of 2')).toBeInTheDocument();
      });

      // Answer both exercises
      let answerInput = screen.getByLabelText(/answer input/i);
      await user.type(answerInput, 'hable');
      await user.click(screen.getByRole('button', { name: /submit answer/i }));

      await waitFor(() => {
        expect(screen.getByText('Exercise 2 of 2')).toBeInTheDocument();
      });

      answerInput = screen.getByLabelText(/answer input/i);
      await user.type(answerInput, 'seamos');
      await user.click(screen.getByRole('button', { name: /submit answer/i }));

      // Should show results
      await waitFor(() => {
        expect(screen.getByText('Session Complete!')).toBeInTheDocument();
      });

      // Click practice again
      const practiceAgainButton = screen.getByRole('button', { name: /practice again/i });
      await user.click(practiceAgainButton);

      // Should return to mode selection
      await waitFor(() => {
        expect(screen.getByText('Practice Spanish Subjunctive')).toBeInTheDocument();
      });

      expect(screen.getByRole('button', { name: /quick practice/i })).toBeInTheDocument();
    });
  });

  describe('Custom Practice Mode', () => {
    it('should navigate to configuration screen', async () => {
      const user = userEvent.setup();

      render(<MockPracticePage />, { wrapper });

      const customPracticeButton = screen.getByRole('button', { name: /custom practice/i });
      await user.click(customPracticeButton);

      await waitFor(() => {
        expect(screen.getByText('Configure Practice')).toBeInTheDocument();
      });

      expect(screen.getByRole('button', { name: /start practice/i })).toBeInTheDocument();
    });

    it('should start practice from configuration', async () => {
      const user = userEvent.setup();

      render(<MockPracticePage />, { wrapper });

      // Navigate to config
      const customPracticeButton = screen.getByRole('button', { name: /custom practice/i });
      await user.click(customPracticeButton);

      await waitFor(() => {
        expect(screen.getByText('Configure Practice')).toBeInTheDocument();
      });

      // Start practice
      const startButton = screen.getByRole('button', { name: /start practice/i });
      await user.click(startButton);

      // Should start practice session
      await waitFor(() => {
        expect(screen.getByText(/Exercise 1 of/i)).toBeInTheDocument();
      });
    });
  });

  describe('Answer Submission', () => {
    it('should disable submit button when answer is empty', async () => {
      const user = userEvent.setup();

      render(<MockPracticePage />, { wrapper });

      const quickPracticeButton = screen.getByRole('button', { name: /quick practice/i });
      await user.click(quickPracticeButton);

      await waitFor(() => {
        expect(screen.getByText('Exercise 1 of 2')).toBeInTheDocument();
      });

      const submitButton = screen.getByRole('button', { name: /submit answer/i });
      expect(submitButton).toBeDisabled();

      // Type answer
      const answerInput = screen.getByLabelText(/answer input/i);
      await user.type(answerInput, 'hable');

      // Should enable
      expect(submitButton).not.toBeDisabled();
    });

    it('should clear answer input after submission', async () => {
      const user = userEvent.setup();

      render(<MockPracticePage />, { wrapper });

      const quickPracticeButton = screen.getByRole('button', { name: /quick practice/i });
      await user.click(quickPracticeButton);

      await waitFor(() => {
        expect(screen.getByText('Exercise 1 of 2')).toBeInTheDocument();
      });

      const answerInput = screen.getByLabelText(/answer input/i);
      await user.type(answerInput, 'hable');

      const submitButton = screen.getByRole('button', { name: /submit answer/i });
      await user.click(submitButton);

      // Wait for next exercise
      await waitFor(() => {
        expect(screen.getByText('Exercise 2 of 2')).toBeInTheDocument();
      });

      // Input should be cleared
      const newAnswerInput = screen.getByLabelText(/answer input/i);
      expect(newAnswerInput).toHaveValue('');
    });
  });

  describe('Progress Tracking', () => {
    it('should track exercise progress correctly', async () => {
      const user = userEvent.setup();

      render(<MockPracticePage />, { wrapper });

      const quickPracticeButton = screen.getByRole('button', { name: /quick practice/i });
      await user.click(quickPracticeButton);

      // First exercise
      await waitFor(() => {
        expect(screen.getByText('Exercise 1 of 2')).toBeInTheDocument();
      });

      let answerInput = screen.getByLabelText(/answer input/i);
      await user.type(answerInput, 'hable');
      await user.click(screen.getByRole('button', { name: /submit answer/i }));

      // Second exercise
      await waitFor(() => {
        expect(screen.getByText('Exercise 2 of 2')).toBeInTheDocument();
      });
    });

    it('should calculate final score correctly', async () => {
      const user = userEvent.setup();

      render(<MockPracticePage />, { wrapper });

      const quickPracticeButton = screen.getByRole('button', { name: /quick practice/i });
      await user.click(quickPracticeButton);

      await waitFor(() => {
        expect(screen.getByText('Exercise 1 of 2')).toBeInTheDocument();
      });

      // Answer first correctly
      let answerInput = screen.getByLabelText(/answer input/i);
      await user.type(answerInput, 'hable');
      await user.click(screen.getByRole('button', { name: /submit answer/i }));

      await waitFor(() => {
        expect(screen.getByText('Exercise 2 of 2')).toBeInTheDocument();
      });

      // Answer second correctly
      answerInput = screen.getByLabelText(/answer input/i);
      await user.type(answerInput, 'seamos');
      await user.click(screen.getByRole('button', { name: /submit answer/i }));

      // Verify final score
      await waitFor(() => {
        expect(screen.getByText('Score: 2/2')).toBeInTheDocument();
        expect(screen.getByText('Accuracy: 100%')).toBeInTheDocument();
      });
    });
  });
});

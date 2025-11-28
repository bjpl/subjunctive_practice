import { render, screen } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import { ExerciseCard } from '@/components/practice/ExerciseCard';
import type { Exercise } from '@/types';

expect.extend(toHaveNoViolations);

const mockExercise: Exercise = {
  id: '1',
  type: 'fill-blank',
  verb: 'hablar',
  tense: 'Present Subjunctive',
  sentence: 'Espero que tú _____ español.',
  blanks: ['hables'],
  correctAnswer: 'hables',
  explanation: 'After espero que, we use the present subjunctive.',
  difficulty: 'beginner',
  hints: ['Think about the -ar verb conjugation', 'The subject is tú'],
};

describe('ExerciseCard Component', () => {
  it('should render correctly with all props', () => {
    render(
      <ExerciseCard
        exercise={mockExercise}
        exerciseNumber={1}
        totalExercises={10}
      >
        <div>Child content</div>
      </ExerciseCard>
    );

    expect(screen.getByText('Question 1 of 10')).toBeInTheDocument();
    expect(screen.getByText('Beginner')).toBeInTheDocument();
    expect(screen.getByText('hablar')).toBeInTheDocument();
    expect(screen.getByText('Present Subjunctive')).toBeInTheDocument();
    expect(screen.getByText('Espero que tú _____ español.')).toBeInTheDocument();
    expect(screen.getByText('Child content')).toBeInTheDocument();
  });

  it('should display correct difficulty color for beginner', () => {
    const { container } = render(
      <ExerciseCard
        exercise={mockExercise}
        exerciseNumber={1}
        totalExercises={10}
      >
        <div>Content</div>
      </ExerciseCard>
    );

    const difficultyElement = container.querySelector('.difficulty-beginner');
    expect(difficultyElement).toBeInTheDocument();
  });

  it('should display correct difficulty color for intermediate', () => {
    const intermediateExercise = { ...mockExercise, difficulty: 'intermediate' as const };
    const { container } = render(
      <ExerciseCard
        exercise={intermediateExercise}
        exerciseNumber={1}
        totalExercises={10}
      >
        <div>Content</div>
      </ExerciseCard>
    );

    const difficultyElement = container.querySelector('.difficulty-intermediate');
    expect(difficultyElement).toBeInTheDocument();
    expect(screen.getByText('Intermediate')).toBeInTheDocument();
  });

  it('should display correct difficulty color for advanced', () => {
    const advancedExercise = { ...mockExercise, difficulty: 'advanced' as const };
    const { container } = render(
      <ExerciseCard
        exercise={advancedExercise}
        exerciseNumber={1}
        totalExercises={10}
      >
        <div>Content</div>
      </ExerciseCard>
    );

    const difficultyElement = container.querySelector('.difficulty-advanced');
    expect(difficultyElement).toBeInTheDocument();
    expect(screen.getByText('Advanced')).toBeInTheDocument();
  });

  it('should format exercise type correctly', () => {
    render(
      <ExerciseCard
        exercise={mockExercise}
        exerciseNumber={1}
        totalExercises={10}
      >
        <div>Content</div>
      </ExerciseCard>
    );

    expect(screen.getByText('FILL BLANK')).toBeInTheDocument();
  });

  it('should handle different exercise types', () => {
    const multipleChoiceExercise = { ...mockExercise, type: 'multiple-choice' as const };
    const { rerender } = render(
      <ExerciseCard
        exercise={multipleChoiceExercise}
        exerciseNumber={1}
        totalExercises={10}
      >
        <div>Content</div>
      </ExerciseCard>
    );

    expect(screen.getByText('MULTIPLE CHOICE')).toBeInTheDocument();

    const conjugationExercise = { ...mockExercise, type: 'conjugation' as const };
    rerender(
      <ExerciseCard
        exercise={conjugationExercise}
        exerciseNumber={1}
        totalExercises={10}
      >
        <div>Content</div>
      </ExerciseCard>
    );

    expect(screen.getByText('CONJUGATION')).toBeInTheDocument();
  });

  it('should have proper ARIA labels for sentence', () => {
    render(
      <ExerciseCard
        exercise={mockExercise}
        exerciseNumber={5}
        totalExercises={10}
      >
        <div>Content</div>
      </ExerciseCard>
    );

    const sentenceElement = screen.getByRole('main', { name: /exercise sentence/i });
    expect(sentenceElement).toBeInTheDocument();
  });

  it('should render children content correctly', () => {
    render(
      <ExerciseCard
        exercise={mockExercise}
        exerciseNumber={1}
        totalExercises={10}
      >
        <div data-testid="child-content">
          <input placeholder="Answer here" />
          <button>Submit</button>
        </div>
      </ExerciseCard>
    );

    expect(screen.getByTestId('child-content')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Answer here')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /submit/i })).toBeInTheDocument();
  });

  it('should not have accessibility violations', async () => {
    const { container } = render(
      <ExerciseCard
        exercise={mockExercise}
        exerciseNumber={1}
        totalExercises={10}
      >
        <div>Content</div>
      </ExerciseCard>
    );

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('should display correct progress indication', () => {
    render(
      <ExerciseCard
        exercise={mockExercise}
        exerciseNumber={7}
        totalExercises={15}
      >
        <div>Content</div>
      </ExerciseCard>
    );

    expect(screen.getByText('Question 7 of 15')).toBeInTheDocument();
  });

  it('should capitalize difficulty correctly', () => {
    const { rerender } = render(
      <ExerciseCard
        exercise={mockExercise}
        exerciseNumber={1}
        totalExercises={10}
      >
        <div>Content</div>
      </ExerciseCard>
    );

    expect(screen.getByText('Beginner')).toBeInTheDocument();

    const intermediateExercise = { ...mockExercise, difficulty: 'intermediate' as const };
    rerender(
      <ExerciseCard
        exercise={intermediateExercise}
        exerciseNumber={1}
        totalExercises={10}
      >
        <div>Content</div>
      </ExerciseCard>
    );

    expect(screen.getByText('Intermediate')).toBeInTheDocument();
  });
});

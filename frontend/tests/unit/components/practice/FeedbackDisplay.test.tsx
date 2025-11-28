import { render, screen } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import { FeedbackDisplay } from '@/components/practice/FeedbackDisplay';

expect.extend(toHaveNoViolations);

describe('FeedbackDisplay Component', () => {
  it('should not render when show is false', () => {
    const { container } = render(
      <FeedbackDisplay isCorrect={true} show={false} />
    );

    expect(container.firstChild).toBeNull();
  });

  it('should render success message when answer is correct', () => {
    render(
      <FeedbackDisplay
        isCorrect={true}
        show={true}
      />
    );

    expect(screen.getByText('Correct!')).toBeInTheDocument();
    expect(screen.getByText('Great job! Keep it up!')).toBeInTheDocument();
  });

  it('should render error message when answer is incorrect', () => {
    render(
      <FeedbackDisplay
        isCorrect={false}
        show={true}
      />
    );

    expect(screen.getByText('Not quite right')).toBeInTheDocument();
  });

  it('should display user answer when incorrect', () => {
    render(
      <FeedbackDisplay
        isCorrect={false}
        userAnswer="hablo"
        show={true}
      />
    );

    expect(screen.getByText('Your answer:')).toBeInTheDocument();
    expect(screen.getByText('hablo')).toBeInTheDocument();
  });

  it('should display correct answer when provided', () => {
    render(
      <FeedbackDisplay
        isCorrect={false}
        correctAnswer="hable"
        userAnswer="hablo"
        show={true}
      />
    );

    expect(screen.getByText('Correct answer:')).toBeInTheDocument();
    expect(screen.getByText('hable')).toBeInTheDocument();
  });

  it('should handle array of correct answers', () => {
    render(
      <FeedbackDisplay
        isCorrect={false}
        correctAnswer={['hable', 'hables']}
        show={true}
      />
    );

    expect(screen.getByText('hable, hables')).toBeInTheDocument();
  });

  it('should display explanation when provided', () => {
    render(
      <FeedbackDisplay
        isCorrect={false}
        explanation="After 'espero que', we use the present subjunctive."
        show={true}
      />
    );

    expect(screen.getByText('Explanation')).toBeInTheDocument();
    expect(screen.getByText("After 'espero que', we use the present subjunctive.")).toBeInTheDocument();
  });

  it('should apply success styling for correct answers', () => {
    const { container } = render(
      <FeedbackDisplay
        isCorrect={true}
        show={true}
      />
    );

    const feedback = container.querySelector('.feedback-display');
    expect(feedback).toHaveClass('feedback-success');
  });

  it('should apply error styling for incorrect answers', () => {
    const { container } = render(
      <FeedbackDisplay
        isCorrect={false}
        show={true}
      />
    );

    const feedback = container.querySelector('.feedback-display');
    expect(feedback).toHaveClass('feedback-error');
  });

  it('should have proper ARIA attributes', () => {
    const { container } = render(
      <FeedbackDisplay
        isCorrect={true}
        show={true}
      />
    );

    const feedback = container.querySelector('.feedback-display');
    expect(feedback).toHaveAttribute('role', 'alert');
    expect(feedback).toHaveAttribute('aria-live', 'polite');
  });

  it('should not show user answer section when answer is correct', () => {
    render(
      <FeedbackDisplay
        isCorrect={true}
        userAnswer="hable"
        correctAnswer="hable"
        show={true}
      />
    );

    expect(screen.queryByText('Your answer:')).not.toBeInTheDocument();
    expect(screen.queryByText('Correct answer:')).not.toBeInTheDocument();
  });

  it('should show explanation for both correct and incorrect answers', () => {
    const { rerender } = render(
      <FeedbackDisplay
        isCorrect={true}
        explanation="This is the subjunctive form."
        show={true}
      />
    );

    expect(screen.getByText('Explanation')).toBeInTheDocument();
    expect(screen.getByText('This is the subjunctive form.')).toBeInTheDocument();

    rerender(
      <FeedbackDisplay
        isCorrect={false}
        explanation="This is the subjunctive form."
        show={true}
      />
    );

    expect(screen.getByText('Explanation')).toBeInTheDocument();
    expect(screen.getByText('This is the subjunctive form.')).toBeInTheDocument();
  });

  it('should handle empty string correct answer', () => {
    render(
      <FeedbackDisplay
        isCorrect={false}
        correctAnswer=""
        show={true}
      />
    );

    expect(screen.getByText('Correct answer:')).toBeInTheDocument();
  });

  it('should handle undefined correct answer', () => {
    render(
      <FeedbackDisplay
        isCorrect={false}
        correctAnswer={undefined}
        show={true}
      />
    );

    expect(screen.queryByText('Correct answer:')).not.toBeInTheDocument();
  });

  it('should not have accessibility violations for success state', async () => {
    const { container } = render(
      <FeedbackDisplay
        isCorrect={true}
        show={true}
      />
    );

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('should not have accessibility violations for error state', async () => {
    const { container } = render(
      <FeedbackDisplay
        isCorrect={false}
        userAnswer="wrong"
        correctAnswer="right"
        explanation="Explanation here"
        show={true}
      />
    );

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('should display complete feedback with all props', () => {
    render(
      <FeedbackDisplay
        isCorrect={false}
        userAnswer="hablo"
        correctAnswer={['hable', 'hables']}
        explanation="Use the subjunctive after expressions of desire."
        show={true}
      />
    );

    expect(screen.getByText('Not quite right')).toBeInTheDocument();
    expect(screen.getByText('Your answer:')).toBeInTheDocument();
    expect(screen.getByText('hablo')).toBeInTheDocument();
    expect(screen.getByText('Correct answer:')).toBeInTheDocument();
    expect(screen.getByText('hable, hables')).toBeInTheDocument();
    expect(screen.getByText('Explanation')).toBeInTheDocument();
    expect(screen.getByText('Use the subjunctive after expressions of desire.')).toBeInTheDocument();
  });

  it('should render SVG icons correctly', () => {
    const { container, rerender } = render(
      <FeedbackDisplay isCorrect={true} show={true} />
    );

    let icon = container.querySelector('.feedback-icon svg');
    expect(icon).toBeInTheDocument();

    rerender(<FeedbackDisplay isCorrect={false} show={true} />);

    icon = container.querySelector('.feedback-icon svg');
    expect(icon).toBeInTheDocument();
  });

  it('should toggle visibility based on show prop', () => {
    const { container, rerender } = render(
      <FeedbackDisplay isCorrect={true} show={false} />
    );

    expect(container.firstChild).toBeNull();

    rerender(<FeedbackDisplay isCorrect={true} show={true} />);

    expect(screen.getByText('Correct!')).toBeInTheDocument();
  });
});

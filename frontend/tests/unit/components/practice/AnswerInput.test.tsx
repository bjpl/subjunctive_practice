import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { axe, toHaveNoViolations } from 'jest-axe';
import { AnswerInput } from '@/components/practice/AnswerInput';

expect.extend(toHaveNoViolations);

describe('AnswerInput Component', () => {
  const mockOnChange = jest.fn();
  const mockOnSubmit = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should render correctly with default props', () => {
    render(<AnswerInput value="" onChange={mockOnChange} />);

    const input = screen.getByRole('textbox', { name: /your answer/i });
    expect(input).toBeInTheDocument();
    expect(input).toHaveAttribute('placeholder', 'Type your answer here...');
    expect(input).toHaveAttribute('autocomplete', 'off');
    expect(input).toHaveAttribute('spellcheck', 'false');
  });

  it('should call onChange when user types', async () => {
    const user = userEvent.setup();
    render(<AnswerInput value="" onChange={mockOnChange} />);

    const input = screen.getByRole('textbox');
    await user.type(input, 'hable');

    expect(mockOnChange).toHaveBeenCalledWith('h');
    expect(mockOnChange).toHaveBeenCalledWith('a');
    expect(mockOnChange).toHaveBeenCalledWith('b');
    expect(mockOnChange).toHaveBeenCalledWith('l');
    expect(mockOnChange).toHaveBeenCalledWith('e');
  });

  it('should call onSubmit when Enter key is pressed', async () => {
    const user = userEvent.setup();
    render(<AnswerInput value="hable" onChange={mockOnChange} onSubmit={mockOnSubmit} />);

    const input = screen.getByRole('textbox');
    await user.type(input, '{Enter}');

    expect(mockOnSubmit).toHaveBeenCalledTimes(1);
  });

  it('should not call onSubmit when Enter is pressed if disabled', async () => {
    const user = userEvent.setup();
    render(
      <AnswerInput
        value="hable"
        onChange={mockOnChange}
        onSubmit={mockOnSubmit}
        disabled
      />
    );

    const input = screen.getByRole('textbox');
    await user.type(input, '{Enter}');

    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it('should not call onSubmit when Enter is pressed if no handler provided', async () => {
    const user = userEvent.setup();
    render(<AnswerInput value="hable" onChange={mockOnChange} />);

    const input = screen.getByRole('textbox');
    await user.type(input, '{Enter}');

    // Should not throw error
    expect(mockOnChange).toHaveBeenCalled();
  });

  it('should display correct state when answer is correct', () => {
    const { container } = render(
      <AnswerInput value="hable" onChange={mockOnChange} isCorrect />
    );

    const input = screen.getByRole('textbox');
    expect(input).toHaveClass('answer-input-correct');

    const successIcon = container.querySelector('.answer-input-icon-success');
    expect(successIcon).toBeInTheDocument();
    expect(screen.getByLabelText('Correct')).toBeInTheDocument();
  });

  it('should display correct state when answer is incorrect', () => {
    const { container } = render(
      <AnswerInput value="hablo" onChange={mockOnChange} isIncorrect />
    );

    const input = screen.getByRole('textbox');
    expect(input).toHaveClass('answer-input-incorrect');
    expect(input).toHaveAttribute('aria-invalid', 'true');

    const errorIcon = container.querySelector('.answer-input-icon-error');
    expect(errorIcon).toBeInTheDocument();
    expect(screen.getByLabelText('Incorrect')).toBeInTheDocument();
  });

  it('should apply disabled styling when disabled', () => {
    render(<AnswerInput value="" onChange={mockOnChange} disabled />);

    const input = screen.getByRole('textbox');
    expect(input).toBeDisabled();
    expect(input).toHaveClass('answer-input-disabled');
  });

  it('should use custom placeholder', () => {
    render(
      <AnswerInput
        value=""
        onChange={mockOnChange}
        placeholder="Enter conjugation"
      />
    );

    const input = screen.getByPlaceholderText('Enter conjugation');
    expect(input).toBeInTheDocument();
  });

  it('should not autofocus when autoFocus is false', () => {
    render(<AnswerInput value="" onChange={mockOnChange} autoFocus={false} />);

    const input = screen.getByRole('textbox');
    expect(input).not.toHaveFocus();
  });

  it('should have proper ARIA attributes for errors', () => {
    render(<AnswerInput value="wrong" onChange={mockOnChange} isIncorrect />);

    const input = screen.getByRole('textbox');
    expect(input).toHaveAttribute('aria-invalid', 'true');
    expect(input).toHaveAttribute('aria-describedby', 'answer-error');
  });

  it('should not have aria-describedby when answer is correct', () => {
    render(<AnswerInput value="correct" onChange={mockOnChange} isCorrect />);

    const input = screen.getByRole('textbox');
    expect(input).not.toHaveAttribute('aria-describedby');
    expect(input).toHaveAttribute('aria-invalid', 'false');
  });

  it('should display value correctly', () => {
    render(<AnswerInput value="hable" onChange={mockOnChange} />);

    const input = screen.getByRole('textbox');
    expect(input).toHaveValue('hable');
  });

  it('should update value when props change', () => {
    const { rerender } = render(<AnswerInput value="hab" onChange={mockOnChange} />);

    let input = screen.getByRole('textbox');
    expect(input).toHaveValue('hab');

    rerender(<AnswerInput value="hable" onChange={mockOnChange} />);

    input = screen.getByRole('textbox');
    expect(input).toHaveValue('hable');
  });

  it('should show both correct and incorrect icons appropriately', () => {
    const { rerender, container } = render(
      <AnswerInput value="test" onChange={mockOnChange} />
    );

    expect(container.querySelector('.answer-input-icon')).not.toBeInTheDocument();

    rerender(<AnswerInput value="test" onChange={mockOnChange} isCorrect />);
    expect(container.querySelector('.answer-input-icon-success')).toBeInTheDocument();
    expect(container.querySelector('.answer-input-icon-error')).not.toBeInTheDocument();

    rerender(<AnswerInput value="test" onChange={mockOnChange} isIncorrect />);
    expect(container.querySelector('.answer-input-icon-success')).not.toBeInTheDocument();
    expect(container.querySelector('.answer-input-icon-error')).toBeInTheDocument();
  });

  it('should not have accessibility violations', async () => {
    const { container } = render(
      <AnswerInput value="test answer" onChange={mockOnChange} />
    );

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('should not have accessibility violations when showing error', async () => {
    const { container } = render(
      <AnswerInput value="wrong" onChange={mockOnChange} isIncorrect />
    );

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('should handle rapid typing correctly', async () => {
    const user = userEvent.setup();
    render(<AnswerInput value="" onChange={mockOnChange} />);

    const input = screen.getByRole('textbox');
    await user.type(input, 'quicktyping');

    expect(mockOnChange).toHaveBeenCalledTimes('quicktyping'.length);
  });

  it('should prevent typing when disabled', async () => {
    const user = userEvent.setup();
    render(<AnswerInput value="" onChange={mockOnChange} disabled />);

    const input = screen.getByRole('textbox');
    await user.type(input, 'test');

    expect(mockOnChange).not.toHaveBeenCalled();
  });
});

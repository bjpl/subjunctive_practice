import React from 'react';
import './AnswerInput.css';

interface AnswerInputProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit?: () => void;
  disabled?: boolean;
  isCorrect?: boolean;
  isIncorrect?: boolean;
  placeholder?: string;
  autoFocus?: boolean;
}

export const AnswerInput: React.FC<AnswerInputProps> = ({
  value,
  onChange,
  onSubmit,
  disabled = false,
  isCorrect = false,
  isIncorrect = false,
  placeholder = 'Type your answer here...',
  autoFocus = true,
}) => {
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && onSubmit && !disabled) {
      onSubmit();
    }
  };

  const getInputClass = () => {
    const classes = ['answer-input'];
    if (isCorrect) classes.push('answer-input-correct');
    if (isIncorrect) classes.push('answer-input-incorrect');
    if (disabled) classes.push('answer-input-disabled');
    return classes.join(' ');
  };

  return (
    <div className="answer-input-wrapper">
      <label htmlFor="answer" className="answer-input-label">
        Your Answer
      </label>

      <div className="answer-input-container">
        <input
          id="answer"
          type="text"
          className={getInputClass()}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={disabled}
          placeholder={placeholder}
          autoFocus={autoFocus}
          autoComplete="off"
          spellCheck="false"
          aria-invalid={isIncorrect}
          aria-describedby={isIncorrect ? 'answer-error' : undefined}
        />

        {isCorrect && (
          <div className="answer-input-icon answer-input-icon-success" aria-label="Correct">
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <polyline points="20 6 9 17 4 12" />
            </svg>
          </div>
        )}

        {isIncorrect && (
          <div className="answer-input-icon answer-input-icon-error" aria-label="Incorrect">
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <circle cx="12" cy="12" r="10" />
              <line x1="15" y1="9" x2="9" y2="15" />
              <line x1="9" y1="9" x2="15" y2="15" />
            </svg>
          </div>
        )}
      </div>
    </div>
  );
};

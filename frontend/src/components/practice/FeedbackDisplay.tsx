import React from 'react';
import './FeedbackDisplay.css';

interface FeedbackDisplayProps {
  isCorrect: boolean;
  correctAnswer?: string | string[];
  userAnswer?: string;
  explanation?: string;
  show: boolean;
}

export const FeedbackDisplay: React.FC<FeedbackDisplayProps> = ({
  isCorrect,
  correctAnswer,
  userAnswer,
  explanation,
  show,
}) => {
  if (!show) return null;

  const formatAnswer = (answer: string | string[] | undefined): string => {
    if (!answer) return '';
    return Array.isArray(answer) ? answer.join(', ') : answer;
  };

  return (
    <div
      className={`feedback-display ${isCorrect ? 'feedback-success' : 'feedback-error'}`}
      role="alert"
      aria-live="polite"
    >
      <div className="feedback-header">
        <div className="feedback-icon">
          {isCorrect ? (
            <svg
              width="32"
              height="32"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
              <polyline points="22 4 12 14.01 9 11.01" />
            </svg>
          ) : (
            <svg
              width="32"
              height="32"
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
          )}
        </div>

        <div className="feedback-title">
          <h3>{isCorrect ? 'Correct!' : 'Not quite right'}</h3>
          {isCorrect && <p>Great job! Keep it up!</p>}
        </div>
      </div>

      {!isCorrect && (
        <div className="feedback-answers">
          {userAnswer && (
            <div className="feedback-answer-row">
              <span className="feedback-answer-label">Your answer:</span>
              <span className="feedback-answer-value feedback-answer-incorrect">
                {userAnswer}
              </span>
            </div>
          )}

          {correctAnswer && (
            <div className="feedback-answer-row">
              <span className="feedback-answer-label">Correct answer:</span>
              <span className="feedback-answer-value feedback-answer-correct">
                {formatAnswer(correctAnswer)}
              </span>
            </div>
          )}
        </div>
      )}

      {explanation && (
        <div className="feedback-explanation">
          <h4>Explanation</h4>
          <p>{explanation}</p>
        </div>
      )}
    </div>
  );
};

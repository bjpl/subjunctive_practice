import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import './HintButton.css';

interface HintButtonProps {
  hints: string[];
  onHintUsed?: (hintIndex: number) => void;
  disabled?: boolean;
}

export const HintButton: React.FC<HintButtonProps> = ({
  hints,
  onHintUsed,
  disabled = false,
}) => {
  const [currentHintIndex, setCurrentHintIndex] = useState(-1);
  const [showHint, setShowHint] = useState(false);

  const hasMoreHints = currentHintIndex < hints.length - 1;
  const currentHint = currentHintIndex >= 0 ? hints[currentHintIndex] : null;

  const handleRequestHint = () => {
    if (hasMoreHints) {
      const nextIndex = currentHintIndex + 1;
      setCurrentHintIndex(nextIndex);
      setShowHint(true);
      onHintUsed?.(nextIndex);
    }
  };

  const handleCloseHint = () => {
    setShowHint(false);
  };

  return (
    <div className="hint-button-wrapper">
      <Button
        variant="ghost"
        size="sm"
        onClick={handleRequestHint}
        disabled={disabled || !hasMoreHints}
        aria-label={`Request hint ${currentHintIndex + 2} of ${hints.length}`}
      >
        <svg
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <circle cx="12" cy="12" r="10" />
          <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" />
          <line x1="12" y1="17" x2="12.01" y2="17" />
        </svg>
        {hasMoreHints
          ? `Get Hint (${currentHintIndex + 2}/${hints.length})`
          : 'No More Hints'}
      </Button>

      {showHint && currentHint && (
        <div className="hint-display" role="alert" aria-live="polite">
          <div className="hint-header">
            <div className="hint-icon">
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M9 18h6" />
                <path d="M10 22h4" />
                <path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 0 1 8.91 14" />
              </svg>
            </div>
            <span className="hint-title">Hint {currentHintIndex + 1}</span>
            <button
              className="hint-close"
              onClick={handleCloseHint}
              aria-label="Close hint"
              type="button"
            >
              <svg
                width="18"
                height="18"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
          </div>
          <p className="hint-content">{currentHint}</p>
        </div>
      )}
    </div>
  );
};

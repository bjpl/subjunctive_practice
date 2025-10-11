import React from 'react';
import './ProgressBar.css';

interface ProgressBarProps {
  current: number;
  total: number;
  label?: string;
  showPercentage?: boolean;
  color?: 'primary' | 'success' | 'warning';
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  current,
  total,
  label,
  showPercentage = true,
  color = 'primary',
}) => {
  const percentage = Math.round((current / total) * 100);
  const progressWidth = `${percentage}%`;

  return (
    <div className="progress-bar-wrapper">
      {(label || showPercentage) && (
        <div className="progress-bar-header">
          {label && <span className="progress-bar-label">{label}</span>}
          {showPercentage && (
            <span className="progress-bar-percentage" aria-label={`${percentage}% complete`}>
              {percentage}%
            </span>
          )}
        </div>
      )}

      <div
        className="progress-bar-track"
        role="progressbar"
        aria-valuenow={current}
        aria-valuemin={0}
        aria-valuemax={total}
        aria-label={label || 'Progress'}
      >
        <div
          className={`progress-bar-fill progress-bar-${color}`}
          style={{ width: progressWidth }}
        >
          <span className="sr-only">{percentage}% complete</span>
        </div>
      </div>

      <div className="progress-bar-footer">
        <span className="progress-bar-count">
          {current} of {total}
        </span>
      </div>
    </div>
  );
};

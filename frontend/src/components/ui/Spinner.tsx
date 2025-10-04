import React from 'react';
import './Spinner.css';

interface SpinnerProps {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  color?: string;
  label?: string;
}

export const Spinner: React.FC<SpinnerProps> = ({
  size = 'md',
  color,
  label = 'Loading',
}) => {
  return (
    <div className={`spinner-wrapper spinner-${size}`} role="status" aria-label={label}>
      <svg
        className="spinner-svg"
        viewBox="0 0 50 50"
        style={color ? { color } : undefined}
      >
        <circle
          className="spinner-circle"
          cx="25"
          cy="25"
          r="20"
          fill="none"
          strokeWidth="4"
        />
      </svg>
      <span className="sr-only">{label}</span>
    </div>
  );
};

export const FullPageSpinner: React.FC<{ label?: string }> = ({ label }) => {
  return (
    <div className="spinner-fullpage">
      <Spinner size="xl" label={label} />
    </div>
  );
};

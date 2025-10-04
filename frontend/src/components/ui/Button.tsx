import React from 'react';
import { ButtonProps } from '../../types';
import './Button.css';

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  fullWidth = false,
  loading = false,
  disabled = false,
  type = 'button',
  onClick,
  children,
  className = '',
  ariaLabel,
}) => {
  const baseClasses = 'btn';
  const variantClass = `btn-${variant}`;
  const sizeClass = `btn-${size}`;
  const widthClass = fullWidth ? 'btn-full-width' : '';
  const disabledClass = (disabled || loading) ? 'btn-disabled' : '';

  const classes = [
    baseClasses,
    variantClass,
    sizeClass,
    widthClass,
    disabledClass,
    className,
  ].filter(Boolean).join(' ');

  return (
    <button
      type={type}
      className={classes}
      onClick={onClick}
      disabled={disabled || loading}
      aria-label={ariaLabel || (typeof children === 'string' ? children : undefined)}
      aria-busy={loading}
    >
      {loading && (
        <span className="btn-spinner" role="status" aria-label="Loading">
          <svg className="spinner" viewBox="0 0 24 24">
            <circle
              className="spinner-circle"
              cx="12"
              cy="12"
              r="10"
              fill="none"
              strokeWidth="3"
            />
          </svg>
        </span>
      )}
      <span className={loading ? 'btn-content-loading' : ''}>{children}</span>
    </button>
  );
};

import React from 'react';
import { InputProps } from '../../types';
import './Input.css';

export const Input: React.FC<InputProps> = ({
  id,
  name,
  label,
  type = 'text',
  value,
  onChange,
  onBlur,
  error,
  helpText,
  placeholder,
  disabled = false,
  required = false,
  autoComplete,
  className = '',
}) => {
  const inputClasses = [
    'input',
    error ? 'input-error' : '',
    disabled ? 'input-disabled' : '',
    className,
  ].filter(Boolean).join(' ');

  return (
    <div className="input-wrapper">
      <label htmlFor={id} className="input-label">
        {label}
        {required && <span className="input-required" aria-label="required"> *</span>}
      </label>

      <input
        id={id}
        name={name}
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onBlur={onBlur}
        placeholder={placeholder}
        disabled={disabled}
        required={required}
        autoComplete={autoComplete}
        className={inputClasses}
        aria-invalid={error ? 'true' : 'false'}
        aria-describedby={
          error ? `${id}-error` : helpText ? `${id}-help` : undefined
        }
      />

      {helpText && !error && (
        <p id={`${id}-help`} className="input-help">
          {helpText}
        </p>
      )}

      {error && (
        <p id={`${id}-error`} className="input-error-message" role="alert">
          {error}
        </p>
      )}
    </div>
  );
};

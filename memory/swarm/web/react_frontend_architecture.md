# React Frontend Architecture
## 20 Modules for Spanish Subjunctive Learning Web App

### Overview
Modern React/TypeScript frontend replacing 135+ PyQt desktop UI modules with responsive, accessible web components.

---

## Module Structure (20 modules)

### 1. Core Components (8 modules)

#### `src/components/ExerciseCard.tsx` - Primary Exercise Interface
```typescript
import React, { useState, useEffect, useRef } from 'react';
import { ExerciseType, Exercise, ExerciseResult } from '../types';
import { AnswerInput } from './AnswerInput';
import { MultipleChoice } from './MultipleChoice';
import { FeedbackDisplay } from './FeedbackDisplay';
import { useAccessibility } from '../hooks/useAccessibility';

interface ExerciseCardProps {
  exercise: Exercise;
  onSubmit: (answer: string, responseTime: number) => void;
  showHint?: boolean;
  allowSkip?: boolean;
  className?: string;
}

export const ExerciseCard: React.FC<ExerciseCardProps> = ({
  exercise,
  onSubmit,
  showHint = false,
  allowSkip = false,
  className = ''
}) => {
  const [userAnswer, setUserAnswer] = useState('');
  const [startTime, setStartTime] = useState(Date.now());
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [feedback, setFeedback] = useState<ExerciseResult | null>(null);
  const [hintsUsed, setHintsUsed] = useState(0);
  
  const cardRef = useRef<HTMLDivElement>(null);
  const { announceToScreenReader, focusElement } = useAccessibility();

  useEffect(() => {
    setStartTime(Date.now());
    setUserAnswer('');
    setIsSubmitted(false);
    setFeedback(null);
    setHintsUsed(0);
    
    // Announce new exercise to screen readers
    announceToScreenReader(`New exercise: ${exercise.question}`);
    
    // Focus the exercise card
    focusElement(cardRef.current);
  }, [exercise.id]);

  const handleSubmit = () => {
    const responseTime = Date.now() - startTime;
    setIsSubmitted(true);
    onSubmit(userAnswer, responseTime);
  };

  const handleShowHint = () => {
    setHintsUsed(prev => prev + 1);
    announceToScreenReader('Hint displayed');
  };

  const renderExerciseInput = () => {
    switch (exercise.exercise_type) {
      case ExerciseType.MULTIPLE_CHOICE:
        return (
          <MultipleChoice
            options={exercise.options || []}
            value={userAnswer}
            onChange={setUserAnswer}
            disabled={isSubmitted}
            name={`exercise-${exercise.id}`}
            aria-labelledby="exercise-question"
          />
        );
      
      case ExerciseType.CONJUGATION:
      case ExerciseType.FILL_BLANK:
        return (
          <AnswerInput
            value={userAnswer}
            onChange={setUserAnswer}
            onSubmit={handleSubmit}
            placeholder="Type your answer..."
            disabled={isSubmitted}
            autoComplete="off"
            aria-labelledby="exercise-question"
            suggestions={exercise.metadata?.suggestions || []}
          />
        );
      
      default:
        return (
          <AnswerInput
            value={userAnswer}
            onChange={setUserAnswer}
            onSubmit={handleSubmit}
            placeholder="Type your answer..."
            disabled={isSubmitted}
            aria-labelledby="exercise-question"
          />
        );
    }
  };

  return (
    <div
      ref={cardRef}
      className={`exercise-card bg-white rounded-lg shadow-md p-6 max-w-2xl mx-auto ${className}`}
      role="region"
      aria-labelledby="exercise-question"
      tabIndex={-1}
    >
      {/* Exercise Header */}
      <div className="exercise-header mb-6">
        <div className="exercise-meta flex items-center justify-between mb-4">
          <span className="difficulty-badge bg-blue-100 text-blue-800 text-sm font-medium px-2.5 py-0.5 rounded">
            {exercise.difficulty}
          </span>
          <span className="exercise-type text-gray-500 text-sm">
            {exercise.exercise_type.replace('_', ' ').toUpperCase()}
          </span>
        </div>
        
        {/* Context (if available) */}
        {exercise.context && (
          <div className="context-box bg-amber-50 border-l-4 border-amber-400 p-4 mb-4">
            <p className="text-amber-800 text-sm font-medium">Context:</p>
            <p className="text-amber-700">{exercise.context}</p>
          </div>
        )}
      </div>

      {/* Exercise Question */}
      <div className="exercise-question mb-6">
        <h2 
          id="exercise-question"
          className="text-lg font-semibold text-gray-900 mb-4"
        >
          {exercise.question}
        </h2>
        
        {/* Exercise Input */}
        {renderExerciseInput()}
      </div>

      {/* Action Buttons */}
      <div className="exercise-actions flex gap-3 mb-4">
        {!isSubmitted && (
          <>
            <button
              onClick={handleSubmit}
              disabled={!userAnswer.trim()}
              className="submit-btn flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white font-medium py-2 px-4 rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              aria-describedby="submit-help"
            >
              Submit Answer
            </button>
            
            {showHint && (
              <button
                onClick={handleShowHint}
                className="hint-btn bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium py-2 px-4 rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
                aria-label="Show hint for this exercise"
              >
                Hint ({hintsUsed})
              </button>
            )}
          </>
        )}
        
        {allowSkip && !isSubmitted && (
          <button
            onClick={() => onSubmit('', Date.now() - startTime)}
            className="skip-btn bg-gray-300 hover:bg-gray-400 text-gray-700 font-medium py-2 px-4 rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
          >
            Skip
          </button>
        )}
      </div>

      {/* Hint Display */}
      {showHint && hintsUsed > 0 && exercise.hint && (
        <div className="hint-box bg-blue-50 border border-blue-200 rounded-md p-3 mb-4">
          <p className="text-blue-700 text-sm">
            <span className="font-medium">💡 Hint:</span> {exercise.hint}
          </p>
        </div>
      )}

      {/* Feedback */}
      {feedback && (
        <FeedbackDisplay
          feedback={feedback}
          variant="inline"
          showExplanation={true}
        />
      )}

      {/* Cultural Note */}
      {exercise.cultural_note && (
        <div className="cultural-note bg-purple-50 border border-purple-200 rounded-md p-3 mt-4">
          <p className="text-purple-700 text-sm">
            <span className="font-medium">🌍 Cultural Note:</span> {exercise.cultural_note}
          </p>
        </div>
      )}

      {/* Screen reader only help text */}
      <div id="submit-help" className="sr-only">
        Press Enter or click Submit to answer this exercise
      </div>
    </div>
  );
};
```

#### `src/components/ProgressBar.tsx` - Progress Visualization
```typescript
import React from 'react';
import { Progress } from '../types';

interface ProgressBarProps {
  progress: Progress;
  variant?: 'linear' | 'circular' | 'detailed';
  size?: 'sm' | 'md' | 'lg';
  showLabels?: boolean;
  color?: 'blue' | 'green' | 'purple' | 'orange';
  className?: string;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  progress,
  variant = 'linear',
  size = 'md',
  showLabels = true,
  color = 'blue',
  className = ''
}) => {
  const sizeClasses = {
    sm: 'h-2',
    md: 'h-3',
    lg: 'h-4'
  };

  const colorClasses = {
    blue: 'bg-blue-600',
    green: 'bg-green-600',
    purple: 'bg-purple-600',
    orange: 'bg-orange-600'
  };

  if (variant === 'circular') {
    return (
      <CircularProgress 
        progress={progress} 
        size={size} 
        color={color}
        showLabels={showLabels}
        className={className}
      />
    );
  }

  if (variant === 'detailed') {
    return (
      <DetailedProgress 
        progress={progress}
        className={className}
      />
    );
  }

  return (
    <div className={`progress-container ${className}`} role="progressbar" 
         aria-valuenow={progress.percentage} 
         aria-valuemin={0} 
         aria-valuemax={100}
         aria-label="Exercise progress">
      
      {showLabels && (
        <div className="progress-labels flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-gray-700">
            Progress: {progress.current}/{progress.total}
          </span>
          <span className="text-sm text-gray-500">
            {Math.round(progress.percentage)}%
          </span>
        </div>
      )}
      
      <div className="progress-track bg-gray-200 rounded-full overflow-hidden">
        <div
          className={`progress-fill ${colorClasses[color]} ${sizeClasses[size]} transition-all duration-300 ease-out rounded-full`}
          style={{ width: `${progress.percentage}%` }}
        />
      </div>
      
      {showLabels && progress.streak > 0 && (
        <div className="streak-indicator mt-2 flex items-center text-sm text-gray-600">
          <span className="mr-1">🔥</span>
          <span>{progress.streak} day streak</span>
          {progress.accuracy && (
            <span className="ml-4">
              📊 {Math.round(progress.accuracy * 100)}% accuracy
            </span>
          )}
        </div>
      )}
    </div>
  );
};

const CircularProgress: React.FC<{
  progress: Progress;
  size: string;
  color: string;
  showLabels: boolean;
  className: string;
}> = ({ progress, size, color, showLabels, className }) => {
  const sizeValues = { sm: 60, md: 80, lg: 100 };
  const strokeWidth = 8;
  const radius = (sizeValues[size as keyof typeof sizeValues] - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const strokeDasharray = circumference;
  const strokeDashoffset = circumference - (progress.percentage / 100) * circumference;

  return (
    <div className={`circular-progress relative inline-flex items-center justify-center ${className}`}>
      <svg
        width={sizeValues[size as keyof typeof sizeValues]}
        height={sizeValues[size as keyof typeof sizeValues]}
        className="transform -rotate-90"
      >
        {/* Background circle */}
        <circle
          cx="50%"
          cy="50%"
          r={radius}
          stroke="currentColor"
          strokeWidth={strokeWidth}
          fill="transparent"
          className="text-gray-200"
        />
        {/* Progress circle */}
        <circle
          cx="50%"
          cy="50%"
          r={radius}
          stroke="currentColor"
          strokeWidth={strokeWidth}
          fill="transparent"
          strokeDasharray={strokeDasharray}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          className={`text-${color}-600 transition-all duration-300 ease-out`}
        />
      </svg>
      
      {showLabels && (
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-lg font-bold text-gray-900">
            {Math.round(progress.percentage)}%
          </span>
          <span className="text-xs text-gray-500">
            {progress.current}/{progress.total}
          </span>
        </div>
      )}
    </div>
  );
};
```

#### `src/components/AnswerInput.tsx` - Enhanced Input Component
```typescript
import React, { useState, useRef, useEffect } from 'react';
import { useAccessibility } from '../hooks/useAccessibility';

interface AnswerInputProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit?: () => void;
  placeholder?: string;
  suggestions?: string[];
  autoComplete?: boolean;
  maxLength?: number;
  disabled?: boolean;
  variant?: 'default' | 'underlined' | 'filled';
  className?: string;
  'aria-labelledby'?: string;
}

export const AnswerInput: React.FC<AnswerInputProps> = ({
  value,
  onChange,
  onSubmit,
  placeholder = "Type your answer...",
  suggestions = [],
  autoComplete = true,
  maxLength = 100,
  disabled = false,
  variant = 'default',
  className = '',
  'aria-labelledby': ariaLabelledBy
}) => {
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [filteredSuggestions, setFilteredSuggestions] = useState<string[]>([]);
  const [selectedSuggestionIndex, setSelectedSuggestionIndex] = useState(-1);
  const [isValid, setIsValid] = useState<boolean | null>(null);
  
  const inputRef = useRef<HTMLInputElement>(null);
  const suggestionsRef = useRef<HTMLUListElement>(null);
  const { announceToScreenReader } = useAccessibility();

  useEffect(() => {
    if (autoComplete && suggestions.length > 0 && value.length > 0) {
      const filtered = suggestions.filter(suggestion =>
        suggestion.toLowerCase().includes(value.toLowerCase())
      ).slice(0, 5); // Limit to 5 suggestions
      
      setFilteredSuggestions(filtered);
      setShowSuggestions(filtered.length > 0);
      setSelectedSuggestionIndex(-1);
    } else {
      setShowSuggestions(false);
      setFilteredSuggestions([]);
    }
  }, [value, suggestions, autoComplete]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    if (newValue.length <= maxLength) {
      onChange(newValue);
      setIsValid(null); // Reset validation state when user types
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (!showSuggestions) {
      if (e.key === 'Enter' && onSubmit) {
        e.preventDefault();
        onSubmit();
      }
      return;
    }

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setSelectedSuggestionIndex(prev => 
          prev < filteredSuggestions.length - 1 ? prev + 1 : 0
        );
        break;
        
      case 'ArrowUp':
        e.preventDefault();
        setSelectedSuggestionIndex(prev => 
          prev > 0 ? prev - 1 : filteredSuggestions.length - 1
        );
        break;
        
      case 'Enter':
        e.preventDefault();
        if (selectedSuggestionIndex >= 0) {
          selectSuggestion(filteredSuggestions[selectedSuggestionIndex]);
        } else if (onSubmit) {
          onSubmit();
        }
        break;
        
      case 'Escape':
        setShowSuggestions(false);
        setSelectedSuggestionIndex(-1);
        break;
        
      case 'Tab':
        setShowSuggestions(false);
        break;
    }
  };

  const selectSuggestion = (suggestion: string) => {
    onChange(suggestion);
    setShowSuggestions(false);
    setSelectedSuggestionIndex(-1);
    inputRef.current?.focus();
    announceToScreenReader(`Selected: ${suggestion}`);
  };

  const handleBlur = (e: React.FocusEvent<HTMLInputElement>) => {
    // Delay hiding suggestions to allow clicking on them
    setTimeout(() => {
      if (!suggestionsRef.current?.contains(document.activeElement)) {
        setShowSuggestions(false);
      }
    }, 150);
  };

  const getVariantClasses = () => {
    const base = "w-full px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all";
    
    switch (variant) {
      case 'underlined':
        return `${base} border-0 border-b-2 border-gray-300 bg-transparent rounded-none focus:border-blue-500`;
      case 'filled':
        return `${base} bg-gray-100 border border-gray-300 rounded-md focus:bg-white`;
      default:
        return `${base} border border-gray-300 rounded-md`;
    }
  };

  const getStatusClasses = () => {
    if (isValid === true) return 'border-green-500 focus:ring-green-500';
    if (isValid === false) return 'border-red-500 focus:ring-red-500';
    return '';
  };

  return (
    <div className={`answer-input-container relative ${className}`}>
      <div className="input-wrapper relative">
        <input
          ref={inputRef}
          type="text"
          value={value}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          onBlur={handleBlur}
          placeholder={placeholder}
          disabled={disabled}
          className={`answer-input ${getVariantClasses()} ${getStatusClasses()} ${
            disabled ? 'bg-gray-100 cursor-not-allowed' : ''
          }`}
          aria-labelledby={ariaLabelledBy}
          aria-describedby="answer-help"
          aria-autocomplete={autoComplete ? "list" : "off"}
          aria-expanded={showSuggestions}
          aria-haspopup={autoComplete ? "listbox" : "false"}
          role="combobox"
        />
        
        {/* Character counter */}
        {maxLength && value.length > maxLength * 0.8 && (
          <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
            <span className={`text-xs ${
              value.length >= maxLength ? 'text-red-500' : 'text-gray-400'
            }`}>
              {value.length}/{maxLength}
            </span>
          </div>
        )}
      </div>

      {/* Suggestions dropdown */}
      {showSuggestions && filteredSuggestions.length > 0 && (
        <ul
          ref={suggestionsRef}
          className="suggestions-list absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg max-h-48 overflow-y-auto"
          role="listbox"
          aria-label="Suggestions"
        >
          {filteredSuggestions.map((suggestion, index) => (
            <li
              key={suggestion}
              role="option"
              aria-selected={index === selectedSuggestionIndex}
              className={`px-3 py-2 cursor-pointer text-sm ${
                index === selectedSuggestionIndex
                  ? 'bg-blue-100 text-blue-900'
                  : 'hover:bg-gray-100 text-gray-900'
              }`}
              onClick={() => selectSuggestion(suggestion)}
              onMouseEnter={() => setSelectedSuggestionIndex(index)}
            >
              {suggestion}
            </li>
          ))}
        </ul>
      )}

      {/* Help text */}
      <div id="answer-help" className="sr-only">
        {autoComplete && suggestions.length > 0 
          ? "Type to see suggestions. Use arrow keys to navigate, Enter to select."
          : "Type your answer and press Enter to submit."
        }
      </div>

      {/* Validation message */}
      {isValid === false && (
        <div className="validation-message mt-1 text-sm text-red-600" role="alert">
          Please check your answer and try again.
        </div>
      )}
    </div>
  );
};
```

#### `src/components/MultipleChoice.tsx` - Multiple Choice Component
```typescript
import React from 'react';

interface Option {
  id: string;
  label: string;
  value: string;
  description?: string;
  disabled?: boolean;
}

interface MultipleChoiceProps {
  options: Option[];
  value: string;
  onChange: (value: string, option: Option) => void;
  name: string;
  variant?: 'default' | 'cards' | 'buttons' | 'minimal';
  layout?: 'vertical' | 'horizontal' | 'grid';
  disabled?: boolean;
  allowDeselect?: boolean;
  className?: string;
  'aria-labelledby'?: string;
}

export const MultipleChoice: React.FC<MultipleChoiceProps> = ({
  options,
  value,
  onChange,
  name,
  variant = 'default',
  layout = 'vertical',
  disabled = false,
  allowDeselect = false,
  className = '',
  'aria-labelledby': ariaLabelledBy
}) => {
  const handleOptionChange = (option: Option) => {
    if (disabled || option.disabled) return;
    
    if (allowDeselect && value === option.value) {
      onChange('', option);
    } else {
      onChange(option.value, option);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent, option: Option) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleOptionChange(option);
    }
  };

  const getLayoutClasses = () => {
    switch (layout) {
      case 'horizontal':
        return 'flex flex-wrap gap-4';
      case 'grid':
        return 'grid grid-cols-1 sm:grid-cols-2 gap-4';
      default:
        return 'space-y-3';
    }
  };

  const getOptionClasses = (option: Option, isSelected: boolean) => {
    const base = "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all cursor-pointer";
    
    switch (variant) {
      case 'cards':
        return `${base} p-4 border-2 rounded-lg ${
          isSelected 
            ? 'border-blue-500 bg-blue-50' 
            : 'border-gray-300 hover:border-gray-400'
        } ${option.disabled ? 'opacity-50 cursor-not-allowed' : ''}`;
        
      case 'buttons':
        return `${base} px-4 py-2 border rounded-md font-medium ${
          isSelected
            ? 'bg-blue-600 text-white border-blue-600'
            : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
        } ${option.disabled ? 'opacity-50 cursor-not-allowed' : ''}`;
        
      case 'minimal':
        return `${base} p-2 rounded ${
          isSelected ? 'bg-blue-100 text-blue-900' : 'hover:bg-gray-100'
        } ${option.disabled ? 'opacity-50 cursor-not-allowed' : ''}`;
        
      default:
        return `${base} flex items-start ${option.disabled ? 'opacity-50 cursor-not-allowed' : ''}`;
    }
  };

  const renderOption = (option: Option) => {
    const isSelected = value === option.value;
    
    if (variant === 'default') {
      return (
        <label
          key={option.id}
          className={getOptionClasses(option, isSelected)}
          onKeyDown={(e) => handleKeyDown(e, option)}
          tabIndex={0}
        >
          <input
            type="radio"
            name={name}
            value={option.value}
            checked={isSelected}
            onChange={() => handleOptionChange(option)}
            disabled={disabled || option.disabled}
            className="sr-only"
            aria-describedby={option.description ? `${option.id}-desc` : undefined}
          />
          <div className="flex items-start">
            <div className="flex items-center h-5">
              <div className={`w-4 h-4 border-2 rounded-full flex items-center justify-center ${
                isSelected ? 'border-blue-600 bg-blue-600' : 'border-gray-300'
              }`}>
                {isSelected && (
                  <div className="w-2 h-2 bg-white rounded-full" />
                )}
              </div>
            </div>
            <div className="ml-3">
              <span className="text-sm font-medium text-gray-900">
                {option.label}
              </span>
              {option.description && (
                <p id={`${option.id}-desc`} className="text-sm text-gray-500 mt-1">
                  {option.description}
                </p>
              )}
            </div>
          </div>
        </label>
      );
    }

    return (
      <div
        key={option.id}
        role="radio"
        aria-checked={isSelected}
        aria-labelledby={`${option.id}-label`}
        aria-describedby={option.description ? `${option.id}-desc` : undefined}
        tabIndex={0}
        className={getOptionClasses(option, isSelected)}
        onClick={() => handleOptionChange(option)}
        onKeyDown={(e) => handleKeyDown(e, option)}
      >
        <div id={`${option.id}-label`} className="font-medium">
          {option.label}
        </div>
        {option.description && (
          <div id={`${option.id}-desc`} className="text-sm text-gray-600 mt-1">
            {option.description}
          </div>
        )}
        {variant === 'cards' && isSelected && (
          <div className="absolute top-2 right-2 text-blue-600">
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
          </div>
        )}
      </div>
    );
  };

  return (
    <fieldset 
      className={`multiple-choice ${className}`}
      disabled={disabled}
      aria-labelledby={ariaLabelledBy}
    >
      <div className={getLayoutClasses()}>
        {options.map(renderOption)}
      </div>
      
      {/* Screen reader instructions */}
      <div className="sr-only" id="mc-instructions">
        {allowDeselect 
          ? "Select an option or press the same option again to deselect. Use Tab to navigate between options."
          : "Select one option. Use Tab to navigate between options."
        }
      </div>
    </fieldset>
  );
};
```

#### `src/components/FeedbackDisplay.tsx` - Rich Feedback Component
```typescript
import React, { useEffect, useState } from 'react';
import { ExerciseResult } from '../types';
import { useAccessibility } from '../hooks/useAccessibility';

interface FeedbackProps {
  feedback: ExerciseResult;
  variant?: 'toast' | 'inline' | 'modal';
  position?: 'top' | 'bottom' | 'center';
  showExplanation?: boolean;
  autoHide?: boolean;
  duration?: number;
  onClose?: () => void;
  onRetry?: () => void;
  className?: string;
}

export const FeedbackDisplay: React.FC<FeedbackProps> = ({
  feedback,
  variant = 'inline',
  position = 'top',
  showExplanation = true,
  autoHide = false,
  duration = 5000,
  onClose,
  onRetry,
  className = ''
}) => {
  const [isVisible, setIsVisible] = useState(true);
  const [timeLeft, setTimeLeft] = useState(duration);
  const { announceToScreenReader } = useAccessibility();

  useEffect(() => {
    // Announce feedback to screen readers
    const message = `${feedback.is_correct ? 'Correct' : 'Incorrect'}. ${feedback.feedback_message}`;
    announceToScreenReader(message, 'assertive');
  }, [feedback]);

  useEffect(() => {
    if (autoHide && duration > 0) {
      const timer = setInterval(() => {
        setTimeLeft(prev => {
          if (prev <= 100) {
            setIsVisible(false);
            onClose?.();
            return 0;
          }
          return prev - 100;
        });
      }, 100);

      return () => clearInterval(timer);
    }
  }, [autoHide, duration, onClose]);

  const handleClose = () => {
    setIsVisible(false);
    onClose?.();
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      handleClose();
    }
  };

  const getFeedbackIcon = () => {
    if (feedback.is_correct) {
      return (
        <div className="feedback-icon w-8 h-8 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
          <svg className="w-5 h-5 text-green-600" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
          </svg>
        </div>
      );
    } else {
      return (
        <div className="feedback-icon w-8 h-8 bg-red-100 rounded-full flex items-center justify-center flex-shrink-0">
          <svg className="w-5 h-5 text-red-600" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
          </svg>
        </div>
      );
    }
  };

  const getContainerClasses = () => {
    const base = feedback.is_correct 
      ? 'bg-green-50 border-green-200 text-green-800'
      : 'bg-red-50 border-red-200 text-red-800';

    switch (variant) {
      case 'toast':
        return `${base} fixed z-50 max-w-md p-4 border rounded-lg shadow-lg transform transition-all duration-300 ${
          position === 'top' ? 'top-4 right-4' : 
          position === 'bottom' ? 'bottom-4 right-4' : 
          'top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2'
        } ${isVisible ? 'translate-x-0 opacity-100' : 'translate-x-full opacity-0'}`;
        
      case 'modal':
        return `${base} fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50`;
        
      default:
        return `${base} border rounded-lg p-4 ${isVisible ? 'block' : 'hidden'}`;
    }
  };

  if (!isVisible) return null;

  const feedbackContent = (
    <div className={`feedback-content ${variant === 'modal' ? 'bg-white rounded-lg p-6 max-w-md mx-auto' : ''}`}>
      <div className="flex items-start space-x-3">
        {getFeedbackIcon()}
        
        <div className="flex-1 min-w-0">
          <div className="feedback-header flex items-center justify-between">
            <h3 className="feedback-title text-sm font-medium">
              {feedback.is_correct ? '✅ Correct!' : '❌ Not quite right'}
            </h3>
            
            {(variant === 'toast' || variant === 'modal') && (
              <button
                onClick={handleClose}
                className="text-gray-400 hover:text-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 rounded-md p-1"
                aria-label="Close feedback"
              >
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              </button>
            )}
          </div>
          
          <p className="feedback-message text-sm mt-1">
            {feedback.feedback_message}
          </p>
          
          {!feedback.is_correct && feedback.correct_answer && (
            <div className="correct-answer mt-2 p-2 bg-white bg-opacity-50 rounded text-sm">
              <strong>Correct answer:</strong> {feedback.correct_answer}
            </div>
          )}
          
          {showExplanation && feedback.explanation && (
            <div className="explanation mt-3 p-3 bg-white bg-opacity-75 rounded text-sm">
              <strong>Explanation:</strong>
              <p className="mt-1">{feedback.explanation}</p>
            </div>
          )}
          
          {/* Action buttons */}
          <div className="feedback-actions mt-4 flex gap-2">
            {onRetry && !feedback.is_correct && (
              <button
                onClick={onRetry}
                className="retry-btn bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-3 py-1.5 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
              >
                Try Again
              </button>
            )}
            
            {variant === 'modal' && (
              <button
                onClick={handleClose}
                className="close-btn bg-gray-600 hover:bg-gray-700 text-white text-sm font-medium px-3 py-1.5 rounded focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
              >
                Continue
              </button>
            )}
          </div>
        </div>
      </div>
      
      {/* Progress bar for auto-hide */}
      {autoHide && variant === 'toast' && (
        <div className="progress-bar mt-3 bg-white bg-opacity-30 rounded-full h-1 overflow-hidden">
          <div 
            className="bg-white h-full transition-all duration-100 ease-linear"
            style={{ width: `${(timeLeft / duration) * 100}%` }}
          />
        </div>
      )}
    </div>
  );

  return (
    <div
      className={`feedback-display ${getContainerClasses()} ${className}`}
      role="alert"
      aria-live="assertive"
      onKeyDown={handleKeyDown}
      tabIndex={variant === 'modal' ? -1 : undefined}
    >
      {variant === 'modal' ? (
        <div className="modal-backdrop" onClick={handleClose}>
          <div onClick={(e) => e.stopPropagation()}>
            {feedbackContent}
          </div>
        </div>
      ) : (
        feedbackContent
      )}
    </div>
  );
};
```

### 2. Feature Modules (7 modules)

#### `src/features/authentication/AuthProvider.tsx` - Authentication Context
```typescript
import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { User, LoginCredentials, RegisterData } from '../../types';
import { authService } from '../../api/authService';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

interface AuthContextValue extends AuthState {
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => void;
  clearError: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

type AuthAction =
  | { type: 'AUTH_START' }
  | { type: 'AUTH_SUCCESS'; payload: User }
  | { type: 'AUTH_ERROR'; payload: string }
  | { type: 'AUTH_LOGOUT' }
  | { type: 'CLEAR_ERROR' };

const authReducer = (state: AuthState, action: AuthAction): AuthState => {
  switch (action.type) {
    case 'AUTH_START':
      return { ...state, isLoading: true, error: null };
    case 'AUTH_SUCCESS':
      return {
        ...state,
        user: action.payload,
        isAuthenticated: true,
        isLoading: false,
        error: null
      };
    case 'AUTH_ERROR':
      return {
        ...state,
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: action.payload
      };
    case 'AUTH_LOGOUT':
      return {
        ...state,
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null
      };
    case 'CLEAR_ERROR':
      return { ...state, error: null };
    default:
      return state;
  }
};

const initialState: AuthState = {
  user: null,
  isAuthenticated: false,
  isLoading: false,
  error: null
};

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  useEffect(() => {
    // Check for existing session on mount
    const initAuth = async () => {
      const token = localStorage.getItem('access_token');
      if (token) {
        dispatch({ type: 'AUTH_START' });
        try {
          const user = await authService.getCurrentUser();
          dispatch({ type: 'AUTH_SUCCESS', payload: user });
        } catch (error) {
          localStorage.removeItem('access_token');
          dispatch({ type: 'AUTH_ERROR', payload: 'Session expired' });
        }
      }
    };

    initAuth();
  }, []);

  const login = async (credentials: LoginCredentials) => {
    dispatch({ type: 'AUTH_START' });
    try {
      const response = await authService.login(credentials);
      localStorage.setItem('access_token', response.access_token);
      const user = await authService.getCurrentUser();
      dispatch({ type: 'AUTH_SUCCESS', payload: user });
    } catch (error) {
      dispatch({ type: 'AUTH_ERROR', payload: error.message });
      throw error;
    }
  };

  const register = async (data: RegisterData) => {
    dispatch({ type: 'AUTH_START' });
    try {
      await authService.register(data);
      // Auto-login after successful registration
      await login({ email: data.email, password: data.password });
    } catch (error) {
      dispatch({ type: 'AUTH_ERROR', payload: error.message });
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    dispatch({ type: 'AUTH_LOGOUT' });
  };

  const clearError = () => {
    dispatch({ type: 'CLEAR_ERROR' });
  };

  const value: AuthContextValue = {
    ...state,
    login,
    register,
    logout,
    clearError
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextValue => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
```

#### `src/features/practice/PracticeSession.tsx` - Practice Session Container
```typescript
import React, { useState, useEffect } from 'react';
import { Exercise, SessionStats } from '../../types';
import { ExerciseCard } from '../../components/ExerciseCard';
import { ProgressBar } from '../../components/ProgressBar';
import { LoadingState } from '../../components/LoadingState';
import { usePracticeSession } from '../../hooks/usePracticeSession';
import { useAuth } from '../authentication/AuthProvider';

interface PracticeSessionProps {
  sessionType?: 'practice' | 'review' | 'assessment';
  difficulty?: 'beginner' | 'intermediate' | 'advanced';
  onComplete?: (stats: SessionStats) => void;
  onExit?: () => void;
}

export const PracticeSession: React.FC<PracticeSessionProps> = ({
  sessionType = 'practice',
  difficulty = 'intermediate',
  onComplete,
  onExit
}) => {
  const { user } = useAuth();
  const {
    currentExercise,
    progress,
    isLoading,
    error,
    startSession,
    submitAnswer,
    getNextExercise,
    completeSession
  } = usePracticeSession();

  const [sessionStarted, setSessionStarted] = useState(false);
  const [showExitConfirm, setShowExitConfirm] = useState(false);

  useEffect(() => {
    if (user && !sessionStarted) {
      startSession({
        sessionType,
        difficulty,
        estimatedDurationMinutes: 15
      });
      setSessionStarted(true);
    }
  }, [user, sessionStarted]);

  const handleSubmitAnswer = async (answer: string, responseTime: number) => {
    if (!currentExercise) return;

    try {
      const result = await submitAnswer(currentExercise.id, answer, responseTime);
      
      // Show feedback and then get next exercise
      setTimeout(async () => {
        const nextExercise = await getNextExercise();
        if (!nextExercise) {
          // Session complete
          const stats = await completeSession();
          onComplete?.(stats);
        }
      }, 2000);
    } catch (error) {
      console.error('Error submitting answer:', error);
    }
  };

  const handleExit = () => {
    if (progress.current > 0) {
      setShowExitConfirm(true);
    } else {
      onExit?.();
    }
  };

  const confirmExit = () => {
    setShowExitConfirm(false);
    onExit?.();
  };

  if (isLoading) {
    return (
      <div className="practice-session-loading flex items-center justify-center min-h-screen">
        <LoadingState message="Preparing your practice session..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="practice-session-error flex items-center justify-center min-h-screen">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md mx-auto">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">
                Session Error
              </h3>
              <div className="mt-2 text-sm text-red-700">
                <p>{error}</p>
              </div>
              <div className="mt-4">
                <button
                  onClick={() => window.location.reload()}
                  className="bg-red-600 hover:bg-red-700 text-white font-medium py-2 px-4 rounded text-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
                >
                  Try Again
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="practice-session min-h-screen bg-gray-50">
      {/* Session Header */}
      <div className="session-header bg-white shadow-sm border-b">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="session-info">
              <h1 className="text-xl font-semibold text-gray-900 capitalize">
                {sessionType} Session
              </h1>
              <p className="text-sm text-gray-600">
                Difficulty: <span className="capitalize font-medium">{difficulty}</span>
              </p>
            </div>
            
            <div className="session-controls flex items-center space-x-4">
              <ProgressBar
                progress={progress}
                variant="linear"
                size="sm"
                showLabels={false}
                className="w-32"
              />
              <button
                onClick={handleExit}
                className="exit-btn text-gray-400 hover:text-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 rounded-md p-2"
                aria-label="Exit session"
                title="Exit session"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Session Content */}
      <div className="session-content flex-1 py-8">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          {currentExercise ? (
            <ExerciseCard
              exercise={currentExercise}
              onSubmit={handleSubmitAnswer}
              showHint={true}
              allowSkip={sessionType !== 'assessment'}
            />
          ) : (
            <div className="session-complete text-center">
              <div className="mb-8">
                <svg className="mx-auto h-16 w-16 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h2 className="text-2xl font-bold text-gray-900 mb-4">
                Session Complete!
              </h2>
              <p className="text-gray-600 mb-8">
                Great job! You've completed {progress.current} exercises with {Math.round(progress.accuracy * 100)}% accuracy.
              </p>
              <div className="flex justify-center space-x-4">
                <button
                  onClick={() => startSession({ sessionType, difficulty })}
                  className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                >
                  Start Another Session
                </button>
                <button
                  onClick={onExit}
                  className="bg-gray-300 hover:bg-gray-400 text-gray-700 font-medium py-2 px-6 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
                >
                  Back to Dashboard
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Exit Confirmation Modal */}
      {showExitConfirm && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3 text-center">
              <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-yellow-100 mb-4">
                <svg className="h-6 w-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                Exit Session?
              </h3>
              <p className="text-sm text-gray-500 mb-6">
                You've completed {progress.current} out of {progress.total} exercises. 
                Your progress will not be saved if you exit now.
              </p>
              <div className="flex justify-center space-x-4">
                <button
                  onClick={confirmExit}
                  className="bg-red-600 hover:bg-red-700 text-white font-medium py-2 px-4 rounded text-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
                >
                  Exit Anyway
                </button>
                <button
                  onClick={() => setShowExitConfirm(false)}
                  className="bg-gray-300 hover:bg-gray-400 text-gray-700 font-medium py-2 px-4 rounded text-sm focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
                >
                  Continue Session
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
```

### 3. Infrastructure (5 modules)

#### `src/App.tsx` - Main Application Component
```typescript
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

import { AuthProvider, useAuth } from './features/authentication/AuthProvider';
import { AccessibilityProvider } from './features/accessibility/AccessibilityProvider';
import { NavigationMenu } from './components/NavigationMenu';
import { LoadingState } from './components/LoadingState';
import { ErrorBoundary } from './components/ErrorBoundary';

// Lazy load pages for better performance
import { lazy, Suspense } from 'react';
const Dashboard = lazy(() => import('./features/dashboard/Dashboard'));
const PracticeSession = lazy(() => import('./features/practice/PracticeSession'));
const ProgressDashboard = lazy(() => import('./features/analytics/ProgressDashboard'));
const UserProfile = lazy(() => import('./features/profile/UserProfile'));
const LoginPage = lazy(() => import('./pages/LoginPage'));
const RegisterPage = lazy(() => import('./pages/RegisterPage'));

// Create Query Client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 3,
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
    },
  },
});

// Protected Route Component
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <LoadingState message="Authenticating..." />;
  }

  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />;
};

// Main App Layout
const AppLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <>{children}</>;
  }

  return (
    <div className="app-layout min-h-screen bg-gray-50">
      <NavigationMenu
        items={[
          { id: 'dashboard', label: 'Dashboard', icon: '📊', path: '/' },
          { id: 'practice', label: 'Practice', icon: '📝', path: '/practice' },
          { id: 'progress', label: 'Progress', icon: '📈', path: '/progress' },
          { id: 'profile', label: 'Profile', icon: '👤', path: '/profile' }
        ]}
        variant="sidebar"
        collapsible={true}
      />
      
      <main className="app-main ml-64 p-6">
        {children}
      </main>
    </div>
  );
};

// Main App Component
export const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <ErrorBoundary>
        <AuthProvider>
          <AccessibilityProvider>
            <Router>
              <AppLayout>
                <Suspense fallback={<LoadingState message="Loading page..." />}>
                  <Routes>
                    {/* Public routes */}
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/register" element={<RegisterPage />} />
                    
                    {/* Protected routes */}
                    <Route path="/" element={
                      <ProtectedRoute>
                        <Dashboard />
                      </ProtectedRoute>
                    } />
                    
                    <Route path="/practice" element={
                      <ProtectedRoute>
                        <PracticeSession />
                      </ProtectedRoute>
                    } />
                    
                    <Route path="/progress" element={
                      <ProtectedRoute>
                        <ProgressDashboard />
                      </ProtectedRoute>
                    } />
                    
                    <Route path="/profile" element={
                      <ProtectedRoute>
                        <UserProfile />
                      </ProtectedRoute>
                    } />
                    
                    {/* Fallback route */}
                    <Route path="*" element={<Navigate to="/" replace />} />
                  </Routes>
                </Suspense>
              </AppLayout>
            </Router>
          </AccessibilityProvider>
        </AuthProvider>
      </ErrorBoundary>
      
      {process.env.NODE_ENV === 'development' && <ReactQueryDevtools />}
    </QueryClientProvider>
  );
};

export default App;
```

#### `src/api/client.ts` - API Client Configuration
```typescript
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth token
apiClient.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers = {
        ...config.headers,
        Authorization: `Bearer ${token}`,
      };
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling auth errors
apiClient.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API Service Classes
export class ExerciseService {
  static async generateExercise(params: {
    difficulty: string;
    exercise_type: string;
  }) {
    const response = await apiClient.post('/exercises/generate', null, { params });
    return response.data;
  }

  static async submitAnswer(exerciseId: number, data: {
    answer: string;
    response_time: number;
    hints_used?: number;
  }) {
    const response = await apiClient.post(`/exercises/${exerciseId}/submit`, data);
    return response.data;
  }

  static async getExercises(params?: {
    skip?: number;
    limit?: number;
    difficulty?: string;
  }) {
    const response = await apiClient.get('/exercises', { params });
    return response.data;
  }
}

export class SessionService {
  static async startSession(data: {
    session_type: string;
    difficulty: string;
    estimated_duration_minutes?: number;
  }) {
    const response = await apiClient.post('/sessions/start', data);
    return response.data;
  }

  static async completeSession(sessionId: number) {
    const response = await apiClient.post(`/sessions/${sessionId}/complete`);
    return response.data;
  }

  static async getSessionStats() {
    const response = await apiClient.get('/sessions/stats');
    return response.data;
  }
}

export class AnalyticsService {
  static async getProgressReport(days: number = 30) {
    const response = await apiClient.get('/analytics/progress', {
      params: { days }
    });
    return response.data;
  }

  static async getErrorPatterns() {
    const response = await apiClient.get('/analytics/error-patterns');
    return response.data;
  }

  static async getAchievements() {
    const response = await apiClient.get('/analytics/achievements');
    return response.data;
  }

  static async getLeaderboard(timeframe: string = 'weekly') {
    const response = await apiClient.get('/analytics/leaderboard', {
      params: { timeframe }
    });
    return response.data;
  }
}

export class AuthService {
  static async login(credentials: {
    email: string;
    password: string;
  }) {
    const response = await apiClient.post('/auth/login', {
      username: credentials.email, // FastAPI OAuth2 expects 'username'
      password: credentials.password,
    }, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  }

  static async register(data: {
    email: string;
    password: string;
    full_name: string;
  }) {
    const response = await apiClient.post('/auth/register', data);
    return response.data;
  }

  static async getCurrentUser() {
    const response = await apiClient.get('/users/me');
    return response.data;
  }

  static async updateProfile(data: Partial<{
    full_name: string;
    preferred_difficulty: string;
    learning_goals: Record<string, any>;
    accessibility_settings: Record<string, any>;
  }>) {
    const response = await apiClient.patch('/users/me', data);
    return response.data;
  }
}

export default apiClient;
```

This React frontend architecture consolidates 135+ PyQt desktop UI modules into 20 focused, modern web components while preserving all accessibility features and enhancing the user experience with responsive design, real-time updates, and comprehensive error handling.
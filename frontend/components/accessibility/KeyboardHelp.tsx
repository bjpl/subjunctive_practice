/**
 * Keyboard Shortcuts Help Dialog
 *
 * Displays available keyboard shortcuts to users.
 * Meets WCAG 2.1 Success Criterion 2.1.1 (Keyboard)
 */

'use client';

import React, { useState, useEffect, useRef } from 'react';
import { useFocusTrap, useFocusRestoration } from '@/hooks/accessibility/useA11y';

export interface KeyboardShortcut {
  keys: string[];
  description: string;
  category: string;
}

const KEYBOARD_SHORTCUTS: KeyboardShortcut[] = [
  // Navigation
  {
    keys: ['Tab'],
    description: 'Move to next interactive element',
    category: 'Navigation',
  },
  {
    keys: ['Shift', 'Tab'],
    description: 'Move to previous interactive element',
    category: 'Navigation',
  },
  {
    keys: ['Enter'],
    description: 'Activate button or link',
    category: 'Navigation',
  },
  {
    keys: ['Space'],
    description: 'Activate button or checkbox',
    category: 'Navigation',
  },
  {
    keys: ['Escape'],
    description: 'Close dialog or cancel action',
    category: 'Navigation',
  },
  // Application shortcuts
  {
    keys: ['?'],
    description: 'Show this help dialog',
    category: 'General',
  },
  {
    keys: ['Ctrl', 'K'],
    description: 'Open search',
    category: 'General',
  },
  {
    keys: ['Alt', 'H'],
    description: 'Go to home page',
    category: 'General',
  },
  {
    keys: ['Alt', 'D'],
    description: 'Go to dashboard',
    category: 'General',
  },
  // Practice shortcuts
  {
    keys: ['Enter'],
    description: 'Submit answer',
    category: 'Practice',
  },
  {
    keys: ['Ctrl', 'H'],
    description: 'Show hint',
    category: 'Practice',
  },
  {
    keys: ['Ctrl', 'N'],
    description: 'Next exercise',
    category: 'Practice',
  },
  {
    keys: ['Ctrl', 'P'],
    description: 'Previous exercise',
    category: 'Practice',
  },
  // Accessibility
  {
    keys: ['Alt', 'A'],
    description: 'Open accessibility settings',
    category: 'Accessibility',
  },
  {
    keys: ['Ctrl', '+'],
    description: 'Increase font size',
    category: 'Accessibility',
  },
  {
    keys: ['Ctrl', '-'],
    description: 'Decrease font size',
    category: 'Accessibility',
  },
];

export interface KeyboardHelpProps {
  isOpen: boolean;
  onClose: () => void;
}

export function KeyboardHelp({ isOpen, onClose }: KeyboardHelpProps) {
  const dialogRef = useRef<HTMLDivElement>(null);

  useFocusTrap(dialogRef, isOpen);
  useFocusRestoration(isOpen);

  // Group shortcuts by category
  const groupedShortcuts = KEYBOARD_SHORTCUTS.reduce((acc, shortcut) => {
    if (!acc[shortcut.category]) {
      acc[shortcut.category] = [];
    }
    acc[shortcut.category].push(shortcut);
    return acc;
  }, {} as Record<string, KeyboardShortcut[]>);

  // Handle escape key
  useEffect(() => {
    if (!isOpen) return;

    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      className="keyboard-help-overlay"
      onClick={(e) => {
        if (e.target === e.currentTarget) {
          onClose();
        }
      }}
      role="presentation"
    >
      <div
        ref={dialogRef}
        className="keyboard-help-dialog"
        role="dialog"
        aria-modal="true"
        aria-labelledby="keyboard-help-title"
      >
        <div className="keyboard-help-header">
          <h2 id="keyboard-help-title" className="keyboard-help-title">
            Keyboard Shortcuts
          </h2>
          <button
            className="keyboard-help-close"
            onClick={onClose}
            aria-label="Close keyboard shortcuts dialog"
            type="button"
          >
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              aria-hidden="true"
            >
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        </div>

        <div className="keyboard-help-content">
          {Object.entries(groupedShortcuts).map(([category, shortcuts]) => (
            <div key={category} className="keyboard-help-section">
              <h3 className="keyboard-help-category">{category}</h3>
              <dl className="keyboard-help-list">
                {shortcuts.map((shortcut, index) => (
                  <div key={index} className="keyboard-help-item">
                    <dt className="keyboard-help-keys">
                      {shortcut.keys.map((key, keyIndex) => (
                        <React.Fragment key={keyIndex}>
                          {keyIndex > 0 && <span className="keyboard-help-plus">+</span>}
                          <kbd className="keyboard-help-key">{key}</kbd>
                        </React.Fragment>
                      ))}
                    </dt>
                    <dd className="keyboard-help-description">{shortcut.description}</dd>
                  </div>
                ))}
              </dl>
            </div>
          ))}
        </div>

        <div className="keyboard-help-footer">
          <p className="keyboard-help-note">
            Press <kbd className="keyboard-help-key">Escape</kbd> to close this dialog
          </p>
        </div>

        <style jsx>{`
          .keyboard-help-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.75);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
            padding: 20px;
          }

          .keyboard-help-dialog {
            background: var(--color-background, #ffffff);
            border-radius: 8px;
            max-width: 800px;
            width: 100%;
            max-height: 90vh;
            display: flex;
            flex-direction: column;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1),
              0 10px 10px -5px rgba(0, 0, 0, 0.04);
          }

          .keyboard-help-header {
            padding: 24px;
            border-bottom: 1px solid var(--color-border, #e5e7eb);
            display: flex;
            justify-content: space-between;
            align-items: center;
          }

          .keyboard-help-title {
            margin: 0;
            font-size: 24px;
            font-weight: 700;
            color: var(--color-text, #1f2937);
          }

          .keyboard-help-close {
            background: none;
            border: none;
            padding: 8px;
            cursor: pointer;
            color: var(--color-text-secondary, #6b7280);
            border-radius: 4px;
            transition: background-color 0.2s, color 0.2s;
          }

          .keyboard-help-close:hover {
            background: var(--color-hover, #f3f4f6);
            color: var(--color-text, #1f2937);
          }

          .keyboard-help-close:focus {
            outline: 3px solid var(--color-focus, #ffbf47);
            outline-offset: 2px;
          }

          .keyboard-help-content {
            padding: 24px;
            overflow-y: auto;
            flex: 1;
          }

          .keyboard-help-section {
            margin-bottom: 32px;
          }

          .keyboard-help-section:last-child {
            margin-bottom: 0;
          }

          .keyboard-help-category {
            font-size: 18px;
            font-weight: 600;
            color: var(--color-text, #1f2937);
            margin: 0 0 16px 0;
            padding-bottom: 8px;
            border-bottom: 2px solid var(--color-primary, #0066cc);
          }

          .keyboard-help-list {
            margin: 0;
            display: grid;
            gap: 12px;
          }

          .keyboard-help-item {
            display: grid;
            grid-template-columns: 200px 1fr;
            gap: 16px;
            align-items: center;
          }

          .keyboard-help-keys {
            display: flex;
            align-items: center;
            gap: 4px;
            margin: 0;
          }

          .keyboard-help-key {
            background: var(--color-background-secondary, #f9fafb);
            border: 1px solid var(--color-border, #d1d5db);
            border-radius: 4px;
            padding: 4px 8px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            font-weight: 600;
            color: var(--color-text, #1f2937);
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
          }

          .keyboard-help-plus {
            color: var(--color-text-secondary, #6b7280);
            font-weight: 600;
          }

          .keyboard-help-description {
            margin: 0;
            color: var(--color-text-secondary, #6b7280);
            font-size: 14px;
          }

          .keyboard-help-footer {
            padding: 16px 24px;
            border-top: 1px solid var(--color-border, #e5e7eb);
            background: var(--color-background-secondary, #f9fafb);
            border-radius: 0 0 8px 8px;
          }

          .keyboard-help-note {
            margin: 0;
            font-size: 14px;
            color: var(--color-text-secondary, #6b7280);
            text-align: center;
          }

          @media (max-width: 768px) {
            .keyboard-help-item {
              grid-template-columns: 1fr;
              gap: 8px;
            }

            .keyboard-help-keys {
              justify-content: flex-start;
            }
          }

          @media (prefers-reduced-motion: reduce) {
            .keyboard-help-close {
              transition: none;
            }
          }

          @media (prefers-contrast: high) {
            .keyboard-help-dialog {
              border: 2px solid currentColor;
            }

            .keyboard-help-key {
              border-width: 2px;
            }
          }

          /* Dark mode */
          .dark .keyboard-help-dialog {
            background: var(--color-background-dark, #1f2937);
          }

          .dark .keyboard-help-title {
            color: var(--color-text-dark, #f9fafb);
          }

          .dark .keyboard-help-key {
            background: var(--color-background-secondary-dark, #374151);
            border-color: var(--color-border-dark, #4b5563);
            color: var(--color-text-dark, #f9fafb);
          }
        `}</style>
      </div>
    </div>
  );
}

export default KeyboardHelp;

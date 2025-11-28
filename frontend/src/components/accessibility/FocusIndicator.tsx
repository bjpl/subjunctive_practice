/**
 * Focus Indicator Component
 *
 * Provides visible focus indicators for keyboard navigation.
 * Meets WCAG 2.1 Success Criterion 2.4.7 (Focus Visible)
 */

'use client';

import React, { useEffect, useState } from 'react';

export function FocusIndicator() {
  const [isKeyboardUser, setIsKeyboardUser] = useState(false);

  useEffect(() => {
    const handleMouseDown = () => {
      setIsKeyboardUser(false);
    };

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Tab') {
        setIsKeyboardUser(true);
      }
    };

    document.addEventListener('mousedown', handleMouseDown);
    document.addEventListener('keydown', handleKeyDown);

    return () => {
      document.removeEventListener('mousedown', handleMouseDown);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, []);

  useEffect(() => {
    if (isKeyboardUser) {
      document.body.classList.add('keyboard-user');
    } else {
      document.body.classList.remove('keyboard-user');
    }
  }, [isKeyboardUser]);

  return (
    <style jsx global>{`
      /* Base focus styles - always visible for keyboard users */
      *:focus {
        outline: 2px solid transparent;
        outline-offset: 2px;
      }

      /* Enhanced focus for keyboard users */
      .keyboard-user *:focus {
        outline: 3px solid var(--color-focus, #ffbf47);
        outline-offset: 2px;
      }

      /* Skip link focus is always visible */
      .skip-link:focus {
        outline: 3px solid var(--color-focus, #ffbf47);
        outline-offset: 0;
      }

      /* Button focus */
      .keyboard-user button:focus,
      .keyboard-user [role='button']:focus {
        outline: 3px solid var(--color-focus, #ffbf47);
        outline-offset: 2px;
        position: relative;
        z-index: 1;
      }

      /* Link focus */
      .keyboard-user a:focus {
        outline: 3px solid var(--color-focus, #ffbf47);
        outline-offset: 2px;
        text-decoration: underline;
      }

      /* Input focus */
      .keyboard-user input:focus,
      .keyboard-user textarea:focus,
      .keyboard-user select:focus {
        outline: 3px solid var(--color-focus, #ffbf47);
        outline-offset: 2px;
        border-color: var(--color-primary, #0066cc);
      }

      /* High contrast focus */
      @media (prefers-contrast: high) {
        .keyboard-user *:focus {
          outline-width: 4px;
          outline-color: currentColor;
        }
      }

      /* Reduce motion */
      @media (prefers-reduced-motion: reduce) {
        *:focus {
          transition: none;
        }
      }

      /* Focus within for containers */
      .keyboard-user *:focus-within {
        outline: none;
      }

      /* Remove default browser outlines on mouse interaction */
      body:not(.keyboard-user) *:focus {
        outline: none;
      }

      /* But keep visible focus for critical elements */
      body:not(.keyboard-user) input:focus,
      body:not(.keyboard-user) textarea:focus,
      body:not(.keyboard-user) select:focus {
        outline: 2px solid var(--color-primary, #0066cc);
        outline-offset: 2px;
      }
    `}</style>
  );
}

export default FocusIndicator;

/**
 * Live Region Component
 *
 * Provides screen reader announcements for dynamic content.
 * Meets WCAG 2.1 Success Criterion 4.1.3 (Status Messages)
 */

'use client';

import React, { useEffect, useState } from 'react';

export interface LiveRegionProps {
  message: string;
  priority?: 'polite' | 'assertive';
  clearDelay?: number;
}

export function LiveRegion({ message, priority = 'polite', clearDelay = 5000 }: LiveRegionProps) {
  const [currentMessage, setCurrentMessage] = useState('');

  useEffect(() => {
    if (message) {
      // Clear and then set message to ensure screen reader picks it up
      setCurrentMessage('');
      const timeout = setTimeout(() => {
        setCurrentMessage(message);
      }, 100);

      // Clear message after delay
      const clearTimeout = setTimeout(() => {
        setCurrentMessage('');
      }, clearDelay);

      return () => {
        clearTimeout(timeout);
        clearTimeout(clearTimeout);
      };
    }
  }, [message, clearDelay]);

  return (
    <div
      role="status"
      aria-live={priority}
      aria-atomic="true"
      className="sr-only"
    >
      {currentMessage}
    </div>
  );
}

/**
 * Global Live Region Container
 * Place this in your app layout to provide global announcements
 */
export function LiveRegionContainer() {
  return (
    <>
      <div
        id="sr-live-region-polite"
        role="status"
        aria-live="polite"
        aria-atomic="true"
        className="sr-only"
      />
      <div
        id="sr-live-region-assertive"
        role="status"
        aria-live="assertive"
        aria-atomic="true"
        className="sr-only"
      />
      <style jsx global>{`
        .sr-only {
          position: absolute;
          width: 1px;
          height: 1px;
          padding: 0;
          margin: -1px;
          overflow: hidden;
          clip: rect(0, 0, 0, 0);
          white-space: nowrap;
          border-width: 0;
        }
      `}</style>
    </>
  );
}

export default LiveRegion;

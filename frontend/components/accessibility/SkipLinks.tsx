/**
 * Skip Navigation Links Component
 *
 * Provides keyboard users with quick navigation to main content areas.
 * Meets WCAG 2.1 Success Criterion 2.4.1 (Bypass Blocks)
 */

'use client';

import React from 'react';
import { useSkipLinks } from '@/hooks/accessibility/useA11y';

export interface SkipLinksProps {
  className?: string;
}

export function SkipLinks({ className = '' }: SkipLinksProps) {
  const { skipToContent, skipToNavigation, skipToFooter } = useSkipLinks();

  return (
    <div className={`skip-links ${className}`}>
      <a
        href="#main-content"
        className="skip-link"
        onClick={(e) => {
          e.preventDefault();
          skipToContent();
        }}
      >
        Skip to main content
      </a>
      <a
        href="#navigation"
        className="skip-link"
        onClick={(e) => {
          e.preventDefault();
          skipToNavigation();
        }}
      >
        Skip to navigation
      </a>
      <a
        href="#footer"
        className="skip-link"
        onClick={(e) => {
          e.preventDefault();
          skipToFooter();
        }}
      >
        Skip to footer
      </a>

      <style jsx>{`
        .skip-links {
          position: fixed;
          top: 0;
          left: 0;
          z-index: 9999;
        }

        .skip-link {
          position: absolute;
          top: -100px;
          left: 0;
          padding: 12px 16px;
          background: var(--color-primary, #0066cc);
          color: var(--color-white, #ffffff);
          text-decoration: none;
          font-weight: 600;
          font-size: 16px;
          border-radius: 0 0 4px 0;
          transition: top 0.2s ease-in-out;
          white-space: nowrap;
        }

        .skip-link:focus {
          top: 0;
          outline: 3px solid var(--color-focus, #ffbf47);
          outline-offset: 0;
        }

        .skip-link:hover {
          background: var(--color-primary-dark, #0052a3);
        }

        @media (prefers-reduced-motion: reduce) {
          .skip-link {
            transition: none;
          }
        }

        /* High contrast mode */
        @media (prefers-contrast: high) {
          .skip-link {
            border: 2px solid currentColor;
          }

          .skip-link:focus {
            outline-width: 4px;
          }
        }
      `}</style>
    </div>
  );
}

export default SkipLinks;

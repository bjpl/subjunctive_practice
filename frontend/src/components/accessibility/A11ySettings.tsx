/**
 * Accessibility Settings Panel
 *
 * Provides users with customizable accessibility options.
 * Meets multiple WCAG 2.1 success criteria including:
 * - 1.4.3 Contrast (Minimum)
 * - 1.4.4 Resize text
 * - 1.4.8 Visual Presentation
 * - 2.3.3 Animation from Interactions
 */

'use client';

import React, { useState, useRef } from 'react';
import { useA11y, useFocusTrap, useFocusRestoration } from '@/hooks/accessibility/useA11y';

export interface A11ySettingsProps {
  isOpen: boolean;
  onClose: () => void;
}

export function A11ySettings({ isOpen, onClose }: A11ySettingsProps) {
  const { preferences, updatePreference, resetPreferences } = useA11y();
  const panelRef = useRef<HTMLDivElement>(null);
  const [activeTab, setActiveTab] = useState<'visual' | 'motion' | 'navigation'>('visual');

  useFocusTrap(panelRef, isOpen);
  useFocusRestoration(isOpen);

  if (!isOpen) return null;

  return (
    <div
      className="a11y-settings-overlay"
      onClick={(e) => {
        if (e.target === e.currentTarget) {
          onClose();
        }
      }}
      role="presentation"
    >
      <div
        ref={panelRef}
        className="a11y-settings-panel"
        role="dialog"
        aria-modal="true"
        aria-labelledby="a11y-settings-title"
      >
        <div className="a11y-settings-header">
          <h2 id="a11y-settings-title" className="a11y-settings-title">
            Accessibility Settings
          </h2>
          <button
            className="a11y-settings-close"
            onClick={onClose}
            aria-label="Close accessibility settings"
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

        <div
          className="a11y-settings-tabs"
          role="tablist"
          aria-label="Accessibility settings categories"
        >
          <button
            role="tab"
            aria-selected={activeTab === 'visual'}
            aria-controls="visual-panel"
            id="visual-tab"
            className={`a11y-settings-tab ${activeTab === 'visual' ? 'active' : ''}`}
            onClick={() => setActiveTab('visual')}
          >
            Visual
          </button>
          <button
            role="tab"
            aria-selected={activeTab === 'motion'}
            aria-controls="motion-panel"
            id="motion-tab"
            className={`a11y-settings-tab ${activeTab === 'motion' ? 'active' : ''}`}
            onClick={() => setActiveTab('motion')}
          >
            Motion
          </button>
          <button
            role="tab"
            aria-selected={activeTab === 'navigation'}
            aria-controls="navigation-panel"
            id="navigation-tab"
            className={`a11y-settings-tab ${activeTab === 'navigation' ? 'active' : ''}`}
            onClick={() => setActiveTab('navigation')}
          >
            Navigation
          </button>
        </div>

        <div className="a11y-settings-content">
          {/* Visual Settings */}
          <div
            role="tabpanel"
            id="visual-panel"
            aria-labelledby="visual-tab"
            hidden={activeTab !== 'visual'}
            className="a11y-settings-section"
          >
            <div className="a11y-setting">
              <div className="a11y-setting-header">
                <label htmlFor="dark-mode" className="a11y-setting-label">
                  Dark Mode
                </label>
                <p className="a11y-setting-description">
                  Use dark colors for reduced eye strain
                </p>
              </div>
              <label className="a11y-toggle">
                <input
                  id="dark-mode"
                  type="checkbox"
                  checked={preferences.darkMode}
                  onChange={(e) => updatePreference('darkMode', e.target.checked)}
                  className="a11y-toggle-input"
                />
                <span className="a11y-toggle-slider" aria-hidden="true" />
                <span className="sr-only">
                  {preferences.darkMode ? 'Dark mode enabled' : 'Dark mode disabled'}
                </span>
              </label>
            </div>

            <div className="a11y-setting">
              <div className="a11y-setting-header">
                <label htmlFor="high-contrast" className="a11y-setting-label">
                  High Contrast
                </label>
                <p className="a11y-setting-description">
                  Increase contrast for better visibility
                </p>
              </div>
              <label className="a11y-toggle">
                <input
                  id="high-contrast"
                  type="checkbox"
                  checked={preferences.highContrast}
                  onChange={(e) => updatePreference('highContrast', e.target.checked)}
                  className="a11y-toggle-input"
                />
                <span className="a11y-toggle-slider" aria-hidden="true" />
                <span className="sr-only">
                  {preferences.highContrast ? 'High contrast enabled' : 'High contrast disabled'}
                </span>
              </label>
            </div>

            <div className="a11y-setting">
              <div className="a11y-setting-header">
                <label htmlFor="font-size" className="a11y-setting-label">
                  Font Size
                </label>
                <p className="a11y-setting-description">
                  Adjust text size (current: {preferences.fontSize}px)
                </p>
              </div>
              <div className="a11y-slider-controls">
                <button
                  onClick={() => updatePreference('fontSize', Math.max(12, preferences.fontSize - 2))}
                  aria-label="Decrease font size"
                  className="a11y-slider-button"
                >
                  A-
                </button>
                <input
                  id="font-size"
                  type="range"
                  min="12"
                  max="24"
                  step="2"
                  value={preferences.fontSize}
                  onChange={(e) => updatePreference('fontSize', parseInt(e.target.value))}
                  className="a11y-slider"
                  aria-valuemin={12}
                  aria-valuemax={24}
                  aria-valuenow={preferences.fontSize}
                  aria-valuetext={`${preferences.fontSize} pixels`}
                />
                <button
                  onClick={() => updatePreference('fontSize', Math.min(24, preferences.fontSize + 2))}
                  aria-label="Increase font size"
                  className="a11y-slider-button"
                >
                  A+
                </button>
              </div>
            </div>

            <div className="a11y-setting">
              <div className="a11y-setting-header">
                <label htmlFor="line-height" className="a11y-setting-label">
                  Line Height
                </label>
                <p className="a11y-setting-description">
                  Adjust spacing between lines ({preferences.lineHeight.toFixed(1)})
                </p>
              </div>
              <input
                id="line-height"
                type="range"
                min="1.0"
                max="2.5"
                step="0.1"
                value={preferences.lineHeight}
                onChange={(e) => updatePreference('lineHeight', parseFloat(e.target.value))}
                className="a11y-slider"
                aria-valuemin={1.0}
                aria-valuemax={2.5}
                aria-valuenow={preferences.lineHeight}
                aria-valuetext={`${preferences.lineHeight.toFixed(1)}`}
              />
            </div>

            <div className="a11y-setting">
              <div className="a11y-setting-header">
                <label htmlFor="letter-spacing" className="a11y-setting-label">
                  Letter Spacing
                </label>
                <p className="a11y-setting-description">
                  Adjust spacing between letters ({preferences.letterSpacing.toFixed(2)}em)
                </p>
              </div>
              <input
                id="letter-spacing"
                type="range"
                min="0"
                max="0.3"
                step="0.01"
                value={preferences.letterSpacing}
                onChange={(e) => updatePreference('letterSpacing', parseFloat(e.target.value))}
                className="a11y-slider"
                aria-valuemin={0}
                aria-valuemax={0.3}
                aria-valuenow={preferences.letterSpacing}
                aria-valuetext={`${preferences.letterSpacing.toFixed(2)} em`}
              />
            </div>
          </div>

          {/* Motion Settings */}
          <div
            role="tabpanel"
            id="motion-panel"
            aria-labelledby="motion-tab"
            hidden={activeTab !== 'motion'}
            className="a11y-settings-section"
          >
            <div className="a11y-setting">
              <div className="a11y-setting-header">
                <label htmlFor="reduced-motion" className="a11y-setting-label">
                  Reduced Motion
                </label>
                <p className="a11y-setting-description">
                  Minimize animations and transitions
                </p>
              </div>
              <label className="a11y-toggle">
                <input
                  id="reduced-motion"
                  type="checkbox"
                  checked={preferences.reducedMotion}
                  onChange={(e) => updatePreference('reducedMotion', e.target.checked)}
                  className="a11y-toggle-input"
                />
                <span className="a11y-toggle-slider" aria-hidden="true" />
                <span className="sr-only">
                  {preferences.reducedMotion ? 'Reduced motion enabled' : 'Reduced motion disabled'}
                </span>
              </label>
            </div>

            <div className="a11y-info-box">
              <svg
                className="a11y-info-icon"
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                aria-hidden="true"
              >
                <circle cx="12" cy="12" r="10" />
                <line x1="12" y1="16" x2="12" y2="12" />
                <line x1="12" y1="8" x2="12.01" y2="8" />
              </svg>
              <p className="a11y-info-text">
                Reduced motion helps prevent vestibular disorders and motion sickness triggered
                by animations.
              </p>
            </div>
          </div>

          {/* Navigation Settings */}
          <div
            role="tabpanel"
            id="navigation-panel"
            aria-labelledby="navigation-tab"
            hidden={activeTab !== 'navigation'}
            className="a11y-settings-section"
          >
            <div className="a11y-setting">
              <div className="a11y-setting-header">
                <label htmlFor="keyboard-nav" className="a11y-setting-label">
                  Enhanced Keyboard Navigation
                </label>
                <p className="a11y-setting-description">
                  Show focus indicators and keyboard shortcuts
                </p>
              </div>
              <label className="a11y-toggle">
                <input
                  id="keyboard-nav"
                  type="checkbox"
                  checked={preferences.keyboardNavigation}
                  onChange={(e) => updatePreference('keyboardNavigation', e.target.checked)}
                  className="a11y-toggle-input"
                />
                <span className="a11y-toggle-slider" aria-hidden="true" />
                <span className="sr-only">
                  {preferences.keyboardNavigation
                    ? 'Keyboard navigation enabled'
                    : 'Keyboard navigation disabled'}
                </span>
              </label>
            </div>

            <div className="a11y-setting">
              <div className="a11y-setting-header">
                <label htmlFor="screen-reader" className="a11y-setting-label">
                  Screen Reader Announcements
                </label>
                <p className="a11y-setting-description">
                  Announce dynamic content changes
                </p>
              </div>
              <label className="a11y-toggle">
                <input
                  id="screen-reader"
                  type="checkbox"
                  checked={preferences.screenReaderAnnouncements}
                  onChange={(e) =>
                    updatePreference('screenReaderAnnouncements', e.target.checked)
                  }
                  className="a11y-toggle-input"
                />
                <span className="a11y-toggle-slider" aria-hidden="true" />
                <span className="sr-only">
                  {preferences.screenReaderAnnouncements
                    ? 'Screen reader announcements enabled'
                    : 'Screen reader announcements disabled'}
                </span>
              </label>
            </div>

            <div className="a11y-info-box">
              <svg
                className="a11y-info-icon"
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                aria-hidden="true"
              >
                <circle cx="12" cy="12" r="10" />
                <line x1="12" y1="16" x2="12" y2="12" />
                <line x1="12" y1="8" x2="12.01" y2="8" />
              </svg>
              <p className="a11y-info-text">
                Press <kbd>?</kbd> to view all available keyboard shortcuts.
              </p>
            </div>
          </div>
        </div>

        <div className="a11y-settings-footer">
          <button
            className="a11y-settings-reset"
            onClick={resetPreferences}
            type="button"
          >
            Reset to Defaults
          </button>
          <button
            className="a11y-settings-done"
            onClick={onClose}
            type="button"
          >
            Done
          </button>
        </div>

        <style jsx>{`
          .a11y-settings-overlay {
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

          .a11y-settings-panel {
            background: var(--color-background, #ffffff);
            border-radius: 8px;
            max-width: 600px;
            width: 100%;
            max-height: 90vh;
            display: flex;
            flex-direction: column;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1),
              0 10px 10px -5px rgba(0, 0, 0, 0.04);
          }

          .a11y-settings-header {
            padding: 24px;
            border-bottom: 1px solid var(--color-border, #e5e7eb);
            display: flex;
            justify-content: space-between;
            align-items: center;
          }

          .a11y-settings-title {
            margin: 0;
            font-size: 24px;
            font-weight: 700;
            color: var(--color-text, #1f2937);
          }

          .a11y-settings-close {
            background: none;
            border: none;
            padding: 8px;
            cursor: pointer;
            color: var(--color-text-secondary, #6b7280);
            border-radius: 4px;
            transition: background-color 0.2s, color 0.2s;
          }

          .a11y-settings-close:hover {
            background: var(--color-hover, #f3f4f6);
            color: var(--color-text, #1f2937);
          }

          .a11y-settings-close:focus {
            outline: 3px solid var(--color-focus, #ffbf47);
            outline-offset: 2px;
          }

          .a11y-settings-tabs {
            display: flex;
            border-bottom: 1px solid var(--color-border, #e5e7eb);
          }

          .a11y-settings-tab {
            flex: 1;
            padding: 16px;
            background: none;
            border: none;
            border-bottom: 3px solid transparent;
            font-size: 16px;
            font-weight: 600;
            color: var(--color-text-secondary, #6b7280);
            cursor: pointer;
            transition: color 0.2s, border-color 0.2s;
          }

          .a11y-settings-tab:hover {
            color: var(--color-text, #1f2937);
          }

          .a11y-settings-tab:focus {
            outline: 3px solid var(--color-focus, #ffbf47);
            outline-offset: -3px;
          }

          .a11y-settings-tab.active {
            color: var(--color-primary, #0066cc);
            border-bottom-color: var(--color-primary, #0066cc);
          }

          .a11y-settings-content {
            padding: 24px;
            overflow-y: auto;
            flex: 1;
          }

          .a11y-settings-section {
            display: flex;
            flex-direction: column;
            gap: 24px;
          }

          .a11y-setting {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 16px;
          }

          .a11y-setting-header {
            flex: 1;
          }

          .a11y-setting-label {
            display: block;
            font-size: 16px;
            font-weight: 600;
            color: var(--color-text, #1f2937);
            margin-bottom: 4px;
          }

          .a11y-setting-description {
            margin: 0;
            font-size: 14px;
            color: var(--color-text-secondary, #6b7280);
          }

          .a11y-toggle {
            position: relative;
            display: inline-block;
            width: 48px;
            height: 24px;
            flex-shrink: 0;
          }

          .a11y-toggle-input {
            opacity: 0;
            width: 0;
            height: 0;
          }

          .a11y-toggle-slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: var(--color-border, #d1d5db);
            transition: background-color 0.3s;
            border-radius: 24px;
          }

          .a11y-toggle-slider:before {
            position: absolute;
            content: '';
            height: 18px;
            width: 18px;
            left: 3px;
            bottom: 3px;
            background-color: white;
            transition: transform 0.3s;
            border-radius: 50%;
          }

          .a11y-toggle-input:checked + .a11y-toggle-slider {
            background-color: var(--color-primary, #0066cc);
          }

          .a11y-toggle-input:checked + .a11y-toggle-slider:before {
            transform: translateX(24px);
          }

          .a11y-toggle-input:focus + .a11y-toggle-slider {
            outline: 3px solid var(--color-focus, #ffbf47);
            outline-offset: 2px;
          }

          .a11y-slider {
            width: 100%;
            height: 8px;
            border-radius: 4px;
            background: var(--color-border, #d1d5db);
            outline: none;
            -webkit-appearance: none;
          }

          .a11y-slider::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: var(--color-primary, #0066cc);
            cursor: pointer;
          }

          .a11y-slider::-moz-range-thumb {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: var(--color-primary, #0066cc);
            cursor: pointer;
            border: none;
          }

          .a11y-slider:focus {
            outline: 3px solid var(--color-focus, #ffbf47);
            outline-offset: 2px;
          }

          .a11y-slider-controls {
            display: flex;
            align-items: center;
            gap: 12px;
          }

          .a11y-slider-button {
            padding: 8px 12px;
            background: var(--color-background-secondary, #f3f4f6);
            border: 1px solid var(--color-border, #d1d5db);
            border-radius: 4px;
            font-size: 14px;
            font-weight: 600;
            color: var(--color-text, #1f2937);
            cursor: pointer;
            transition: background-color 0.2s;
          }

          .a11y-slider-button:hover {
            background: var(--color-hover, #e5e7eb);
          }

          .a11y-slider-button:focus {
            outline: 3px solid var(--color-focus, #ffbf47);
            outline-offset: 2px;
          }

          .a11y-info-box {
            display: flex;
            gap: 12px;
            padding: 16px;
            background: var(--color-info-bg, #eff6ff);
            border: 1px solid var(--color-info-border, #bfdbfe);
            border-radius: 6px;
          }

          .a11y-info-icon {
            flex-shrink: 0;
            color: var(--color-info, #3b82f6);
          }

          .a11y-info-text {
            margin: 0;
            font-size: 14px;
            color: var(--color-text-secondary, #6b7280);
          }

          .a11y-info-text kbd {
            background: var(--color-background, #ffffff);
            border: 1px solid var(--color-border, #d1d5db);
            border-radius: 3px;
            padding: 2px 6px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
          }

          .a11y-settings-footer {
            padding: 16px 24px;
            border-top: 1px solid var(--color-border, #e5e7eb);
            display: flex;
            justify-content: space-between;
            gap: 12px;
          }

          .a11y-settings-reset,
          .a11y-settings-done {
            padding: 10px 20px;
            border-radius: 6px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.2s, color 0.2s;
          }

          .a11y-settings-reset {
            background: none;
            border: 1px solid var(--color-border, #d1d5db);
            color: var(--color-text, #1f2937);
          }

          .a11y-settings-reset:hover {
            background: var(--color-hover, #f3f4f6);
          }

          .a11y-settings-reset:focus {
            outline: 3px solid var(--color-focus, #ffbf47);
            outline-offset: 2px;
          }

          .a11y-settings-done {
            background: var(--color-primary, #0066cc);
            border: none;
            color: white;
          }

          .a11y-settings-done:hover {
            background: var(--color-primary-dark, #0052a3);
          }

          .a11y-settings-done:focus {
            outline: 3px solid var(--color-focus, #ffbf47);
            outline-offset: 2px;
          }

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

          @media (prefers-reduced-motion: reduce) {
            .a11y-settings-close,
            .a11y-settings-tab,
            .a11y-toggle-slider,
            .a11y-toggle-slider:before,
            .a11y-slider-button,
            .a11y-settings-reset,
            .a11y-settings-done {
              transition: none;
            }
          }

          @media (prefers-contrast: high) {
            .a11y-settings-panel {
              border: 2px solid currentColor;
            }
          }
        `}</style>
      </div>
    </div>
  );
}

export default A11ySettings;

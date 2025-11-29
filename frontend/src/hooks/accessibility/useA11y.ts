/**
 * useA11y Hook
 *
 * React hook for managing accessibility features and preferences.
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import {
  A11yPreferences,
  getA11yPreferences,
  saveA11yPreferences,
  applyA11yPreferences,
  announceToScreenReader,
  createFocusTrap,
  createFocusRestoration,
  KeyboardShortcut,
  registerKeyboardShortcuts,
} from '../../lib/accessibility/a11y-utils';

export interface UseA11yReturn {
  preferences: A11yPreferences;
  updatePreference: <K extends keyof A11yPreferences>(
    key: K,
    value: A11yPreferences[K]
  ) => void;
  announce: (message: string, priority?: 'polite' | 'assertive') => void;
  resetPreferences: () => void;
}

/**
 * Hook for managing accessibility preferences and features
 */
export function useA11y(): UseA11yReturn {
  const [preferences, setPreferences] = useState<A11yPreferences>(() =>
    getA11yPreferences()
  );

  // Apply preferences on mount and when they change
  useEffect(() => {
    applyA11yPreferences(preferences);
    saveA11yPreferences(preferences);
  }, [preferences]);

  // Listen for system preference changes
  useEffect(() => {
    const mediaQueries = [
      window.matchMedia('(prefers-reduced-motion: reduce)'),
      window.matchMedia('(prefers-color-scheme: dark)'),
      window.matchMedia('(prefers-contrast: high)'),
    ];

    const handleChange = () => {
      const systemPrefs = getA11yPreferences();
      setPreferences((current: A11yPreferences) => ({
        ...current,
        reducedMotion: systemPrefs.reducedMotion,
        darkMode: current.darkMode || systemPrefs.darkMode,
        highContrast: current.highContrast || systemPrefs.highContrast,
      }));
    };

    mediaQueries.forEach((mq) => mq.addEventListener('change', handleChange));

    return () => {
      mediaQueries.forEach((mq) => mq.removeEventListener('change', handleChange));
    };
  }, []);

  const updatePreference = useCallback(
    <K extends keyof A11yPreferences>(key: K, value: A11yPreferences[K]) => {
      setPreferences((current: A11yPreferences) => ({
        ...current,
        [key]: value,
      }));
    },
    []
  );

  const announce = useCallback(
    (message: string, priority: 'polite' | 'assertive' = 'polite') => {
      if (preferences.screenReaderAnnouncements) {
        announceToScreenReader(message, priority);
      }
    },
    [preferences.screenReaderAnnouncements]
  );

  const resetPreferences = useCallback(() => {
    const defaultPrefs = getA11yPreferences();
    setPreferences(defaultPrefs);
  }, []);

  return {
    preferences,
    updatePreference,
    announce,
    resetPreferences,
  };
}

/**
 * Hook for managing focus trap in modals/dialogs
 */
export function useFocusTrap(
  containerRef: React.RefObject<HTMLElement>,
  isActive: boolean
) {
  useEffect(() => {
    const container = containerRef.current;
    if (!container || !isActive) return;

    const focusTrap = createFocusTrap(container);
    focusTrap.activate();

    return () => {
      focusTrap.deactivate();
    };
  }, [containerRef, isActive]);
}

/**
 * Hook for managing focus restoration
 */
export function useFocusRestoration(isActive: boolean) {
  const restorationRef = useRef(createFocusRestoration());

  useEffect(() => {
    if (isActive) {
      restorationRef.current.save();
    }

    return () => {
      if (isActive) {
        restorationRef.current.restore();
      }
    };
  }, [isActive]);
}

/**
 * Hook for registering keyboard shortcuts
 */
export function useKeyboardShortcuts(shortcuts: KeyboardShortcut[]) {
  useEffect(() => {
    const unregister = registerKeyboardShortcuts(shortcuts);
    return unregister;
  }, [shortcuts]);
}

/**
 * Hook for managing skip links
 */
export function useSkipLinks() {
  const skipToContent = useCallback(() => {
    const mainContent = document.querySelector('main');
    if (mainContent) {
      mainContent.setAttribute('tabindex', '-1');
      mainContent.focus();
      mainContent.addEventListener(
        'blur',
        () => mainContent.removeAttribute('tabindex'),
        { once: true }
      );
    }
  }, []);

  const skipToNavigation = useCallback(() => {
    const navigation = document.querySelector('nav');
    if (navigation) {
      navigation.setAttribute('tabindex', '-1');
      navigation.focus();
      navigation.addEventListener(
        'blur',
        () => navigation.removeAttribute('tabindex'),
        { once: true }
      );
    }
  }, []);

  const skipToFooter = useCallback(() => {
    const footer = document.querySelector('footer');
    if (footer) {
      footer.setAttribute('tabindex', '-1');
      footer.focus();
      footer.addEventListener(
        'blur',
        () => footer.removeAttribute('tabindex'),
        { once: true }
      );
    }
  }, []);

  return {
    skipToContent,
    skipToNavigation,
    skipToFooter,
  };
}

/**
 * Hook for announcing route changes to screen readers
 */
export function useRouteAnnouncement(pathname: string) {
  const { announce } = useA11y();

  useEffect(() => {
    // Announce page change
    const pageName = pathname
      .split('/')
      .filter(Boolean)
      .map((segment) => segment.charAt(0).toUpperCase() + segment.slice(1))
      .join(' - ') || 'Home';

    announce(`Navigated to ${pageName} page`, 'polite');
  }, [pathname, announce]);
}

/**
 * Hook for managing live region announcements
 */
export function useLiveRegion() {
  const { announce } = useA11y();

  const announcePolite = useCallback(
    (message: string) => {
      announce(message, 'polite');
    },
    [announce]
  );

  const announceAssertive = useCallback(
    (message: string) => {
      announce(message, 'assertive');
    },
    [announce]
  );

  return {
    announcePolite,
    announceAssertive,
  };
}

/**
 * Hook for detecting if user prefers keyboard navigation
 */
export function useKeyboardNavigation() {
  const [isUsingKeyboard, setIsUsingKeyboard] = useState(false);

  useEffect(() => {
    const handleMouseDown = () => setIsUsingKeyboard(false);
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Tab') {
        setIsUsingKeyboard(true);
      }
    };

    document.addEventListener('mousedown', handleMouseDown);
    document.addEventListener('keydown', handleKeyDown);

    return () => {
      document.removeEventListener('mousedown', handleMouseDown);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, []);

  return isUsingKeyboard;
}

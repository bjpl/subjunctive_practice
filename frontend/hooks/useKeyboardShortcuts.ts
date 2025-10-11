"use client";

import { useEffect, useCallback, useRef } from "react";

export interface KeyboardShortcut {
  key: string;
  ctrl?: boolean;
  shift?: boolean;
  alt?: boolean;
  meta?: boolean;
  callback: (event: KeyboardEvent) => void;
  description?: string;
  preventDefault?: boolean;
}

interface UseKeyboardShortcutsOptions {
  enabled?: boolean;
  preventDefault?: boolean;
}

/**
 * Hook for managing keyboard shortcuts
 *
 * @example
 * useKeyboardShortcuts([
 *   {
 *     key: 's',
 *     ctrl: true,
 *     callback: () => console.log('Save'),
 *     description: 'Save document'
 *   },
 *   {
 *     key: 'Escape',
 *     callback: () => console.log('Close modal')
 *   }
 * ]);
 */
export function useKeyboardShortcuts(
  shortcuts: KeyboardShortcut[],
  options: UseKeyboardShortcutsOptions = {}
) {
  const { enabled = true, preventDefault: defaultPreventDefault = true } = options;
  const shortcutsRef = useRef(shortcuts);

  // Update ref when shortcuts change
  useEffect(() => {
    shortcutsRef.current = shortcuts;
  }, [shortcuts]);

  const handleKeyDown = useCallback(
    (event: KeyboardEvent) => {
      if (!enabled) return;

      const activeElement = document.activeElement;
      const isInputField =
        activeElement?.tagName === "INPUT" ||
        activeElement?.tagName === "TEXTAREA" ||
        activeElement?.getAttribute("contenteditable") === "true";

      for (const shortcut of shortcutsRef.current) {
        const keyMatches =
          event.key.toLowerCase() === shortcut.key.toLowerCase() ||
          event.code.toLowerCase() === shortcut.key.toLowerCase();

        const ctrlMatches = shortcut.ctrl === undefined || shortcut.ctrl === (event.ctrlKey || event.metaKey);
        const shiftMatches = shortcut.shift === undefined || shortcut.shift === event.shiftKey;
        const altMatches = shortcut.alt === undefined || shortcut.alt === event.altKey;
        const metaMatches = shortcut.meta === undefined || shortcut.meta === event.metaKey;

        if (keyMatches && ctrlMatches && shiftMatches && altMatches && metaMatches) {
          // Skip if typing in an input field and no modifier keys
          if (isInputField && !shortcut.ctrl && !shortcut.meta && !shortcut.alt) {
            continue;
          }

          const shouldPreventDefault = shortcut.preventDefault ?? defaultPreventDefault;
          if (shouldPreventDefault) {
            event.preventDefault();
          }

          shortcut.callback(event);
          break;
        }
      }
    },
    [enabled, defaultPreventDefault]
  );

  useEffect(() => {
    if (enabled) {
      window.addEventListener("keydown", handleKeyDown);
      return () => window.removeEventListener("keydown", handleKeyDown);
    }
  }, [enabled, handleKeyDown]);
}

/**
 * Common keyboard shortcuts preset
 */
export const commonShortcuts = {
  save: (callback: () => void): KeyboardShortcut => ({
    key: "s",
    ctrl: true,
    callback,
    description: "Save",
  }),
  submit: (callback: () => void): KeyboardShortcut => ({
    key: "Enter",
    ctrl: true,
    callback,
    description: "Submit",
  }),
  escape: (callback: () => void): KeyboardShortcut => ({
    key: "Escape",
    callback,
    description: "Close/Cancel",
  }),
  undo: (callback: () => void): KeyboardShortcut => ({
    key: "z",
    ctrl: true,
    callback,
    description: "Undo",
  }),
  redo: (callback: () => void): KeyboardShortcut => ({
    key: "y",
    ctrl: true,
    callback,
    description: "Redo",
  }),
  find: (callback: () => void): KeyboardShortcut => ({
    key: "f",
    ctrl: true,
    callback,
    description: "Find",
  }),
  help: (callback: () => void): KeyboardShortcut => ({
    key: "?",
    shift: true,
    callback,
    description: "Show help",
  }),
  refresh: (callback: () => void): KeyboardShortcut => ({
    key: "r",
    ctrl: true,
    callback,
    description: "Refresh",
  }),
  nextItem: (callback: () => void): KeyboardShortcut => ({
    key: "ArrowDown",
    callback,
    description: "Next item",
  }),
  previousItem: (callback: () => void): KeyboardShortcut => ({
    key: "ArrowUp",
    callback,
    description: "Previous item",
  }),
  delete: (callback: () => void): KeyboardShortcut => ({
    key: "Delete",
    callback,
    description: "Delete",
  }),
};

/**
 * Hook for managing a single keyboard shortcut
 */
export function useKeyboardShortcut(
  key: string,
  callback: (event: KeyboardEvent) => void,
  options: {
    ctrl?: boolean;
    shift?: boolean;
    alt?: boolean;
    meta?: boolean;
    enabled?: boolean;
    preventDefault?: boolean;
  } = {}
) {
  const { enabled = true, preventDefault = true, ...modifiers } = options;

  useKeyboardShortcuts(
    [
      {
        key,
        ...modifiers,
        callback,
        preventDefault,
      },
    ],
    { enabled }
  );
}

/**
 * Hook for creating a shortcuts help dialog data
 */
export function useShortcutsHelp(shortcuts: KeyboardShortcut[]) {
  const formatShortcut = useCallback((shortcut: KeyboardShortcut): string => {
    const parts: string[] = [];

    if (shortcut.ctrl || shortcut.meta) parts.push("Ctrl");
    if (shortcut.shift) parts.push("Shift");
    if (shortcut.alt) parts.push("Alt");
    parts.push(shortcut.key.toUpperCase());

    return parts.join(" + ");
  }, []);

  const helpData = shortcuts
    .filter((s) => s.description)
    .map((shortcut) => ({
      shortcut: formatShortcut(shortcut),
      description: shortcut.description!,
    }));

  return helpData;
}

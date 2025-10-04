/**
 * Memoized selectors for UI state
 */

import { createSelector } from '@reduxjs/toolkit';
import type { RootState } from '../store';

// Base selectors
const selectUIState = (state: RootState) => state.ui;

// Memoized selectors
export const selectTheme = createSelector(
  [selectUIState],
  (ui) => ui.theme
);

export const selectSidebarOpen = createSelector(
  [selectUIState],
  (ui) => ui.sidebarOpen
);

export const selectModals = createSelector(
  [selectUIState],
  (ui) => ui.modals
);

export const selectToasts = createSelector(
  [selectUIState],
  (ui) => ui.toasts
);

export const selectIsOnline = createSelector(
  [selectUIState],
  (ui) => ui.isOnline
);

// Computed selectors
export const selectIsDarkMode = createSelector(
  [selectTheme],
  (theme) => theme === 'dark'
);

export const selectIsLightMode = createSelector(
  [selectTheme],
  (theme) => theme === 'light'
);

export const selectModalOpen = (modalId: string) =>
  createSelector([selectModals], (modals) => modals[modalId] || false);

export const selectActiveToastCount = createSelector(
  [selectToasts],
  (toasts) => toasts.length
);

export const selectHasToasts = createSelector(
  [selectActiveToastCount],
  (count) => count > 0
);

export const selectLatestToast = createSelector(
  [selectToasts],
  (toasts) => toasts[toasts.length - 1] || null
);

export const selectIsOffline = createSelector(
  [selectIsOnline],
  (isOnline) => !isOnline
);

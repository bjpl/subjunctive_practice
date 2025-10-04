/**
 * UI state slice
 */

import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { UIState, Toast } from '../../types';
import { getStorageItem, setStorageItem, StorageKeys } from '../../lib/storage';

const initialState: UIState = {
  theme: getStorageItem<'light' | 'dark'>(StorageKeys.THEME, 'light'),
  sidebarOpen: true,
  modals: {},
  toasts: [],
  isOnline: navigator.onLine,
};

const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    setTheme: (state, action: PayloadAction<'light' | 'dark'>) => {
      state.theme = action.payload;
      setStorageItem(StorageKeys.THEME, action.payload);
    },

    toggleTheme: (state) => {
      state.theme = state.theme === 'light' ? 'dark' : 'light';
      setStorageItem(StorageKeys.THEME, state.theme);
    },

    setSidebarOpen: (state, action: PayloadAction<boolean>) => {
      state.sidebarOpen = action.payload;
    },

    toggleSidebar: (state) => {
      state.sidebarOpen = !state.sidebarOpen;
    },

    openModal: (state, action: PayloadAction<string>) => {
      state.modals[action.payload] = true;
    },

    closeModal: (state, action: PayloadAction<string>) => {
      state.modals[action.payload] = false;
    },

    toggleModal: (state, action: PayloadAction<string>) => {
      state.modals[action.payload] = !state.modals[action.payload];
    },

    addToast: (state, action: PayloadAction<Omit<Toast, 'id'>>) => {
      const id = Date.now().toString() + Math.random().toString(36).substr(2, 9);
      state.toasts.push({ ...action.payload, id });
    },

    removeToast: (state, action: PayloadAction<string>) => {
      state.toasts = state.toasts.filter((toast) => toast.id !== action.payload);
    },

    clearToasts: (state) => {
      state.toasts = [];
    },

    setOnlineStatus: (state, action: PayloadAction<boolean>) => {
      state.isOnline = action.payload;
    },
  },
});

export const {
  setTheme,
  toggleTheme,
  setSidebarOpen,
  toggleSidebar,
  openModal,
  closeModal,
  toggleModal,
  addToast,
  removeToast,
  clearToasts,
  setOnlineStatus,
} = uiSlice.actions;

export default uiSlice.reducer;

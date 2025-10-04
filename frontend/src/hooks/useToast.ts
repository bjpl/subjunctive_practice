/**
 * Toast notifications hook
 */

import { useCallback } from 'react';
import { useAppSelector } from './useAppSelector';
import { useAppDispatch } from './useAppDispatch';
import { addToast, removeToast, clearToasts } from '../store/slices/uiSlice';
import type { Toast } from '../types/api';

export const useToast = () => {
  const dispatch = useAppDispatch();
  const toasts = useAppSelector((state) => state.ui.toasts);

  // Show toast
  const showToast = useCallback(
    (toast: Omit<Toast, 'id'>) => {
      dispatch(addToast(toast));
    },
    [dispatch]
  );

  // Show success toast
  const success = useCallback(
    (message: string, duration = 3000) => {
      dispatch(addToast({ type: 'success', message, duration }));
    },
    [dispatch]
  );

  // Show error toast
  const error = useCallback(
    (message: string, duration = 5000) => {
      dispatch(addToast({ type: 'error', message, duration }));
    },
    [dispatch]
  );

  // Show info toast
  const info = useCallback(
    (message: string, duration = 3000) => {
      dispatch(addToast({ type: 'info', message, duration }));
    },
    [dispatch]
  );

  // Show warning toast
  const warning = useCallback(
    (message: string, duration = 4000) => {
      dispatch(addToast({ type: 'warning', message, duration }));
    },
    [dispatch]
  );

  // Remove specific toast
  const remove = useCallback(
    (id: string) => {
      dispatch(removeToast(id));
    },
    [dispatch]
  );

  // Clear all toasts
  const clearAll = useCallback(() => {
    dispatch(clearToasts());
  }, [dispatch]);

  return {
    toasts,
    showToast,
    success,
    error,
    info,
    warning,
    remove,
    clearAll,
  };
};

"use client";

import * as React from "react";
import { EnhancedToastProps, ToastVariant } from "@/components/feedback/EnhancedToast";

interface ToastOptions {
  title?: string;
  description?: string;
  variant?: ToastVariant;
  duration?: number;
  action?: React.ReactNode;
}

interface ToastState extends EnhancedToastProps {
  id: string;
}

const TOAST_LIMIT = 5;
let toastCount = 0;

function generateId(): string {
  toastCount = (toastCount + 1) % Number.MAX_SAFE_INTEGER;
  return `toast-${toastCount}-${Date.now()}`;
}

type ToastActionType =
  | { type: "ADD_TOAST"; toast: ToastState }
  | { type: "REMOVE_TOAST"; id: string }
  | { type: "UPDATE_TOAST"; id: string; toast: Partial<ToastState> };

const toastReducer = (state: ToastState[], action: ToastActionType): ToastState[] => {
  switch (action.type) {
    case "ADD_TOAST":
      return [action.toast, ...state].slice(0, TOAST_LIMIT);
    case "REMOVE_TOAST":
      return state.filter((t) => t.id !== action.id);
    case "UPDATE_TOAST":
      return state.map((t) =>
        t.id === action.id ? { ...t, ...action.toast } : t
      );
    default:
      return state;
  }
};

// Global state for toasts
let listeners: Array<(state: ToastState[]) => void> = [];
let memoryState: ToastState[] = [];

function dispatch(action: ToastActionType) {
  memoryState = toastReducer(memoryState, action);
  listeners.forEach((listener) => listener(memoryState));
}

// ============================================================================
// Enhanced Toast Hook
// ============================================================================

export function useEnhancedToast() {
  const [state, setState] = React.useState<ToastState[]>(memoryState);

  React.useEffect(() => {
    listeners.push(setState);
    return () => {
      const index = listeners.indexOf(setState);
      if (index > -1) {
        listeners.splice(index, 1);
      }
    };
  }, []);

  const addToast = React.useCallback((options: ToastOptions) => {
    const id = generateId();
    const toast: ToastState = {
      id,
      ...options,
      onClose: () => removeToast(id),
    };
    dispatch({ type: "ADD_TOAST", toast });
    return id;
  }, []);

  const removeToast = React.useCallback((id: string) => {
    dispatch({ type: "REMOVE_TOAST", id });
  }, []);

  const updateToast = React.useCallback((id: string, options: Partial<ToastOptions>) => {
    dispatch({ type: "UPDATE_TOAST", id, toast: options });
  }, []);

  // Convenience methods
  const toast = React.useCallback((options: ToastOptions) => {
    return addToast({ variant: "default", ...options });
  }, [addToast]);

  const success = React.useCallback((title: string, description?: string) => {
    return addToast({ title, description, variant: "success" });
  }, [addToast]);

  const error = React.useCallback((title: string, description?: string) => {
    return addToast({ title, description, variant: "error" });
  }, [addToast]);

  const warning = React.useCallback((title: string, description?: string) => {
    return addToast({ title, description, variant: "warning" });
  }, [addToast]);

  const info = React.useCallback((title: string, description?: string) => {
    return addToast({ title, description, variant: "info" });
  }, [addToast]);

  const promise = React.useCallback(
    async <T,>(
      promise: Promise<T>,
      options: {
        loading: string;
        success: string | ((data: T) => string);
        error: string | ((error: Error) => string);
      }
    ): Promise<T> => {
      const id = addToast({ title: options.loading, variant: "info", duration: 0 });

      try {
        const data = await promise;
        const successMessage = typeof options.success === "function"
          ? options.success(data)
          : options.success;

        updateToast(id, {
          title: successMessage,
          variant: "success",
          duration: 5000
        });
        return data;
      } catch (err) {
        const error = err instanceof Error ? err : new Error("Unknown error");
        const errorMessage = typeof options.error === "function"
          ? options.error(error)
          : options.error;

        updateToast(id, {
          title: errorMessage,
          variant: "error",
          duration: 5000
        });
        throw err;
      }
    },
    [addToast, updateToast]
  );

  return {
    toasts: state,
    toast,
    success,
    error,
    warning,
    info,
    promise,
    dismiss: removeToast,
    dismissAll: () => {
      state.forEach((t) => removeToast(t.id));
    },
  };
}

/**
 * Error handling middleware for RTK Query
 */

import { isRejectedWithValue, Middleware } from '@reduxjs/toolkit';
import { addToast } from '../slices/uiSlice';
import { logout } from '../slices/authSlice';

/**
 * Middleware to handle API errors globally
 */
export const errorMiddleware: Middleware = (store) => (next) => (action) => {
  // Check if this is a rejected RTK Query action
  if (isRejectedWithValue(action)) {
    const error = action.payload;

    // Handle 401 Unauthorized - token expired
    if (error?.status === 401) {
      store.dispatch(logout());
      store.dispatch(
        addToast({
          type: 'error',
          message: 'Session expired. Please login again.',
          duration: 5000,
        })
      );
      return next(action);
    }

    // Handle 403 Forbidden
    if (error?.status === 403) {
      store.dispatch(
        addToast({
          type: 'error',
          message: 'Access denied. You do not have permission to perform this action.',
          duration: 5000,
        })
      );
      return next(action);
    }

    // Handle 404 Not Found
    if (error?.status === 404) {
      store.dispatch(
        addToast({
          type: 'error',
          message: 'Resource not found.',
          duration: 3000,
        })
      );
      return next(action);
    }

    // Handle 500 Server Error
    if (error?.status === 500) {
      store.dispatch(
        addToast({
          type: 'error',
          message: 'Server error. Please try again later.',
          duration: 5000,
        })
      );
      return next(action);
    }

    // Handle network errors
    if (error?.status === 'FETCH_ERROR') {
      store.dispatch(
        addToast({
          type: 'error',
          message: 'Network error. Please check your connection.',
          duration: 5000,
        })
      );
      return next(action);
    }

    // Handle validation errors (400)
    if (error?.status === 400 && error?.data?.message) {
      store.dispatch(
        addToast({
          type: 'error',
          message: error.data.message,
          duration: 4000,
        })
      );
      return next(action);
    }

    // Generic error handling
    const message = error?.data?.message || error?.error || 'An unexpected error occurred';
    store.dispatch(
      addToast({
        type: 'error',
        message,
        duration: 4000,
      })
    );
  }

  return next(action);
};

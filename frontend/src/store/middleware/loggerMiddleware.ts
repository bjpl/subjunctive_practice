/**
 * Logger middleware for development
 */

import { Middleware } from '@reduxjs/toolkit';

/**
 * Simple logger middleware for debugging (dev only)
 */
export const loggerMiddleware: Middleware = () => (next) => (action) => {
  if (process.env.NODE_ENV === 'development') {
    console.group(`Action: ${action.type}`);
    console.log('Payload:', action.payload);
    console.log('Timestamp:', new Date().toISOString());
    console.groupEnd();
  }
  return next(action);
};

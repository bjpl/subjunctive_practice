import { setupWorker } from 'msw/browser';
import { handlers } from './handlers';

// Setup MSW worker for browser environment (development/testing)
export const worker = setupWorker(...handlers);

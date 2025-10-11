import { setupServer } from 'msw/node';
import { handlers } from './handlers';

// Setup MSW server for Node environment (Jest tests)
export const server = setupServer(...handlers);

// Note: Lifecycle hooks are now in jest.setup.js to avoid import-time execution
// This prevents "beforeAll is not defined" errors when modules are imported outside Jest context

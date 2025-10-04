/**
 * Redux store configuration with RTK Query and persistence
 */

import { configureStore, combineReducers } from '@reduxjs/toolkit';
import {
  persistStore,
  persistReducer,
  FLUSH,
  REHYDRATE,
  PAUSE,
  PERSIST,
  PURGE,
  REGISTER,
} from 'redux-persist';
import storage from 'redux-persist/lib/storage';

// API
import { baseApi } from './api/baseApi';

// Reducers
import authReducer from './slices/authSlice';
import exerciseReducer from './slices/exerciseSlice';
import progressReducer from './slices/progressSlice';
import uiReducer from './slices/uiSlice';
import settingsReducer from './slices/settingsSlice';

// Middleware
import { errorMiddleware } from './middleware/errorMiddleware';
import { loggerMiddleware } from './middleware/loggerMiddleware';

// Persist configuration
const persistConfig = {
  key: 'root',
  version: 1,
  storage,
  whitelist: ['auth', 'settings', 'ui'], // Only persist these reducers
  blacklist: ['api', 'exercise', 'progress'], // Don't persist these
};

// Root reducer
const rootReducer = combineReducers({
  [baseApi.reducerPath]: baseApi.reducer,
  auth: authReducer,
  exercise: exerciseReducer,
  progress: progressReducer,
  ui: uiReducer,
  settings: settingsReducer,
});

// Persisted reducer
const persistedReducer = persistReducer(persistConfig, rootReducer);

// Configure store
export const store = configureStore({
  reducer: persistedReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
      },
    })
      .concat(baseApi.middleware)
      .concat(errorMiddleware)
      .concat(loggerMiddleware),
  devTools: process.env.NODE_ENV !== 'production',
});

// Persistor
export const persistor = persistStore(store);

// Export types
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

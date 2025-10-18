import { configureStore } from "@reduxjs/toolkit";
import { persistStore, persistReducer } from "redux-persist";
import storage from "redux-persist/lib/storage";
import { combineReducers } from "redux";
import authReducer from "./slices/authSlice";
import exerciseReducer from "./slices/exerciseSlice";
import progressReducer from "./slices/progressSlice";
import uiReducer from "./slices/uiSlice";
import settingsReducer from "./slices/settingsSlice";
import { api } from "./services/api";

const persistConfig = {
  key: "root",
  storage,
  whitelist: ["auth", "settings"], // Persist auth and settings state
};

const rootReducer = combineReducers({
  auth: authReducer,
  exercise: exerciseReducer,
  progress: progressReducer,
  ui: uiReducer,
  settings: settingsReducer,
  [api.reducerPath]: api.reducer,
});

const persistedReducer = persistReducer(persistConfig, rootReducer);

export const store = configureStore({
  reducer: persistedReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ["persist/PERSIST", "persist/REHYDRATE"],
      },
    }).concat(api.middleware),
  devTools: process.env.NODE_ENV !== "production",
});

export const persistor = persistStore(store);

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

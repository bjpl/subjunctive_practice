import { renderHook } from '@testing-library/react';
import { Provider } from 'react-redux';
import { configureStore } from '@reduxjs/toolkit';
import { useAppDispatch, useAppSelector } from '@/hooks/use-redux';
import authReducer, { logout } from '@/store/slices/auth-slice';

const createTestStore = () =>
  configureStore({
    reducer: {
      auth: authReducer,
    },
  });

const wrapper = ({ children }: { children: React.ReactNode }) => (
  <Provider store={createTestStore()}>{children}</Provider>
);

describe('useAppDispatch Hook', () => {
  it('returns dispatch function', () => {
    const { result } = renderHook(() => useAppDispatch(), { wrapper });
    expect(typeof result.current).toBe('function');
  });

  it('can dispatch actions', () => {
    const { result } = renderHook(() => useAppDispatch(), { wrapper });
    expect(() => result.current(logout())).not.toThrow();
  });
});

describe('useAppSelector Hook', () => {
  it('selects state from store', () => {
    const { result } = renderHook(
      () => useAppSelector((state) => state.auth.isAuthenticated),
      { wrapper }
    );
    expect(result.current).toBe(false);
  });

  it('updates when state changes', () => {
    const store = createTestStore();
    const customWrapper = ({ children }: { children: React.ReactNode }) => (
      <Provider store={store}>{children}</Provider>
    );

    const { result } = renderHook(
      () => useAppSelector((state) => state.auth.isAuthenticated),
      { wrapper: customWrapper }
    );

    expect(result.current).toBe(false);

    // Dispatch action to change state
    store.dispatch({
      type: 'auth/login/fulfilled',
      payload: { user: { id: 1 }, access_token: 'token' },
    });

    // Hook should re-render with new state
    expect(result.current).toBe(true);
  });

  it('can select complex state', () => {
    const store = createTestStore();
    const customWrapper = ({ children }: { children: React.ReactNode }) => (
      <Provider store={store}>{children}</Provider>
    );

    store.dispatch({
      type: 'auth/login/fulfilled',
      payload: {
        user: { id: 1, email: 'test@example.com', username: 'testuser' },
        access_token: 'token',
      },
    });

    const { result } = renderHook(
      () => useAppSelector((state) => state.auth.user),
      { wrapper: customWrapper }
    );

    expect(result.current).toEqual({
      id: 1,
      email: 'test@example.com',
      username: 'testuser',
    });
  });
});

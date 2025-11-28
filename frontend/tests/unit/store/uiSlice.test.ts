import uiReducer, {
  openModal,
  closeModal,
  addToast,
  removeToast,
  clearAllToasts,
  setGlobalLoading,
  toggleSidebar,
  setSidebarOpen,
  setActiveTab,
  resetUIState,
} from '@/store/slices/uiSlice';
import type { ToastNotification } from '@/types';

const mockToast: ToastNotification = {
  id: 'toast-1',
  type: 'success',
  message: 'Exercise completed!',
  duration: 3000,
};

describe('uiSlice', () => {
  describe('initial state', () => {
    it('should have correct initial state', () => {
      const state = uiReducer(undefined, { type: 'unknown' });

      expect(state).toEqual({
        modal: {
          isOpen: false,
          type: null,
          data: undefined,
        },
        toasts: [],
        isGlobalLoading: false,
        isSidebarOpen: true,
        activeTab: null,
      });
    });
  });

  describe('openModal', () => {
    it('should open modal with type', () => {
      const state = uiReducer(undefined, openModal({ type: 'confirm' }));

      expect(state.modal.isOpen).toBe(true);
      expect(state.modal.type).toBe('confirm');
      expect(state.modal.data).toBeUndefined();
    });

    it('should open modal with type and data', () => {
      const modalData = { message: 'Are you sure?', action: 'delete' };
      const state = uiReducer(
        undefined,
        openModal({ type: 'confirm', data: modalData })
      );

      expect(state.modal.isOpen).toBe(true);
      expect(state.modal.type).toBe('confirm');
      expect(state.modal.data).toEqual(modalData);
    });

    it('should replace existing modal', () => {
      const initialState = {
        ...uiReducer(undefined, { type: 'unknown' }),
        modal: {
          isOpen: true,
          type: 'old-modal',
          data: { old: 'data' },
        },
      };

      const state = uiReducer(
        initialState,
        openModal({ type: 'new-modal', data: { new: 'data' } })
      );

      expect(state.modal.type).toBe('new-modal');
      expect(state.modal.data).toEqual({ new: 'data' });
    });
  });

  describe('closeModal', () => {
    it('should close modal and clear data', () => {
      const initialState = {
        ...uiReducer(undefined, { type: 'unknown' }),
        modal: {
          isOpen: true,
          type: 'confirm',
          data: { message: 'test' },
        },
      };

      const state = uiReducer(initialState, closeModal());

      expect(state.modal.isOpen).toBe(false);
      expect(state.modal.type).toBeNull();
      expect(state.modal.data).toBeUndefined();
    });

    it('should handle closing already closed modal', () => {
      const state = uiReducer(undefined, closeModal());

      expect(state.modal.isOpen).toBe(false);
      expect(state.modal.type).toBeNull();
    });
  });

  describe('addToast', () => {
    it('should add toast to empty list', () => {
      const state = uiReducer(undefined, addToast(mockToast));

      expect(state.toasts).toHaveLength(1);
      expect(state.toasts[0]).toEqual(mockToast);
    });

    it('should append toast to existing toasts', () => {
      const existingToast: ToastNotification = {
        id: 'toast-0',
        type: 'info',
        message: 'Existing toast',
      };

      const initialState = {
        ...uiReducer(undefined, { type: 'unknown' }),
        toasts: [existingToast],
      };

      const state = uiReducer(initialState, addToast(mockToast));

      expect(state.toasts).toHaveLength(2);
      expect(state.toasts[0]).toEqual(existingToast);
      expect(state.toasts[1]).toEqual(mockToast);
    });

    it('should handle different toast types', () => {
      let state = uiReducer(undefined, { type: 'unknown' });

      const successToast: ToastNotification = { id: '1', type: 'success', message: 'Success' };
      state = uiReducer(state, addToast(successToast));

      const errorToast: ToastNotification = { id: '2', type: 'error', message: 'Error' };
      state = uiReducer(state, addToast(errorToast));

      const warningToast: ToastNotification = { id: '3', type: 'warning', message: 'Warning' };
      state = uiReducer(state, addToast(warningToast));

      const infoToast: ToastNotification = { id: '4', type: 'info', message: 'Info' };
      state = uiReducer(state, addToast(infoToast));

      expect(state.toasts).toHaveLength(4);
      expect(state.toasts[0].type).toBe('success');
      expect(state.toasts[1].type).toBe('error');
      expect(state.toasts[2].type).toBe('warning');
      expect(state.toasts[3].type).toBe('info');
    });
  });

  describe('removeToast', () => {
    it('should remove toast by id', () => {
      const toast1: ToastNotification = { id: 'toast-1', type: 'success', message: 'First' };
      const toast2: ToastNotification = { id: 'toast-2', type: 'info', message: 'Second' };

      const initialState = {
        ...uiReducer(undefined, { type: 'unknown' }),
        toasts: [toast1, toast2],
      };

      const state = uiReducer(initialState, removeToast('toast-1'));

      expect(state.toasts).toHaveLength(1);
      expect(state.toasts[0]).toEqual(toast2);
    });

    it('should handle removing non-existent toast', () => {
      const initialState = {
        ...uiReducer(undefined, { type: 'unknown' }),
        toasts: [mockToast],
      };

      const state = uiReducer(initialState, removeToast('non-existent'));

      expect(state.toasts).toHaveLength(1);
      expect(state.toasts[0]).toEqual(mockToast);
    });

    it('should handle empty toast list', () => {
      const state = uiReducer(undefined, removeToast('toast-1'));

      expect(state.toasts).toHaveLength(0);
    });
  });

  describe('clearAllToasts', () => {
    it('should clear all toasts', () => {
      const toast1: ToastNotification = { id: 'toast-1', type: 'success', message: 'First' };
      const toast2: ToastNotification = { id: 'toast-2', type: 'info', message: 'Second' };
      const toast3: ToastNotification = { id: 'toast-3', type: 'error', message: 'Third' };

      const initialState = {
        ...uiReducer(undefined, { type: 'unknown' }),
        toasts: [toast1, toast2, toast3],
      };

      const state = uiReducer(initialState, clearAllToasts());

      expect(state.toasts).toHaveLength(0);
    });

    it('should handle clearing empty toast list', () => {
      const state = uiReducer(undefined, clearAllToasts());

      expect(state.toasts).toHaveLength(0);
    });
  });

  describe('setGlobalLoading', () => {
    it('should enable global loading', () => {
      const state = uiReducer(undefined, setGlobalLoading(true));

      expect(state.isGlobalLoading).toBe(true);
    });

    it('should disable global loading', () => {
      const initialState = {
        ...uiReducer(undefined, { type: 'unknown' }),
        isGlobalLoading: true,
      };

      const state = uiReducer(initialState, setGlobalLoading(false));

      expect(state.isGlobalLoading).toBe(false);
    });
  });

  describe('toggleSidebar', () => {
    it('should toggle sidebar from open to closed', () => {
      const state = uiReducer(undefined, toggleSidebar());

      expect(state.isSidebarOpen).toBe(false);
    });

    it('should toggle sidebar from closed to open', () => {
      const initialState = {
        ...uiReducer(undefined, { type: 'unknown' }),
        isSidebarOpen: false,
      };

      const state = uiReducer(initialState, toggleSidebar());

      expect(state.isSidebarOpen).toBe(true);
    });

    it('should toggle multiple times', () => {
      let state = uiReducer(undefined, { type: 'unknown' });
      expect(state.isSidebarOpen).toBe(true);

      state = uiReducer(state, toggleSidebar());
      expect(state.isSidebarOpen).toBe(false);

      state = uiReducer(state, toggleSidebar());
      expect(state.isSidebarOpen).toBe(true);

      state = uiReducer(state, toggleSidebar());
      expect(state.isSidebarOpen).toBe(false);
    });
  });

  describe('setSidebarOpen', () => {
    it('should open sidebar', () => {
      const initialState = {
        ...uiReducer(undefined, { type: 'unknown' }),
        isSidebarOpen: false,
      };

      const state = uiReducer(initialState, setSidebarOpen(true));

      expect(state.isSidebarOpen).toBe(true);
    });

    it('should close sidebar', () => {
      const state = uiReducer(undefined, setSidebarOpen(false));

      expect(state.isSidebarOpen).toBe(false);
    });
  });

  describe('setActiveTab', () => {
    it('should set active tab', () => {
      const state = uiReducer(undefined, setActiveTab('practice'));

      expect(state.activeTab).toBe('practice');
    });

    it('should change active tab', () => {
      const initialState = {
        ...uiReducer(undefined, { type: 'unknown' }),
        activeTab: 'practice',
      };

      const state = uiReducer(initialState, setActiveTab('progress'));

      expect(state.activeTab).toBe('progress');
    });

    it('should set active tab to null', () => {
      const initialState = {
        ...uiReducer(undefined, { type: 'unknown' }),
        activeTab: 'practice',
      };

      const state = uiReducer(initialState, setActiveTab(null));

      expect(state.activeTab).toBeNull();
    });
  });

  describe('resetUIState', () => {
    it('should reset to initial state', () => {
      const modifiedState = {
        modal: {
          isOpen: true,
          type: 'confirm',
          data: { test: 'data' },
        },
        toasts: [mockToast],
        isGlobalLoading: true,
        isSidebarOpen: false,
        activeTab: 'practice',
      };

      const state = uiReducer(modifiedState, resetUIState());

      expect(state).toEqual({
        modal: {
          isOpen: false,
          type: null,
          data: undefined,
        },
        toasts: [],
        isGlobalLoading: false,
        isSidebarOpen: true,
        activeTab: null,
      });
    });
  });

  describe('complex scenarios', () => {
    it('should handle multiple toasts being added and removed', () => {
      let state = uiReducer(undefined, { type: 'unknown' });

      const toast1: ToastNotification = { id: '1', type: 'success', message: 'First' };
      state = uiReducer(state, addToast(toast1));

      const toast2: ToastNotification = { id: '2', type: 'info', message: 'Second' };
      state = uiReducer(state, addToast(toast2));

      expect(state.toasts).toHaveLength(2);

      state = uiReducer(state, removeToast('1'));
      expect(state.toasts).toHaveLength(1);
      expect(state.toasts[0]).toEqual(toast2);

      const toast3: ToastNotification = { id: '3', type: 'error', message: 'Third' };
      state = uiReducer(state, addToast(toast3));

      expect(state.toasts).toHaveLength(2);

      state = uiReducer(state, clearAllToasts());
      expect(state.toasts).toHaveLength(0);
    });

    it('should handle modal opening, closing, and reopening', () => {
      let state = uiReducer(undefined, { type: 'unknown' });

      state = uiReducer(state, openModal({ type: 'settings' }));
      expect(state.modal.isOpen).toBe(true);

      state = uiReducer(state, closeModal());
      expect(state.modal.isOpen).toBe(false);

      state = uiReducer(state, openModal({ type: 'confirm', data: { message: 'test' } }));
      expect(state.modal.isOpen).toBe(true);
      expect(state.modal.data).toEqual({ message: 'test' });
    });
  });
});

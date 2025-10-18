import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import type { ToastNotification } from "@/types";

interface ModalState {
  isOpen: boolean;
  type: string | null;
  data?: any;
}

interface UIState {
  modal: ModalState;
  toasts: ToastNotification[];
  isGlobalLoading: boolean;
  isSidebarOpen: boolean;
  activeTab: string | null;
}

const initialState: UIState = {
  modal: {
    isOpen: false,
    type: null,
    data: undefined,
  },
  toasts: [],
  isGlobalLoading: false,
  isSidebarOpen: true,
  activeTab: null,
};

const uiSlice = createSlice({
  name: "ui",
  initialState,
  reducers: {
    openModal: (state, action: PayloadAction<{ type: string; data?: any }>) => {
      state.modal.isOpen = true;
      state.modal.type = action.payload.type;
      state.modal.data = action.payload.data;
    },
    closeModal: (state) => {
      state.modal.isOpen = false;
      state.modal.type = null;
      state.modal.data = undefined;
    },
    addToast: (state, action: PayloadAction<ToastNotification>) => {
      state.toasts.push(action.payload);
    },
    removeToast: (state, action: PayloadAction<string>) => {
      state.toasts = state.toasts.filter((toast) => toast.id !== action.payload);
    },
    clearAllToasts: (state) => {
      state.toasts = [];
    },
    setGlobalLoading: (state, action: PayloadAction<boolean>) => {
      state.isGlobalLoading = action.payload;
    },
    toggleSidebar: (state) => {
      state.isSidebarOpen = !state.isSidebarOpen;
    },
    setSidebarOpen: (state, action: PayloadAction<boolean>) => {
      state.isSidebarOpen = action.payload;
    },
    setActiveTab: (state, action: PayloadAction<string | null>) => {
      state.activeTab = action.payload;
    },
    resetUIState: () => initialState,
  },
});

export const {
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
} = uiSlice.actions;

export default uiSlice.reducer;

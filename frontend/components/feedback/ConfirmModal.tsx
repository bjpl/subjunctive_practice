"use client";

import * as React from "react";
import * as AlertDialog from "@radix-ui/react-alert-dialog";
import { motion, AnimatePresence } from "framer-motion";
import { AlertTriangle, Info, CheckCircle, XCircle } from "lucide-react";
import { cn } from "@/lib/utils";
import { modalBackdropVariants, modalContentVariants } from "@/lib/animations";

export type ConfirmVariant = "danger" | "warning" | "info" | "success";

interface ConfirmModalProps {
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
  title: string;
  description: string;
  variant?: ConfirmVariant;
  confirmLabel?: string;
  cancelLabel?: string;
  onConfirm: () => void | Promise<void>;
  onCancel?: () => void;
  loading?: boolean;
  children?: React.ReactNode;
}

const variantConfig = {
  danger: {
    icon: XCircle,
    iconColor: "text-red-600 dark:text-red-400",
    iconBg: "bg-red-100 dark:bg-red-900/20",
    confirmButton: "bg-red-600 hover:bg-red-700 focus:ring-red-500 text-white",
  },
  warning: {
    icon: AlertTriangle,
    iconColor: "text-yellow-600 dark:text-yellow-400",
    iconBg: "bg-yellow-100 dark:bg-yellow-900/20",
    confirmButton: "bg-yellow-600 hover:bg-yellow-700 focus:ring-yellow-500 text-white",
  },
  info: {
    icon: Info,
    iconColor: "text-blue-600 dark:text-blue-400",
    iconBg: "bg-blue-100 dark:bg-blue-900/20",
    confirmButton: "bg-blue-600 hover:bg-blue-700 focus:ring-blue-500 text-white",
  },
  success: {
    icon: CheckCircle,
    iconColor: "text-green-600 dark:text-green-400",
    iconBg: "bg-green-100 dark:bg-green-900/20",
    confirmButton: "bg-green-600 hover:bg-green-700 focus:ring-green-500 text-white",
  },
};

export const ConfirmModal: React.FC<ConfirmModalProps> = ({
  open,
  onOpenChange,
  title,
  description,
  variant = "info",
  confirmLabel = "Confirm",
  cancelLabel = "Cancel",
  onConfirm,
  onCancel,
  loading = false,
  children,
}) => {
  const [isLoading, setIsLoading] = React.useState(false);
  const config = variantConfig[variant];
  const Icon = config.icon;

  const handleConfirm = async () => {
    try {
      setIsLoading(true);
      await onConfirm();
      onOpenChange?.(false);
    } catch (error) {
      console.error("Confirm action failed:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancel = () => {
    onCancel?.();
    onOpenChange?.(false);
  };

  return (
    <AlertDialog.Root open={open} onOpenChange={onOpenChange}>
      {children}

      <AnimatePresence>
        {open && (
          <AlertDialog.Portal forceMount>
            {/* Backdrop */}
            <AlertDialog.Overlay asChild>
              <motion.div
                variants={modalBackdropVariants}
                initial="hidden"
                animate="visible"
                exit="exit"
                className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm"
              />
            </AlertDialog.Overlay>

            {/* Content */}
            <AlertDialog.Content asChild>
              <motion.div
                variants={modalContentVariants}
                initial="hidden"
                animate="visible"
                exit="exit"
                className="fixed left-1/2 top-1/2 z-50 w-full max-w-md -translate-x-1/2 -translate-y-1/2 p-4"
              >
                <div className="rounded-lg border bg-white dark:bg-gray-800 shadow-lg">
                  <div className="p-6">
                    {/* Icon */}
                    <div className="flex justify-center mb-4">
                      <div className={cn("rounded-full p-3", config.iconBg)}>
                        <Icon className={cn("h-6 w-6", config.iconColor)} />
                      </div>
                    </div>

                    {/* Title */}
                    <AlertDialog.Title className="text-lg font-semibold text-center text-gray-900 dark:text-gray-100 mb-2">
                      {title}
                    </AlertDialog.Title>

                    {/* Description */}
                    <AlertDialog.Description className="text-sm text-center text-gray-600 dark:text-gray-400 mb-6">
                      {description}
                    </AlertDialog.Description>

                    {/* Actions */}
                    <div className="flex flex-col-reverse sm:flex-row gap-3">
                      <AlertDialog.Cancel asChild>
                        <button
                          onClick={handleCancel}
                          disabled={isLoading || loading}
                          className={cn(
                            "flex-1 px-4 py-2.5 rounded-md font-medium",
                            "border border-gray-300 dark:border-gray-600",
                            "bg-white dark:bg-gray-700",
                            "text-gray-700 dark:text-gray-200",
                            "hover:bg-gray-50 dark:hover:bg-gray-600",
                            "focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2",
                            "disabled:opacity-50 disabled:cursor-not-allowed",
                            "transition-colors"
                          )}
                        >
                          {cancelLabel}
                        </button>
                      </AlertDialog.Cancel>

                      <AlertDialog.Action asChild>
                        <button
                          onClick={handleConfirm}
                          disabled={isLoading || loading}
                          className={cn(
                            "flex-1 px-4 py-2.5 rounded-md font-medium",
                            "focus:outline-none focus:ring-2 focus:ring-offset-2",
                            "disabled:opacity-50 disabled:cursor-not-allowed",
                            "transition-colors inline-flex items-center justify-center gap-2",
                            config.confirmButton
                          )}
                        >
                          {(isLoading || loading) && (
                            <motion.div
                              className="h-4 w-4 border-2 border-current border-t-transparent rounded-full"
                              animate={{ rotate: 360 }}
                              transition={{
                                duration: 1,
                                repeat: Infinity,
                                ease: "linear",
                              }}
                            />
                          )}
                          {confirmLabel}
                        </button>
                      </AlertDialog.Action>
                    </div>
                  </div>
                </div>
              </motion.div>
            </AlertDialog.Content>
          </AlertDialog.Portal>
        )}
      </AnimatePresence>
    </AlertDialog.Root>
  );
};

// ============================================================================
// Trigger Component
// ============================================================================

export const ConfirmModalTrigger = AlertDialog.Trigger;

// ============================================================================
// Hook for Imperative Usage
// ============================================================================

interface UseConfirmModalOptions {
  title: string;
  description: string;
  variant?: ConfirmVariant;
  confirmLabel?: string;
  cancelLabel?: string;
}

export function useConfirmModal() {
  const [isOpen, setIsOpen] = React.useState(false);
  const [config, setConfig] = React.useState<UseConfirmModalOptions | null>(null);
  const resolveRef = React.useRef<((value: boolean) => void) | null>(null);

  const confirm = React.useCallback((options: UseConfirmModalOptions): Promise<boolean> => {
    setConfig(options);
    setIsOpen(true);

    return new Promise((resolve) => {
      resolveRef.current = resolve;
    });
  }, []);

  const handleConfirm = React.useCallback(() => {
    resolveRef.current?.(true);
    setIsOpen(false);
    setConfig(null);
  }, []);

  const handleCancel = React.useCallback(() => {
    resolveRef.current?.(false);
    setIsOpen(false);
    setConfig(null);
  }, []);

  const ConfirmModalComponent = React.useCallback(() => {
    if (!config) return null;

    return (
      <ConfirmModal
        open={isOpen}
        onOpenChange={setIsOpen}
        title={config.title}
        description={config.description}
        variant={config.variant}
        confirmLabel={config.confirmLabel}
        cancelLabel={config.cancelLabel}
        onConfirm={handleConfirm}
        onCancel={handleCancel}
      />
    );
  }, [isOpen, config, handleConfirm, handleCancel]);

  return {
    confirm,
    ConfirmModal: ConfirmModalComponent,
  };
}

"use client";

import * as React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, CheckCircle2, XCircle, AlertCircle, Info } from "lucide-react";
import { cn } from "@/lib/utils";
import { toastVariants } from "@/lib/animations";

export type ToastVariant = "default" | "success" | "error" | "warning" | "info";

export interface EnhancedToastProps {
  id: string;
  title?: string;
  description?: string;
  variant?: ToastVariant;
  duration?: number;
  action?: React.ReactNode;
  onClose?: () => void;
}

const variantStyles: Record<ToastVariant, string> = {
  default: "bg-background border-border text-foreground",
  success: "bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800 text-green-900 dark:text-green-100",
  error: "bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800 text-red-900 dark:text-red-100",
  warning: "bg-yellow-50 dark:bg-yellow-900/20 border-yellow-200 dark:border-yellow-800 text-yellow-900 dark:text-yellow-100",
  info: "bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800 text-blue-900 dark:text-blue-100",
};

const variantIcons: Record<ToastVariant, React.ReactNode> = {
  default: null,
  success: <CheckCircle2 className="h-5 w-5 text-green-600 dark:text-green-400" />,
  error: <XCircle className="h-5 w-5 text-red-600 dark:text-red-400" />,
  warning: <AlertCircle className="h-5 w-5 text-yellow-600 dark:text-yellow-400" />,
  info: <Info className="h-5 w-5 text-blue-600 dark:text-blue-400" />,
};

export const EnhancedToast: React.FC<EnhancedToastProps> = ({
  id,
  title,
  description,
  variant = "default",
  duration = 5000,
  action,
  onClose,
}) => {
  const [progress, setProgress] = React.useState(100);

  React.useEffect(() => {
    if (!duration || duration <= 0) return;

    const startTime = Date.now();
    const interval = setInterval(() => {
      const elapsed = Date.now() - startTime;
      const remaining = Math.max(0, 100 - (elapsed / duration) * 100);
      setProgress(remaining);

      if (remaining <= 0) {
        clearInterval(interval);
        onClose?.();
      }
    }, 16); // ~60fps

    return () => clearInterval(interval);
  }, [duration, onClose]);

  const icon = variantIcons[variant];

  return (
    <motion.div
      layout
      variants={toastVariants}
      initial="initial"
      animate="animate"
      exit="exit"
      className={cn(
        "pointer-events-auto relative flex w-full max-w-md items-start gap-3 overflow-hidden rounded-lg border p-4 pr-8 shadow-lg",
        variantStyles[variant]
      )}
      role="alert"
      aria-live="polite"
    >
      {/* Icon */}
      {icon && <div className="flex-shrink-0 mt-0.5">{icon}</div>}

      {/* Content */}
      <div className="flex-1 space-y-1">
        {title && (
          <div className="text-sm font-semibold leading-none tracking-tight">
            {title}
          </div>
        )}
        {description && (
          <div className="text-sm opacity-90 leading-snug">
            {description}
          </div>
        )}
        {action && <div className="mt-2">{action}</div>}
      </div>

      {/* Close Button */}
      <button
        onClick={onClose}
        className="absolute right-2 top-2 rounded-md p-1 opacity-60 transition-opacity hover:opacity-100 focus:opacity-100 focus:outline-none focus:ring-2 focus:ring-offset-1"
        aria-label="Close notification"
      >
        <X className="h-4 w-4" />
      </button>

      {/* Progress Bar */}
      {duration > 0 && (
        <motion.div
          className="absolute bottom-0 left-0 h-1 bg-current opacity-30"
          initial={{ width: "100%" }}
          animate={{ width: `${progress}%` }}
          transition={{ duration: 0.1, ease: "linear" }}
        />
      )}
    </motion.div>
  );
};

// ============================================================================
// Toast Container Component
// ============================================================================

interface ToastContainerProps {
  toasts: EnhancedToastProps[];
  position?: "top-right" | "top-left" | "bottom-right" | "bottom-left" | "top-center" | "bottom-center";
}

const positionStyles = {
  "top-right": "top-4 right-4 items-end",
  "top-left": "top-4 left-4 items-start",
  "bottom-right": "bottom-4 right-4 items-end",
  "bottom-left": "bottom-4 left-4 items-start",
  "top-center": "top-4 left-1/2 -translate-x-1/2 items-center",
  "bottom-center": "bottom-4 left-1/2 -translate-x-1/2 items-center",
};

export const ToastContainer: React.FC<ToastContainerProps> = ({
  toasts,
  position = "top-right",
}) => {
  return (
    <div
      className={cn(
        "fixed z-[100] flex max-h-screen w-full max-w-md flex-col gap-2 p-4 pointer-events-none",
        positionStyles[position]
      )}
    >
      <AnimatePresence mode="popLayout">
        {toasts.map((toast) => (
          <EnhancedToast key={toast.id} {...toast} />
        ))}
      </AnimatePresence>
    </div>
  );
};

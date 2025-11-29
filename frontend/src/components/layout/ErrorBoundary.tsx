"use client";

import * as React from "react";
import { motion } from "framer-motion";
import { AlertTriangle, RefreshCw, Home, Bug } from "lucide-react";
import { cn } from "@/lib/utils";
import { fadeInVariants, errorShakeVariants } from "@/lib/animations";

interface ErrorBoundaryProps {
  children: React.ReactNode;
  fallback?: React.ComponentType<ErrorBoundaryFallbackProps>;
  onError?: (error: Error, errorInfo: React.ErrorInfo) => void;
  onReset?: () => void;
}

export interface ErrorBoundaryFallbackProps {
  error: Error;
  resetError: () => void;
  componentStack?: string;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
  errorInfo: React.ErrorInfo | null;
}

export class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    };
  }

  static getDerivedStateFromError(error: Error): Partial<ErrorBoundaryState> {
    return {
      hasError: true,
      error,
    };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo): void {
    this.setState({
      errorInfo,
    });

    // Log error to console in development
    if (process.env.NODE_ENV === "development") {
      console.error("ErrorBoundary caught an error:", error, errorInfo);
    }

    // Call custom error handler
    this.props.onError?.(error, errorInfo);
  }

  resetError = (): void => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
    });
    this.props.onReset?.();
  };

  render(): React.ReactNode {
    if (this.state.hasError && this.state.error) {
      const FallbackComponent = this.props.fallback || DefaultErrorFallback;
      return (
        <FallbackComponent
          error={this.state.error}
          resetError={this.resetError}
          componentStack={this.state.errorInfo?.componentStack ?? undefined}
        />
      );
    }

    return this.props.children;
  }
}

// ============================================================================
// Default Error Fallback Component
// ============================================================================

export const DefaultErrorFallback: React.FC<ErrorBoundaryFallbackProps> = ({
  error,
  resetError,
  componentStack,
}) => {
  const [showDetails, setShowDetails] = React.useState(false);

  const handleGoHome = () => {
    window.location.href = "/";
  };

  const handleReportBug = () => {
    // In a real app, this would open a bug report modal or redirect to a bug tracker
    const subject = encodeURIComponent(`Bug Report: ${error.message}`);
    const body = encodeURIComponent(
      `Error: ${error.message}\n\nStack: ${error.stack}\n\nComponent Stack: ${componentStack || "N/A"}`
    );
    console.log("Bug report data:", { subject, body });
  };

  return (
    <motion.div
      variants={fadeInVariants}
      initial="hidden"
      animate="visible"
      className="flex min-h-screen items-center justify-center bg-gray-50 dark:bg-gray-900 p-4"
    >
      <motion.div
        variants={errorShakeVariants}
        animate="shake"
        className="w-full max-w-2xl rounded-lg border border-red-200 bg-white dark:bg-gray-800 dark:border-red-800 p-8 shadow-lg"
      >
        {/* Icon */}
        <div className="flex justify-center mb-6">
          <div className="rounded-full bg-red-100 dark:bg-red-900/20 p-4">
            <AlertTriangle className="h-12 w-12 text-red-600 dark:text-red-400" />
          </div>
        </div>

        {/* Title */}
        <h1 className="text-2xl font-bold text-center text-gray-900 dark:text-gray-100 mb-2">
          Oops! Something went wrong
        </h1>

        {/* Description */}
        <p className="text-center text-gray-600 dark:text-gray-400 mb-6">
          We encountered an unexpected error. Don&apos;t worry, you can try one of the options below.
        </p>

        {/* Error Message */}
        <div className="mb-6 rounded-md bg-red-50 dark:bg-red-900/10 border border-red-200 dark:border-red-800 p-4">
          <p className="text-sm font-mono text-red-800 dark:text-red-200 break-words">
            {error.message}
          </p>
        </div>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-3 mb-6">
          <button
            onClick={resetError}
            className={cn(
              "flex-1 inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-md",
              "bg-blue-600 text-white font-medium",
              "hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2",
              "transition-colors"
            )}
          >
            <RefreshCw className="h-4 w-4" />
            Try Again
          </button>

          <button
            onClick={handleGoHome}
            className={cn(
              "flex-1 inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-md",
              "border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-200 font-medium",
              "hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2",
              "transition-colors"
            )}
          >
            <Home className="h-4 w-4" />
            Go Home
          </button>

          <button
            onClick={handleReportBug}
            className={cn(
              "flex-1 inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-md",
              "border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-200 font-medium",
              "hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2",
              "transition-colors"
            )}
          >
            <Bug className="h-4 w-4" />
            Report Bug
          </button>
        </div>

        {/* Technical Details Toggle */}
        {process.env.NODE_ENV === "development" && (
          <div className="border-t border-gray-200 dark:border-gray-700 pt-4">
            <button
              onClick={() => setShowDetails(!showDetails)}
              className="text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 underline"
            >
              {showDetails ? "Hide" : "Show"} technical details
            </button>

            {showDetails && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                className="mt-4 space-y-4"
              >
                {/* Stack Trace */}
                <div>
                  <h3 className="text-sm font-semibold text-gray-900 dark:text-gray-100 mb-2">
                    Stack Trace:
                  </h3>
                  <pre className="text-xs bg-gray-100 dark:bg-gray-900 p-4 rounded-md overflow-x-auto max-h-64 overflow-y-auto">
                    <code className="text-gray-800 dark:text-gray-200">
                      {error.stack}
                    </code>
                  </pre>
                </div>

                {/* Component Stack */}
                {componentStack && (
                  <div>
                    <h3 className="text-sm font-semibold text-gray-900 dark:text-gray-100 mb-2">
                      Component Stack:
                    </h3>
                    <pre className="text-xs bg-gray-100 dark:bg-gray-900 p-4 rounded-md overflow-x-auto max-h-64 overflow-y-auto">
                      <code className="text-gray-800 dark:text-gray-200">
                        {componentStack}
                      </code>
                    </pre>
                  </div>
                )}
              </motion.div>
            )}
          </div>
        )}
      </motion.div>
    </motion.div>
  );
};

// ============================================================================
// Compact Error Fallback (for smaller components)
// ============================================================================

export const CompactErrorFallback: React.FC<ErrorBoundaryFallbackProps> = ({
  error,
  resetError,
}) => {
  return (
    <div className="flex flex-col items-center justify-center p-6 text-center space-y-4">
      <AlertTriangle className="h-8 w-8 text-red-500" />
      <div>
        <h3 className="font-semibold text-gray-900 dark:text-gray-100">
          Something went wrong
        </h3>
        <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
          {error.message}
        </p>
      </div>
      <button
        onClick={resetError}
        className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
      >
        <RefreshCw className="h-4 w-4" />
        Try Again
      </button>
    </div>
  );
};

"use client";

import * as React from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import { skeletonPulseVariants } from "@/lib/animations";

interface SkeletonProps {
  className?: string;
  variant?: "text" | "circular" | "rectangular";
  width?: string | number;
  height?: string | number;
  animation?: "pulse" | "wave" | "none";
}

export const Skeleton: React.FC<SkeletonProps> = ({
  className,
  variant = "rectangular",
  width,
  height,
  animation = "pulse",
}) => {
  const variantClasses = {
    text: "h-4 rounded",
    circular: "rounded-full",
    rectangular: "rounded-md",
  };

  const animationClasses = {
    pulse: "",
    wave: "bg-gradient-to-r from-gray-200 via-gray-300 to-gray-200 dark:from-gray-800 dark:via-gray-700 dark:to-gray-800 bg-[length:200%_100%] animate-shimmer",
    none: "",
  };

  const style: React.CSSProperties = {
    width: width || undefined,
    height: height || undefined,
  };

  const Component = animation === "pulse" ? motion.div : "div";
  const animationProps = animation === "pulse"
    ? { variants: skeletonPulseVariants, animate: "pulse" }
    : {};

  return (
    <Component
      className={cn(
        "bg-gray-200 dark:bg-gray-800",
        variantClasses[variant],
        animationClasses[animation],
        className
      )}
      style={style}
      {...animationProps}
    />
  );
};

// ============================================================================
// Predefined Skeleton Patterns
// ============================================================================

export const CardSkeleton: React.FC<{ className?: string }> = ({ className }) => {
  return (
    <div className={cn("rounded-lg border p-6 space-y-4", className)}>
      <div className="flex items-center gap-4">
        <Skeleton variant="circular" width={48} height={48} />
        <div className="flex-1 space-y-2">
          <Skeleton width="60%" height={16} />
          <Skeleton width="40%" height={12} />
        </div>
      </div>
      <div className="space-y-2">
        <Skeleton width="100%" height={12} />
        <Skeleton width="90%" height={12} />
        <Skeleton width="70%" height={12} />
      </div>
    </div>
  );
};

export const ListSkeleton: React.FC<{
  items?: number;
  className?: string;
}> = ({
  items = 3,
  className
}) => {
  return (
    <div className={cn("space-y-3", className)}>
      {Array.from({ length: items }).map((_, i) => (
        <div key={i} className="flex items-center gap-3 p-4 rounded-lg border">
          <Skeleton variant="circular" width={40} height={40} />
          <div className="flex-1 space-y-2">
            <Skeleton width="70%" height={16} />
            <Skeleton width="40%" height={12} />
          </div>
        </div>
      ))}
    </div>
  );
};

export const ExerciseCardSkeleton: React.FC<{ className?: string }> = ({ className }) => {
  return (
    <div className={cn("rounded-lg border p-6 space-y-6", className)}>
      {/* Header */}
      <div className="flex items-center justify-between">
        <Skeleton width={120} height={16} />
        <Skeleton width={80} height={20} />
      </div>

      {/* Verb Info */}
      <div className="flex items-center gap-4">
        <Skeleton width={100} height={24} />
        <Skeleton width={80} height={20} />
      </div>

      {/* Sentence */}
      <div className="space-y-2">
        <Skeleton width="100%" height={16} />
        <Skeleton width="85%" height={16} />
      </div>

      {/* Input Area */}
      <div className="space-y-3">
        <Skeleton width="100%" height={48} />
        <div className="flex gap-2">
          <Skeleton width={100} height={40} />
          <Skeleton width={100} height={40} />
        </div>
      </div>
    </div>
  );
};

export const DashboardSkeleton: React.FC<{ className?: string }> = ({ className }) => {
  return (
    <div className={cn("space-y-6", className)}>
      {/* Header */}
      <div className="space-y-2">
        <Skeleton width={200} height={32} />
        <Skeleton width={300} height={16} />
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-3">
        {Array.from({ length: 3 }).map((_, i) => (
          <div key={i} className="rounded-lg border p-6 space-y-2">
            <Skeleton width={100} height={14} />
            <Skeleton width={60} height={28} />
            <Skeleton width={80} height={12} />
          </div>
        ))}
      </div>

      {/* Content Area */}
      <div className="grid gap-6 md:grid-cols-2">
        <CardSkeleton />
        <CardSkeleton />
      </div>
    </div>
  );
};

export const TableSkeleton: React.FC<{
  rows?: number;
  columns?: number;
  className?: string;
}> = ({
  rows = 5,
  columns = 4,
  className
}) => {
  return (
    <div className={cn("space-y-2", className)}>
      {/* Header */}
      <div className="flex gap-4 p-4 border-b">
        {Array.from({ length: columns }).map((_, i) => (
          <Skeleton key={i} width={`${100 / columns}%`} height={16} />
        ))}
      </div>

      {/* Rows */}
      {Array.from({ length: rows }).map((_, rowIndex) => (
        <div key={rowIndex} className="flex gap-4 p-4">
          {Array.from({ length: columns }).map((_, colIndex) => (
            <Skeleton key={colIndex} width={`${100 / columns}%`} height={14} />
          ))}
        </div>
      ))}
    </div>
  );
};

// ============================================================================
// Loading Spinner
// ============================================================================

export const LoadingSpinner: React.FC<{
  size?: "sm" | "md" | "lg";
  className?: string;
}> = ({
  size = "md",
  className
}) => {
  const sizeClasses = {
    sm: "h-4 w-4",
    md: "h-8 w-8",
    lg: "h-12 w-12",
  };

  return (
    <motion.div
      className={cn("border-2 border-gray-300 border-t-blue-600 rounded-full", sizeClasses[size], className)}
      animate={{ rotate: 360 }}
      transition={{
        duration: 1,
        repeat: Infinity,
        ease: "linear",
      }}
    />
  );
};

export const LoadingOverlay: React.FC<{
  message?: string;
  className?: string;
}> = ({ message, className }) => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className={cn(
        "fixed inset-0 z-50 flex items-center justify-center bg-background/80 backdrop-blur-sm",
        className
      )}
    >
      <div className="flex flex-col items-center gap-4">
        <LoadingSpinner size="lg" />
        {message && (
          <p className="text-sm text-muted-foreground">{message}</p>
        )}
      </div>
    </motion.div>
  );
};

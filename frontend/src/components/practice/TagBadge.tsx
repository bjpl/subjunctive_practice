"use client";

import * as React from "react";
import { cn } from "@/lib/utils";
import { Tag, X } from "lucide-react";
import { motion } from "framer-motion";

interface TagBadgeProps {
  tag: string;
  variant?: "default" | "outline" | "solid";
  size?: "sm" | "md" | "lg";
  removable?: boolean;
  onRemove?: () => void;
  className?: string;
}

const tagColorMap: Record<string, string> = {
  "trigger-phrases": "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300",
  "common-verbs": "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300",
  "beginner": "bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300",
  "intermediate": "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300",
  "advanced": "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300",
  "a1-level": "bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300",
  "a2-level": "bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300",
  "b1-level": "bg-indigo-100 text-indigo-800 dark:bg-indigo-900/30 dark:text-indigo-300",
  "b2-level": "bg-indigo-100 text-indigo-800 dark:bg-indigo-900/30 dark:text-indigo-300",
  "subjunctive-present": "bg-pink-100 text-pink-800 dark:bg-pink-900/30 dark:text-pink-300",
  "subjunctive-imperfect": "bg-pink-100 text-pink-800 dark:bg-pink-900/30 dark:text-pink-300",
  "irregular-verbs": "bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-300",
};

const sizeClasses = {
  sm: "px-2 py-0.5 text-xs",
  md: "px-2.5 py-1 text-sm",
  lg: "px-3 py-1.5 text-base",
};

export const TagBadge: React.FC<TagBadgeProps> = ({
  tag,
  variant = "default",
  size = "sm",
  removable = false,
  onRemove,
  className,
}) => {
  const colorClass = tagColorMap[tag.toLowerCase()] ||
    "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300";

  const baseClasses = cn(
    "inline-flex items-center gap-1 rounded-full font-medium transition-colors",
    sizeClasses[size],
    variant === "outline" && "border border-current",
    variant === "solid" && colorClass,
    variant === "default" && colorClass,
    removable && "pr-1",
    className
  );

  return (
    <motion.span
      initial={{ scale: 0, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      exit={{ scale: 0, opacity: 0 }}
      transition={{ type: "spring", stiffness: 500, damping: 30 }}
      className={baseClasses}
    >
      <Tag className="h-3 w-3" />
      <span>{tag}</span>
      {removable && onRemove && (
        <button
          onClick={(e) => {
            e.stopPropagation();
            onRemove();
          }}
          className="ml-0.5 rounded-full p-0.5 hover:bg-black/10 dark:hover:bg-white/10 transition-colors"
          aria-label={`Remove ${tag} tag`}
        >
          <X className="h-3 w-3" />
        </button>
      )}
    </motion.span>
  );
};

interface TagListProps {
  tags: string[];
  variant?: "default" | "outline" | "solid";
  size?: "sm" | "md" | "lg";
  removable?: boolean;
  onRemoveTag?: (tag: string) => void;
  maxDisplay?: number;
  className?: string;
}

export const TagList: React.FC<TagListProps> = ({
  tags,
  variant = "default",
  size = "sm",
  removable = false,
  onRemoveTag,
  maxDisplay,
  className,
}) => {
  const displayTags = maxDisplay ? tags.slice(0, maxDisplay) : tags;
  const remainingCount = maxDisplay && tags.length > maxDisplay ? tags.length - maxDisplay : 0;

  if (!tags || tags.length === 0) {
    return null;
  }

  return (
    <div className={cn("flex flex-wrap gap-1.5", className)}>
      {displayTags.map((tag, index) => (
        <TagBadge
          key={`${tag}-${index}`}
          tag={tag}
          variant={variant}
          size={size}
          removable={removable}
          onRemove={onRemoveTag ? () => onRemoveTag(tag) : undefined}
        />
      ))}
      {remainingCount > 0 && (
        <span className={cn(
          "inline-flex items-center rounded-full font-medium",
          sizeClasses[size],
          "bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-400"
        )}>
          +{remainingCount} more
        </span>
      )}
    </div>
  );
};

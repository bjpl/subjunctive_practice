"use client";

import * as React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "@/lib/utils";
import {
  cardVariants,
  successVariants,
  errorShakeVariants,
  fadeInVariants,
} from "@/lib/animations";
import { useSwipeNavigation } from "@/hooks/useSwipeGesture";
import { CheckCircle2, XCircle } from "lucide-react";
import { TagList } from "./TagBadge";

interface AnimatedExerciseCardProps {
  children: React.ReactNode;
  exerciseNumber: number;
  totalExercises: number;
  difficulty: "beginner" | "intermediate" | "advanced";
  type: string;
  verb: string;
  tense: string;
  tags?: string[];
  feedbackState?: "correct" | "incorrect" | null;
  onNext?: () => void;
  onPrevious?: () => void;
  className?: string;
}

const difficultyColors = {
  beginner: "bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-300",
  intermediate: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-300",
  advanced: "bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-300",
};

export const AnimatedExerciseCard: React.FC<AnimatedExerciseCardProps> = ({
  children,
  exerciseNumber,
  totalExercises,
  difficulty,
  type,
  verb,
  tense,
  tags = [],
  feedbackState,
  onNext,
  onPrevious,
  className,
}) => {
  const swipeRef = useSwipeNavigation({
    onNext,
    onPrevious,
    threshold: 100,
  });

  return (
    <motion.div
      ref={swipeRef as any}
      variants={cardVariants}
      initial="hidden"
      animate="visible"
      whileHover="hover"
      className={cn("relative", className)}
    >
      {/* Feedback Overlay */}
      <AnimatePresence>
        {feedbackState && (
          <motion.div
            variants={fadeInVariants}
            initial="hidden"
            animate="visible"
            exit="exit"
            className="absolute inset-0 z-10 flex items-center justify-center bg-white/90 dark:bg-gray-900/90 backdrop-blur-sm rounded-lg"
          >
            <motion.div
              variants={feedbackState === "correct" ? successVariants : errorShakeVariants}
              initial="initial"
              animate={feedbackState === "correct" ? "animate" : "shake"}
            >
              {feedbackState === "correct" ? (
                <CheckCircle2 className="h-24 w-24 text-green-500" />
              ) : (
                <XCircle className="h-24 w-24 text-red-500" />
              )}
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Card Content */}
      <div className="rounded-lg border bg-white dark:bg-gray-800 shadow-lg overflow-hidden">
        {/* Header */}
        <div className="border-b bg-gray-50 dark:bg-gray-900/50 px-6 py-4">
          <div className="flex items-center justify-between">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 }}
              className="flex items-center gap-3"
            >
              <span className="text-sm font-medium text-gray-600 dark:text-gray-400">
                Question {exerciseNumber} of {totalExercises}
              </span>
              <motion.span
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.2, type: "spring" }}
                className={cn(
                  "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium",
                  difficultyColors[difficulty]
                )}
              >
                {difficulty.charAt(0).toUpperCase() + difficulty.slice(1)}
              </motion.span>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.15 }}
              className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider"
            >
              {type.replace("-", " ")}
            </motion.div>
          </div>
        </div>

        {/* Verb Info */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="px-6 pt-6 pb-4 border-b"
        >
          <div className="flex items-center gap-4">
            <div className="flex-1">
              <div className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                {verb}
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                {tense}
              </div>
              {tags && tags.length > 0 && (
                <div className="mt-2">
                  <TagList tags={tags} size="sm" maxDisplay={5} />
                </div>
              )}
            </div>

            {/* Progress Indicator */}
            <div className="flex gap-1">
              {Array.from({ length: totalExercises }).map((_, i) => (
                <motion.div
                  key={i}
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.3 + i * 0.05 }}
                  className={cn(
                    "h-2 w-2 rounded-full",
                    i < exerciseNumber
                      ? "bg-blue-500"
                      : i === exerciseNumber - 1
                      ? "bg-blue-400"
                      : "bg-gray-300 dark:bg-gray-600"
                  )}
                />
              ))}
            </div>
          </div>
        </motion.div>

        {/* Content */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.25 }}
          className="p-6"
        >
          {children}
        </motion.div>

        {/* Swipe Indicator (Mobile) */}
        <div className="md:hidden px-6 pb-4">
          <div className="text-xs text-center text-gray-400">
            Swipe left or right to navigate
          </div>
        </div>
      </div>
    </motion.div>
  );
};

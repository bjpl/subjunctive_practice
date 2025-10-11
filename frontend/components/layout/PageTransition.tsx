"use client";

import * as React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { usePathname } from "next/navigation";
import { pageVariants, pageSlideVariants } from "@/lib/animations";

interface PageTransitionProps {
  children: React.ReactNode;
  variant?: "slide" | "fade";
  className?: string;
}

/**
 * Wrapper component for page transitions
 *
 * Use this component to wrap page content for smooth transitions
 */
export const PageTransition: React.FC<PageTransitionProps> = ({
  children,
  variant = "slide",
  className,
}) => {
  const pathname = usePathname();
  const variants = variant === "slide" ? pageSlideVariants : pageVariants;

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={pathname}
        variants={variants}
        initial="initial"
        animate="enter"
        exit="exit"
        className={className}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
};

/**
 * Stagger children animation wrapper
 */
export const StaggerContainer: React.FC<{
  children: React.ReactNode;
  className?: string;
  staggerDelay?: number;
}> = ({ children, className, staggerDelay = 0.1 }) => {
  return (
    <motion.div
      className={className}
      initial="hidden"
      animate="visible"
      variants={{
        visible: {
          transition: {
            staggerChildren: staggerDelay,
          },
        },
      }}
    >
      {children}
    </motion.div>
  );
};

/**
 * Individual stagger item
 */
export const StaggerItem: React.FC<{
  children: React.ReactNode;
  className?: string;
}> = ({ children, className }) => {
  return (
    <motion.div
      className={className}
      variants={{
        hidden: { opacity: 0, y: 20 },
        visible: { opacity: 1, y: 0 },
      }}
    >
      {children}
    </motion.div>
  );
};

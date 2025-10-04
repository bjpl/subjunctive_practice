"use client";

import * as React from "react";
import * as Tooltip from "@radix-ui/react-tooltip";
import { motion } from "framer-motion";
import { HelpCircle, Info } from "lucide-react";
import { cn } from "@/lib/utils";
import { fadeInVariants } from "@/lib/animations";

interface HelpTooltipProps {
  content: React.ReactNode;
  children?: React.ReactNode;
  side?: "top" | "right" | "bottom" | "left";
  align?: "start" | "center" | "end";
  delayDuration?: number;
  icon?: "help" | "info" | "none";
  className?: string;
}

export const HelpTooltip: React.FC<HelpTooltipProps> = ({
  content,
  children,
  side = "top",
  align = "center",
  delayDuration = 200,
  icon = "help",
  className,
}) => {
  const IconComponent = icon === "help" ? HelpCircle : icon === "info" ? Info : null;

  return (
    <Tooltip.Provider delayDuration={delayDuration}>
      <Tooltip.Root>
        <Tooltip.Trigger asChild>
          {children || (
            <button
              className={cn(
                "inline-flex items-center justify-center",
                "text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200",
                "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 rounded-full",
                "transition-colors",
                className
              )}
              aria-label="Help"
            >
              {IconComponent && <IconComponent className="h-4 w-4" />}
            </button>
          )}
        </Tooltip.Trigger>

        <Tooltip.Portal>
          <Tooltip.Content
            side={side}
            align={align}
            sideOffset={5}
            asChild
          >
            <motion.div
              variants={fadeInVariants}
              initial="hidden"
              animate="visible"
              exit="exit"
              className={cn(
                "z-50 max-w-xs rounded-md border bg-white dark:bg-gray-800 px-3 py-2 shadow-md",
                "text-sm text-gray-700 dark:text-gray-200"
              )}
            >
              {content}
              <Tooltip.Arrow className="fill-white dark:fill-gray-800" />
            </motion.div>
          </Tooltip.Content>
        </Tooltip.Portal>
      </Tooltip.Root>
    </Tooltip.Provider>
  );
};

// ============================================================================
// Keyboard Shortcut Tooltip
// ============================================================================

interface KeyboardShortcutTooltipProps {
  label: string;
  shortcut: string | string[];
  children: React.ReactNode;
  side?: "top" | "right" | "bottom" | "left";
}

export const KeyboardShortcutTooltip: React.FC<KeyboardShortcutTooltipProps> = ({
  label,
  shortcut,
  children,
  side = "bottom",
}) => {
  const shortcuts = Array.isArray(shortcut) ? shortcut : [shortcut];

  return (
    <Tooltip.Provider delayDuration={300}>
      <Tooltip.Root>
        <Tooltip.Trigger asChild>{children}</Tooltip.Trigger>

        <Tooltip.Portal>
          <Tooltip.Content side={side} sideOffset={5} asChild>
            <motion.div
              variants={fadeInVariants}
              initial="hidden"
              animate="visible"
              exit="exit"
              className="z-50 rounded-md border bg-gray-900 dark:bg-gray-950 px-3 py-2 shadow-md"
            >
              <div className="flex items-center gap-2">
                <span className="text-sm text-gray-100">{label}</span>
                <div className="flex items-center gap-1">
                  {shortcuts.map((key, index) => (
                    <React.Fragment key={key}>
                      {index > 0 && (
                        <span className="text-xs text-gray-400">+</span>
                      )}
                      <kbd className="inline-flex items-center justify-center px-2 py-1 text-xs font-mono font-semibold text-gray-900 bg-gray-100 border border-gray-300 rounded">
                        {key}
                      </kbd>
                    </React.Fragment>
                  ))}
                </div>
              </div>
              <Tooltip.Arrow className="fill-gray-900 dark:fill-gray-950" />
            </motion.div>
          </Tooltip.Content>
        </Tooltip.Portal>
      </Tooltip.Root>
    </Tooltip.Provider>
  );
};

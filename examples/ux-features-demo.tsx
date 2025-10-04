"use client";

/**
 * UX Features Demonstration
 *
 * This file demonstrates all the UX enhancement features
 * implemented in the application.
 */

import { useState } from "react";
import { motion } from "framer-motion";
import { useEnhancedToast } from "@/hooks/useEnhancedToast";
import { useKeyboardShortcuts, commonShortcuts } from "@/hooks/useKeyboardShortcuts";
import { useSwipeNavigation } from "@/hooks/useSwipeGesture";
import { useConfirmModal } from "@/components/feedback/ConfirmModal";
import { AnimatedExerciseCard } from "@/components/practice/AnimatedExerciseCard";
import { HelpTooltip, KeyboardShortcutTooltip } from "@/components/feedback/HelpTooltip";
import { ErrorBoundary, CompactErrorFallback } from "@/components/layout/ErrorBoundary";
import {
  Skeleton,
  CardSkeleton,
  ListSkeleton,
  LoadingSpinner,
  LoadingOverlay,
} from "@/components/layout/LoadingSkeleton";
import {
  PageTransition,
  StaggerContainer,
  StaggerItem,
} from "@/components/layout/PageTransition";
import { fadeInVariants, buttonHoverVariants } from "@/lib/animations";

// ============================================================================
// 1. TOAST NOTIFICATIONS DEMO
// ============================================================================

function ToastDemo() {
  const { success, error, warning, info, promise } = useEnhancedToast();

  const simulateAsyncOperation = () => {
    return new Promise<string>((resolve, reject) => {
      setTimeout(() => {
        Math.random() > 0.5
          ? resolve("Operation successful!")
          : reject(new Error("Operation failed!"));
      }, 2000);
    });
  };

  return (
    <div className="space-y-4 p-6 border rounded-lg">
      <h3 className="text-lg font-semibold">Toast Notifications</h3>

      <div className="grid grid-cols-2 gap-2">
        <button
          onClick={() => success("Success!", "Operation completed successfully")}
          className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
        >
          Success Toast
        </button>

        <button
          onClick={() => error("Error!", "Something went wrong")}
          className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
        >
          Error Toast
        </button>

        <button
          onClick={() => warning("Warning!", "Please review your input")}
          className="px-4 py-2 bg-yellow-600 text-white rounded hover:bg-yellow-700"
        >
          Warning Toast
        </button>

        <button
          onClick={() => info("Info", "Here's some helpful information")}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Info Toast
        </button>

        <button
          onClick={() =>
            promise(simulateAsyncOperation(), {
              loading: "Processing...",
              success: (data) => data,
              error: (err) => err.message,
            })
          }
          className="col-span-2 px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700"
        >
          Promise Toast (Random Success/Error)
        </button>
      </div>
    </div>
  );
}

// ============================================================================
// 2. LOADING STATES DEMO
// ============================================================================

function LoadingStatesDemo() {
  const [loading, setLoading] = useState(false);

  return (
    <div className="space-y-4 p-6 border rounded-lg">
      <h3 className="text-lg font-semibold">Loading States</h3>

      <div className="space-y-4">
        <div>
          <h4 className="text-sm font-medium mb-2">Skeletons:</h4>
          <div className="space-y-2">
            <Skeleton width="100%" height={16} />
            <Skeleton width="80%" height={16} />
            <Skeleton width="60%" height={16} />
          </div>
        </div>

        <div>
          <h4 className="text-sm font-medium mb-2">Card Skeleton:</h4>
          <CardSkeleton />
        </div>

        <div>
          <h4 className="text-sm font-medium mb-2">List Skeleton:</h4>
          <ListSkeleton items={3} />
        </div>

        <div className="flex items-center gap-4">
          <LoadingSpinner size="sm" />
          <LoadingSpinner size="md" />
          <LoadingSpinner size="lg" />
        </div>

        <button
          onClick={() => setLoading(!loading)}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Toggle Loading Overlay
        </button>

        {loading && <LoadingOverlay message="Loading..." />}
      </div>
    </div>
  );
}

// ============================================================================
// 3. CONFIRMATION MODAL DEMO
// ============================================================================

function ConfirmModalDemo() {
  const { confirm, ConfirmModal } = useConfirmModal();
  const { success, error } = useEnhancedToast();

  const handleDangerousAction = async () => {
    const confirmed = await confirm({
      title: "Delete Exercise?",
      description: "This action cannot be undone. Are you sure?",
      variant: "danger",
      confirmLabel: "Delete",
      cancelLabel: "Cancel",
    });

    if (confirmed) {
      success("Deleted!", "Exercise was deleted successfully");
    }
  };

  const handleWarningAction = async () => {
    const confirmed = await confirm({
      title: "Reset Progress?",
      description: "This will reset all your progress. Continue?",
      variant: "warning",
      confirmLabel: "Reset",
    });

    if (confirmed) {
      success("Reset!", "Progress has been reset");
    }
  };

  return (
    <div className="space-y-4 p-6 border rounded-lg">
      <h3 className="text-lg font-semibold">Confirmation Modals</h3>

      <div className="flex gap-2">
        <button
          onClick={handleDangerousAction}
          className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
        >
          Danger Confirm
        </button>

        <button
          onClick={handleWarningAction}
          className="px-4 py-2 bg-yellow-600 text-white rounded hover:bg-yellow-700"
        >
          Warning Confirm
        </button>
      </div>

      <ConfirmModal />
    </div>
  );
}

// ============================================================================
// 4. KEYBOARD SHORTCUTS DEMO
// ============================================================================

function KeyboardShortcutsDemo() {
  const { success } = useEnhancedToast();
  const [lastAction, setLastAction] = useState<string>("");

  useKeyboardShortcuts([
    commonShortcuts.save(() => {
      setLastAction("Saved (Ctrl+S)");
      success("Saved!", "Document saved successfully");
    }),
    commonShortcuts.submit(() => {
      setLastAction("Submitted (Ctrl+Enter)");
      success("Submitted!", "Answer submitted");
    }),
    {
      key: "h",
      callback: () => {
        setLastAction("Help (H)");
        success("Help", "Showing help dialog");
      },
      description: "Show help",
    },
    {
      key: "n",
      ctrl: true,
      callback: () => {
        setLastAction("Next (Ctrl+N)");
        success("Next", "Moving to next exercise");
      },
      description: "Next exercise",
    },
  ]);

  return (
    <div className="space-y-4 p-6 border rounded-lg">
      <h3 className="text-lg font-semibold">Keyboard Shortcuts</h3>

      <div className="space-y-2">
        <p className="text-sm text-gray-600">Try these shortcuts:</p>
        <ul className="text-sm space-y-1">
          <li>
            <kbd className="px-2 py-1 bg-gray-100 rounded text-xs">Ctrl+S</kbd> - Save
          </li>
          <li>
            <kbd className="px-2 py-1 bg-gray-100 rounded text-xs">Ctrl+Enter</kbd> - Submit
          </li>
          <li>
            <kbd className="px-2 py-1 bg-gray-100 rounded text-xs">H</kbd> - Help
          </li>
          <li>
            <kbd className="px-2 py-1 bg-gray-100 rounded text-xs">Ctrl+N</kbd> - Next
          </li>
        </ul>

        {lastAction && (
          <div className="mt-4 p-3 bg-blue-50 rounded">
            <p className="text-sm font-medium">Last action: {lastAction}</p>
          </div>
        )}

        <KeyboardShortcutTooltip label="Submit answer" shortcut={["Ctrl", "Enter"]}>
          <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
            Hover for shortcut hint
          </button>
        </KeyboardShortcutTooltip>
      </div>
    </div>
  );
}

// ============================================================================
// 5. SWIPE GESTURES DEMO
// ============================================================================

function SwipeGesturesDemo() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"];

  const swipeRef = useSwipeNavigation({
    onNext: () => setCurrentIndex((i) => Math.min(i + 1, items.length - 1)),
    onPrevious: () => setCurrentIndex((i) => Math.max(i - 1, 0)),
    threshold: 50,
  });

  return (
    <div className="space-y-4 p-6 border rounded-lg">
      <h3 className="text-lg font-semibold">Swipe Gestures (Mobile)</h3>

      <div
        ref={swipeRef as any}
        className="p-8 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-lg text-center touch-pan-y"
      >
        <p className="text-2xl font-bold">{items[currentIndex]}</p>
        <p className="text-sm mt-2 opacity-80">Swipe left or right</p>
      </div>

      <div className="flex justify-center gap-2">
        {items.map((_, index) => (
          <div
            key={index}
            className={`h-2 w-2 rounded-full ${
              index === currentIndex ? "bg-blue-600" : "bg-gray-300"
            }`}
          />
        ))}
      </div>
    </div>
  );
}

// ============================================================================
// 6. HELP TOOLTIPS DEMO
// ============================================================================

function HelpTooltipsDemo() {
  return (
    <div className="space-y-4 p-6 border rounded-lg">
      <h3 className="text-lg font-semibold">Help Tooltips</h3>

      <div className="flex flex-wrap gap-4">
        <HelpTooltip content="This is helpful information about this feature">
          <button className="px-4 py-2 border rounded hover:bg-gray-50">
            Hover me (default)
          </button>
        </HelpTooltip>

        <HelpTooltip content="Top tooltip" side="top">
          <button className="px-4 py-2 border rounded hover:bg-gray-50">Top</button>
        </HelpTooltip>

        <HelpTooltip content="Right tooltip" side="right">
          <button className="px-4 py-2 border rounded hover:bg-gray-50">Right</button>
        </HelpTooltip>

        <HelpTooltip content="Bottom tooltip" side="bottom">
          <button className="px-4 py-2 border rounded hover:bg-gray-50">Bottom</button>
        </HelpTooltip>

        <HelpTooltip content="Left tooltip" side="left">
          <button className="px-4 py-2 border rounded hover:bg-gray-50">Left</button>
        </HelpTooltip>

        <div className="flex items-center gap-2">
          <span className="text-sm">Conjugate the verb</span>
          <HelpTooltip content="Use the present subjunctive form of the verb" icon="help" />
        </div>
      </div>
    </div>
  );
}

// ============================================================================
// 7. ANIMATED EXERCISE CARD DEMO
// ============================================================================

function AnimatedExerciseCardDemo() {
  const [exerciseNumber, setExerciseNumber] = useState(1);
  const [feedbackState, setFeedbackState] = useState<"correct" | "incorrect" | null>(null);
  const [answer, setAnswer] = useState("");

  const handleSubmit = () => {
    const isCorrect = answer.toLowerCase() === "hables";
    setFeedbackState(isCorrect ? "correct" : "incorrect");

    setTimeout(() => {
      if (isCorrect) {
        setExerciseNumber((n) => n + 1);
        setAnswer("");
      }
      setFeedbackState(null);
    }, 1500);
  };

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold">Animated Exercise Card</h3>

      <AnimatedExerciseCard
        exerciseNumber={exerciseNumber}
        totalExercises={5}
        difficulty="intermediate"
        type="present-subjunctive"
        verb="hablar"
        tense="Present Subjunctive"
        feedbackState={feedbackState}
        onNext={() => setExerciseNumber((n) => Math.min(n + 1, 5))}
        onPrevious={() => setExerciseNumber((n) => Math.max(n - 1, 1))}
      >
        <div className="space-y-4">
          <p className="text-lg">
            Complete the sentence: Espero que tú <strong>_____</strong> español.
          </p>

          <input
            type="text"
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            className="w-full px-4 py-2 border rounded focus:ring-2 focus:ring-blue-500"
            placeholder="Type your answer..."
            onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
          />

          <button
            onClick={handleSubmit}
            className="w-full px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Submit
          </button>

          <p className="text-xs text-gray-500 text-center">
            Hint: Answer is "hables"
          </p>
        </div>
      </AnimatedExerciseCard>
    </div>
  );
}

// ============================================================================
// 8. ERROR BOUNDARY DEMO
// ============================================================================

function BuggyComponent({ shouldError }: { shouldError: boolean }) {
  if (shouldError) {
    throw new Error("This is a test error!");
  }
  return <div className="p-4 bg-green-50 rounded">Component works fine!</div>;
}

function ErrorBoundaryDemo() {
  const [shouldError, setShouldError] = useState(false);

  return (
    <div className="space-y-4 p-6 border rounded-lg">
      <h3 className="text-lg font-semibold">Error Boundary</h3>

      <button
        onClick={() => setShouldError(!shouldError)}
        className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
      >
        {shouldError ? "Fix Error" : "Trigger Error"}
      </button>

      <ErrorBoundary fallback={CompactErrorFallback} onReset={() => setShouldError(false)}>
        <BuggyComponent shouldError={shouldError} />
      </ErrorBoundary>
    </div>
  );
}

// ============================================================================
// MAIN DEMO PAGE
// ============================================================================

export default function UXFeaturesDemo() {
  return (
    <PageTransition>
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-6xl mx-auto px-4">
          <motion.div variants={fadeInVariants} initial="hidden" animate="visible">
            <h1 className="text-4xl font-bold text-center mb-2">
              UX Features Demo
            </h1>
            <p className="text-center text-gray-600 mb-12">
              Interactive demonstration of all UX enhancements
            </p>
          </motion.div>

          <StaggerContainer className="space-y-6">
            <StaggerItem>
              <ToastDemo />
            </StaggerItem>

            <StaggerItem>
              <LoadingStatesDemo />
            </StaggerItem>

            <StaggerItem>
              <ConfirmModalDemo />
            </StaggerItem>

            <StaggerItem>
              <KeyboardShortcutsDemo />
            </StaggerItem>

            <StaggerItem>
              <SwipeGesturesDemo />
            </StaggerItem>

            <StaggerItem>
              <HelpTooltipsDemo />
            </StaggerItem>

            <StaggerItem>
              <AnimatedExerciseCardDemo />
            </StaggerItem>

            <StaggerItem>
              <ErrorBoundaryDemo />
            </StaggerItem>
          </StaggerContainer>
        </div>
      </div>
    </PageTransition>
  );
}

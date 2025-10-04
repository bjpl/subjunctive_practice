"use client";

import { useEffect, useRef, RefObject } from "react";

export type SwipeDirection = "left" | "right" | "up" | "down";

export interface SwipeConfig {
  onSwipe?: (direction: SwipeDirection) => void;
  onSwipeLeft?: () => void;
  onSwipeRight?: () => void;
  onSwipeUp?: () => void;
  onSwipeDown?: () => void;
  threshold?: number; // minimum distance in pixels
  preventDefaultTouchmoveEvent?: boolean;
}

interface TouchPosition {
  x: number;
  y: number;
}

/**
 * Hook for detecting swipe gestures on mobile devices
 *
 * @example
 * const ref = useSwipeGesture({
 *   onSwipeLeft: () => console.log('Swiped left'),
 *   onSwipeRight: () => console.log('Swiped right'),
 *   threshold: 50
 * });
 *
 * return <div ref={ref}>Swipe me!</div>
 */
export function useSwipeGesture<T extends HTMLElement = HTMLDivElement>(
  config: SwipeConfig
): RefObject<T> {
  const {
    onSwipe,
    onSwipeLeft,
    onSwipeRight,
    onSwipeUp,
    onSwipeDown,
    threshold = 50,
    preventDefaultTouchmoveEvent = false,
  } = config;

  const elementRef = useRef<T>(null);
  const touchStart = useRef<TouchPosition | null>(null);
  const touchEnd = useRef<TouchPosition | null>(null);

  useEffect(() => {
    const element = elementRef.current;
    if (!element) return;

    const handleTouchStart = (e: TouchEvent) => {
      touchEnd.current = null;
      touchStart.current = {
        x: e.targetTouches[0].clientX,
        y: e.targetTouches[0].clientY,
      };
    };

    const handleTouchMove = (e: TouchEvent) => {
      touchEnd.current = {
        x: e.targetTouches[0].clientX,
        y: e.targetTouches[0].clientY,
      };

      if (preventDefaultTouchmoveEvent) {
        e.preventDefault();
      }
    };

    const handleTouchEnd = () => {
      if (!touchStart.current || !touchEnd.current) return;

      const deltaX = touchStart.current.x - touchEnd.current.x;
      const deltaY = touchStart.current.y - touchEnd.current.y;

      const absX = Math.abs(deltaX);
      const absY = Math.abs(deltaY);

      // Determine if the swipe was primarily horizontal or vertical
      if (Math.max(absX, absY) < threshold) return;

      let direction: SwipeDirection;

      if (absX > absY) {
        // Horizontal swipe
        direction = deltaX > 0 ? "left" : "right";
      } else {
        // Vertical swipe
        direction = deltaY > 0 ? "up" : "down";
      }

      // Call the appropriate callbacks
      onSwipe?.(direction);

      switch (direction) {
        case "left":
          onSwipeLeft?.();
          break;
        case "right":
          onSwipeRight?.();
          break;
        case "up":
          onSwipeUp?.();
          break;
        case "down":
          onSwipeDown?.();
          break;
      }

      // Reset
      touchStart.current = null;
      touchEnd.current = null;
    };

    element.addEventListener("touchstart", handleTouchStart);
    element.addEventListener("touchmove", handleTouchMove);
    element.addEventListener("touchend", handleTouchEnd);

    return () => {
      element.removeEventListener("touchstart", handleTouchStart);
      element.removeEventListener("touchmove", handleTouchMove);
      element.removeEventListener("touchend", handleTouchEnd);
    };
  }, [
    onSwipe,
    onSwipeLeft,
    onSwipeRight,
    onSwipeUp,
    onSwipeDown,
    threshold,
    preventDefaultTouchmoveEvent,
  ]);

  return elementRef;
}

/**
 * Hook for swipeable card/carousel navigation
 */
export function useSwipeNavigation(options: {
  onNext?: () => void;
  onPrevious?: () => void;
  threshold?: number;
}) {
  const { onNext, onPrevious, threshold = 75 } = options;

  return useSwipeGesture({
    onSwipeLeft: onNext,
    onSwipeRight: onPrevious,
    threshold,
    preventDefaultTouchmoveEvent: false,
  });
}

/**
 * Hook for swipe-to-dismiss functionality
 */
export function useSwipeToDismiss(options: {
  onDismiss: () => void;
  direction?: "left" | "right" | "up" | "down";
  threshold?: number;
}) {
  const { onDismiss, direction = "right", threshold = 100 } = options;

  const callbacks: SwipeConfig = {
    threshold,
  };

  switch (direction) {
    case "left":
      callbacks.onSwipeLeft = onDismiss;
      break;
    case "right":
      callbacks.onSwipeRight = onDismiss;
      break;
    case "up":
      callbacks.onSwipeUp = onDismiss;
      break;
    case "down":
      callbacks.onSwipeDown = onDismiss;
      break;
  }

  return useSwipeGesture(callbacks);
}

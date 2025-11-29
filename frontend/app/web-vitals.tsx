'use client';

import { useEffect } from 'react';
import { useReportWebVitals } from 'next/web-vitals';
import { reportMetric } from '../lib/performance';

/**
 * Web Vitals Reporter Component
 * Uses Next.js built-in useReportWebVitals hook
 */
export function WebVitalsReporter() {
  useReportWebVitals(reportMetric);
  return null;
}

/**
 * Alternative implementation using direct web-vitals integration
 * Use this if you want more control or custom behavior
 */
export function DirectWebVitalsReporter() {
  useEffect(() => {
    // Dynamic import to avoid loading in SSR
    import('../lib/performance').then(({ initWebVitals }) => {
      initWebVitals();
    });
  }, []);

  return null;
}

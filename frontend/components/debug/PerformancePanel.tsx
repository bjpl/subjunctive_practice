'use client';

import { useEffect, useState } from 'react';
import { onCLS, onFCP, onLCP, onTTFB, onINP, Metric } from 'web-vitals';
import { formatMetricValue, getRatingLabel } from '../../lib/performance';

interface MetricData {
  name: string;
  value: number;
  rating: string;
  formattedValue: string;
  ratingLabel: string;
  timestamp: number;
}

/**
 * Performance Panel - Debug component for development
 * Shows real-time Web Vitals metrics in development mode
 */
export function PerformancePanel() {
  const [metrics, setMetrics] = useState<Map<string, MetricData>>(new Map());
  const [isVisible, setIsVisible] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);

  useEffect(() => {
    // Only show in development
    if (process.env.NODE_ENV !== 'development') return;

    const handleMetric = (metric: Metric) => {
      const ratingLabel = getRatingLabel(metric.name, metric.value);

      setMetrics((prev) => {
        const updated = new Map(prev);
        updated.set(metric.name, {
          name: metric.name,
          value: metric.value,
          rating: metric.rating,
          formattedValue: formatMetricValue(metric.name, metric.value),
          ratingLabel,
          timestamp: Date.now(),
        });
        return updated;
      });
    };

    // Subscribe to all Web Vitals (FID deprecated, replaced by INP)
    onCLS(handleMetric);
    onFCP(handleMetric);
    onLCP(handleMetric);
    onTTFB(handleMetric);
    onINP(handleMetric);

    setIsVisible(true);
  }, []);

  // Don't render in production
  if (process.env.NODE_ENV !== 'development' || !isVisible) {
    return null;
  }

  const getRatingColor = (rating: string) => {
    switch (rating) {
      case 'good':
        return 'bg-green-500';
      case 'needs-improvement':
        return 'bg-yellow-500';
      case 'poor':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  };

  const metricsArray = Array.from(metrics.values()).sort((a, b) =>
    a.name.localeCompare(b.name)
  );

  return (
    <div className="fixed bottom-4 right-4 z-50 font-mono text-xs">
      <div className="bg-gray-900 text-white rounded-lg shadow-2xl border border-gray-700 overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between px-3 py-2 bg-gray-800 border-b border-gray-700">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse"></div>
            <span className="font-semibold">Web Vitals</span>
          </div>
          <div className="flex gap-1">
            <button
              onClick={() => setIsMinimized(!isMinimized)}
              className="px-2 py-1 hover:bg-gray-700 rounded transition-colors"
              title={isMinimized ? 'Expand' : 'Minimize'}
            >
              {isMinimized ? '□' : '_'}
            </button>
            <button
              onClick={() => setIsVisible(false)}
              className="px-2 py-1 hover:bg-gray-700 rounded transition-colors"
              title="Close"
            >
              ×
            </button>
          </div>
        </div>

        {/* Content */}
        {!isMinimized && (
          <div className="p-3 space-y-2 min-w-[280px]">
            {metricsArray.length === 0 ? (
              <div className="text-gray-400 text-center py-4">
                Waiting for metrics...
              </div>
            ) : (
              metricsArray.map((metric) => (
                <div
                  key={metric.name}
                  className="flex items-center justify-between gap-3 p-2 bg-gray-800 rounded"
                >
                  <div className="flex items-center gap-2">
                    <div
                      className={`w-2 h-2 rounded-full ${getRatingColor(metric.ratingLabel)}`}
                      title={metric.ratingLabel}
                    ></div>
                    <span className="font-semibold">{metric.name}</span>
                  </div>
                  <div className="text-right">
                    <div className="font-bold">{metric.formattedValue}</div>
                    <div className="text-gray-400 text-[10px]">
                      {metric.ratingLabel}
                    </div>
                  </div>
                </div>
              ))
            )}

            {/* Legend */}
            <div className="pt-2 mt-2 border-t border-gray-700">
              <div className="text-gray-400 text-[10px] space-y-1">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-green-500"></div>
                  <span>Good</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-yellow-500"></div>
                  <span>Needs Improvement</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-red-500"></div>
                  <span>Poor</span>
                </div>
              </div>
            </div>

            {/* Info */}
            <div className="pt-2 mt-2 border-t border-gray-700 text-gray-400 text-[10px]">
              <div>CLS: Cumulative Layout Shift</div>
              <div>FCP: First Contentful Paint</div>
              <div>LCP: Largest Contentful Paint</div>
              <div>TTFB: Time to First Byte</div>
              <div>INP: Interaction to Next Paint</div>
            </div>
          </div>
        )}
      </div>

      {/* Reopen button when closed */}
      {!isVisible && (
        <button
          onClick={() => setIsVisible(true)}
          className="mt-2 px-3 py-2 bg-gray-900 text-white rounded-lg shadow-lg border border-gray-700 hover:bg-gray-800 transition-colors"
        >
          📊 Web Vitals
        </button>
      )}
    </div>
  );
}

export default PerformancePanel;

"use client";

import { useMemo } from "react";
import { PracticeSession, ExerciseAttempt } from "@/types";
import { PerformanceChart } from "@/components/dashboard/PerformanceChart";
import { calculatePerformanceTrends } from "@/lib/analytics";

interface ProgressChartsProps {
  sessions: PracticeSession[];
  attempts?: ExerciseAttempt[];
  period?: number; // days
  chartType?: "line" | "bar" | "area";
}

export function ProgressCharts({
  sessions,
  attempts = [],
  period = 30,
  chartType = "line",
}: ProgressChartsProps) {
  const performanceTrends = useMemo(() => {
    return calculatePerformanceTrends(sessions, period);
  }, [sessions, period]);

  return (
    <div className="space-y-6">
      <PerformanceChart data={performanceTrends} chartType={chartType} metric="all" />
    </div>
  );
}

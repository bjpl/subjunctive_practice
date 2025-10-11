"use client";

import { useMemo } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { DailyActivity } from "@/lib/analytics";
import { format, startOfWeek, endOfWeek, eachDayOfInterval, startOfMonth, endOfMonth } from "date-fns";
import { Calendar, Flame, TrendingUp } from "lucide-react";

interface StudyHeatmapProps {
  data: DailyActivity[];
  period?: "week" | "month" | "quarter";
}

export function StudyHeatmap({ data, period = "quarter" }: StudyHeatmapProps) {
  const heatmapData = useMemo(() => {
    // Create a map for quick lookup
    const dataMap = new Map(data.map((d) => [d.date, d]));

    // Get the date range
    const endDate = new Date();
    const startDate = new Date();
    if (period === "week") {
      startDate.setDate(endDate.getDate() - 7);
    } else if (period === "month") {
      startDate.setDate(endDate.getDate() - 30);
    } else {
      startDate.setDate(endDate.getDate() - 90);
    }

    const days = eachDayOfInterval({ start: startDate, end: endDate });

    return days.map((day) => {
      const dateKey = format(day, "yyyy-MM-dd");
      const activity = dataMap.get(dateKey) || { date: dateKey, count: 0, accuracy: 0 };
      return {
        ...activity,
        dayOfWeek: day.getDay(),
        weekNumber: Math.floor((day.getTime() - startDate.getTime()) / (7 * 24 * 60 * 60 * 1000)),
        displayDate: format(day, "MMM d"),
        dayName: format(day, "EEE"),
      };
    });
  }, [data, period]);

  const weeks = useMemo(() => {
    const weekCount = Math.max(...heatmapData.map((d) => d.weekNumber)) + 1;
    return Array.from({ length: weekCount }, (_, i) => i);
  }, [heatmapData]);

  const getIntensityColor = (count: number) => {
    if (count === 0) return "bg-gray-100 dark:bg-gray-800";
    if (count === 1) return "bg-green-200 dark:bg-green-900";
    if (count === 2) return "bg-green-300 dark:bg-green-700";
    if (count === 3) return "bg-green-400 dark:bg-green-600";
    return "bg-green-500 dark:bg-green-500";
  };

  const getTooltipText = (activity: any) => {
    if (activity.count === 0) {
      return `${activity.displayDate}: No activity`;
    }
    return `${activity.displayDate}: ${activity.count} session${activity.count > 1 ? "s" : ""}, ${activity.accuracy}% accuracy`;
  };

  const stats = useMemo(() => {
    const activeDays = heatmapData.filter((d) => d.count > 0).length;
    const totalSessions = heatmapData.reduce((sum, d) => sum + d.count, 0);
    const avgAccuracy = heatmapData.filter((d) => d.count > 0).length > 0
      ? Math.round(
          heatmapData.filter((d) => d.count > 0).reduce((sum, d) => sum + d.accuracy, 0) /
            heatmapData.filter((d) => d.count > 0).length
        )
      : 0;
    const currentStreak = calculateCurrentStreak(heatmapData);

    return { activeDays, totalSessions, avgAccuracy, currentStreak };
  }, [heatmapData]);

  function calculateCurrentStreak(activities: any[]): number {
    let streak = 0;
    const reversedData = [...activities].reverse();

    for (const activity of reversedData) {
      if (activity.count > 0) {
        streak++;
      } else if (streak > 0) {
        break;
      }
    }
    return streak;
  }

  const dayLabels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Calendar className="h-5 w-5" />
          Study Activity Heatmap
        </CardTitle>
        <CardDescription>
          Your practice activity over the last {period === "week" ? "7 days" : period === "month" ? "30 days" : "90 days"}
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Stats Summary */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center p-3 rounded-lg bg-muted/50">
            <p className="text-2xl font-bold text-green-600">{stats.activeDays}</p>
            <p className="text-xs text-muted-foreground">Active Days</p>
          </div>
          <div className="text-center p-3 rounded-lg bg-muted/50">
            <p className="text-2xl font-bold text-blue-600">{stats.totalSessions}</p>
            <p className="text-xs text-muted-foreground">Total Sessions</p>
          </div>
          <div className="text-center p-3 rounded-lg bg-muted/50">
            <p className="text-2xl font-bold text-purple-600">{stats.avgAccuracy}%</p>
            <p className="text-xs text-muted-foreground">Avg Accuracy</p>
          </div>
          <div className="text-center p-3 rounded-lg bg-muted/50">
            <p className="text-2xl font-bold text-orange-600">{stats.currentStreak}</p>
            <p className="text-xs text-muted-foreground">Current Streak</p>
          </div>
        </div>

        {/* Heatmap */}
        <div className="overflow-x-auto">
          <div className="inline-block min-w-full">
            <div className="flex gap-1">
              {/* Day labels */}
              <div className="flex flex-col gap-1 pr-2">
                <div className="h-4"></div> {/* Spacer for month labels */}
                {dayLabels.map((day) => (
                  <div key={day} className="h-3 flex items-center">
                    <span className="text-[10px] text-muted-foreground">{day[0]}</span>
                  </div>
                ))}
              </div>

              {/* Heatmap grid */}
              {weeks.map((weekNum) => (
                <div key={weekNum} className="flex flex-col gap-1">
                  {/* Month label (only show on first day of month) */}
                  <div className="h-4 text-[10px] text-muted-foreground">
                    {heatmapData.find((d) => d.weekNumber === weekNum && d.dayOfWeek === 0)?.displayDate.split(" ")[0]}
                  </div>
                  {[0, 1, 2, 3, 4, 5, 6].map((dayOfWeek) => {
                    const activity = heatmapData.find(
                      (d) => d.weekNumber === weekNum && d.dayOfWeek === dayOfWeek
                    );
                    if (!activity) {
                      return <div key={dayOfWeek} className="h-3 w-3" />;
                    }
                    return (
                      <div
                        key={`${weekNum}-${dayOfWeek}`}
                        className={`h-3 w-3 rounded-sm ${getIntensityColor(
                          activity.count
                        )} hover:ring-2 hover:ring-gray-400 cursor-pointer transition-all`}
                        title={getTooltipText(activity)}
                      />
                    );
                  })}
                </div>
              ))}
            </div>

            {/* Legend */}
            <div className="flex items-center gap-2 mt-4 text-xs text-muted-foreground">
              <span>Less</span>
              <div className="flex gap-1">
                <div className="h-3 w-3 rounded-sm bg-gray-100 dark:bg-gray-800" />
                <div className="h-3 w-3 rounded-sm bg-green-200 dark:bg-green-900" />
                <div className="h-3 w-3 rounded-sm bg-green-300 dark:bg-green-700" />
                <div className="h-3 w-3 rounded-sm bg-green-400 dark:bg-green-600" />
                <div className="h-3 w-3 rounded-sm bg-green-500 dark:bg-green-500" />
              </div>
              <span>More</span>
            </div>
          </div>
        </div>

        {/* Insights */}
        {stats.currentStreak >= 3 && (
          <div className="flex items-start gap-3 p-4 bg-orange-50 dark:bg-orange-950/20 rounded-lg">
            <Flame className="h-5 w-5 text-orange-600 flex-shrink-0 mt-0.5" />
            <div>
              <p className="font-medium text-orange-900 dark:text-orange-100">
                {stats.currentStreak} Day Streak!
              </p>
              <p className="text-sm text-orange-700 dark:text-orange-200">
                You&apos;re on fire! Keep practicing to maintain your streak.
              </p>
            </div>
          </div>
        )}

        {stats.activeDays > 0 && (
          <div className="flex items-start gap-3 p-4 bg-blue-50 dark:bg-blue-950/20 rounded-lg">
            <TrendingUp className="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" />
            <div>
              <p className="font-medium text-blue-900 dark:text-blue-100">Activity Insight</p>
              <p className="text-sm text-blue-700 dark:text-blue-200">
                You&apos;ve been active {stats.activeDays} out of the last{" "}
                {period === "week" ? "7" : period === "month" ? "30" : "90"} days (
                {Math.round((stats.activeDays / heatmapData.length) * 100)}% of the time).
              </p>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

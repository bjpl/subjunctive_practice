"use client";

import { useMemo, useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { PerformanceTrend } from "@/lib/analytics";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Area,
  AreaChart,
} from "recharts";
import { format } from "date-fns";
import { TrendingUp, Activity, Clock } from "lucide-react";

interface PerformanceChartProps {
  data: PerformanceTrend[];
  chartType?: "line" | "bar" | "area";
  metric?: "accuracy" | "exerciseCount" | "all";
}

export function PerformanceChart({
  data,
  chartType = "line",
  metric = "all",
}: PerformanceChartProps) {
  const [activeMetric, setActiveMetric] = useState<"accuracy" | "exerciseCount" | "all">(metric);
  const [activeChart, setActiveChart] = useState<"line" | "bar" | "area">(chartType);

  const formattedData = useMemo(() => {
    return data.map((item) => ({
      ...item,
      formattedDate: format(new Date(item.date), "MMM d"),
    }));
  }, [data]);

  const averageAccuracy = useMemo(() => {
    if (data.length === 0) return 0;
    const sum = data.reduce((acc, item) => acc + item.accuracy, 0);
    return Math.round(sum / data.length);
  }, [data]);

  const totalExercises = useMemo(() => {
    return data.reduce((acc, item) => acc + item.exerciseCount, 0);
  }, [data]);

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white dark:bg-gray-800 p-3 rounded-lg shadow-lg border">
          <p className="font-medium mb-2">{label}</p>
          {payload.map((entry: any, index: number) => (
            <p key={index} className="text-sm" style={{ color: entry.color }}>
              {entry.name}: {entry.value}
              {entry.name === "Accuracy" ? "%" : ""}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  const renderChart = () => {
    const commonProps = {
      data: formattedData,
      margin: { top: 10, right: 30, left: 0, bottom: 0 },
    };

    switch (activeChart) {
      case "bar":
        return (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart {...commonProps}>
              <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
              <XAxis
                dataKey="formattedDate"
                className="text-xs"
                tick={{ fontSize: 12 }}
              />
              <YAxis className="text-xs" tick={{ fontSize: 12 }} />
              <Tooltip content={<CustomTooltip />} />
              <Legend />
              {(activeMetric === "accuracy" || activeMetric === "all") && (
                <Bar dataKey="accuracy" fill="#3b82f6" name="Accuracy" />
              )}
              {(activeMetric === "exerciseCount" || activeMetric === "all") && (
                <Bar dataKey="exerciseCount" fill="#10b981" name="Exercises" />
              )}
            </BarChart>
          </ResponsiveContainer>
        );

      case "area":
        return (
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart {...commonProps}>
              <defs>
                <linearGradient id="colorAccuracy" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8} />
                  <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="colorExercises" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.8} />
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
              <XAxis
                dataKey="formattedDate"
                className="text-xs"
                tick={{ fontSize: 12 }}
              />
              <YAxis className="text-xs" tick={{ fontSize: 12 }} />
              <Tooltip content={<CustomTooltip />} />
              <Legend />
              {(activeMetric === "accuracy" || activeMetric === "all") && (
                <Area
                  type="monotone"
                  dataKey="accuracy"
                  stroke="#3b82f6"
                  fillOpacity={1}
                  fill="url(#colorAccuracy)"
                  name="Accuracy"
                />
              )}
              {(activeMetric === "exerciseCount" || activeMetric === "all") && (
                <Area
                  type="monotone"
                  dataKey="exerciseCount"
                  stroke="#10b981"
                  fillOpacity={1}
                  fill="url(#colorExercises)"
                  name="Exercises"
                />
              )}
            </AreaChart>
          </ResponsiveContainer>
        );

      default: // line chart
        return (
          <ResponsiveContainer width="100%" height={300}>
            <LineChart {...commonProps}>
              <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
              <XAxis
                dataKey="formattedDate"
                className="text-xs"
                tick={{ fontSize: 12 }}
              />
              <YAxis className="text-xs" tick={{ fontSize: 12 }} />
              <Tooltip content={<CustomTooltip />} />
              <Legend />
              {(activeMetric === "accuracy" || activeMetric === "all") && (
                <Line
                  type="monotone"
                  dataKey="accuracy"
                  stroke="#3b82f6"
                  strokeWidth={2}
                  dot={{ fill: "#3b82f6", r: 4 }}
                  activeDot={{ r: 6 }}
                  name="Accuracy"
                />
              )}
              {(activeMetric === "exerciseCount" || activeMetric === "all") && (
                <Line
                  type="monotone"
                  dataKey="exerciseCount"
                  stroke="#10b981"
                  strokeWidth={2}
                  dot={{ fill: "#10b981", r: 4 }}
                  activeDot={{ r: 6 }}
                  name="Exercises"
                />
              )}
            </LineChart>
          </ResponsiveContainer>
        );
    }
  };

  return (
    <Card>
      <CardHeader>
        <div className="flex items-start justify-between">
          <div>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5" />
              Performance Trends
            </CardTitle>
            <CardDescription>Track your learning progress over time</CardDescription>
          </div>
          <div className="flex gap-2">
            <select
              value={activeChart}
              onChange={(e) => setActiveChart(e.target.value as any)}
              className="text-sm border rounded-md px-2 py-1"
            >
              <option value="line">Line</option>
              <option value="bar">Bar</option>
              <option value="area">Area</option>
            </select>
            <select
              value={activeMetric}
              onChange={(e) => setActiveMetric(e.target.value as any)}
              className="text-sm border rounded-md px-2 py-1"
            >
              <option value="all">All Metrics</option>
              <option value="accuracy">Accuracy</option>
              <option value="exerciseCount">Exercise Count</option>
            </select>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {/* Summary Stats */}
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4 pb-4">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-blue-50">
                <TrendingUp className="h-5 w-5 text-blue-600" />
              </div>
              <div>
                <p className="text-xs text-muted-foreground">Avg Accuracy</p>
                <p className="text-lg font-bold">{averageAccuracy}%</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-green-50">
                <Activity className="h-5 w-5 text-green-600" />
              </div>
              <div>
                <p className="text-xs text-muted-foreground">Total Exercises</p>
                <p className="text-lg font-bold">{totalExercises}</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-purple-50">
                <Clock className="h-5 w-5 text-purple-600" />
              </div>
              <div>
                <p className="text-xs text-muted-foreground">Days Tracked</p>
                <p className="text-lg font-bold">{data.length}</p>
              </div>
            </div>
          </div>

          {/* Chart */}
          <div className="w-full">{renderChart()}</div>

          {/* Insight */}
          {data.length >= 7 && (
            <div className="bg-muted/50 rounded-lg p-4">
              <p className="text-sm font-medium mb-1">Trend Analysis</p>
              <p className="text-sm text-muted-foreground">
                {averageAccuracy >= 80
                  ? "Excellent work! Your accuracy is consistently high."
                  : averageAccuracy >= 60
                  ? "Good progress! Keep practicing to improve further."
                  : "Focus on understanding concepts better. Regular practice will help!"}
              </p>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}

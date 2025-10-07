"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAppSelector } from "@/hooks/use-redux";
import { useGetUserProgressQuery, useGetUserStatisticsQuery } from "@/store/api/progressApi";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import {
  ArrowLeft,
  Trophy,
  Target,
  Flame,
  BookOpen,
  TrendingUp,
  Calendar as CalendarIcon,
  Award,
  CheckCircle2,
  XCircle,
} from "lucide-react";

export default function ProgressPage() {
  const router = useRouter();
  const { isAuthenticated } = useAppSelector((state) => state.auth);

  const { data: progress, isLoading: progressLoading } = useGetUserProgressQuery();
  const { data: statistics, isLoading: statsLoading } = useGetUserStatisticsQuery();

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/auth/login");
    }
  }, [isAuthenticated, router]);

  if (!isAuthenticated) {
    return null;
  }

  const isLoading = progressLoading || statsLoading;

  const levelProgress = progress
    ? ((progress.experience_points % 100) / 100) * 100
    : 0;

  return (
    <div className="min-h-screen bg-background p-4 md:p-8">
      <div className="mx-auto max-w-7xl">
        {/* Header */}
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold">Your Progress</h1>
            <p className="mt-2 text-muted-foreground">
              Track your learning journey and achievements
            </p>
          </div>
          <Button variant="outline" onClick={() => router.push("/dashboard")}>
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back
          </Button>
        </div>

        {/* Loading State */}
        {isLoading && (
          <div className="flex items-center justify-center py-12">
            <div className="text-center">
              <div className="mx-auto h-16 w-16 animate-spin rounded-full border-b-2 border-t-2 border-primary"></div>
              <p className="mt-4 text-muted-foreground">Loading your progress...</p>
            </div>
          </div>
        )}

        {!isLoading && (
          <>
            {/* Level and XP Card */}
            <Card className="mb-8">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Trophy className="h-6 w-6 text-yellow-500" />
                  Level {progress?.level || 1}
                </CardTitle>
                <CardDescription>
                  {progress?.experience_points || 0} XP total
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Progress to next level</span>
                    <span>{levelProgress.toFixed(0)}%</span>
                  </div>
                  <Progress value={levelProgress} className="h-3" />
                  <p className="text-xs text-muted-foreground">
                    {100 - (progress?.experience_points || 0) % 100} XP until level{" "}
                    {(progress?.level || 1) + 1}
                  </p>
                </div>
              </CardContent>
            </Card>

            {/* Streak and Stats Grid */}
            <div className="mb-8 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
              <Card>
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-muted-foreground">
                        Current Streak
                      </p>
                      <p className="text-3xl font-bold text-orange-600">
                        {progress?.current_streak || 0}
                      </p>
                      <p className="text-xs text-muted-foreground">days</p>
                    </div>
                    <Flame className="h-8 w-8 text-orange-500" />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-muted-foreground">
                        Best Streak
                      </p>
                      <p className="text-3xl font-bold">{progress?.best_streak || 0}</p>
                      <p className="text-xs text-muted-foreground">days</p>
                    </div>
                    <Award className="h-8 w-8 text-purple-500" />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-muted-foreground">
                        Total Exercises
                      </p>
                      <p className="text-3xl font-bold">{progress?.total_exercises || 0}</p>
                    </div>
                    <BookOpen className="h-8 w-8 text-blue-500" />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="pt-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-muted-foreground">
                        Accuracy Rate
                      </p>
                      <p className="text-3xl font-bold">
                        {progress?.accuracy_rate.toFixed(1) || 0}%
                      </p>
                    </div>
                    <Target className="h-8 w-8 text-green-500" />
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Overall Statistics */}
            <Card className="mb-8">
              <CardHeader>
                <CardTitle>Overall Statistics</CardTitle>
                <CardDescription>Your performance summary</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid gap-6 md:grid-cols-2">
                  <div>
                    <div className="mb-2 flex items-center justify-between">
                      <span className="text-sm font-medium">Total Exercises</span>
                      <span className="text-sm font-bold">
                        {statistics?.overall_stats.total_exercises || 0}
                      </span>
                    </div>
                    <Progress
                      value={
                        statistics?.overall_stats.total_exercises
                          ? (statistics.overall_stats.total_exercises / 100) * 100
                          : 0
                      }
                    />
                  </div>

                  <div>
                    <div className="mb-2 flex items-center justify-between">
                      <span className="text-sm font-medium">Accuracy Rate</span>
                      <span className="text-sm font-bold">
                        {statistics?.overall_stats.accuracy_rate.toFixed(1) || 0}%
                      </span>
                    </div>
                    <Progress value={statistics?.overall_stats.accuracy_rate || 0} />
                  </div>

                  <div>
                    <div className="mb-2 flex items-center justify-between">
                      <span className="text-sm font-medium">Correct Answers</span>
                      <span className="text-sm font-bold text-green-600">
                        {statistics?.overall_stats.correct_answers || 0}
                      </span>
                    </div>
                    <div className="flex items-center gap-2">
                      <CheckCircle2 className="h-4 w-4 text-green-600" />
                      <Progress
                        value={
                          statistics?.overall_stats.total_exercises
                            ? ((statistics.overall_stats.correct_answers || 0) /
                                statistics.overall_stats.total_exercises) *
                              100
                            : 0
                        }
                        className="flex-1"
                      />
                    </div>
                  </div>

                  <div>
                    <div className="mb-2 flex items-center justify-between">
                      <span className="text-sm font-medium">Average Score</span>
                      <span className="text-sm font-bold">
                        {statistics?.overall_stats.average_score.toFixed(1) || 0}
                      </span>
                    </div>
                    <Progress value={statistics?.overall_stats.average_score || 0} />
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Performance by Exercise Type */}
            {statistics && Object.keys(statistics.by_type).length > 0 && (
              <Card className="mb-8">
                <CardHeader>
                  <CardTitle>Performance by Exercise Type</CardTitle>
                  <CardDescription>
                    See how you&apos;re doing with different subjunctive types
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {Object.entries(statistics.by_type).map(([type, stats]) => {
                      const typeStats = stats as { total: number; correct: number; accuracy: number };
                      return (
                        <div key={type}>
                          <div className="mb-2 flex items-center justify-between">
                            <span className="text-sm font-medium capitalize">
                              {type.replace(/_/g, " ")}
                            </span>
                            <div className="text-right text-sm">
                              <span className="font-bold">{typeStats.accuracy.toFixed(1)}%</span>
                              <span className="ml-2 text-muted-foreground">
                                ({typeStats.correct}/{typeStats.total})
                              </span>
                            </div>
                          </div>
                          <Progress value={typeStats.accuracy} />
                        </div>
                      );
                    })}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Performance by Difficulty */}
            {statistics && Object.keys(statistics.by_difficulty).length > 0 && (
              <Card className="mb-8">
                <CardHeader>
                  <CardTitle>Performance by Difficulty Level</CardTitle>
                  <CardDescription>Track your progress across difficulty levels</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {Object.entries(statistics.by_difficulty)
                      .sort(([a], [b]) => parseInt(a) - parseInt(b))
                      .map(([level, stats]) => {
                        const difficultyStats = stats as { total: number; correct: number; accuracy: number };
                        return (
                          <div key={level}>
                            <div className="mb-2 flex items-center justify-between">
                              <span className="text-sm font-medium">Level {level}</span>
                              <div className="text-right text-sm">
                                <span className="font-bold">{difficultyStats.accuracy.toFixed(1)}%</span>
                                <span className="ml-2 text-muted-foreground">
                                  ({difficultyStats.correct}/{difficultyStats.total})
                                </span>
                              </div>
                            </div>
                            <Progress value={difficultyStats.accuracy} />
                          </div>
                        );
                      })}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Recent Performance Timeline */}
            {statistics && statistics.recent_performance.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <CalendarIcon className="h-5 w-5" />
                    Recent Performance
                  </CardTitle>
                  <CardDescription>Your last {statistics.recent_performance.length} exercises</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {statistics.recent_performance.map((perf: any, index: number) => (
                      <div
                        key={index}
                        className="flex items-center justify-between border-b pb-3 last:border-0"
                      >
                        <div className="flex items-center gap-3">
                          {perf.is_correct ? (
                            <CheckCircle2 className="h-5 w-5 text-green-500" />
                          ) : (
                            <XCircle className="h-5 w-5 text-red-500" />
                          )}
                          <div>
                            <p className="text-sm font-medium capitalize">
                              {perf.exercise_type.replace(/_/g, " ")}
                            </p>
                            <p className="text-xs text-muted-foreground">
                              {new Date(perf.timestamp).toLocaleString()}
                            </p>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="text-sm font-bold">{perf.score}</p>
                          <p className="text-xs text-muted-foreground">points</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </>
        )}
      </div>
    </div>
  );
}

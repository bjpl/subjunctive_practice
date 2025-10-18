"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAppSelector, useAppDispatch } from "@/hooks/use-redux";
import { logout } from "@/store/slices/authSlice";
import { useGetUserProgressQuery, useGetUserStatisticsQuery } from "@/store/api/progressApi";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import {
  Trophy,
  Target,
  Flame,
  TrendingUp,
  BookOpen,
  Award,
  Brain,
  Calendar,
  LogOut,
  Play,
  BarChart3,
  Settings
} from "lucide-react";

export default function DashboardPage() {
  const router = useRouter();
  const dispatch = useAppDispatch();
  const { isAuthenticated, user } = useAppSelector((state) => state.auth);

  // Fetch progress and statistics
  const { data: progress, isLoading: progressLoading } = useGetUserProgressQuery();
  const { data: statistics, isLoading: statsLoading } = useGetUserStatisticsQuery();

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/auth/login");
    }
  }, [isAuthenticated, router]);

  const handleLogout = () => {
    dispatch(logout());
    router.push("/auth/login");
  };

  if (!isAuthenticated) {
    return null;
  }

  const isLoading = progressLoading || statsLoading;

  return (
    <div className="min-h-screen bg-background p-4 md:p-8">
      <div className="mx-auto max-w-7xl">
        {/* Header */}
        <div className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h1 className="text-4xl font-bold">Dashboard</h1>
            <p className="mt-2 text-muted-foreground">Welcome back, {user?.username}!</p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" onClick={() => router.push("/settings")}>
              <Settings className="mr-2 h-4 w-4" />
              Settings
            </Button>
            <Button onClick={handleLogout} variant="outline">
              <LogOut className="mr-2 h-4 w-4" />
              Logout
            </Button>
          </div>
        </div>

        {/* Loading State */}
        {isLoading && (
          <div className="flex items-center justify-center py-12">
            <div className="text-center">
              <div className="h-16 w-16 animate-spin rounded-full border-b-2 border-t-2 border-primary mx-auto"></div>
              <p className="mt-4 text-muted-foreground">Loading your progress...</p>
            </div>
          </div>
        )}

        {!isLoading && (
          <>
            {/* Quick Actions */}
            <div className="mb-8 grid gap-4 md:grid-cols-3">
              <Card className="cursor-pointer transition-all hover:shadow-lg" onClick={() => router.push("/practice")}>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Play className="h-5 w-5 text-green-600" />
                    Start Practice
                  </CardTitle>
                  <CardDescription>Begin a new practice session</CardDescription>
                </CardHeader>
                <CardContent>
                  <Button className="w-full">
                    <Play className="mr-2 h-4 w-4" />
                    Start Now
                  </Button>
                </CardContent>
              </Card>

              <Card className="cursor-pointer transition-all hover:shadow-lg" onClick={() => router.push("/progress")}>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <BarChart3 className="h-5 w-5 text-blue-600" />
                    View Progress
                  </CardTitle>
                  <CardDescription>Track your learning journey</CardDescription>
                </CardHeader>
                <CardContent>
                  <Button variant="outline" className="w-full">
                    <BarChart3 className="mr-2 h-4 w-4" />
                    View Details
                  </Button>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Flame className="h-5 w-5 text-orange-600" />
                    Current Streak
                  </CardTitle>
                  <CardDescription>Keep your momentum going!</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="text-center">
                    <div className="text-4xl font-bold text-orange-600">
                      {progress?.current_streak || 0}
                    </div>
                    <p className="text-sm text-muted-foreground">days in a row</p>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Stats Overview */}
            <div className="mb-8">
              <h2 className="mb-4 text-2xl font-bold">Your Statistics</h2>
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                <Card>
                  <CardContent className="pt-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-muted-foreground">Total Exercises</p>
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
                        <p className="text-sm font-medium text-muted-foreground">Accuracy Rate</p>
                        <p className="text-3xl font-bold">{progress?.accuracy_rate.toFixed(1) || 0}%</p>
                      </div>
                      <Target className="h-8 w-8 text-green-500" />
                    </div>
                    <Progress value={progress?.accuracy_rate || 0} className="mt-2" />
                  </CardContent>
                </Card>

                <Card>
                  <CardContent className="pt-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-muted-foreground">Current Level</p>
                        <p className="text-3xl font-bold">{progress?.level || 1}</p>
                      </div>
                      <Trophy className="h-8 w-8 text-yellow-500" />
                    </div>
                    <p className="mt-2 text-xs text-muted-foreground">
                      {progress?.experience_points || 0} XP
                    </p>
                  </CardContent>
                </Card>

                <Card>
                  <CardContent className="pt-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-muted-foreground">Best Streak</p>
                        <p className="text-3xl font-bold">{progress?.best_streak || 0}</p>
                      </div>
                      <Flame className="h-8 w-8 text-orange-500" />
                    </div>
                    <p className="mt-2 text-xs text-muted-foreground">days</p>
                  </CardContent>
                </Card>
              </div>
            </div>

            {/* Performance by Type */}
            {statistics && Object.keys(statistics.by_type).length > 0 && (
              <div className="mb-8">
                <h2 className="mb-4 text-2xl font-bold">Performance by Type</h2>
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                  {Object.entries(statistics.by_type).map(([type, stats]) => {
                    const typeStats = stats as { total: number; correct: number; accuracy: number };
                    return (
                      <Card key={type}>
                        <CardHeader>
                          <CardTitle className="text-base capitalize">
                            {type.replace(/_/g, " ")}
                          </CardTitle>
                        </CardHeader>
                        <CardContent>
                          <div className="space-y-2">
                            <div className="flex justify-between text-sm">
                              <span>Accuracy:</span>
                              <span className="font-bold">{typeStats.accuracy.toFixed(1)}%</span>
                            </div>
                            <Progress value={typeStats.accuracy} />
                            <div className="flex justify-between text-xs text-muted-foreground">
                              <span>{typeStats.correct} correct</span>
                              <span>{typeStats.total} total</span>
                            </div>
                          </div>
                        </CardContent>
                      </Card>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Learning Insights */}
            {statistics && statistics.learning_insights.length > 0 && (
              <div className="mb-8">
                <h2 className="mb-4 text-2xl font-bold flex items-center gap-2">
                  <Brain className="h-6 w-6" />
                  Learning Insights
                </h2>
                <div className="grid gap-4 md:grid-cols-2">
                  {statistics.learning_insights.map((insight: string, index: number) => (
                    <Card key={index}>
                      <CardContent className="pt-6">
                        <p className="flex items-start gap-2 text-sm">
                          <Award className="h-5 w-5 flex-shrink-0 text-primary" />
                          <span>{insight}</span>
                        </p>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>
            )}

            {/* Recent Activity */}
            {statistics && statistics.recent_performance.length > 0 && (
              <div>
                <h2 className="mb-4 text-2xl font-bold flex items-center gap-2">
                  <Calendar className="h-6 w-6" />
                  Recent Activity
                </h2>
                <Card>
                  <CardContent className="pt-6">
                    <div className="space-y-3">
                      {statistics.recent_performance.slice(0, 5).map((perf: any, index: number) => (
                        <div key={index} className="flex items-center justify-between border-b pb-3 last:border-0">
                          <div className="flex items-center gap-3">
                            <div className={`h-3 w-3 rounded-full ${
                              perf.is_correct ? 'bg-green-500' : 'bg-red-500'
                            }`} />
                            <div>
                              <p className="text-sm font-medium capitalize">
                                {perf.exercise_type.replace(/_/g, ' ')}
                              </p>
                              <p className="text-xs text-muted-foreground">
                                {new Date(perf.timestamp).toLocaleDateString()}
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
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

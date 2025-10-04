"use client";

import { Progress } from "@/types";
import { LevelInfo } from "@/lib/gamification";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress as ProgressBar } from "@/components/ui/progress";
import { Trophy, Target, Flame, Zap, TrendingUp, Clock } from "lucide-react";

interface OverallProgressProps {
  progress: Progress;
  levelInfo: LevelInfo;
  totalTimeSpent?: number;
  averageAccuracy?: number;
}

export function OverallProgress({
  progress,
  levelInfo,
  totalTimeSpent = 0,
  averageAccuracy = 0,
}: OverallProgressProps) {
  const formatTime = (seconds: number): string => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    if (hours > 0) {
      return `${hours}h ${minutes}m`;
    }
    return `${minutes}m`;
  };

  const stats = [
    {
      title: "Current Level",
      value: levelInfo.currentLevel,
      icon: Trophy,
      description: `${levelInfo.currentXP} / ${levelInfo.xpForNextLevel} XP`,
      color: "text-yellow-600",
      bgColor: "bg-yellow-50",
    },
    {
      title: "Overall Accuracy",
      value: `${Math.round(progress.accuracy)}%`,
      icon: Target,
      description: `${progress.correct_answers} / ${progress.completed_exercises} correct`,
      color: "text-blue-600",
      bgColor: "bg-blue-50",
    },
    {
      title: "Current Streak",
      value: `${progress.streak} days`,
      icon: Flame,
      description: progress.streak > 0 ? "Keep it going!" : "Start practicing today",
      color: "text-orange-600",
      bgColor: "bg-orange-50",
    },
    {
      title: "Total XP",
      value: levelInfo.totalXP.toLocaleString(),
      icon: Zap,
      description: `${levelInfo.progressToNextLevel}% to next level`,
      color: "text-purple-600",
      bgColor: "bg-purple-50",
    },
    {
      title: "Exercises Completed",
      value: progress.completed_exercises.toLocaleString(),
      icon: TrendingUp,
      description: `${progress.total_exercises} total exercises`,
      color: "text-green-600",
      bgColor: "bg-green-50",
    },
    {
      title: "Time Spent",
      value: formatTime(totalTimeSpent),
      icon: Clock,
      description: "Total practice time",
      color: "text-indigo-600",
      bgColor: "bg-indigo-50",
    },
  ];

  return (
    <div className="space-y-6">
      {/* Level Progress Card */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Trophy className="h-5 w-5 text-yellow-600" />
            Level {levelInfo.currentLevel}
          </CardTitle>
          <CardDescription>
            {levelInfo.xpForNextLevel - levelInfo.currentXP} XP until Level {levelInfo.currentLevel + 1}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Progress to Next Level</span>
              <span className="font-medium">{levelInfo.progressToNextLevel}%</span>
            </div>
            <ProgressBar value={levelInfo.progressToNextLevel} className="h-3" />
            <div className="flex justify-between text-xs text-muted-foreground">
              <span>{levelInfo.currentXP} XP</span>
              <span>{levelInfo.xpForNextLevel} XP</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <Card key={stat.title}>
              <CardContent className="p-6">
                <div className="flex items-start justify-between">
                  <div className="space-y-2">
                    <p className="text-sm font-medium text-muted-foreground">{stat.title}</p>
                    <p className="text-3xl font-bold">{stat.value}</p>
                    <p className="text-xs text-muted-foreground">{stat.description}</p>
                  </div>
                  <div className={`p-3 rounded-lg ${stat.bgColor}`}>
                    <Icon className={`h-6 w-6 ${stat.color}`} />
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Quick Stats Summary */}
      <Card>
        <CardHeader>
          <CardTitle>Learning Summary</CardTitle>
          <CardDescription>Your performance at a glance</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-muted-foreground">Completion Rate</span>
              <span className="text-sm font-medium">
                {progress.total_exercises > 0
                  ? Math.round((progress.completed_exercises / progress.total_exercises) * 100)
                  : 0}
                %
              </span>
            </div>
            <ProgressBar
              value={
                progress.total_exercises > 0
                  ? (progress.completed_exercises / progress.total_exercises) * 100
                  : 0
              }
            />

            <div className="grid grid-cols-3 gap-4 pt-4">
              <div className="text-center">
                <p className="text-2xl font-bold text-green-600">{progress.correct_answers}</p>
                <p className="text-xs text-muted-foreground">Correct</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-red-600">
                  {progress.completed_exercises - progress.correct_answers}
                </p>
                <p className="text-xs text-muted-foreground">Incorrect</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-blue-600">
                  {Math.round(progress.accuracy)}%
                </p>
                <p className="text-xs text-muted-foreground">Accuracy</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

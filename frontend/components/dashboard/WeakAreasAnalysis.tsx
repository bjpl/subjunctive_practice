"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { WeakArea } from "@/lib/analytics";
import { AlertCircle, BookOpen, Target, TrendingDown, Lightbulb } from "lucide-react";

interface WeakAreasAnalysisProps {
  weakAreas: WeakArea[];
  strongAreas?: WeakArea[];
  showRecommendations?: boolean;
}

export function WeakAreasAnalysis({
  weakAreas,
  strongAreas = [],
  showRecommendations = true,
}: WeakAreasAnalysisProps) {
  const getAccuracyColor = (accuracy: number) => {
    if (accuracy >= 70) return "text-yellow-600 bg-yellow-50";
    if (accuracy >= 50) return "text-orange-600 bg-orange-50";
    return "text-red-600 bg-red-50";
  };

  const getProgressColor = (accuracy: number) => {
    if (accuracy >= 70) return "bg-yellow-500";
    if (accuracy >= 50) return "bg-orange-500";
    return "bg-red-500";
  };

  const getDifficultyBadge = (difficulty?: string) => {
    if (!difficulty) return null;
    const colors = {
      easy: "bg-green-100 text-green-800",
      medium: "bg-yellow-100 text-yellow-800",
      hard: "bg-red-100 text-red-800",
    };
    return (
      <span
        className={`px-2 py-0.5 rounded-full text-xs font-medium ${
          colors[difficulty as keyof typeof colors]
        }`}
      >
        {difficulty}
      </span>
    );
  };

  const generateRecommendation = (area: WeakArea): string => {
    if (area.accuracy < 40) {
      return "Review fundamentals and complete beginner exercises in this category";
    } else if (area.accuracy < 60) {
      return "Practice more exercises and review explanations carefully";
    } else {
      return "You&apos;re close to mastery! A few more practice sessions should do it";
    }
  };

  return (
    <div className="space-y-6">
      {/* Weak Areas Card */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <AlertCircle className="h-5 w-5 text-orange-600" />
            Areas Needing Attention
          </CardTitle>
          <CardDescription>
            {weakAreas.length > 0
              ? "Focus on these topics to improve your overall performance"
              : "Great job! No weak areas detected. Keep up the excellent work!"}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {weakAreas.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-8 text-center">
              <Target className="h-12 w-12 text-green-600 mb-3" />
              <p className="text-lg font-medium">All Areas Looking Good!</p>
              <p className="text-sm text-muted-foreground mt-1">
                You&apos;re maintaining strong performance across all topics.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {weakAreas.map((area, index) => (
                <div
                  key={area.category}
                  className="border rounded-lg p-4 space-y-3 hover:bg-muted/50 transition-colors"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <h4 className="font-semibold">{area.category}</h4>
                        {getDifficultyBadge(area.difficulty)}
                      </div>
                      <p className="text-sm text-muted-foreground">
                        {area.correctAttempts} / {area.totalAttempts} correct attempts
                      </p>
                    </div>
                    <div
                      className={`px-3 py-1 rounded-full font-bold ${getAccuracyColor(
                        area.accuracy
                      )}`}
                    >
                      {area.accuracy}%
                    </div>
                  </div>

                  <div className="space-y-1">
                    <div className="flex justify-between text-xs text-muted-foreground">
                      <span>Accuracy</span>
                      <span>{area.accuracy}%</span>
                    </div>
                    <Progress
                      value={area.accuracy}
                      className={`h-2 ${getProgressColor(area.accuracy)}`}
                    />
                  </div>

                  {showRecommendations && (
                    <div className="flex items-start gap-2 bg-blue-50 dark:bg-blue-950 rounded-md p-3">
                      <Lightbulb className="h-4 w-4 text-blue-600 mt-0.5 flex-shrink-0" />
                      <p className="text-sm text-blue-900 dark:text-blue-100">
                        {generateRecommendation(area)}
                      </p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Strong Areas Card */}
      {strongAreas.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Target className="h-5 w-5 text-green-600" />
              Mastered Topics
            </CardTitle>
            <CardDescription>
              Topics where you&apos;re excelling - keep up the great work!
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {strongAreas.map((area) => (
                <div
                  key={area.category}
                  className="border rounded-lg p-4 bg-green-50 dark:bg-green-950/20"
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <h4 className="font-semibold">{area.category}</h4>
                        {getDifficultyBadge(area.difficulty)}
                      </div>
                      <p className="text-sm text-muted-foreground">
                        {area.correctAttempts} / {area.totalAttempts} correct
                      </p>
                    </div>
                    <div className="px-3 py-1 rounded-full font-bold text-green-600 bg-green-100">
                      {area.accuracy}%
                    </div>
                  </div>
                  <Progress value={area.accuracy} className="h-2 bg-green-500" />
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Study Tips Card */}
      {weakAreas.length > 0 && (
        <Card className="border-blue-200 bg-blue-50/50 dark:bg-blue-950/20">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-blue-900 dark:text-blue-100">
              <BookOpen className="h-5 w-5" />
              Study Tips
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <div className="flex items-start gap-2">
              <div className="h-1.5 w-1.5 rounded-full bg-blue-600 mt-2" />
              <p className="text-sm text-blue-900 dark:text-blue-100">
                Focus on one weak area at a time for better retention
              </p>
            </div>
            <div className="flex items-start gap-2">
              <div className="h-1.5 w-1.5 rounded-full bg-blue-600 mt-2" />
              <p className="text-sm text-blue-900 dark:text-blue-100">
                Review explanations after incorrect answers to understand concepts
              </p>
            </div>
            <div className="flex items-start gap-2">
              <div className="h-1.5 w-1.5 rounded-full bg-blue-600 mt-2" />
              <p className="text-sm text-blue-900 dark:text-blue-100">
                Practice weak areas daily for at least 5-10 minutes
              </p>
            </div>
            <div className="flex items-start gap-2">
              <div className="h-1.5 w-1.5 rounded-full bg-blue-600 mt-2" />
              <p className="text-sm text-blue-900 dark:text-blue-100">
                Revisit mastered topics occasionally to maintain proficiency
              </p>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

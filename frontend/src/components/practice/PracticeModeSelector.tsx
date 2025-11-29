"use client";

import { useRouter } from "next/navigation";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Zap, Settings2, Clock, Brain, Home } from "lucide-react";
import { PracticeConfig, PracticeConfigOptions } from "@/components/practice/PracticeConfig";
import type { ReviewStatsResponse } from "@/types/api";

interface PracticeModeSelectorProps {
  reviewStats?: ReviewStatsResponse;
  onStartQuickPractice: () => void;
  onStartCustomPractice: (config: PracticeConfigOptions) => Promise<void>;
  onStartReviewPractice: () => void;
  isGeneratingCustom: boolean;
}

export function PracticeModeSelector({
  reviewStats,
  onStartQuickPractice,
  onStartCustomPractice,
  onStartReviewPractice,
  isGeneratingCustom,
}: PracticeModeSelectorProps) {
  const router = useRouter();

  return (
    <div className="min-h-screen bg-background p-4 md:p-8">
      <div className="mx-auto max-w-4xl">
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold mb-2">Practice Spanish Subjunctive</h1>
          <p className="text-muted-foreground">
            Choose how you want to practice today
          </p>
        </div>

        {/* Mode Selection Cards */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          {/* Spaced Repetition Review Card */}
          {reviewStats && reviewStats.total_due > 0 && (
            <Card
              className="cursor-pointer hover:border-primary transition-colors border-2 border-orange-500 bg-orange-50 dark:bg-orange-950"
              onClick={onStartReviewPractice}
            >
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Brain className="h-6 w-6 text-orange-500" />
                  Review Due
                  <span className="ml-auto bg-orange-500 text-white rounded-full px-2 py-0.5 text-sm">
                    {reviewStats.total_due}
                  </span>
                </CardTitle>
                <CardDescription>
                  Practice items that are ready for review based on spaced repetition.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="text-sm text-muted-foreground space-y-1 mb-4">
                  <li>• {reviewStats.total_due} items due for review</li>
                  <li>• {Math.round(reviewStats.average_retention)}% retention rate</li>
                  <li>• {reviewStats.streak_days} day streak</li>
                </ul>
                <Button className="w-full bg-orange-500 hover:bg-orange-600">
                  <Clock className="mr-2 h-4 w-4" />
                  Start Review
                </Button>
              </CardContent>
            </Card>
          )}

          <Card className="cursor-pointer hover:border-primary transition-colors" onClick={onStartQuickPractice}>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Zap className="h-6 w-6 text-yellow-500" />
                Quick Practice
              </CardTitle>
              <CardDescription>
                Jump right in with a random selection of exercises from our database.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="text-sm text-muted-foreground space-y-1 mb-4">
                <li>• 10 random exercises</li>
                <li>• Mixed verb types and difficulties</li>
                <li>• Instant start</li>
              </ul>
              <Button className="w-full">
                <Zap className="mr-2 h-4 w-4" />
                Start Quick Practice
              </Button>
            </CardContent>
          </Card>

          <Card className="border-2 border-dashed">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Settings2 className="h-6 w-6 text-blue-500" />
                Custom Practice
              </CardTitle>
              <CardDescription>
                Configure exactly what you want to practice with full control over verbs, tenses, and context.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="text-sm text-muted-foreground space-y-1 mb-4">
                <li>• Choose specific verbs</li>
                <li>• Set custom sentences/context</li>
                <li>• Select tense, persons, difficulty</li>
              </ul>
            </CardContent>
          </Card>
        </div>

        {/* Custom Practice Configuration */}
        <PracticeConfig onStartPractice={onStartCustomPractice} isLoading={isGeneratingCustom} />

        <div className="mt-8 text-center">
          <Button variant="outline" onClick={() => router.push("/dashboard")}>
            <Home className="mr-2 h-4 w-4" />
            Back to Dashboard
          </Button>
        </div>
      </div>
    </div>
  );
}

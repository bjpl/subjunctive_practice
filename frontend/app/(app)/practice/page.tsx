"use client";

import { useState, useEffect } from "react";
import dynamic from "next/dynamic";
import { useRouter } from "next/navigation";
import { useAppSelector } from "@/hooks/use-redux";
import {
  useGenerateCustomExercisesMutation,
  useGetReviewStatsQuery,
  useGetDueReviewsQuery,
} from "@/store/api/exerciseApi";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Home } from "lucide-react";
import { useExerciseTags } from "@/hooks/useExerciseTags";
import { PracticeModeSelector } from "@/components/practice/PracticeModeSelector";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import type { GeneratedExercise } from "@/types/api";
import type { PracticeConfigOptions } from "@/components/practice/PracticeConfig";

// Dynamically import practice mode components with code splitting
const QuickPracticeMode = dynamic(
  () => import("@/components/practice/QuickPracticeMode").then(mod => ({ default: mod.QuickPracticeMode })),
  {
    loading: () => <LoadingSpinner message="Loading Quick Practice..." />,
    ssr: false
  }
);

const CustomPracticeMode = dynamic(
  () => import("@/components/practice/CustomPracticeMode").then(mod => ({ default: mod.CustomPracticeMode })),
  {
    loading: () => <LoadingSpinner message="Loading Custom Practice..." />,
    ssr: false
  }
);

const ReviewPracticeMode = dynamic(
  () => import("@/components/practice/ReviewPracticeMode").then(mod => ({ default: mod.ReviewPracticeMode })),
  {
    loading: () => <LoadingSpinner message="Loading Review Mode..." />,
    ssr: false
  }
);

type PracticeMode = "select" | "quick" | "custom" | "review";

export default function PracticePage() {
  const router = useRouter();
  const { isAuthenticated } = useAppSelector((state) => state.auth);

  // Practice mode state
  const [practiceMode, setPracticeMode] = useState<PracticeMode>("select");
  const [customExercises, setCustomExercises] = useState<GeneratedExercise[]>([]);

  // Tag filtering for quick mode
  const { selectedTags, setTags } = useExerciseTags([]);

  // Generate custom exercises mutation
  const [generateCustomExercises, { isLoading: isGenerating }] = useGenerateCustomExercisesMutation();

  // Spaced repetition review data
  const { data: reviewStats } = useGetReviewStatsQuery(undefined, { skip: practiceMode !== "select" });
  const { refetch: refetchReviews } = useGetDueReviewsQuery({ limit: 20 }, { skip: practiceMode !== "review" });

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/auth/login");
    }
  }, [isAuthenticated, router]);

  if (!isAuthenticated) {
    return null;
  }

  // Handle custom practice start
  const handleStartCustomPractice = async (config: PracticeConfigOptions) => {
    try {
      const result = await generateCustomExercises({
        verbs: config.verbs,
        tense: config.tense,
        persons: config.persons,
        difficulty: config.difficulty,
        custom_context: config.customContext,
        trigger_category: config.triggerCategory,
        exercise_count: config.exerciseCount,
        include_hints: config.includeHints,
        include_explanations: config.includeExplanations,
      }).unwrap();

      setCustomExercises(result.exercises);
      setPracticeMode("custom");
    } catch (error) {
      console.error("Error generating custom exercises:", error);
    }
  };

  // Handle quick practice start
  const handleStartQuickPractice = () => {
    setPracticeMode("quick");
  };

  // Handle review practice start
  const handleStartReviewPractice = () => {
    setPracticeMode("review");
  };

  // Handle exit to mode selection
  const handleBackToModeSelect = () => {
    setPracticeMode("select");
    setCustomExercises([]);
  };

  // Mode selection screen
  if (practiceMode === "select") {
    return (
      <PracticeModeSelector
        reviewStats={reviewStats}
        onStartQuickPractice={handleStartQuickPractice}
        onStartCustomPractice={handleStartCustomPractice}
        onStartReviewPractice={handleStartReviewPractice}
        isGeneratingCustom={isGenerating}
      />
    );
  }

  // Quick practice mode
  if (practiceMode === "quick") {
    return (
      <QuickPracticeMode
        selectedTags={selectedTags}
        onTagsChange={setTags}
        onExit={handleBackToModeSelect}
      />
    );
  }

  // Custom practice mode
  if (practiceMode === "custom") {
    if (customExercises.length === 0) {
      return (
        <div className="flex min-h-screen items-center justify-center bg-background p-4">
          <Card className="max-w-md">
            <CardHeader>
              <CardTitle>No Exercises Available</CardTitle>
              <CardDescription>
                No exercises could be generated with your configuration. Try different settings.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button onClick={handleBackToModeSelect} className="w-full">
                <Home className="mr-2 h-4 w-4" />
                Back to Practice Selection
              </Button>
            </CardContent>
          </Card>
        </div>
      );
    }

    return (
      <CustomPracticeMode
        exercises={customExercises}
        onExit={handleBackToModeSelect}
      />
    );
  }

  // Review practice mode
  if (practiceMode === "review") {
    return (
      <ReviewPracticeMode
        onExit={handleBackToModeSelect}
      />
    );
  }

  return null;
}

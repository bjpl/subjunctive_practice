"use client";

import { useState } from "react";
import { useGetExercisesQuery, useSubmitAnswerMutation } from "@/store/api/exerciseApi";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";
import { Home } from "lucide-react";
import { TagFilter } from "@/components/practice/TagFilter";
import { SessionStats } from "@/components/practice/SessionStats";
import { ExerciseDisplay, DisplayExercise } from "@/components/practice/ExerciseDisplay";
import type { ApiExercise, AnswerValidation } from "@/types/api";

interface QuickPracticeModeProps {
  selectedTags: string[];
  onTagsChange: (tags: string[]) => void;
  onExit: () => void;
}

export function QuickPracticeMode({ selectedTags, onTagsChange, onExit }: QuickPracticeModeProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [showFeedback, setShowFeedback] = useState(false);
  const [validationResult, setValidationResult] = useState<AnswerValidation | null>(null);
  const [sessionStats, setSessionStats] = useState({
    correct: 0,
    total: 0,
    startTime: Date.now(),
  });

  const { data: exerciseData, isLoading } = useGetExercisesQuery({
    limit: 10,
    random_order: true,
    tags: selectedTags.length > 0 ? selectedTags : undefined,
  });

  const [submitAnswer, { isLoading: isSubmitting }] = useSubmitAnswerMutation();

  const exercises = exerciseData?.exercises || [];
  const currentExercise = exercises[currentIndex] as ApiExercise | undefined;
  const progress = exercises.length > 0 ? ((currentIndex + 1) / exercises.length) * 100 : 0;

  const getExerciseForDisplay = (): DisplayExercise | null => {
    if (!currentExercise) return null;

    return {
      id: currentExercise.id,
      type: currentExercise.type || "practice",
      prompt: currentExercise.prompt,
      difficulty: currentExercise.difficulty || 2,
      explanation: currentExercise.explanation,
      hints: currentExercise.hints || [],
      tags: currentExercise.tags || [],
    };
  };

  const handleSubmit = async (answer: string) => {
    if (!currentExercise) return;

    const timeTaken = Math.floor((Date.now() - sessionStats.startTime) / 1000);

    try {
      const result = await submitAnswer({
        exercise_id: currentExercise.id,
        user_answer: answer,
        time_taken: timeTaken,
      }).unwrap();

      setValidationResult(result);
      setShowFeedback(true);

      setSessionStats((prev) => ({
        ...prev,
        total: prev.total + 1,
        correct: prev.correct + (result.is_correct ? 1 : 0),
      }));
    } catch (error) {
      console.error("Error submitting answer:", error);
    }
  };

  const handleNext = () => {
    if (currentIndex < exercises.length - 1) {
      setCurrentIndex(currentIndex + 1);
      setShowFeedback(false);
      setValidationResult(null);
      setSessionStats((prev) => ({ ...prev, startTime: Date.now() }));
    } else {
      // Session complete
      onExit();
    }
  };

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background">
        <div className="text-center">
          <div className="h-32 w-32 animate-spin rounded-full border-b-2 border-t-2 border-primary"></div>
          <p className="mt-4 text-lg text-muted-foreground">Loading exercises...</p>
        </div>
      </div>
    );
  }

  const displayExercise = getExerciseForDisplay();

  return (
    <div className="min-h-screen bg-background p-4 md:p-8">
      <div className="mx-auto max-w-4xl">
        {/* Header */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold">Quick Practice</h1>
              <p className="text-muted-foreground">
                Exercise {currentIndex + 1} of {exercises.length}
              </p>
            </div>
            <Button variant="outline" onClick={onExit}>
              <Home className="mr-2 h-4 w-4" />
              Exit
            </Button>
          </div>

          {/* Tag Filter */}
          <div className="flex items-center gap-2">
            <TagFilter selectedTags={selectedTags} onTagsChange={onTagsChange} />
          </div>
        </div>

        {/* Progress Bar */}
        <div className="mb-8">
          <div className="mb-2 flex justify-between text-sm">
            <span>Progress</span>
            <span>{Math.round(progress)}%</span>
          </div>
          <Progress value={progress} className="h-2" />
        </div>

        {/* Session Stats */}
        <SessionStats correct={sessionStats.correct} total={sessionStats.total} />

        {/* Exercise Display */}
        {displayExercise && (
          <ExerciseDisplay
            exercise={displayExercise}
            onSubmit={handleSubmit}
            onNext={handleNext}
            isSubmitting={isSubmitting}
            validationResult={validationResult}
            showFeedback={showFeedback}
            isLastExercise={currentIndex === exercises.length - 1}
          />
        )}
      </div>
    </div>
  );
}

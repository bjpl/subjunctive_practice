"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAppSelector } from "@/hooks/use-redux";
import { useGetExercisesQuery, useSubmitAnswerMutation } from "@/store/api/exerciseApi";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Progress } from "@/components/ui/progress";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { CheckCircle2, XCircle, Lightbulb, ArrowRight, Home } from "lucide-react";
import { TagFilter } from "@/components/practice/TagFilter";
import { TagList } from "@/components/practice/TagBadge";
import { useExerciseTags } from "@/hooks/useExerciseTags";

export default function PracticePage() {
  const router = useRouter();
  const { isAuthenticated } = useAppSelector((state) => state.auth);

  const [currentIndex, setCurrentIndex] = useState(0);
  const [userAnswer, setUserAnswer] = useState("");
  const [showFeedback, setShowFeedback] = useState(false);
  const [showHint, setShowHint] = useState(false);
  const [sessionStats, setSessionStats] = useState({
    correct: 0,
    total: 0,
    startTime: Date.now(),
  });

  // Tag filtering
  const { selectedTags, setTags } = useExerciseTags([]);

  // Fetch exercises with tag filters
  const { data: exerciseData, isLoading, error } = useGetExercisesQuery({
    limit: 10,
    random_order: true,
    tags: selectedTags.length > 0 ? selectedTags : undefined,
  });

  // Submit answer mutation
  const [submitAnswer, { isLoading: isSubmitting }] = useSubmitAnswerMutation();
  const [validationResult, setValidationResult] = useState<any>(null);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/auth/login");
    }
  }, [isAuthenticated, router]);

  if (!isAuthenticated) {
    return null;
  }

  const currentExercise = exerciseData?.exercises[currentIndex];
  const progress = exerciseData ? ((currentIndex + 1) / exerciseData.exercises.length) * 100 : 0;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentExercise || !userAnswer.trim()) return;

    const timeTaken = Math.floor((Date.now() - sessionStats.startTime) / 1000);

    try {
      const result = await submitAnswer({
        exercise_id: currentExercise.id,
        user_answer: userAnswer.trim(),
        time_taken: timeTaken,
      }).unwrap();

      setValidationResult(result);
      setShowFeedback(true);

      // Update session stats
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
    if (!exerciseData) return;

    if (currentIndex < exerciseData.exercises.length - 1) {
      setCurrentIndex(currentIndex + 1);
      setUserAnswer("");
      setShowFeedback(false);
      setShowHint(false);
      setValidationResult(null);
      setSessionStats((prev) => ({ ...prev, startTime: Date.now() }));
    } else {
      // Session complete
      router.push("/dashboard");
    }
  };

  const handleShowHint = () => {
    setShowHint(!showHint);
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

  if (error) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background p-4">
        <Card className="max-w-md">
          <CardHeader>
            <CardTitle className="text-destructive">Error Loading Exercises</CardTitle>
            <CardDescription>
              We couldn&apos;t load the exercises. Please try again.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button onClick={() => router.push("/dashboard")} className="w-full">
              <Home className="mr-2 h-4 w-4" />
              Back to Dashboard
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!exerciseData || exerciseData.exercises.length === 0) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background p-4">
        <Card className="max-w-md">
          <CardHeader>
            <CardTitle>No Exercises Available</CardTitle>
            <CardDescription>
              There are no exercises available at the moment.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button onClick={() => router.push("/dashboard")} className="w-full">
              <Home className="mr-2 h-4 w-4" />
              Back to Dashboard
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background p-4 md:p-8">
      <div className="mx-auto max-w-4xl">
        {/* Header */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold">Practice Session</h1>
              <p className="text-muted-foreground">
                Exercise {currentIndex + 1} of {exerciseData.exercises.length}
              </p>
            </div>
            <Button variant="outline" onClick={() => router.push("/dashboard")}>
              <Home className="mr-2 h-4 w-4" />
              Exit
            </Button>
          </div>

          {/* Tag Filter */}
          <div className="flex items-center gap-2">
            <TagFilter
              selectedTags={selectedTags}
              onTagsChange={setTags}
            />
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
        <div className="mb-6 grid grid-cols-2 gap-4 md:grid-cols-4">
          <Card>
            <CardContent className="pt-6">
              <div className="text-2xl font-bold">{sessionStats.total}</div>
              <p className="text-sm text-muted-foreground">Completed</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="text-2xl font-bold text-green-600">{sessionStats.correct}</div>
              <p className="text-sm text-muted-foreground">Correct</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="text-2xl font-bold text-red-600">
                {sessionStats.total - sessionStats.correct}
              </div>
              <p className="text-sm text-muted-foreground">Incorrect</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="text-2xl font-bold">
                {sessionStats.total > 0
                  ? Math.round((sessionStats.correct / sessionStats.total) * 100)
                  : 0}
                %
              </div>
              <p className="text-sm text-muted-foreground">Accuracy</p>
            </CardContent>
          </Card>
        </div>

        {/* Exercise Card */}
        {currentExercise && (
          <Card className="mb-6">
            <CardHeader>
              <div className="flex items-center justify-between mb-2">
                <CardTitle>Exercise</CardTitle>
                <div className="flex items-center gap-2">
                  <span className="rounded-full bg-primary/10 px-3 py-1 text-sm font-medium text-primary">
                    {currentExercise.type.replace(/_/g, " ")}
                  </span>
                  <span className="rounded-full bg-secondary px-3 py-1 text-sm font-medium">
                    Level {currentExercise.difficulty}
                  </span>
                </div>
              </div>
              {currentExercise.tags && currentExercise.tags.length > 0 && (
                <div className="flex items-center gap-2">
                  <TagList tags={currentExercise.tags} size="sm" maxDisplay={8} />
                </div>
              )}
            </CardHeader>
            <CardContent>
              <p className="mb-6 text-lg">{currentExercise.prompt}</p>

              {!showFeedback ? (
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div>
                    <Input
                      type="text"
                      value={userAnswer}
                      onChange={(e) => setUserAnswer(e.target.value)}
                      placeholder="Type your answer here..."
                      className="text-lg"
                      autoFocus
                      disabled={isSubmitting}
                    />
                  </div>

                  <div className="flex gap-2">
                    <Button type="submit" disabled={!userAnswer.trim() || isSubmitting} className="flex-1">
                      {isSubmitting ? "Checking..." : "Submit Answer"}
                    </Button>
                    {currentExercise.hints && currentExercise.hints.length > 0 && (
                      <Button type="button" variant="outline" onClick={handleShowHint}>
                        <Lightbulb className="mr-2 h-4 w-4" />
                        Hint
                      </Button>
                    )}
                  </div>
                </form>
              ) : (
                <div className="space-y-4">
                  {/* Feedback */}
                  {validationResult && (
                    <Alert
                      className={
                        validationResult.is_correct
                          ? "border-green-500 bg-green-50 dark:bg-green-950"
                          : "border-red-500 bg-red-50 dark:bg-red-950"
                      }
                    >
                      <div className="flex items-start gap-3">
                        {validationResult.is_correct ? (
                          <CheckCircle2 className="h-5 w-5 text-green-600" />
                        ) : (
                          <XCircle className="h-5 w-5 text-red-600" />
                        )}
                        <div className="flex-1">
                          <h4 className="mb-1 font-semibold">
                            {validationResult.is_correct ? "Correct!" : "Not quite"}
                          </h4>
                          <AlertDescription>{validationResult.feedback}</AlertDescription>
                          {!validationResult.is_correct && (
                            <div className="mt-2">
                              <p className="text-sm">
                                <strong>Correct answer:</strong> {validationResult.correct_answer}
                              </p>
                              {validationResult.alternative_answers &&
                                validationResult.alternative_answers.length > 0 && (
                                  <p className="mt-1 text-sm">
                                    <strong>Also accepted:</strong>{" "}
                                    {validationResult.alternative_answers.join(", ")}
                                  </p>
                                )}
                            </div>
                          )}
                        </div>
                      </div>
                    </Alert>
                  )}

                  {/* Explanation */}
                  {validationResult?.explanation && (
                    <Card className="border-primary/20 bg-primary/5">
                      <CardHeader>
                        <CardTitle className="text-base">Explanation</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <p className="text-sm">{validationResult.explanation}</p>
                      </CardContent>
                    </Card>
                  )}

                  {/* Next Button */}
                  <Button onClick={handleNext} className="w-full">
                    {currentIndex < exerciseData.exercises.length - 1 ? (
                      <>
                        Next Exercise
                        <ArrowRight className="ml-2 h-4 w-4" />
                      </>
                    ) : (
                      <>
                        Complete Session
                        <CheckCircle2 className="ml-2 h-4 w-4" />
                      </>
                    )}
                  </Button>
                </div>
              )}

              {/* Hint Display */}
              {showHint && currentExercise.hints && currentExercise.hints.length > 0 && !showFeedback && (
                <Card className="mt-4 border-yellow-500 bg-yellow-50 dark:bg-yellow-950">
                  <CardHeader>
                    <CardTitle className="flex items-center text-base">
                      <Lightbulb className="mr-2 h-4 w-4" />
                      Hint
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm">{currentExercise.hints[0]}</p>
                  </CardContent>
                </Card>
              )}
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}

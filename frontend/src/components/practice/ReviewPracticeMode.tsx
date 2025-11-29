"use client";

/**
 * ReviewPracticeMode - Lazy-loaded component for spaced repetition review mode
 * This component will be loaded on-demand when the user selects review practice
 */

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Progress } from "@/components/ui/progress";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { CheckCircle2, XCircle, Lightbulb, ArrowRight, Home, Brain } from "lucide-react";
import { TagList } from "@/components/practice/TagBadge";
import { useGetDueReviewsQuery, useSubmitAnswerMutation } from "@/store/api/exerciseApi";
import type { DueReviewItem } from "@/types/api";

interface ReviewExercise {
  id: string;
  verb: string;
  verb_translation: string;
  tense: string;
  person: string;
  prompt: string;
  difficulty: number;
  days_overdue: number;
  difficulty_level: string;
}

interface ReviewPracticeModeProps {
  onExit: () => void;
}

export function ReviewPracticeMode({ onExit }: ReviewPracticeModeProps) {
  const [reviewExercises, setReviewExercises] = useState<ReviewExercise[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [userAnswer, setUserAnswer] = useState("");
  const [showFeedback, setShowFeedback] = useState(false);
  const [showHint, setShowHint] = useState(false);
  const [sessionStats, setSessionStats] = useState({
    correct: 0,
    total: 0,
    startTime: Date.now(),
  });

  const { data: dueReviews, isLoading, refetch } = useGetDueReviewsQuery({ limit: 20 });
  const [submitAnswer, { isLoading: isSubmitting }] = useSubmitAnswerMutation();
  const [validationResult, setValidationResult] = useState<any>(null);

  useEffect(() => {
    if (dueReviews?.items) {
      const converted: ReviewExercise[] = dueReviews.items.map((item: DueReviewItem) => {
        const personLabels: Record<string, string> = {
          "yo": "I",
          "tú": "you (informal)",
          "él/ella/usted": "he/she/you (formal)",
          "nosotros": "we",
          "vosotros": "you all (Spain)",
          "ellos/ellas/ustedes": "they/you all"
        };
        const personLabel = item.person ? personLabels[item.person] || item.person : "yo";
        const tenseLabel = item.tense.replace(/_/g, " ");

        return {
          id: `review_${item.verb_id}_${item.tense}_${item.person || "yo"}`,
          verb: item.verb_infinitive,
          verb_translation: item.verb_translation,
          tense: item.tense,
          person: item.person || "yo",
          prompt: `Conjugate "${item.verb_infinitive}" (${item.verb_translation}) in the ${tenseLabel} for "${personLabel}"`,
          difficulty: item.difficulty_level === "new" ? 1 : item.difficulty_level === "learning" ? 2 : item.difficulty_level === "reviewing" ? 3 : 4,
          days_overdue: item.days_overdue,
          difficulty_level: item.difficulty_level,
        };
      });
      setReviewExercises(converted);
    }
  }, [dueReviews]);

  const currentExercise = reviewExercises[currentIndex];
  const progress = reviewExercises.length > 0 ? ((currentIndex + 1) / reviewExercises.length) * 100 : 0;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentExercise || !userAnswer.trim()) return;

    const timeTaken = Math.floor((Date.now() - sessionStats.startTime) / 1000);

    try {
      const result = await submitAnswer({
        exercise_id: currentExercise.id,
        user_answer: userAnswer.trim(),
        time_taken: timeTaken,
        verb: currentExercise.verb,
        tense: currentExercise.tense,
        person: currentExercise.person,
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
    if (currentIndex < reviewExercises.length - 1) {
      setCurrentIndex(currentIndex + 1);
      setUserAnswer("");
      setShowFeedback(false);
      setShowHint(false);
      setValidationResult(null);
      setSessionStats((prev) => ({ ...prev, startTime: Date.now() }));
    } else {
      refetch();
      onExit();
    }
  };

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background">
        <div className="text-center">
          <div className="h-32 w-32 animate-spin rounded-full border-b-2 border-t-2 border-orange-500"></div>
          <p className="mt-4 text-lg text-muted-foreground">Loading review items...</p>
        </div>
      </div>
    );
  }

  if (reviewExercises.length === 0) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background p-4">
        <Card className="max-w-md">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <CheckCircle2 className="h-6 w-6 text-green-500" />
              All Caught Up!
            </CardTitle>
            <CardDescription>
              You have no items due for review right now. Keep practicing to build your review queue!
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button onClick={onExit} className="w-full">
              <Home className="mr-2 h-4 w-4" />
              Back to Practice Selection
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background p-4 md:p-8">
      <div className="mx-auto max-w-4xl">
        <div className="mb-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold">Spaced Repetition Review</h1>
              <p className="text-muted-foreground">
                Review Item {currentIndex + 1} of {reviewExercises.length}
              </p>
            </div>
            <Button variant="outline" onClick={onExit}>
              <Home className="mr-2 h-4 w-4" />
              Exit
            </Button>
          </div>
        </div>

        <div className="mb-8">
          <div className="mb-2 flex justify-between text-sm">
            <span>Progress</span>
            <span>{Math.round(progress)}%</span>
          </div>
          <Progress value={progress} className="h-2" />
        </div>

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

        {currentExercise && (
          <Card className="mb-6">
            <CardHeader>
              <div className="flex items-center justify-between mb-2">
                <CardTitle>Exercise</CardTitle>
                <div className="flex items-center gap-2">
                  <span className="rounded-full bg-primary/10 px-3 py-1 text-sm font-medium text-primary">
                    {currentExercise.tense.replace(/_/g, " ")}
                  </span>
                  <span className="rounded-full bg-secondary px-3 py-1 text-sm font-medium">
                    Level {currentExercise.difficulty}
                  </span>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <TagList
                  tags={[currentExercise.verb, currentExercise.person, currentExercise.difficulty_level]}
                  size="sm"
                  maxDisplay={8}
                />
              </div>
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
                    {currentExercise.days_overdue > 0 && (
                      <Button type="button" variant="outline" onClick={() => setShowHint(!showHint)}>
                        <Lightbulb className="mr-2 h-4 w-4" />
                        Hint
                      </Button>
                    )}
                  </div>
                </form>
              ) : (
                <div className="space-y-4">
                  {validationResult && (
                    <>
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
                              </div>
                            )}
                          </div>
                        </div>
                      </Alert>

                      {validationResult.next_review_date && (
                        <Card className="border-orange-200 bg-orange-50 dark:border-orange-800 dark:bg-orange-950">
                          <CardHeader className="pb-2">
                            <CardTitle className="flex items-center text-base">
                              <Brain className="mr-2 h-4 w-4 text-orange-500" />
                              Spaced Repetition
                            </CardTitle>
                          </CardHeader>
                          <CardContent>
                            <div className="flex items-center justify-between text-sm">
                              <span>Next review:</span>
                              <span className="font-medium">
                                {validationResult.interval_days === 0
                                  ? "Later today"
                                  : validationResult.interval_days === 1
                                    ? "Tomorrow"
                                    : `In ${validationResult.interval_days} days`}
                              </span>
                            </div>
                            {validationResult.difficulty_level && (
                              <div className="flex items-center justify-between text-sm mt-1">
                                <span>Status:</span>
                                <span className={`font-medium capitalize ${
                                  validationResult.difficulty_level === "mastered" ? "text-green-600" :
                                  validationResult.difficulty_level === "reviewing" ? "text-blue-600" :
                                  validationResult.difficulty_level === "learning" ? "text-yellow-600" : "text-gray-600"
                                }`}>
                                  {validationResult.difficulty_level}
                                </span>
                              </div>
                            )}
                          </CardContent>
                        </Card>
                      )}
                    </>
                  )}

                  <Button onClick={handleNext} className="w-full">
                    {currentIndex < reviewExercises.length - 1 ? (
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

              {showHint && currentExercise.days_overdue > 0 && !showFeedback && (
                <Card className="mt-4 border-yellow-500 bg-yellow-50 dark:bg-yellow-950">
                  <CardHeader>
                    <CardTitle className="flex items-center text-base">
                      <Lightbulb className="mr-2 h-4 w-4" />
                      Hint
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm">
                      This item is {currentExercise.days_overdue} day(s) overdue for review
                    </p>
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

export default ReviewPracticeMode;

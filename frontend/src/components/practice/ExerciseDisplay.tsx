"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { CheckCircle2, XCircle, Lightbulb, ArrowRight, Brain } from "lucide-react";
import { TagList } from "@/components/practice/TagBadge";
import type { AnswerValidation } from "@/types/api";

export interface DisplayExercise {
  id: string;
  type: string;
  prompt: string;
  difficulty: number;
  explanation?: string;
  hints: string[];
  tags: string[];
  correct_answer?: string;
}

interface ExerciseDisplayProps {
  exercise: DisplayExercise;
  onSubmit: (answer: string) => Promise<void>;
  onNext: () => void;
  isSubmitting: boolean;
  validationResult: AnswerValidation | null;
  showFeedback: boolean;
  isLastExercise: boolean;
}

export function ExerciseDisplay({
  exercise,
  onSubmit,
  onNext,
  isSubmitting,
  validationResult,
  showFeedback,
  isLastExercise,
}: ExerciseDisplayProps) {
  const [userAnswer, setUserAnswer] = useState("");
  const [showHint, setShowHint] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!userAnswer.trim()) return;
    await onSubmit(userAnswer.trim());
  };

  const handleNext = () => {
    setUserAnswer("");
    setShowHint(false);
    onNext();
  };

  return (
    <Card className="mb-6">
      <CardHeader>
        <div className="flex items-center justify-between mb-2">
          <CardTitle>Exercise</CardTitle>
          <div className="flex items-center gap-2">
            <span className="rounded-full bg-primary/10 px-3 py-1 text-sm font-medium text-primary">
              {exercise.type.replace(/_/g, " ")}
            </span>
            <span className="rounded-full bg-secondary px-3 py-1 text-sm font-medium">
              Level {exercise.difficulty}
            </span>
          </div>
        </div>
        {exercise.tags && exercise.tags.length > 0 && (
          <div className="flex items-center gap-2">
            <TagList tags={exercise.tags} size="sm" maxDisplay={8} />
          </div>
        )}
      </CardHeader>
      <CardContent>
        <p className="mb-6 text-lg">{exercise.prompt}</p>

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
              {exercise.hints && exercise.hints.length > 0 && (
                <Button type="button" variant="outline" onClick={() => setShowHint(!showHint)}>
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

            {/* Spaced Repetition Info */}
            {validationResult?.next_review_date && (
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

            {/* Suggestions */}
            {validationResult?.suggestions && validationResult.suggestions.length > 0 && (
              <Card className="border-blue-200 bg-blue-50 dark:border-blue-800 dark:bg-blue-950">
                <CardHeader className="pb-2">
                  <CardTitle className="text-base">Suggestions</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="text-sm space-y-1">
                    {validationResult.suggestions.map((suggestion: string, idx: number) => (
                      <li key={idx}>• {suggestion}</li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            )}

            {/* Next Button */}
            <Button onClick={handleNext} className="w-full">
              {!isLastExercise ? (
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
        {showHint && exercise.hints && exercise.hints.length > 0 && !showFeedback && (
          <Card className="mt-4 border-yellow-500 bg-yellow-50 dark:bg-yellow-950">
            <CardHeader>
              <CardTitle className="flex items-center text-base">
                <Lightbulb className="mr-2 h-4 w-4" />
                Hint
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm">{exercise.hints[0]}</p>
            </CardContent>
          </Card>
        )}
      </CardContent>
    </Card>
  );
}

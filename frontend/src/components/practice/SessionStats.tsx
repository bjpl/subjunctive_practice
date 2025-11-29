"use client";

import { Card, CardContent } from "@/components/ui/card";

interface SessionStatsProps {
  correct: number;
  total: number;
}

export function SessionStats({ correct, total }: SessionStatsProps) {
  const accuracy = total > 0 ? Math.round((correct / total) * 100) : 0;

  return (
    <div className="mb-6 grid grid-cols-2 gap-4 md:grid-cols-4">
      <Card>
        <CardContent className="pt-6">
          <div className="text-2xl font-bold">{total}</div>
          <p className="text-sm text-muted-foreground">Completed</p>
        </CardContent>
      </Card>
      <Card>
        <CardContent className="pt-6">
          <div className="text-2xl font-bold text-green-600">{correct}</div>
          <p className="text-sm text-muted-foreground">Correct</p>
        </CardContent>
      </Card>
      <Card>
        <CardContent className="pt-6">
          <div className="text-2xl font-bold text-red-600">{total - correct}</div>
          <p className="text-sm text-muted-foreground">Incorrect</p>
        </CardContent>
      </Card>
      <Card>
        <CardContent className="pt-6">
          <div className="text-2xl font-bold">{accuracy}%</div>
          <p className="text-sm text-muted-foreground">Accuracy</p>
        </CardContent>
      </Card>
    </div>
  );
}

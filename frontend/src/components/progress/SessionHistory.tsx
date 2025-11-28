"use client";

import { useState, useMemo } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { PracticeSession } from "@/types";
import { format, formatDistanceToNow } from "date-fns";
import {
  History,
  Calendar,
  Clock,
  Target,
  CheckCircle2,
  XCircle,
  TrendingUp,
  Filter,
} from "lucide-react";

interface SessionHistoryProps {
  sessions: PracticeSession[];
  maxItems?: number;
}

export function SessionHistory({ sessions, maxItems = 20 }: SessionHistoryProps) {
  const [filterAccuracy, setFilterAccuracy] = useState<"all" | "high" | "medium" | "low">("all");
  const [sortBy, setSortBy] = useState<"date" | "accuracy" | "exercises">("date");
  const [showAll, setShowAll] = useState(false);

  const filteredAndSortedSessions = useMemo(() => {
    let filtered = [...sessions];

    // Filter by accuracy
    if (filterAccuracy !== "all") {
      filtered = filtered.filter((session) => {
        const accuracy = (session.correct_answers / session.exercises_completed) * 100;
        if (filterAccuracy === "high") return accuracy >= 80;
        if (filterAccuracy === "medium") return accuracy >= 50 && accuracy < 80;
        if (filterAccuracy === "low") return accuracy < 50;
        return true;
      });
    }

    // Sort
    filtered.sort((a, b) => {
      if (sortBy === "date") {
        return new Date(b.started_at).getTime() - new Date(a.started_at).getTime();
      } else if (sortBy === "accuracy") {
        const accA = (a.correct_answers / a.exercises_completed) * 100;
        const accB = (b.correct_answers / b.exercises_completed) * 100;
        return accB - accA;
      } else {
        return b.exercises_completed - a.exercises_completed;
      }
    });

    return showAll ? filtered : filtered.slice(0, maxItems);
  }, [sessions, filterAccuracy, sortBy, showAll, maxItems]);

  const stats = useMemo(() => {
    const totalSessions = sessions.length;
    const totalExercises = sessions.reduce((sum, s) => sum + s.exercises_completed, 0);
    const totalCorrect = sessions.reduce((sum, s) => sum + s.correct_answers, 0);
    const totalTime = sessions.reduce((sum, s) => sum + s.total_time, 0);
    const avgAccuracy = totalExercises > 0 ? Math.round((totalCorrect / totalExercises) * 100) : 0;

    return { totalSessions, totalExercises, totalCorrect, totalTime, avgAccuracy };
  }, [sessions]);

  const formatDuration = (seconds: number): string => {
    if (seconds < 60) return `${seconds}s`;
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return remainingSeconds > 0 ? `${minutes}m ${remainingSeconds}s` : `${minutes}m`;
  };

  const getAccuracyBadge = (accuracy: number) => {
    if (accuracy >= 80) {
      return (
        <span className="px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
          Excellent
        </span>
      );
    } else if (accuracy >= 60) {
      return (
        <span className="px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
          Good
        </span>
      );
    } else if (accuracy >= 40) {
      return (
        <span className="px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
          Fair
        </span>
      );
    } else {
      return (
        <span className="px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
          Needs Work
        </span>
      );
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <History className="h-5 w-5" />
          Practice History
        </CardTitle>
        <CardDescription>
          View and analyze your past practice sessions
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Summary Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center p-3 rounded-lg bg-muted/50">
            <p className="text-2xl font-bold text-blue-600">{stats.totalSessions}</p>
            <p className="text-xs text-muted-foreground">Total Sessions</p>
          </div>
          <div className="text-center p-3 rounded-lg bg-muted/50">
            <p className="text-2xl font-bold text-green-600">{stats.totalExercises}</p>
            <p className="text-xs text-muted-foreground">Exercises Done</p>
          </div>
          <div className="text-center p-3 rounded-lg bg-muted/50">
            <p className="text-2xl font-bold text-purple-600">{stats.avgAccuracy}%</p>
            <p className="text-xs text-muted-foreground">Avg Accuracy</p>
          </div>
          <div className="text-center p-3 rounded-lg bg-muted/50">
            <p className="text-2xl font-bold text-orange-600">{formatDuration(stats.totalTime)}</p>
            <p className="text-xs text-muted-foreground">Total Time</p>
          </div>
        </div>

        {/* Filters */}
        <div className="flex flex-col sm:flex-row gap-2">
          <div className="flex items-center gap-2 flex-1">
            <Filter className="h-4 w-4 text-muted-foreground" />
            <select
              value={filterAccuracy}
              onChange={(e) => setFilterAccuracy(e.target.value as any)}
              className="flex-1 text-sm border rounded-md px-3 py-2"
            >
              <option value="all">All Accuracies</option>
              <option value="high">High (80%+)</option>
              <option value="medium">Medium (50-80%)</option>
              <option value="low">Low (&lt;50%)</option>
            </select>
          </div>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as any)}
            className="text-sm border rounded-md px-3 py-2"
          >
            <option value="date">Sort by Date</option>
            <option value="accuracy">Sort by Accuracy</option>
            <option value="exercises">Sort by Exercises</option>
          </select>
        </div>

        {/* Session List */}
        <div className="space-y-3">
          {filteredAndSortedSessions.length === 0 ? (
            <div className="text-center py-8">
              <History className="h-12 w-12 text-muted-foreground mx-auto mb-3" />
              <p className="text-muted-foreground">No sessions found</p>
            </div>
          ) : (
            filteredAndSortedSessions.map((session) => {
              const accuracy = Math.round(
                (session.correct_answers / session.exercises_completed) * 100
              );
              const avgTimePerExercise = Math.round(
                session.total_time / session.exercises_completed
              );

              return (
                <div
                  key={session.id}
                  className="border rounded-lg p-4 hover:bg-muted/50 transition-colors"
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <Calendar className="h-4 w-4 text-muted-foreground" />
                        <span className="font-medium">
                          {format(new Date(session.started_at), "MMM d, yyyy 'at' h:mm a")}
                        </span>
                      </div>
                      <p className="text-sm text-muted-foreground">
                        {formatDistanceToNow(new Date(session.started_at), { addSuffix: true })}
                      </p>
                    </div>
                    {getAccuracyBadge(accuracy)}
                  </div>

                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="flex items-center gap-2">
                      <div className="p-2 rounded-lg bg-blue-50">
                        <TrendingUp className="h-4 w-4 text-blue-600" />
                      </div>
                      <div>
                        <p className="text-xs text-muted-foreground">Accuracy</p>
                        <p className="font-semibold">{accuracy}%</p>
                      </div>
                    </div>

                    <div className="flex items-center gap-2">
                      <div className="p-2 rounded-lg bg-green-50">
                        <CheckCircle2 className="h-4 w-4 text-green-600" />
                      </div>
                      <div>
                        <p className="text-xs text-muted-foreground">Correct</p>
                        <p className="font-semibold">{session.correct_answers}</p>
                      </div>
                    </div>

                    <div className="flex items-center gap-2">
                      <div className="p-2 rounded-lg bg-red-50">
                        <XCircle className="h-4 w-4 text-red-600" />
                      </div>
                      <div>
                        <p className="text-xs text-muted-foreground">Incorrect</p>
                        <p className="font-semibold">
                          {session.exercises_completed - session.correct_answers}
                        </p>
                      </div>
                    </div>

                    <div className="flex items-center gap-2">
                      <div className="p-2 rounded-lg bg-purple-50">
                        <Clock className="h-4 w-4 text-purple-600" />
                      </div>
                      <div>
                        <p className="text-xs text-muted-foreground">Duration</p>
                        <p className="font-semibold">{formatDuration(session.total_time)}</p>
                      </div>
                    </div>
                  </div>

                  <div className="mt-3 pt-3 border-t text-xs text-muted-foreground">
                    <span>
                      {session.exercises_completed} exercises completed • {avgTimePerExercise}s per
                      exercise
                    </span>
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Show More/Less Button */}
        {sessions.length > maxItems && (
          <button
            onClick={() => setShowAll(!showAll)}
            className="w-full py-2 text-sm font-medium text-blue-600 hover:text-blue-700 hover:bg-blue-50 rounded-lg transition-colors"
          >
            {showAll ? "Show Less" : `Show All (${sessions.length - maxItems} more)`}
          </button>
        )}
      </CardContent>
    </Card>
  );
}

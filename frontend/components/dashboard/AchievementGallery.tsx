"use client";

import { useState, useMemo } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Achievement, getTierColor } from "@/lib/gamification";
import {
  Trophy,
  Flame,
  Target,
  BookOpen,
  GraduationCap,
  Zap,
  Moon,
  Sunrise,
  Award,
  Lock,
  Star,
} from "lucide-react";
import { motion } from "framer-motion";

interface AchievementGalleryProps {
  achievements: Achievement[];
  showLocked?: boolean;
}

const iconMap: Record<string, any> = {
  flame: Flame,
  target: Target,
  "book-open": BookOpen,
  "graduation-cap": GraduationCap,
  award: Award,
  trophy: Trophy,
  zap: Zap,
  moon: Moon,
  sunrise: Sunrise,
};

export function AchievementGallery({
  achievements,
  showLocked = true,
}: AchievementGalleryProps) {
  const [filter, setFilter] = useState<"all" | "unlocked" | "locked">("all");
  const [categoryFilter, setCategoryFilter] = useState<Achievement["category"] | "all">("all");

  const filteredAchievements = useMemo(() => {
    return achievements.filter((achievement) => {
      if (filter === "unlocked" && !achievement.unlocked) return false;
      if (filter === "locked" && achievement.unlocked) return false;
      if (categoryFilter !== "all" && achievement.category !== categoryFilter) return false;
      return true;
    });
  }, [achievements, filter, categoryFilter]);

  const stats = useMemo(() => {
    const unlocked = achievements.filter((a) => a.unlocked).length;
    const total = achievements.length;
    const percentage = Math.round((unlocked / total) * 100);
    const byTier = {
      bronze: achievements.filter((a) => a.unlocked && a.tier === "bronze").length,
      silver: achievements.filter((a) => a.unlocked && a.tier === "silver").length,
      gold: achievements.filter((a) => a.unlocked && a.tier === "gold").length,
      platinum: achievements.filter((a) => a.unlocked && a.tier === "platinum").length,
    };
    return { unlocked, total, percentage, byTier };
  }, [achievements]);

  const AchievementCard = ({ achievement }: { achievement: Achievement }) => {
    const Icon = iconMap[achievement.icon] || Trophy;
    const isLocked = !achievement.unlocked;

    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.2 }}
        className={`border rounded-lg p-4 ${
          isLocked ? "opacity-60 bg-muted/30" : "bg-card"
        } hover:shadow-md transition-all`}
      >
        <div className="flex items-start gap-3">
          <div
            className={`p-3 rounded-full ${
              isLocked ? "bg-gray-200 dark:bg-gray-700" : getTierColor(achievement.tier)
            }`}
          >
            {isLocked ? (
              <Lock className="h-6 w-6 text-gray-500" />
            ) : (
              <Icon className="h-6 w-6" />
            )}
          </div>

          <div className="flex-1 space-y-2">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <h4 className="font-semibold">{achievement.name}</h4>
                <span
                  className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                    isLocked
                      ? "bg-gray-200 text-gray-600"
                      : achievement.tier === "bronze"
                      ? "bg-amber-100 text-amber-800"
                      : achievement.tier === "silver"
                      ? "bg-gray-200 text-gray-700"
                      : achievement.tier === "gold"
                      ? "bg-yellow-100 text-yellow-800"
                      : "bg-purple-100 text-purple-800"
                  }`}
                >
                  {achievement.tier}
                </span>
              </div>
              <p className="text-sm text-muted-foreground">{achievement.description}</p>
            </div>

            {!achievement.unlocked && (
              <div className="space-y-1">
                <div className="flex justify-between text-xs text-muted-foreground">
                  <span>Progress</span>
                  <span>
                    {achievement.currentValue} / {achievement.requirement}
                  </span>
                </div>
                <Progress value={achievement.progress} className="h-2" />
              </div>
            )}

            {achievement.unlockedAt && (
              <p className="text-xs text-muted-foreground">
                Unlocked {new Date(achievement.unlockedAt).toLocaleDateString()}
              </p>
            )}
          </div>

          {achievement.unlocked && (
            <Star className="h-5 w-5 text-yellow-500 fill-yellow-500" />
          )}
        </div>
      </motion.div>
    );
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Trophy className="h-5 w-5" />
          Achievements
        </CardTitle>
        <CardDescription>
          Track your accomplishments and unlock new achievements
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Progress Overview */}
        <div className="space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-sm font-medium">Overall Progress</span>
            <span className="text-sm text-muted-foreground">
              {stats.unlocked} / {stats.total} unlocked ({stats.percentage}%)
            </span>
          </div>
          <Progress value={stats.percentage} className="h-3" />

          <div className="grid grid-cols-4 gap-2 pt-2">
            <div className="text-center p-2 rounded-lg bg-amber-50 dark:bg-amber-950/20">
              <p className="text-lg font-bold text-amber-700">{stats.byTier.bronze}</p>
              <p className="text-xs text-amber-600">Bronze</p>
            </div>
            <div className="text-center p-2 rounded-lg bg-gray-50 dark:bg-gray-800">
              <p className="text-lg font-bold text-gray-700 dark:text-gray-300">
                {stats.byTier.silver}
              </p>
              <p className="text-xs text-gray-600 dark:text-gray-400">Silver</p>
            </div>
            <div className="text-center p-2 rounded-lg bg-yellow-50 dark:bg-yellow-950/20">
              <p className="text-lg font-bold text-yellow-700">{stats.byTier.gold}</p>
              <p className="text-xs text-yellow-600">Gold</p>
            </div>
            <div className="text-center p-2 rounded-lg bg-purple-50 dark:bg-purple-950/20">
              <p className="text-lg font-bold text-purple-700">{stats.byTier.platinum}</p>
              <p className="text-xs text-purple-600">Platinum</p>
            </div>
          </div>
        </div>

        {/* Filters */}
        <div className="flex flex-col sm:flex-row gap-2">
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value as any)}
            className="flex-1 text-sm border rounded-md px-3 py-2"
          >
            <option value="all">All Achievements</option>
            <option value="unlocked">Unlocked Only</option>
            <option value="locked">Locked Only</option>
          </select>
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value as any)}
            className="flex-1 text-sm border rounded-md px-3 py-2"
          >
            <option value="all">All Categories</option>
            <option value="streak">Streak</option>
            <option value="accuracy">Accuracy</option>
            <option value="volume">Volume</option>
            <option value="mastery">Mastery</option>
            <option value="special">Special</option>
          </select>
        </div>

        {/* Achievements Grid */}
        <div className="space-y-3">
          {filteredAchievements.length === 0 ? (
            <div className="text-center py-8">
              <Trophy className="h-12 w-12 text-muted-foreground mx-auto mb-3" />
              <p className="text-muted-foreground">No achievements found</p>
            </div>
          ) : (
            filteredAchievements.map((achievement) => (
              <AchievementCard key={achievement.id} achievement={achievement} />
            ))
          )}
        </div>

        {/* Motivation Message */}
        {stats.unlocked < stats.total && (
          <div className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-950/20 dark:to-purple-950/20 rounded-lg p-4 border border-blue-200 dark:border-blue-800">
            <div className="flex items-start gap-3">
              <Award className="h-5 w-5 text-blue-600 flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-medium text-blue-900 dark:text-blue-100">
                  Keep Going!
                </p>
                <p className="text-sm text-blue-700 dark:text-blue-200">
                  You have {stats.total - stats.unlocked} more achievement
                  {stats.total - stats.unlocked !== 1 ? "s" : ""} to unlock. Keep
                  practicing to earn them all!
                </p>
              </div>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

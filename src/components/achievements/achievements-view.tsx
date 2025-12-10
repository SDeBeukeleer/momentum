"use client";

import { motion } from "framer-motion";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Trophy,
  Flame,
  Target,
  Zap,
  Star,
  Crown,
  Medal,
  Award,
  Lock,
} from "lucide-react";
import type { Habit, HabitCompletion, ActivityLog, WeightLog } from "@prisma/client";

interface AchievementsViewProps {
  habits: (Habit & { completions: HabitCompletion[] })[];
  activities: ActivityLog[];
  weightLogs: WeightLog[];
}

// Badge definitions
const badgeDefinitions = [
  {
    id: "first-habit",
    name: "First Step",
    description: "Create your first habit",
    icon: Target,
    color: "from-blue-400 to-blue-600",
    check: (data: AchievementsViewProps) => data.habits.length >= 1,
  },
  {
    id: "3-day-streak",
    name: "Getting Started",
    description: "Achieve a 3-day streak",
    icon: Flame,
    color: "from-orange-400 to-orange-600",
    check: (data: AchievementsViewProps) =>
      data.habits.some((h) => h.currentStreak >= 3 || h.longestStreak >= 3),
  },
  {
    id: "7-day-streak",
    name: "Week Warrior",
    description: "Achieve a 7-day streak",
    icon: Flame,
    color: "from-orange-500 to-red-500",
    check: (data: AchievementsViewProps) =>
      data.habits.some((h) => h.currentStreak >= 7 || h.longestStreak >= 7),
  },
  {
    id: "14-day-streak",
    name: "Two Week Champion",
    description: "Achieve a 14-day streak",
    icon: Zap,
    color: "from-yellow-400 to-amber-500",
    check: (data: AchievementsViewProps) =>
      data.habits.some((h) => h.currentStreak >= 14 || h.longestStreak >= 14),
  },
  {
    id: "30-day-streak",
    name: "Monthly Master",
    description: "Achieve a 30-day streak",
    icon: Crown,
    color: "from-purple-500 to-pink-500",
    check: (data: AchievementsViewProps) =>
      data.habits.some((h) => h.currentStreak >= 30 || h.longestStreak >= 30),
  },
  {
    id: "first-credit",
    name: "Credit Earned",
    description: "Earn your first skip credit",
    icon: Star,
    color: "from-amber-400 to-yellow-500",
    check: (data: AchievementsViewProps) =>
      data.habits.some((h) => h.currentCredits >= 1),
  },
  {
    id: "5-credits",
    name: "Credit Collector",
    description: "Accumulate 5 credits on any habit",
    icon: Medal,
    color: "from-slate-400 to-slate-600",
    check: (data: AchievementsViewProps) =>
      data.habits.some((h) => h.currentCredits >= 5),
  },
  {
    id: "first-activity",
    name: "Active Life",
    description: "Log your first activity",
    icon: Award,
    color: "from-green-400 to-emerald-500",
    check: (data: AchievementsViewProps) => data.activities.length >= 1,
  },
  {
    id: "10-activities",
    name: "Fitness Fan",
    description: "Log 10 activities",
    icon: Trophy,
    color: "from-green-500 to-teal-500",
    check: (data: AchievementsViewProps) => data.activities.length >= 10,
  },
  {
    id: "first-weight",
    name: "Scale Starter",
    description: "Log your first weight entry",
    icon: Target,
    color: "from-cyan-400 to-blue-500",
    check: (data: AchievementsViewProps) => data.weightLogs.length >= 1,
  },
  {
    id: "30-weights",
    name: "Consistent Tracker",
    description: "Log 30 weight entries",
    icon: Trophy,
    color: "from-indigo-500 to-purple-600",
    check: (data: AchievementsViewProps) => data.weightLogs.length >= 30,
  },
  {
    id: "5-habits",
    name: "Habit Builder",
    description: "Create 5 habits",
    icon: Target,
    color: "from-pink-400 to-rose-500",
    check: (data: AchievementsViewProps) => data.habits.length >= 5,
  },
];

export function AchievementsView({
  habits,
  activities,
  weightLogs,
}: AchievementsViewProps) {
  const data = { habits, activities, weightLogs };

  const earnedBadges = badgeDefinitions.filter((badge) => badge.check(data));
  const lockedBadges = badgeDefinitions.filter((badge) => !badge.check(data));

  // Calculate stats
  const totalCompletions = habits.reduce(
    (sum, h) => sum + h.completions.length,
    0
  );
  const longestStreak = Math.max(...habits.map((h) => h.longestStreak), 0);
  const totalCredits = habits.reduce((sum, h) => sum + h.currentCredits, 0);
  const totalActivities = activities.length;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-3">
        <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-amber-500 to-orange-500 flex items-center justify-center">
          <Trophy className="h-6 w-6 text-white" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Achievements</h1>
          <p className="text-slate-600">Your badges and personal records</p>
        </div>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card className="p-4 text-center">
          <div className="text-3xl font-bold text-indigo-600">
            {earnedBadges.length}
          </div>
          <div className="text-sm text-slate-500">Badges Earned</div>
        </Card>
        <Card className="p-4 text-center">
          <div className="text-3xl font-bold text-orange-600">{longestStreak}</div>
          <div className="text-sm text-slate-500">Best Streak</div>
        </Card>
        <Card className="p-4 text-center">
          <div className="text-3xl font-bold text-green-600">
            {totalCompletions}
          </div>
          <div className="text-sm text-slate-500">Total Completions</div>
        </Card>
        <Card className="p-4 text-center">
          <div className="text-3xl font-bold text-amber-600">{totalCredits}</div>
          <div className="text-sm text-slate-500">Credits Earned</div>
        </Card>
      </div>

      {/* Earned Badges */}
      <div>
        <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <Trophy className="h-5 w-5 text-amber-500" />
          Earned Badges ({earnedBadges.length})
        </h2>
        {earnedBadges.length === 0 ? (
          <Card className="p-8 text-center">
            <p className="text-slate-500">
              No badges earned yet. Keep tracking your habits to unlock achievements!
            </p>
          </Card>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {earnedBadges.map((badge, index) => (
              <motion.div
                key={badge.id}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.1 }}
              >
                <Card className="p-4 text-center hover:shadow-lg transition-shadow">
                  <div
                    className={`h-16 w-16 mx-auto rounded-full bg-gradient-to-br ${badge.color} flex items-center justify-center mb-3 shadow-lg`}
                  >
                    <badge.icon className="h-8 w-8 text-white" />
                  </div>
                  <h3 className="font-semibold text-slate-900">{badge.name}</h3>
                  <p className="text-xs text-slate-500 mt-1">
                    {badge.description}
                  </p>
                  <Badge className="mt-2 bg-green-100 text-green-700">
                    Unlocked
                  </Badge>
                </Card>
              </motion.div>
            ))}
          </div>
        )}
      </div>

      {/* Locked Badges */}
      <div>
        <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <Lock className="h-5 w-5 text-slate-400" />
          Locked Badges ({lockedBadges.length})
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {lockedBadges.map((badge) => (
            <Card
              key={badge.id}
              className="p-4 text-center opacity-60 bg-slate-50"
            >
              <div className="h-16 w-16 mx-auto rounded-full bg-slate-200 flex items-center justify-center mb-3">
                <badge.icon className="h-8 w-8 text-slate-400" />
              </div>
              <h3 className="font-semibold text-slate-600">{badge.name}</h3>
              <p className="text-xs text-slate-400 mt-1">{badge.description}</p>
              <Badge variant="secondary" className="mt-2">
                Locked
              </Badge>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}

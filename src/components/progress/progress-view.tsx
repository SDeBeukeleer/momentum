"use client";

import { motion } from "framer-motion";
import { Card } from "@/components/ui/card";
import {
  BarChart3,
  Target,
  Flame,
  Calendar,
  Trophy,
  Zap,
  Star,
  Crown,
  Medal,
  Lock,
} from "lucide-react";
import { HabitHeatmap } from "@/components/dashboard/habit-heatmap";
import { ShareCard } from "@/components/share/share-card";
import type { Habit, HabitCompletion, WeightLog } from "@prisma/client";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  CartesianGrid,
} from "recharts";

interface ProgressViewProps {
  habits: (Habit & { completions: HabitCompletion[] })[];
  weightLogs: WeightLog[];
}

// Badge definitions - indigo theme colors
const badgeDefinitions = [
  {
    id: "first-habit",
    name: "First Step",
    description: "Create your first habit",
    icon: Target,
    color: "from-indigo-500 to-indigo-600",
    check: (data: ProgressViewProps) => data.habits.length >= 1,
  },
  {
    id: "3-day-streak",
    name: "Getting Started",
    description: "Achieve a 3-day streak",
    icon: Flame,
    color: "from-orange-500 to-amber-500",
    check: (data: ProgressViewProps) =>
      data.habits.some((h) => h.currentStreak >= 3 || h.longestStreak >= 3),
  },
  {
    id: "7-day-streak",
    name: "Week Warrior",
    description: "Achieve a 7-day streak",
    icon: Flame,
    color: "from-rose-500 to-pink-500",
    check: (data: ProgressViewProps) =>
      data.habits.some((h) => h.currentStreak >= 7 || h.longestStreak >= 7),
  },
  {
    id: "14-day-streak",
    name: "Two Week Champion",
    description: "Achieve a 14-day streak",
    icon: Zap,
    color: "from-purple-500 to-violet-500",
    check: (data: ProgressViewProps) =>
      data.habits.some((h) => h.currentStreak >= 14 || h.longestStreak >= 14),
  },
  {
    id: "30-day-streak",
    name: "Monthly Master",
    description: "Achieve a 30-day streak",
    icon: Crown,
    color: "from-amber-400 to-yellow-500",
    check: (data: ProgressViewProps) =>
      data.habits.some((h) => h.currentStreak >= 30 || h.longestStreak >= 30),
  },
  {
    id: "first-credit",
    name: "Credit Earned",
    description: "Earn your first skip credit",
    icon: Star,
    color: "from-emerald-500 to-teal-500",
    check: (data: ProgressViewProps) =>
      data.habits.some((h) => h.currentCredits >= 1),
  },
  {
    id: "5-credits",
    name: "Credit Collector",
    description: "Accumulate 5 credits on any habit",
    icon: Medal,
    color: "from-slate-400 to-slate-500",
    check: (data: ProgressViewProps) =>
      data.habits.some((h) => h.currentCredits >= 5),
  },
  {
    id: "first-weight",
    name: "Scale Starter",
    description: "Log your first weight entry",
    icon: Target,
    color: "from-cyan-500 to-blue-500",
    check: (data: ProgressViewProps) => data.weightLogs.length >= 1,
  },
  {
    id: "30-weights",
    name: "Consistent Tracker",
    description: "Log 30 weight entries",
    icon: Trophy,
    color: "from-indigo-600 to-purple-600",
    check: (data: ProgressViewProps) => data.weightLogs.length >= 30,
  },
  {
    id: "5-habits",
    name: "Habit Builder",
    description: "Create 5 habits",
    icon: Target,
    color: "from-indigo-500 to-violet-500",
    check: (data: ProgressViewProps) => data.habits.length >= 5,
  },
];

// Get day of week stats
function getDayOfWeekStats(habits: (Habit & { completions: HabitCompletion[] })[]) {
  const dayStats = Array(7)
    .fill(0)
    .map((_, i) => ({
      day: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"][i],
      completions: 0,
    }));

  habits.forEach((habit) => {
    habit.completions.forEach((completion) => {
      const d = new Date(completion.date);
      dayStats[d.getUTCDay()].completions++;
    });
  });

  // Reorder to start from Monday
  return [...dayStats.slice(1), dayStats[0]];
}

// Get weekly trend (last 8 weeks)
function getWeeklyTrend(habits: (Habit & { completions: HabitCompletion[] })[]) {
  const weeks: { week: string; completions: number }[] = [];
  const now = new Date();

  for (let i = 7; i >= 0; i--) {
    const weekStart = new Date(now);
    weekStart.setDate(now.getDate() - i * 7 - now.getDay() + 1);
    const weekEnd = new Date(weekStart);
    weekEnd.setDate(weekStart.getDate() + 6);

    let completions = 0;
    habits.forEach((habit) => {
      habit.completions.forEach((c) => {
        const d = new Date(c.date);
        if (d >= weekStart && d <= weekEnd) {
          completions++;
        }
      });
    });

    weeks.push({
      week: weekStart.toLocaleDateString("default", {
        month: "short",
        day: "numeric",
      }),
      completions,
    });
  }

  return weeks;
}

// Calculate streaks
function calculateStreakStats(habits: (Habit & { completions: HabitCompletion[] })[]) {
  const currentStreaks = habits.map((h) => h.currentStreak);
  const longestStreaks = habits.map((h) => h.longestStreak);

  return {
    totalCurrentStreak: currentStreaks.reduce((a, b) => a + b, 0),
    maxCurrentStreak: Math.max(...currentStreaks, 0),
    maxLongestStreak: Math.max(...longestStreaks, 0),
    avgCurrentStreak: habits.length
      ? (currentStreaks.reduce((a, b) => a + b, 0) / habits.length).toFixed(1)
      : 0,
  };
}

export function ProgressView({ habits, weightLogs }: ProgressViewProps) {
  const data = { habits, weightLogs };
  const dayStats = getDayOfWeekStats(habits);
  const weeklyTrend = getWeeklyTrend(habits);
  const streakStats = calculateStreakStats(habits);

  // Total stats
  const totalCompletions = habits.reduce(
    (sum, h) => sum + h.completions.length,
    0
  );

  // Weight trend (last 30 entries)
  const weightTrend = weightLogs
    .slice(0, 30)
    .reverse()
    .map((w) => ({
      date: new Date(w.date).toLocaleDateString("default", {
        month: "short",
        day: "numeric",
      }),
      weight: w.weight,
    }));

  // Badges
  const earnedBadges = badgeDefinitions.filter((badge) => badge.check(data));
  const lockedBadges = badgeDefinitions.filter((badge) => !badge.check(data));

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="h-12 w-12 rounded-xl bg-indigo-100 flex items-center justify-center">
            <BarChart3 className="h-6 w-6 text-indigo-600" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-slate-900" style={{ fontFamily: 'var(--font-fraunces)' }}>Progress</h1>
            <p className="text-slate-500">Your stats and achievements</p>
          </div>
        </div>
        <ShareCard habits={habits} />
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card className="p-4 text-center">
          <Target className="h-5 w-5 mx-auto text-indigo-600 mb-2" />
          <div className="text-2xl font-bold text-slate-900">{habits.length}</div>
          <div className="text-xs text-slate-500">Active Habits</div>
        </Card>
        <Card className="p-4 text-center">
          <Calendar className="h-5 w-5 mx-auto text-indigo-600 mb-2" />
          <div className="text-2xl font-bold text-slate-900">
            {totalCompletions}
          </div>
          <div className="text-xs text-slate-500">Total Completions</div>
        </Card>
        <Card className="p-4 text-center">
          <Flame className="h-5 w-5 mx-auto text-amber-500 mb-2" />
          <div className="text-2xl font-bold text-slate-900">
            {streakStats.maxLongestStreak}
          </div>
          <div className="text-xs text-slate-500">Best Streak Ever</div>
        </Card>
        <Card className="p-4 text-center">
          <Trophy className="h-5 w-5 mx-auto text-amber-500 mb-2" />
          <div className="text-2xl font-bold text-slate-900">{earnedBadges.length}</div>
          <div className="text-xs text-slate-500">Badges Earned</div>
        </Card>
      </div>

      {/* Heatmap */}
      <HabitHeatmap habits={habits} />

      {/* Achievements Section */}
      <Card className="p-4">
        <h3 className="font-semibold mb-4 flex items-center gap-2 text-slate-900">
          <Trophy className="h-5 w-5 text-amber-500" />
          Achievements ({earnedBadges.length}/{badgeDefinitions.length})
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
          {earnedBadges.map((badge, index) => (
            <motion.div
              key={badge.id}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.05 }}
              className="text-center p-3 rounded-xl bg-slate-50 border border-slate-200"
            >
              <div
                className={`h-10 w-10 mx-auto rounded-full bg-gradient-to-br ${badge.color} flex items-center justify-center mb-2 shadow-lg`}
              >
                <badge.icon className="h-5 w-5 text-white" />
              </div>
              <p className="text-xs font-medium text-slate-900">{badge.name}</p>
            </motion.div>
          ))}
          {lockedBadges.slice(0, 5 - earnedBadges.length).map((badge) => (
            <div
              key={badge.id}
              className="text-center p-3 rounded-xl bg-slate-100 opacity-50"
            >
              <div className="h-10 w-10 mx-auto rounded-full bg-slate-200 flex items-center justify-center mb-2">
                <Lock className="h-4 w-4 text-slate-400" />
              </div>
              <p className="text-xs font-medium text-slate-400">{badge.name}</p>
            </div>
          ))}
        </div>
        {lockedBadges.length > 0 && (
          <p className="text-xs text-slate-500 mt-3 text-center">
            {lockedBadges.length} more badge{lockedBadges.length > 1 ? 's' : ''} to unlock
          </p>
        )}
      </Card>

      {/* Weekly Trend */}
      <Card className="p-4">
        <h3 className="font-semibold mb-4 text-slate-900">Weekly Trend</h3>
        <div className="h-48">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={weeklyTrend}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" opacity={0.8} />
              <XAxis dataKey="week" fontSize={12} stroke="#94a3b8" />
              <YAxis fontSize={12} stroke="#94a3b8" />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#ffffff",
                  border: "1px solid #e2e8f0",
                  borderRadius: "12px",
                  color: "#1e293b",
                  boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
                }}
              />
              <Bar
                dataKey="completions"
                fill="#4f46e5"
                radius={[4, 4, 0, 0]}
                name="Completions"
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </Card>

      {/* Day of Week Distribution */}
      <Card className="p-4">
        <h3 className="font-semibold mb-4 text-slate-900">Best Days</h3>
        <div className="h-48">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={dayStats} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" opacity={0.8} />
              <XAxis type="number" fontSize={12} stroke="#94a3b8" />
              <YAxis
                dataKey="day"
                type="category"
                fontSize={12}
                stroke="#94a3b8"
                width={40}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#ffffff",
                  border: "1px solid #e2e8f0",
                  borderRadius: "12px",
                  color: "#1e293b",
                  boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
                }}
              />
              <Bar
                dataKey="completions"
                fill="#6366f1"
                radius={[0, 4, 4, 0]}
                name="Completions"
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </Card>

      {/* Weight Trend */}
      {weightTrend.length > 1 && (
        <Card className="p-4">
          <h3 className="font-semibold mb-4 text-slate-900">Weight Trend</h3>
          <div className="h-48">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={weightTrend}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" opacity={0.8} />
                <XAxis dataKey="date" fontSize={12} stroke="#94a3b8" />
                <YAxis
                  fontSize={12}
                  stroke="#94a3b8"
                  domain={["dataMin - 1", "dataMax + 1"]}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#ffffff",
                    border: "1px solid #e2e8f0",
                    borderRadius: "12px",
                    color: "#1e293b",
                    boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
                  }}
                />
                <Line
                  type="monotone"
                  dataKey="weight"
                  stroke="#4f46e5"
                  strokeWidth={2}
                  dot={{ fill: "#4f46e5", strokeWidth: 2 }}
                  name="Weight (kg)"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Card>
      )}

      {/* Streak Stats */}
      <Card className="p-4">
        <h3 className="font-semibold mb-4 flex items-center gap-2 text-slate-900">
          <Flame className="h-5 w-5 text-amber-500" />
          Streak Statistics
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold text-indigo-600">
              {streakStats.maxCurrentStreak}
            </div>
            <div className="text-xs text-slate-500">Best Current</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-amber-500">
              {streakStats.maxLongestStreak}
            </div>
            <div className="text-xs text-slate-500">All-Time Best</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-indigo-600">
              {streakStats.totalCurrentStreak}
            </div>
            <div className="text-xs text-slate-500">Combined Streaks</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-amber-500">
              {streakStats.avgCurrentStreak}
            </div>
            <div className="text-xs text-slate-500">Avg Streak</div>
          </div>
        </div>
      </Card>
    </div>
  );
}

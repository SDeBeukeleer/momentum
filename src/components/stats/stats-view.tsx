"use client";

import { Card } from "@/components/ui/card";
import {
  BarChart3,
  TrendingUp,
  Target,
  Flame,
  Calendar,
  Activity,
} from "lucide-react";
import { HabitHeatmap } from "@/components/dashboard/habit-heatmap";
import { ShareCard } from "@/components/share/share-card";
import type { Habit, HabitCompletion, ActivityLog, WeightLog } from "@prisma/client";
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

interface StatsViewProps {
  habits: (Habit & { completions: HabitCompletion[] })[];
  activities: ActivityLog[];
  weightLogs: WeightLog[];
}

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

export function StatsView({ habits, activities, weightLogs }: StatsViewProps) {
  const dayStats = getDayOfWeekStats(habits);
  const weeklyTrend = getWeeklyTrend(habits);
  const streakStats = calculateStreakStats(habits);

  // Total stats
  const totalCompletions = habits.reduce(
    (sum, h) => sum + h.completions.length,
    0
  );
  const totalCredits = habits.reduce((sum, h) => sum + h.currentCredits, 0);
  const totalActivities = activities.length;
  const totalActivityMinutes = activities.reduce(
    (sum, a) => sum + (a.duration || 0),
    0
  );
  const totalActivityKm = activities.reduce(
    (sum, a) => sum + (a.distance || 0),
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

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center">
            <BarChart3 className="h-6 w-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-slate-900">Statistics</h1>
            <p className="text-slate-600">Your progress at a glance</p>
          </div>
        </div>
        <ShareCard habits={habits} />
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card className="p-4 text-center">
          <Target className="h-5 w-5 mx-auto text-indigo-500 mb-2" />
          <div className="text-2xl font-bold text-slate-900">{habits.length}</div>
          <div className="text-xs text-slate-500">Active Habits</div>
        </Card>
        <Card className="p-4 text-center">
          <Calendar className="h-5 w-5 mx-auto text-green-500 mb-2" />
          <div className="text-2xl font-bold text-slate-900">
            {totalCompletions}
          </div>
          <div className="text-xs text-slate-500">Total Completions</div>
        </Card>
        <Card className="p-4 text-center">
          <Flame className="h-5 w-5 mx-auto text-orange-500 mb-2" />
          <div className="text-2xl font-bold text-slate-900">
            {streakStats.maxLongestStreak}
          </div>
          <div className="text-xs text-slate-500">Best Streak Ever</div>
        </Card>
        <Card className="p-4 text-center">
          <TrendingUp className="h-5 w-5 mx-auto text-amber-500 mb-2" />
          <div className="text-2xl font-bold text-slate-900">{totalCredits}</div>
          <div className="text-xs text-slate-500">Total Credits</div>
        </Card>
      </div>

      {/* Heatmap */}
      <HabitHeatmap habits={habits} />

      {/* Weekly Trend */}
      <Card className="p-4">
        <h3 className="font-semibold mb-4">Weekly Trend</h3>
        <div className="h-48">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={weeklyTrend}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="week" fontSize={12} stroke="#94a3b8" />
              <YAxis fontSize={12} stroke="#94a3b8" />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#fff",
                  border: "1px solid #e2e8f0",
                  borderRadius: "8px",
                }}
              />
              <Bar
                dataKey="completions"
                fill="#6366f1"
                radius={[4, 4, 0, 0]}
                name="Completions"
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </Card>

      {/* Day of Week Distribution */}
      <Card className="p-4">
        <h3 className="font-semibold mb-4">Best Days</h3>
        <div className="h-48">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={dayStats} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
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
                  backgroundColor: "#fff",
                  border: "1px solid #e2e8f0",
                  borderRadius: "8px",
                }}
              />
              <Bar
                dataKey="completions"
                fill="#10b981"
                radius={[0, 4, 4, 0]}
                name="Completions"
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </Card>

      {/* Activity Stats */}
      {totalActivities > 0 && (
        <Card className="p-4">
          <h3 className="font-semibold mb-4 flex items-center gap-2">
            <Activity className="h-5 w-5 text-orange-500" />
            Activity Summary
          </h3>
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <div className="text-2xl font-bold text-slate-900">
                {totalActivities}
              </div>
              <div className="text-xs text-slate-500">Workouts</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-slate-900">
                {Math.round(totalActivityMinutes / 60)}h
              </div>
              <div className="text-xs text-slate-500">Total Time</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-slate-900">
                {totalActivityKm.toFixed(1)}km
              </div>
              <div className="text-xs text-slate-500">Distance</div>
            </div>
          </div>
        </Card>
      )}

      {/* Weight Trend */}
      {weightTrend.length > 1 && (
        <Card className="p-4">
          <h3 className="font-semibold mb-4">Weight Trend</h3>
          <div className="h-48">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={weightTrend}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="date" fontSize={12} stroke="#94a3b8" />
                <YAxis
                  fontSize={12}
                  stroke="#94a3b8"
                  domain={["dataMin - 1", "dataMax + 1"]}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#fff",
                    border: "1px solid #e2e8f0",
                    borderRadius: "8px",
                  }}
                />
                <Line
                  type="monotone"
                  dataKey="weight"
                  stroke="#6366f1"
                  strokeWidth={2}
                  dot={{ fill: "#6366f1", strokeWidth: 2 }}
                  name="Weight (kg)"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Card>
      )}

      {/* Streak Stats */}
      <Card className="p-4">
        <h3 className="font-semibold mb-4 flex items-center gap-2">
          <Flame className="h-5 w-5 text-orange-500" />
          Streak Statistics
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold text-orange-600">
              {streakStats.maxCurrentStreak}
            </div>
            <div className="text-xs text-slate-500">Best Current</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-amber-600">
              {streakStats.maxLongestStreak}
            </div>
            <div className="text-xs text-slate-500">All-Time Best</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-green-600">
              {streakStats.totalCurrentStreak}
            </div>
            <div className="text-xs text-slate-500">Combined Streaks</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-indigo-600">
              {streakStats.avgCurrentStreak}
            </div>
            <div className="text-xs text-slate-500">Avg Streak</div>
          </div>
        </div>
      </Card>
    </div>
  );
}

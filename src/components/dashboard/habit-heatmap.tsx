"use client";

import { motion } from "framer-motion";
import { Card } from "@/components/ui/card";
import type { Habit, HabitCompletion } from "@prisma/client";

interface HabitHeatmapProps {
  habits: (Habit & { completions: HabitCompletion[] })[];
}

// Get last N days including today
function getLastNDays(n: number): Date[] {
  const days: Date[] = [];
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  for (let i = n - 1; i >= 0; i--) {
    const date = new Date(today);
    date.setDate(today.getDate() - i);
    days.push(date);
  }
  return days;
}

// Format date as key for comparison
function dateKey(date: Date): string {
  return `${date.getFullYear()}-${date.getMonth()}-${date.getDate()}`;
}

// Get intensity level (0-4) based on completion count
function getIntensity(count: number, max: number): number {
  if (count === 0) return 0;
  if (max <= 1) return 4;
  const ratio = count / max;
  if (ratio >= 0.75) return 4;
  if (ratio >= 0.5) return 3;
  if (ratio >= 0.25) return 2;
  return 1;
}

const intensityColors = [
  "bg-slate-100", // 0 - no completions
  "bg-emerald-200", // 1 - low
  "bg-emerald-400", // 2 - medium-low
  "bg-emerald-500", // 3 - medium-high
  "bg-emerald-600", // 4 - high
];

export function HabitHeatmap({ habits }: HabitHeatmapProps) {
  const days = getLastNDays(84); // 12 weeks
  const maxHabits = habits.length;

  // Build completion map: date -> count of completed habits
  const completionMap = new Map<string, number>();

  habits.forEach((habit) => {
    habit.completions.forEach((completion) => {
      const d = new Date(completion.date);
      const key = `${d.getUTCFullYear()}-${d.getUTCMonth()}-${d.getUTCDate()}`;
      completionMap.set(key, (completionMap.get(key) || 0) + 1);
    });
  });

  // Group days by week
  const weeks: Date[][] = [];
  for (let i = 0; i < days.length; i += 7) {
    weeks.push(days.slice(i, i + 7));
  }

  // Calculate stats
  const totalCompletions = Array.from(completionMap.values()).reduce(
    (sum, count) => sum + count,
    0
  );
  const activeDays = completionMap.size;
  const avgPerDay =
    activeDays > 0 ? (totalCompletions / activeDays).toFixed(1) : "0";

  return (
    <Card className="p-4">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-slate-900">Activity Heatmap</h3>
        <div className="flex items-center gap-4 text-sm text-slate-500">
          <span>{totalCompletions} completions</span>
          <span>{activeDays} active days</span>
          <span>{avgPerDay}/day avg</span>
        </div>
      </div>

      {/* Month labels */}
      <div className="flex gap-1 mb-2 ml-10 text-xs text-slate-500">
        {weeks.map((week, i) => {
          const firstDay = week[0];
          // Show month label at the start of each month
          const showMonth =
            i === 0 || firstDay.getDate() <= 7;
          return (
            <div key={i} className="w-3 text-center">
              {showMonth
                ? firstDay.toLocaleString("default", { month: "short" }).slice(0, 3)
                : ""}
            </div>
          );
        })}
      </div>

      {/* Heatmap grid */}
      <div className="flex gap-1">
        {/* Day labels - all 7 days */}
        <div className="flex flex-col gap-1 text-xs text-slate-500 pr-2 w-6">
          <span className="h-3 leading-3">Mon</span>
          <span className="h-3 leading-3">Tue</span>
          <span className="h-3 leading-3">Wed</span>
          <span className="h-3 leading-3">Thu</span>
          <span className="h-3 leading-3">Fri</span>
          <span className="h-3 leading-3">Sat</span>
          <span className="h-3 leading-3">Sun</span>
        </div>

        {/* Weeks */}
        <div className="flex gap-1">
          {weeks.map((week, weekIndex) => (
            <div key={weekIndex} className="flex flex-col gap-1">
              {week.map((day, dayIndex) => {
                const key = dateKey(day);
                const count = completionMap.get(key) || 0;
                const intensity = getIntensity(count, maxHabits);
                const isToday =
                  dateKey(day) === dateKey(new Date());

                return (
                  <motion.div
                    key={day.toISOString()}
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{
                      delay: (weekIndex * 7 + dayIndex) * 0.005,
                      type: "spring",
                      stiffness: 300,
                    }}
                    className={`w-3 h-3 rounded-sm ${intensityColors[intensity]} ${
                      isToday ? "ring-2 ring-indigo-500 ring-offset-1" : ""
                    }`}
                    title={`${day.toLocaleDateString()}: ${count} habit${count !== 1 ? "s" : ""} completed`}
                  />
                );
              })}
            </div>
          ))}
        </div>
      </div>

      {/* Legend */}
      <div className="flex items-center justify-end gap-2 mt-3">
        <span className="text-xs text-slate-400">Less</span>
        {intensityColors.map((color, i) => (
          <div
            key={i}
            className={`w-3 h-3 rounded-sm ${color}`}
            title={`Level ${i}`}
          />
        ))}
        <span className="text-xs text-slate-400">More</span>
      </div>
    </Card>
  );
}

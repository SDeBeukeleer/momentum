"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { toast } from "sonner";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  ArrowLeft,
  Flame,
  Coins,
  Trophy,
  Calendar,
  Check,
  Pencil,
  Trash2,
} from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import type { Habit, HabitCompletion } from "@prisma/client";

type HabitWithCompletions = Habit & {
  completions: HabitCompletion[];
};

interface HabitDetailProps {
  habit: HabitWithCompletions;
}

const SUGGESTED_EMOJIS = [
  "🎯", "💪", "📚", "🧘", "💧", "😴", "🥗", "💻", "✍️", "🎵",
  "🏃", "🚴", "🏊", "🧘‍♀️", "🏋️", "🌱", "🎨", "🎸", "📝", "🧠",
];

// Legacy icon mapping for backward compatibility with old data
const legacyIconMap: Record<string, string> = {
  target: "🎯",
  exercise: "💪",
  book: "📚",
  meditation: "🧘",
  water: "💧",
  sleep: "😴",
  healthy: "🥗",
  coding: "💻",
  writing: "✍️",
  music: "🎵",
  running: "🏃",
  cycling: "🚴",
  swimming: "🏊",
  yoga: "🧘‍♀️",
  weight: "🏋️",
  default: "✨",
};

// Get display emoji - handles both legacy icon keys and direct emojis
function getDisplayIcon(icon: string): string {
  return legacyIconMap[icon] || icon || "✨";
}

function getMonthDays(year: number, month: number) {
  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);
  const days = [];

  // Add empty slots for days before first day of month
  // Convert Sunday=0 to Monday=0 format: (day + 6) % 7
  const firstDayOfWeek = (firstDay.getDay() + 6) % 7;
  for (let i = 0; i < firstDayOfWeek; i++) {
    days.push(null);
  }

  // Add all days of the month
  for (let i = 1; i <= lastDay.getDate(); i++) {
    days.push(new Date(year, month, i));
  }

  return days;
}

function isSameDay(d1: Date, d2: Date) {
  // Compare using UTC for d1 (from DB) and local for d2 (calendar)
  return (
    d1.getUTCFullYear() === d2.getFullYear() &&
    d1.getUTCMonth() === d2.getMonth() &&
    d1.getUTCDate() === d2.getDate()
  );
}

export function HabitDetail({ habit: initialHabit }: HabitDetailProps) {
  const router = useRouter();
  const [habit, setHabit] = useState(initialHabit);
  const [currentMonth, setCurrentMonth] = useState(new Date());
  const [loading, setLoading] = useState(false);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [editForm, setEditForm] = useState({
    name: initialHabit.name,
    icon: initialHabit.icon,
    color: initialHabit.color,
  });

  // Automatically recalculate streak and credits on mount
  useEffect(() => {
    const recalculate = async () => {
      try {
        const res = await fetch(`/api/habits/${initialHabit.id}/recalculate`, {
          method: "POST",
        });

        if (res.ok) {
          const data = await res.json();
          setHabit((prev) => ({ ...prev, ...data.habit }));
        }
      } catch {
        // Silently fail - data will just show cached values
      }
    };

    recalculate();
  }, [initialHabit.id]);

  const icon = getDisplayIcon(habit.icon);
  const [customEmoji, setCustomEmoji] = useState("");

  const monthDays = getMonthDays(
    currentMonth.getFullYear(),
    currentMonth.getMonth()
  );

  // Use UTC dates to avoid timezone issues
  const completionDates = new Set(
    habit.completions.map((c) => {
      const d = new Date(c.date);
      // Use UTC to match how we store dates
      return `${d.getUTCFullYear()}-${d.getUTCMonth()}-${d.getUTCDate()}`;
    })
  );

  const isCompleted = (date: Date) => {
    // Compare using local date parts since calendar shows local dates
    return completionDates.has(
      `${date.getFullYear()}-${date.getMonth()}-${date.getDate()}`
    );
  };

  const today = new Date();
  today.setHours(0, 0, 0, 0);

  // Format date as YYYY-MM-DD in local timezone (not UTC)
  const formatLocalDate = (date: Date) => {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
  };

  const handleDayClick = async (date: Date) => {
    if (loading) return;
    if (date > today) return; // Can't mark future dates

    setLoading(true);
    const dateStr = formatLocalDate(date);
    const wasCompleted = isCompleted(date);

    try {
      if (wasCompleted) {
        // Remove completion
        const res = await fetch(`/api/habits/${habit.id}/backfill`, {
          method: "DELETE",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ date: dateStr }),
        });

        if (res.ok) {
          setHabit((prev) => ({
            ...prev,
            completions: prev.completions.filter(
              (c) => !isSameDay(new Date(c.date), date)
            ),
          }));
          toast.success("Completion removed");
        }
      } else {
        // Add completion
        const res = await fetch(`/api/habits/${habit.id}/backfill`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ dates: [dateStr] }),
        });

        if (res.ok) {
          const data = await res.json();
          setHabit((prev) => ({
            ...prev,
            ...data.habit,
            completions: [...prev.completions, ...data.completions],
          }));
          toast.success("Day marked complete!");
        }
      }
    } catch {
      toast.error("Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  const prevMonth = () => {
    setCurrentMonth(
      new Date(currentMonth.getFullYear(), currentMonth.getMonth() - 1)
    );
  };

  const nextMonth = () => {
    const next = new Date(
      currentMonth.getFullYear(),
      currentMonth.getMonth() + 1
    );
    if (next <= new Date()) {
      setCurrentMonth(next);
    }
  };

  const handleEditSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (loading) return;
    setLoading(true);

    try {
      const res = await fetch(`/api/habits/${habit.id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(editForm),
      });

      if (res.ok) {
        const updatedHabit = await res.json();
        setHabit((prev) => ({ ...prev, ...updatedHabit }));
        setEditDialogOpen(false);
        toast.success("Habit updated!");
      } else {
        toast.error("Failed to update habit");
      }
    } catch {
      toast.error("Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (loading) return;
    setLoading(true);

    try {
      const res = await fetch(`/api/habits/${habit.id}`, {
        method: "DELETE",
      });

      if (res.ok) {
        toast.success("Habit deleted");
        router.push("/dashboard");
      } else {
        toast.error("Failed to delete habit");
      }
    } catch {
      toast.error("Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={() => router.back()}>
          <ArrowLeft className="h-5 w-5" />
        </Button>
        <div
          className="h-12 w-12 rounded-xl flex items-center justify-center text-2xl"
          style={{
            backgroundColor: `${habit.color}15`,
            borderColor: habit.color,
            borderWidth: 2,
          }}
        >
          {icon}
        </div>
        <div className="flex-1">
          <h1 className="text-2xl font-bold text-amber-950">{habit.name}</h1>
          <p className="text-amber-800/70">Tap days to mark them complete</p>
        </div>

        {/* Edit & Delete buttons */}
        <div className="flex gap-2">
          <Dialog open={editDialogOpen} onOpenChange={setEditDialogOpen}>
            <DialogTrigger asChild>
              <Button variant="outline" size="icon">
                <Pencil className="h-4 w-4" />
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Edit Habit</DialogTitle>
              </DialogHeader>
              <form onSubmit={handleEditSubmit} className="space-y-4">
                <div>
                  <Label htmlFor="name">Name</Label>
                  <Input
                    id="name"
                    value={editForm.name}
                    onChange={(e) =>
                      setEditForm((prev) => ({ ...prev, name: e.target.value }))
                    }
                    className="mt-1"
                  />
                </div>

                <div>
                  <Label>Icon</Label>
                  <div className="flex items-center gap-2 mt-1 mb-2">
                    <Input
                      placeholder="Type or paste any emoji..."
                      value={customEmoji}
                      onChange={(e) => {
                        setCustomEmoji(e.target.value);
                        if (e.target.value) {
                          setEditForm((prev) => ({ ...prev, icon: e.target.value }));
                        }
                      }}
                      className="flex-1"
                    />
                    <div className="h-10 w-10 rounded-lg flex items-center justify-center text-xl bg-amber-50 border-2 border-amber-200">
                      {getDisplayIcon(editForm.icon)}
                    </div>
                  </div>
                  <p className="text-xs text-amber-700/60 mb-2">Or pick from suggestions:</p>
                  <div className="grid grid-cols-10 gap-1">
                    {SUGGESTED_EMOJIS.map((emoji) => (
                      <button
                        key={emoji}
                        type="button"
                        onClick={() => {
                          setEditForm((prev) => ({ ...prev, icon: emoji }));
                          setCustomEmoji("");
                        }}
                        className={`h-8 rounded-lg text-base transition-all ${
                          editForm.icon === emoji
                            ? "bg-gradient-to-r from-amber-500 to-orange-500 shadow-md"
                            : "bg-amber-50 hover:bg-amber-100"
                        }`}
                      >
                        {emoji}
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <Label htmlFor="color">Color</Label>
                  <Input
                    id="color"
                    type="color"
                    value={editForm.color}
                    onChange={(e) =>
                      setEditForm((prev) => ({ ...prev, color: e.target.value }))
                    }
                    className="mt-1 h-10 w-full"
                  />
                </div>

                {/* Info about credits */}
                <div className="p-4 bg-amber-50/50 rounded-lg">
                  <p className="text-sm text-amber-800/70">
                    Earn credits by hitting milestones (7, 14, 30, 50, 100+ days).
                    Use credits to skip days without breaking your streak!
                  </p>
                </div>

                <Button type="submit" className="w-full bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-700 hover:to-orange-700" disabled={loading}>
                  {loading ? "Saving..." : "Save Changes"}
                </Button>
              </form>
            </DialogContent>
          </Dialog>

          <AlertDialog>
            <AlertDialogTrigger asChild>
              <Button variant="outline" size="icon" className="text-red-500 hover:text-red-600 hover:bg-red-50">
                <Trash2 className="h-4 w-4" />
              </Button>
            </AlertDialogTrigger>
            <AlertDialogContent>
              <AlertDialogHeader>
                <AlertDialogTitle>Delete Habit</AlertDialogTitle>
                <AlertDialogDescription>
                  Are you sure you want to delete &quot;{habit.name}&quot;? This will
                  permanently remove all completion history and credits. This
                  action cannot be undone.
                </AlertDialogDescription>
              </AlertDialogHeader>
              <AlertDialogFooter>
                <AlertDialogCancel>Cancel</AlertDialogCancel>
                <AlertDialogAction
                  onClick={handleDelete}
                  className="bg-red-500 hover:bg-red-600"
                >
                  Delete
                </AlertDialogAction>
              </AlertDialogFooter>
            </AlertDialogContent>
          </AlertDialog>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4">
        <Card className="p-4 text-center">
          <Flame className="h-6 w-6 mx-auto text-orange-500 mb-2" />
          <div className="text-2xl font-bold text-amber-950">
            {habit.currentStreak}
          </div>
          <div className="text-xs text-amber-700/60">Current Streak</div>
        </Card>
        <Card className="p-4 text-center">
          <Trophy className="h-6 w-6 mx-auto text-amber-500 mb-2" />
          <div className="text-2xl font-bold text-amber-950">
            {habit.longestStreak}
          </div>
          <div className="text-xs text-amber-700/60">Best Streak</div>
        </Card>
        <Card className="p-4 text-center">
          <Coins className="h-6 w-6 mx-auto text-amber-500 mb-2" />
          <div className="text-2xl font-bold text-amber-950">
            {habit.currentCredits}
          </div>
          <div className="text-xs text-amber-700/60">Credits</div>
        </Card>
      </div>

      {/* Calendar */}
      <Card className="p-4">
        <div className="flex items-center justify-between mb-4">
          <Button variant="ghost" size="sm" onClick={prevMonth}>
            ← Prev
          </Button>
          <div className="flex items-center gap-2">
            <Calendar className="h-5 w-5 text-amber-600" />
            <span className="font-semibold">
              {currentMonth.toLocaleString("default", {
                month: "long",
                year: "numeric",
              })}
            </span>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={nextMonth}
            disabled={
              currentMonth.getMonth() === new Date().getMonth() &&
              currentMonth.getFullYear() === new Date().getFullYear()
            }
          >
            Next →
          </Button>
        </div>

        {/* Day headers - Week starts on Monday */}
        <div className="grid grid-cols-7 gap-1 mb-2">
          {["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].map((day) => (
            <div
              key={day}
              className="text-center text-xs font-medium text-amber-700/60 py-2"
            >
              {day}
            </div>
          ))}
        </div>

        {/* Days grid */}
        <div className="grid grid-cols-7 gap-1">
          {monthDays.map((date, i) => {
            if (!date) {
              return <div key={`empty-${i}`} className="h-10" />;
            }

            const completed = isCompleted(date);
            const isToday = isSameDay(date, today);
            const isFuture = date > today;

            return (
              <motion.button
                key={date.toISOString()}
                whileHover={{ scale: isFuture ? 1 : 1.1 }}
                whileTap={{ scale: isFuture ? 1 : 0.95 }}
                onClick={() => handleDayClick(date)}
                disabled={isFuture || loading}
                className={`h-10 rounded-lg flex items-center justify-center text-sm font-medium transition-all relative ${
                  isFuture
                    ? "text-amber-300 cursor-not-allowed"
                    : completed
                    ? "bg-gradient-to-br from-green-400 to-emerald-500 text-white shadow-sm"
                    : isToday
                    ? "bg-amber-100 text-amber-700 ring-2 ring-amber-500"
                    : "hover:bg-amber-50 text-amber-900"
                }`}
              >
                {completed && (
                  <Check className="h-4 w-4 absolute" />
                )}
                {!completed && date.getDate()}
              </motion.button>
            );
          })}
        </div>
      </Card>

      {/* Quick backfill */}
      <Card className="p-4">
        <h3 className="font-semibold text-amber-950 mb-3">Quick Backfill</h3>
        <p className="text-sm text-amber-800/70 mb-4">
          Mark multiple consecutive days at once
        </p>
        <div className="flex gap-2 flex-wrap">
          {[3, 5, 7, 14, 30].map((days) => (
            <Button
              key={days}
              variant="outline"
              size="sm"
              onClick={async () => {
                setLoading(true);
                const dates = [];
                for (let i = 0; i < days; i++) {
                  const d = new Date();
                  d.setDate(d.getDate() - i);
                  dates.push(formatLocalDate(d));
                }

                try {
                  const res = await fetch(`/api/habits/${habit.id}/backfill`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ dates }),
                  });

                  if (res.ok) {
                    const data = await res.json();
                    setHabit((prev) => ({
                      ...prev,
                      ...data.habit,
                      completions: [
                        ...prev.completions,
                        ...data.completions,
                      ],
                    }));
                    toast.success(`Marked last ${days} days complete!`);
                  }
                } catch {
                  toast.error("Something went wrong");
                } finally {
                  setLoading(false);
                }
              }}
              disabled={loading}
            >
              Last {days} days
            </Button>
          ))}
        </div>
      </Card>
    </div>
  );
}

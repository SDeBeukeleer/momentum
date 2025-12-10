"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import {
  Check,
  Flame,
  Coins,
  MoreVertical,
  Undo2,
  Calendar,
} from "lucide-react";
import Link from "next/link";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import type { Habit, HabitCompletion } from "@prisma/client";

interface HabitCardProps {
  habit: Habit & { completions: HabitCompletion[] };
  isCompleted: boolean;
  onComplete: (habitId: string, completion: HabitCompletion, updatedHabit: Habit) => void;
  onUncomplete: (habitId: string) => void;
}

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

export function HabitCard({
  habit,
  isCompleted,
  onComplete,
  onUncomplete,
}: HabitCardProps) {
  const [loading, setLoading] = useState(false);
  const [showCelebration, setShowCelebration] = useState(false);

  const icon = getDisplayIcon(habit.icon);
  const creditProgress = (habit.completionCount / habit.completionsForCredit) * 100;

  const handleComplete = async (useCredit = false) => {
    if (loading) return;
    setLoading(true);

    try {
      const res = await fetch(`/api/habits/${habit.id}/complete`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ useCredit }),
      });

      const data = await res.json();

      if (!res.ok) {
        toast.error(data.error || "Failed to complete habit");
        return;
      }

      onComplete(habit.id, data.completion, data.habit);

      // Show celebration
      setShowCelebration(true);
      setTimeout(() => setShowCelebration(false), 1000);

      if (data.creditEarned) {
        toast.success("You earned a credit! 🎉", {
          description: `Keep going to earn more skips!`,
        });
      } else if (useCredit) {
        toast.success("Credit used! Streak preserved 🛡️");
      } else {
        toast.success("Habit completed! 🔥");
      }
    } catch {
      toast.error("Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  const handleUncomplete = async () => {
    if (loading) return;
    setLoading(true);

    try {
      const res = await fetch(`/api/habits/${habit.id}/complete`, {
        method: "DELETE",
      });

      if (!res.ok) {
        const data = await res.json();
        toast.error(data.error || "Failed to undo completion");
        return;
      }

      onUncomplete(habit.id);
      toast.success("Completion undone");
    } catch {
      toast.error("Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card
      className={`relative overflow-hidden transition-all duration-300 ${
        isCompleted
          ? "bg-gradient-to-r from-green-50 to-emerald-50 border-green-200"
          : "bg-white hover:shadow-md"
      }`}
    >
      {/* Celebration Animation */}
      <AnimatePresence>
        {showCelebration && (
          <motion.div
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1.5, opacity: 1 }}
            exit={{ scale: 2, opacity: 0 }}
            className="absolute inset-0 flex items-center justify-center pointer-events-none z-10"
          >
            <span className="text-6xl">🎉</span>
          </motion.div>
        )}
      </AnimatePresence>

      <div className="p-4">
        <div className="flex items-center gap-4">
          {/* Icon */}
          <div
            className="h-12 w-12 rounded-xl flex items-center justify-center text-2xl shadow-sm"
            style={{
              backgroundColor: `${habit.color}15`,
              borderColor: habit.color,
              borderWidth: 2,
            }}
          >
            {icon}
          </div>

          {/* Content - Clickable to go to detail view */}
          <Link href={`/dashboard/habits/${habit.id}`} className="flex-1 min-w-0 cursor-pointer">
            <div className="flex items-center gap-2">
              <h3 className="font-semibold text-slate-900 truncate hover:text-indigo-600 transition-colors">
                {habit.name}
              </h3>
              {habit.currentStreak > 0 && (
                <Badge
                  variant="secondary"
                  className="bg-orange-100 text-orange-700 gap-1"
                >
                  <Flame className="h-3 w-3" />
                  {habit.currentStreak}
                </Badge>
              )}
            </div>

            {/* Credit Progress */}
            <div className="mt-2 flex items-center gap-2">
              <div className="flex-1">
                <Progress value={creditProgress} className="h-2" />
              </div>
              <div className="flex items-center gap-1 text-xs text-slate-500">
                <Coins className="h-3 w-3 text-amber-500" />
                <span className="font-medium">{habit.currentCredits}</span>
              </div>
            </div>
            <p className="text-xs text-slate-500 mt-1">
              {habit.completionCount}/{habit.completionsForCredit} to next credit
            </p>
          </Link>

          {/* Actions */}
          <div className="flex items-center gap-2">
            {isCompleted ? (
              <Button
                size="icon"
                variant="ghost"
                className="h-10 w-10 rounded-full bg-green-500 text-white hover:bg-green-600"
                onClick={handleUncomplete}
                disabled={loading}
              >
                <Check className="h-5 w-5" />
              </Button>
            ) : (
              <>
                {habit.currentCredits > 0 && (
                  <Button
                    size="sm"
                    variant="outline"
                    className="gap-1 text-amber-600 border-amber-300 hover:bg-amber-50"
                    onClick={() => handleComplete(true)}
                    disabled={loading}
                  >
                    <Coins className="h-4 w-4" />
                    Skip
                  </Button>
                )}
                <Button
                  size="icon"
                  className="h-10 w-10 rounded-full bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700"
                  onClick={() => handleComplete(false)}
                  disabled={loading}
                >
                  {loading ? (
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{
                        duration: 1,
                        repeat: Infinity,
                        ease: "linear",
                      }}
                      className="h-4 w-4 border-2 border-white border-t-transparent rounded-full"
                    />
                  ) : (
                    <Check className="h-5 w-5" />
                  )}
                </Button>
              </>
            )}

            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button size="icon" variant="ghost" className="h-8 w-8">
                  <MoreVertical className="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuItem asChild>
                  <Link href={`/dashboard/habits/${habit.id}`}>
                    <Calendar className="mr-2 h-4 w-4" />
                    Backfill days
                  </Link>
                </DropdownMenuItem>
                {isCompleted && (
                  <DropdownMenuItem onClick={handleUncomplete}>
                    <Undo2 className="mr-2 h-4 w-4" />
                    Undo completion
                  </DropdownMenuItem>
                )}
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </div>
      </div>
    </Card>
  );
}

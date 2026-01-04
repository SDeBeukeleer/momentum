"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import {
  Check,
  Flame,
  Coins,
  MoreVertical,
  Undo2,
  Calendar,
  Edit,
  Archive,
  Trash2,
  Sparkles,
} from "lucide-react";
import Link from "next/link";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { HabitIconDisplay } from "./habit-icons";
import { DioramaDisplay } from "@/components/diorama-display";
import { getThemeConfig, type DioramaTheme } from "@/types/diorama";
import type { Habit, HabitCompletion } from "@prisma/client";

interface MilestoneData {
  name: string;
  emoji: string;
  description: string;
  bonusCredits: number;
}

interface HabitCardProps {
  habit: Habit & { completions: HabitCompletion[] };
  isCompleted: boolean;
  onComplete: (habitId: string, completion: HabitCompletion, updatedHabit: Habit, milestoneReached?: MilestoneData | null) => void;
  onUncomplete: (habitId: string) => void;
  onEdit?: (habit: Habit & { completions: HabitCompletion[] }) => void;
  onArchive?: (habitId: string) => void;
  onDelete?: (habitId: string) => void;
}

// Streak tier system for visual progression
type StreakTier = 'none' | 'starter' | 'intermediate' | 'advanced' | 'epic' | 'legendary';

function getStreakTier(streak: number): StreakTier {
  if (streak >= 100) return 'legendary';
  if (streak >= 50) return 'epic';
  if (streak >= 30) return 'advanced';
  if (streak >= 14) return 'intermediate';
  if (streak >= 7) return 'starter';
  return 'none';
}

function getStreakBadgeClasses(tier: StreakTier): string {
  switch (tier) {
    case 'legendary':
      return 'streak-badge-legendary text-white animate-streak-shimmer';
    case 'epic':
      return 'streak-badge-epic text-slate-900 animate-streak-pulse';
    case 'advanced':
      return 'streak-badge-advanced text-white';
    case 'intermediate':
      return 'streak-badge-intermediate text-white';
    case 'starter':
      return 'streak-badge-starter text-white';
    default:
      return 'bg-slate-100 text-slate-600';
  }
}

export function HabitCard({
  habit,
  isCompleted,
  onComplete,
  onUncomplete,
  onEdit,
  onArchive,
  onDelete,
}: HabitCardProps) {
  const [loading, setLoading] = useState(false);
  const [showCelebration, setShowCelebration] = useState(false);

  const streakTier = getStreakTier(habit.currentStreak);
  const theme = (habit.dioramaTheme || 'plant') as DioramaTheme;
  const themeConfig = getThemeConfig(theme);

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

      onComplete(habit.id, data.completion, data.habit, data.milestoneReached);

      setShowCelebration(true);
      setTimeout(() => setShowCelebration(false), 1000);

      if (data.milestoneReached) {
        toast.success(`${data.milestoneReached.name}!`, {
          description: `+${data.milestoneReached.bonusCredits} credit${data.milestoneReached.bonusCredits > 1 ? 's' : ''} earned!`,
        });
      } else if (useCredit) {
        toast.success("Credit used! Streak preserved");
      } else {
        toast.success("Habit completed!");
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
    <motion.div
      data-onboarding="habit-card"
      className={`relative overflow-hidden rounded-2xl border transition-all duration-300 ${
        isCompleted
          ? "bg-indigo-50 border-indigo-200 shadow-md shadow-indigo-100"
          : "bg-white border-slate-200 shadow-sm hover:shadow-md hover:border-slate-300"
      }`}
      whileHover={{ scale: 1.01 }}
      whileTap={{ scale: 0.99 }}
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
            <div className="relative">
              <Sparkles className="h-16 w-16 text-indigo-500" />
              <div className="absolute inset-0 animate-ping">
                <Sparkles className="h-16 w-16 text-indigo-300" />
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <div className="p-4 relative z-0">
        <div className="flex items-center gap-4">
          {/* Icon or Mini Diorama */}
          <motion.div
            animate={isCompleted ? { scale: [1, 1.05, 1] } : {}}
            transition={{ duration: 0.5 }}
            className="relative"
          >
            {habit.currentStreak > 0 ? (
              <Link href={`/dashboard/habits/${habit.id}`} className="block">
                <DioramaDisplay
                  day={Math.min(habit.currentStreak, themeConfig.maxDays)}
                  theme={theme}
                  size="mini"
                  animate={false}
                  showGlow={false}
                />
              </Link>
            ) : (
              <HabitIconDisplay
                iconId={habit.icon}
                size="md"
                glowing={isCompleted}
              />
            )}
            {isCompleted && (
              <motion.div
                className="absolute -top-1 -right-1 h-5 w-5 rounded-full bg-indigo-600 flex items-center justify-center shadow-sm"
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: "spring", stiffness: 500 }}
              >
                <Check className="h-3 w-3 text-white" />
              </motion.div>
            )}
          </motion.div>

          {/* Content */}
          <Link href={`/dashboard/habits/${habit.id}`} className="flex-1 min-w-0 cursor-pointer group">
            <div className="flex items-center gap-2 flex-wrap">
              <h3 className="font-semibold text-slate-900 truncate group-hover:text-indigo-600 transition-colors">
                {habit.name}
              </h3>
              {habit.currentStreak > 0 && (
                <div
                  className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-semibold ${getStreakBadgeClasses(streakTier)}`}
                >
                  <Flame className="h-3 w-3" />
                  {habit.currentStreak}
                </div>
              )}
            </div>

            {habit.currentCredits > 0 && (
              <div className="mt-1.5 flex items-center gap-1.5 text-xs text-slate-500">
                <Coins className="h-3.5 w-3.5 text-amber-500" />
                <span>{habit.currentCredits} credit{habit.currentCredits > 1 ? 's' : ''} available</span>
              </div>
            )}
          </Link>

          {/* Actions */}
          <div className="flex items-center gap-2">
            {isCompleted ? (
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: "spring", stiffness: 400 }}
              >
                <Button
                  size="icon"
                  variant="ghost"
                  className="h-11 w-11 rounded-full bg-indigo-600 text-white hover:bg-indigo-700 shadow-lg shadow-indigo-200"
                  onClick={handleUncomplete}
                  disabled={loading}
                >
                  <Check className="h-5 w-5" />
                </Button>
              </motion.div>
            ) : (
              <>
                {habit.currentCredits > 0 && (
                  <Button
                    size="sm"
                    variant="outline"
                    className="gap-1.5 text-amber-600 border-amber-300 hover:bg-amber-50 hover:border-amber-400"
                    onClick={() => handleComplete(true)}
                    disabled={loading}
                  >
                    <Coins className="h-4 w-4" />
                    Skip
                  </Button>
                )}
                <Button
                  size="icon"
                  className="h-11 w-11 rounded-full bg-indigo-600 hover:bg-indigo-700 shadow-lg shadow-indigo-200 transition-all"
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
                      className="h-5 w-5 border-2 border-white border-t-transparent rounded-full"
                    />
                  ) : (
                    <Check className="h-5 w-5" />
                  )}
                </Button>
              </>
            )}

            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button size="icon" variant="ghost" className="h-8 w-8 text-slate-400 hover:text-slate-600">
                  <MoreVertical className="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                {onEdit && (
                  <DropdownMenuItem onClick={() => onEdit(habit)} className="focus:bg-slate-100">
                    <Edit className="mr-2 h-4 w-4" />
                    Edit
                  </DropdownMenuItem>
                )}
                <DropdownMenuItem asChild className="focus:bg-slate-100">
                  <Link href={`/dashboard/habits/${habit.id}`}>
                    <Calendar className="mr-2 h-4 w-4" />
                    Backfill days
                  </Link>
                </DropdownMenuItem>
                {isCompleted && (
                  <DropdownMenuItem onClick={handleUncomplete} className="focus:bg-slate-100">
                    <Undo2 className="mr-2 h-4 w-4" />
                    Undo completion
                  </DropdownMenuItem>
                )}
                {onArchive && (
                  <>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem onClick={() => onArchive(habit.id)} className="focus:bg-slate-100">
                      <Archive className="mr-2 h-4 w-4" />
                      Archive
                    </DropdownMenuItem>
                  </>
                )}
                {onDelete && (
                  <DropdownMenuItem
                    className="text-red-600 focus:bg-red-50 focus:text-red-600"
                    onClick={() => onDelete(habit.id)}
                  >
                    <Trash2 className="mr-2 h-4 w-4" />
                    Delete
                  </DropdownMenuItem>
                )}
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </div>
      </div>
    </motion.div>
  );
}

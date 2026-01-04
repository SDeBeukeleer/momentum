"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { HabitCard } from "./habit-card";
import { CreateHabitDialog } from "./create-habit-dialog";
import { EditHabitDialog } from "./edit-habit-dialog";
import { MilestoneCelebration } from "@/components/celebrations/MilestoneCelebration";
import { DioramaDisplay } from "@/components/diorama-display";
import { useGuidanceContext } from "@/components/guidance";
import { Button } from "@/components/ui/button";
import { Plus, Sparkles, Flame, ArrowRight, Leaf, Target } from "lucide-react";
import Link from "next/link";
import { toast } from "sonner";
import type { Habit, HabitCompletion } from "@prisma/client";

interface MilestoneData {
  name: string;
  emoji: string;
  description: string;
  bonusCredits: number;
}

type HabitWithCompletions = Habit & {
  completions: HabitCompletion[];
};

interface TodayViewProps {
  habits: HabitWithCompletions[];
  userName: string;
}

function getGreeting() {
  const hour = new Date().getHours();
  if (hour < 12) return "Good morning";
  if (hour < 18) return "Good afternoon";
  return "Good evening";
}

function getMotivationalMessage(completedCount: number, totalCount: number) {
  if (totalCount === 0) return "Plant your first seed to start growing";
  if (completedCount === totalCount) return "Your garden is thriving today!";
  if (completedCount === 0) return "Time to nurture your habits";
  if (completedCount / totalCount >= 0.5) return "Growing strong! Keep nurturing";
  return "Every small step helps your garden grow";
}

export function TodayView({ habits: initialHabits, userName }: TodayViewProps) {
  const [habits, setHabits] = useState(initialHabits);
  const [showCreateDialog, setShowCreateDialog] = useState(false);
  const [editingHabit, setEditingHabit] = useState<HabitWithCompletions | null>(null);
  const [celebratingMilestone, setCelebratingMilestone] = useState<MilestoneData | null>(null);

  const { onHabitCreated, onHabitCompleted } = useGuidanceContext();

  const completedCount = habits.filter((h) => h.completions.length > 0).length;
  const totalCount = habits.length;
  const progressPercent = totalCount > 0 ? (completedCount / totalCount) * 100 : 0;

  const handleHabitComplete = (
    habitId: string,
    completion: HabitCompletion,
    updatedHabit: Habit,
    milestoneReached?: MilestoneData | null
  ) => {
    setHabits((prev) =>
      prev.map((h) =>
        h.id === habitId
          ? { ...updatedHabit, completions: [completion] }
          : h
      )
    );

    if (milestoneReached) {
      setCelebratingMilestone(milestoneReached);
    }

    if (!milestoneReached) {
      onHabitCompleted(updatedHabit.currentStreak);
    }
  };

  const handleHabitUncomplete = (habitId: string) => {
    setHabits((prev) =>
      prev.map((h) =>
        h.id === habitId
          ? { ...h, completions: [], currentStreak: Math.max(0, h.currentStreak - 1) }
          : h
      )
    );
  };

  const handleHabitCreated = (habit: HabitWithCompletions) => {
    setHabits((prev) => [...prev, habit]);
    setShowCreateDialog(false);
    onHabitCreated();
  };

  const handleHabitUpdated = (updatedHabit: Habit) => {
    setHabits((prev) =>
      prev.map((h) =>
        h.id === updatedHabit.id ? { ...h, ...updatedHabit } : h
      )
    );
    setEditingHabit(null);
  };

  const handleArchive = async (habitId: string) => {
    try {
      const res = await fetch(`/api/habits/${habitId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ isArchived: true }),
      });

      if (!res.ok) {
        toast.error("Failed to archive habit");
        return;
      }

      setHabits((prev) => prev.filter((h) => h.id !== habitId));
      toast.success("Habit archived");
    } catch {
      toast.error("Something went wrong");
    }
  };

  const handleDelete = async (habitId: string) => {
    if (!confirm("Are you sure you want to delete this habit? This cannot be undone.")) {
      return;
    }

    try {
      const res = await fetch(`/api/habits/${habitId}`, {
        method: "DELETE",
      });

      if (!res.ok) {
        toast.error("Failed to delete habit");
        return;
      }

      setHabits((prev) => prev.filter((h) => h.id !== habitId));
      toast.success("Habit deleted");
    } catch {
      toast.error("Something went wrong");
    }
  };

  return (
    <div className="space-y-8 max-w-2xl mx-auto">
      {/* Header */}
      <div className="space-y-3">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center gap-3"
        >
          <div className="h-12 w-12 rounded-2xl bg-indigo-100 flex items-center justify-center">
            <Leaf className="h-6 w-6 text-indigo-600" />
          </div>
          <div>
            <h1
              className="text-2xl md:text-3xl font-semibold text-slate-900"
              style={{ fontFamily: 'var(--font-fraunces)' }}
            >
              {getGreeting()}, {userName}
            </h1>
          </div>
        </motion.div>
        <motion.p
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="text-slate-500 flex items-center gap-2 pl-1"
        >
          <Sparkles className="h-4 w-4 text-indigo-500" />
          {getMotivationalMessage(completedCount, totalCount)}
        </motion.p>
      </div>

      {/* Progress Summary */}
      {totalCount > 0 && (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-2xl border border-slate-200 shadow-sm p-5"
        >
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Target className="h-4 w-4 text-indigo-600" />
              <span className="text-sm font-medium text-slate-700">Today&apos;s Progress</span>
            </div>
            <div className="flex items-baseline gap-1">
              <span className="text-2xl font-bold text-indigo-600">{completedCount}</span>
              <span className="text-slate-400">/</span>
              <span className="text-lg text-slate-500">{totalCount}</span>
            </div>
          </div>
          <div className="relative h-3 bg-slate-100 rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${progressPercent}%` }}
              transition={{ duration: 0.8, delay: 0.3, ease: "easeOut" }}
              className="absolute inset-y-0 left-0 bg-gradient-to-r from-indigo-500 to-indigo-600 rounded-full"
            />
            {progressPercent > 0 && progressPercent < 100 && (
              <motion.div
                className="absolute inset-y-0 left-0 rounded-full"
                style={{ width: `${progressPercent}%` }}
              >
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent animate-shimmer" />
              </motion.div>
            )}
          </div>
          {completedCount === totalCount && totalCount > 0 && (
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
              className="text-sm text-indigo-600 mt-3 text-center font-medium"
            >
              All habits complete! Your garden flourishes.
            </motion.p>
          )}
        </motion.div>
      )}

      {/* Mini Diorama Preview */}
      {(() => {
        const bestHabit = habits.reduce((best, h) =>
          h.currentStreak > (best?.currentStreak || 0) ? h : best,
          habits[0]
        );
        if (!bestHabit || bestHabit.currentStreak === 0) return null;

        return (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.3 }}
          >
            <Link href="/garden">
              <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-4 cursor-pointer group transition-all hover:shadow-md hover:border-indigo-200">
                <div className="flex items-center gap-4">
                  <div className="relative">
                    <DioramaDisplay
                      day={Math.min(bestHabit.currentStreak, 200)}
                      size="mini"
                      animate={false}
                      showGlow={false}
                    />
                    <div className="absolute inset-0 rounded-xl bg-indigo-500/10 opacity-0 group-hover:opacity-100 transition-opacity" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-slate-500">Your best streak</p>
                    <p className="font-semibold text-slate-900 truncate">{bestHabit.name}</p>
                    <div className="flex items-center gap-1.5 text-indigo-600 mt-1">
                      <Flame className="h-4 w-4" />
                      <span className="font-bold">{bestHabit.currentStreak} days</span>
                    </div>
                  </div>
                  <ArrowRight className="h-5 w-5 text-slate-400 group-hover:text-indigo-600 group-hover:translate-x-1 transition-all" />
                </div>
              </div>
            </Link>
          </motion.div>
        );
      })()}

      {/* Habits List */}
      <div className="space-y-3">
        <AnimatePresence mode="popLayout">
          {habits.map((habit, index) => (
            <motion.div
              key={habit.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, x: -100 }}
              transition={{ delay: index * 0.05 }}
            >
              <HabitCard
                habit={habit}
                isCompleted={habit.completions.length > 0}
                onComplete={handleHabitComplete}
                onUncomplete={handleHabitUncomplete}
                onEdit={setEditingHabit}
                onArchive={handleArchive}
                onDelete={handleDelete}
              />
            </motion.div>
          ))}
        </AnimatePresence>

        {habits.length === 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center py-16"
          >
            <div className="relative h-24 w-24 mx-auto mb-6">
              <div className="absolute inset-0 rounded-full bg-indigo-100 animate-pulse" />
              <div className="absolute inset-2 rounded-full bg-indigo-50 flex items-center justify-center">
                <Leaf className="h-10 w-10 text-indigo-500" />
              </div>
            </div>
            <h3
              className="text-xl font-semibold text-slate-900 mb-2"
              style={{ fontFamily: 'var(--font-fraunces)' }}
            >
              Plant your first seed
            </h3>
            <p className="text-slate-500 mb-6 max-w-xs mx-auto">
              Create your first habit and watch your garden grow with each day of progress
            </p>
            <Button
              onClick={() => setShowCreateDialog(true)}
              className="bg-indigo-600 hover:bg-indigo-700 text-white shadow-lg shadow-indigo-200"
            >
              <Plus className="h-4 w-4 mr-2" />
              Create Habit
            </Button>
          </motion.div>
        )}
      </div>

      {/* Add Habit FAB */}
      {habits.length > 0 && (
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.5, type: "spring" }}
          className="fixed bottom-24 right-4 md:bottom-8 md:right-8 z-40"
        >
          <Button
            onClick={() => setShowCreateDialog(true)}
            size="lg"
            className="h-14 w-14 rounded-full bg-indigo-600 hover:bg-indigo-700 shadow-xl shadow-indigo-300 transition-all hover:scale-105"
          >
            <Plus className="h-6 w-6" />
          </Button>
        </motion.div>
      )}

      {/* Create Habit Dialog */}
      <CreateHabitDialog
        open={showCreateDialog}
        onOpenChange={setShowCreateDialog}
        onCreated={handleHabitCreated}
      />

      {/* Milestone Celebration */}
      <MilestoneCelebration
        milestone={celebratingMilestone}
        onClose={() => setCelebratingMilestone(null)}
      />

      {/* Edit Habit Dialog */}
      {editingHabit && (
        <EditHabitDialog
          habit={editingHabit}
          open={!!editingHabit}
          onOpenChange={(open) => !open && setEditingHabit(null)}
          onUpdated={handleHabitUpdated}
        />
      )}
    </div>
  );
}

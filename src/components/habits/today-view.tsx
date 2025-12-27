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
import { Card } from "@/components/ui/card";
import { Plus, Sparkles, Flame, ArrowRight } from "lucide-react";
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
  if (totalCount === 0) return "Create your first habit to get started!";
  if (completedCount === totalCount) return "You're on fire! All habits completed!";
  if (completedCount === 0) return "Let's crush those habits today!";
  if (completedCount / totalCount >= 0.5) return "Great progress! Keep it going!";
  return "You've got this! One habit at a time.";
}

export function TodayView({ habits: initialHabits, userName }: TodayViewProps) {
  const [habits, setHabits] = useState(initialHabits);
  const [showCreateDialog, setShowCreateDialog] = useState(false);
  const [editingHabit, setEditingHabit] = useState<HabitWithCompletions | null>(null);
  const [celebratingMilestone, setCelebratingMilestone] = useState<MilestoneData | null>(null);

  const { onHabitCreated, onHabitCompleted } = useGuidanceContext();

  const completedCount = habits.filter((h) => h.completions.length > 0).length;
  const totalCount = habits.length;

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

    // Show milestone celebration if one was reached
    if (milestoneReached) {
      setCelebratingMilestone(milestoneReached);
    }

    // Trigger guidance pop-up (only if no milestone celebration)
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

    // Trigger guidance pop-up for first habit creation
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
    <div className="space-y-6">
      {/* Header */}
      <div className="space-y-2">
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-2xl md:text-3xl font-bold text-amber-950"
        >
          {getGreeting()}, {userName}!
        </motion.h1>
        <motion.p
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="text-amber-800/70 flex items-center gap-2"
        >
          <Sparkles className="h-4 w-4 text-amber-500" />
          {getMotivationalMessage(completedCount, totalCount)}
        </motion.p>
      </div>

      {/* Progress Summary */}
      {totalCount > 0 && (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="bg-white/80 rounded-2xl p-4 shadow-sm border border-amber-200/60"
        >
          <div className="flex items-center justify-between mb-3">
            <span className="text-sm font-medium text-amber-800/70">Today&apos;s Progress</span>
            <span className="text-sm font-bold text-amber-950">
              {completedCount}/{totalCount}
            </span>
          </div>
          <div className="h-3 bg-amber-100 rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{
                width: `${totalCount > 0 ? (completedCount / totalCount) * 100 : 0}%`,
              }}
              transition={{ duration: 0.5, delay: 0.3 }}
              className="h-full bg-gradient-to-r from-amber-500 to-orange-500 rounded-full"
            />
          </div>
        </motion.div>
      )}

      {/* Mini Diorama Preview - Show best streak habit */}
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
              <Card className="p-4 hover:shadow-md transition-shadow cursor-pointer group">
                <div className="flex items-center gap-4">
                  <DioramaDisplay
                    day={Math.min(bestHabit.currentStreak, 200)}
                    size="mini"
                    animate={false}
                    showGlow={false}
                  />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-amber-700/60">Your best streak</p>
                    <p className="font-semibold text-amber-950 truncate">{bestHabit.name}</p>
                    <div className="flex items-center gap-1 text-orange-600">
                      <Flame className="h-4 w-4" />
                      <span className="font-bold">{bestHabit.currentStreak} days</span>
                    </div>
                  </div>
                  <ArrowRight className="h-5 w-5 text-amber-400 group-hover:text-amber-600 transition-colors" />
                </div>
              </Card>
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
            className="text-center py-12"
          >
            <div className="h-20 w-20 mx-auto mb-4 rounded-full bg-gradient-to-br from-amber-100 to-orange-100 flex items-center justify-center">
              <Plus className="h-10 w-10 text-amber-600" />
            </div>
            <h3 className="text-lg font-semibold text-amber-950 mb-2">
              No habits yet
            </h3>
            <p className="text-amber-800/70 mb-4">
              Create your first habit to start building momentum!
            </p>
            <Button
              onClick={() => setShowCreateDialog(true)}
              className="bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-700 hover:to-orange-700"
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
          className="fixed bottom-24 right-4 md:bottom-6 md:right-6"
        >
          <Button
            onClick={() => setShowCreateDialog(true)}
            size="lg"
            className="h-14 w-14 rounded-full bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-700 hover:to-orange-700 shadow-lg hover:shadow-xl transition-all"
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

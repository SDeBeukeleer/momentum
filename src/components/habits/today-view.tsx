"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { HabitCard } from "./habit-card";
import { CreateHabitDialog } from "./create-habit-dialog";
import { Button } from "@/components/ui/button";
import { Plus, Sparkles } from "lucide-react";
import type { Habit, HabitCompletion } from "@prisma/client";

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

  const completedCount = habits.filter((h) => h.completions.length > 0).length;
  const totalCount = habits.length;

  const handleHabitComplete = (habitId: string, completion: HabitCompletion, updatedHabit: Habit) => {
    setHabits((prev) =>
      prev.map((h) =>
        h.id === habitId
          ? { ...updatedHabit, completions: [completion] }
          : h
      )
    );
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
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="space-y-2">
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-2xl md:text-3xl font-bold text-slate-900"
        >
          {getGreeting()}, {userName}!
        </motion.h1>
        <motion.p
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="text-slate-600 flex items-center gap-2"
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
          className="bg-white rounded-2xl p-4 shadow-sm border border-slate-200"
        >
          <div className="flex items-center justify-between mb-3">
            <span className="text-sm font-medium text-slate-600">Today&apos;s Progress</span>
            <span className="text-sm font-bold text-slate-900">
              {completedCount}/{totalCount}
            </span>
          </div>
          <div className="h-3 bg-slate-100 rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{
                width: `${totalCount > 0 ? (completedCount / totalCount) * 100 : 0}%`,
              }}
              transition={{ duration: 0.5, delay: 0.3 }}
              className="h-full bg-gradient-to-r from-indigo-500 to-purple-600 rounded-full"
            />
          </div>
        </motion.div>
      )}

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
            <div className="h-20 w-20 mx-auto mb-4 rounded-full bg-gradient-to-br from-indigo-100 to-purple-100 flex items-center justify-center">
              <Plus className="h-10 w-10 text-indigo-500" />
            </div>
            <h3 className="text-lg font-semibold text-slate-900 mb-2">
              No habits yet
            </h3>
            <p className="text-slate-600 mb-4">
              Create your first habit to start building momentum!
            </p>
            <Button
              onClick={() => setShowCreateDialog(true)}
              className="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700"
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
            className="h-14 w-14 rounded-full bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 shadow-lg hover:shadow-xl transition-all"
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
    </div>
  );
}

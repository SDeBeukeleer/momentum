"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { CreateHabitDialog } from "./create-habit-dialog";
import { EditHabitDialog } from "./edit-habit-dialog";
import {
  Plus,
  Flame,
  Coins,
  Edit,
  Archive,
  Trash2,
  MoreVertical,
} from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { toast } from "sonner";
import type { Habit, HabitCompletion } from "@prisma/client";

type HabitWithCompletions = Habit & {
  completions: HabitCompletion[];
};

interface HabitsListProps {
  habits: HabitWithCompletions[];
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

export function HabitsList({ habits: initialHabits }: HabitsListProps) {
  const [habits, setHabits] = useState(initialHabits);
  const [showCreateDialog, setShowCreateDialog] = useState(false);
  const [editingHabit, setEditingHabit] = useState<HabitWithCompletions | null>(
    null
  );
  const [showArchived, setShowArchived] = useState(false);

  const activeHabits = habits.filter((h) => !h.isArchived);
  const archivedHabits = habits.filter((h) => h.isArchived);

  const handleHabitCreated = (habit: HabitWithCompletions) => {
    setHabits((prev) => [...prev, habit]);
    setShowCreateDialog(false);
  };

  const handleHabitUpdated = (updatedHabit: Habit) => {
    setHabits((prev) =>
      prev.map((h) =>
        h.id === updatedHabit.id ? { ...h, ...updatedHabit } : h
      )
    );
    setEditingHabit(null);
  };

  const handleArchive = async (habitId: string, archive: boolean) => {
    try {
      const res = await fetch(`/api/habits/${habitId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ isArchived: archive }),
      });

      if (!res.ok) {
        toast.error("Failed to update habit");
        return;
      }

      setHabits((prev) =>
        prev.map((h) =>
          h.id === habitId ? { ...h, isArchived: archive } : h
        )
      );

      toast.success(archive ? "Habit archived" : "Habit restored");
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

  const renderHabitCard = (habit: HabitWithCompletions) => {
    const icon = getDisplayIcon(habit.icon);
    const creditProgress =
      (habit.completionCount / habit.completionsForCredit) * 100;

    return (
      <motion.div
        key={habit.id}
        layout
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, x: -100 }}
      >
        <Card className="p-4">
          <div className="flex items-start gap-4">
            <div
              className="h-12 w-12 rounded-xl flex items-center justify-center text-2xl shrink-0"
              style={{
                backgroundColor: `${habit.color}15`,
                borderColor: habit.color,
                borderWidth: 2,
              }}
            >
              {icon}
            </div>

            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                <h3 className="font-semibold text-slate-900 truncate">
                  {habit.name}
                </h3>
                {habit.isArchived && (
                  <Badge variant="secondary">Archived</Badge>
                )}
              </div>

              <div className="flex items-center gap-4 text-sm text-slate-500">
                <div className="flex items-center gap-1">
                  <Flame className="h-4 w-4 text-orange-500" />
                  <span>
                    {habit.currentStreak} day streak (best: {habit.longestStreak})
                  </span>
                </div>
                <div className="flex items-center gap-1">
                  <Coins className="h-4 w-4 text-amber-500" />
                  <span>{habit.currentCredits} credits</span>
                </div>
              </div>

              <div className="mt-3">
                <div className="flex items-center justify-between text-xs text-slate-500 mb-1">
                  <span>Credit progress</span>
                  <span>
                    {habit.completionCount}/{habit.completionsForCredit}
                  </span>
                </div>
                <Progress value={creditProgress} className="h-2" />
              </div>
            </div>

            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button size="icon" variant="ghost">
                  <MoreVertical className="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuItem onClick={() => setEditingHabit(habit)}>
                  <Edit className="mr-2 h-4 w-4" />
                  Edit
                </DropdownMenuItem>
                <DropdownMenuItem
                  onClick={() => handleArchive(habit.id, !habit.isArchived)}
                >
                  <Archive className="mr-2 h-4 w-4" />
                  {habit.isArchived ? "Restore" : "Archive"}
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem
                  className="text-red-600"
                  onClick={() => handleDelete(habit.id)}
                >
                  <Trash2 className="mr-2 h-4 w-4" />
                  Delete
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </Card>
      </motion.div>
    );
  };

  return (
    <div className="space-y-6">
      {/* Active Habits */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="font-semibold text-slate-900">
            Active Habits ({activeHabits.length})
          </h2>
          <Button
            onClick={() => setShowCreateDialog(true)}
            className="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700"
          >
            <Plus className="h-4 w-4 mr-2" />
            New Habit
          </Button>
        </div>

        <AnimatePresence mode="popLayout">
          {activeHabits.map(renderHabitCard)}
        </AnimatePresence>

        {activeHabits.length === 0 && (
          <Card className="p-8 text-center">
            <p className="text-slate-500">No active habits yet</p>
          </Card>
        )}
      </div>

      {/* Archived Habits */}
      {archivedHabits.length > 0 && (
        <div className="space-y-3">
          <button
            onClick={() => setShowArchived(!showArchived)}
            className="flex items-center gap-2 text-slate-600 hover:text-slate-900 transition-colors"
          >
            <Archive className="h-4 w-4" />
            <span className="font-medium">
              Archived ({archivedHabits.length})
            </span>
          </button>

          <AnimatePresence>
            {showArchived && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                className="space-y-3"
              >
                {archivedHabits.map(renderHabitCard)}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      )}

      {/* Dialogs */}
      <CreateHabitDialog
        open={showCreateDialog}
        onOpenChange={setShowCreateDialog}
        onCreated={handleHabitCreated}
      />

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

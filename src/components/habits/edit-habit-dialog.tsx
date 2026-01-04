"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { toast } from "sonner";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { IconPicker, HabitIconDisplay, HABIT_ICONS } from "./habit-icons";
import { Save } from "lucide-react";
import type { Habit } from "@prisma/client";

interface EditHabitDialogProps {
  habit: Habit;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onUpdated: (habit: Habit) => void;
}

export function EditHabitDialog({
  habit,
  open,
  onOpenChange,
  onUpdated,
}: EditHabitDialogProps) {
  const [name, setName] = useState(habit.name);
  const [icon, setIcon] = useState(habit.icon);
  const [loading, setLoading] = useState(false);

  // Update state when habit changes
  useEffect(() => {
    setName(habit.name);
    // Convert old emoji icons to new icon IDs if needed
    const isValidIconId = HABIT_ICONS.some((i) => i.id === habit.icon);
    setIcon(isValidIconId ? habit.icon : "target");
  }, [habit]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) {
      toast.error("Please enter a habit name");
      return;
    }

    setLoading(true);

    try {
      const res = await fetch(`/api/habits/${habit.id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: name.trim(),
          icon,
          color: "#00c458", // Keep consistent with primary green
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        toast.error(data.error || "Failed to update habit");
        return;
      }

      onUpdated(data);
      toast.success("Habit updated!");
    } catch {
      toast.error("Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md bg-white border-slate-200">
        <DialogHeader>
          <DialogTitle
            className="text-xl font-semibold text-slate-900"
            style={{ fontFamily: "var(--font-fraunces)" }}
          >
            Edit Habit
          </DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Preview */}
          <div className="flex items-center justify-center py-4">
            <div className="flex items-center gap-4 bg-slate-50 border border-slate-200 rounded-2xl p-4 pr-8">
              <HabitIconDisplay iconId={icon} size="lg" glowing />
              <div>
                <p className="font-semibold text-slate-900">
                  {name || "Your habit name"}
                </p>
                <p className="text-sm text-slate-500">
                  {habit.currentStreak} day streak
                </p>
              </div>
            </div>
          </div>

          {/* Name */}
          <div className="space-y-2">
            <Label htmlFor="edit-name" className="text-slate-700">
              Habit Name
            </Label>
            <Input
              id="edit-name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="h-12 bg-white border-slate-300 rounded-xl focus:border-indigo-500 focus:ring-indigo-200 placeholder:text-slate-400"
            />
          </div>

          {/* Icon Selection */}
          <div className="space-y-3">
            <Label className="text-slate-700">Choose an Icon</Label>
            <IconPicker value={icon} onChange={setIcon} />
          </div>

          {/* Actions */}
          <div className="flex gap-3">
            <Button
              type="button"
              variant="outline"
              className="flex-1 h-12 rounded-xl border-slate-300 hover:bg-slate-50"
              onClick={() => onOpenChange(false)}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              className="flex-1 h-12 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-medium shadow-lg shadow-indigo-200 transition-all"
              disabled={loading}
            >
              {loading ? (
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                  className="h-5 w-5 border-2 border-white border-t-transparent rounded-full"
                />
              ) : (
                <>
                  <Save className="h-4 w-4 mr-2" />
                  Save Changes
                </>
              )}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}

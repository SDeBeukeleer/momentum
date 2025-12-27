"use client";

import { useState } from "react";
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
import type { Habit } from "@prisma/client";

const SUGGESTED_EMOJIS = [
  "🎯", "💪", "📚", "🧘", "💧", "😴", "🥗", "💻", "✍️", "🎵",
  "🏃", "🚴", "🏊", "🧘‍♀️", "🏋️", "🌱", "🎨", "🎸", "📝", "🧠",
];

const COLORS = [
  "#d97706", // Amber
  "#ea580c", // Orange
  "#dc2626", // Red
  "#db2777", // Pink
  "#9333ea", // Purple
  "#2563eb", // Blue
  "#0891b2", // Cyan
  "#059669", // Emerald
  "#65a30d", // Lime
  "#ca8a04", // Yellow
];

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
  const [color, setColor] = useState(habit.color);
  const [customEmoji, setCustomEmoji] = useState("");
  const [loading, setLoading] = useState(false);

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
          color,
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
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Edit Habit</DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="name">Habit Name</Label>
            <Input
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="h-11"
            />
          </div>

          <div className="space-y-2">
            <Label>Icon</Label>
            <div className="flex items-center gap-2 mb-2">
              <Input
                placeholder="Type or paste any emoji..."
                value={customEmoji}
                onChange={(e) => {
                  setCustomEmoji(e.target.value);
                  if (e.target.value) {
                    setIcon(e.target.value);
                  }
                }}
                className="flex-1"
              />
              <div
                className="h-10 w-10 rounded-lg flex items-center justify-center text-xl bg-amber-50 border-2 border-amber-200"
              >
                {icon}
              </div>
            </div>
            <p className="text-xs text-amber-700/60 mb-2">Or pick from suggestions:</p>
            <div className="grid grid-cols-10 gap-1">
              {SUGGESTED_EMOJIS.map((emoji) => (
                <motion.button
                  key={emoji}
                  type="button"
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => {
                    setIcon(emoji);
                    setCustomEmoji("");
                  }}
                  className={`h-9 rounded-lg text-lg transition-all ${
                    icon === emoji
                      ? "bg-gradient-to-r from-amber-500 to-orange-500 shadow-md"
                      : "bg-amber-50 hover:bg-amber-100"
                  }`}
                >
                  {emoji}
                </motion.button>
              ))}
            </div>
          </div>

          <div className="space-y-2">
            <Label>Color</Label>
            <div className="flex gap-2 flex-wrap">
              {COLORS.map((c) => (
                <motion.button
                  key={c}
                  type="button"
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setColor(c)}
                  className={`h-8 w-8 rounded-full transition-all ${
                    color === c ? "ring-2 ring-offset-2 ring-slate-900" : ""
                  }`}
                  style={{ backgroundColor: c }}
                />
              ))}
            </div>
          </div>

          {/* Info about credits */}
          <div className="p-4 bg-amber-50/50 rounded-lg">
            <p className="text-sm text-amber-800/70">
              Earn credits by hitting milestones (7, 14, 30, 50, 100+ days).
              Use credits to skip days without breaking your streak!
            </p>
          </div>

          <div className="flex gap-3">
            <Button
              type="button"
              variant="outline"
              className="flex-1"
              onClick={() => onOpenChange(false)}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              className="flex-1 bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-700 hover:to-orange-700"
              disabled={loading}
            >
              {loading ? (
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                  className="h-5 w-5 border-2 border-white border-t-transparent rounded-full"
                />
              ) : (
                "Save Changes"
              )}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}

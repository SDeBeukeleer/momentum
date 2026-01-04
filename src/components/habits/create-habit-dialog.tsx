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
import { IconPicker, HabitIconDisplay } from "./habit-icons";
import { ThemePicker } from "./theme-picker";
import { Coins, Sparkles } from "lucide-react";
import type { Habit, HabitCompletion } from "@prisma/client";
import type { DioramaTheme } from "@/types/diorama";

interface CreateHabitDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onCreated: (habit: Habit & { completions: HabitCompletion[] }) => void;
}

export function CreateHabitDialog({
  open,
  onOpenChange,
  onCreated,
}: CreateHabitDialogProps) {
  const [name, setName] = useState("");
  const [icon, setIcon] = useState("target");
  const [theme, setTheme] = useState<DioramaTheme>("plant");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) {
      toast.error("Please enter a habit name");
      return;
    }

    setLoading(true);

    try {
      const res = await fetch("/api/habits", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: name.trim(),
          icon,
          color: "#00c458", // Default to primary green
          dioramaTheme: theme,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        toast.error(data.error || "Failed to create habit");
        return;
      }

      onCreated({ ...data, completions: [] });
      toast.success("Habit created! Start building your streak");

      // Reset form
      setName("");
      setIcon("target");
      setTheme("plant");
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
            Create New Habit
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
                  Starting fresh
                </p>
              </div>
            </div>
          </div>

          {/* Name */}
          <div className="space-y-2">
            <Label htmlFor="name" className="text-slate-700">
              Habit Name
            </Label>
            <Input
              id="name"
              placeholder="e.g., Morning workout"
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

          {/* Theme Selection */}
          <div className="space-y-3">
            <Label className="text-slate-700">Choose a Theme</Label>
            <ThemePicker value={theme} onChange={setTheme} />
          </div>

          {/* Info about credits */}
          <div className="flex items-start gap-3 p-4 rounded-xl bg-indigo-50 border border-indigo-100">
            <Coins className="h-5 w-5 text-indigo-600 mt-0.5 shrink-0" />
            <div className="space-y-1">
              <p className="text-sm font-medium text-slate-900">
                Earn credits at milestones
              </p>
              <p className="text-xs text-slate-500">
                Hit 7, 14, 30, 50, 100+ days to earn credits. Use them to skip days without breaking your streak!
              </p>
            </div>
          </div>

          {/* Submit */}
          <Button
            type="submit"
            className="w-full h-12 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-medium shadow-lg shadow-indigo-200 transition-all"
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
                <Sparkles className="h-4 w-4 mr-2" />
                Create Habit
              </>
            )}
          </Button>
        </form>
      </DialogContent>
    </Dialog>
  );
}

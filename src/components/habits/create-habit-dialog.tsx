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
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import type { Habit, HabitCompletion } from "@prisma/client";

const SUGGESTED_EMOJIS = [
  "🎯", "💪", "📚", "🧘", "💧", "😴", "🥗", "💻", "✍️", "🎵",
  "🏃", "🚴", "🏊", "🧘‍♀️", "🏋️", "🌱", "🎨", "🎸", "📝", "🧠",
];

const COLORS = [
  "#6366f1", // Indigo
  "#8b5cf6", // Purple
  "#ec4899", // Pink
  "#ef4444", // Red
  "#f97316", // Orange
  "#eab308", // Yellow
  "#22c55e", // Green
  "#14b8a6", // Teal
  "#06b6d4", // Cyan
  "#3b82f6", // Blue
];

const CREDIT_TEMPLATES = [
  { name: "Easy", completions: 5, credits: 1, description: "For beginners" },
  { name: "Standard", completions: 10, credits: 1, description: "Balanced" },
  { name: "Challenging", completions: 20, credits: 1, description: "Serious commitment" },
  { name: "Marathon", completions: 30, credits: 2, description: "High reward" },
];

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
  const [icon, setIcon] = useState("🎯");
  const [color, setColor] = useState("#6366f1");
  const [customEmoji, setCustomEmoji] = useState("");
  const [completionsForCredit, setCompletionsForCredit] = useState(10);
  const [creditsToEarn, setCreditsToEarn] = useState(1);
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
          color,
          completionsForCredit,
          creditsToEarn,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        toast.error(data.error || "Failed to create habit");
        return;
      }

      onCreated({ ...data, completions: [] });
      toast.success("Habit created! Let's build that streak! 🚀");

      // Reset form
      setName("");
      setIcon("🎯");
      setCustomEmoji("");
      setColor("#6366f1");
      setCompletionsForCredit(10);
      setCreditsToEarn(1);
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
          <DialogTitle className="text-xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
            Create New Habit
          </DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Name */}
          <div className="space-y-2">
            <Label htmlFor="name">Habit Name</Label>
            <Input
              id="name"
              placeholder="e.g., Morning workout"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="h-11"
            />
          </div>

          {/* Icon Selection */}
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
                className="h-10 w-10 rounded-lg flex items-center justify-center text-xl bg-slate-100 border-2 border-slate-200"
              >
                {icon}
              </div>
            </div>
            <p className="text-xs text-slate-500 mb-2">Or pick from suggestions:</p>
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
                      ? "bg-gradient-to-r from-indigo-500 to-purple-600 shadow-md"
                      : "bg-slate-100 hover:bg-slate-200"
                  }`}
                >
                  {emoji}
                </motion.button>
              ))}
            </div>
          </div>

          {/* Color Selection */}
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

          {/* Credit System */}
          <div className="space-y-3">
            <Label>Credit System</Label>
            <Tabs defaultValue="templates" className="w-full">
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="templates">Templates</TabsTrigger>
                <TabsTrigger value="custom">Custom</TabsTrigger>
              </TabsList>

              <TabsContent value="templates" className="space-y-2 mt-3">
                {CREDIT_TEMPLATES.map((template) => (
                  <motion.button
                    key={template.name}
                    type="button"
                    whileTap={{ scale: 0.98 }}
                    onClick={() => {
                      setCompletionsForCredit(template.completions);
                      setCreditsToEarn(template.credits);
                    }}
                    className={`w-full p-3 rounded-lg text-left transition-all ${
                      completionsForCredit === template.completions &&
                      creditsToEarn === template.credits
                        ? "bg-gradient-to-r from-indigo-50 to-purple-50 border-2 border-indigo-300"
                        : "bg-slate-50 border-2 border-transparent hover:border-slate-200"
                    }`}
                  >
                    <div className="flex justify-between items-center">
                      <span className="font-medium">{template.name}</span>
                      <span className="text-sm text-slate-500">
                        {template.completions} completions = {template.credits} credit
                      </span>
                    </div>
                    <p className="text-xs text-slate-500 mt-1">
                      {template.description}
                    </p>
                  </motion.button>
                ))}
              </TabsContent>

              <TabsContent value="custom" className="space-y-4 mt-3">
                <div className="space-y-2">
                  <Label htmlFor="completions">Completions for credit</Label>
                  <Input
                    id="completions"
                    type="number"
                    min={1}
                    value={completionsForCredit}
                    onChange={(e) =>
                      setCompletionsForCredit(parseInt(e.target.value) || 1)
                    }
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="credits">Credits earned</Label>
                  <Input
                    id="credits"
                    type="number"
                    min={1}
                    value={creditsToEarn}
                    onChange={(e) =>
                      setCreditsToEarn(parseInt(e.target.value) || 1)
                    }
                  />
                </div>
              </TabsContent>
            </Tabs>
          </div>

          {/* Preview */}
          <div className="p-4 bg-slate-50 rounded-lg">
            <p className="text-sm text-slate-600">
              Complete this habit <strong>{completionsForCredit}</strong> times to earn{" "}
              <strong>{creditsToEarn}</strong> credit{creditsToEarn > 1 ? "s" : ""}. Use
              credits to skip days without breaking your streak!
            </p>
          </div>

          {/* Submit */}
          <Button
            type="submit"
            className="w-full h-11 bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700"
            disabled={loading}
          >
            {loading ? (
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                className="h-5 w-5 border-2 border-white border-t-transparent rounded-full"
              />
            ) : (
              "Create Habit"
            )}
          </Button>
        </form>
      </DialogContent>
    </Dialog>
  );
}

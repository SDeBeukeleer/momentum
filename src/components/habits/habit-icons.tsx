"use client";

import {
  Target,
  Dumbbell,
  BookOpen,
  Brain,
  Droplets,
  Moon,
  Salad,
  Code,
  PenTool,
  Music,
  Footprints,
  Bike,
  Waves,
  Heart,
  Flame,
  Sprout,
  Palette,
  Guitar,
  NotebookPen,
  Sparkles,
  Coffee,
  Sun,
  Zap,
  Trophy,
  type LucideIcon,
} from "lucide-react";
import { cn } from "@/lib/utils";

export const HABIT_ICONS: { id: string; icon: LucideIcon; label: string }[] = [
  { id: "target", icon: Target, label: "Target" },
  { id: "dumbbell", icon: Dumbbell, label: "Exercise" },
  { id: "book", icon: BookOpen, label: "Reading" },
  { id: "brain", icon: Brain, label: "Learning" },
  { id: "droplets", icon: Droplets, label: "Hydration" },
  { id: "moon", icon: Moon, label: "Sleep" },
  { id: "salad", icon: Salad, label: "Nutrition" },
  { id: "code", icon: Code, label: "Coding" },
  { id: "pen", icon: PenTool, label: "Writing" },
  { id: "music", icon: Music, label: "Music" },
  { id: "footprints", icon: Footprints, label: "Walking" },
  { id: "bike", icon: Bike, label: "Cycling" },
  { id: "waves", icon: Waves, label: "Swimming" },
  { id: "heart", icon: Heart, label: "Wellness" },
  { id: "flame", icon: Flame, label: "Fitness" },
  { id: "sprout", icon: Sprout, label: "Growth" },
  { id: "palette", icon: Palette, label: "Art" },
  { id: "guitar", icon: Guitar, label: "Practice" },
  { id: "notebook", icon: NotebookPen, label: "Journal" },
  { id: "sparkles", icon: Sparkles, label: "Mindfulness" },
  { id: "coffee", icon: Coffee, label: "Morning" },
  { id: "sun", icon: Sun, label: "Energy" },
  { id: "zap", icon: Zap, label: "Productivity" },
  { id: "trophy", icon: Trophy, label: "Goals" },
];

export function getHabitIcon(iconId: string): LucideIcon {
  const found = HABIT_ICONS.find((i) => i.id === iconId);
  return found?.icon || Target;
}

interface HabitIconDisplayProps {
  iconId: string;
  size?: "sm" | "md" | "lg";
  className?: string;
  glowing?: boolean;
}

export function HabitIconDisplay({
  iconId,
  size = "md",
  className,
  glowing = false,
}: HabitIconDisplayProps) {
  const Icon = getHabitIcon(iconId);

  const sizeClasses = {
    sm: "h-8 w-8",
    md: "h-12 w-12",
    lg: "h-16 w-16",
  };

  const iconSizes = {
    sm: "h-4 w-4",
    md: "h-6 w-6",
    lg: "h-8 w-8",
  };

  return (
    <div
      className={cn(
        "relative rounded-xl bg-gradient-to-br from-indigo-100 to-indigo-50 flex items-center justify-center",
        sizeClasses[size],
        glowing && "shadow-lg shadow-indigo-200",
        className
      )}
    >
      <div className="absolute inset-0 rounded-xl border border-indigo-200" />
      <Icon className={cn("text-indigo-600", iconSizes[size])} />
      {glowing && (
        <div className="absolute inset-0 rounded-xl bg-indigo-100/50 animate-pulse" />
      )}
    </div>
  );
}

interface IconPickerProps {
  value: string;
  onChange: (iconId: string) => void;
}

export function IconPicker({ value, onChange }: IconPickerProps) {
  return (
    <div className="grid grid-cols-6 gap-2">
      {HABIT_ICONS.map(({ id, icon: Icon, label }) => (
        <button
          key={id}
          type="button"
          onClick={() => onChange(id)}
          className={cn(
            "relative h-11 w-11 rounded-xl flex items-center justify-center transition-all",
            value === id
              ? "bg-indigo-100 border-2 border-indigo-500 shadow-lg shadow-indigo-200"
              : "bg-slate-50 border border-slate-200 hover:bg-slate-100 hover:border-indigo-300"
          )}
          title={label}
        >
          <Icon
            className={cn(
              "h-5 w-5 transition-colors",
              value === id ? "text-indigo-600" : "text-slate-400"
            )}
          />
          {value === id && (
            <div className="absolute inset-0 rounded-xl bg-indigo-50 animate-pulse" />
          )}
        </button>
      ))}
    </div>
  );
}

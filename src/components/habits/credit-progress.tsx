"use client";

import { motion } from "framer-motion";
import { Gift, Sparkles } from "lucide-react";
import { getNextMilestone, getMilestoneProgress, MILESTONES } from "@/types/diorama";

interface CreditProgressProps {
  currentStreak: number;
  className?: string;
  showLabel?: boolean;
  compact?: boolean;
}

export function CreditProgress({
  currentStreak,
  className = "",
  showLabel = true,
  compact = false
}: CreditProgressProps) {
  const nextMilestone = getNextMilestone(currentStreak);
  const progress = getMilestoneProgress(currentStreak);

  // Don't show if no next milestone (reached max)
  if (!nextMilestone) {
    return (
      <div className={`flex items-center gap-2 text-xs ${className}`}>
        <Sparkles className="h-3.5 w-3.5 text-amber-500" />
        <span className="text-slate-600 font-medium">Max milestone reached!</span>
      </div>
    );
  }

  // Find previous milestone for calculating days in current segment
  const prevMilestoneDay = [...MILESTONES].reverse().find(m => m <= currentStreak) ?? 0;
  const daysIntoSegment = currentStreak - prevMilestoneDay;
  const daysTotal = nextMilestone.day - prevMilestoneDay;
  const daysRemaining = nextMilestone.day - currentStreak;

  // Determine if close to milestone (within 20% of segment)
  const isClose = progress >= 0.8;

  if (compact) {
    return (
      <div className={`flex items-center gap-2 ${className}`}>
        <div className="flex-1 h-1.5 bg-slate-100 rounded-full overflow-hidden">
          <motion.div
            className={`h-full rounded-full ${isClose ? 'bg-amber-500' : 'bg-indigo-500'}`}
            initial={{ width: 0 }}
            animate={{ width: `${progress * 100}%` }}
            transition={{ duration: 0.5, ease: "easeOut" }}
          />
        </div>
        <span className="text-xs text-slate-500 tabular-nums">
          {daysRemaining}d
        </span>
      </div>
    );
  }

  return (
    <div className={`space-y-1.5 ${className}`}>
      {showLabel && (
        <div className="flex items-center justify-between text-xs">
          <div className="flex items-center gap-1.5 text-slate-600">
            <Gift className={`h-3.5 w-3.5 ${isClose ? 'text-amber-500' : 'text-slate-400'}`} />
            <span>
              {isClose ? (
                <span className="text-amber-600 font-medium">
                  {daysRemaining} day{daysRemaining !== 1 ? 's' : ''} to +{nextMilestone.bonusCredits} credit{nextMilestone.bonusCredits > 1 ? 's' : ''}!
                </span>
              ) : (
                <>Day {daysIntoSegment}/{daysTotal} to {nextMilestone.name}</>
              )}
            </span>
          </div>
          <span className="text-slate-400 tabular-nums">
            +{nextMilestone.bonusCredits}
          </span>
        </div>
      )}

      <div className="relative h-2 bg-slate-100 rounded-full overflow-hidden">
        <motion.div
          className={`absolute inset-y-0 left-0 rounded-full ${
            isClose
              ? 'bg-gradient-to-r from-amber-400 to-amber-500'
              : 'bg-gradient-to-r from-indigo-500 to-indigo-600'
          }`}
          initial={{ width: 0 }}
          animate={{ width: `${progress * 100}%` }}
          transition={{ duration: 0.5, ease: "easeOut" }}
        />
        {isClose && (
          <motion.div
            className="absolute inset-y-0 left-0 rounded-full bg-gradient-to-r from-transparent via-white/40 to-transparent"
            initial={{ width: 0 }}
            animate={{
              width: `${progress * 100}%`,
              x: ['-100%', '100%']
            }}
            transition={{
              width: { duration: 0.5 },
              x: { duration: 1.5, repeat: Infinity, ease: "linear" }
            }}
            style={{ width: `${progress * 100}%` }}
          />
        )}
      </div>
    </div>
  );
}

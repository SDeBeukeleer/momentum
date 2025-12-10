"use client";

import { useRef, useState } from "react";
import html2canvas from "html2canvas";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Flame, Trophy, Target, Download, Share2, Sparkles } from "lucide-react";
import type { Habit, HabitCompletion } from "@prisma/client";

interface ShareCardProps {
  habits: (Habit & { completions: HabitCompletion[] })[];
  userName?: string;
}

export function ShareCard({ habits, userName = "User" }: ShareCardProps) {
  const cardRef = useRef<HTMLDivElement>(null);
  const [downloading, setDownloading] = useState(false);
  const [dialogOpen, setDialogOpen] = useState(false);

  // Calculate stats
  const totalCompletions = habits.reduce(
    (sum, h) => sum + h.completions.length,
    0
  );
  const longestStreak = Math.max(...habits.map((h) => h.longestStreak), 0);
  const currentStreaks = habits.filter((h) => h.currentStreak > 0).length;
  const totalCredits = habits.reduce((sum, h) => sum + h.currentCredits, 0);

  // Get week's completions
  const weekStart = new Date();
  weekStart.setDate(weekStart.getDate() - 7);
  const thisWeekCompletions = habits.reduce((sum, h) => {
    return (
      sum +
      h.completions.filter((c) => new Date(c.date) >= weekStart).length
    );
  }, 0);

  const handleDownload = async () => {
    if (!cardRef.current) return;

    setDownloading(true);
    try {
      const canvas = await html2canvas(cardRef.current, {
        scale: 2,
        backgroundColor: null,
        useCORS: true,
      });

      const link = document.createElement("a");
      link.download = `momentum-stats-${new Date().toISOString().split("T")[0]}.png`;
      link.href = canvas.toDataURL("image/png");
      link.click();
    } catch (error) {
      console.error("Failed to generate image:", error);
    } finally {
      setDownloading(false);
    }
  };

  const handleShare = async () => {
    if (!cardRef.current) return;

    setDownloading(true);
    try {
      const canvas = await html2canvas(cardRef.current, {
        scale: 2,
        backgroundColor: null,
        useCORS: true,
      });

      canvas.toBlob(async (blob) => {
        if (!blob) return;

        const file = new File([blob], "momentum-stats.png", {
          type: "image/png",
        });

        if (navigator.share && navigator.canShare({ files: [file] })) {
          await navigator.share({
            files: [file],
            title: "My Momentum Progress",
            text: `Check out my habit tracking progress! ${longestStreak} day best streak!`,
          });
        } else {
          // Fallback to download
          handleDownload();
        }
        setDownloading(false);
      });
    } catch (error) {
      console.error("Failed to share:", error);
      setDownloading(false);
    }
  };

  return (
    <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
      <DialogTrigger asChild>
        <Button variant="outline" className="gap-2">
          <Share2 className="h-4 w-4" />
          Share Progress
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Share Your Progress</DialogTitle>
        </DialogHeader>

        {/* Shareable Card */}
        <div className="flex justify-center py-4">
          <div
            ref={cardRef}
            className="w-80 p-6 rounded-2xl bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-500"
          >
            {/* Header */}
            <div className="flex items-center gap-3 mb-6">
              <div className="h-12 w-12 rounded-xl bg-white/20 backdrop-blur flex items-center justify-center">
                <Sparkles className="h-6 w-6 text-white" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-white">Momentum</h3>
                <p className="text-sm text-white/70">{userName}&apos;s Progress</p>
              </div>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-2 gap-4 mb-6">
              <div className="bg-white/10 backdrop-blur rounded-xl p-4 text-center">
                <Flame className="h-6 w-6 mx-auto text-orange-300 mb-2" />
                <div className="text-3xl font-bold text-white">
                  {longestStreak}
                </div>
                <div className="text-xs text-white/70">Best Streak</div>
              </div>
              <div className="bg-white/10 backdrop-blur rounded-xl p-4 text-center">
                <Trophy className="h-6 w-6 mx-auto text-amber-300 mb-2" />
                <div className="text-3xl font-bold text-white">
                  {totalCredits}
                </div>
                <div className="text-xs text-white/70">Credits Earned</div>
              </div>
              <div className="bg-white/10 backdrop-blur rounded-xl p-4 text-center">
                <Target className="h-6 w-6 mx-auto text-green-300 mb-2" />
                <div className="text-3xl font-bold text-white">
                  {totalCompletions}
                </div>
                <div className="text-xs text-white/70">Completions</div>
              </div>
              <div className="bg-white/10 backdrop-blur rounded-xl p-4 text-center">
                <Flame className="h-6 w-6 mx-auto text-red-300 mb-2" />
                <div className="text-3xl font-bold text-white">
                  {currentStreaks}
                </div>
                <div className="text-xs text-white/70">Active Streaks</div>
              </div>
            </div>

            {/* This Week */}
            <div className="bg-white/10 backdrop-blur rounded-xl p-4 text-center">
              <div className="text-2xl font-bold text-white">
                {thisWeekCompletions} habits
              </div>
              <div className="text-sm text-white/70">completed this week</div>
            </div>

            {/* Footer */}
            <div className="mt-6 text-center">
              <p className="text-xs text-white/50">
                Track your habits with Momentum
              </p>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-3">
          <Button
            onClick={handleDownload}
            disabled={downloading}
            className="flex-1 gap-2"
            variant="outline"
          >
            <Download className="h-4 w-4" />
            {downloading ? "Generating..." : "Download"}
          </Button>
          <Button
            onClick={handleShare}
            disabled={downloading}
            className="flex-1 gap-2"
          >
            <Share2 className="h-4 w-4" />
            {downloading ? "Generating..." : "Share"}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}

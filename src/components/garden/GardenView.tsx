'use client';

import { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { DioramaDisplay, TimelineScrubber, useDioramaPreloader } from '@/components/diorama-display';
import { MILESTONES, MILESTONE_CONFIGS, getNextMilestone, getMilestoneProgress } from '@/types/diorama';
import { Flame, ChevronLeft, ChevronRight, Sparkles, Gift } from 'lucide-react';

interface HabitData {
  id: string;
  name: string;
  color: string;
  streak: number;
  plantStage: number;
  worldTier: number;
}

interface GardenViewProps {
  habits: HabitData[];
  selectedHabitId?: string;
}

export function GardenView({ habits, selectedHabitId }: GardenViewProps) {
  const [currentIndex, setCurrentIndex] = useState(() => {
    const index = habits.findIndex(h => h.id === selectedHabitId);
    return index >= 0 ? index : 0;
  });

  const [displayDay, setDisplayDay] = useState(() => {
    const habit = habits.find(h => h.id === selectedHabitId) || habits[0];
    return Math.max(1, habit?.streak || 1);
  });

  // Get current habit
  const currentHabit = habits[currentIndex];

  // Preload nearby images for smooth scrubbing
  useDioramaPreloader({
    currentDay: displayDay,
    preloadRadius: 10,
    enabled: !!currentHabit,
  });

  if (habits.length === 0) {
    return (
      <Card className="p-8 text-center">
        <Sparkles className="w-12 h-12 mx-auto text-amber-300 mb-4" />
        <h3 className="text-lg font-semibold text-amber-950 mb-2">No habits yet</h3>
        <p className="text-amber-800/70">
          Create your first habit to start growing your garden!
        </p>
      </Card>
    );
  }

  const milestoneProgress = getMilestoneProgress(currentHabit.streak);

  // Find next milestone with full config
  const nextMilestone = getNextMilestone(currentHabit.streak);
  const daysToNextMilestone = nextMilestone ? nextMilestone.day - currentHabit.streak : null;

  // Check if viewing current streak or a different day
  const isViewingCurrentDay = displayDay === Math.max(1, currentHabit.streak);

  const goToPrevious = () => {
    setCurrentIndex(prev => (prev - 1 + habits.length) % habits.length);
    // Reset display day to new habit's streak
    const newIndex = (currentIndex - 1 + habits.length) % habits.length;
    setDisplayDay(Math.max(1, habits[newIndex].streak));
  };

  const goToNext = () => {
    setCurrentIndex(prev => (prev + 1) % habits.length);
    // Reset display day to new habit's streak
    const newIndex = (currentIndex + 1) % habits.length;
    setDisplayDay(Math.max(1, habits[newIndex].streak));
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Main Diorama View */}
      <Card className="lg:col-span-2 overflow-hidden">
        <div className="relative bg-gradient-to-b from-amber-50/50 to-white p-4">
          <div className="flex justify-center">
            <DioramaDisplay
              day={displayDay}
              size="full"
              habitColor={currentHabit.color}
              animate={isViewingCurrentDay}
              showGlow={true}
              priority={true}
            />
          </div>

          {/* Navigation arrows for multiple habits */}
          {habits.length > 1 && (
            <>
              <Button
                variant="ghost"
                size="icon"
                className="absolute left-2 top-1/2 -translate-y-1/2 bg-white/80 hover:bg-white"
                onClick={goToPrevious}
              >
                <ChevronLeft className="w-5 h-5" />
              </Button>
              <Button
                variant="ghost"
                size="icon"
                className="absolute right-2 top-1/2 -translate-y-1/2 bg-white/80 hover:bg-white"
                onClick={goToNext}
              >
                <ChevronRight className="w-5 h-5" />
              </Button>
            </>
          )}

          {/* Viewing past day indicator */}
          {!isViewingCurrentDay && (
            <div className="absolute top-3 left-3 bg-gradient-to-r from-amber-500 to-orange-500 text-white px-3 py-1 rounded-full text-sm font-medium">
              Day {displayDay}
            </div>
          )}
        </div>

        {/* Timeline Scrubber - always visible */}
        <TimelineScrubber
          currentStreak={currentHabit.streak}
          displayDay={displayDay}
          onDayChange={setDisplayDay}
        />
      </Card>

      {/* Stats Panel */}
      <div className="space-y-4">
        {/* Current Habit Info */}
        <Card className="p-4">
          <div className="flex items-center gap-3 mb-4">
            <div
              className="w-4 h-4 rounded-full"
              style={{ backgroundColor: currentHabit.color }}
            />
            <h2 className="font-semibold text-lg text-amber-950">{currentHabit.name}</h2>
          </div>

          <div className="flex items-center gap-2 mb-4">
            <Flame className="w-5 h-5 text-orange-500" />
            <span className="text-2xl font-bold text-amber-950">{currentHabit.streak}</span>
            <span className="text-amber-800/70">day streak</span>
          </div>

          {!isViewingCurrentDay && (
            <div className="text-sm text-amber-700/60">
              Viewing day {displayDay} of your journey
            </div>
          )}
        </Card>

        {/* Next Milestone */}
        {nextMilestone && daysToNextMilestone !== null && (
          <Card className="p-4">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-2xl">{nextMilestone.emoji}</span>
              <h3 className="font-medium text-amber-950">{nextMilestone.name}</h3>
            </div>
            <div className="flex items-baseline gap-2 mb-3">
              <span className="text-3xl font-bold text-green-700">
                {daysToNextMilestone}
              </span>
              <span className="text-amber-800/70">days to go</span>
            </div>
            <div className="w-full bg-amber-100 rounded-full h-2">
              <div
                className="bg-green-600 h-2 rounded-full transition-all"
                style={{ width: `${milestoneProgress * 100}%` }}
              />
            </div>
            <div className="flex items-center justify-between mt-2">
              <p className="text-sm text-amber-700/60">
                Day {nextMilestone.day}
              </p>
              <div className="flex items-center gap-1 text-sm text-amber-600">
                <Gift className="w-3.5 h-3.5" />
                <span>+{nextMilestone.bonusCredits} credit{nextMilestone.bonusCredits > 1 ? 's' : ''}</span>
              </div>
            </div>
          </Card>
        )}

        {/* Habit Selector */}
        {habits.length > 1 && (
          <Card className="p-4">
            <h3 className="font-medium text-amber-950 mb-3">Your Habits</h3>
            <div className="space-y-2">
              {habits.map((habit, index) => (
                <button
                  key={habit.id}
                  onClick={() => {
                    setCurrentIndex(index);
                    setDisplayDay(Math.max(1, habit.streak));
                  }}
                  className={`w-full flex items-center gap-3 p-2 rounded-lg transition-colors ${
                    index === currentIndex
                      ? 'bg-amber-100/50'
                      : 'hover:bg-amber-50'
                  }`}
                >
                  <div
                    className="w-3 h-3 rounded-full"
                    style={{ backgroundColor: habit.color }}
                  />
                  <span className="flex-1 text-left text-sm">{habit.name}</span>
                  <span className="text-sm text-amber-700/60">
                    {habit.streak} days
                  </span>
                </button>
              ))}
            </div>
          </Card>
        )}

        {/* Milestone Reference */}
        <Card className="p-4">
          <h3 className="font-medium text-amber-950 mb-3">Milestones</h3>
          <div className="space-y-2">
            {MILESTONES.map((day) => {
              const config = MILESTONE_CONFIGS[day];
              const reached = currentHabit.streak >= day;
              return (
                <div
                  key={day}
                  className={`flex items-center gap-2 p-2 rounded-lg text-sm ${
                    reached
                      ? 'bg-green-50 text-green-700'
                      : 'bg-amber-50 text-amber-700/60'
                  }`}
                >
                  <span className={reached ? '' : 'grayscale opacity-50'}>{config.emoji}</span>
                  <span className="flex-1">Day {day}</span>
                  <span className="text-xs flex items-center gap-1">
                    <Gift className="w-3 h-3" />
                    +{config.bonusCredits}
                  </span>
                </div>
              );
            })}
          </div>
        </Card>
      </div>
    </div>
  );
}

'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { DioramaDisplay, TimelineScrubber, useDioramaPreloader } from '@/components/diorama-display';
import { MILESTONES, MILESTONE_CONFIGS, getNextMilestone, getMilestoneProgress } from '@/types/diorama';
import { Flame, ChevronLeft, ChevronRight, Gift, Leaf } from 'lucide-react';
import { motion } from 'framer-motion';

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

  const currentHabit = habits[currentIndex];

  useDioramaPreloader({
    currentDay: displayDay,
    preloadRadius: 10,
    enabled: !!currentHabit,
  });

  if (habits.length === 0) {
    return (
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-12 text-center">
        <div className="relative h-20 w-20 mx-auto mb-6">
          <div className="absolute inset-0 rounded-full bg-indigo-100 animate-pulse" />
          <div className="absolute inset-2 rounded-full bg-indigo-50 flex items-center justify-center">
            <Leaf className="h-8 w-8 text-indigo-500" />
          </div>
        </div>
        <h3 className="text-lg font-semibold text-slate-900 mb-2" style={{ fontFamily: 'var(--font-fraunces)' }}>
          Your garden awaits
        </h3>
        <p className="text-slate-500">
          Create your first habit to start growing your garden!
        </p>
      </div>
    );
  }

  const milestoneProgress = getMilestoneProgress(currentHabit.streak);
  const nextMilestone = getNextMilestone(currentHabit.streak);
  const daysToNextMilestone = nextMilestone ? nextMilestone.day - currentHabit.streak : null;
  const isViewingCurrentDay = displayDay === Math.max(1, currentHabit.streak);

  const goToPrevious = () => {
    setCurrentIndex(prev => (prev - 1 + habits.length) % habits.length);
    const newIndex = (currentIndex - 1 + habits.length) % habits.length;
    setDisplayDay(Math.max(1, habits[newIndex].streak));
  };

  const goToNext = () => {
    setCurrentIndex(prev => (prev + 1) % habits.length);
    const newIndex = (currentIndex + 1) % habits.length;
    setDisplayDay(Math.max(1, habits[newIndex].streak));
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
      {/* Main Diorama View */}
      <motion.div
        className="lg:col-span-2 bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="relative p-6 bg-gradient-to-b from-indigo-50/50 to-transparent">
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

          {/* Navigation arrows */}
          {habits.length > 1 && (
            <>
              <Button
                variant="ghost"
                size="icon"
                className="absolute left-4 top-1/2 -translate-y-1/2 bg-white/80 hover:bg-white border border-slate-200 shadow-sm"
                onClick={goToPrevious}
              >
                <ChevronLeft className="w-5 h-5" />
              </Button>
              <Button
                variant="ghost"
                size="icon"
                className="absolute right-4 top-1/2 -translate-y-1/2 bg-white/80 hover:bg-white border border-slate-200 shadow-sm"
                onClick={goToNext}
              >
                <ChevronRight className="w-5 h-5" />
              </Button>
            </>
          )}

          {/* Day indicator */}
          {!isViewingCurrentDay && (
            <Badge className="absolute top-4 left-4 bg-indigo-600 text-white">
              Day {displayDay}
            </Badge>
          )}
        </div>

        <TimelineScrubber
          currentStreak={currentHabit.streak}
          displayDay={displayDay}
          onDayChange={setDisplayDay}
        />
      </motion.div>

      {/* Stats Panel */}
      <div className="space-y-4">
        {/* Current Habit Info */}
        <motion.div
          className="bg-white rounded-2xl border border-slate-200 shadow-sm p-5"
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.1 }}
        >
          <div className="flex items-center gap-3 mb-4">
            <div
              className="w-4 h-4 rounded-full shadow-lg"
              style={{ backgroundColor: currentHabit.color, boxShadow: `0 0 12px ${currentHabit.color}60` }}
            />
            <h2 className="font-semibold text-lg text-slate-900" style={{ fontFamily: 'var(--font-fraunces)' }}>
              {currentHabit.name}
            </h2>
          </div>

          <div className="flex items-center gap-2 mb-4">
            <Flame className="w-6 h-6 text-indigo-600" />
            <span className="text-3xl font-bold text-indigo-600">{currentHabit.streak}</span>
            <span className="text-slate-500">day streak</span>
          </div>

          {!isViewingCurrentDay && (
            <div className="text-sm text-slate-500">
              Viewing day {displayDay} of your journey
            </div>
          )}
        </motion.div>

        {/* Next Milestone */}
        {nextMilestone && daysToNextMilestone !== null && (
          <motion.div
            className="bg-white rounded-2xl border border-slate-200 shadow-sm p-5"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
          >
            <div className="flex items-center gap-2 mb-3">
              <span className="text-2xl">{nextMilestone.emoji}</span>
              <h3 className="font-medium text-slate-900">{nextMilestone.name}</h3>
            </div>
            <div className="flex items-baseline gap-2 mb-3">
              <span className="text-3xl font-bold text-indigo-600">
                {daysToNextMilestone}
              </span>
              <span className="text-slate-500">days to go</span>
            </div>
            <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
              <motion.div
                className="bg-gradient-to-r from-indigo-500 to-indigo-600 h-full rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${milestoneProgress * 100}%` }}
                transition={{ duration: 0.5 }}
              />
            </div>
            <div className="flex items-center justify-between mt-3">
              <p className="text-sm text-slate-500">
                Day {nextMilestone.day}
              </p>
              <div className="flex items-center gap-1 text-sm text-amber-500">
                <Gift className="w-4 h-4" />
                <span>+{nextMilestone.bonusCredits} credit{nextMilestone.bonusCredits > 1 ? 's' : ''}</span>
              </div>
            </div>
          </motion.div>
        )}

        {/* Habit Selector */}
        {habits.length > 1 && (
          <motion.div
            className="bg-white rounded-2xl border border-slate-200 shadow-sm p-5"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
          >
            <h3 className="font-medium text-slate-900 mb-3">Your Habits</h3>
            <div className="space-y-2">
              {habits.map((habit, index) => (
                <button
                  key={habit.id}
                  onClick={() => {
                    setCurrentIndex(index);
                    setDisplayDay(Math.max(1, habit.streak));
                  }}
                  className={`w-full flex items-center gap-3 p-3 rounded-xl transition-all ${
                    index === currentIndex
                      ? 'bg-indigo-50 border border-indigo-200'
                      : 'hover:bg-slate-50'
                  }`}
                >
                  <div
                    className="w-3 h-3 rounded-full"
                    style={{ backgroundColor: habit.color }}
                  />
                  <span className="flex-1 text-left text-sm text-slate-900">{habit.name}</span>
                  <span className="text-sm text-slate-500">
                    {habit.streak} days
                  </span>
                </button>
              ))}
            </div>
          </motion.div>
        )}

        {/* Milestone Reference */}
        <motion.div
          className="bg-white rounded-2xl border border-slate-200 shadow-sm p-5"
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4 }}
        >
          <h3 className="font-medium text-slate-900 mb-3">Milestones</h3>
          <div className="space-y-2">
            {MILESTONES.map((day) => {
              const config = MILESTONE_CONFIGS[day];
              const reached = currentHabit.streak >= day;
              return (
                <div
                  key={day}
                  className={`flex items-center gap-2 p-2.5 rounded-xl text-sm transition-all ${
                    reached
                      ? 'bg-indigo-50 text-indigo-600'
                      : 'bg-slate-50 text-slate-400'
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
        </motion.div>
      </div>
    </div>
  );
}

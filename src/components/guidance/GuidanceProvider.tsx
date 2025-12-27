'use client';

import { createContext, useContext, type ReactNode } from 'react';
import { GuidancePopup } from './GuidancePopup';
import { useGuidance } from './useGuidance';

interface GuidanceContextType {
  onHabitCreated: () => void;
  onHabitCompleted: (newStreak: number) => void;
  showStreakAtRisk: (streakLength: number) => void;
}

const GuidanceContext = createContext<GuidanceContextType | null>(null);

interface GuidanceProviderProps {
  children: ReactNode;
  habitCount?: number;
  maxStreak?: number;
  totalCredits?: number;
}

export function GuidanceProvider({
  children,
  habitCount = 0,
  maxStreak = 0,
  totalCredits = 0,
}: GuidanceProviderProps) {
  const {
    currentGuidance,
    dismissGuidance,
    onHabitCreated,
    onHabitCompleted,
    showStreakAtRisk,
  } = useGuidance({
    habitCount,
    maxStreak,
    totalCredits,
  });

  return (
    <GuidanceContext.Provider
      value={{
        onHabitCreated,
        onHabitCompleted,
        showStreakAtRisk,
      }}
    >
      {children}
      <GuidancePopup guidance={currentGuidance} onDismiss={dismissGuidance} />
    </GuidanceContext.Provider>
  );
}

export function useGuidanceContext() {
  const context = useContext(GuidanceContext);
  if (!context) {
    throw new Error('useGuidanceContext must be used within a GuidanceProvider');
  }
  return context;
}

'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import type { GuidanceMessage } from './GuidancePopup';
import {
  type GuidanceKey,
  getGuidanceMessage,
  getMilestoneGuidanceKey
} from './guidance-definitions';

interface GuidanceState {
  shownKeys: string[];
  shownToday: number;
  isLoading: boolean;
}

interface UseGuidanceOptions {
  // Current app state for triggering guidance
  habitCount?: number;
  hasCompletedToday?: boolean;
  maxStreak?: number;
  totalCredits?: number;
  hasVisitedGarden?: boolean;
  streakAtRisk?: boolean;
  justCompletedStreak?: number; // Streak length when just completed
  isReturningAfterBreak?: boolean;
}

const DAILY_LIMIT = 2;

export function useGuidance(options: UseGuidanceOptions = {}) {
  const router = useRouter();
  const [state, setState] = useState<GuidanceState>({
    shownKeys: [],
    shownToday: 0,
    isLoading: true,
  });
  const [currentGuidance, setCurrentGuidance] = useState<GuidanceMessage | null>(null);
  const [pendingGuidance, setPendingGuidance] = useState<GuidanceKey | null>(null);

  // Fetch shown guidance keys on mount
  useEffect(() => {
    const fetchGuidance = async () => {
      try {
        const res = await fetch('/api/guidance');
        if (res.ok) {
          const data = await res.json();
          setState({
            shownKeys: data.shownKeys,
            shownToday: data.shownToday,
            isLoading: false,
          });
        }
      } catch {
        setState((prev) => ({ ...prev, isLoading: false }));
      }
    };

    fetchGuidance();
  }, []);

  // Check if guidance can be shown
  const canShowGuidance = useCallback(
    (key: GuidanceKey): boolean => {
      if (state.isLoading) return false;
      if (state.shownToday >= DAILY_LIMIT) return false;
      if (state.shownKeys.includes(key)) return false;
      return true;
    },
    [state]
  );

  // Mark guidance as shown
  const markAsShown = useCallback(async (key: GuidanceKey) => {
    try {
      const res = await fetch('/api/guidance', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ guidanceKey: key }),
      });

      if (res.ok) {
        setState((prev) => ({
          ...prev,
          shownKeys: [...prev.shownKeys, key],
          shownToday: prev.shownToday + 1,
        }));
      }
    } catch {
      // Silently fail
    }
  }, []);

  // Show a specific guidance
  const showGuidance = useCallback(
    (key: GuidanceKey) => {
      if (!canShowGuidance(key)) return false;

      const message = getGuidanceMessage(key);

      // Add navigation handlers
      if (key === 'onboarding_first_habit_created') {
        message.secondaryAction = {
          label: 'Visit Garden',
          onClick: () => router.push('/garden'),
        };
      }
      if (key === 'milestone_14' || key === 'feature_garden_discovery') {
        message.secondaryAction = {
          label: 'See My Garden',
          onClick: () => router.push('/garden'),
        };
      }
      if (key === 'feature_garden_discovery') {
        message.primaryAction = {
          label: 'Visit Garden',
          onClick: () => router.push('/garden'),
        };
      }

      setCurrentGuidance(message);
      markAsShown(key);
      return true;
    },
    [canShowGuidance, markAsShown, router]
  );

  // Dismiss current guidance
  const dismissGuidance = useCallback(() => {
    setCurrentGuidance(null);

    // Show pending guidance if any
    if (pendingGuidance) {
      setTimeout(() => {
        showGuidance(pendingGuidance);
        setPendingGuidance(null);
      }, 500);
    }
  }, [pendingGuidance, showGuidance]);

  // Trigger guidance based on current state
  const checkTriggers = useCallback(() => {
    if (state.isLoading) return;

    const {
      habitCount = 0,
      maxStreak = 0,
      totalCredits = 0,
      hasVisitedGarden = true, // Default true to avoid spam
      justCompletedStreak,
      isReturningAfterBreak = false,
    } = options;

    // Priority 1: Milestone celebrations (triggered by justCompletedStreak)
    if (justCompletedStreak) {
      const milestoneKey = getMilestoneGuidanceKey(justCompletedStreak);
      if (milestoneKey && canShowGuidance(milestoneKey)) {
        showGuidance(milestoneKey);
        return;
      }
    }

    // Priority 2: First completion
    if (justCompletedStreak === 1 && canShowGuidance('onboarding_first_completion')) {
      showGuidance('onboarding_first_completion');
      return;
    }

    // Priority 3: No habits (onboarding)
    if (habitCount === 0 && canShowGuidance('onboarding_no_habits')) {
      showGuidance('onboarding_no_habits');
      return;
    }

    // Priority 4: Returning after break
    if (isReturningAfterBreak && canShowGuidance('welcome_back')) {
      showGuidance('welcome_back');
      return;
    }

    // Priority 5: First credit earned (discovered after getting credits)
    if (totalCredits > 0 && canShowGuidance('feature_first_credit')) {
      showGuidance('feature_first_credit');
      return;
    }

    // Priority 6: Garden discovery (has 3+ day streak, hasn't visited garden)
    if (maxStreak >= 3 && !hasVisitedGarden && canShowGuidance('feature_garden_discovery')) {
      showGuidance('feature_garden_discovery');
      return;
    }
  }, [state.isLoading, options, canShowGuidance, showGuidance]);

  // Run triggers when state or options change
  useEffect(() => {
    checkTriggers();
  }, [checkTriggers]);

  // Trigger guidance after habit creation
  const onHabitCreated = useCallback(() => {
    if (canShowGuidance('onboarding_first_habit_created')) {
      showGuidance('onboarding_first_habit_created');
    }
  }, [canShowGuidance, showGuidance]);

  // Trigger guidance after completion (with streak number)
  const onHabitCompleted = useCallback(
    (newStreak: number) => {
      // Check for milestone first
      const milestoneKey = getMilestoneGuidanceKey(newStreak);
      if (milestoneKey && canShowGuidance(milestoneKey)) {
        showGuidance(milestoneKey);
        return;
      }

      // First completion
      if (newStreak === 1 && canShowGuidance('onboarding_first_completion')) {
        showGuidance('onboarding_first_completion');
      }
    },
    [canShowGuidance, showGuidance]
  );

  // Trigger streak at risk warning
  const showStreakAtRisk = useCallback(
    (streakLength: number) => {
      if (canShowGuidance('streak_at_risk')) {
        const message = getGuidanceMessage('streak_at_risk');
        message.message = `You've got a ${streakLength}-day streak going! There's still time today to keep it alive. Your future self will thank you.`;
        setCurrentGuidance(message);
        markAsShown('streak_at_risk');
      }
    },
    [canShowGuidance, markAsShown]
  );

  return {
    currentGuidance,
    dismissGuidance,
    showGuidance,
    onHabitCreated,
    onHabitCompleted,
    showStreakAtRisk,
    canShowGuidance,
    isLoading: state.isLoading,
    shownToday: state.shownToday,
  };
}

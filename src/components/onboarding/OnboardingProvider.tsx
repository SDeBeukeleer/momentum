'use client';

import { createContext, useContext, useState, useEffect, useCallback, type ReactNode } from 'react';
import { AnimatePresence } from 'framer-motion';
import { WelcomeScreen } from './WelcomeScreen';
import { Spotlight } from './Spotlight';
import { GuidancePopup } from '@/components/guidance/GuidancePopup';
import {
  type OnboardingStep,
  ONBOARDING_STEPS,
  getNextOnboardingStep,
  isOnboardingComplete,
} from './onboarding-steps';

interface OnboardingContextType {
  isOnboardingActive: boolean;
  currentStep: OnboardingStep | null;
  completedSteps: string[];
  completeStep: () => void;
  skipOnboarding: () => void;
  // Triggers for habit actions
  onHabitCreated: () => void;
  onHabitCompleted: () => void;
}

const OnboardingContext = createContext<OnboardingContextType | null>(null);

export function useOnboarding() {
  const context = useContext(OnboardingContext);
  if (!context) {
    throw new Error('useOnboarding must be used within an OnboardingProvider');
  }
  return context;
}

interface OnboardingProviderProps {
  children: ReactNode;
  habitCount?: number;
  hasCompletedToday?: boolean;
}

export function OnboardingProvider({
  children,
  habitCount = 0,
  hasCompletedToday = false,
}: OnboardingProviderProps) {
  const [isLoading, setIsLoading] = useState(true);
  const [hasCompletedOnboarding, setHasCompletedOnboarding] = useState(true); // Default true to avoid flash
  const [completedSteps, setCompletedSteps] = useState<string[]>([]);
  const [currentStep, setCurrentStep] = useState<OnboardingStep | null>(null);
  const [localHabitCount, setLocalHabitCount] = useState(habitCount);
  const [localHasCompletedToday, setLocalHasCompletedToday] = useState(hasCompletedToday);

  // Update local state when props change
  useEffect(() => {
    setLocalHabitCount(habitCount);
  }, [habitCount]);

  useEffect(() => {
    setLocalHasCompletedToday(hasCompletedToday);
  }, [hasCompletedToday]);

  // Fetch onboarding state on mount
  useEffect(() => {
    const fetchOnboardingState = async () => {
      try {
        const res = await fetch('/api/onboarding');
        if (res.ok) {
          const data = await res.json();
          setHasCompletedOnboarding(data.hasCompletedOnboarding);
          setCompletedSteps(data.completedSteps || []);
        }
      } catch {
        // Silently fail - default to completed onboarding
      } finally {
        setIsLoading(false);
      }
    };

    fetchOnboardingState();
  }, []);

  // Determine current step when state changes
  useEffect(() => {
    if (isLoading || hasCompletedOnboarding) {
      setCurrentStep(null);
      return;
    }

    const nextStep = getNextOnboardingStep(
      completedSteps,
      localHabitCount,
      localHasCompletedToday
    );
    setCurrentStep(nextStep);
  }, [isLoading, hasCompletedOnboarding, completedSteps, localHabitCount, localHasCompletedToday]);

  // Complete the current step
  const completeStep = useCallback(async () => {
    if (!currentStep) return;

    const newCompletedSteps = [...completedSteps, currentStep.id];
    setCompletedSteps(newCompletedSteps);

    // Check if onboarding is complete
    if (isOnboardingComplete(newCompletedSteps)) {
      setHasCompletedOnboarding(true);
    }

    // Persist to API
    try {
      await fetch('/api/onboarding', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          stepId: currentStep.id,
          isComplete: isOnboardingComplete(newCompletedSteps),
        }),
      });
    } catch {
      // Silently fail
    }
  }, [currentStep, completedSteps]);

  // Skip onboarding entirely
  const skipOnboarding = useCallback(async () => {
    setHasCompletedOnboarding(true);
    setCurrentStep(null);

    try {
      await fetch('/api/onboarding', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ skip: true }),
      });
    } catch {
      // Silently fail
    }
  }, []);

  // Trigger when habit is created
  const onHabitCreated = useCallback(() => {
    setLocalHabitCount((prev) => prev + 1);
  }, []);

  // Trigger when habit is completed
  const onHabitCompleted = useCallback(() => {
    setLocalHasCompletedToday(true);
  }, []);

  const value: OnboardingContextType = {
    isOnboardingActive: !hasCompletedOnboarding && currentStep !== null,
    currentStep,
    completedSteps,
    completeStep,
    skipOnboarding,
    onHabitCreated,
    onHabitCompleted,
  };

  return (
    <OnboardingContext.Provider value={value}>
      {children}

      <AnimatePresence>
        {/* Welcome Screen */}
        {currentStep?.type === 'welcome' && (
          <WelcomeScreen onGetStarted={completeStep} />
        )}

        {/* Spotlight */}
        {currentStep?.type === 'spotlight' && currentStep.targetSelector && (
          <Spotlight
            targetSelector={currentStep.targetSelector}
            title={currentStep.title}
            message={currentStep.message}
            position={currentStep.position}
            onDismiss={completeStep}
            buttonLabel={currentStep.buttonLabel}
          />
        )}

        {/* Guidance Popup */}
        {currentStep?.type === 'guidance' && (
          <GuidancePopup
            guidance={{
              key: currentStep.id,
              title: currentStep.title,
              message: currentStep.message,
              emoji: currentStep.emoji,
              primaryAction: {
                label: currentStep.buttonLabel || 'Got it!',
              },
              celebrate: true,
            }}
            onDismiss={completeStep}
          />
        )}
      </AnimatePresence>
    </OnboardingContext.Provider>
  );
}

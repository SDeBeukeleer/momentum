// Onboarding step definitions

export type OnboardingStepType = 'welcome' | 'spotlight' | 'guidance';

export interface OnboardingStep {
  id: string;
  type: OnboardingStepType;
  // For spotlight type
  targetSelector?: string;
  position?: 'top' | 'bottom' | 'left' | 'right';
  // Common
  title: string;
  message: string;
  emoji?: string;
  buttonLabel?: string;
  // Trigger condition - what needs to happen before showing this step
  trigger?: 'immediate' | 'habit_created' | 'habit_completed';
}

export const ONBOARDING_STEPS: OnboardingStep[] = [
  {
    id: 'welcome',
    type: 'welcome',
    title: 'Welcome to Momentum',
    message: 'Build lasting habits with visual progress',
    trigger: 'immediate',
  },
  {
    id: 'create_habit_spotlight',
    type: 'spotlight',
    targetSelector: '[data-onboarding="create-habit-button"]',
    position: 'top',
    title: 'Create Your First Habit',
    message: 'Start by adding a habit you want to track daily. Tap this button to begin!',
    buttonLabel: 'Got it!',
    trigger: 'immediate',
  },
  {
    id: 'habit_card_spotlight',
    type: 'spotlight',
    targetSelector: '[data-onboarding="habit-card"]',
    position: 'bottom',
    title: 'Complete Your Habit',
    message: 'Tap your habit card to mark it complete for today and start building your streak!',
    buttonLabel: 'Let\'s go!',
    trigger: 'habit_created',
  },
  {
    id: 'diorama_explanation',
    type: 'guidance',
    title: 'Your Progress Comes to Life',
    emoji: '✨',
    message: 'As your streak grows, tap your habit card to watch your visual journey evolve into something amazing!',
    buttonLabel: 'Amazing!',
    trigger: 'habit_completed',
  },
];

// Get the next step based on current progress
export function getNextOnboardingStep(
  completedSteps: string[],
  habitCount: number,
  hasCompletedToday: boolean
): OnboardingStep | null {
  for (const step of ONBOARDING_STEPS) {
    // Skip already completed steps
    if (completedSteps.includes(step.id)) continue;

    // Check trigger conditions
    switch (step.trigger) {
      case 'immediate':
        return step;
      case 'habit_created':
        if (habitCount > 0) return step;
        break;
      case 'habit_completed':
        if (hasCompletedToday) return step;
        break;
    }
  }

  return null;
}

// Check if onboarding is complete
export function isOnboardingComplete(completedSteps: string[]): boolean {
  return ONBOARDING_STEPS.every((step) => completedSteps.includes(step.id));
}

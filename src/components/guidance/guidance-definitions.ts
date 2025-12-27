import type { GuidanceMessage } from './GuidancePopup';

// All guidance keys - used for tracking what's been shown
export type GuidanceKey =
  // Onboarding
  | 'onboarding_no_habits'
  | 'onboarding_first_habit_created'
  | 'onboarding_first_completion'
  // Milestones
  | 'milestone_3'
  | 'milestone_7'
  | 'milestone_14'
  | 'milestone_21'
  | 'milestone_30'
  | 'milestone_50'
  | 'milestone_100'
  | 'milestone_150'
  | 'milestone_200'
  // Feature discovery
  | 'feature_first_credit'
  | 'feature_garden_discovery'
  // Re-engagement
  | 'streak_at_risk'
  | 'welcome_back';

// Guidance message definitions
export const GUIDANCE_MESSAGES: Record<GuidanceKey, Omit<GuidanceMessage, 'key'>> = {
  // === ONBOARDING ===
  onboarding_no_habits: {
    title: "Let's Plant Your First Seed",
    emoji: '🌱',
    message: "Every great journey starts with a single step. Create your first habit and watch it grow into something beautiful.",
    primaryAction: {
      label: 'Create My First Habit',
    },
    celebrate: false,
  },

  onboarding_first_habit_created: {
    title: 'Your Garden Awaits',
    emoji: '🌿',
    message: "As your streak grows, so does your garden. Each day you show up, your plant evolves into something more beautiful. Check it out anytime!",
    primaryAction: {
      label: 'Start Tracking',
    },
    secondaryAction: {
      label: 'Visit Garden',
    },
    celebrate: true,
  },

  onboarding_first_completion: {
    title: 'Day One Complete!',
    emoji: '🎉',
    message: "The hardest part is starting. You just did that. Come back tomorrow to keep your streak alive!",
    primaryAction: {
      label: 'Got it!',
    },
    celebrate: true,
  },

  // === MILESTONES ===
  milestone_3: {
    title: 'Three Days Strong',
    emoji: '💪',
    message: "You're building momentum! Studies show it takes about 21 days to form a habit. You're already 14% of the way there!",
    primaryAction: {
      label: 'Keep Going!',
    },
    celebrate: true,
  },

  milestone_7: {
    title: 'One Week Champion!',
    emoji: '🌱',
    message: "A full week of showing up! You just earned your first credit. Use it to skip a day without breaking your streak - life happens, and now you're covered.",
    primaryAction: {
      label: 'Amazing!',
    },
    celebrate: true,
  },

  milestone_14: {
    title: 'Two Weeks!',
    emoji: '🌿',
    message: "You're officially in habit-forming territory. Your garden is flourishing - have you checked it lately?",
    primaryAction: {
      label: 'Keep Going!',
    },
    secondaryAction: {
      label: 'See My Garden',
    },
    celebrate: true,
  },

  milestone_21: {
    title: 'Habit Formed!',
    emoji: '🧠',
    message: "21 days - scientists say this is when habits start to stick. This isn't just something you do anymore. It's who you are.",
    primaryAction: {
      label: 'I Am Unstoppable!',
    },
    celebrate: true,
  },

  milestone_30: {
    title: 'One Month Legend',
    emoji: '🌳',
    message: "30 days of showing up. That's not luck - that's dedication. You've earned 2 more credits for this milestone!",
    primaryAction: {
      label: 'Incredible!',
    },
    celebrate: true,
  },

  milestone_50: {
    title: 'Fifty Days!',
    emoji: '✨',
    message: "Halfway to 100! You've proven this habit is part of your life now. The garden shows your incredible journey.",
    primaryAction: {
      label: 'Onwards!',
    },
    celebrate: true,
  },

  milestone_100: {
    title: 'Century Club!',
    emoji: '🏆',
    message: "100 days. One hundred. You've joined an elite group of people who don't just try things - they become them. Legendary!",
    primaryAction: {
      label: 'I Am Legend!',
    },
    celebrate: true,
  },

  milestone_150: {
    title: 'Master Level!',
    emoji: '👑',
    message: "150 days of dedication. At this point, NOT doing this habit would feel strange. You've truly mastered consistency.",
    primaryAction: {
      label: 'Bow Down!',
    },
    celebrate: true,
  },

  milestone_200: {
    title: 'Transcendent!',
    emoji: '🌟',
    message: "200 days. Your garden has reached its ultimate form. You've achieved what most only dream of. You are the habit.",
    primaryAction: {
      label: 'Enlightened!',
    },
    celebrate: true,
  },

  // === FEATURE DISCOVERY ===
  feature_first_credit: {
    title: 'You Have a Safety Net',
    emoji: '🛡️',
    message: "That credit you earned? Tap 'Skip' on any day to use it. Your streak stays safe, and you get a guilt-free rest day when life gets busy.",
    primaryAction: {
      label: 'Got It!',
    },
    celebrate: false,
  },

  feature_garden_discovery: {
    title: 'Your Garden is Growing',
    emoji: '🌱',
    message: "Your streak is alive in the garden! Watch your progress bloom into a living scene that evolves with every day you show up.",
    primaryAction: {
      label: 'Visit Garden',
    },
    celebrate: false,
  },

  // === RE-ENGAGEMENT ===
  streak_at_risk: {
    title: "Don't Break the Chain!",
    emoji: '🔥',
    message: "You've got a streak going! There's still time today to keep it alive. Your future self will thank you.",
    primaryAction: {
      label: 'Complete Now',
    },
    secondaryAction: {
      label: 'Remind Later',
    },
    celebrate: false,
  },

  welcome_back: {
    title: 'Welcome Back, Champion',
    emoji: '🌅',
    message: "Streaks end. Habits don't have to. The best time to start again is right now. Your garden is ready to grow again.",
    primaryAction: {
      label: "Let's Go!",
    },
    celebrate: false,
  },
};

// Helper to get full guidance message with key
export function getGuidanceMessage(key: GuidanceKey): GuidanceMessage {
  return {
    key,
    ...GUIDANCE_MESSAGES[key],
  };
}

// Milestone days that trigger guidance
export const MILESTONE_GUIDANCE_DAYS = [3, 7, 14, 21, 30, 50, 100, 150, 200] as const;

// Get milestone guidance key for a streak day
export function getMilestoneGuidanceKey(day: number): GuidanceKey | null {
  if (day === 3) return 'milestone_3';
  if (day === 7) return 'milestone_7';
  if (day === 14) return 'milestone_14';
  if (day === 21) return 'milestone_21';
  if (day === 30) return 'milestone_30';
  if (day === 50) return 'milestone_50';
  if (day === 100) return 'milestone_100';
  if (day === 150) return 'milestone_150';
  if (day === 200) return 'milestone_200';
  return null;
}

// Living Diorama Types - Image-based visualization of habit streaks

// Available diorama themes
export const DIORAMA_THEMES = ['plant', 'car', 'spaceship'] as const;
export type DioramaTheme = (typeof DIORAMA_THEMES)[number];

export interface ThemeConfig {
  id: DioramaTheme;
  name: string;
  description: string;
  emoji: string;
  folder: string;
  maxDays: number;
  previewDay: number; // Day to show in preview
}

export const THEME_CONFIGS: Record<DioramaTheme, ThemeConfig> = {
  plant: {
    id: 'plant',
    name: 'Growing Garden',
    description: 'Watch a plant grow from seed to flourishing garden',
    emoji: '🌱',
    folder: 'final',
    maxDays: 200,
    previewDay: 50,
  },
  car: {
    id: 'car',
    name: 'Car Restoration',
    description: 'Restore a rusty Porsche into a championship race car',
    emoji: '🏎️',
    folder: 'v13-auto-anchor-nobg',
    maxDays: 200,
    previewDay: 100,
  },
  spaceship: {
    id: 'spaceship',
    name: 'Spaceship Builder',
    description: 'Build a spaceship piece by piece',
    emoji: '🚀',
    folder: 'v14-spaceship-nobg',
    maxDays: 130,
    previewDay: 65,
  },
};

// Get theme config by ID
export function getThemeConfig(theme: DioramaTheme): ThemeConfig {
  return THEME_CONFIGS[theme] ?? THEME_CONFIGS.plant;
}

// Get diorama image path for a theme and day
export function getDioramaPath(theme: DioramaTheme, day: number): string {
  const config = getThemeConfig(theme);
  const clampedDay = Math.max(1, Math.min(config.maxDays, day));
  const paddedDay = clampedDay.toString().padStart(3, '0');
  return `/diorama/${config.folder}/day-${paddedDay}.png`;
}

// Simplified plant stages for display purposes
export const PLANT_STAGES = [
  'seed',
  'sprout',
  'seedling',
  'young',
  'mature',
  'flourishing',
  'ancient',
  'mythic',
] as const;

export type PlantStage = (typeof PLANT_STAGES)[number];

// Milestone days for celebrations and bonus credits
export const MILESTONES = [7, 14, 30, 50, 100, 150, 200] as const;
export type MilestoneDay = (typeof MILESTONES)[number];

export interface MilestoneConfig {
  day: number;
  name: string;
  emoji: string;
  description: string;
  bonusCredits: number;
}

export const MILESTONE_CONFIGS: Record<MilestoneDay, MilestoneConfig> = {
  7: {
    day: 7,
    name: 'First Week',
    emoji: '🌱',
    description: 'One week strong!',
    bonusCredits: 1,
  },
  14: {
    day: 14,
    name: 'Two Weeks',
    emoji: '🌿',
    description: 'Two weeks of dedication!',
    bonusCredits: 1,
  },
  30: {
    day: 30,
    name: 'One Month',
    emoji: '🌳',
    description: 'A full month - habit formed!',
    bonusCredits: 2,
  },
  50: {
    day: 50,
    name: 'Fifty Days',
    emoji: '✨',
    description: 'Halfway to 100!',
    bonusCredits: 2,
  },
  100: {
    day: 100,
    name: 'Century Club',
    emoji: '🏆',
    description: '100 days - legendary!',
    bonusCredits: 5,
  },
  150: {
    day: 150,
    name: 'Master',
    emoji: '👑',
    description: '150 days of mastery!',
    bonusCredits: 5,
  },
  200: {
    day: 200,
    name: 'Transcendent',
    emoji: '🌟',
    description: 'Maximum evolution achieved!',
    bonusCredits: 10,
  },
};

// Starting day for each plant stage (for display label purposes)
export const STAGE_START_DAYS: Record<number, number> = {
  0: 0,   // seed
  1: 3,   // sprout
  2: 7,   // seedling
  3: 14,  // young
  4: 30,  // mature
  5: 50,  // flourishing
  6: 100, // ancient
  7: 150, // mythic
};

// Helper to get the next milestone for a given streak
export function getNextMilestone(currentStreak: number): MilestoneConfig | null {
  for (const day of MILESTONES) {
    if (day > currentStreak) {
      return MILESTONE_CONFIGS[day];
    }
  }
  return null;
}

// Helper to check if a streak just hit a milestone
export function checkMilestoneReached(newStreak: number): MilestoneConfig | null {
  if (MILESTONES.includes(newStreak as MilestoneDay)) {
    return MILESTONE_CONFIGS[newStreak as MilestoneDay];
  }
  return null;
}

// Helper to get plant stage index from streak (for display label)
export function getPlantStageForStreak(streak: number): number {
  let stage = 0;
  for (let i = 0; i < PLANT_STAGES.length; i++) {
    const startDay = STAGE_START_DAYS[i] ?? 0;
    if (streak >= startDay) {
      stage = i;
    }
  }
  return stage;
}

// Helper to calculate progress towards next milestone (0-1)
export function getMilestoneProgress(currentStreak: number): number {
  let prevMilestone: number = 0;
  let nextMilestone: number = MILESTONES[0];

  for (let i = 0; i < MILESTONES.length; i++) {
    const milestone = MILESTONES[i] as number;
    if (milestone <= currentStreak) {
      prevMilestone = milestone;
      nextMilestone = (MILESTONES[i + 1] as number | undefined) ?? milestone;
    } else {
      nextMilestone = milestone;
      break;
    }
  }

  if (prevMilestone === nextMilestone) {
    return 1; // Max milestone reached
  }

  const range = nextMilestone - prevMilestone;
  const progress = currentStreak - prevMilestone;
  return Math.min(1, progress / range);
}

// Get all milestones reached for a given streak
export function getMilestonesReached(streak: number): MilestoneConfig[] {
  return MILESTONES
    .filter(day => day <= streak)
    .map(day => MILESTONE_CONFIGS[day]);
}

import { prisma } from "@/lib/prisma";

// Get yesterday at UTC midnight based on local date
function getYesterdayUTC(): Date {
  const now = new Date();
  return new Date(Date.UTC(now.getFullYear(), now.getMonth(), now.getDate() - 1));
}

// Get today at UTC midnight based on local date
function getTodayUTC(): Date {
  const now = new Date();
  return new Date(Date.UTC(now.getFullYear(), now.getMonth(), now.getDate()));
}

// Convert a Date to UTC midnight
function toUTCMidnight(date: Date): Date {
  return new Date(Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate()));
}

/**
 * Check if a habit's streak is still valid.
 * If yesterday wasn't completed (and today isn't completed yet), reset streak and completionCount.
 */
export async function checkAndResetStreakIfNeeded(habitId: string): Promise<void> {
  const habit = await prisma.habit.findUnique({
    where: { id: habitId },
  });

  if (!habit || habit.currentStreak === 0) return;

  const today = getTodayUTC();
  const yesterday = getYesterdayUTC();

  // Check if completed today
  const todayCompletion = await prisma.habitCompletion.findUnique({
    where: {
      habitId_date: {
        habitId,
        date: today,
      },
    },
  });

  // If completed today, streak is fine
  if (todayCompletion) return;

  // Check if completed yesterday
  const yesterdayCompletion = await prisma.habitCompletion.findUnique({
    where: {
      habitId_date: {
        habitId,
        date: yesterday,
      },
    },
  });

  // If yesterday was completed, streak is still valid (user just hasn't completed today yet)
  if (yesterdayCompletion) return;

  // Check lastCompletedAt - if it's before yesterday, streak should be reset
  if (habit.lastCompletedAt) {
    const lastCompletedMidnight = toUTCMidnight(habit.lastCompletedAt);

    // If last completion was yesterday or today, streak is fine
    if (lastCompletedMidnight.getTime() >= yesterday.getTime()) {
      return;
    }
  }

  // Streak is broken - reset both streak and completionCount
  await prisma.habit.update({
    where: { id: habitId },
    data: {
      currentStreak: 0,
      completionCount: 0,
    },
  });
}

/**
 * Check all habits for a user and reset streaks if needed
 */
export async function checkAndResetAllStreaks(userId: string): Promise<void> {
  const habits = await prisma.habit.findMany({
    where: {
      userId,
      isArchived: false,
      currentStreak: { gt: 0 }, // Only check habits with active streaks
    },
    select: { id: true },
  });

  // Check each habit
  await Promise.all(habits.map((h) => checkAndResetStreakIfNeeded(h.id)));
}

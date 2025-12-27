import { NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import { getMilestonesReached } from "@/types/diorama";

// Get today at UTC midnight
function getTodayUTC(): Date {
  const now = new Date();
  return new Date(Date.UTC(now.getFullYear(), now.getMonth(), now.getDate()));
}

// Get UTC midnight from a Date
function toUTCMidnight(date: Date): Date {
  return new Date(Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate()));
}

export async function POST(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const session = await auth();
  const { id } = await params;

  if (!session?.user?.id) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const habit = await prisma.habit.findFirst({
    where: {
      id,
      userId: session.user.id,
    },
  });

  if (!habit) {
    return NextResponse.json({ error: "Habit not found" }, { status: 404 });
  }

  // Get all completions for this habit
  const allCompletions = await prisma.habitCompletion.findMany({
    where: { habitId: id },
    orderBy: { date: "desc" },
  });

  const today = getTodayUTC();

  // Calculate current streak from today backwards
  let currentStreak = 0;
  let checkDate = new Date(today);

  for (let i = 0; i < 365; i++) {
    const hasCompletion = allCompletions.some(
      (c) => toUTCMidnight(c.date).getTime() === checkDate.getTime()
    );

    if (hasCompletion) {
      currentStreak++;
      // Move to previous day in UTC
      checkDate = new Date(Date.UTC(
        checkDate.getUTCFullYear(),
        checkDate.getUTCMonth(),
        checkDate.getUTCDate() - 1
      ));
    } else {
      break;
    }
  }

  // Calculate credits based on milestones reached
  const milestonesReached = getMilestonesReached(currentStreak);
  const creditsFromMilestones = milestonesReached.reduce((sum, m) => sum + m.bonusCredits, 0);

  // Keep existing credits if they're higher (user already earned them before)
  const newCredits = Math.max(habit.currentCredits, creditsFromMilestones);

  // Update habit with recalculated values
  const updatedHabit = await prisma.habit.update({
    where: { id },
    data: {
      currentStreak,
      longestStreak: Math.max(habit.longestStreak, currentStreak),
      currentCredits: newCredits,
      lastCompletedAt: allCompletions[0]?.date || null,
    },
  });

  return NextResponse.json({
    habit: updatedHabit,
    recalculated: {
      previousCredits: habit.currentCredits,
      newCredits,
      previousStreak: habit.currentStreak,
      newStreak: currentStreak,
      milestonesReached: milestonesReached.length,
    },
  });
}

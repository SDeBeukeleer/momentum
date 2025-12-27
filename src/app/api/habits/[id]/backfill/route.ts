import { NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import { getMilestonesReached } from "@/types/diorama";

// Parse "YYYY-MM-DD" string to UTC midnight Date
function parseLocalDateString(dateStr: string): Date {
  const [year, month, day] = dateStr.split('-').map(Number);
  return new Date(Date.UTC(year, month - 1, day));
}

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

  const body = await request.json();
  const { dates } = body; // Array of date strings

  if (!dates || !Array.isArray(dates)) {
    return NextResponse.json({ error: "Dates array required" }, { status: 400 });
  }

  const today = getTodayUTC();
  const completions = [];

  for (const dateStr of dates) {
    const date = parseLocalDateString(dateStr);

    // Don't allow future dates
    if (date > today) continue;

    // Check if already exists
    const existing = await prisma.habitCompletion.findUnique({
      where: {
        habitId_date: {
          habitId: id,
          date,
        },
      },
    });

    if (!existing) {
      const completion = await prisma.habitCompletion.create({
        data: {
          habitId: id,
          date,
          skipped: false,
        },
      });
      completions.push(completion);
    }
  }

  // Recalculate streak and credits
  const allCompletions = await prisma.habitCompletion.findMany({
    where: { habitId: id },
    orderBy: { date: "desc" },
  });

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
  const currentCredits = Math.max(habit.currentCredits, creditsFromMilestones);

  // Update habit stats
  const updatedHabit = await prisma.habit.update({
    where: { id },
    data: {
      currentStreak,
      longestStreak: Math.max(habit.longestStreak, currentStreak),
      currentCredits,
      lastCompletedAt: allCompletions[0]?.date || null,
    },
  });

  return NextResponse.json({
    completions,
    habit: updatedHabit,
  });
}

export async function DELETE(
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

  const body = await request.json();
  const { date } = body;

  if (!date) {
    return NextResponse.json({ error: "Date required" }, { status: 400 });
  }

  const targetDate = parseLocalDateString(date);

  await prisma.habitCompletion.deleteMany({
    where: {
      habitId: id,
      date: targetDate,
    },
  });

  // Recalculate streak
  const allCompletions = await prisma.habitCompletion.findMany({
    where: { habitId: id },
    orderBy: { date: "desc" },
  });

  const today = getTodayUTC();
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

  // Don't reduce credits when removing completions (they keep earned credits)
  await prisma.habit.update({
    where: { id },
    data: {
      currentStreak,
      // Keep existing credits (don't reduce)
      lastCompletedAt: allCompletions[0]?.date || null,
    },
  });

  return NextResponse.json({ success: true });
}

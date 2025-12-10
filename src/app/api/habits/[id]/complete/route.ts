import { NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { prisma } from "@/lib/prisma";

// Get today at UTC midnight based on local date
function getTodayUTC(): Date {
  const now = new Date();
  return new Date(Date.UTC(now.getFullYear(), now.getMonth(), now.getDate()));
}

// Get yesterday at UTC midnight based on local date
function getYesterdayUTC(): Date {
  const now = new Date();
  return new Date(Date.UTC(now.getFullYear(), now.getMonth(), now.getDate() - 1));
}

// Convert a Date to UTC midnight
function toUTCMidnight(date: Date): Date {
  return new Date(Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate()));
}

function isYesterday(date: Date): boolean {
  const yesterday = getYesterdayUTC();
  return toUTCMidnight(date).getTime() === yesterday.getTime();
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

  const today = getTodayUTC();
  const body = await request.json().catch(() => ({}));
  const useCredit = body.useCredit === true;

  // Check if already completed today
  const existingCompletion = await prisma.habitCompletion.findUnique({
    where: {
      habitId_date: {
        habitId: id,
        date: today,
      },
    },
  });

  if (existingCompletion) {
    return NextResponse.json(
      { error: "Already completed today" },
      { status: 400 }
    );
  }

  // If using credit, check if user has credits
  if (useCredit && habit.currentCredits < 1) {
    return NextResponse.json(
      { error: "Not enough credits" },
      { status: 400 }
    );
  }

  // Calculate new streak
  let newStreak = habit.currentStreak;
  let streakBroken = false;

  if (!useCredit) {
    // Check if last completion was yesterday to continue streak
    if (habit.lastCompletedAt && isYesterday(habit.lastCompletedAt)) {
      newStreak = habit.currentStreak + 1;
    } else if (
      habit.lastCompletedAt &&
      toUTCMidnight(habit.lastCompletedAt).getTime() === today.getTime()
    ) {
      // Already completed today, keep streak
      newStreak = habit.currentStreak;
    } else {
      // Streak broken, start fresh
      newStreak = 1;
      streakBroken = true;
    }
  }
  // If using credit, keep current streak

  // Calculate credit progress
  // If streak was broken, reset completionCount to start fresh
  let newCompletionCount = streakBroken ? 1 : habit.completionCount + (useCredit ? 0 : 1);
  let newCredits = useCredit ? habit.currentCredits - 1 : habit.currentCredits;

  // Check if earned a new credit
  if (
    !useCredit &&
    newCompletionCount >= habit.completionsForCredit
  ) {
    newCredits += habit.creditsToEarn;
    newCompletionCount = 0; // Reset counter
  }

  // Create completion and update habit in transaction
  const [completion, updatedHabit] = await prisma.$transaction([
    prisma.habitCompletion.create({
      data: {
        habitId: id,
        date: today,
        skipped: useCredit,
      },
    }),
    prisma.habit.update({
      where: { id },
      data: {
        currentStreak: newStreak,
        longestStreak: Math.max(habit.longestStreak, newStreak),
        lastCompletedAt: today,
        completionCount: newCompletionCount,
        currentCredits: newCredits,
      },
    }),
  ]);

  return NextResponse.json({
    completion,
    habit: updatedHabit,
    creditEarned:
      !useCredit &&
      habit.completionCount + 1 >= habit.completionsForCredit,
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

  const today = getTodayUTC();

  const completion = await prisma.habitCompletion.findUnique({
    where: {
      habitId_date: {
        habitId: id,
        date: today,
      },
    },
  });

  if (!completion) {
    return NextResponse.json(
      { error: "No completion found for today" },
      { status: 404 }
    );
  }

  // Reverse the completion
  let newStreak = Math.max(0, habit.currentStreak - 1);
  let newCompletionCount = habit.completionCount;
  let newCredits = habit.currentCredits;

  if (completion.skipped) {
    // Was a credit skip, restore the credit
    newCredits += 1;
  } else {
    // Was a real completion
    if (newCompletionCount === 0 && newCredits > 0) {
      // They just earned a credit, remove it and restore counter
      newCredits = Math.max(0, newCredits - habit.creditsToEarn);
      newCompletionCount = habit.completionsForCredit - 1;
    } else {
      newCompletionCount = Math.max(0, newCompletionCount - 1);
    }
  }

  await prisma.$transaction([
    prisma.habitCompletion.delete({
      where: { id: completion.id },
    }),
    prisma.habit.update({
      where: { id },
      data: {
        currentStreak: newStreak,
        completionCount: newCompletionCount,
        currentCredits: newCredits,
        lastCompletedAt: null,
      },
    }),
  ]);

  return NextResponse.json({ success: true });
}

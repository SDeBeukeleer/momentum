import { auth } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import { TodayView } from "@/components/habits/today-view";
import { checkAndResetAllStreaks } from "@/lib/streak-checker";

// Always fetch fresh data - don't cache
export const dynamic = "force-dynamic";

// Get today's date range in UTC (based on local date)
function getTodayRangeUTC() {
  const now = new Date();
  const startOfDay = new Date(Date.UTC(now.getFullYear(), now.getMonth(), now.getDate()));
  const endOfDay = new Date(Date.UTC(now.getFullYear(), now.getMonth(), now.getDate() + 1));
  return { startOfDay, endOfDay };
}

export default async function DashboardPage() {
  const session = await auth();
  const { startOfDay, endOfDay } = getTodayRangeUTC();

  // Check and reset any broken streaks before fetching habits
  await checkAndResetAllStreaks(session!.user.id);

  const habits = await prisma.habit.findMany({
    where: {
      userId: session!.user.id,
      isArchived: false,
    },
    include: {
      completions: {
        where: {
          date: {
            gte: startOfDay,
            lt: endOfDay,
          },
        },
      },
    },
    orderBy: { createdAt: "asc" },
  });

  return (
    <TodayView
      habits={habits}
      userName={session!.user.name || "there"}
    />
  );
}

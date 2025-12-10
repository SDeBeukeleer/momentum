import { auth } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import { StatsView } from "@/components/stats/stats-view";

export const dynamic = "force-dynamic";

export default async function StatsPage() {
  const session = await auth();

  const [habits, activities, weightLogs] = await Promise.all([
    prisma.habit.findMany({
      where: { userId: session!.user.id },
      include: { completions: true },
    }),
    prisma.activityLog.findMany({
      where: { userId: session!.user.id },
      orderBy: { date: "desc" },
    }),
    prisma.weightLog.findMany({
      where: { userId: session!.user.id },
      orderBy: { date: "desc" },
    }),
  ]);

  return (
    <StatsView
      habits={habits}
      activities={activities}
      weightLogs={weightLogs}
    />
  );
}

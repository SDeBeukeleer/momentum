import { auth } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import { AchievementsView } from "@/components/achievements/achievements-view";

export const dynamic = "force-dynamic";

export default async function AchievementsPage() {
  const session = await auth();

  const [habits, activities, weightLogs] = await Promise.all([
    prisma.habit.findMany({
      where: { userId: session!.user.id },
      include: { completions: true },
    }),
    prisma.activityLog.findMany({
      where: { userId: session!.user.id },
    }),
    prisma.weightLog.findMany({
      where: { userId: session!.user.id },
    }),
  ]);

  return (
    <AchievementsView
      habits={habits}
      activities={activities}
      weightLogs={weightLogs}
    />
  );
}

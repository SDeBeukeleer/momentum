import { auth } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import { ProgressView } from "@/components/progress/progress-view";

export const dynamic = "force-dynamic";

export default async function ProgressPage() {
  const session = await auth();

  const [habits, weightLogs] = await Promise.all([
    prisma.habit.findMany({
      where: { userId: session!.user.id },
      include: { completions: true },
    }),
    prisma.weightLog.findMany({
      where: { userId: session!.user.id },
      orderBy: { date: "desc" },
    }),
  ]);

  return (
    <ProgressView
      habits={habits}
      weightLogs={weightLogs}
    />
  );
}

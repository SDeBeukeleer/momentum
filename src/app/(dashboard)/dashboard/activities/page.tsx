import { auth } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import { ActivityView } from "@/components/activities/activity-view";

export const dynamic = "force-dynamic";

export default async function ActivitiesPage() {
  const session = await auth();

  const activityLogs = await prisma.activityLog.findMany({
    where: { userId: session!.user.id },
    orderBy: { date: "desc" },
    take: 100,
  });

  return <ActivityView initialLogs={activityLogs} />;
}

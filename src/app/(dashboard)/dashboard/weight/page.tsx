import { auth } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import { WeightView } from "@/components/weight/weight-view";

export const dynamic = "force-dynamic";

export default async function WeightPage() {
  const session = await auth();

  const weightLogs = await prisma.weightLog.findMany({
    where: { userId: session!.user.id },
    orderBy: { date: "desc" },
    take: 90,
  });

  // TODO: Add goal weight to user preferences
  const goalWeight = undefined;

  return <WeightView initialLogs={weightLogs} goalWeight={goalWeight} />;
}

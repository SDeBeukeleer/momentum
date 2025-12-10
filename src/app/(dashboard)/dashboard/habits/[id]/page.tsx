import { auth } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import { notFound } from "next/navigation";
import { HabitDetail } from "@/components/habits/habit-detail";

export default async function HabitDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const session = await auth();
  const { id } = await params;

  const habit = await prisma.habit.findFirst({
    where: {
      id,
      userId: session!.user.id,
    },
    include: {
      completions: {
        orderBy: { date: "desc" },
      },
    },
  });

  if (!habit) {
    notFound();
  }

  return <HabitDetail habit={habit} />;
}

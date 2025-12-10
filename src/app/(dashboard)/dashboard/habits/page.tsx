import { auth } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import { HabitsList } from "@/components/habits/habits-list";

export default async function HabitsPage() {
  const session = await auth();

  const habits = await prisma.habit.findMany({
    where: {
      userId: session!.user.id,
    },
    include: {
      completions: {
        orderBy: { date: "desc" },
        take: 30,
      },
    },
    orderBy: { createdAt: "asc" },
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">My Habits</h1>
        <p className="text-slate-600">
          Manage your habits and track your progress
        </p>
      </div>

      <HabitsList habits={habits} />
    </div>
  );
}

import { auth } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import { GardenView } from "@/components/garden/GardenView";
import { getPlantStageForStreak } from "@/types/diorama";

export default async function GardenPage({
  searchParams,
}: {
  searchParams: Promise<{ habit?: string }>;
}) {
  const session = await auth();
  const params = await searchParams;

  // Fetch all habits
  const habits = await prisma.habit.findMany({
    where: {
      userId: session!.user.id,
    },
    orderBy: { createdAt: "asc" },
  });

  // Map habits to the format GardenView expects
  const habitsWithStreaks = habits.map((habit) => ({
    id: habit.id,
    name: habit.name,
    color: habit.color,
    streak: habit.currentStreak,
    plantStage: getPlantStageForStreak(habit.currentStreak),
    worldTier: 1, // Simplified - no world tiers anymore
  }));

  // Default to first habit or the one specified in query
  const selectedHabitId = params.habit || habits[0]?.id;

  return (
    <div className="space-y-4">
      <div>
        <h1 className="text-2xl font-bold text-amber-950">Garden</h1>
        <p className="text-amber-800/70">
          Watch your habits grow into beautiful dioramas
        </p>
      </div>

      <GardenView
        habits={habitsWithStreaks}
        selectedHabitId={selectedHabitId}
      />
    </div>
  );
}

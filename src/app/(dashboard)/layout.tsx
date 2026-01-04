import { auth } from "@/lib/auth";
import { redirect } from "next/navigation";
import { Toaster } from "@/components/ui/sonner";
import { prisma } from "@/lib/prisma";
import { GuidanceProvider } from "@/components/guidance";
import { OnboardingProvider } from "@/components/onboarding";
import { DashboardShell } from "@/components/layout/dashboard-shell";

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await auth();

  if (!session) {
    redirect("/login");
  }

  // Get today's date for completion check
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  // Fetch data for guidance and onboarding triggers
  const habits = await prisma.habit.findMany({
    where: {
      userId: session.user.id,
      isArchived: false,
    },
    select: {
      currentStreak: true,
      currentCredits: true,
      completions: {
        where: {
          date: today,
        },
        select: { id: true },
      },
    },
  });

  const habitCount = habits.length;
  const maxStreak = Math.max(0, ...habits.map((h) => h.currentStreak));
  const totalCredits = habits.reduce((sum, h) => sum + h.currentCredits, 0);
  const hasCompletedToday = habits.some((h) => h.completions.length > 0);

  return (
    <div className="min-h-screen bg-background">
      <OnboardingProvider
        habitCount={habitCount}
        hasCompletedToday={hasCompletedToday}
      >
        <GuidanceProvider
          habitCount={habitCount}
          maxStreak={maxStreak}
          totalCredits={totalCredits}
        >
          <DashboardShell user={session.user}>
            {children}
          </DashboardShell>
          <Toaster position="top-center" richColors />
        </GuidanceProvider>
      </OnboardingProvider>
    </div>
  );
}

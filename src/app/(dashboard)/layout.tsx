import { auth } from "@/lib/auth";
import { redirect } from "next/navigation";
import { Toaster } from "@/components/ui/sonner";
import { prisma } from "@/lib/prisma";
import { GuidanceProvider } from "@/components/guidance";
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

  // Fetch data for guidance triggers
  const habits = await prisma.habit.findMany({
    where: {
      userId: session.user.id,
      isArchived: false,
    },
    select: {
      currentStreak: true,
      currentCredits: true,
    },
  });

  const habitCount = habits.length;
  const maxStreak = Math.max(0, ...habits.map((h) => h.currentStreak));
  const totalCredits = habits.reduce((sum, h) => sum + h.currentCredits, 0);

  return (
    <div className="min-h-screen bg-background">
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
    </div>
  );
}

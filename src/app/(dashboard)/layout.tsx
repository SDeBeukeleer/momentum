import { auth } from "@/lib/auth";
import { redirect } from "next/navigation";
import { Navbar } from "@/components/layout/navbar";
import { Toaster } from "@/components/ui/sonner";
import { prisma } from "@/lib/prisma";
import { GuidanceProvider } from "@/components/guidance";

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
    <div className="min-h-screen bg-gradient-to-br from-amber-50/50 to-orange-50/30">
      <GuidanceProvider
        habitCount={habitCount}
        maxStreak={maxStreak}
        totalCredits={totalCredits}
      >
        <Navbar user={session.user} />
        <main className="pb-20 md:pb-6 md:pl-64">
          <div className="container mx-auto px-4 py-6">{children}</div>
        </main>
        <Toaster position="top-center" richColors />
      </GuidanceProvider>
    </div>
  );
}

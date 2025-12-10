import { auth } from "@/lib/auth";
import { redirect } from "next/navigation";
import { Navbar } from "@/components/layout/navbar";
import { Toaster } from "@/components/ui/sonner";

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await auth();

  if (!session) {
    redirect("/login");
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      <Navbar user={session.user} />
      <main className="pb-20 md:pb-6 md:pl-64">
        <div className="container mx-auto px-4 py-6">{children}</div>
      </main>
      <Toaster position="top-center" richColors />
    </div>
  );
}

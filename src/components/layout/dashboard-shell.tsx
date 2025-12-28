'use client';

import { Navbar } from './navbar';
import { SwipeNavigation } from './swipe-navigation';

interface DashboardShellProps {
  children: React.ReactNode;
  user: {
    name?: string | null;
    email?: string | null;
  };
}

export function DashboardShell({ children, user }: DashboardShellProps) {
  return (
    <>
      <Navbar user={user} />
      <main className="pb-20 md:pb-6 md:pl-64">
        <SwipeNavigation>
          <div className="container mx-auto px-4 py-6">{children}</div>
        </SwipeNavigation>
      </main>
    </>
  );
}

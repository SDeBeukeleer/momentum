"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { signOut } from "next-auth/react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import {
  Home,
  Scale,
  LogOut,
  User,
  BarChart3,
  Leaf,
} from "lucide-react";

interface NavbarProps {
  user: {
    name?: string | null;
    email?: string | null;
  };
}

const navItems = [
  { href: "/dashboard", label: "Home", icon: Home },
  { href: "/dashboard/weight", label: "Weight", icon: Scale },
  { href: "/dashboard/progress", label: "Progress", icon: BarChart3 },
];

export function Navbar({ user }: NavbarProps) {
  const pathname = usePathname();

  return (
    <>
      {/* Desktop Sidebar */}
      <aside className="hidden md:fixed md:inset-y-0 md:left-0 md:flex md:w-64 md:flex-col">
        <div className="flex min-h-0 flex-1 flex-col bg-white border-r border-slate-200">
          {/* Logo */}
          <div className="flex h-16 items-center px-6 border-b border-slate-200">
            <Link href="/dashboard" className="flex items-center gap-3 group">
              <div className="relative h-10 w-10 rounded-xl bg-indigo-100 flex items-center justify-center overflow-hidden">
                <Leaf className="h-5 w-5 text-indigo-600 transition-transform group-hover:scale-110" />
                <div className="absolute inset-0 bg-indigo-600/10 opacity-0 group-hover:opacity-100 transition-opacity" />
              </div>
              <span className="text-xl font-semibold text-slate-900" style={{ fontFamily: 'var(--font-fraunces)' }}>
                Momentum
              </span>
            </Link>
          </div>

          {/* Navigation */}
          <nav className="flex-1 space-y-1 p-4">
            {navItems.map((item) => {
              const isActive =
                pathname === item.href ||
                (item.href !== "/dashboard" && pathname.startsWith(item.href));
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={cn(
                    "relative flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium transition-all duration-200",
                    isActive
                      ? "bg-indigo-50 text-indigo-600"
                      : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
                  )}
                >
                  {isActive && (
                    <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-indigo-600 rounded-r-full" />
                  )}
                  <item.icon className={cn(
                    "h-5 w-5 transition-colors",
                    isActive ? "text-indigo-600" : "text-slate-500"
                  )} />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </nav>

          {/* User Section */}
          <div className="border-t border-slate-200 p-4">
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button
                  variant="ghost"
                  className="w-full justify-start gap-3 h-auto py-3 px-3 hover:bg-slate-100 rounded-xl"
                >
                  <Avatar className="h-9 w-9 ring-2 ring-indigo-100">
                    <AvatarFallback className="bg-indigo-600 text-white font-semibold">
                      {user.name?.charAt(0) || user.email?.charAt(0) || "U"}
                    </AvatarFallback>
                  </Avatar>
                  <div className="flex flex-col items-start text-sm min-w-0 flex-1">
                    <span className="font-medium truncate w-full text-slate-900">
                      {user.name || "User"}
                    </span>
                    <span className="text-xs text-slate-500 truncate w-full">
                      {user.email}
                    </span>
                  </div>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-56">
                <DropdownMenuItem className="focus:bg-slate-100">
                  <User className="mr-2 h-4 w-4" />
                  Profile
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem
                  className="text-red-600 focus:bg-red-50 focus:text-red-600"
                  onClick={() => signOut({ callbackUrl: "/login" })}
                >
                  <LogOut className="mr-2 h-4 w-4" />
                  Sign out
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </div>
      </aside>

      {/* Mobile Bottom Navigation */}
      <nav className="fixed bottom-0 left-0 right-0 z-50 bg-white border-t border-slate-200 md:hidden safe-area-bottom">
        <div className="flex items-center justify-around h-16 px-2">
          {navItems.map((item) => {
            const isActive =
              pathname === item.href ||
              (item.href !== "/dashboard" && pathname.startsWith(item.href));
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "relative flex flex-col items-center justify-center gap-1 px-4 py-2 rounded-xl transition-all min-w-[60px]",
                  isActive
                    ? "text-indigo-600"
                    : "text-slate-500"
                )}
              >
                {isActive && (
                  <div className="absolute inset-0 bg-indigo-50 rounded-xl" />
                )}
                <item.icon
                  className={cn(
                    "h-5 w-5 relative z-10 transition-transform",
                    isActive && "scale-110"
                  )}
                />
                <span className={cn(
                  "text-xs font-medium relative z-10",
                  isActive && "text-indigo-600"
                )}>
                  {item.label}
                </span>
                {isActive && (
                  <div className="absolute -top-1 left-1/2 -translate-x-1/2 w-8 h-1 bg-indigo-600 rounded-full" />
                )}
              </Link>
            );
          })}
        </div>
      </nav>

      {/* Mobile Header */}
      <header className="sticky top-0 z-40 bg-white border-b border-slate-200 shadow-sm md:hidden">
        <div className="flex items-center justify-between h-14 px-4">
          <Link href="/dashboard" className="flex items-center gap-2">
            <div className="h-8 w-8 rounded-lg bg-indigo-100 flex items-center justify-center">
              <Leaf className="h-4 w-4 text-indigo-600" />
            </div>
            <span className="text-lg font-semibold text-slate-900" style={{ fontFamily: 'var(--font-fraunces)' }}>
              Momentum
            </span>
          </Link>

          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon" className="rounded-full">
                <Avatar className="h-8 w-8 ring-2 ring-indigo-100">
                  <AvatarFallback className="bg-indigo-600 text-white text-sm font-semibold">
                    {user.name?.charAt(0) || user.email?.charAt(0) || "U"}
                  </AvatarFallback>
                </Avatar>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-56">
              <div className="px-3 py-2">
                <p className="text-sm font-medium text-slate-900">{user.name || "User"}</p>
                <p className="text-xs text-slate-500">{user.email}</p>
              </div>
              <DropdownMenuSeparator />
              <DropdownMenuItem className="focus:bg-slate-100">
                <User className="mr-2 h-4 w-4" />
                Profile
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem
                className="text-red-600 focus:bg-red-50 focus:text-red-600"
                onClick={() => signOut({ callbackUrl: "/login" })}
              >
                <LogOut className="mr-2 h-4 w-4" />
                Sign out
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </header>
    </>
  );
}

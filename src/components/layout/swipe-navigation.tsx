'use client';

import { useRef } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { motion, useMotionValue, useTransform, PanInfo } from 'framer-motion';

const navOrder = [
  '/dashboard',
  '/dashboard/weight',
  '/dashboard/progress',
];

interface SwipeNavigationProps {
  children: React.ReactNode;
}

export function SwipeNavigation({ children }: SwipeNavigationProps) {
  const router = useRouter();
  const pathname = usePathname();
  const containerRef = useRef<HTMLDivElement>(null);
  const x = useMotionValue(0);
  const opacity = useTransform(x, [-100, 0, 100], [0.5, 1, 0.5]);

  // Find current index, handling sub-routes
  const currentIndex = navOrder.findIndex((path) => {
    if (path === '/dashboard') {
      return pathname === '/dashboard' || pathname.startsWith('/dashboard/habits');
    }
    return pathname === path || pathname.startsWith(path + '/');
  });

  const handleDragEnd = (_: MouseEvent | TouchEvent | PointerEvent, info: PanInfo) => {
    const threshold = 50;
    const velocity = info.velocity.x;
    const offset = info.offset.x;

    // Swipe right (go to previous tab)
    if ((offset > threshold || velocity > 500) && currentIndex > 0) {
      router.push(navOrder[currentIndex - 1]);
    }
    // Swipe left (go to next tab)
    else if ((offset < -threshold || velocity < -500) && currentIndex < navOrder.length - 1) {
      router.push(navOrder[currentIndex + 1]);
    }
  };

  // Only enable swipe on mobile
  return (
    <motion.div
      ref={containerRef}
      drag="x"
      dragConstraints={{ left: 0, right: 0 }}
      dragElastic={0.1}
      onDragEnd={handleDragEnd}
      style={{ x, opacity }}
      className="min-h-full touch-pan-y md:!transform-none"
    >
      {children}
    </motion.div>
  );
}

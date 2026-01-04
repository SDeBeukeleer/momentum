'use client';

import { useState, useEffect } from 'react';
import Image from 'next/image';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface DioramaDisplayProps {
  day: number;
  size?: 'mini' | 'medium' | 'full';
  animate?: boolean;
  showGlow?: boolean;
  habitColor?: string;
  className?: string;
  priority?: boolean;
}

function getDioramaPath(day: number): string {
  const clampedDay = Math.max(1, Math.min(200, day));
  const paddedDay = clampedDay.toString().padStart(3, '0');

  // TEST: Show isometric platform test for day 75
  if (clampedDay === 75) {
    return `/diorama/isometric-test/day-075.png`;
  }

  return `/diorama/final/day-${paddedDay}.png`;
}

const sizeConfig = {
  mini: {
    width: 80,
    height: 80,
    containerClass: 'w-20 h-20',
    sizes: '80px'
  },
  medium: {
    width: 200,
    height: 200,
    containerClass: 'w-48 h-48',
    sizes: '200px'
  },
  full: {
    width: 600,
    height: 600,
    containerClass: 'w-full aspect-square max-w-[600px]',
    sizes: '(max-width: 768px) 100vw, 600px'
  },
};

export function DioramaDisplay({
  day,
  size = 'full',
  animate = true,
  showGlow = true,
  habitColor = '#d97706',
  className = '',
  priority = false,
}: DioramaDisplayProps) {
  const [isLoaded, setIsLoaded] = useState(false);
  const [imageSrc, setImageSrc] = useState(getDioramaPath(day));

  useEffect(() => {
    setImageSrc(getDioramaPath(day));
  }, [day]);

  const config = sizeConfig[size];

  return (
    <div className={cn(
      'relative overflow-hidden rounded-xl',
      config.containerClass,
      className
    )}>
      {/* Loading skeleton */}
      {!isLoaded && (
        <div className="absolute inset-0 bg-gradient-to-br from-indigo-100 to-slate-100 animate-pulse rounded-xl flex items-center justify-center">
          <div className="w-8 h-8 border-2 border-indigo-600 border-t-transparent rounded-full animate-spin" />
        </div>
      )}

      {/* Glow effect behind image - indigo theme */}
      {showGlow && isLoaded && (
        <motion.div
          className="absolute inset-4 rounded-full blur-2xl bg-indigo-500/40"
          animate={{
            opacity: [0.15, 0.3, 0.15],
            scale: [0.9, 1, 0.9],
          }}
          transition={{
            duration: 4,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        />
      )}

      {/* Main image with float animation */}
      <motion.div
        className="relative w-full h-full"
        animate={animate ? {
          y: [0, -6, 0],
        } : {}}
        transition={{
          duration: 5,
          repeat: Infinity,
          ease: 'easeInOut',
        }}
      >
        <Image
          src={imageSrc}
          alt={`Diorama day ${day}`}
          fill
          sizes={config.sizes}
          className={cn(
            'object-contain transition-opacity duration-300',
            isLoaded ? 'opacity-100' : 'opacity-0'
          )}
          onLoad={() => setIsLoaded(true)}
          priority={priority}
        />
      </motion.div>

      {/* Day badge */}
      {size !== 'mini' && (
        <div className="absolute bottom-2 right-2 bg-indigo-600/90 text-white text-xs px-2 py-1 rounded-full shadow-sm">
          Day {Math.max(1, Math.min(200, day))}
        </div>
      )}
    </div>
  );
}

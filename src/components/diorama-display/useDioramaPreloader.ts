'use client';

import { useEffect, useRef, useCallback } from 'react';

const MAX_DAY = 200;

function getDioramaPath(day: number): string {
  const clampedDay = Math.max(1, Math.min(MAX_DAY, day));
  const paddedDay = clampedDay.toString().padStart(3, '0');
  return `/diorama/final/day-${paddedDay}.png`;
}

interface PreloaderOptions {
  currentDay: number;
  preloadRadius?: number;
  enabled?: boolean;
}

export function useDioramaPreloader({
  currentDay,
  preloadRadius = 5,
  enabled = true,
}: PreloaderOptions) {
  const preloadedRef = useRef<Set<number>>(new Set());
  const loadingRef = useRef<Set<number>>(new Set());

  const preloadImage = useCallback((day: number) => {
    if (day < 1 || day > MAX_DAY) return;
    if (preloadedRef.current.has(day) || loadingRef.current.has(day)) return;

    loadingRef.current.add(day);

    const img = new window.Image();
    img.src = getDioramaPath(day);
    img.onload = () => {
      preloadedRef.current.add(day);
      loadingRef.current.delete(day);
    };
    img.onerror = () => {
      loadingRef.current.delete(day);
    };
  }, []);

  useEffect(() => {
    if (!enabled) return;

    // Preload current day first
    preloadImage(currentDay);

    // Preload surrounding days (prioritize forward)
    for (let offset = 1; offset <= preloadRadius; offset++) {
      preloadImage(currentDay + offset);
      preloadImage(currentDay - offset);
    }
  }, [currentDay, preloadRadius, enabled, preloadImage]);

  const isPreloaded = useCallback(
    (day: number) => preloadedRef.current.has(day),
    []
  );

  const preloadRange = useCallback(
    (start: number, end: number) => {
      for (let day = start; day <= end; day++) {
        preloadImage(day);
      }
    },
    [preloadImage]
  );

  return {
    isPreloaded,
    preloadRange,
  };
}

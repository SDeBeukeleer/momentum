'use client';

import { useEffect, useRef, useCallback } from 'react';
import { getDioramaPath, getThemeConfig, type DioramaTheme } from '@/types/diorama';

interface PreloaderOptions {
  currentDay: number;
  theme?: DioramaTheme;
  preloadRadius?: number;
  enabled?: boolean;
}

export function useDioramaPreloader({
  currentDay,
  theme = 'plant',
  preloadRadius = 5,
  enabled = true,
}: PreloaderOptions) {
  const preloadedRef = useRef<Set<string>>(new Set());
  const loadingRef = useRef<Set<string>>(new Set());
  const themeConfig = getThemeConfig(theme);

  const preloadImage = useCallback((day: number, currentTheme: DioramaTheme) => {
    const config = getThemeConfig(currentTheme);
    if (day < 1 || day > config.maxDays) return;

    const key = `${currentTheme}-${day}`;
    if (preloadedRef.current.has(key) || loadingRef.current.has(key)) return;

    loadingRef.current.add(key);

    const img = new window.Image();
    img.src = getDioramaPath(currentTheme, day);
    img.onload = () => {
      preloadedRef.current.add(key);
      loadingRef.current.delete(key);
    };
    img.onerror = () => {
      loadingRef.current.delete(key);
    };
  }, []);

  useEffect(() => {
    if (!enabled) return;

    // Preload current day first
    preloadImage(currentDay, theme);

    // Preload surrounding days (prioritize forward)
    for (let offset = 1; offset <= preloadRadius; offset++) {
      preloadImage(currentDay + offset, theme);
      preloadImage(currentDay - offset, theme);
    }
  }, [currentDay, theme, preloadRadius, enabled, preloadImage]);

  const isPreloaded = useCallback(
    (day: number) => preloadedRef.current.has(`${theme}-${day}`),
    [theme]
  );

  const preloadRange = useCallback(
    (start: number, end: number) => {
      for (let day = start; day <= end; day++) {
        preloadImage(day, theme);
      }
    },
    [preloadImage, theme]
  );

  return {
    isPreloaded,
    preloadRange,
    maxDays: themeConfig.maxDays,
  };
}

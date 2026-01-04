'use client';

import { useState, useEffect, useRef, useLayoutEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from '@/components/ui/button';

interface SpotlightProps {
  targetSelector: string;
  title: string;
  message: string;
  position?: 'top' | 'bottom' | 'left' | 'right';
  onDismiss: () => void;
  buttonLabel?: string;
}

interface TargetRect {
  top: number;
  left: number;
  width: number;
  height: number;
}

interface TooltipPosition {
  top: number;
  left: number;
}

export function Spotlight({
  targetSelector,
  title,
  message,
  position = 'bottom',
  onDismiss,
  buttonLabel = 'Got it',
}: SpotlightProps) {
  const [targetRect, setTargetRect] = useState<TargetRect | null>(null);
  const [tooltipPosition, setTooltipPosition] = useState<TooltipPosition | null>(null);
  const tooltipRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let retryCount = 0;
    const maxRetries = 20;
    let retryTimeout: NodeJS.Timeout;

    const updatePosition = () => {
      const target = document.querySelector(targetSelector);
      if (target) {
        const rect = target.getBoundingClientRect();
        setTargetRect({
          top: rect.top,
          left: rect.left,
          width: rect.width,
          height: rect.height,
        });
      } else if (retryCount < maxRetries) {
        // Retry finding the element
        retryCount++;
        retryTimeout = setTimeout(updatePosition, 100);
      }
    };

    // Initial position with small delay to let DOM settle
    retryTimeout = setTimeout(updatePosition, 100);

    // Update on scroll/resize
    window.addEventListener('scroll', updatePosition, true);
    window.addEventListener('resize', updatePosition);

    return () => {
      clearTimeout(retryTimeout);
      window.removeEventListener('scroll', updatePosition, true);
      window.removeEventListener('resize', updatePosition);
    };
  }, [targetSelector]);

  // Calculate and adjust tooltip position after render
  useLayoutEffect(() => {
    if (!targetRect || !tooltipRef.current) return;

    const tooltip = tooltipRef.current;
    const tooltipRect = tooltip.getBoundingClientRect();
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;
    const margin = 16; // Minimum margin from screen edges
    const tooltipOffset = 12;

    // Calculate initial position based on preferred position
    let top: number;
    let left: number;

    const centerX = targetRect.left + targetRect.width / 2;
    const centerY = targetRect.top + targetRect.height / 2;

    switch (position) {
      case 'top':
        top = targetRect.top - tooltipOffset - tooltipRect.height;
        left = centerX - tooltipRect.width / 2;
        break;
      case 'bottom':
        top = targetRect.top + targetRect.height + tooltipOffset;
        left = centerX - tooltipRect.width / 2;
        break;
      case 'left':
        top = centerY - tooltipRect.height / 2;
        left = targetRect.left - tooltipOffset - tooltipRect.width;
        break;
      case 'right':
        top = centerY - tooltipRect.height / 2;
        left = targetRect.left + targetRect.width + tooltipOffset;
        break;
    }

    // Clamp to viewport bounds
    left = Math.max(margin, Math.min(left, viewportWidth - tooltipRect.width - margin));
    top = Math.max(margin, Math.min(top, viewportHeight - tooltipRect.height - margin));

    setTooltipPosition({ top, left });
  }, [targetRect, position]);

  if (!targetRect) return null;

  const padding = 16;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-[100]"
      >
        {/* Dark overlay with cutout */}
        <svg className="absolute inset-0 w-full h-full">
          <defs>
            <mask id="spotlight-mask">
              <rect x="0" y="0" width="100%" height="100%" fill="white" />
              <rect
                x={targetRect.left - padding}
                y={targetRect.top - padding}
                width={targetRect.width + padding * 2}
                height={targetRect.height + padding * 2}
                rx="12"
                fill="black"
              />
            </mask>
          </defs>
          <rect
            x="0"
            y="0"
            width="100%"
            height="100%"
            fill="rgba(0, 0, 0, 0.75)"
            mask="url(#spotlight-mask)"
          />
        </svg>

        {/* Pulsing ring around target */}
        <motion.div
          className="absolute rounded-xl border-2 border-indigo-400 pointer-events-none"
          style={{
            top: targetRect.top - padding,
            left: targetRect.left - padding,
            width: targetRect.width + padding * 2,
            height: targetRect.height + padding * 2,
          }}
          animate={{
            boxShadow: [
              '0 0 0 0 rgba(99, 102, 241, 0.4)',
              '0 0 0 8px rgba(99, 102, 241, 0)',
            ],
          }}
          transition={{
            duration: 1.5,
            repeat: Infinity,
            ease: 'easeOut',
          }}
        />

        {/* Tooltip */}
        <motion.div
          ref={tooltipRef}
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: tooltipPosition ? 1 : 0, scale: 1 }}
          exit={{ opacity: 0, scale: 0.9 }}
          transition={{ delay: 0.2 }}
          className="absolute bg-white rounded-2xl shadow-xl p-5 z-10 mx-4"
          style={{
            top: tooltipPosition?.top ?? targetRect.top + targetRect.height + 12,
            left: tooltipPosition?.left ?? 16,
            maxWidth: 'calc(100vw - 32px)',
            width: 280,
          }}
        >
          <h3
            className="text-lg font-semibold text-slate-900 mb-2"
            style={{ fontFamily: 'var(--font-fraunces)' }}
          >
            {title}
          </h3>
          <p className="text-slate-600 mb-4">{message}</p>
          <Button
            onClick={onDismiss}
            className="w-full bg-indigo-600 hover:bg-indigo-700 text-white"
          >
            {buttonLabel}
          </Button>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}

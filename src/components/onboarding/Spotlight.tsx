'use client';

import { useState, useEffect, useRef } from 'react';
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

export function Spotlight({
  targetSelector,
  title,
  message,
  position = 'bottom',
  onDismiss,
  buttonLabel = 'Got it',
}: SpotlightProps) {
  const [targetRect, setTargetRect] = useState<TargetRect | null>(null);
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

  if (!targetRect) return null;

  // Calculate tooltip position
  const padding = 16;
  const tooltipOffset = 12;

  const getTooltipPosition = () => {
    const centerX = targetRect.left + targetRect.width / 2;
    const centerY = targetRect.top + targetRect.height / 2;

    switch (position) {
      case 'top':
        return {
          top: targetRect.top - tooltipOffset,
          left: centerX,
          transform: 'translate(-50%, -100%)',
        };
      case 'bottom':
        return {
          top: targetRect.top + targetRect.height + tooltipOffset,
          left: centerX,
          transform: 'translate(-50%, 0)',
        };
      case 'left':
        return {
          top: centerY,
          left: targetRect.left - tooltipOffset,
          transform: 'translate(-100%, -50%)',
        };
      case 'right':
        return {
          top: centerY,
          left: targetRect.left + targetRect.width + tooltipOffset,
          transform: 'translate(0, -50%)',
        };
    }
  };

  const tooltipPosition = getTooltipPosition();

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
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.9 }}
          transition={{ delay: 0.2 }}
          className="absolute bg-white rounded-2xl shadow-xl p-5 max-w-xs z-10"
          style={{
            top: tooltipPosition.top,
            left: tooltipPosition.left,
            transform: tooltipPosition.transform,
          }}
        >
          {/* Arrow */}
          <div
            className={`absolute w-3 h-3 bg-white transform rotate-45 ${
              position === 'top'
                ? 'bottom-0 left-1/2 -translate-x-1/2 translate-y-1/2'
                : position === 'bottom'
                ? 'top-0 left-1/2 -translate-x-1/2 -translate-y-1/2'
                : position === 'left'
                ? 'right-0 top-1/2 translate-x-1/2 -translate-y-1/2'
                : 'left-0 top-1/2 -translate-x-1/2 -translate-y-1/2'
            }`}
          />

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

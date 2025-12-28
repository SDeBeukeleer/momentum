'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { X } from 'lucide-react';
import confetti from 'canvas-confetti';

export interface GuidanceMessage {
  key: string;
  title: string;
  message: string;
  emoji?: string;
  primaryAction?: {
    label: string;
    href?: string;
    onClick?: () => void;
  };
  secondaryAction?: {
    label: string;
    onClick?: () => void;
  };
  celebrate?: boolean; // Trigger confetti
}

interface GuidancePopupProps {
  guidance: GuidanceMessage | null;
  onDismiss: () => void;
}

export function GuidancePopup({ guidance, onDismiss }: GuidancePopupProps) {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    if (guidance) {
      // Small delay before showing for smoother UX
      const timer = setTimeout(() => {
        setIsVisible(true);
        if (guidance.celebrate) {
          // Fire confetti
          confetti({
            particleCount: 100,
            spread: 70,
            origin: { y: 0.6 },
            colors: ['#d97706', '#ea580c', '#f59e0b', '#fbbf24'],
          });
        }
      }, 300);
      return () => clearTimeout(timer);
    } else {
      setIsVisible(false);
    }
  }, [guidance]);

  const handleDismiss = () => {
    setIsVisible(false);
    setTimeout(onDismiss, 200);
  };

  const handlePrimaryAction = () => {
    if (guidance?.primaryAction?.onClick) {
      guidance.primaryAction.onClick();
    }
    if (guidance?.primaryAction?.href) {
      window.location.href = guidance.primaryAction.href;
    }
    handleDismiss();
  };

  return (
    <AnimatePresence>
      {isVisible && guidance && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/30 backdrop-blur-sm z-50"
            onClick={handleDismiss}
          />

          {/* Popup */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
            className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-50 w-[calc(100%-2rem)] max-w-md"
          >
            <div className="bg-white rounded-2xl shadow-2xl overflow-hidden">
              {/* Header gradient */}
              <div className="bg-gradient-to-r from-amber-500 to-orange-500 px-6 py-4 relative">
                <button
                  onClick={handleDismiss}
                  className="absolute right-3 top-3 text-white/80 hover:text-white transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
                {guidance.emoji && (
                  <div className="text-5xl mb-2">{guidance.emoji}</div>
                )}
                <h2 className="text-xl font-bold text-white pr-8">
                  {guidance.title}
                </h2>
              </div>

              {/* Content */}
              <div className="px-6 py-5">
                <p className="text-amber-900/80 leading-relaxed">
                  {guidance.message}
                </p>
              </div>

              {/* Actions */}
              <div className="px-6 pb-6 flex gap-3">
                {guidance.secondaryAction && (
                  <Button
                    variant="outline"
                    className="flex-1"
                    onClick={() => {
                      guidance.secondaryAction?.onClick?.();
                      handleDismiss();
                    }}
                  >
                    {guidance.secondaryAction.label}
                  </Button>
                )}
                <Button
                  className={`${guidance.secondaryAction ? 'flex-1' : 'w-full'} bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-700 hover:to-orange-700`}
                  onClick={handlePrimaryAction}
                >
                  {guidance.primaryAction?.label || 'Got it!'}
                </Button>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}

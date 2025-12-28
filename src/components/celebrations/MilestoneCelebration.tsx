'use client';

import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface MilestoneCelebrationProps {
  milestone: {
    name: string;
    emoji: string;
    description: string;
    bonusCredits: number;
  } | null;
  onClose: () => void;
}

// Confetti particle component
function ConfettiParticle({ delay, color }: { delay: number; color: string }) {
  const randomX = Math.random() * 100;
  const randomRotate = Math.random() * 360;
  const randomDuration = 2 + Math.random() * 2;

  return (
    <motion.div
      className="absolute w-3 h-3 rounded-sm"
      style={{
        backgroundColor: color,
        left: `${randomX}%`,
        top: '-20px',
      }}
      initial={{ y: 0, rotate: 0, opacity: 1 }}
      animate={{
        y: '100vh',
        rotate: randomRotate + 720,
        opacity: [1, 1, 0],
      }}
      transition={{
        duration: randomDuration,
        delay,
        ease: 'easeIn',
      }}
    />
  );
}

export function MilestoneCelebration({ milestone, onClose }: MilestoneCelebrationProps) {
  const [particles, setParticles] = useState<{ id: number; delay: number; color: string }[]>([]);

  useEffect(() => {
    if (milestone) {
      // Generate confetti particles
      const colors = ['#f59e0b', '#ef4444', '#22c55e', '#3b82f6', '#a855f7', '#ec4899'];
      const newParticles = Array.from({ length: 50 }, (_, i) => ({
        id: i,
        delay: Math.random() * 0.5,
        color: colors[Math.floor(Math.random() * colors.length)],
      }));
      setParticles(newParticles);

      // Auto-close after 5 seconds
      const timer = setTimeout(() => {
        onClose();
      }, 5000);

      return () => clearTimeout(timer);
    }
  }, [milestone, onClose]);

  return (
    <AnimatePresence>
      {milestone && (
        <motion.div
          className="fixed inset-0 z-50 flex items-center justify-center"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          {/* Backdrop */}
          <motion.div
            className="absolute inset-0 bg-black/60 backdrop-blur-sm"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />

          {/* Confetti */}
          <div className="absolute inset-0 overflow-hidden pointer-events-none">
            {particles.map((particle) => (
              <ConfettiParticle
                key={particle.id}
                delay={particle.delay}
                color={particle.color}
              />
            ))}
          </div>

          {/* Celebration Card */}
          <motion.div
            className="relative bg-white rounded-2xl shadow-2xl p-6 sm:p-8 w-[calc(100%-2rem)] max-w-sm text-center"
            initial={{ scale: 0, rotate: -10 }}
            animate={{ scale: 1, rotate: 0 }}
            exit={{ scale: 0, rotate: 10 }}
            transition={{ type: 'spring', damping: 15 }}
          >
            <Button
              variant="ghost"
              size="icon"
              className="absolute top-2 right-2"
              onClick={onClose}
            >
              <X className="h-4 w-4" />
            </Button>

            {/* Emoji */}
            <motion.div
              className="text-7xl mb-4"
              initial={{ scale: 0 }}
              animate={{ scale: [0, 1.2, 1] }}
              transition={{ delay: 0.2, duration: 0.5 }}
            >
              {milestone.emoji}
            </motion.div>

            {/* Title */}
            <motion.h2
              className="text-2xl font-bold bg-gradient-to-r from-amber-600 to-orange-600 bg-clip-text text-transparent mb-2"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
            >
              {milestone.name}!
            </motion.h2>

            {/* Description */}
            <motion.p
              className="text-amber-800/70 mb-4"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
            >
              {milestone.description}
            </motion.p>

            {/* Bonus Credits */}
            <motion.div
              className="bg-gradient-to-r from-amber-50 to-orange-50 rounded-xl p-4 border border-amber-200"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
            >
              <div className="text-sm text-amber-700/70 mb-1">Bonus Reward</div>
              <div className="text-2xl font-bold text-amber-700">
                +{milestone.bonusCredits} Credit{milestone.bonusCredits > 1 ? 's' : ''}
              </div>
            </motion.div>

            {/* Close Button */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.7 }}
            >
              <Button
                className="mt-6 bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-700 hover:to-orange-700"
                onClick={onClose}
              >
                Awesome!
              </Button>
            </motion.div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

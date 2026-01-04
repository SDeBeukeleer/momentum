'use client';

import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Sparkles, Target, Trophy, Shield } from 'lucide-react';

interface WelcomeScreenProps {
  onGetStarted: () => void;
}

const features = [
  {
    icon: Target,
    title: 'Track Daily Habits',
    description: 'Build streaks and stay consistent',
  },
  {
    icon: Sparkles,
    title: 'Watch Progress Come to Life',
    description: 'Your journey evolves into a visual story',
  },
  {
    icon: Shield,
    title: 'Protect Your Streaks',
    description: 'Earn credits to skip days without breaking streaks',
  },
];

export function WelcomeScreen({ onGetStarted }: WelcomeScreenProps) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-[100] bg-gradient-to-b from-indigo-50 via-white to-indigo-50 flex items-center justify-center p-6"
    >
      <div className="max-w-md w-full">
        {/* Logo/Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="text-center mb-10"
        >
          <div className="relative w-20 h-20 mx-auto mb-6">
            <motion.div
              className="absolute inset-0 rounded-full bg-indigo-100"
              animate={{
                scale: [1, 1.1, 1],
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                ease: 'easeInOut',
              }}
            />
            <div className="absolute inset-2 rounded-full bg-indigo-600 flex items-center justify-center">
              <Trophy className="w-8 h-8 text-white" />
            </div>
          </div>

          <h1
            className="text-3xl font-bold text-slate-900 mb-3"
            style={{ fontFamily: 'var(--font-fraunces)' }}
          >
            Welcome to Momentum
          </h1>
          <p className="text-slate-600 text-lg">
            Build lasting habits with visual progress
          </p>
        </motion.div>

        {/* Features */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="space-y-4 mb-10"
        >
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.5 + index * 0.1 }}
              className="flex items-start gap-4 bg-white rounded-xl p-4 shadow-sm border border-slate-100"
            >
              <div className="h-10 w-10 rounded-lg bg-indigo-100 flex items-center justify-center flex-shrink-0">
                <feature.icon className="h-5 w-5 text-indigo-600" />
              </div>
              <div>
                <h3 className="font-medium text-slate-900">{feature.title}</h3>
                <p className="text-sm text-slate-500">{feature.description}</p>
              </div>
            </motion.div>
          ))}
        </motion.div>

        {/* CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
        >
          <Button
            onClick={onGetStarted}
            size="lg"
            className="w-full h-14 text-lg bg-indigo-600 hover:bg-indigo-700 text-white shadow-lg shadow-indigo-200"
          >
            Get Started
          </Button>
        </motion.div>
      </div>
    </motion.div>
  );
}

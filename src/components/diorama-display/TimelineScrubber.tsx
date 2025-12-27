'use client';

import { useState, useCallback, useRef, useEffect } from 'react';
import { Slider } from '@/components/ui/slider';
import { Button } from '@/components/ui/button';
import { Play, Pause, Leaf, SkipBack, SkipForward } from 'lucide-react';

interface TimelineScrubberProps {
  currentStreak: number;
  displayDay: number;
  onDayChange: (day: number) => void;
}

export function TimelineScrubber({
  currentStreak,
  displayDay,
  onDayChange,
}: TimelineScrubberProps) {
  const [isPlaying, setIsPlaying] = useState(false);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  // Cap at 200 (max images) and user's streak
  const maxDay = Math.min(200, Math.max(1, currentStreak));

  // Autoplay functionality
  useEffect(() => {
    if (isPlaying) {
      intervalRef.current = setInterval(() => {
        onDayChange(displayDay + 1);
      }, 400);
    } else if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [isPlaying, displayDay, onDayChange]);

  // Stop playing when reaching the end
  useEffect(() => {
    if (displayDay >= maxDay) {
      setIsPlaying(false);
    }
  }, [displayDay, maxDay]);

  const handlePlayPause = useCallback(() => {
    if (displayDay >= maxDay) {
      // Restart from beginning
      onDayChange(1);
      setIsPlaying(true);
    } else {
      setIsPlaying(prev => !prev);
    }
  }, [onDayChange, displayDay, maxDay]);

  if (maxDay < 1) {
    return (
      <div className="p-4 border-t border-amber-100 text-center text-amber-700/60 text-sm">
        <Leaf className="w-5 h-5 mx-auto mb-2 opacity-50" />
        Complete your first day to unlock the timeline!
      </div>
    );
  }

  return (
    <div className="p-4 border-t border-amber-100 space-y-4">
      {/* Header */}
      <div className="flex items-center gap-2">
        <Leaf className="w-4 h-4 text-green-600" />
        <span className="text-sm font-medium text-amber-800">
          Journey Timeline
        </span>
      </div>

      {/* Slider */}
      <div className="space-y-2">
        <div className="flex justify-between text-xs text-amber-700/60">
          <span>Day 1</span>
          <span className="font-medium text-amber-800">Day {displayDay}</span>
          <span>Day {maxDay}</span>
        </div>
        <Slider
          value={[displayDay]}
          onValueChange={(value) => {
            onDayChange(value[0]);
            setIsPlaying(false);
          }}
          max={maxDay}
          min={1}
          step={1}
        />
      </div>

      {/* Playback controls - always visible */}
      {maxDay > 1 && (
        <div className="flex items-center justify-center gap-2">
          <Button
            variant="outline"
            size="icon"
            className="h-8 w-8"
            onClick={() => {
              onDayChange(1);
              setIsPlaying(false);
            }}
            disabled={displayDay === 1}
          >
            <SkipBack className="h-4 w-4" />
          </Button>
          <Button
            variant="outline"
            size="icon"
            className="h-10 w-10"
            onClick={handlePlayPause}
          >
            {isPlaying ? (
              <Pause className="h-5 w-5" />
            ) : (
              <Play className="h-5 w-5 ml-0.5" />
            )}
          </Button>
          <Button
            variant="outline"
            size="icon"
            className="h-8 w-8"
            onClick={() => {
              onDayChange(maxDay);
              setIsPlaying(false);
            }}
            disabled={displayDay === maxDay}
          >
            <SkipForward className="h-4 w-4" />
          </Button>
        </div>
      )}
    </div>
  );
}

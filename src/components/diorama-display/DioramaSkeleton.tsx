'use client';

import { cn } from '@/lib/utils';

interface DioramaSkeletonProps {
  size?: 'mini' | 'medium' | 'full';
  className?: string;
}

const sizeClasses = {
  mini: 'w-20 h-20',
  medium: 'w-48 h-48',
  full: 'w-full aspect-square max-w-[600px]',
};

export function DioramaSkeleton({ size = 'full', className }: DioramaSkeletonProps) {
  return (
    <div className={cn(
      'rounded-xl bg-gradient-to-br from-slate-200 to-slate-300 animate-pulse flex items-center justify-center',
      sizeClasses[size],
      className
    )}>
      <div className="flex flex-col items-center gap-2 text-slate-400">
        <div className="w-8 h-8 border-2 border-slate-400 border-t-transparent rounded-full animate-spin" />
        {size !== 'mini' && (
          <span className="text-sm">Loading garden...</span>
        )}
      </div>
    </div>
  );
}

'use client';

import { cn } from '@/lib/utils';
import { DIORAMA_THEMES, THEME_CONFIGS, type DioramaTheme } from '@/types/diorama';
import Image from 'next/image';

interface ThemePickerProps {
  value: DioramaTheme;
  onChange: (theme: DioramaTheme) => void;
}

export function ThemePicker({ value, onChange }: ThemePickerProps) {
  return (
    <div className="grid grid-cols-3 gap-3">
      {DIORAMA_THEMES.map((themeId) => {
        const theme = THEME_CONFIGS[themeId];
        const isSelected = value === themeId;
        const previewPath = `/diorama/${theme.folder}/day-${theme.previewDay.toString().padStart(3, '0')}.png`;

        return (
          <button
            key={themeId}
            type="button"
            onClick={() => onChange(themeId)}
            className={cn(
              'relative flex flex-col items-center gap-2 rounded-xl p-3 transition-all duration-200',
              'border-2 hover:border-primary/50',
              isSelected
                ? 'border-primary bg-primary/10 ring-2 ring-primary/20'
                : 'border-border/50 bg-card/50'
            )}
          >
            {/* Preview Image */}
            <div className="relative aspect-square w-full overflow-hidden rounded-lg bg-muted">
              <Image
                src={previewPath}
                alt={theme.name}
                fill
                className="object-cover"
                sizes="(max-width: 768px) 80px, 100px"
              />
            </div>

            {/* Theme Info */}
            <div className="flex flex-col items-center gap-0.5">
              <span className="text-lg">{theme.emoji}</span>
              <span className={cn(
                'text-xs font-medium',
                isSelected ? 'text-primary' : 'text-muted-foreground'
              )}>
                {theme.name}
              </span>
            </div>

            {/* Selected Indicator */}
            {isSelected && (
              <div className="absolute -right-1 -top-1 flex h-5 w-5 items-center justify-center rounded-full bg-primary text-[10px] text-primary-foreground">
                ✓
              </div>
            )}
          </button>
        );
      })}
    </div>
  );
}

// Compact theme display for showing current theme
export function ThemeDisplay({ theme }: { theme: DioramaTheme }) {
  const config = THEME_CONFIGS[theme] ?? THEME_CONFIGS.plant;

  return (
    <div className="flex items-center gap-2 text-sm text-muted-foreground">
      <span>{config.emoji}</span>
      <span>{config.name}</span>
    </div>
  );
}

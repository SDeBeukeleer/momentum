# CLAUDE.md - Momentum Habit Tracker

This file provides context for Claude Code when working on this project.

## Project Overview

Momentum is a habit tracking PWA that uses visual dioramas to show progress. Users build streaks, earn credits at milestones, and can use credits to skip days without breaking streaks.

**Production URL:** https://momentum.lolala.be
**Server:** Hetzner VPS at 91.99.160.39

## Tech Stack

- **Framework:** Next.js 16 (App Router, Turbopack)
- **Language:** TypeScript
- **Database:** PostgreSQL 16 with Prisma 5.22.0
- **Auth:** NextAuth.js v5
- **Styling:** Tailwind CSS + shadcn/ui
- **Animations:** Framer Motion

## Key Features

### Diorama Themes
Three visual themes for habit progression:
- **Plant** (`final/`): Growing garden, 200 days
- **Car** (`v13-auto-anchor-nobg/`): Porsche restoration, 200 days
- **Spaceship** (`v14-spaceship-nobg/`): Spaceship builder, 130 days

Theme config in `src/types/diorama.ts`

### Credit System
Milestones award bonus credits:
- Day 7: +1, Day 14: +1, Day 30: +2
- Day 50: +2, Day 100: +5, Day 150: +5, Day 200: +10

### Onboarding System
Progressive onboarding for new users:
1. Welcome screen (full-screen intro)
2. Spotlight on "Create Habit" button
3. Spotlight on habit card after creation
4. Guidance popup after first completion

Components in `src/components/onboarding/`

### Guidance System
Smart popups triggered by user state (max 2/day).
Components in `src/components/guidance/`

## Important Files

```
src/
├── app/
│   ├── (dashboard)/layout.tsx    # Dashboard wrapper with providers
│   ├── api/onboarding/route.ts   # Onboarding API
│   └── api/habits/               # Habit CRUD APIs
├── components/
│   ├── onboarding/               # Onboarding flow components
│   │   ├── OnboardingProvider.tsx
│   │   ├── WelcomeScreen.tsx
│   │   ├── Spotlight.tsx
│   │   └── onboarding-steps.ts
│   ├── habits/
│   │   ├── today-view.tsx        # Main habit list
│   │   └── habit-card.tsx        # Individual habit card
│   └── diorama-display/          # Diorama image display
├── types/
│   └── diorama.ts                # Theme configs, milestones
└── lib/
    ├── auth.ts                   # NextAuth config
    └── prisma.ts                 # Prisma client
```

## Database Schema

Key models in `prisma/schema.prisma`:
- **User**: email, password, hasCompletedOnboarding
- **Habit**: name, icon, theme, currentStreak, currentCredits
- **HabitCompletion**: date, usedCredit
- **UserGuidance**: tracks shown guidance/onboarding steps

## Deployment

### Quick Deploy
```bash
# From local
rsync -avz --progress ./ root@91.99.160.39:/opt/momentum/ \
  --exclude node_modules --exclude .next --exclude .git

# On server
ssh root@91.99.160.39
cd /opt/momentum
docker compose -f docker-compose.prod.yml build --no-cache
docker compose -f docker-compose.prod.yml up -d
```

### Environment Variables (on server)
```env
DB_PASSWORD=momentum_secure_2024
DATABASE_URL=postgresql://momentum:momentum_secure_2024@db:5432/momentum
NEXTAUTH_SECRET=xK9mP2nQ7vR4sT8wY1zA3bC6dE0fG5hJ
NEXTAUTH_URL=https://momentum.lolala.be
```

### Database Commands
```bash
# Access DB
docker exec -it momentum-db psql -U momentum -d momentum

# Run migrations
docker exec momentum-app npx prisma@5.22.0 db push

# View logs
docker logs -f momentum-app
```

## Common Tasks

### Adding a new diorama theme
1. Add images to `public/diorama/<folder-name>/`
2. Update `THEME_CONFIGS` in `src/types/diorama.ts`
3. Add theme option to habit creation dialog

### Modifying onboarding flow
1. Edit steps in `src/components/onboarding/onboarding-steps.ts`
2. Add data-onboarding attributes to target elements
3. Update OnboardingProvider if new step types needed

### Testing onboarding
Create a new user - they'll have `hasCompletedOnboarding: false` and see the full flow.

## Known Issues

- Prisma 7.x has breaking changes; use `npx prisma@5.22.0` on server
- `.env.production` permission warning in logs is harmless

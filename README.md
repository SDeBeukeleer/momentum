# Momentum - Habit Tracker

A modern habit tracking app that helps users build lasting habits through a unique credit system and visual progression. Watch your habits grow into beautiful dioramas as you maintain your streaks.

## Features

### Core Habits
- **Daily Habit Tracking** - Track multiple habits with one-tap completion
- **Streak System** - Build momentum with consecutive day streaks
- **Credit System** - Earn credits at milestones (Day 7, 14, 30, 50, 100, 150, 200)
- **Skip Days** - Use earned credits to take guilt-free rest days without breaking streaks

### Garden & Dioramas
- **Visual Progression** - 200 unique diorama images showing habit growth
- **Timeline Scrubber** - View your journey from Day 1 to your current streak
- **Milestone Rewards** - Celebrate achievements with credits and visual upgrades

### Weight Tracking
- **Daily Logging** - Track weight with trend analysis
- **Goal Setting** - Set target weight and track progress
- **Historical Data** - View weight history and monthly changes

### Progress & Stats
- **Activity Heatmap** - GitHub-style visualization of completions
- **Achievement Badges** - Unlock badges for milestones and consistency
- **Weekly Trends** - Charts showing habit completion patterns
- **Best Days Analysis** - Identify your most productive days

### User Guidance
- **Smart Pop-ups** - Contextual guidance for new users (max 2/day)
- **Onboarding Flow** - Helpful tips for first habit, first completion, etc.
- **Milestone Celebrations** - Celebratory messages with confetti at key streaks
- **Feature Discovery** - Gentle nudges to explore garden and credits

## Tech Stack

- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript
- **Database**: PostgreSQL with Prisma ORM
- **Authentication**: NextAuth.js
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui
- **Animations**: Framer Motion
- **Charts**: Recharts

## Getting Started

### Prerequisites
- Node.js 18+
- PostgreSQL database

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd momentum
```

2. Install dependencies
```bash
npm install
```

3. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your database URL and auth secrets
```

4. Set up the database
```bash
npx prisma db push
npx prisma generate
```

5. Run the development server
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to see the app.

## Project Structure

```
src/
├── app/                    # Next.js App Router pages
│   ├── (dashboard)/        # Protected dashboard routes
│   │   ├── dashboard/      # Home, habits, weight, progress
│   │   └── garden/         # Diorama garden view
│   └── api/                # API routes
├── components/
│   ├── diorama-display/    # Pre-rendered diorama images
│   ├── garden/             # Garden view components
│   ├── guidance/           # User guidance pop-up system
│   ├── habits/             # Habit cards, dialogs, views
│   ├── layout/             # Navbar, layout components
│   ├── stats/              # Progress and statistics
│   ├── ui/                 # shadcn/ui components
│   └── weight/             # Weight tracking components
├── lib/                    # Utilities and configurations
└── types/                  # TypeScript type definitions
```

## Key Components

### Guidance System
The app includes a smart guidance system that helps onboard new users:
- Tracks which guidance messages have been shown
- Limits to 2 pop-ups per day to avoid annoyance
- Triggers based on user state (habits, streaks, credits)
- Includes milestone celebrations with confetti

### Credit System
Users earn credits at specific milestones:
- Day 7: +1 credit
- Day 14: +1 credit
- Day 30: +2 credits
- Day 50: +2 credits
- Day 100: +5 credits
- Day 150: +5 credits
- Day 200: +10 credits

Credits can be used to skip days without breaking streaks.

### Diorama Display
200 pre-rendered PNG images showing habit progression from seed to thriving community. Images are displayed based on current streak day with CSS animations.

## Environment Variables

```env
DATABASE_URL="postgresql://..."
NEXTAUTH_SECRET="your-secret"
NEXTAUTH_URL="http://localhost:3000"
```

## Deployment

### Production URL

**Live at:** https://momentum.lolala.be

### Local Development

```bash
npm run dev
```

### Production Build

```bash
npm run build
```

### Docker Deployment (Hetzner)

The app is deployed on a Hetzner server using Docker Compose.

#### Server Setup

1. **SSH into the server**
```bash
ssh root@91.99.160.39
```

2. **Navigate to the project**
```bash
cd /opt/momentum
```

3. **Environment variables** (`.env` file)
```env
DB_PASSWORD=your-secure-password
NEXTAUTH_SECRET=your-secret-key
NEXTAUTH_URL=https://momentum.lolala.be
```

4. **Start the containers**
```bash
docker compose -f docker-compose.prod.yml up -d
```

5. **View logs**
```bash
docker logs -f momentum-app
```

#### Docker Architecture

```
┌─────────────────────────────────────────────────┐
│                   Hetzner VPS                   │
│                  91.99.160.39                   │
├─────────────────────────────────────────────────┤
│  Nginx (port 80/443)                            │
│    └── SSL via Let's Encrypt                    │
│    └── Reverse proxy to :3001                   │
├─────────────────────────────────────────────────┤
│  Docker Compose                                 │
│    ├── momentum-app (Next.js) → port 3001      │
│    └── momentum-db (PostgreSQL 16)              │
└─────────────────────────────────────────────────┘
```

#### Deploying Updates

```bash
# From local machine
rsync -avz --progress ./ root@91.99.160.39:/opt/momentum/ \
  --exclude node_modules --exclude .next --exclude .git

# On server
ssh root@91.99.160.39
cd /opt/momentum
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml build --no-cache
docker compose -f docker-compose.prod.yml up -d
```

#### SSL Certificate

- **Provider:** Let's Encrypt via Certbot
- **Auto-renewal:** Enabled (certbot scheduled task)
- **Expiry:** Auto-renews before expiration
- **Config:** `/etc/nginx/sites-available/momentum`

#### Database Management

```bash
# Access PostgreSQL
docker exec -it momentum-db psql -U momentum -d momentum

# Run migrations (from app container)
docker exec -it momentum-app npx prisma db push

# Backup database
docker exec momentum-db pg_dump -U momentum momentum > backup.sql
```

### Vercel Deployment (Alternative)

The app is also optimized for Vercel deployment:

```bash
npm run build
vercel --prod
```

## DNS Configuration

| Record | Type | Name | Value |
|--------|------|------|-------|
| A | momentum | 91.99.160.39 | Points subdomain to Hetzner server |

Domain managed at GoDaddy (lolala.be).

## License

Private project.

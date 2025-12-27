import { NextResponse } from 'next/server';
import { auth } from '@/lib/auth';
import { prisma } from '@/lib/prisma';

// GET - Fetch all shown guidance keys for the user
export async function GET() {
  const session = await auth();

  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const guidances = await prisma.userGuidance.findMany({
    where: { userId: session.user.id },
    select: { guidanceKey: true, shownAt: true },
  });

  // Also count how many were shown today (for daily limit)
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const shownToday = guidances.filter(
    (g) => new Date(g.shownAt) >= today
  ).length;

  return NextResponse.json({
    shownKeys: guidances.map((g) => g.guidanceKey),
    shownToday,
  });
}

// POST - Mark a guidance as shown
export async function POST(request: Request) {
  const session = await auth();

  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const body = await request.json();
  const { guidanceKey } = body;

  if (!guidanceKey) {
    return NextResponse.json({ error: 'Guidance key required' }, { status: 400 });
  }

  // Check daily limit (max 2 per day)
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const shownTodayCount = await prisma.userGuidance.count({
    where: {
      userId: session.user.id,
      shownAt: { gte: today },
    },
  });

  if (shownTodayCount >= 2) {
    return NextResponse.json(
      { error: 'Daily guidance limit reached', limitReached: true },
      { status: 429 }
    );
  }

  // Create or update the guidance record
  const guidance = await prisma.userGuidance.upsert({
    where: {
      userId_guidanceKey: {
        userId: session.user.id,
        guidanceKey,
      },
    },
    update: {
      shownAt: new Date(),
    },
    create: {
      userId: session.user.id,
      guidanceKey,
    },
  });

  return NextResponse.json({ success: true, guidance });
}

import { NextResponse } from 'next/server';
import { auth } from '@/lib/auth';
import { prisma } from '@/lib/prisma';

// GET - Fetch onboarding state for the user
export async function GET() {
  const session = await auth();

  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const user = await prisma.user.findUnique({
    where: { id: session.user.id },
    select: {
      hasCompletedOnboarding: true,
      guidances: {
        where: {
          guidanceKey: {
            startsWith: 'onboarding_step_',
          },
        },
        select: { guidanceKey: true },
      },
    },
  });

  if (!user) {
    return NextResponse.json({ error: 'User not found' }, { status: 404 });
  }

  // Extract step IDs from guidance keys (e.g., "onboarding_step_welcome" -> "welcome")
  const completedSteps = user.guidances.map((g) =>
    g.guidanceKey.replace('onboarding_step_', '')
  );

  return NextResponse.json({
    hasCompletedOnboarding: user.hasCompletedOnboarding,
    completedSteps,
  });
}

// POST - Mark an onboarding step as complete
export async function POST(request: Request) {
  const session = await auth();

  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const body = await request.json();
  const { stepId, isComplete } = body;

  if (!stepId) {
    return NextResponse.json({ error: 'Step ID required' }, { status: 400 });
  }

  // Record the completed step using guidance system
  const guidanceKey = `onboarding_step_${stepId}`;

  await prisma.userGuidance.upsert({
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

  // If all steps complete, mark onboarding as done
  if (isComplete) {
    await prisma.user.update({
      where: { id: session.user.id },
      data: { hasCompletedOnboarding: true },
    });
  }

  return NextResponse.json({ success: true });
}

// PATCH - Skip onboarding entirely
export async function PATCH(request: Request) {
  const session = await auth();

  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const body = await request.json();

  if (body.skip) {
    await prisma.user.update({
      where: { id: session.user.id },
      data: { hasCompletedOnboarding: true },
    });
  }

  return NextResponse.json({ success: true });
}

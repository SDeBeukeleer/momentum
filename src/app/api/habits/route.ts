import { NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { prisma } from "@/lib/prisma";

export async function GET() {
  const session = await auth();

  if (!session?.user?.id) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const habits = await prisma.habit.findMany({
    where: {
      userId: session.user.id,
      isArchived: false,
    },
    include: {
      completions: {
        orderBy: { date: "desc" },
        take: 30,
      },
    },
    orderBy: { createdAt: "asc" },
  });

  return NextResponse.json(habits);
}

export async function POST(request: Request) {
  const session = await auth();

  if (!session?.user?.id) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const body = await request.json();
  const {
    name,
    description,
    icon,
    color,
    creditsToEarn,
    completionsForCredit,
    frequency,
    targetDays,
  } = body;

  if (!name) {
    return NextResponse.json({ error: "Name is required" }, { status: 400 });
  }

  const habit = await prisma.habit.create({
    data: {
      userId: session.user.id,
      name,
      description,
      icon: icon || "target",
      color: color || "#6366f1",
      creditsToEarn: creditsToEarn || 1,
      completionsForCredit: completionsForCredit || 10,
      frequency: frequency || "daily",
      targetDays,
    },
  });

  return NextResponse.json(habit);
}

import { NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { prisma } from "@/lib/prisma";

// Parse "YYYY-MM-DD" string to UTC midnight Date
function parseLocalDateString(dateStr: string): Date {
  const [year, month, day] = dateStr.split('-').map(Number);
  return new Date(Date.UTC(year, month - 1, day));
}

// Format date as YYYY-MM-DD
function formatDate(date: Date): string {
  return `${date.getUTCFullYear()}-${String(date.getUTCMonth() + 1).padStart(2, '0')}-${String(date.getUTCDate()).padStart(2, '0')}`;
}

// GET - List activity logs
export async function GET() {
  const session = await auth();

  if (!session?.user?.id) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const activityLogs = await prisma.activityLog.findMany({
    where: { userId: session.user.id },
    orderBy: { date: "desc" },
    take: 100,
  });

  return NextResponse.json(activityLogs);
}

// POST - Create activity log
export async function POST(request: Request) {
  const session = await auth();

  if (!session?.user?.id) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const body = await request.json();
  const { activityType, date, duration, distance, notes, metrics } = body;

  if (!activityType) {
    return NextResponse.json({ error: "Activity type is required" }, { status: 400 });
  }

  const logDate = date ? parseLocalDateString(date) : parseLocalDateString(formatDate(new Date()));

  const activityLog = await prisma.activityLog.create({
    data: {
      userId: session.user.id,
      activityType,
      date: logDate,
      duration: duration || null,
      distance: distance || null,
      notes: notes || null,
      metrics: metrics || null,
    },
  });

  return NextResponse.json(activityLog);
}

// DELETE - Delete activity log
export async function DELETE(request: Request) {
  const session = await auth();

  if (!session?.user?.id) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { searchParams } = new URL(request.url);
  const id = searchParams.get("id");

  if (!id) {
    return NextResponse.json({ error: "ID is required" }, { status: 400 });
  }

  // Verify ownership
  const activityLog = await prisma.activityLog.findFirst({
    where: { id, userId: session.user.id },
  });

  if (!activityLog) {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }

  await prisma.activityLog.delete({ where: { id } });

  return NextResponse.json({ success: true });
}

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

// GET - List weight logs
export async function GET() {
  const session = await auth();

  if (!session?.user?.id) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const weightLogs = await prisma.weightLog.findMany({
    where: { userId: session.user.id },
    orderBy: { date: "desc" },
    take: 90, // Last 90 days
  });

  return NextResponse.json(weightLogs);
}

// POST - Create weight log
export async function POST(request: Request) {
  const session = await auth();

  if (!session?.user?.id) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const body = await request.json();
  const { weight, date, notes } = body;

  if (!weight || typeof weight !== "number") {
    return NextResponse.json({ error: "Weight is required" }, { status: 400 });
  }

  // Use today if no date provided
  const logDate = date ? parseLocalDateString(date) : parseLocalDateString(formatDate(new Date()));

  // Upsert - update if exists for this date, create if not
  const weightLog = await prisma.weightLog.upsert({
    where: {
      userId_date: {
        userId: session.user.id,
        date: logDate,
      },
    },
    update: {
      weight,
      notes: notes || null,
    },
    create: {
      userId: session.user.id,
      weight,
      date: logDate,
      notes: notes || null,
    },
  });

  return NextResponse.json(weightLog);
}

// DELETE - Delete weight log
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
  const weightLog = await prisma.weightLog.findFirst({
    where: { id, userId: session.user.id },
  });

  if (!weightLog) {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }

  await prisma.weightLog.delete({ where: { id } });

  return NextResponse.json({ success: true });
}

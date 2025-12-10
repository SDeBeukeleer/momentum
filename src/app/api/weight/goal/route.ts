import { NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { prisma } from "@/lib/prisma";

// POST - Save goal weight
export async function POST(request: Request) {
  const session = await auth();

  if (!session?.user?.id) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const body = await request.json();
  const { goalWeight } = body;

  // Update user's goal weight
  const user = await prisma.user.update({
    where: { id: session.user.id },
    data: {
      goalWeight: goalWeight || null,
    },
    select: {
      id: true,
      goalWeight: true,
    },
  });

  return NextResponse.json(user);
}

// GET - Get goal weight
export async function GET() {
  const session = await auth();

  if (!session?.user?.id) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const user = await prisma.user.findUnique({
    where: { id: session.user.id },
    select: {
      goalWeight: true,
    },
  });

  return NextResponse.json(user);
}

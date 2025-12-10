import { PrismaClient } from "@prisma/client";
import { PrismaPg } from "@prisma/adapter-pg";
import { Pool } from "pg";
import { hash } from "bcryptjs";

const pool = new Pool({
  connectionString: process.env.DATABASE_URL || "postgresql://momentum:momentum_dev_password@localhost:5433/momentum",
});
const adapter = new PrismaPg(pool);
const prisma = new PrismaClient({ adapter });

async function main() {
  // Create test user for Playwright testing
  const testEmail = "test@momentum.app";
  const testPassword = "Test1234!";

  const existingUser = await prisma.user.findUnique({
    where: { email: testEmail },
  });

  if (!existingUser) {
    const hashedPassword = await hash(testPassword, 12);

    const user = await prisma.user.create({
      data: {
        email: testEmail,
        password: hashedPassword,
        name: "Test User",
      },
    });

    console.log(`Created test user: ${user.email}`);
    console.log(`Password: ${testPassword}`);
  } else {
    console.log(`Test user already exists: ${existingUser.email}`);
  }
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });

import { PrismaClient } from '@prisma/client'

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined
}

export const db =
  globalForPrisma.prisma ??
  new PrismaClient({
    log: process.env.NODE_ENV === 'development' ? ['error'] : [],
  })

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = db

// Track if DB has been verified
let dbReady = false

export async function ensureDatabase() {
  if (dbReady) return true

  try {
    // Try a simple query to check if tables exist
    await db.admin.count()
    dbReady = true
    return true
  } catch {
    // Tables might not exist, try to create them
    return false
  }
}
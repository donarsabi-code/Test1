import { db } from '@/lib/db';
import { NextResponse } from 'next/server';

// GET /api/init-db - Ensures database tables exist and admin is created
export async function GET() {
  try {
    // Test if tables exist by querying
    await db.admin.count();

    // Ensure default admin exists
    const adminCount = await db.admin.count();
    if (adminCount === 0) {
      await db.admin.create({
        data: { email: 'admin@estam.cg', password: 'Estam@2025' },
      });
    }

    return NextResponse.json({ success: true, initialized: true });
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : 'Erreur';
    return NextResponse.json({
      success: false,
      error: message,
      hint: 'La base de données doit être configurée dans Vercel (Storage > Postgres)'
    }, { status: 500 });
  }
}
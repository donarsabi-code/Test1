import { db } from '@/lib/db';
import { NextRequest, NextResponse } from 'next/server';

async function ensureAdmin() {
  const count = await db.admin.count();
  if (count === 0) {
    await db.admin.create({
      data: { email: 'admin@estam.cg', password: 'Estam@2025' },
    });
  }
}

// POST /api/admin/login
export async function POST(req: NextRequest) {
  try {
    await ensureAdmin();
    const { email, password } = await req.json();
    if (!email || !password) {
      return NextResponse.json({ error: 'Email et mot de passe requis' }, { status: 400 });
    }
    const admin = await db.admin.findFirst();
    if (!admin || admin.email !== email || admin.password !== password) {
      return NextResponse.json({ error: 'Identifiants incorrects' }, { status: 401 });
    }
    const studentCount = await db.student.count();
    const verifiedCount = await db.student.count({ where: { verified: true } });
    return NextResponse.json({
      success: true,
      admin: { id: admin.id, email: admin.email },
      stats: { studentCount, verifiedCount },
    });
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : 'Erreur serveur';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}

// GET /api/admin/login
export async function GET() {
  await ensureAdmin();
  const admin = await db.admin.findFirst();
  return NextResponse.json({ id: admin?.id, email: admin?.email });
}
import { db } from '@/lib/db';
import { NextRequest, NextResponse } from 'next/server';

// POST /api/notifications/broadcast - Send notification to ALL students
export async function POST(req: NextRequest) {
  try {
    const { titre, message, type } = await req.json();
    if (!titre || !message) {
      return NextResponse.json({ error: 'titre et message requis' }, { status: 400 });
    }
    const students = await db.student.findMany({ where: { verified: true }, select: { id: true } });
    const notifType = type || 'info';
    const data = students.map(s => ({
      studentId: s.id,
      titre,
      message,
      type: notifType,
    }));
    if (data.length > 0) {
      await db.notification.createMany({ data });
    }
    return NextResponse.json({ success: true, sent: data.length });
  } catch (error: unknown) {
    const msg = error instanceof Error ? error.message : 'Erreur serveur';
    return NextResponse.json({ error: msg }, { status: 500 });
  }
}
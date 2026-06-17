import { db } from '@/lib/db';
import { NextRequest, NextResponse } from 'next/server';

// GET /api/notifications?studentDbId=xxx
export async function GET(req: NextRequest) {
  try {
    const { searchParams } = new URL(req.url);
    const studentDbId = searchParams.get('studentDbId');
    if (!studentDbId) {
      return NextResponse.json({ error: 'studentDbId requis' }, { status: 400 });
    }
    const notifications = await db.notification.findMany({
      where: { studentId: studentDbId },
      orderBy: { createdAt: 'desc' },
    });
    return NextResponse.json({ notifications });
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : 'Erreur serveur';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}

// PUT /api/notifications - Mark as read
export async function PUT(req: NextRequest) {
  try {
    const { notificationId } = await req.json();
    if (!notificationId) {
      return NextResponse.json({ error: 'notificationId requis' }, { status: 400 });
    }
    await db.notification.update({
      where: { id: notificationId },
      data: { lu: true },
    });
    return NextResponse.json({ success: true });
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : 'Erreur serveur';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
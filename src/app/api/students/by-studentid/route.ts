import { db } from '@/lib/db';
import { NextRequest, NextResponse } from 'next/server';

// GET /api/students/by-studentid?studentId=EST123456789
export async function GET(req: NextRequest) {
  try {
    const { searchParams } = new URL(req.url);
    const studentId = searchParams.get('studentId');
    if (!studentId) {
      return NextResponse.json({ error: 'studentId requis' }, { status: 400 });
    }
    const student = await db.student.findUnique({
      where: { studentId },
      include: {
        grades: { orderBy: { createdAt: 'desc' } },
        payments: { orderBy: { createdAt: 'desc' } },
        notifications: { orderBy: { createdAt: 'desc' }, take: 20 },
      },
    });
    if (!student) {
      return NextResponse.json({ error: 'Étudiant non trouvé' }, { status: 404 });
    }
    return NextResponse.json({ student });
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : 'Erreur serveur';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
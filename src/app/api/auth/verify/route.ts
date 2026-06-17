import { db } from '@/lib/db';
import { NextRequest, NextResponse } from 'next/server';

// POST /api/auth/verify - Verify student account with code
export async function POST(req: NextRequest) {
  try {
    const { studentId, code } = await req.json();

    if (!studentId || !code) {
      return NextResponse.json({ error: 'Identifiant et code requis' }, { status: 400 });
    }

    const student = await db.student.findUnique({ where: { studentId } });

    if (!student) {
      return NextResponse.json({ error: 'Étudiant non trouvé' }, { status: 404 });
    }

    if (student.verificationCode !== code) {
      return NextResponse.json({ error: 'Code de vérification incorrect' }, { status: 400 });
    }

    await db.student.update({
      where: { studentId },
      data: { verified: true, verificationCode: null },
    });

    return NextResponse.json({ success: true, message: 'Compte vérifié avec succès' });
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : 'Erreur serveur';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
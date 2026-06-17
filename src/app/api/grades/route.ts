import { db } from '@/lib/db';
import { NextRequest, NextResponse } from 'next/server';

// GET /api/grades?studentId=xxx
export async function GET(req: NextRequest) {
  try {
    const { searchParams } = new URL(req.url);
    const studentDbId = searchParams.get('studentDbId');
    if (!studentDbId) {
      return NextResponse.json({ error: 'studentDbId requis' }, { status: 400 });
    }
    const grades = await db.grade.findMany({
      where: { studentId: studentDbId },
      orderBy: { createdAt: 'desc' },
    });
    return NextResponse.json({ grades });
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : 'Erreur serveur';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}

// POST /api/grades - Create a grade (admin)
export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { studentId, matiere, type, note, coefficient, semestre, anneeScolaire, comment } = body;
    if (!studentId || !matiere || !type || !note || !semestre) {
      return NextResponse.json({ error: 'Champs obligatoires manquants' }, { status: 400 });
    }
    const grade = await db.grade.create({
      data: {
        studentId, matiere, type, note,
        coefficient: coefficient || null,
        semestre, anneeScolaire: anneeScolaire || new Date().getFullYear().toString(),
        comment: comment || null,
      },
    });
    // Create notification for student
    const student = await db.student.findUnique({ where: { id: studentId } });
    if (student) {
      await db.notification.create({
        data: {
          studentId,
          titre: 'Nouvelle note publiée',
          message: `Votre note de ${matiere} (${type}) a été publiée : ${note}`,
          type: 'note',
        },
      });
    }
    return NextResponse.json({ success: true, grade });
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : 'Erreur serveur';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
import { db } from '@/lib/db';
import { NextRequest, NextResponse } from 'next/server';

// POST /api/auth/login - Student login
export async function POST(req: NextRequest) {
  try {
    const { email, password } = await req.json();

    if (!email || !password) {
      return NextResponse.json({ error: 'Email et mot de passe requis' }, { status: 400 });
    }

    const student = await db.student.findUnique({ where: { email } });

    if (!student || student.password !== password) {
      return NextResponse.json({ error: 'Identifiants incorrects' }, { status: 401 });
    }

    if (!student.verified) {
      return NextResponse.json({ error: 'Compte non vérifié', needsVerification: true, studentId: student.studentId }, { status: 403 });
    }

    const notifications = await db.notification.findMany({
      where: { studentId: student.id },
      orderBy: { createdAt: 'desc' },
      take: 10,
    });

    return NextResponse.json({
      success: true,
      student: {
        id: student.id,
        studentId: student.studentId,
        email: student.email,
        firstName: student.firstName,
        lastName: student.lastName,
        filiereCategory: student.filiereCategory,
        filiere: student.filiere,
        niveau: student.niveau,
        anneeScolaire: student.anneeScolaire,
        city: student.city,
        phone: student.phone,
        photoUrl: student.photoUrl,
        status: student.status,
      },
      notifications,
    });
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : 'Erreur serveur';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
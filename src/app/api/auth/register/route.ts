import { db } from '@/lib/db';
import { NextRequest, NextResponse } from 'next/server';
import { randomInt } from 'crypto';

// POST /api/auth/register - Student registration
export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const {
      email, password, firstName, lastName, dateOfBirth, phone,
      address, city, nationality, genre, filiereCategory, filiere, niveau, anneeScolaire
    } = body;

    console.log('[REGISTER] filiereCategory:', filiereCategory, 'filiere:', filiere);

    if (!email || !password || !firstName || !lastName || !filiereCategory || !filiere || !niveau) {
      return NextResponse.json({ error: 'Champs obligatoires manquants' }, { status: 400 });
    }

    // Only allow @gmail.com emails
    if (!email.toLowerCase().endsWith('@gmail.com')) {
      return NextResponse.json({ error: 'Seules les adresses @gmail.com sont acceptées' }, { status: 400 });
    }

    const existingStudent = await db.student.findUnique({ where: { email: email.toLowerCase() } });
    if (existingStudent) {
      return NextResponse.json({ error: 'Cet email est déjà utilisé' }, { status: 409 });
    }

    // Generate student ID: EST + 9 digits
    const digits = Array.from({ length: 9 }, () => randomInt(0, 10)).join('');
    const studentId = `EST${digits}`;

    // Generate verification code
    const verificationCode = Array.from({ length: 6 }, () => randomInt(0, 10)).join('');

    const student = await db.student.create({
      data: {
        studentId,
        email: email.toLowerCase(),
        password,
        firstName,
        lastName,
        dateOfBirth: dateOfBirth || null,
        phone: phone || null,
        address: address || null,
        city: city || null,
        nationality: nationality || null,
        genre: genre || null,
        filiereCategory,
        filiere,
        niveau,
        anneeScolaire: anneeScolaire || new Date().getFullYear().toString(),
        verified: false,
        verificationCode,
      },
    });

    // Create notification for admin
    await db.admin.findFirst().then(async (admin) => {
      if (admin) {
        await db.notification.create({
          data: {
            studentId: student.id,
            titre: 'Nouvelle inscription',
            message: `${firstName} ${lastName} (${studentId}) vient de s\'inscrire en ${filiere}.`,
            type: 'info',
          },
        });
      }
    });

    return NextResponse.json({
      success: true,
      message: 'Inscription réussie',
      studentId: student.studentId,
      verificationCode,
      email: student.email,
    });
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : 'Erreur serveur';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
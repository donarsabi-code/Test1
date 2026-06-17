import { db } from '@/lib/db';
import { NextRequest, NextResponse } from 'next/server';

// GET /api/payments?studentDbId=xxx
export async function GET(req: NextRequest) {
  try {
    const { searchParams } = new URL(req.url);
    const studentDbId = searchParams.get('studentDbId');
    if (!studentDbId) {
      return NextResponse.json({ error: 'studentDbId requis' }, { status: 400 });
    }
    const payments = await db.payment.findMany({
      where: { studentId: studentDbId },
      orderBy: { createdAt: 'desc' },
    });
    return NextResponse.json({ payments });
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : 'Erreur serveur';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}

// POST /api/payments - Create/update payment (admin)
export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { studentId, mois, montant, datePaiement, statut, anneeScolaire } = body;
    if (!studentId || !mois || !montant) {
      return NextResponse.json({ error: 'Champs obligatoires manquants' }, { status: 400 });
    }
    const payment = await db.payment.create({
      data: {
        studentId, mois, montant: parseFloat(montant),
        datePaiement: datePaiement || null,
        statut: statut || 'impaye',
        anneeScolaire: anneeScolaire || new Date().getFullYear().toString(),
      },
    });
    const student = await db.student.findUnique({ where: { id: studentId } });
    if (student) {
      await db.notification.create({
        data: {
          studentId,
          titre: statut === 'paye' ? 'Paiement enregistré' : 'Paiement en attente',
          message: `Le paiement de ${mois} (${montant} FCFA) est marqué comme ${statut === 'paye' ? 'payé' : 'impayé'}.${datePaiement ? ` Date: ${datePaiement}` : ''}`,
          type: 'paiement',
        },
      });
    }
    return NextResponse.json({ success: true, payment });
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : 'Erreur serveur';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
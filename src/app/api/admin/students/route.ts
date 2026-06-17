import { db } from '@/lib/db';
import { NextRequest, NextResponse } from 'next/server';

// GET /api/admin/students?category=Gestion&filiere=Comptabilité&search=EST123456789
export async function GET(req: NextRequest) {
  try {
    const { searchParams } = new URL(req.url);
    const category = searchParams.get('category');
    const filiere = searchParams.get('filiere');
    const search = searchParams.get('search');

    const where: Record<string, unknown> = {};

    if (category) where.filiereCategory = category;
    if (filiere) where.filiere = filiere;
    if (search) where.studentId = { contains: search };

    const students = await db.student.findMany({
      where: Object.keys(where).length > 0 ? where : undefined,
      orderBy: { createdAt: 'desc' },
      include: {
        grades: { orderBy: { createdAt: 'desc' } },
        payments: { orderBy: { createdAt: 'desc' } },
      },
    });

    return NextResponse.json({ students });
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : 'Erreur serveur';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
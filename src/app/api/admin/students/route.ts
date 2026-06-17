import { db } from '@/lib/db';
import { NextRequest, NextResponse } from 'next/server';
import { Prisma } from '@prisma/client';

// GET /api/admin/students?category=Gestion&filiere=Comptabilité&search=EST123 or Jean
export async function GET(req: NextRequest) {
  try {
    const { searchParams } = new URL(req.url);
    const category = searchParams.get('category');
    const filiere = searchParams.get('filiere');
    const search = searchParams.get('search');

    const where: Record<string, unknown> = {};

    if (category) where.filiereCategory = category;
    if (filiere) where.filiere = filiere;
    if (search) {
      where.OR = [
        { studentId: { contains: search } },
        { firstName: { contains: search } },
        { lastName: { contains: search } },
      ];
    }

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

// DELETE /api/admin/students?ids=id1,id2
export async function DELETE(req: NextRequest) {
  try {
    const { searchParams } = new URL(req.url);
    const ids = searchParams.get('ids');
    if (!ids) {
      return NextResponse.json({ error: 'ids requis' }, { status: 400 });
    }
    const idList = ids.split(',').filter(Boolean);
    const result = await db.student.deleteMany({
      where: { id: { in: idList } },
    });
    return NextResponse.json({ success: true, deleted: result.count });
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : 'Erreur serveur';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
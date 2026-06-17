import { db } from '@/lib/db';
import { NextResponse } from 'next/server';

// GET /api/admin/counts - Get student counts per filière
export async function GET() {
  try {
    const allStudents = await db.student.findMany({
      select: { filiereCategory: true, filiere: true },
    });
    
    const counts: Record<string, number> = {};
    for (const s of allStudents) {
      const key = `${s.filiereCategory}|||${s.filiere}`;
      counts[key] = (counts[key] || 0) + 1;
    }
    
    const categoryCounts: Record<string, number> = {};
    for (const s of allStudents) {
      categoryCounts[s.filiereCategory] = (categoryCounts[s.filiereCategory] || 0) + 1;
    }

    return NextResponse.json({ counts, categoryCounts, total: allStudents.length });
  } catch (error: unknown) {
    const msg = error instanceof Error ? error.message : 'Erreur serveur';
    return NextResponse.json({ error: msg }, { status: 500 });
  }
}
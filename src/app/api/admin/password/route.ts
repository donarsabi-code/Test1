import { db } from '@/lib/db';
import { NextRequest, NextResponse } from 'next/server';

// PUT /api/admin/password - Change admin password
export async function PUT(req: NextRequest) {
  try {
    const { currentPassword, newPassword } = await req.json();
    if (!currentPassword || !newPassword) {
      return NextResponse.json({ error: 'Mots de passe requis' }, { status: 400 });
    }
    const admin = await db.admin.findFirst();
    if (!admin || admin.password !== currentPassword) {
      return NextResponse.json({ error: 'Mot de passe actuel incorrect' }, { status: 401 });
    }
    await db.admin.update({
      where: { id: admin.id },
      data: { password: newPassword },
    });
    return NextResponse.json({ success: true, message: 'Mot de passe modifié avec succès' });
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : 'Erreur serveur';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
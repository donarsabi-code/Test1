import { db } from '@/lib/db';
import { NextRequest, NextResponse } from 'next/server';

// PUT /api/students/update - Student updates own profile
export async function PUT(req: NextRequest) {
  try {
    const body = await req.json();
    const { id, firstName, lastName, phone, address, city, nationality, genre, dateOfBirth } = body;
    if (!id) {
      return NextResponse.json({ error: 'id requis' }, { status: 400 });
    }
    const updateData: Record<string, unknown> = {};
    if (firstName !== undefined) updateData.firstName = firstName;
    if (lastName !== undefined) updateData.lastName = lastName;
    if (phone !== undefined) updateData.phone = phone;
    if (address !== undefined) updateData.address = address;
    if (city !== undefined) updateData.city = city;
    if (nationality !== undefined) updateData.nationality = nationality;
    if (genre !== undefined) updateData.genre = genre;
    if (dateOfBirth !== undefined) updateData.dateOfBirth = dateOfBirth;

    const student = await db.student.update({
      where: { id },
      data: updateData,
    });

    return NextResponse.json({ success: true, student });
  } catch (error: unknown) {
    const msg = error instanceof Error ? error.message : 'Erreur serveur';
    return NextResponse.json({ error: msg }, { status: 500 });
  }
}
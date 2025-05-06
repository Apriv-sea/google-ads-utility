import { PrismaClient } from '@prisma/client';
import bcrypt from 'bcryptjs';
const prisma = new PrismaClient();

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).end();
  const { email } = req.body;
  try {
    await prisma.user.upsert({
      where: { email },
      update: {},
      create: { email }
    });
    res.status(201).end();
  } catch {
    res.status(400).json({ error: 'Erreur création utilisateur' });
  }
}
import { getSession } from 'next-auth/react';
import { PrismaClient } from '@prisma/client';
const prisma = new PrismaClient();

export default async function handler(req, res) {
  const session = await getSession({ req });
  if (!session || session.user.id !== req.query.id) return res.status(401).end();
  if (req.method !== 'POST') return res.status(405).end();
  const { iaProvider, iaModel } = req.body;
  await prisma.user.update({ where: { id: req.query.id }, data: { iaProvider, iaModel } });
  res.status(200).end();
}
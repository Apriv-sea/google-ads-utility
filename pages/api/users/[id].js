import { getSession } from 'next-auth/react'
import { PrismaClient } from '@prisma/client'
const prisma = new PrismaClient()

export default async function handler(req, res) {
  const session = await getSession({ req })
  if (!session) return res.status(401).end()
  const { id } = req.query
  if (session.user.id !== id) return res.status(403).end()
  const user = await prisma.user.findUnique({ where: { id }, select: { openaiKey: true, anthropicKey: true, googleId: true } })
  res.json(user)
}
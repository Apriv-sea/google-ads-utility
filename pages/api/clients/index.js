import { getSession } from 'next-auth/react'
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

export default async function handler(req, res) {
  const session = await getSession({ req })
  if (!session) return res.status(401).end()
  const userId = session.user.id
  if (req.method === 'GET') {
    const clients = await prisma.client.findMany({ where: { userId } })
    res.json(clients)
  } else if (req.method === 'POST') {
    const { name } = req.body
    const client = await prisma.client.create({ data: { name, userId } })
    res.status(201).json(client)
  } else {
    res.status(405).end()
  }
}
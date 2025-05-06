import { getSession } from 'next-auth/react'
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

export default async function handler(req, res) {
  const session = await getSession({ req })
  if (!session) return res.status(401).end()
  const { clientId } = req.query
  if (req.method === 'POST') {
    const { context } = req.body
    await prisma.client.update({ where: { id: clientId }, data: { context } })
    res.status(200).end()
  } else {
    res.status(405).end()
  }
}
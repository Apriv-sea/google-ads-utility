import { getSession } from 'next-auth/react'
import axios from 'axios'
import { useState } from 'react'
import { useRouter } from 'next/router'

export default function ContextPage({ initialContext, clientId }) {
  const [context, setContext] = useState(initialContext || '')
  const router = useRouter()

  const save = async () => {
    await axios.post(`/api/clients/${clientId}/context`, { context })
  }

  return (
    <div className="p-6 max-w-xl mx-auto">
      <h1 className="text-xl mb-4">Contexte du client</h1>
      <textarea
        value={context}
        onChange={e => setContext(e.target.value)}
        className="w-full border p-2 h-48"
        placeholder="Décrivez le contexte..."
      />
      <div className="mt-4 flex justify-between">
        <button onClick={save} className="bg-blue-600 text-white px-4 py-2 rounded">Enregistrer</button>
        <button onClick={() => router.push(`/clients/${clientId}/sheet`)} className="bg-green-600 text-white px-4 py-2 rounded">Suivant</button>
      </div>
    </div>
}

export async function getServerSideProps(ctx) {
  const session = await getSession(ctx)
  if (!session) return { redirect: { destination: '/login', permanent: false } }
  const { clientId } = ctx.params
  const prisma = new (await import('@prisma/client')).PrismaClient()
  const client = await prisma.client.findUnique({ where: { id: clientId } })
  if (!client || client.userId !== session.user.id) return { notFound: true }
  return { props: { initialContext: client.context || '', clientId } }
}
import { getSession } from 'next-auth/react'
import axios from 'axios'
import Link from 'next/link'

export default function Dashboard({ clients }) {
  return (
    <div className="p-6">
      <h1 className="text-2xl mb-4">Mes clients</h1>
      <Link href="/clients/new"><a className="bg-green-500 text-white px-4 py-2 rounded">+ Nouveau client</a></Link>
      <ul className="mt-4">
        {clients.map(c => (
          <li key={c.id} className="mb-2">
            <Link href={`/clients/${c.id}/context`}><a className="text-blue-600">{c.name}</a></Link>
          </li>
        ))}
      </ul>
    </div>
  )
}

export async function getServerSideProps(ctx) {
  const session = await getSession(ctx)
  if (!session) return { redirect: { destination: '/login', permanent: false } }
  const res = await axios.get(`${process.env.NEXTAUTH_URL}/api/clients`, { headers: { cookie: ctx.req.headers.cookie } })
  return { props: { clients: res.data } }
}
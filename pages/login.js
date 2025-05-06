import { getCsrfToken } from 'next-auth/react'

export default function Login({ csrfToken }) {
  return (
    <div className="flex items-center justify-center h-screen">
      <form method="post" action="/api/auth/callback/credentials" className="p-6 bg-white rounded shadow w-full max-w-sm">
        <input name="csrfToken" type="hidden" defaultValue={csrfToken} />
        <h1 className="text-xl mb-4">Se connecter</h1>
        <label className="block mb-2">Email
          <input name="email" type="email" required className="border p-2 w-full"/>
        </label>
        <label className="block mb-4">Mot de passe
          <input name="password" type="password" required className="border p-2 w-full"/>
        </label>
        <button type="submit" className="w-full bg-blue-600 text-white p-2 rounded">Se connecter</button>
        <p className="mt-4 text-center">
          Pas de compte ? <a href="/register" className="text-blue-600">Inscrivez-vous</a>
        </p>
      </form>
    </div>
  )
}

export async function getServerSideProps(context) {
  return { props: { csrfToken: await getCsrfToken(context) } }
}
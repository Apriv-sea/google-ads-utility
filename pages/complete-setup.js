import Link from 'next/link'

export default function CompleteSetup() {
  return (
    <div className="flex flex-col items-center justify-center h-screen p-4">
      <h1 className="text-2xl mb-4">Configuration incomplète</h1>
      <p className="mb-2">Vous devez :</p>
      <ul className="list-disc list-inside mb-4">
        <li>Renseigner vos clés API OpenAI / Anthropic (<Link href="/profile"><a className="text-blue-600">Voir profil</a></Link>)</li>
        <li>Lier votre compte Google via OAuth (<Link href="/api/auth/signin"><a className="text-blue-600">Se connecter avec Google</a></Link>)</li>
      </ul>
      <p>Après ces étapes, vous pourrez accéder à l’outil.</p>
    </div>
  )
}
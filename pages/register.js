import { useState } from 'react'
import axios from 'axios'
import { signIn } from 'next-auth/react'

export default function Register() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [openaiKey, setOpenaiKey] = useState('')
  const [anthropicKey, setAnthropicKey] = useState('')

  const handleSubmit = async e => {
    e.preventDefault()
    await axios.post('/api/register', { email, password, openaiKey, anthropicKey })
    signIn('google', { callbackUrl: '/dashboard' })
  }

  return (
    <div className="flex items-center justify-center h-screen">
      <form onSubmit={handleSubmit} className="p-6 bg-white rounded shadow w-full max-w-md">
        <h1 className="text-xl mb-4">Créer un compte</h1>
        <label className="block mb-2">Email
          <input type="email" required value={email} onChange={e => setEmail(e.target.value)} className="border p-2 w-full"/>
        </label>
        <label className="block mb-2">Mot de passe
          <input type="password" required value={password} onChange={e => setPassword(e.target.value)} className="border p-2 w-full"/>
        </label>
        <label className="block mb-2">Clé API OpenAI
          <input type="text" required value={openaiKey} onChange={e => setOpenaiKey(e.target.value)} className="border p-2 w-full"/>
        </label>
        <label className="block mb-4">Clé API Claude (Anthropic)
          <input type="text" required value={anthropicKey} onChange={e => setAnthropicKey(e.target.value)} className="border p-2 w-full"/>
        </label>
        <button type="submit" className="w-full bg-green-600 text-white p-2 rounded">S'inscrire et lier Google</button>
      </form>
    </div>
  )
}
import { useState, useEffect } from 'react';
import { useSession, signOut } from 'next-auth/react';
import axios from 'axios';
import { useRouter } from 'next/router';

export default function Profile() {
  const { data: session, status } = useSession();
  const router = useRouter();
  const [openaiKey, setOpenaiKey] = useState('');
  const [anthropicKey, setAnthropicKey] = useState('');
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (status === 'loading') return;
    if (!session) router.push('/');
  }, [status, session]);

  const handleSubmit = async e => {
    e.preventDefault();
    setSaving(true);
    await axios.post(`/api/users/${session.user.id}/keys`, { openaiKey, anthropicKey });
    router.push('/select-ia');
  };

  return (
    <div className="p-6 max-w-md mx-auto">
      <h1 className="text-2xl mb-4">Bienvenue, {session.user.email}</h1>
      <p className="mb-2">Pour continuer, renseignez vos clés API :</p>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label>Clé API OpenAI</label>
          <input type="text" required value={openaiKey} onChange={e => setOpenaiKey(e.target.value)} className="border p-2 w-full" />
        </div>
        <div>
          <label>Clé API Anthropic</label>
          <input type="text" required value={anthropicKey} onChange={e => setAnthropicKey(e.target.value)} className="border p-2 w-full" />
        </div>
        <button type="submit" disabled={saving} className="w-full bg-green-600 text-white p-2 rounded">
          {saving ? 'Enregistrement…' : 'Enregistrer et continuer'}
        </button>
      </form>
      <button onClick={() => signOut()} className="mt-4 text-red-600">
        Se déconnecter
      </button>
    </div>
}
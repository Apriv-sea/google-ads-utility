import { useState, useEffect } from 'react';
import { useSession } from 'next-auth/react';
import { useRouter } from 'next/router';
import axios from 'axios';

export default function SelectIA() {
  const { data: session } = useSession();
  const router = useRouter();
  const [provider, setProvider] = useState('openai');
  const [models, setModels] = useState([]);
  const [model, setModel] = useState('');

  useEffect(() => {
    if (!session) return;
    axios.get(`/api/ia/models?provider=${provider}`).then(res => {
      setModels(res.data);
      setModel(res.data[0] || '');
    });
  }, [provider, session]);

  const handleSubmit = async e => {
    e.preventDefault();
    await axios.post(`/api/users/${session.user.id}/settings`, { iaProvider: provider, iaModel: model });
    router.replace('/dashboard');
  };

  return (
    <div className="p-6 max-w-md mx-auto">
      <h1 className="text-2xl mb-4">Choisissez votre IA</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label>Fournisseur</label>
          <select value={provider} onChange={e => setProvider(e.target.value)} className="border p-2 w-full">
            <option value="openai">OpenAI</option>
            <option value="anthropic">Anthropic</option>
          </select>
        </div>
        <div>
          <label>Modèle</label>
          <select value={model} onChange={e => setModel(e.target.value)} className="border p-2 w-full">
            {models.map(m => <option key={m} value={m}>{m}</option>)}
          </select>
        </div>
        <button type="submit" className="w-full bg-blue-600 text-white p-2 rounded">Valider</button>
      </form>
    </div>
);
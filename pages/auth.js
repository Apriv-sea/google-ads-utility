import { useState } from 'react';
import { signIn } from 'next-auth/react';
import axios from 'axios';
import GoogleButton from 'react-google-button';

export default function AuthPage() {
  const [tab, setTab] = useState('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirm, setConfirm] = useState('');
  const [error, setError] = useState('');

  const handleRegister = async e => {
    e.preventDefault();
    if (password !== confirm) {
      setError('Les mots de passe ne correspondent pas');
      return;
    }
    try {
      await axios.post('/api/register', { email, password });
      setTab('login');
      setError('Inscription réussie ! Connectez-vous.');
    } catch (e) {
      setError(e.response?.data?.error || 'Erreur lors de l’inscription');
    }
  };

  const handleLogin = async e => {
    e.preventDefault();
    const res = await signIn('credentials', {
      redirect: false,
      email,
      password
    });
    if (res.error) {
      setError('E-mail ou mot de passe incorrect');
    } else {
      window.location.href = '/';
    }
  };

  return (
    <div className="max-w-md mx-auto mt-20 p-6 bg-white rounded shadow">
      <div className="flex mb-4">
        <button
          className={`flex-1 py-2 ${tab === 'login' ? 'border-b-2 border-blue-600' : ''}`}
          onClick={() => { setTab('login'); setError(''); }}
        >
          Login
        </button>
        <button
          className={`flex-1 py-2 ${tab === 'register' ? 'border-b-2 border-blue-600' : ''}`}
          onClick={() => { setTab('register'); setError(''); }}
        >
          Register
        </button>
      </div>

      {error && <div className="mb-4 text-red-600">{error}</div>}

      {tab === 'login' ? (
        <>
          <form onSubmit={handleLogin} className="space-y-4">
            <label className="block">
              Email
              <input
                type="email"
                required
                value={email}
                onChange={e => setEmail(e.target.value)}
                className="w-full border p-2 rounded"
              />
            </label>
            <label className="block">
              Mot de passe
              <input
                type="password"
                required
                value={password}
                onChange={e => setPassword(e.target.value)}
                className="w-full border p-2 rounded"
              />
            </label>
            <button type="submit" className="w-full bg-blue-600 text-white p-2 rounded">
              Se connecter
            </button>
          </form>
          <div className="mt-4 text-center">ou</div>
          <div className="mt-4">
            <GoogleButton onClick={() => signIn('google', { callbackUrl: '/' })} />
          </div>
        </>
      ) : (
        <>
          <form onSubmit={handleRegister} className="space-y-4">
            <label className="block">
              Email
              <input
                type="email"
                required
                value={email}
                onChange={e => setEmail(e.target.value)}
                className="w-full border p-2 rounded"
              />
            </label>
            <label className="block">
              Mot de passe
              <input
                type="password"
                required
                value={password}
                onChange={e => setPassword(e.target.value)}
                className="w-full border p-2 rounded"
              />
            </label>
            <label className="block">
              Confirmez le mot de passe
              <input
                type="password"
                required
                value={confirm}
                onChange={e => setConfirm(e.target.value)}
                className="w-full border p-2 rounded"
              />
            </label>
            <button type="submit" className="w-full bg-green-600 text-white p-2 rounded">
              S'inscrire
            </button>
          </form>
          <div className="mt-4 text-center">ou</div>
          <div className="mt-4">
            <GoogleButton onClick={() => signIn('google', { callbackUrl: '/select-ia' })} />
          </div>
        </>
      )}
    </div>
  );
}
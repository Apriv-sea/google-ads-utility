import { useSession } from 'next-auth/react';
import GoogleButton from 'react-google-button';
import { signIn } from 'next-auth/react';
import { useRouter } from 'next/router';
import { useEffect } from 'react';

export default function Home() {
  const { data: session, status } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (status === 'loading') return;
    if (session) {
      router.push('/profile');
    }
  }, [session, status]);

  return (
    <div className="flex items-center justify-center h-screen">
      <GoogleButton onClick={() => signIn('google', { callbackUrl: '/profile' })} />
    </div>
  );
}
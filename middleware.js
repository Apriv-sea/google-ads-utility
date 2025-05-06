import { NextResponse } from 'next/server';
import { getToken } from 'next-auth/jwt';

export async function middleware(req) {
  const { pathname } = req.nextUrl;
  const publicPaths = ['/api/auth', '/profile', '/select-ia'];
  if (publicPaths.some(p => pathname.startsWith(p))) return NextResponse.next();
  const token = await getToken({ req, secret: process.env.NEXTAUTH_SECRET });
  if (!token) return NextResponse.redirect('/api/auth/signin');
  const res = await fetch(`${process.env.NEXTAUTH_URL}/api/users/${token.id}`);
  const user = await res.json();
  if (!user.openaiKey || !user.anthropicKey) return NextResponse.redirect('/profile');
  if (!user.iaProvider || !user.iaModel) return NextResponse.redirect('/select-ia');
  return NextResponse.next();
}
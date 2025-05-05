import { NextResponse } from 'next/server'
import { getToken } from 'next-auth/jwt'

export async function middleware(req) {
  const { pathname } = req.nextUrl
  if (pathname.startsWith('/login') || pathname.startsWith('/register') || pathname.startsWith('/api/auth')) {
    return NextResponse.next()
  }
  const token = await getToken({ req, secret: process.env.NEXTAUTH_SECRET })
  if (!token) return NextResponse.redirect('/login')
  const res = await fetch(`${process.env.NEXTAUTH_URL}/api/users/${token.id}`)
  const user = await res.json()
  if (!user.openaiKey || !user.anthropicKey || !user.googleId) {
    return NextResponse.redirect('/complete-setup')
  }
  return NextResponse.next()
}
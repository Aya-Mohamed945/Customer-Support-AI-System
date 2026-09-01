// frontend/app/login/page.tsx
'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import Button from '../components/ui/Button';
import Toast from '../components/ui/Toast';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await fetch('http://localhost:8000/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        setToast({ message: '✅ Login successful!', type: 'success' });
        setTimeout(() => {
          sessionStorage.setItem('token', data.access_token);
          sessionStorage.setItem('user', JSON.stringify(data.user));
          router.push('/');
        }, 1000);
      } else {
        setToast({ message: data.detail || 'Login failed', type: 'error' });
      }
    } catch (err) {
      setToast({ message: 'Network error', type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen py-10 px-4 sm:py-16 lg:py-20 flex items-center justify-center">
      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}

      <div className="max-w-md w-full">
        <div className="text-center mb-10 animate-fade-in-up">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl gradient-bg shadow-2xl mb-4 relative">
            <div className="absolute inset-0 rounded-2xl bg-white/20 blur-xl" />
            <span className="text-3xl text-white relative z-10">🔐</span>
          </div>
          <h2 className="text-3xl font-bold tracking-tight">
            <span className="gradient-text gradient-text-glow">Welcome Back</span>
          </h2>
          <p className="mt-2 text-white/60">Sign in to your account</p>
        </div>

        <div className="glass-card rounded-2xl p-8 sm:p-10 animate-fade-in-up delay-200 glow-blue">
          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-sm font-semibold text-white/90 mb-2">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-5 py-3.5 rounded-xl bg-white/10 backdrop-blur-sm border border-white/10 focus:border-blue-400/50 focus:ring-2 focus:ring-blue-400/20 transition-all duration-300 outline-none text-white placeholder:text-white/40"
                placeholder="you@example.com"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-white/90 mb-2">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-5 py-3.5 rounded-xl bg-white/10 backdrop-blur-sm border border-white/10 focus:border-blue-400/50 focus:ring-2 focus:ring-blue-400/20 transition-all duration-300 outline-none text-white placeholder:text-white/40"
                placeholder="••••••••"
                required
              />
            </div>

            {error && (
              <div className="p-4 bg-red-500/10 backdrop-blur-sm border border-red-500/20 rounded-xl text-red-200 text-sm">
                {error}
              </div>
            )}

            <Button
              type="submit"
              variant="primary"
              size="lg"
              fullWidth
              loading={loading}
            >
              Sign In
            </Button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-white/40 text-sm">
              Don't have an account?{' '}
              <Link href="/signup" className="text-white/70 hover:text-white hover:underline transition-all duration-200">
                Sign Up
              </Link>
            </p>
          </div>
        </div>

        <div className="mt-8 text-center">
          <p className="text-white/20 text-sm font-light tracking-wider">
            ⚡ Powered by Customer Support AI
          </p>
        </div>
      </div>
    </div>
  );
}

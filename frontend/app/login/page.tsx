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
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        setToast({ message: '✅ Welcome back!', type: 'success' });
        setTimeout(() => {
          sessionStorage.setItem('token', data.access_token);
          sessionStorage.setItem('user', JSON.stringify(data.user));
          router.push('/');
        }, 800);
      } else {
        setToast({ message: data.detail || 'Invalid credentials', type: 'error' });
      }
    } catch {
      setToast({ message: 'Connection error. Please try again.', type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-8">
      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}

      <div className="w-full max-w-[420px]">
        {/* ============================================
            HEADER - نفس تصميم الصفحة الرئيسية
            ============================================ */}
        <div className="text-center mb-10 animate-fade-up">
          {/* Logo - نفس اللي في الصفحة الرئيسية */}
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl gradient-bg shadow-2xl mb-4 relative">
            <div className="absolute inset-0 rounded-2xl bg-white/20 blur-xl" />
            <svg 
              className="w-8 h-8 text-white relative z-10" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>

          {/* Brand Name - نفس الـ Gradient text */}
          <h1 className="text-3xl font-bold tracking-tight">
            <span className="gradient-text gradient-text-glow">SupportAI</span>
          </h1>
          
          {/* Tagline */}
          <p className="mt-2 text-sm text-white/50 font-light">
            Intelligent Customer Support Platform
          </p>
          
          {/* Separator - نفس اللي في الصفحة الرئيسية */}
          <div className="flex items-center justify-center gap-3 mt-4">
            <div className="h-px w-8 bg-gradient-to-r from-transparent to-white/10" />
            <span className="text-xs text-white/20">●</span>
            <div className="h-px w-8 bg-gradient-to-l from-transparent to-white/10" />
          </div>

          {/* Welcome Message */}
          <h2 className="mt-5 text-xl font-semibold text-white/90">
            Welcome Back
          </h2>
          <p className="mt-1 text-sm text-white/40">
            Sign in to analyze your support tickets
          </p>
        </div>

        {/* ============================================
            FORM - نفس Glass Card بتاع الصفحة الرئيسية
            ============================================ */}
        <div className="glass-card rounded-2xl p-6 sm:p-8 animate-fade-up delay-200">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-semibold text-white/90 mb-1.5">
                Email Address
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-5 py-3.5 rounded-xl glass-input text-white placeholder:text-white/30 outline-none transition-all duration-300"
                placeholder="you@company.com"
                required
                disabled={loading}
                autoComplete="email"
              />
            </div>

            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label className="block text-sm font-semibold text-white/90">
                  Password
                </label>
                <Link 
                  href="/forgot-password" 
                  className="text-sm text-white/30 hover:text-white/60 transition-colors"
                >
                  Forgot?
                </Link>
              </div>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-5 py-3.5 rounded-xl glass-input text-white placeholder:text-white/30 outline-none transition-all duration-300"
                placeholder="Enter your password"
                required
                disabled={loading}
                autoComplete="current-password"
              />
            </div>

            <Button
              type="submit"
              variant="primary"
              size="lg"
              fullWidth
              loading={loading}
              className="mt-2"
            >
              Sign In
            </Button>
          </form>

          {/* ============================================
              FOOTER
              ============================================ */}
          <div className="mt-6 text-center">
            <p className="text-sm text-white/30">
              Don't have an account?{' '}
              <Link 
                href="/signup" 
                className="text-white/60 hover:text-white transition-colors duration-200 font-medium"
              >
                Create one
              </Link>
            </p>
          </div>
        </div>

        {/* ============================================
            FOOTER - نفس اللي في الصفحة الرئيسية
            ============================================ */}
        <div className="mt-8 text-center">
          <p className="text-xs text-white/20 font-light tracking-wider">
            ⚡ Powered by FastAPI • XGBoost • RAG • Next.js
          </p>
        </div>
      </div>
    </div>
  );
}
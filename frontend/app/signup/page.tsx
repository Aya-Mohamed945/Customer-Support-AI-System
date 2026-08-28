// frontend/app/signup/page.tsx

'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import Button from '../components/ui/Button';
import Toast from '../components/ui/Toast';

export default function SignupPage() {
  const router = useRouter();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/v1/auth/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        setToast({ message: '✅ Account created successfully!', type: 'success' });
        setTimeout(() => router.push('/login'), 1200);
      } else {
        setToast({ message: data.detail || 'Signup failed', type: 'error' });
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
          {/* Logo */}
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl gradient-bg shadow-2xl mb-4 relative">
            <div className="absolute inset-0 rounded-2xl bg-white/20 blur-xl" />
            <svg 
              className="w-8 h-8 text-white relative z-10" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
          </div>

          {/* Brand Name */}
          <h1 className="text-3xl font-bold tracking-tight">
            <span className="gradient-text gradient-text-glow">SupportAI</span>
          </h1>
          
          {/* Tagline */}
          <p className="mt-2 text-sm text-white/50 font-light">
            Intelligent Customer Support Platform
          </p>
          
          {/* Separator */}
          <div className="flex items-center justify-center gap-3 mt-4">
            <div className="h-px w-8 bg-gradient-to-r from-transparent to-white/10" />
            <span className="text-xs text-white/20">●</span>
            <div className="h-px w-8 bg-gradient-to-l from-transparent to-white/10" />
          </div>

          {/* Welcome Message */}
          <h2 className="mt-5 text-xl font-semibold text-white/90">
            Create Account
          </h2>
          <p className="mt-1 text-sm text-white/40">
            Start using SupportAI today
          </p>
        </div>

        {/* ============================================
            FORM - نفس Glass Card
            ============================================ */}
        <div className="glass-card rounded-2xl p-6 sm:p-8 animate-fade-up delay-200">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-semibold text-white/90 mb-1.5">
                Full Name
              </label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full px-5 py-3.5 rounded-xl glass-input text-white placeholder:text-white/30 outline-none transition-all duration-300"
                placeholder="John Doe"
                required
                disabled={loading}
                autoComplete="name"
              />
            </div>

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
              <label className="block text-sm font-semibold text-white/90 mb-1.5">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-5 py-3.5 rounded-xl glass-input text-white placeholder:text-white/30 outline-none transition-all duration-300"
                placeholder="Create a strong password"
                required
                disabled={loading}
                autoComplete="new-password"
                minLength={6}
              />
              <p className="mt-1.5 text-xs text-white/20">
                Must be at least 6 characters
              </p>
            </div>

            <Button
              type="submit"
              variant="primary"
              size="lg"
              fullWidth
              loading={loading}
              className="mt-2"
            >
              Create Account
            </Button>
          </form>

          {/* ============================================
              FOOTER
              ============================================ */}
          <div className="mt-6 text-center">
            <p className="text-sm text-white/30">
              Already have an account?{' '}
              <Link 
                href="/login" 
                className="text-white/60 hover:text-white transition-colors duration-200 font-medium"
              >
                Sign in
              </Link>
            </p>
          </div>
        </div>

        {/* ============================================
            FOOTER
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
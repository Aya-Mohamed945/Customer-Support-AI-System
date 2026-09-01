// frontend/app/signup/page.tsx
'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { User, Mail, Lock, Sparkles, ArrowRight, CheckCircle2 } from 'lucide-react';
import Button from '../components/ui/Button';
import Toast from '../components/ui/Toast';
import { signupUser } from '../utils/api';
import { ToastData } from '../types';

export default function SignupPage() {
  const router = useRouter();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState<ToastData | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await signupUser({ name, email, password });
      setToast({ message: 'Account created successfully!', type: 'success' });
      setTimeout(() => router.push('/login'), 1500);
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Signup failed';
      setToast({ message: msg, type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen py-12 px-4 flex items-center justify-center relative overflow-hidden">
      {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}

      <div className="max-w-4xl w-full grid grid-cols-1 md:grid-cols-2 gap-8 items-center z-10">

        {/* الجانب الأيسر: معلومات ومميزات الموديل */}
        <div className="hidden md:block space-y-6 p-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-semibold">
            <Sparkles className="w-4 h-4" /> Next-Gen AI Support
          </div>
          <h1 className="text-4xl font-extrabold text-white leading-tight">
            Automate your support tickets with <span className="gradient-text gradient-text-glow">Precision AI</span>
          </h1>
          <p className="text-white/60 text-sm">
            Powered by XGBoost &amp; RAG architecture for instant resolution generation.
          </p>

          <div className="space-y-3 pt-4">
            {['Instant Ticket Classification', 'Context-Aware Solutions', 'Real-time Analytics'].map((feat, idx) => (
              <div key={idx} className="flex items-center gap-3 text-white/80 text-sm">
                <CheckCircle2 className="w-5 h-5 text-indigo-400" />
                <span>{feat}</span>
              </div>
            ))}
          </div>
        </div>

        {/* الجانب الأيمن: كارت التسجيل */}
        <div className="glow-card glass-card rounded-3xl p-8 border border-white/10 shadow-2xl backdrop-blur-2xl">
          <div className="mb-6 text-center md:text-left">
            <h2 className="text-2xl font-bold text-white">Create Account</h2>
            <p className="text-white/50 text-xs mt-1">Get started with your free account today</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-medium uppercase tracking-wider text-white/70 mb-1.5">Full Name</label>
              <div className="relative">
                <User className="w-4 h-4 text-white/40 absolute left-3.5 top-3.5" />
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-white/5 border border-white/10 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all duration-200 text-white placeholder:text-white/20 text-sm"
                  placeholder="John Doe"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium uppercase tracking-wider text-white/70 mb-1.5">Email Address</label>
              <div className="relative">
                <Mail className="w-4 h-4 text-white/40 absolute left-3.5 top-3.5" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-white/5 border border-white/10 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all duration-200 text-white placeholder:text-white/20 text-sm"
                  placeholder="name@company.com"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium uppercase tracking-wider text-white/70 mb-1.5">Password</label>
              <div className="relative">
                <Lock className="w-4 h-4 text-white/40 absolute left-3.5 top-3.5" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-white/5 border border-white/10 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all duration-200 text-white placeholder:text-white/20 text-sm"
                  placeholder="••••••••"
                  required
                />
              </div>
            </div>

            <Button type="submit" variant="primary" size="lg" fullWidth loading={loading} className="mt-2">
              <span className="flex items-center justify-center gap-2">
                Get Started <ArrowRight className="w-4 h-4" />
              </span>
            </Button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-white/50 text-xs">
              Already have an account?{' '}
              <Link href="/login" className="text-indigo-400 hover:text-indigo-300 font-semibold transition-all">
                Sign In
              </Link>
            </p>
          </div>
        </div>

      </div>
    </div>
  );
}

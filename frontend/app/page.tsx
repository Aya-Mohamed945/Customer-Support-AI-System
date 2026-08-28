// frontend/app/page.tsx

'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import TicketForm from './components/TicketForm';
import ResultsDisplay from './components/ResultsDisplay';
import LoadingSkeleton from './components/ui/LoadingSkeleton';
import Toast from './components/ui/Toast';
import { predictTicket, PredictionResponse } from './utils/api';

interface User {
  name: string;
  email: string;
  role: string;
}

export default function Home() {
  const router = useRouter();
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' | 'info' } | null>(null);

  useEffect(() => {
    const checkAuth = () => {
      const token = sessionStorage.getItem('token');
      const userData = sessionStorage.getItem('user');
      
      if (!token) {
        router.push('/login');
        return;
      }

      if (userData) {
        try {
          setUser(JSON.parse(userData));
        } catch {
          sessionStorage.removeItem('token');
          sessionStorage.removeItem('user');
          router.push('/login');
        }
      } else {
        sessionStorage.removeItem('token');
        sessionStorage.removeItem('user');
        router.push('/login');
      }
      
      setLoading(false);
    };

    checkAuth();
  }, [router]);

  const handleLogout = () => {
    sessionStorage.removeItem('token');
    sessionStorage.removeItem('user');
    router.push('/login');
  };

  const handleSubmit = async (data: { title: string; description: string; resolution_time?: number }) => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const userData = sessionStorage.getItem('user');
      const user = userData ? JSON.parse(userData) : null;
      
      const response = await predictTicket({
        ...data,
        user_id: user?.email || 'anonymous',
      });
      setResult(response);
      setToast({ message: '✅ Ticket analyzed successfully!', type: 'success' });
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'An error occurred';
      setError(errorMsg);
      setToast({ message: `❌ ${errorMsg}`, type: 'error' });
    } finally {
      setIsLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="relative w-12 h-12">
            <div className="absolute inset-0 rounded-full border-3 border-white/5" />
            <div className="absolute inset-0 rounded-full border-3 border-t-transparent border-primary-400 animate-spin" />
          </div>
          <p className="text-sm text-white/30">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-8 sm:py-12 px-4">
      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}

      <div className="max-w-3xl mx-auto">
        {/* ============================================
            HEADER - Minimal & Clean
            ============================================ */}
        <header className="text-center mb-10 animate-fade-up">
          {/* Brand */}
          <div className="inline-flex items-center gap-2.5 mb-4">
            <div className="w-9 h-9 rounded-xl gradient-bg flex items-center justify-center shadow-lg">
              <svg 
                className="w-5 h-5 text-white" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <span className="text-lg font-bold text-white/90">Support<span className="gradient-text">AI</span></span>
          </div>

          {/* Title */}
          <h1 className="heading-hero text-white/95">
            Ticket Intelligence
          </h1>
          <p className="mt-2 text-sm text-white/40 max-w-lg mx-auto">
            Paste your support ticket and let AI analyze, categorize, and suggest solutions instantly.
          </p>

          {/* User & Navigation */}
          <div className="mt-5 flex flex-wrap items-center justify-center gap-3">
            {user && (
              <span className="text-xs text-white/30">
                {user.name} <span className="text-white/20">·</span> {user.role}
              </span>
            )}
            
            <div className="flex items-center gap-1.5">
              <Link
                href="/history"
                className="px-3 py-1.5 text-xs font-medium text-white/40 hover:text-white/70 bg-white/5 hover:bg-white/10 rounded-full border border-white/5 hover:border-white/10 transition-all duration-300"
              >
                History
              </Link>
              {user?.role === 'admin' && (
                <Link
                  href="/dashboard"
                  className="px-3 py-1.5 text-xs font-medium text-white/40 hover:text-white/70 bg-white/5 hover:bg-white/10 rounded-full border border-white/5 hover:border-white/10 transition-all duration-300"
                >
                  Dashboard
                </Link>
              )}
              <button
                onClick={handleLogout}
                className="px-3 py-1.5 text-xs font-medium text-white/20 hover:text-white/50 bg-white/5 hover:bg-white/10 rounded-full border border-white/5 hover:border-white/10 transition-all duration-300"
              >
                Logout
              </button>
            </div>
          </div>
        </header>

        {/* ============================================
            MAIN FORM
            ============================================ */}
        <section className="glass rounded-2xl p-6 sm:p-8 animate-fade-up delay-2">
          {isLoading ? (
            <LoadingSkeleton />
          ) : (
            <TicketForm onSubmit={handleSubmit} isLoading={isLoading} />
          )}
        </section>

        {/* ============================================
            ERROR
            ============================================ */}
        {error && !toast && (
          <div className="mt-5 p-4 bg-danger/10 backdrop-blur-sm border border-danger/15 rounded-xl text-danger/80 text-sm animate-fade-up">
            <div className="flex items-start gap-3">
              <svg className="w-4 h-4 text-danger/60 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>{error}</span>
            </div>
          </div>
        )}

        {/* ============================================
            RESULTS
            ============================================ */}
        {result && (
          <div className="mt-8 animate-fade-up delay-3">
            <ResultsDisplay result={result} />
          </div>
        )}

        {/* ============================================
            FOOTER
            ============================================ */}
        <footer className="mt-12 text-center">
          <p className="text-[10px] text-white/10 font-light tracking-widest">
            ⚡ FastAPI · XGBoost · RAG · Next.js
          </p>
        </footer>
      </div>
    </div>
  );
}
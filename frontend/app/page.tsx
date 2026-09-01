// frontend/app/page.tsx
'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import {  BrainCircuit, History, LogOut, LayoutDashboard } from 'lucide-react';
import TicketForm from './components/TicketForm';
import ResultsDisplay from './components/ResultsDisplay';
import Toast from './components/ui/Toast';
import { predictTicket } from './utils/api';
import { PredictionResponse, User, ToastData } from './types';  // ✅ من types

export default function Home() {
  const router = useRouter();
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [user, setUser] = useState<User | null>(null);
  const [pageLoading, setPageLoading] = useState(true);
  const [toast, setToast] = useState<ToastData | null>(null);

  useEffect(() => {
    const token = sessionStorage.getItem('token');
    const userData = sessionStorage.getItem('user');
    if (!token || !userData) {
      router.push('/login');
      return;
    }
    try {
      setUser(JSON.parse(userData));
    } catch {
      router.push('/login');
    } finally {
      setPageLoading(false);
    }
  }, [router]);

  const handleLogout = () => {
    sessionStorage.clear();
    router.push('/login');
  };

  const handleSubmit = async (data: { title: string; description: string; resolution_time?: number }) => {
    setIsLoading(true);
    setResult(null);
    try {
      const response = await predictTicket({
        ...data,
        user_id: user?.email || 'anonymous'
      });
      setResult(response);
      setToast({ message: '✅ Ticket analyzed successfully!', type: 'success' });
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'An error occurred';
      setToast({ message: errorMsg, type: 'error' });
    } finally {
      setIsLoading(false);
    }
  };

  if (pageLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="w-10 h-10 border-4 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen py-10 px-4 sm:py-16 flex items-center justify-center">
      {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}

      <div className="max-w-5xl mx-auto w-full">
        {/* Header Section */}
        <div className="text-center mb-10 animate-fade-in-up">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-3xl bg-gradient-to-br from-blue-500 to-purple-500 shadow-2xl shadow-indigo-500/20 mb-6 relative group">
            <div className="absolute inset-0 rounded-3xl bg-white/10 blur-xl group-hover:blur-2xl transition-all" />
            <BrainCircuit className="w-10 h-10 text-white relative z-10" />
          </div>

          <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight text-white">
            Customer Support <span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">AI</span>
          </h1>
          <p className="mt-3 text-lg text-white/60 font-light max-w-2xl mx-auto leading-relaxed">
            Fast, accurate ticket classification and RAG-powered solution generation for higher efficiency.
          </p>

          {/* User Capsule */}
          <div className="mt-6 inline-flex items-center gap-3.5 px-5 py-2.5 rounded-full bg-white/5 border border-white/10 backdrop-blur-md">
            {user && <span className="text-white/90 text-sm font-semibold">👤 {user.name}</span>}
            <span className="w-px h-4 bg-white/15" />
            <button onClick={handleLogout} className="flex items-center gap-1.5 text-xs text-red-400 hover:text-red-300 font-semibold transition-colors">
              <LogOut className="w-3.5 h-3.5" /> Logout
            </button>
          </div>

          {/* Navigation Links */}
          <div className="mt-4 flex justify-center gap-3">
            <Link href="/history" className="flex items-center gap-1.5 px-4 py-1.5 text-xs font-semibold text-white/80 bg-white/5 hover:bg-white/10 rounded-full border border-white/10 transition-all">
              <History className="w-3.5 h-3.5" /> My History
            </Link>
            {user?.role === 'admin' && (
              <Link href="/dashboard" className="flex items-center gap-1.5 px-4 py-1.5 text-xs font-semibold text-white/80 bg-white/5 hover:bg-white/10 rounded-full border border-white/10 transition-all">
                <LayoutDashboard className="w-3.5 h-3.5" /> Dashboard
              </Link>
            )}
          </div>
        </div>

        {/* Ticket Form Container */}
        <div className="rounded-3xl p-6 sm:p-10 border border-white/10 shadow-2xl shadow-indigo-950/5 backdrop-blur-2xl transition-all duration-300 hover:border-white/15 bg-white/5">
          <TicketForm onSubmit={handleSubmit} isLoading={isLoading} />
        </div>

        {/* Prediction Results Container */}
        {result && (
          <div className="mt-8 animate-slide-in-right">
            <ResultsDisplay result={result} />
          </div>
        )}
      </div>
    </div>
  );
}

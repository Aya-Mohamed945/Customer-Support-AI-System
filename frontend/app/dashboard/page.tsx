// frontend/app/dashboard/page.tsx
'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import MetricsCard from '../components/dashboard/MetricsCard';
import Chart from '../components/dashboard/Chart';
import StatusBadge from '../components/dashboard/StatusBadge';
import RecentActivity from '../components/dashboard/RecentActivity';

interface DashboardData {
  total_predictions: number;
  uptime_hours: number;
  priority_distribution: Record<string, number>;
  sentiment_distribution: Record<string, number>;
  source_distribution: Record<string, number>;
  avg_priority_confidence: number;
  avg_rag_confidence: number;
  errors_count: number;
  last_prediction: any;
}

export default function DashboardPage() {
  const router = useRouter();
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isAdmin, setIsAdmin] = useState(false);
  const [adminKey, setAdminKey] = useState('');
  const [showLogin, setShowLogin] = useState(true);

  useEffect(() => {
    // ✅ التحقق من Admin (sessionStorage)
    const checkAdmin = () => {
      const savedKey = sessionStorage.getItem('admin_key');
      if (savedKey === 'admin123') {
        setIsAdmin(true);
        setShowLogin(false);
        fetchMetrics();
      } else {
        setIsAdmin(false);
        setShowLogin(true);
        setLoading(false);
      }
    };
    checkAdmin();
  }, []);

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    if (adminKey === 'admin123') {
      // ✅ استخدام sessionStorage
      sessionStorage.setItem('admin_key', adminKey);
      setIsAdmin(true);
      setShowLogin(false);
      fetchMetrics();
    } else {
      setError('Invalid admin key');
    }
  };

  const handleLogout = () => {
    sessionStorage.removeItem('admin_key');
    setIsAdmin(false);
    setShowLogin(true);
    setData(null);
  };

  // ✅ Export Function
  const handleExport = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/metrics/export');
      if (!response.ok) throw new Error('Export failed');
      
      const result = await response.json();
      if (result.filename) {
        window.location.href = `http://localhost:8000/api/v1/metrics/download/${result.filename}`;
      } else {
        alert('No data to export');
      }
    } catch (err) {
      alert('Export failed: ' + (err instanceof Error ? err.message : 'Unknown error'));
    }
  };

  const fetchMetrics = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/metrics');
      if (!response.ok) throw new Error('Failed to fetch metrics');
      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  const DashboardHeader = () => (
    <div className="flex items-center justify-between mb-8 flex-wrap gap-4">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">📊 Dashboard</h1>
        <p className="text-gray-500 mt-1">Real-time system monitoring</p>
      </div>
      <div className="flex items-center gap-3 flex-wrap">
        <button
          onClick={handleExport}
          className="px-4 py-2 text-sm font-medium text-white bg-green-600 hover:bg-green-700 rounded-lg transition-colors flex items-center gap-2"
        >
          📥 Export CSV
        </button>
        <StatusBadge status="healthy" />
        <span className="text-sm text-gray-400">
          Updated: {new Date().toLocaleTimeString()}
        </span>
        <button
          onClick={handleLogout}
          className="px-4 py-2 text-sm font-medium text-red-600 hover:text-red-700 bg-red-50 hover:bg-red-100 rounded-lg transition-colors"
        >
          Logout
        </button>
        <Link
          href="/"
          className="px-4 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 bg-gray-100 hover:bg-gray-200 rounded-lg transition-all duration-200"
        >
          ← Back
        </Link>
      </div>
    </div>
  );

  if (showLogin) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4">
        <div className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8">
          <div className="text-center mb-8">
            <div className="text-4xl mb-4">🔐</div>
            <h2 className="text-2xl font-bold text-gray-900">Admin Access</h2>
            <p className="text-gray-500 mt-2">Enter admin key to access dashboard</p>
          </div>
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Admin Key</label>
              <input
                type="password"
                value={adminKey}
                onChange={(e) => setAdminKey(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                placeholder="Enter admin key..."
                required
              />
            </div>
            {error && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
                {error}
              </div>
            )}
            <button
              type="submit"
              className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors"
            >
              Access Dashboard
            </button>
          </form>
          <div className="mt-6 text-center">
            <Link href="/" className="text-sm text-gray-500 hover:text-gray-700">
              ← Back to Home
            </Link>
          </div>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-gray-50 py-12">
        <div className="max-w-7xl mx-auto px-4">
          <DashboardHeader />
          <div className="p-6 bg-red-50 border border-red-200 rounded-xl text-red-700">
            {error || 'No data available'}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-7xl mx-auto">
        <DashboardHeader />

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <MetricsCard
            title="Total Predictions"
            value={data.total_predictions.toLocaleString()}
            icon="📥"
            color="blue"
          />
          <MetricsCard
            title="Uptime"
            value={`${data.uptime_hours.toFixed(1)}h`}
            icon="⏱️"
            color="green"
          />
          <MetricsCard
            title="Avg Confidence"
            value={`${(data.avg_priority_confidence * 100).toFixed(1)}%`}
            icon="🎯"
            color="purple"
          />
          <MetricsCard
            title="Errors"
            value={data.errors_count.toString()}
            icon="❌"
            color="red"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Chart
            title="Priority Distribution"
            data={data.priority_distribution}
            colors={['#EF4444', '#EAB308', '#22C55E']}
          />
          <Chart
            title="Sentiment Distribution"
            data={data.sentiment_distribution}
            colors={['#22C55E', '#6B7280', '#EF4444', '#F97316']}
          />
          <Chart
            title="Source Distribution"
            data={data.source_distribution}
            colors={['#3B82F6', '#8B5CF6']}
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <h3 className="text-sm font-medium text-gray-700 mb-4">📈 Performance Overview</h3>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Priority Confidence</span>
                  <span className="font-medium text-gray-900">{(data.avg_priority_confidence * 100).toFixed(1)}%</span>
                </div>
                <div className="mt-1 w-full bg-gray-200 rounded-full h-2">
                  <div className="h-2 rounded-full bg-blue-500" style={{ width: `${data.avg_priority_confidence * 100}%` }} />
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">RAG Confidence</span>
                  <span className="font-medium text-gray-900">{(data.avg_rag_confidence * 100).toFixed(1)}%</span>
                </div>
                <div className="mt-1 w-full bg-gray-200 rounded-full h-2">
                  <div className="h-2 rounded-full bg-purple-500" style={{ width: `${data.avg_rag_confidence * 100}%` }} />
                </div>
              </div>
            </div>
          </div>

          <RecentActivity lastPrediction={data.last_prediction} />
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <h3 className="text-sm font-medium text-gray-700 mb-4">📚 RAG Performance</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <span className="text-sm text-gray-500">Avg RAG Confidence</span>
              <p className="text-2xl font-bold text-gray-900">
                {(data.avg_rag_confidence * 100).toFixed(1)}%
              </p>
            </div>
            <div>
              <span className="text-sm text-gray-500">RAG Usage</span>
              <p className="text-2xl font-bold text-gray-900">
                {data.source_distribution.FAQ || 0}
              </p>
            </div>
            <div>
              <span className="text-sm text-gray-500">Total Predictions</span>
              <p className="text-2xl font-bold text-gray-900">{data.total_predictions}</p>
            </div>
            <div>
              <span className="text-sm text-gray-500">Errors</span>
              <p className="text-2xl font-bold text-gray-900">{data.errors_count}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
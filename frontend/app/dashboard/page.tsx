// frontend/app/dashboard/page.tsx
'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
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
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchMetrics();
  }, []);

  const fetchMetrics = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/metrics');

      if (!response.ok) {
        throw new Error('Failed to fetch metrics');
      }

      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async () => {
    try {
      const response = await fetch(
        'http://localhost:8000/api/v1/metrics/export'
      );

      if (!response.ok) {
        throw new Error('Export failed');
      }

      const result = await response.json();

      if (result.filename) {
        window.location.href =
          `http://localhost:8000/api/v1/metrics/download/${result.filename}`;
      } else {
        alert('No data to export');
      }
    } catch (err) {
      alert(
        'Export failed: ' +
          (err instanceof Error ? err.message : 'Unknown error')
      );
    }
  };

  const DashboardHeader = () => (
    <div className="flex items-center justify-between mb-8 flex-wrap gap-4">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">
          📊 Dashboard
        </h1>

        <p className="text-gray-500 mt-1">
          Real-time system monitoring
        </p>
      </div>

      <div className="flex items-center gap-3 flex-wrap">
        <button
          onClick={handleExport}
          className="px-4 py-2 text-sm font-medium text-white bg-green-600 hover:bg-green-700 rounded-lg transition-colors flex items-center gap-2"
        >
          📥 Export CSV
        </button>

        <StatusBadge status="healthy" />

        <span className="text-sm text-gray-500">
          Updated: {new Date().toLocaleTimeString()}
        </span>

        <Link
          href="/"
          className="px-4 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 bg-gray-100 hover:bg-gray-200 rounded-lg transition-all duration-200"
        >
          ← Back
        </Link>
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-400"></div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-gray-50 text-gray-900 py-8 px-4">
        <div className="max-w-7xl mx-auto">
          <DashboardHeader />

          <div className="p-6 bg-red-500/10 border border-red-500/20 rounded-xl text-red-500">
            {error || 'No data available'}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 py-8 px-4">
      <div className="max-w-7xl mx-auto">

        <DashboardHeader />

        {/* Metrics Cards */}
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

        {/* Distribution Charts */}
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

        {/* Performance Overview + Recent Activity */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">

          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <h3 className="text-sm font-medium text-gray-700 mb-4">
              📈 Performance Overview
            </h3>

            <div className="space-y-4">

              {/* Priority Confidence */}
              <div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">
                    Priority Confidence
                  </span>

                  <span className="font-medium text-gray-900">
                    {(data.avg_priority_confidence * 100).toFixed(1)}%
                  </span>
                </div>

                <div className="mt-1 w-full bg-gray-100 rounded-full h-2 overflow-hidden">
                  <div
                    className="h-2 rounded-full bg-primary-500 transition-all duration-500"
                    style={{
                      width: `${Math.min(
                        Math.max(data.avg_priority_confidence * 100, 0),
                        100
                      )}%`,
                    }}
                  />
                </div>
              </div>

              {/* RAG Confidence */}
              <div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">
                    RAG Confidence
                  </span>

                  <span className="font-medium text-gray-900">
                    {(data.avg_rag_confidence * 100).toFixed(1)}%
                  </span>
                </div>

                <div className="mt-1 w-full bg-gray-100 rounded-full h-2 overflow-hidden">
                  <div
                    className="h-2 rounded-full bg-accent-500 transition-all duration-500"
                    style={{
                      width: `${Math.min(
                        Math.max(data.avg_rag_confidence * 100, 0),
                        100
                      )}%`,
                    }}
                  />
                </div>
              </div>

            </div>
          </div>

          <RecentActivity lastPrediction={data.last_prediction} />
        </div>

        {/* RAG Performance */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h3 className="text-sm font-medium text-gray-700 mb-4">
            📚 RAG Performance
          </h3>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">

            <div>
              <span className="text-sm text-gray-500">
                Avg RAG Confidence
              </span>

              <p className="text-2xl font-bold text-gray-900">
                {(data.avg_rag_confidence * 100).toFixed(1)}%
              </p>
            </div>

            <div>
              <span className="text-sm text-gray-500">
                RAG Usage
              </span>

              <p className="text-2xl font-bold text-gray-900">
                {data.source_distribution.FAQ || 0}
              </p>
            </div>

            <div>
              <span className="text-sm text-gray-500">
                Total Predictions
              </span>

              <p className="text-2xl font-bold text-gray-900">
                {data.total_predictions}
              </p>
            </div>

            <div>
              <span className="text-sm text-gray-500">
                Errors
              </span>

              <p className="text-2xl font-bold text-gray-900">
                {data.errors_count}
              </p>
            </div>

          </div>
        </div>

      </div>
    </div>
  );
}


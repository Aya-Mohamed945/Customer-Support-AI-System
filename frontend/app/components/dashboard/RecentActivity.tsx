// frontend/app/components/dashboard/RecentActivity.tsx
'use client';

interface RecentActivityProps {
  lastPrediction: any;
}

export default function RecentActivity({ lastPrediction }: RecentActivityProps) {
  if (!lastPrediction) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <h3 className="text-sm font-medium text-gray-700 mb-4">Recent Activity</h3>
        <p className="text-gray-400 text-sm">No recent activity</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
      <h3 className="text-sm font-medium text-gray-700 mb-4">Recent Activity</h3>
      <div className="flex items-center gap-4 p-3 bg-gray-50 rounded-lg">
        <div className="flex-1 min-w-0">
          <p className="text-sm text-gray-600 truncate">
            {lastPrediction.category} • {lastPrediction.priority} • {lastPrediction.sentiment}
          </p>
          <p className="text-xs text-gray-400">
            {new Date(lastPrediction.timestamp).toLocaleString()}
          </p>
        </div>
        <span className="text-xs px-2 py-1 bg-blue-100 text-blue-700 rounded-full">
          {lastPrediction.source}
        </span>
      </div>
    </div>
  );
}
// frontend/app/components/dashboard/StatusBadge.tsx
'use client';

interface StatusBadgeProps {
  status: 'healthy' | 'degraded' | 'down';
}

const statusConfig = {
  healthy: {
    color: 'bg-green-100 text-green-800',
    dot: 'bg-green-500',
    label: 'All Systems Operational',
  },
  degraded: {
    color: 'bg-yellow-100 text-yellow-800',
    dot: 'bg-yellow-500',
    label: 'Degraded Performance',
  },
  down: {
    color: 'bg-red-100 text-red-800',
    dot: 'bg-red-500',
    label: 'System Down',
  },
};

export default function StatusBadge({ status }: StatusBadgeProps) {
  const config = statusConfig[status];

  return (
    <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-sm font-medium ${config.color}`}>
      <span className={`w-2 h-2 rounded-full animate-pulse ${config.dot}`} />
      {config.label}
    </div>
  );
}
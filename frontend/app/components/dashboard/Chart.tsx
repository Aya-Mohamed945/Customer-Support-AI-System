// frontend/app/components/dashboard/Chart.tsx
'use client';

interface ChartProps {
  title: string;
  data: Record<string, number>;
  colors: string[];
}

export default function Chart({ title, data, colors }: ChartProps) {
  const entries = Object.entries(data);
  const total = entries.reduce((sum, [, value]) => sum + value, 0);

  if (total === 0) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <h3 className="text-sm font-medium text-gray-700 mb-4">{title}</h3>
        <p className="text-gray-400 text-sm text-center py-4">No data available</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 hover:shadow-md transition-all duration-200">
      <h3 className="text-sm font-medium text-gray-700 mb-4">{title}</h3>
      <div className="space-y-3">
        {entries.map(([label, value], index) => {
          const percentage = total > 0 ? (value / total) * 100 : 0;
          return (
            <div key={label}>
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-600 capitalize">{label}</span>
                <span className="text-gray-900 font-medium">{value} ({percentage.toFixed(1)}%)</span>
              </div>
              <div className="mt-1 w-full bg-gray-100 rounded-full h-2.5 overflow-hidden">
                <div
                  className="h-2.5 rounded-full transition-all duration-700 ease-out"
                  style={{
                    width: `${percentage}%`,
                    backgroundColor: colors[index % colors.length],
                  }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

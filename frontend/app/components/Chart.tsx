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

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
      <h3 className="text-sm font-medium text-gray-700 mb-4">{title}</h3>
      <div className="space-y-3">
        {entries.map(([label, value], index) => {
          const percentage = total > 0 ? (value / total) * 100 : 0;
          return (
            <div key={label}>
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-600 capitalize">{label}</span>
                <span className="text-gray-900 font-medium">{value}</span>
              </div>
              <div className="mt-1 w-full bg-gray-200 rounded-full h-2">
                <div
                  className="h-2 rounded-full transition-all duration-500"
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

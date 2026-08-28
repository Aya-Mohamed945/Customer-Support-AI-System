// frontend/app/components/LoadingSpinner.tsx
'use client';

export default function LoadingSpinner() {
  return (
    <div className="flex flex-col items-center justify-center py-16">
      <div className="relative">
        <div className="w-20 h-20 rounded-full border-4 border-white/10"></div>
        <div className="absolute top-0 left-0 w-20 h-20 rounded-full border-4 border-t-transparent border-blue-400 animate-spin"></div>
        <div className="absolute top-0 left-0 w-20 h-20 rounded-full border-4 border-r-transparent border-purple-400 animate-spin" style={{ animationDuration: '1.5s', animationDirection: 'reverse' }}></div>
      </div>
      <p className="mt-6 text-white/70 font-medium text-lg">Analyzing your ticket...</p>
      <p className="text-sm text-white/30 mt-1">This may take a few seconds</p>
    </div>
  );
}
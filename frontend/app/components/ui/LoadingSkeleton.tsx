// frontend/app/components/ui/LoadingSkeleton.tsx
'use client';

export default function LoadingSkeleton() {
  return (
    <div className="w-full space-y-4 animate-pulse">
      <div className="h-8 bg-gray-200/50 rounded-lg w-3/4"></div>
      <div className="space-y-4">
        <div className="h-12 bg-gray-200/50 rounded-xl w-full"></div>
        <div className="h-32 bg-gray-200/50 rounded-xl w-full"></div>
        <div className="h-12 bg-gray-200/50 rounded-xl w-full"></div>
      </div>
      <div className="h-14 bg-gray-200/50 rounded-xl w-full"></div>
      <div className="mt-8 space-y-4">
        <div className="h-24 bg-gray-200/50 rounded-xl w-full"></div>
        <div className="h-24 bg-gray-200/50 rounded-xl w-full"></div>
      </div>
    </div>
  );
}
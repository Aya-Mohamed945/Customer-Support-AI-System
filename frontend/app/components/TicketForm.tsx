// frontend/app/components/TicketForm.tsx

'use client';

import { useState } from 'react';

interface TicketFormProps {
  onSubmit: (data: { title: string; description: string; resolution_time?: number }) => void;
  isLoading: boolean;
}

export default function TicketForm({ onSubmit, isLoading }: TicketFormProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [resolutionTime, setResolutionTime] = useState<number | undefined>(undefined);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({ title, description, resolution_time: resolutionTime });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      <div>
        <label htmlFor="ticket-title" className="block text-sm font-semibold text-white/90 mb-1.5">
          Ticket Title <span className="text-rose-400">*</span>
        </label>
        <input
          id="ticket-title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full px-5 py-3.5 rounded-xl glass-input text-white placeholder:text-white/30 outline-none transition-all duration-300"
          placeholder="e.g., Payment failed on checkout"
          required
          disabled={isLoading}
          aria-label="Ticket title"
        />
      </div>

      <div>
        <label htmlFor="ticket-description" className="block text-sm font-semibold text-white/90 mb-1.5">
          Description <span className="text-rose-400">*</span>
        </label>
        <textarea
          id="ticket-description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={5}
          className="w-full px-5 py-3.5 rounded-xl glass-input text-white placeholder:text-white/30 outline-none transition-all duration-300 resize-y min-h-[120px]"
          placeholder="Describe the issue in detail..."
          required
          disabled={isLoading}
          aria-label="Ticket description"
        />
        <div className="mt-1.5 flex justify-between items-center">
          <span className="text-xs text-white/20">
            {description.length} characters
          </span>
          {description.length > 0 && description.length < 10 && (
            <span className="text-xs text-white/30">Please provide more detail</span>
          )}
        </div>
      </div>

      <div>
        <label htmlFor="ticket-resolution" className="block text-sm font-semibold text-white/90 mb-1.5">
          Resolution Time <span className="text-xs font-normal text-white/30">(hours, optional)</span>
        </label>
        <input
          id="ticket-resolution"
          type="number"
          value={resolutionTime || ''}
          onChange={(e) => setResolutionTime(e.target.value ? Number(e.target.value) : undefined)}
          min={0}
          max={168}
          className="w-full px-5 py-3.5 rounded-xl glass-input text-white placeholder:text-white/30 outline-none transition-all duration-300"
          placeholder="e.g., 4"
          disabled={isLoading}
          aria-label="Resolution time in hours"
        />
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className={`w-full py-4 px-6 rounded-xl text-white font-semibold text-base transition-all duration-300 flex items-center justify-center gap-3 ${
          isLoading
            ? 'bg-white/5 cursor-not-allowed text-white/50'
            : 'btn-primary hover:shadow-[0_8px_40px_rgba(79,70,229,0.35)]'
        }`}
        aria-label={isLoading ? 'Analyzing ticket...' : 'Analyze ticket'}
      >
        {isLoading ? (
          <>
            <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" aria-hidden="true">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            Analyzing...
          </>
        ) : (
          <>
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            Analyze Ticket
          </>
        )}
      </button>
    </form>
  );
}

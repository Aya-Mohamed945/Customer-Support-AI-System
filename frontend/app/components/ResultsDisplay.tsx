// frontend/app/components/ResultsDisplay.tsx

'use client';

import { PredictionResponse } from '../utils/api';

interface ResultsDisplayProps {
  result: PredictionResponse | null;
}

export default function ResultsDisplay({ result }: ResultsDisplayProps) {
  if (!result) return null;

  const priorityConfig = {
    High: { color: 'badge-priority-high', icon: '🔴', label: 'High' },
    Medium: { color: 'badge-priority-medium', icon: '🟡', label: 'Medium' },
    Low: { color: 'badge-priority-low', icon: '🟢', label: 'Low' },
  };

  const sentimentConfig = {
    positive: { color: 'badge-sentiment-positive', icon: '😊', label: 'Positive' },
    neutral: { color: 'badge-sentiment-neutral', icon: '😐', label: 'Neutral' },
    negative: { color: 'badge-sentiment-negative', icon: '😞', label: 'Negative' },
    angry: { color: 'badge-sentiment-angry', icon: '😡', label: 'Angry' },
  };

  const getPriority = (p: string) => priorityConfig[p as keyof typeof priorityConfig] || priorityConfig.Medium;
  const getSentiment = (s: string) => sentimentConfig[s as keyof typeof sentimentConfig] || sentimentConfig.neutral;

  const priority = getPriority(result.priority);
  const sentiment = getSentiment(result.sentiment);

  return (
    <div className="glass rounded-2xl overflow-hidden animate-fade-scale">
      {/* Header */}
      <div className="px-6 py-4 border-b border-white/5">
        <div className="flex items-center gap-2.5">
          <svg className="w-4 h-4 text-white/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          <h3 className="text-sm font-semibold text-white/70">Analysis Results</h3>
        </div>
      </div>

      {/* Body */}
      <div className="p-6 space-y-5">
        {/* Metrics Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <div className="p-3.5 bg-white/5 rounded-xl text-center">
            <p className="text-[10px] font-medium text-white/30 uppercase tracking-wider">Category</p>
            <p className="mt-1 text-sm font-semibold text-white/90 capitalize">{result.category}</p>
          </div>

          <div className="p-3.5 bg-white/5 rounded-xl text-center">
            <p className="text-[10px] font-medium text-white/30 uppercase tracking-wider">Priority</p>
            <div className="mt-1 flex items-center justify-center gap-1.5">
              <span className="text-sm">{priority.icon}</span>
              <span className={`badge text-xs ${priority.color}`}>{priority.label}</span>
            </div>
            <p className="mt-1 text-[10px] text-white/20">
              {(result.priority_confidence * 100).toFixed(0)}% confidence
            </p>
          </div>

          <div className="p-3.5 bg-white/5 rounded-xl text-center">
            <p className="text-[10px] font-medium text-white/30 uppercase tracking-wider">Sentiment</p>
            <div className="mt-1 flex items-center justify-center gap-1.5">
              <span className="text-sm">{sentiment.icon}</span>
              <span className={`badge text-xs ${sentiment.color}`}>{sentiment.label}</span>
            </div>
          </div>

          <div className="p-3.5 bg-white/5 rounded-xl text-center">
            <p className="text-[10px] font-medium text-white/30 uppercase tracking-wider">Source</p>
            <p className="mt-1 text-sm font-semibold text-white/90">{result.source}</p>
            {result.rag_confidence > 0 && (
              <p className="mt-1 text-[10px] text-white/20">
                {(result.rag_confidence * 100).toFixed(0)}% confidence
              </p>
            )}
          </div>
        </div>

        {/* Suggested Solution */}
        <div className="p-4 rounded-xl bg-gradient-to-br from-primary-500/10 to-accent-500/10 border border-white/5">
          <div className="flex items-start gap-3">
            <svg className="w-4 h-4 text-primary-400/60 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
            <div>
              <p className="text-[10px] font-semibold text-primary-400/60 uppercase tracking-wider">Suggested Solution</p>
              <p className="mt-1 text-sm text-white/70 leading-relaxed">{result.suggested_solution}</p>
            </div>
          </div>
        </div>

        {/* FAQ Results */}
        {result.rag_results && result.rag_results.length > 0 && (
          <div>
            <div className="flex items-center gap-2 mb-3">
              <svg className="w-3.5 h-3.5 text-white/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <h4 className="text-xs font-medium text-white/40 uppercase tracking-wider">
                Related FAQs
                <span className="ml-1.5 text-[10px] text-white/20">({result.rag_results.length})</span>
              </h4>
            </div>
            <div className="space-y-2.5">
              {result.rag_results.map((faq, index) => (
                <div 
                  key={index} 
                  className="p-3.5 rounded-xl bg-white/5 border border-white/5 hover:bg-white/8 hover:border-white/10 transition-all duration-300"
                >
                  <div className="flex items-start gap-3">
                    <span className="flex-shrink-0 w-5 h-5 rounded-full gradient-bg text-white text-[10px] font-semibold flex items-center justify-center">
                      {index + 1}
                    </span>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-white/80">{faq.question}</p>
                      <p className="text-sm text-white/40 mt-0.5">{faq.answer}</p>
                      <div className="flex items-center gap-3 mt-2">
                        <span className="text-[10px] text-white/20">
                          Similarity: {(faq.similarity * 100).toFixed(0)}%
                        </span>
                        <span className="text-[10px] px-2 py-0.5 bg-white/5 text-white/30 rounded-full">{faq.category}</span>
                        <span className="text-[10px] px-2 py-0.5 bg-white/5 text-white/30 rounded-full">{faq.domain}</span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
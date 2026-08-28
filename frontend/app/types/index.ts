// frontend/app/types/index.ts

export interface TicketFormData {
  title: string;
  description: string;
  resolution_time?: number;
}

export interface PredictionRequest extends TicketFormData {
  user_id?: string;
}

export interface RAGResult {
  question: string;
  answer: string;
  category: string;
  domain: string;
  similarity: number;
}

export interface PredictionResponse {
  category: string;
  priority: string;
  priority_confidence: number;
  sentiment: string;
  suggested_solution: string;
  source: string;
  rag_confidence: number;
  rag_results: RAGResult[] | null;
}

export interface User {
  name: string;
  email: string;
  role: string;
}

export interface ToastData {
  message: string;
  type: 'success' | 'error' | 'info';
}
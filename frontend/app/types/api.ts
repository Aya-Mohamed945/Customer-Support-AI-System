// frontend/app/types/api.ts

// ============================================
// REQUEST TYPES
// ============================================

export interface PredictRequest {
  title: string;
  description: string;
  resolution_time?: number;
}

export interface RAGRequest {
  query: string;
  k?: number;
  threshold?: number;
}

// ============================================
// RESPONSE TYPES
// ============================================

export interface RAGResult {
  question: string;
  answer: string;
  category: string;
  domain: string;
  similarity: number;
}

export interface RAGResponse {
  results: RAGResult[];
}

export interface PredictResponse {
  category: string;
  priority: string;
  priority_confidence: number;
  sentiment: string;
  suggested_solution: string;
  source: string;
  rag_confidence: number;
  rag_results: RAGResult[] | null;
}

export interface HealthResponse {
  status: string;
  service: string;
  version: string;
  models_loaded: boolean;
  sentiment_classes: string[];
}

// ============================================
// ERROR TYPES
// ============================================

export interface APIError {
  message: string;
  status: number;
  detail?: string;
}

// ============================================
// CONFIG TYPES
// ============================================

export interface APIConfig {
  baseURL: string;
  timeout?: number;
  headers?: Record<string, string>;
}
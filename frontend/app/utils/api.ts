// frontend/app/utils/api.ts
import { PredictionRequest, PredictionResponse, User } from '../types';

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export type { PredictionResponse, User };

const getAuthHeaders = () => {
  const token = typeof window !== 'undefined' ? sessionStorage.getItem('token') : null;
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
};

export async function predictTicket(data: PredictionRequest): Promise<PredictionResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/predict`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `API Error: ${response.status}`);
  }

  return response.json();
}

export async function signupUser(data: Record<string, string>) {
  const response = await fetch(`${API_BASE_URL}/api/v1/auth/signup`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });

  const resData = await response.json();
  if (!response.ok) throw new Error(resData.detail || 'Signup failed');
  return resData;
}

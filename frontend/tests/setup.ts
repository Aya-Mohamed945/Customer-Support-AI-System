// frontend/tests/setup.ts
import '@testing-library/jest-dom';

// Mock fetch
global.fetch = jest.fn();

// Mock environment variables
process.env.NEXT_PUBLIC_API_URL = 'http://localhost:8000';
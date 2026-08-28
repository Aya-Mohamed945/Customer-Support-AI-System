// frontend/tests/integration/api.test.ts
import { predictTicket } from '@/app/utils/api';

describe('API Integration', () => {
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  it('predicts ticket successfully', async () => {
    // Mock fetch
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        category: 'billing',
        priority: 'High',
        sentiment: 'negative',
        suggested_solution: 'Test solution',
        source: 'General',
        priority_confidence: 0.8,
        rag_confidence: 0.0,
        rag_results: null,
      }),
    });

    const result = await predictTicket({
      title: 'Test Ticket',
      description: 'Test description',
    });

    expect(result).toHaveProperty('category');
    expect(result).toHaveProperty('priority');
    expect(result).toHaveProperty('sentiment');
    expect(result).toHaveProperty('suggested_solution');
  });

  it('handles API errors', async () => {
    global.fetch = jest.fn().mockRejectedValue(new Error('Network error'));

    await expect(
      predictTicket({
        title: 'Test',
        description: 'Test',
      })
    ).rejects.toThrow();
  });
});
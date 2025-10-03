import { events } from '~/services/BeerService/events';

const mockFetch = vi.fn();
global.fetch = mockFetch;

describe('events service', () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  describe('createEvent', () => {
    it('returns error if required fields are missing', async () => {
      const result = await events.createEvent({ name: '', description: '' });
      expect(result.success).toBe(false);
      expect(result.error).toBe('All fields are required');
    });

    it('returns success if all fields are present and fetch is ok', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ id: 1, name: 'Test Event' })
      });
      const result = await events.createEvent({ name: 'Test', description: 'Desc' });
      expect(result.success).toBe(true);
      expect(result.response).toEqual({ id: 1, name: 'Test Event' });
    });

    it('returns error if fetch fails', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        json: async () => ({ error: 'Failed' })
      });
      const result = await events.createEvent({ name: 'Test', description: 'Desc' });
      expect(result.success).toBe(false);
      expect(result.error).toBe('Failed');
    });
  });

  // getEvents and getEventById use useFetch composable, which is not easily unit testable
});

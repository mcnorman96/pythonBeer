import { eventBeer } from '~/services/BeerService/eventBeer';

const mockFetch = vi.fn();
global.fetch = mockFetch;

describe('eventBeer service', () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  describe('newBeer', () => {
    it('returns error if required fields are missing', async () => {
      const beer = { name: '', brewery: '', description: '', type: '' };
      const result = await eventBeer.newBeer(beer as any);
      expect(result.success).toBe(false);
      expect(result.error).toBe('All fields are required');
    });

    it('returns success if all fields are present and fetch is ok', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ response: { id: 1, name: 'Test Beer' } }),
      });
      const beer = { name: 'Test', brewery: 'Brew', description: 'Desc', type: 'IPA' };
      const result = await eventBeer.newBeer(beer as any);
      expect(result.success).toBe(true);
      expect(result.response).toEqual({ id: 1, name: 'Test Beer' });
    });

    it('returns error if fetch fails', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        json: async () => ({ error: 'Failed' }),
      });
      const beer = { name: 'Test', brewery: 'Brew', description: 'Desc', type: 'IPA' };
      const result = await eventBeer.newBeer(beer as any);
      expect(result.success).toBe(false);
      expect(result.error).toBe('Failed');
    });
  });

  describe('addBeerToEvent', () => {
    it('returns error if eventId or beerId is missing', async () => {
      const result = await eventBeer.addBeerToEvent('', '');
      expect(result.success).toBe(false);
      expect(result.error).toBe('Event ID and Beer ID are required');
    });

    it('returns success if fetch is ok', async () => {
      mockFetch.mockResolvedValueOnce({ ok: true });
      const result = await eventBeer.addBeerToEvent('1', '2');
      expect(result.success).toBe(true);
    });

    it('returns error if fetch fails', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        json: async () => ({ error: 'Failed' }),
      });
      const result = await eventBeer.addBeerToEvent('1', '2');
      expect(result.success).toBe(false);
      expect(result.error).toBe('Failed');
    });
  });

  describe('toplistBeersInEvent', () => {
    it('returns success and response if fetch is ok', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ response: [{ id: 1, name: 'Beer' }] }),
      });
      const result = await eventBeer.toplistBeersInEvent('1');
      expect(result.success).toBe(true);
      expect(result.response).toEqual([{ id: 1, name: 'Beer' }]);
    });

    it('returns error if fetch fails', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        json: async () => ({ error: 'Failed' }),
      });
      const result = await eventBeer.toplistBeersInEvent('1');
      expect(result.success).toBe(false);
      expect(result.error).toBe('Failed');
    });
  });
});

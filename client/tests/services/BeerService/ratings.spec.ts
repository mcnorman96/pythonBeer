import { ratings } from '~/services/BeerService/ratings';

const mockFetch = vi.fn();
global.fetch = mockFetch;
global.localStorage = {
  getItem: vi.fn(() => 'test-token'),
};

describe('ratings service', () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  describe('addRating', () => {
    it('returns error if required fields are missing', async () => {
      const result = await ratings.addRating({
        event_id: '',
        beer_id: '',
        taste: null,
        aftertaste: null,
        smell: null,
        design: null,
        score: null,
      });
      expect(result.success).toBe(false);
      expect(result.error).toBe('All fields are required');
    });

    it('returns success if all fields are present and fetch is ok', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: 'Rating added successfully' }),
      });
      const result = await ratings.addRating({
        event_id: '1',
        beer_id: '2',
        taste: 1,
        aftertaste: 2,
        smell: 3,
        design: 4,
        score: 5,
      });
      expect(result.success).toBe(true);
      expect(result.message).toBe('Rating added successfully');
    });

    it('returns error if fetch fails', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        json: async () => ({ error: 'Failed' }),
      });
      const result = await ratings.addRating({
        event_id: '1',
        beer_id: '2',
        taste: 1,
        aftertaste: 2,
        smell: 3,
        design: 4,
        score: 5,
      });
      expect(result.success).toBe(false);
      expect(result.error).toBe('Failed');
    });
  });

  describe('getRating', () => {
    it('returns error if eventId or beerId is missing', async () => {
      const result = await ratings.getRating('', '');
      expect(result.success).toBe(false);
      expect(result.error).toBe('Event ID and Beer ID are required');
    });

    it('returns success and response if fetch is ok', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ id: 1, score: 5 }),
      });
      const result = await ratings.getRating('1', '2');
      expect(result.success).toBe(true);
      expect(result.response).toEqual({ id: 1, score: 5 });
    });

    it('returns error if fetch fails', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        json: async () => ({ error: 'Failed' }),
      });
      const result = await ratings.getRating('1', '2');
      expect(result.success).toBe(false);
      expect(result.error).toBe('Failed');
    });
  });

  // getAllRatingsForBeer uses useFetch composable, which is not easily unit testable
});

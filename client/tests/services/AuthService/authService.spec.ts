import { authService } from '~/services/AuthService/authService';

const mockFetch = vi.fn();
global.fetch = mockFetch;

describe('authService', () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  describe('registerUser', () => {
    it('throws error if required fields are missing', async () => {
      await expect(
        authService.registerUser({ username: '', password: '', email: '' })
      ).rejects.toThrow('All fields are required');
    });

    it('calls fetch with correct params and returns response', async () => {
      const mockResponse = { ok: true };
      mockFetch.mockResolvedValueOnce(mockResponse);
      const userData = { username: 'user', password: 'pass', email: 'test@test.com' };
      const response = await authService.registerUser(userData);
      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining('/auth/register'),
        expect.objectContaining({ method: 'POST' })
      );
      expect(response).toBe(mockResponse);
    });
  });

  describe('login', () => {
    it('throws error if required fields are missing', async () => {
      await expect(authService.login({ username: '', password: '' })).rejects.toThrow(
        'All fields are required'
      );
    });

    it('calls fetch with correct params and returns response', async () => {
      const mockResponse = { ok: true };
      mockFetch.mockResolvedValueOnce(mockResponse);
      const credentials = { username: 'user', password: 'pass' };
      const response = await authService.login(credentials);
      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining('/auth/login'),
        expect.objectContaining({ method: 'POST' })
      );
      expect(response).toBe(mockResponse);
    });
  });

  describe('logout', () => {
    it('calls fetch with correct params and returns response', async () => {
      const mockResponse = { ok: true };
      mockFetch.mockResolvedValueOnce(mockResponse);
      const response = await authService.logout();
      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining('/auth/logout'),
        expect.objectContaining({ method: 'POST' })
      );
      expect(response).toBe(mockResponse);
    });
  });
});

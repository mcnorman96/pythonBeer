import { API_URL } from '../vars';

export const authService = {
  registerUser: async (userData: { username: string; password: string; email: string }) => {
    if (!userData.username || !userData.password || !userData.email) {
      throw new Error('All fields are required');
    }

    const response = await fetch(`${API_URL}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });
    
    return response;
  },

  login: async (credentials: { username: string; password: string }) => {
    if (!credentials.username || !credentials.password) {
      throw new Error('All fields are required');
    }

    const response = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });
    return response;
  },

  logout: async () => {
    const response = await fetch(`${API_URL}/auth/logout`, {
      method: 'POST',
    });
    return response;
  },
};
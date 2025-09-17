import { API_URL } from '../vars';

export const authService = {
  registerUser: async (userData: { username: string; password: string; email: string }) => {
    const form = new FormData();
    form.append('username', userData.username);
    form.append('password', userData.password);
    form.append('email', userData.email);
    
    const response = await fetch(`${API_URL}/auth/register`, {
      method: 'POST',
      body: form
    });
    
    return response;
  },

  login: async (credentials: { username: string; password: string }) => {
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
import { API_URL } from '../vars';

export interface RegisterUserData {
  username: string;
  password: string;
  email: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface AuthService {
  registerUser: (userData: RegisterUserData) => Promise<Response>;
  login: (credentials: LoginCredentials) => Promise<Response>;
  logout: () => Promise<Response>;
}

export const authService: AuthService = {
  async registerUser(userData: RegisterUserData): Promise<Response> {
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

  async login(credentials: LoginCredentials): Promise<Response> {
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

  async logout(): Promise<Response> {
    const response = await fetch(`${API_URL}/auth/logout`, {
      method: 'POST',
    });
    return response;
  },
};
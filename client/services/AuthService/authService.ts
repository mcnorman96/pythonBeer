import { API_URL } from '../vars';
import type { FetchResult, LoginCredentials, RegisterUserData } from '~/types/types';
import { fetchHelper } from '../fetchHelper';
export interface AuthService {
  registerUser: (userData: RegisterUserData) => Promise<FetchResult<string>>;
  login: (credentials: LoginCredentials) => Promise<FetchResult<string>>;
  logout: () => Promise<FetchResult<string>>;
  getUser: () => Promise<FetchResult<RegisterUserData>>;
  updateUser: (userData: RegisterUserData) => Promise<FetchResult<RegisterUserData>>;
}

export const authService: AuthService = {
  async registerUser(userData: RegisterUserData): Promise<FetchResult<string>> {
    if (!userData.username || !userData.password || !userData.email) {
      throw new Error('All fields are required');
    }

    const response = await fetchHelper({
      path: `${API_URL}/auth/register`,
      method: 'POST',
      body: userData,
      checkToken: false,
    });

    return response;
  },

  async login(credentials: LoginCredentials): Promise<FetchResult<string>> {
    if (!credentials.username || !credentials.password) {
      throw new Error('All fields are required');
    }

    const response = await fetchHelper({
      path: `${API_URL}/auth/login`,
      method: 'POST',
      body: credentials,
      checkToken: false,
    });
    return response;
  },

  async logout(): Promise<FetchResult<string>> {
    const response = await fetchHelper({
      path: `${API_URL}/auth/logout`,
      method: 'POST',
      body: null,
      checkToken: false,
    });
    return response;
  },

  async getUser(): Promise<FetchResult<RegisterUserData>> {
    const response = await fetchHelper({
      path: `${API_URL}/auth/user`,
    });
    return response;
  },

  async updateUser(userData: RegisterUserData): Promise<FetchResult<RegisterUserData>> {
    const response = await fetchHelper({
      path: `${API_URL}/auth/user`,
      method: 'PUT',
      body: userData,
    });
    return response;
  },
};

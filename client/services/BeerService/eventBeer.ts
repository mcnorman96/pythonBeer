import type { Beer, FetchResult, UseFetchResult } from '~/types/types';
import { API_URL } from '../vars';
import { checkTokenExpired } from '@/utils/authUtil';

export interface EventBeerService {
  newBeer: (beer: Beer) => Promise<FetchResult<Beer>>;
  addBeerToEvent: (eventId: string, beerId: string) => Promise<FetchResult<Beer>>;
  searchBeer: (query: string) => Promise<UseFetchResult<Beer>>;
  toplistBeersInEvent: (eventId: string) => Promise<FetchResult<Beer[]>>;
  toplist: () => Promise<UseFetchResult<Beer[]>>;
  updateBeer: (beer: Beer) => Promise<FetchResult<null>>;
  deleteBeerFromEvent: (beer_id: string, event_id: string) => Promise<FetchResult<null>>;
}

export const eventBeer: EventBeerService = {
  async newBeer(beer: Beer): Promise<FetchResult<Beer>> {
    if (!beer.brewery || !beer.description || !beer.name || !beer.type) {
      return {
        success: false,
        error: 'All fields are required',
      };
    }
    const res = await fetch(`${API_URL}/beer/new`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
      body: JSON.stringify(beer),
    });

    const data = await res.json();

    checkTokenExpired(res.status, data.error);

    if (!res.ok) {
      return { success: false, error: data.error };
    }

    return { success: true, response: data.response };
  },

  async addBeerToEvent(eventId: string, beerId: string): Promise<FetchResult<Beer>> {
    if (!eventId || !beerId) {
      return { success: false, error: 'Event ID and Beer ID are required' };
    }
    const res = await fetch(`${API_URL}/events/${eventId}/beers`, {
      method: 'POST',
      body: JSON.stringify({ beer_id: beerId }),
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
    });

    const data = await res.json();

    checkTokenExpired(res.status, data.error);

    if (!res.ok) {
      return { success: false, error: data.error };
    }
    return { success: true };
  },

  async searchBeer(query: string): Promise<UseFetchResult<Beer>> {
    const {
      data: fetchedBeers,
      error: fetchError,
      pending: fetchPending,
    }: UseFetchResult<Beer> = await useFetch(`${API_URL}/beer/search`, {
      params: { s: query },
    });
    return {
      data: fetchedBeers,
      error: fetchError,
      pending: fetchPending,
    };
  },

  async toplistBeersInEvent(eventId: string): Promise<FetchResult<Beer[]>> {
    const response = await fetch(`${API_URL}/ratings/toplist/${eventId}`);

    if (response.status === 204) {
      return { success: true, response: [] };
    }

    const data = await response.json();

    checkTokenExpired(response.status, data.error);

    if (!response.ok) {
      return { success: false, error: data.error };
    }

    return { success: true, response: data.response };
  },

  async toplist(): Promise<UseFetchResult<Beer[]>> {
    const {
      data: fetchedBeers,
      error: fetchError,
      pending: fetchPending,
    }: UseFetchResult<Beer[]> = await useFetch(`${API_URL}/ratings/toplist`);
    return {
      data: fetchedBeers,
      error: fetchError,
      pending: fetchPending,
    };
  },

  async updateBeer(beer: Beer): Promise<FetchResult<null>> {
    const response = await await fetch(`${API_URL}/beer/update`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
      body: JSON.stringify(beer),
    });

    const data = await response.json();

    checkTokenExpired(response.status, data.error);

    if (!response.ok) {
      return { success: false, error: data.error };
    }

    return { success: true };
  },

  async deleteBeerFromEvent(beer_id: string, event_id: string): Promise<FetchResult<null>> {
    const response = await await fetch(`${API_URL}/events/${event_id}/beers/${beer_id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
    });

    const data = await response.json();

    checkTokenExpired(response.status, data.error);

    if (!response.ok) {
      return { success: false, error: data.error };
    }

    return { success: true };
  },
};

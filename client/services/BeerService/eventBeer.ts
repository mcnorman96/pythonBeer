import type { Beer, FetchResult, UseFetchResult } from '~/types/types';
import { API_URL } from '../vars';
import { fetchHelper } from '../fetchHelper';

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

    const response = await fetchHelper({
      path: `${API_URL}/beer/new`,
      method: 'POST',
      body: beer,
    });
    return response;
  },

  async addBeerToEvent(eventId: string, beerId: string): Promise<FetchResult<Beer>> {
    if (!eventId || !beerId) {
      return { success: false, error: 'Event ID and Beer ID are required' };
    }
    const response = await fetchHelper({
      path: `${API_URL}/events/${eventId}/beers`,
      method: 'POST',
      body: { beer_id: beerId },
    });
    return response;
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
    const response = await fetchHelper({
      path: `${API_URL}/ratings/toplist/${eventId}`,
    });
    return response;
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
    const response = await fetchHelper({
      path: `${API_URL}/beer/update`,
      method: 'PUT',
      body: beer,
    });
    return response;
  },

  async deleteBeerFromEvent(beer_id: string, event_id: string): Promise<FetchResult<null>> {
    const response = await fetchHelper({
      path: `${API_URL}/events/${event_id}/beers/${beer_id}`,
      method: 'DELETE',
    });
    return response;
  },
};

import type { Beer, ResponseTypeBeers, Response } from "~/types/types";
import { API_URL } from "../vars";

export interface EventBeerService {
  newBeer: (beer: Beer) => Promise<Response>;
  addBeerToEvent: (eventId: string, beerId: string) => Promise<Response>;
  searchBeer: (query: string) => Promise<{ data: any; error: any; pending: any }>;
  toplistBeersInEvent: (eventId: string) => Promise<Response>;
  toplist: () => Promise<{ data: any; error: any; pending: any }>;
}

export const eventBeer: EventBeerService = {
  async newBeer(beer: Beer): Promise<Response> {
    if (!beer.brewery || !beer.description || !beer.name || !beer.type) {
      return {
        success: false, error: 'All fields are required'
      };
    }
    const res = await fetch(`${API_URL}/beer/new`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(beer)
    });

    const data = await res.json();
    
    if (!res.ok) {
      return { success: false, error: data.error };
    }

    return { success: true, response: data };
  },

  async addBeerToEvent(eventId: string, beerId: string): Promise<Response> {
    if (!eventId || !beerId) {
      return { success: false, error: 'Event ID and Beer ID are required' };
    }
    const res = await fetch(`${API_URL}/events/${eventId}/beers`, {
      method: 'POST',
      body: JSON.stringify({ beer_id: beerId }),
      headers: {
        'Content-Type': 'application/json',
      },
    });
    if (!res.ok) {
      const data = await res.json();
      return { success: false, error: data.error };
    }
    return { success: true };
  },

  async searchBeer(query: string): Promise<{ data: any; error: any; pending: any }> {
    const { data: fetchedBeers, error: fetchError, pending: fetchPending } = await useFetch<ResponseTypeBeers>(`${API_URL}/beer/search`, {
      params: { s: query }
    });
    return {
      data: fetchedBeers,
      error: fetchError,
      pending: fetchPending
    };
  },

  async toplistBeersInEvent(eventId: string): Promise<Response> {
    const response = await fetch(`${API_URL}/ratings/toplist/${eventId}`);

    if (response.status === 204) {
      return { success: true, response: [] };
    }
    
    const data = await response.json();

    if (!response.ok) {
      return { success: false, error: data.error };
    }

    return { success: true, response: data.response };
  },

  async toplist(): Promise<{ data: any; error: any; pending: any }> {
    const { data: fetchedBeers, error: fetchError, pending: fetchPending } = await useFetch<ResponseTypeBeers>(`${API_URL}/ratings/toplist`);
    return {
      data: fetchedBeers,
      error: fetchError,
      pending: fetchPending
    };
  },
};
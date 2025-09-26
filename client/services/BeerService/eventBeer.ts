import type { Beer, ResponseTypeBeers } from "~/types/types";
import { API_URL } from "../vars";

export const eventBeer = {
  newBeer: async (beer: Beer) => {
    if (!beer.brewery || !beer.description || !beer.name || !beer.type) {
      return { success: false, error: 'All fields are required' };
    }
    
    const res = await fetch(`${API_URL}/beer/new`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(beer)
    });

    if (!res.ok) {
      const error = await res.text();
      return { success: false, error };
    }

    const data = await res.json();

    return { success: true, response: data };
  },

  addBeerToEvent: async (eventId: string, beerId: string) => {
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
      const error = await res.text();
      return { success: false, error };
    }
    return { success: true };
  },

  searchBeer: async (query: string) => {
    const { data: fetchedBeers, error: fetchError, pending: fetchPending } = await useFetch<ResponseTypeBeers>(`${API_URL}/beer/search`, {
      params: { s: query }
    });
    
    return {
      data: fetchedBeers,
      error: fetchError,
      pending: fetchPending
    };
  },

  toplistBeersInEvent: async (eventId: string) => {
    const response = await fetch(`${API_URL}/ratings/toplist/${eventId}`);
    if (!response.ok) {
      const error = await response.text();
      return { success: false, error };
    }
    const data = await response.json();
    return { success: true, response: data.response };
  },

  toplist: async () => {
    const { data: fetchedBeers, error: fetchError, pending: fetchPending } = await useFetch<ResponseTypeBeers>(`${API_URL}/ratings/toplist`);

    return {
      data: fetchedBeers,
      error: fetchError,
      pending: fetchPending
    };
  },
};
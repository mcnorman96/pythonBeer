import type { ResponseTypeBeers } from "~/types/types";
import { API_URL } from "../vars";

type beerData = {
  name: string,
  description: string,
  brewery: string,
  type: string
}

export const eventBeer = {
  newBeer: async (beer: beerData) => {
    const formData = new FormData();
    formData.append('name', beer.name);
    formData.append('description', beer.description);
    formData.append('brewery', beer.brewery);
    formData.append('type', beer.type);

    const { data, error } = await useFetch(`${API_URL}/beer/new`, {
      method: 'POST',
      body: formData
    });
    
    if (error.value) {
      return { success: false, error: error.value };
    }
    
    return { success: true, data: data.value };
  },

  addBeerToEvent: async (eventId: string, beerId: string) => {
    const formData = new FormData();
    formData.append('beer_id', beerId);

    const { error } = await useFetch(`${API_URL}/events/${eventId}/beers`, {
      method: 'POST',
      body: formData
    });

    if (error.value) {
      return { success: false, error: error.value };
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
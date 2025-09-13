import type { ResponseTypeBeers } from "~/types/types";
import { API_URL } from "../vars";

export const eventBeer = {
  allBeersInEvent: async (eventId: string) => {
    const { data: fetchedBeers, error: fetchError, pending: fetchPending } = await useFetch<ResponseTypeBeers>(`${API_URL}/events/${eventId}/beers`);

    return {
      data: fetchedBeers,
      error: fetchError,
      pending: fetchPending
    };
  },
  addBeerToEvent: async (eventId: string, beerData: { name: string; type: string }) => {
    // Placeholder for adding a beer to a specific event
    return { success: true };
  },
};
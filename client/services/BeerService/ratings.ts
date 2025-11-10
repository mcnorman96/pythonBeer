import type { FetchResult, Rating, UseFetchResult } from '@/types/types';
import { API_URL } from '../vars';
import { fetchHelper } from '../fetchHelper';
export interface RatingsService {
  addRating: (ratingData: {
    event_id: string;
    beer_id: string;
    taste: number;
    aftertaste: number;
    smell: number;
    design: number;
    score: number;
  }) => Promise<FetchResult<string>>;
  getRating: (eventId: string, beerId: string) => Promise<FetchResult<Rating>>;
  getAllRatingsForBeer: (
    eventId: string,
    beerId: string
  ) => Promise<UseFetchResult<Rating> | { success: boolean; error?: string }>;
}

export const ratings: RatingsService = {
  async addRating(ratingData: {
    event_id: string;
    beer_id: string;
    taste: number;
    aftertaste: number;
    smell: number;
    design: number;
    score: number;
  }): Promise<{ success: boolean; error?: string; message?: string }> {
    if (
      !ratingData.event_id ||
      !ratingData.beer_id ||
      ratingData.taste == null ||
      ratingData.aftertaste == null ||
      ratingData.smell == null ||
      ratingData.design == null ||
      ratingData.score == null
    ) {
      return { success: false, error: 'All fields are required' };
    }

    const response = await fetchHelper({
      path: `${API_URL}/ratings/new`,
      method: 'POST',
      body: ratingData,
    });
    return response;
  },

  async getRating(eventId: string, beerId: string): Promise<FetchResult<Rating>> {
    if (!eventId || !beerId) {
      return { success: false, error: 'Event ID and Beer ID are required' };
    }

    const response = await fetchHelper({
      path: `${API_URL}/ratings/getRating?event_id=${eventId}&beer_id=${beerId}`,
    });

    return response;
  },

  async getAllRatingsForBeer(
    eventId: string,
    beerId: string
  ): Promise<UseFetchResult<Rating> | { success: boolean; error?: string }> {
    if (!eventId || !beerId) {
      return { success: false, error: 'Event ID and Beer ID are required' };
    }
    const { data, error, pending }: UseFetchResult<Rating> = await useFetch(
      `${API_URL}/ratings/all?event_id=${eventId}&beer_id=${beerId}`,
      {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      }
    );
    return { data, error, pending };
  },
};

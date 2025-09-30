import { API_URL } from "../vars";

export interface RatingsService {
  addRating: (ratingData: {
    event_id: string;
    beer_id: string;
    taste: number;
    aftertaste: number;
    smell: number;
    design: number;
    score: number;
  }) => Promise<{ success: boolean; error?: string; message?: string }>;
  getRating: (eventId: string, beerId: string) => Promise<{ success: boolean; error?: string; response?: any }>;
  getAllRatingsForBeer: (eventId: string, beerId: string) => Promise<{ data: any; error: any; pending: any } | { success: boolean; error?: string }>;
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
    if (!ratingData.event_id || !ratingData.beer_id || ratingData.taste == null || ratingData.aftertaste == null || ratingData.smell == null || ratingData.design == null || ratingData.score == null) {
      return { success: false, error: 'All fields are required' };
    }
    const res = await fetch(`${API_URL}/ratings/new`, {
      method: 'POST',
      body: JSON.stringify(ratingData),
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        'content-type': 'application/json'
      }
    });
    if (!res.ok) {
      const error = await res.text();
      return { success: false, error };
    }
    return { success: true, 'message': 'Rating added successfully' };
  },

  async getRating(eventId: string, beerId: string): Promise<{ success: boolean; error?: string; response?: any }> {
    if (!eventId || !beerId) {
      return { success: false, error: 'Event ID and Beer ID are required' };
    }
    const res = await fetch(`${API_URL}/ratings/getRating?event_id=${eventId}&beer_id=${beerId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        'content-type': 'application/json'
      }
    });
    if (!res.ok) {
      const error = await res.text();
      return { success: false, error };
    }
    const data = await res.json();
    return { success: true, response: data };
  },

  async getAllRatingsForBeer(eventId: string, beerId: string): Promise<{ data: any; error: any; pending: any } | { success: boolean; error?: string }> {
    if (!eventId || !beerId) {
      return { success: false, error: 'Event ID and Beer ID are required' };
    }
    const { data, error, pending } = await useFetch(`${API_URL}/ratings/all?event_id=${eventId}&beer_id=${beerId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });
    return { data, error, pending };
  }
};
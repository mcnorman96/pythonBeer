import { API_URL } from "../vars";

export const ratings = {
  addRating: async (ratingData: {
    event_id: string;
    beer_id: string;
    taste: number;
    aftertaste: number;
    smell: number;
    design: number;
    score: number;
  }) => {
    const { data, error, pending } = await useFetch(`${API_URL}/ratings/new`, {
      method: 'POST',
      body: ratingData,
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });
    return { data, error, pending };
  }
};
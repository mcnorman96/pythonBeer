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
    const formdata = new FormData();
    Object.entries(ratingData).forEach(([key, value]) => {
      formdata.append(key, value.toString());
    });
    const { data, error, pending } = await useFetch(`${API_URL}/ratings/new`, {
      method: 'POST',
      body: formdata,
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });
    return { data, error, pending };
  },

  getRating: async (eventId: string, beerId: string) => {
    const { data, error, pending } = await useFetch(`${API_URL}/ratings/getRating?event_id=${eventId}&beer_id=${beerId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });
    return { data, error, pending };
  },

  getAllRatingsForBeer: async (eventId: string, beerId: string) => {
    const { data, error, pending } = await useFetch(`${API_URL}/ratings/all?event_id=${eventId}&beer_id=${beerId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });
    return { data, error, pending };
  }
};
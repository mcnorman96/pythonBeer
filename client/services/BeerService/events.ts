import { API_URL } from "../vars";

export const events = {
  createEvent: async (eventData: { name: string; description: string }) => {
    if (!eventData.name || !eventData.description) {
      return { success: false, error: 'All fields are required' };
    }

    const res = await fetch(`${API_URL}/events/new`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(eventData),
    });

    if (!res.ok) {
      const error = await res.text();
      return { success: false, error };
    }

    return { success: true, response: await res.json() };
  },

  getEvents: async () => {
    const { data, error, pending } = await useFetch(`${API_URL}/events`);
    return { data, error, pending };
  },
  
  getEventById: async (eventId: string) => {
    const { data, error, pending } = await useFetch(`${API_URL}/events/${eventId}`);
    return { data, error, pending };
  }
};
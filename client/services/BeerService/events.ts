import { API_URL } from "../vars";

export const events = {
  createEvent: async (eventData: { name: string; description: string }) => {
    const formData = new FormData();
    formData.append('name', eventData.name);
    formData.append('description', eventData.description);

    const response = await fetch(`${API_URL}/events/new`, {
      method: 'POST',
      body: formData,
    });
    return response.json();
  },
  getEvents: async () => {
    const { data, error, pending } = await useFetch(`${API_URL}/events`);
    return { data, error, pending };
  },
};
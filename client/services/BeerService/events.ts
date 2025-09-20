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

  // getEventById: async (id: string) => {
  //   const response = await fetch(`${API_URL}/events/${id}`);
  //   return response.json();
  // },

  // updateEvent: async (id: string, eventData: { name?: string; date?: string; location?: string }) => {
  //   const response = await fetch(`${API_URL}/events/${id}`, {
  //     method: 'PUT',
  //     headers: {
  //       'Content-Type': 'application/json',
  //     },
  //     body: JSON.stringify(eventData),
  //   });
  //   return response.json();
  // },

  // deleteEvent: async (id: string) => {
  //   const response = await fetch(`${API_URL}/events/${id}`, {
  //     method: 'DELETE',
  //   });
  //   return response.json();
  // },
};
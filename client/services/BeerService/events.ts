import { API_URL } from "../vars";

export interface EventsService {
  createEvent: (eventData: { name: string; description: string }) => Promise<{ success: boolean; error?: string; response?: any }>;
  getEvents: () => Promise<{ data: any; error: any; pending: any }>;
  getEventById: (eventId: string) => Promise<{ data: any; error: any; pending: any }>;
}

export const events: EventsService = {
  async createEvent(eventData: { name: string; description: string }): Promise<{ success: boolean; error?: string; response?: any }> {
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
    
    const data = await res.json();

    if (!res.ok) {
      return { success: false, error: data.error };
    }

    return { success: true, response: data };
  },

  async getEvents(): Promise<{ data: any; error: any; pending: any }> {
    const { data, error, pending } = await useFetch(`${API_URL}/events`);
    return { data, error, pending };
  },

  async getEventById(eventId: string): Promise<{ data: any; error: any; pending: any }> {
    const { data, error, pending } = await useFetch(`${API_URL}/events/${eventId}`);
    return { data, error, pending };
  }
};
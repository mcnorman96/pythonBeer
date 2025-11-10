import type { UseFetchResult } from '@/types/types';
import { API_URL } from '../vars';
import { fetchHelper } from '../fetchHelper';
export interface EventsService {
  createEvent: (eventData: {
    name: string;
    description: string;
  }) => Promise<{ success: boolean; error?: string; response?: Event }>;
  getEvents: () => Promise<{ success: boolean; error?: string; response?: Event[] }>;
  getEventById: (eventId: string) => Promise<UseFetchResult<Event>>;
  updateEvent: (
    eventId: string,
    eventData: { name: string; description: string }
  ) => Promise<{ success: boolean; error?: string | null; response?: Event }>;
  deleteEvent: (
    eventId: string
  ) => Promise<{ success: boolean; error?: string | null; response?: string }>;
}

export const events: EventsService = {
  async createEvent(eventData: {
    name: string;
    description: string;
  }): Promise<{ success: boolean; error?: string; response?: Event }> {
    if (!eventData.name || !eventData.description) {
      return { success: false, error: 'All fields are required' };
    }

    const response = await fetchHelper({
      path: `${API_URL}/events/new`,
      method: 'POST',
      body: eventData,
    });
    return response;
  },

  async getEvents(): Promise<{ success: boolean; error?: string; response?: Event[] }> {
    const response = await fetchHelper({
      path: `${API_URL}/events/`,
    });
    return response;
  },

  async getEventById(eventId: string): Promise<UseFetchResult<Event>> {
    const { data, error, pending }: UseFetchResult<Event> = await useFetch(
      `${API_URL}/events/${eventId}`
    );

    return { data, error, pending };
  },

  async updateEvent(
    eventId: string,
    eventData: { name: string; description: string }
  ): Promise<{ success: boolean; error?: string; response?: Event }> {
    if (!eventData.name || !eventData.description) {
      return { success: false, error: 'All fields are required' };
    }

    const response = await fetchHelper({
      path: `${API_URL}/events/${eventId}`,
      method: 'PUT',
      body: eventData,
    });
    return response;
  },

  async deleteEvent(
    eventId: string
  ): Promise<{ success: boolean; error?: string; response?: string }> {
    const response = await fetchHelper({
      path: `${API_URL}/events/${eventId}`,
      method: 'DELETE',
    });
    return response;
  },
};

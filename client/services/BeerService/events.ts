import type { UseFetchResult } from '@/types/types';
import { API_URL } from '../vars';
import { checkTokenExpired } from '@/utils/authUtil';
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

    const res = await fetch(`${API_URL}/events/new`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
      body: JSON.stringify(eventData),
    });

    const data = await res.json();

    checkTokenExpired(res.status, data.error);

    if (!res.ok) {
      return { success: false, error: data.error };
    }

    return { success: true, response: data };
  },

  async getEvents(): Promise<{ success: boolean; error?: string; response?: Event[] }> {
    const res = await fetch(`${API_URL}/events`, {
      method: 'GET',
    });

    const data = await res.json();

    checkTokenExpired(res.status, data.error);

    if (!res.ok) {
      return { success: false, error: data.error };
    }

    return { success: true, response: data.response || [] };
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

    const res = await fetch(`${API_URL}/events/${eventId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
      body: JSON.stringify(eventData),
    });

    const data = await res.json();

    checkTokenExpired(res.status, data.error);

    if (!res.ok) {
      return { success: false, error: data.error };
    }
    return { success: true, response: data };
  },

  async deleteEvent(
    eventId: string
  ): Promise<{ success: boolean; error?: string; response?: string }> {
    const res = await fetch(`${API_URL}/events/${eventId}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
    });

    const data = await res.json();

    checkTokenExpired(res.status, data.error);

    if (!res.ok) {
      return { success: false, error: data.error };
    }
    return { success: true, response: data.message };
  },
};

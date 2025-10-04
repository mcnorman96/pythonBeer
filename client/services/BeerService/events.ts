import { API_URL } from "../vars";
export interface EventsService {
  createEvent: (eventData: { name: string; description: string }) => Promise<{ success: boolean; error?: string; response?: any }>;
  getEvents: () => Promise<{ success: boolean; error?: string; response?: Array<any> }>;
  getEventById: (eventId: string) => Promise<{ data: any; error: any; pending: any }>;
  updateEvent: (eventId: string, eventData: { name: string; description: string }) => Promise<{ success: boolean; error?: string; response?: any }>;
  deleteEvent: (eventId: string) => Promise<{ success: boolean; error?: string; response?: any }>;
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
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify(eventData),
    });
    
    const data = await res.json();

    if (!res.ok) {
      return { success: false, error: data.error };
    }

    return { success: true, response: data };
  },

  async getEvents(): Promise<{ success: boolean; error?: string; response?: Array<any> }> {
    const res = await fetch(`${API_URL}/events`, {
      method: 'GET',
    });

    if (res.status === 204) {
      return { success: true, response: [] }; // No content, return empty array
    }

    const data = await res.json();

    if (!res.ok) {
      return { success: false, error: data.error };
    }
     
    return { success: true, response: data.response || [] };
  },

  async getEventById(eventId: string): Promise<{ data: any; error: any; pending: any }> {
    const { data, error, pending } = await useFetch(`${API_URL}/events/${eventId}`);
    return { data, error, pending };
  },

  async updateEvent(eventId: string, eventData: { name: string; description: string }): Promise<{ success: boolean; error?: string; response?: any }> {
    if (!eventData.name || !eventData.description) {
      return { success: false, error: 'All fields are required' };
    }
    
    const res = await fetch(`${API_URL}/events/${eventId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify(eventData),
    });
    
    const data = await res.json();
    
    if (!res.ok) {
      return { success: false, error: data.error };
    }
    return { success: true, response: data };
  },

  async deleteEvent(eventId: string): Promise<{ success: boolean; error?: string, response?: any }> {
    const res = await fetch(`${API_URL}/events/${eventId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });

    const data = await res.json();

    if (!res.ok) {
      return { success: false, error: data.error };
    }
    return { success: true, response: data.response };
  }
};
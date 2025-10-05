import { API_URL } from '../vars';

export interface EventParticipantsService {
  getEventParticipants: (eventId: string) => Promise<{ data: any; error: any; pending: any }>;
  newParticipant: (
    eventId: string,
    participantData: { name: string; email: string }
  ) => Promise<{ success: boolean }>;
}

export const eventParticipants: EventParticipantsService = {
  async getEventParticipants(eventId: string): Promise<{ data: any; error: any; pending: any }> {
    const { data, error, pending } = await useFetch(`${API_URL}/events/${eventId}/participants`);
    return { data, error, pending };
  },
  async newParticipant(
    eventId: string,
    participantData: { name: string; email: string }
  ): Promise<{ success: boolean }> {
    // Placeholder for adding a participant to a specific event
    return { success: true };
  },
};

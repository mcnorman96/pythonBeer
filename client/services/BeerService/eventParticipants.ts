import { API_URL } from "../vars";

export const eventParticipants = {
  getEventParticipants: async (eventId: string) => {
    const { data, error, pending } = await useFetch(`${API_URL}/events/${eventId}/participants`);
    return { data, error, pending };
  },
  newParticipant: async (eventId: string, participantData: { name: string; email: string }) => {
    // Placeholder for adding a participant to a specific event
    return { success: true };
  }
};
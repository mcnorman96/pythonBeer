import type { Participants, UseFetchResult } from '@/types/types';
import { API_URL } from '../vars';

export interface EventParticipantsService {
  getEventParticipants: (eventId: string) => Promise<UseFetchResult<Participants>>;
}

export const eventParticipants: EventParticipantsService = {
  async getEventParticipants(eventId: string): Promise<UseFetchResult<Participants>> {
    const { data, error, pending }: UseFetchResult<Participants> = await useFetch(
      `${API_URL}/events/${eventId}/participants`
    );
    return { data, error, pending };
  },
};

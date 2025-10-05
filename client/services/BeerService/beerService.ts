import type {
  EventBeerService,
  EventParticipantsService,
  EventsService,
  RatingsService,
} from '~/types/types';
import { eventBeer } from './eventBeer';
import { eventParticipants } from './eventParticipants';
import { events } from './events';
import { ratings } from './ratings';

export interface BeerService {
  events: EventsService;
  eventBeer: EventBeerService;
  eventParticipants: EventParticipantsService;
  ratings: RatingsService;
}

const beerService: BeerService = {
  events,
  eventBeer,
  eventParticipants,
  ratings,
};

export default beerService;

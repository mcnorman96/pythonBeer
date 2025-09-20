import { eventBeer } from './eventBeer';
import { eventParticipants } from './eventParticipants';
import { events } from './events';
import { ratings } from './ratings';

const beerService = {
  events,
  eventBeer,
  eventParticipants,
  ratings
};

export default beerService;


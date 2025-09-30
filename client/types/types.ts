import type { EventsService } from "../services/BeerService/events";
import type { EventBeerService } from "../services/BeerService/eventBeer";
import type { EventParticipantsService } from "../services/BeerService/eventParticipants";
import type { RatingsService } from "../services/BeerService/ratings";

export interface Event {
  id: Number,
  name: String,
  start_date: String
  end_date: String,
  description: String,
}

export interface Beer {
  id: Number,
  brewery: String,
  description: String,
  name: String,
  type: String 
}

export interface Participants {
  user_id: Number,
  user_name: String
}

export interface User {
  user_name: String,
  password: String,
  email: String 
}

export interface Rating {
  id: Number,
  event_id: String,
  beer_id: String,
  taste: Number,
  aftertaste: Number,
  smell: Number,
  design: Number,
  score: Number
}

export interface ResponseTypeBeers extends Response {
  response: Array<Beer>;
}
export interface ResponseTypeParticipants extends Response {
  response: Array<Participants>;
}

export interface Response {
  'success': Boolean,
  'error'?: String,
  'response'?: Event | Participants | User | Rating | Array<Event> | Array<Participants> | Array<Beer>
}

export type { EventsService, EventBeerService, EventParticipantsService, RatingsService };
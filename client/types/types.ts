import type { EventsService } from '../services/BeerService/events';
import type { EventBeerService } from '../services/BeerService/eventBeer';
import type { EventParticipantsService } from '../services/BeerService/eventParticipants';
import type { RatingsService } from '../services/BeerService/ratings';

export interface Event {
  id: number;
  name: string;
  start_date: string;
  end_date: string;
  description: string;
}

export interface Beer {
  id: number;
  brewery: string;
  description: string;
  name: string;
  type: string;
}

export interface Participants {
  user_id: number;
  user_name: string;
}

export interface User {
  user_name: string;
  password: string;
  email: string;
}

export interface Rating {
  id: number;
  event_id: string;
  beer_id: string;
  taste: number;
  aftertaste: number;
  smell: number;
  design: number;
  score: number;
}

export interface ResponseTypeBeers extends Response {
  response: Array<Beer>;
}
export interface ResponseTypeParticipants extends Response {
  response: Array<Participants>;
}

export interface Response {
  success: boolean;
  error?: string;
  response?:
    | Event
    | Participants
    | User
    | Rating
    | Array<Event>
    | Array<Participants>
    | Array<Beer>;
}

export type { EventsService, EventBeerService, EventParticipantsService, RatingsService };

// Define a generic type for useFetch return
export type UseFetchResult<T> = {
  data: Ref<T | null>;
  error: Ref<string | null>;
  pending: Ref<boolean>;
};

export type FetchResult<T> = {
  success: boolean;
  error?: string | null;
  response?: T;
};

export type FetchMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';

export interface fetchHelperType {
  path: string;
  method?: FetchMethod;
  body?: object | string | null;
  checkToken?: boolean;
}

export interface fetchingOptionsType {
  method: FetchMethod;
  headers: HeadersInit;
  body?: string;
}

export interface RegisterUserData {
  username: string;
  password: string;
  email: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

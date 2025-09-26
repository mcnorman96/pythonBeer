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
export interface ResponseTypeBeers {
  response: Array<Beer>;
}
export interface ResponseTypeParticipants {
  response: Array<Participants>;
}
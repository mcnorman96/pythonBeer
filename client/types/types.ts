export interface EventInterface {
  id: Number,
  name: String,
  start_date: String
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
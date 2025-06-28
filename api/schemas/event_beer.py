from pydantic import BaseModel, validator

class EventBeersSchema(BaseModel):
  event_id: int
  beer_id: int

  @validator('event_id')
  def eventid_must_be_non_empty(cls, v: str) -> str:
      if not v:
          raise ValueError('event id cannot be empty')
      return v
    
  @validator('beer_id')
  def userid_must_be_non_empty(cls, v: str) -> str:
      if not v:
          raise ValueError('user id cannot be empty')
      return v

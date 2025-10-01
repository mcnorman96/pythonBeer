from pydantic import BaseModel, field_validator

class EventParticipantSchema(BaseModel):
  event_id: int
  user_id: int

  @field_validator('event_id')
  def eventid_must_be_non_empty(cls, v: str) -> str:
      if not v:
          raise ValueError('event id cannot be empty')
      return v
    
  @field_validator('user_id')
  def userid_must_be_non_empty(cls, v: str) -> str:
      if not v:
          raise ValueError('user id cannot be empty')
      return v


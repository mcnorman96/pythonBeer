from app import db
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ValidationError, validator

class EventParticipantsModel(BaseModel):
  event_id: int
  user_id: int

  @validator('event_id')
  def eventid_must_be_non_empty(cls, v: str) -> str:
      if not v:
          raise ValueError('event id cannot be empty')
      return v
    
  @validator('user_id')
  def userid_must_be_non_empty(cls, v: str) -> str:
      if not v:
          raise ValueError('user id cannot be empty')
      return v

class EventParticipant:
    @staticmethod
    def create(event_id: int, user_id: int) -> None:
        try:
            events = EventParticipantsModel(event_id=event_id, user_id=user_id)
        except ValidationError as e:
            raise ValueError(f"Invalid data: {e}")

        cur = db.connection.cursor()
        cur.execute("INSERT INTO event_participants (event_id, user_id) VALUES (%s, %s)", (events.event_id, events.user_id ))
        db.connection.commit()
        cur.close()

    @staticmethod
    def get_all_users_in_event(event_id) -> List[Dict[str, Any]]:
        cur = db.connection.cursor()
        cur.execute("SELECT u.id AS user_id, u.username AS user_name FROM user u JOIN event_participants e ON u.id = e.user_id WHERE e.event_id = (%s) GROUP BY u.id ORDER BY u.id DESC", (event_id, ))
        rows = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        cur.close()
        events = [dict(zip(column_names, row)) for row in rows]
        return events

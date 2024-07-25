from app import db
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ValidationError, validator

class EventBeersModel(BaseModel):
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

class EventBeers:
    @staticmethod
    def create(event_id: int, beer_id: int) -> None:
        try:
            events = EventBeersModel(event_id=event_id, beer_id=beer_id)
            print(events)
        except ValidationError as e:
            raise ValueError(f"Invalid data: {e}")

        cur = db.connection.cursor()
        cur.execute("INSERT INTO event_beers (event_id, beer_id) VALUES (%s, %s)", (events.event_id, events.beer_id ))
        db.connection.commit()
        cur.close()

    @staticmethod
    def get_all_beers_in_event(event_id) -> List[Dict[str, Any]]:
        cur = db.connection.cursor()
        cur.execute("SELECT b.id AS id, b.name as name, b.description as description, b.brewery as brewery, b.type as type FROM beer b JOIN event_beers e ON b.id = e.beer_id WHERE e.event_id = (%s)", (event_id, ))
        rows = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        cur.close()
        events = [dict(zip(column_names, row)) for row in rows]
        return events

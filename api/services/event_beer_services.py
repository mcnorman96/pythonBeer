
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ValidationError
from app import db
from schemas.event_beer import EventBeersModel
from models.event_beer import EventBeer as EventBeerORM
from sqlalchemy import text
from datetime import datetime, timedelta

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class EventBeersService:
    @staticmethod
    def create(event_id: int, beer_id: int) -> None:
        try:
            validated_event_beers = EventBeersModel(event_id=event_id, beer_id=beer_id)
        except ValidationError as e:
            raise ValueError(f"Invalid data: {e}")

        event_beers = EventBeerORM(
            event_id=validated_event_beers.event_id,
            beer_id=validated_event_beers.beer_id,
            added_at=datetime.utcnow()
        )

        db.session.add(event_beers)
        db.session.commit()

    @staticmethod
    def get_all_beers_in_event(event_id) -> List[Dict[str, Any]]:
        if not event_id:
            raise ValueError("Event ID must be provided")

        query = text("""
            SELECT 
                b.id AS id, 
                b.name AS name, 
                b.description AS description, 
                b.brewery AS brewery, 
                b.type AS type
            FROM beer AS b
            INNER JOIN event_beer AS e ON b.id = e.beer_id
            WHERE e.event_id = :event_id
        """)

        result = db.session.execute(query, {'event_id': event_id})
        if not result:
            raise ValueError(f"No beers found for event ID {event_id}")
        
        return [dict(row._mapping) for row in result]

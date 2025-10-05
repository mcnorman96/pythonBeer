from typing import List, Dict, Any
from pydantic import ValidationError
from db import db
from schemas.event_beer import EventBeersSchema
from models.event_beer import EventBeer as EventBeerORM
from sqlalchemy import text
from datetime import datetime
from app import socketio
from services.ratings_service import RatingsService

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class EventBeersService:
    @staticmethod
    def add_beer_to_event(event_id):
        socketio.emit('beer_added', {'event_id': event_id})

    @staticmethod
    def create(event_id: int, beer_id: int) -> None:
        try:
            validated_event_beers = EventBeersSchema(event_id=event_id, beer_id=beer_id)
        except ValidationError as e:
            raise ValueError(f"Invalid data: {e}")

        checkIfBeerExists = db.session.query(EventBeerORM).filter_by(event_id=event_id, beer_id=beer_id).first()
        if checkIfBeerExists:
            raise ValueError("This beer is already added to the event")
        
        event_beers = EventBeerORM(
            event_id=validated_event_beers.event_id,
            beer_id=validated_event_beers.beer_id,
            added_at=datetime.utcnow()
        )

        db.session.add(event_beers)
        db.session.commit()
        EventBeersService.add_beer_to_event(event_id)

    @staticmethod
    def deleteAllEventBeersForEvent(event_id: int) -> None:
        if not event_id:
            raise ValueError("event id should be passed")
        
        # Delete all ratings attached to the event beers
        RatingsService.deleteAllRatingsForEvent(event_id)

        # Deleting all the event beers attached to the event
        EventBeerORM.query.filter_by(event_id=event_id).delete()
        db.session.commit()

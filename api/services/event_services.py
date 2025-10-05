
from datetime import datetime, timedelta
from db import db
from typing import List, Dict, Any, Optional
from pydantic import ValidationError
from models.event import Event as EventORM
from schemas.event import EventsSchema
from app import socketio
from services.event_beer_services import EventBeersService
from utils.utils import get_logger
logging = get_logger(__name__)


class EventService:
    @staticmethod
    def event_created():
        socketio.emit("event_created")
        logging.info("Socket event 'event_created' emitted.")

    @staticmethod
    def create(name: str, description: str) -> Optional[EventORM]:
        # Validate input
        if not name or not description:
            logging.error("Event name and description must be provided")
            raise ValueError("Event name and description must be provided")

        try:
            validated_event = EventsSchema(name=name, description=description)
        except ValidationError as e:
            logging.error(f"Invalid data: {e}")
            raise ValueError(f"Invalid data: {e}")

        startDate = datetime.utcnow()
        endDate = startDate + timedelta(days=1)

        event = EventORM(
            name=validated_event.name,
            start_date=startDate,
            end_date=endDate,
            description=validated_event.description,
        )
        db.session.add(event)
        db.session.commit()
        EventService.event_created()
        logging.info(f"Created event '{name}' with description '{description}'")
        return event

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        events = EventORM.query.all()
        logging.info(f"Fetched {len(events)} events")
        return [event.to_dict() for event in events]

    @staticmethod
    def get_by_id(id: int) -> Optional[Dict[str, Any]]:
        event = EventORM.query.get(id)
        if event:
            logging.info(f"Fetched event {id}")
            return event.to_dict()
        else:
            logging.warning(f"Event {id} not found")
            return None

    @staticmethod
    def update(id: int, name: str, description: str) -> bool:
        event = EventORM.query.get(id)
        if event:
            try:
                validated_event = EventsSchema(name=name, description=description)
            except ValidationError as e:
                logging.error(f"Invalid data: {e}")
                raise ValueError(f"Invalid data: {e}")

            event.name = validated_event.name
            event.description = validated_event.description
            db.session.commit()
            EventService.event_created()
            logging.info(f"Updated event {id} with name '{name}' and description '{description}'")
            return True
        logging.warning(f"Event {id} not found for update")
        return False

    @staticmethod
    def delete(id: int) -> bool:
        event = EventORM.query.get(id)
        if event:
            # Deleting the Event Beers
            EventBeersService.deleteAllEventBeersForEvent(id)

            # Deleting the event
            db.session.delete(event)
            db.session.commit()
            logging.info(f"Deleted event {id}")
            return True
        logging.warning(f"Event {id} not found for deletion")
        return False

from pydantic import ValidationError
from db import db
from schemas.event_beer import EventBeersSchema
from models.event_beer import EventBeer as EventBeerORM
from datetime import datetime
from services.ratings_service import RatingsService
from utils.utils import get_logger
from socketio_instance import socketio
logging = get_logger(__name__)

class EventBeersService:
    @staticmethod
    def updated_beer_in_event(event_id: int) -> None:
        logging.info(f"Beers in event updated {event_id}")
        socketio.emit("beers_in_event_updated", {"event_id": event_id})

    @staticmethod
    def create(event_id: int, beer_id: int) -> EventBeerORM:
        try:
            validated_event_beers = EventBeersSchema(event_id=event_id, beer_id=beer_id)
        except ValidationError as e:
            logging.error(f"Validation error: {e}")
            raise ValueError(f"Invalid data: {e}")

        # Check if beer already exists in event
        checkIfBeerExists = (
            db.session.query(EventBeerORM)
            .filter_by(event_id=event_id, beer_id=beer_id)
            .first()
        )
        if checkIfBeerExists:
            logging.warning(f"Beer {beer_id} already added to event {event_id}")
            raise ValueError("This beer is already added to the event")

        # Create new event beer
        event_beers = EventBeerORM(
            event_id=validated_event_beers.event_id,
            beer_id=validated_event_beers.beer_id,
            added_at=datetime.utcnow(),
        )

        db.session.add(event_beers)
        db.session.commit()
        EventBeersService.updated_beer_in_event(event_id)
        logging.info(f"Created EventBeer: event_id={event_id}, beer_id={beer_id}")
        return event_beers

    @staticmethod
    def deleteSingleEventBeerForEvent(event_id: int, beer_id: int) -> None:
        if not event_id or not beer_id:
            logging.error("event id and beer id should be passed")
            raise ValueError("event id and beer id should be passed")

        # Delete all ratings attached to the event beers
        RatingsService.deleteAllRatingsForBeerInEvent(event_id, beer_id)

        # Deleting all the event beers attached to the event
        deleted = EventBeerORM.query.filter_by(event_id=event_id, beer_id=beer_id).delete()
        db.session.commit()
        logging.info(f"Deleted {deleted} EventBeer(s) for event_id={event_id}, beer_id={beer_id}")
        EventBeersService.updated_beer_in_event(event_id)

    @staticmethod
    def deleteAllEventBeersForEvent(event_id: int) -> None:
        # Validate input
        if not event_id:
            logging.error("event id should be passed")
            raise ValueError("event id should be passed")

        # Delete all ratings attached to the event beers
        RatingsService.deleteAllRatingsForEvent(event_id)

        # Deleting all the event beers attached to the event
        deleted = EventBeerORM.query.filter_by(event_id=event_id).delete()
        db.session.commit()
        logging.info(f"Deleted {deleted} EventBeer(s) for event_id={event_id}")

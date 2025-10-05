
from sqlalchemy import text
from models.event_participant import EventParticipant as EventParticipantORM
from schemas.event_participant import EventParticipantSchema
from db import db
from typing import List, Dict, Any
from pydantic import ValidationError
from utils.utils import get_logger
logging = get_logger(__name__)


class EventParticipantService:
    @staticmethod
    def create(event_id: int, user_id: int) -> EventParticipantORM:
        # Validate input
        if not event_id or not user_id:
            logging.error("Event ID and User ID must be provided")
            raise ValueError("Event ID and User ID must be provided")

        try:
            validated_event_participant = EventParticipantSchema(
                event_id=event_id, user_id=user_id
            )
        except ValidationError as e:
            logging.error(f"Invalid data: {e}")
            raise ValueError(f"Invalid data: {e}")

        if EventParticipantORM.query.filter_by(
            event_id=event_id, user_id=user_id
        ).first():
            logging.warning(f"User {user_id} already registered for event {event_id}")
            raise ValueError("User is already registered for this event")

        event_participant = EventParticipantORM(
            event_id=validated_event_participant.event_id,
            user_id=validated_event_participant.user_id,
        )

        db.session.add(event_participant)
        db.session.commit()
        logging.info(f"User {user_id} registered for event {event_id}")
        return event_participant

    @staticmethod
    def get_all_users_in_event(event_id: int) -> List[Dict[str, Any]]:
        # Validate input
        if not event_id:
            logging.error("Event ID must be provided")
            raise ValueError("Event ID must be provided")

        query = text(
            """
            SELECT u.id AS user_id, u.username AS user_name
            FROM user u
            JOIN event_participant e ON u.id = e.user_id
            WHERE e.event_id = :event_id
            GROUP BY u.id
            ORDER BY u.id DESC
            """
        )

        result = db.session.execute(query, {"event_id": event_id})
        users = [dict(row) for row in result.mappings()]
        logging.info(f"Fetched {len(users)} users for event {event_id}")
        return users

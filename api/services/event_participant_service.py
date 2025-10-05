from sqlalchemy import text
from models.event_participant import EventParticipant as EventParticipantORM
from schemas.event_participant import EventParticipantSchema
from db import db
from typing import List, Dict, Any
from pydantic import ValidationError


class EventParticipantService:
    @staticmethod
    def create(event_id: int, user_id: int) -> None:
        if not event_id or not user_id:
            raise ValueError("Event ID and User ID must be provided")

        try:
            validated_event_participant = EventParticipantSchema(
                event_id=event_id, user_id=user_id
            )
        except ValidationError as e:
            raise ValueError(f"Invalid data: {e}")

        if EventParticipantORM.query.filter_by(
            event_id=event_id, user_id=user_id
        ).first():
            raise ValueError("User is already registered for this event")

        event_participant = EventParticipantORM(
            event_id=validated_event_participant.event_id,
            user_id=validated_event_participant.user_id,
        )

        db.session.add(event_participant)
        db.session.commit()

    @staticmethod
    def get_all_users_in_event(event_id) -> List[Dict[str, Any]]:
        if not event_id:
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
        return [dict(row) for row in result.mappings()]

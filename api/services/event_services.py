from datetime import datetime
from app import db
from typing import List,Dict, Any
from pydantic import ValidationError, validator
from models.event import Event as EventORM
from schemas.event import EventsModel

class EventService:
    @staticmethod
    def create(name: str, description: str) -> None:
        try:
            validated_event = EventsModel(
                name=name,
                description=description
            )
        except ValidationError as e:
            raise ValueError(f"Invalid data: {e}")

        events = EventORM(
            name=validated_event.name,
            start_date=datetime.utcnow(),
            end_date=None,
            description=validated_event.description
        )

        db.session.add(events)
        db.session.commit()

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        return [event.to_dict() for event in EventORM.query.all()]

    @staticmethod
    def delete(id: int) -> None:
        event = EventORM.query.get(id)
        if event:
            db.session.delete(event)
            db.session.commit()

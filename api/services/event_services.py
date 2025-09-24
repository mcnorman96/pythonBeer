from datetime import datetime
from db import db
from typing import List,Dict, Any
from pydantic import ValidationError
from models.event import Event as EventORM
from schemas.event import EventsSchema

class EventService:
    @staticmethod
    def create(name: str, description: str) -> None:
        try:
            validated_event = EventsSchema(
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
    def get_by_id(id: int) -> Dict[str, Any]:
        event = EventORM.query.get(id)
        if event:
            return event.to_dict()
        else:
            return None

    @staticmethod
    def delete(id: int) -> None:
        event = EventORM.query.get(id)
        if event:
            db.session.delete(event)
            db.session.commit()

from app import db
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ValidationError, validator

class EventsModel(BaseModel):
    id: Optional[int] = None
    name: str

    @validator('name')
    def name_must_be_non_empty(cls, v: str) -> str:
        if not v:
            raise ValueError('name cannot be empty')
        return v


class Events:
    @staticmethod
    def create(name: str) -> None:

        try:
            events = EventsModel(name=name)
        except ValidationError as e:
            raise ValueError(f"Invalid data: {e}")

        cur = db.connection.cursor()
        cur.execute("INSERT INTO events (name) VALUES (%s)", (events.name, ))
        db.connection.commit()
        cur.close()

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM events")
        rows = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        cur.close()
        events = [dict(zip(column_names, row)) for row in rows]
        return events

    @staticmethod
    def delete(id: int) -> None:
        cur = db.connection.cursor()
        cur.execute("DELETE FROM events WHERE id = %s", [id])
        db.connection.commit()
        cur.close()

from app import db
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ValidationError, validator

class BeerModel(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    brewery: Optional[str]
    type: Optional[str]

    @validator('name')
    def name_must_be_non_empty(cls, v: str) -> str:
        if not v:
            raise ValueError('name cannot be empty')
        return v

    @validator('description')
    def description_must_be_non_empty(cls, v: str) -> str:
        if not v:
            raise ValueError('description cannot be empty')
        return v
    
class Beer:
    @staticmethod
    def create(name: str, description: str, brewery: str, type: str) -> None:
        try:
            beer = BeerModel(name=name, description=description, brewery=brewery, type=type)
        except ValidationError as e:
            raise ValueError(f"Invalid data: {e}")

        cur = db.connection.cursor()
        cur.execute("INSERT INTO beer (name, description, brewery, type) VALUES (%s, %s, %s, %s)", (beer.name, beer.description, beer.brewery, beer.type))
        db.connection.commit()
        cur.close()

    @staticmethod
    def search_by_name(name: str) -> Optional[Dict[str, Any]]:
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM beer WHERE name = %s", [name])
        rows = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        cur.close()
        beers = [dict(zip(column_names, row)) for row in rows]
        if beers:
          return beers
        return None

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM beer")
        rows = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        cur.close()
        beers = [dict(zip(column_names, row)) for row in rows]
        return beers

    @staticmethod
    def delete(id: int) -> None:
        cur = db.connection.cursor()
        cur.execute("DELETE FROM beer WHERE id = %s", [id])
        db.connection.commit()
        cur.close()

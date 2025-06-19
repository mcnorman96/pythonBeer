from app import db
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ValidationError, validator

class RatingsModel(BaseModel):
    id: Optional[int] = None
    event_id: int
    user_id: int
    beer_id: int
    taste: int
    aftertaste: int
    smell: int
    design: int
    score: int

    @validator('event_id')
    def eventid_must_be_non_empty(cls, v: int) -> int:
        if not v:
            raise ValueError('event id cannot be empty')
        return v
    
    @validator('user_id')
    def userid_must_be_non_empty(cls, v: int) -> int:
        if not v:
            raise ValueError('user id cannot be empty')
        return v
    
    @validator('beer_id')
    def beerid_must_be_non_empty(cls, v: int) -> int:
        if not v:
            raise ValueError('beer id cannot be empty')
        return v
    
    @validator('taste')
    def taste_must_be_non_empty(cls, v: int) -> int:
        if not v:
            raise ValueError('taste cannot be empty')
        return v
    
    @validator('aftertaste')
    def aftertaste_must_be_non_empty(cls, v: int) -> int:
        if not v:
            raise ValueError('aftertaste cannot be empty')
        return v
    
    @validator('smell')
    def smell_must_be_non_empty(cls, v: int) -> int:
        if not v:
            raise ValueError('smell cannot be empty')
        return v
    
    @validator('design')
    def design_must_be_non_empty(cls, v: int) -> int:
        if not v:
            raise ValueError('design cannot be empty')
        return v
    
    @validator('score')
    def score_must_be_non_empty(cls, v: int) -> int:
        if not v:
            raise ValueError('score cannot be empty')
        return v

class Ratings:
    @staticmethod
    def create(event_id: int, user_id: int, beer_id: int, taste: int, aftertaste: int, smell: int, design: int,  score: int) -> None:
        try:
            ratings = RatingsModel(event_id=event_id, user_id=user_id, beer_id=beer_id, taste=taste, aftertaste=aftertaste, smell=smell, design=design,  score=score)
        except ValidationError as e:
            raise ValueError(f"Invalid data: {e}")

        cur = db.engine.connect()
        cur.execute("INSERT INTO ratings (event_id, user_id, beer_id, taste, aftertaste, smell, design, score) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (ratings.event_id, ratings.user_id, ratings.beer_id, ratings.taste, ratings.aftertaste, ratings.smell, ratings.design, ratings.score))
        db.connection.commit()
        cur.close()

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        cur = db.engine.connect()
        cur.execute("SELECT * FROM ratings")
        rows = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        cur.close()
        ratings = [dict(zip(column_names, row)) for row in rows]
        return ratings

    @staticmethod
    def get_toplist() -> List[Dict[str, Any]]:
        cur = db.engine.connect()
        cur.execute("SELECT b.id AS beer_id, b.name AS beer_name, b.description, b.brewery, b.type, AVG(r.score) AS average_score FROM beer b JOIN ratings r ON b.id = r.beer_id GROUP BY b.id ORDER BY average_score DESC")
        rows = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        cur.close()
        ratings = [dict(zip(column_names, row)) for row in rows]
        return ratings
    
    @staticmethod
    def get_toplist_by_event(event_id) -> List[Dict[str, Any]]:
        cur = db.engine.connect()
        cur.execute("SELECT b.id AS beer_id, b.name AS beer_name, b.description, b.brewery, b.type, AVG(r.score) AS average_score FROM beer b JOIN ratings r ON b.id = r.beer_id WHERE r.event_id = (%s) GROUP BY b.id ORDER BY average_score DESC", (event_id, ))
        rows = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        cur.close()
        ratings = [dict(zip(column_names, row)) for row in rows]
        return ratings
    
    @staticmethod
    def delete(id: int) -> None:
        cur = db.engine.connect()
        cur.execute("DELETE FROM ratings WHERE id = %s", [id])
        db.connection.commit()
        cur.close()

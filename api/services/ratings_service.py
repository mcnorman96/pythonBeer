from models.rating import Rating as RatingORM
from schemas.ratings import RatingsSchema
from db import db
from typing import List, Dict, Any
from pydantic import ValidationError
from sqlalchemy import text


class RatingsService:
    @staticmethod
    def create(event_id: int, user_id: int, beer_id: int, taste: int, aftertaste: int, smell: int, design: int,  score: int) -> None:
        try:
            validated_rating = RatingsSchema(event_id=event_id, user_id=user_id, beer_id=beer_id, taste=taste, aftertaste=aftertaste, smell=smell, design=design,  score=score)
        except ValidationError as e:
            raise ValueError(f"Invalid data: {e}")

        rating = RatingORM(
            event_id=validated_rating.event_id,
            user_id=validated_rating.user_id,
            beer_id=validated_rating.beer_id,
            taste=validated_rating.taste,
            aftertaste=validated_rating.aftertaste,
            smell=validated_rating.smell,
            design=validated_rating.design,
            score=validated_rating.score
        )
        db.session.add(rating)
        db.session.commit()

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        return [rating.to_dict() for rating in RatingORM.query.all()]

    @staticmethod
    def get_toplist() -> List[Dict[str, Any]]:
        """Get the top beers based on average ratings."""

        query = text("""
            SELECT b.id AS beer_id, b.name AS beer_name, b.description, b.brewery, b.type, AVG(r.score) AS average_score
            FROM beer b
            JOIN rating r ON b.id = r.beer_id
            GROUP BY b.id
            ORDER BY average_score DESC
        """)

        result = db.session.execute(query);
        return [dict(row._mapping) for row in result]

    @staticmethod
    def get_toplist_by_event(event_id) -> List[Dict[str, Any]]:
        if not event_id:
            raise ValueError("Event ID must be provided")

        query = text("""
            SELECT b.id AS beer_id, b.name AS beer_name, b.description, b.brewery, b.type, AVG(r.score) AS average_score
            FROM beer b
            JOIN rating r ON b.id = r.beer_id
            WHERE r.event_id = :event_id
            GROUP BY b.id
            ORDER BY average_score DESC
        """)

        result = db.session.execute(query, {"event_id": event_id})

        if not result:
            raise ValueError("No ratings found for this event")
        return [dict(row._mapping) for row in result]

    @staticmethod
    def delete(id: int) -> None:
        if not id:
            raise ValueError("ID must be provided")
        db.session.query(RatingORM).filter_by(id=id).delete()
        db.session.commit()
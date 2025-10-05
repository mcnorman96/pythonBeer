from models.rating import Rating as RatingORM
from schemas.ratings import RatingsSchema
from db import db
from typing import List, Dict, Any
from pydantic import ValidationError
from sqlalchemy import text
from app import socketio


class RatingsService:
    @staticmethod
    def rating_update(event_id):
        socketio.emit("rating_updated", {"event_id": event_id})

    @staticmethod
    def create(
        event_id: int,
        user_id: int,
        beer_id: int,
        taste: float,
        aftertaste: float,
        smell: float,
        design: float,
        score: float,
    ) -> None:
        try:
            validated_rating = RatingsSchema(
                event_id=event_id,
                user_id=user_id,
                beer_id=beer_id,
                taste=taste,
                aftertaste=aftertaste,
                smell=smell,
                design=design,
                score=score,
            )
        except ValidationError as e:
            raise ValueError(f"Invalid data: {e}")

        # Check if rating already exists for this user, event, and beer
        existing_rating = RatingORM.query.filter_by(
            event_id=event_id, user_id=user_id, beer_id=beer_id
        ).first()
        if existing_rating:
            # Update existing rating
            existing_rating.taste = validated_rating.taste
            existing_rating.aftertaste = validated_rating.aftertaste
            existing_rating.smell = validated_rating.smell
            existing_rating.design = validated_rating.design
            existing_rating.score = validated_rating.score
            db.session.commit()
            RatingsService.rating_update(event_id)
        else:
            # Create new rating
            rating = RatingORM(
                event_id=validated_rating.event_id,
                user_id=validated_rating.user_id,
                beer_id=validated_rating.beer_id,
                taste=validated_rating.taste,
                aftertaste=validated_rating.aftertaste,
                smell=validated_rating.smell,
                design=validated_rating.design,
                score=validated_rating.score,
            )
            db.session.add(rating)
            db.session.commit()
            RatingsService.rating_update(event_id)

    @staticmethod
    def getRating(event_id: int, user_id: int, beer_id: int) -> Dict[str, Any]:
        # Check if rating already exists for this user, event, and beer
        existing_rating = RatingORM.query.filter_by(
            event_id=event_id, user_id=user_id, beer_id=beer_id
        ).first()
        if existing_rating:
            return existing_rating.to_dict()
        else:
            return None

    @staticmethod
    def getAllRatingsForBeer(event_id: int, beer_id: int) -> Dict[str, Any]:
        # Retrieve ratings for a beer in an event, including username
        query = text(
            """
            SELECT r.*, u.username
            FROM rating AS r
            JOIN `user` AS u ON r.user_id = u.id
            WHERE r.event_id = :event_id AND r.beer_id = :beer_id
        """
        )
        result = db.session.execute(query, {"event_id": event_id, "beer_id": beer_id})
        ratings = []
        for row in result:
            rating_dict = dict(row._mapping)
            ratings.append(rating_dict)
        return ratings

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        return [rating.to_dict() for rating in RatingORM.query.all()]

    @staticmethod
    def get_toplist() -> List[Dict[str, Any]]:
        """Get the top beers based on average ratings."""

        query = text(
            """
            SELECT 
                b.id AS id, 
                b.name AS name, 
                b.description AS description, 
                b.brewery AS brewery, 
                b.type AS type,
                ROUND(AVG(r.score), 1) AS average_score,
                ROUND(AVG(r.smell), 1) AS average_smell,
                ROUND(AVG(r.aftertaste), 1) AS average_aftertaste,
                ROUND(AVG(r.taste), 1) AS average_taste,
                ROUND(AVG(r.design), 1) AS average_design
            FROM beer b
            JOIN rating r ON b.id = r.beer_id
            GROUP BY b.id
            ORDER BY average_score DESC
        """
        )

        result = db.session.execute(query)
        return [dict(row._mapping) for row in result]

    @staticmethod
    def get_toplist_by_event(
        event_id, sortby="event_beer_id", order="desc"
    ) -> List[Dict[str, Any]]:
        if not event_id:
            raise ValueError("Event ID must be provided")

        # Validate sortby and order
        allowed_sort_fields = [
            "event_beer_id",
            "average_score",
            "average_smell",
            "average_aftertaste",
            "average_taste",
            "average_design",
        ]
        if sortby not in allowed_sort_fields:
            sortby = "average_score"
        order = "DESC" if order.lower() == "desc" else "ASC"

        query = text(
            f"""
            SELECT 
                b.id AS id, 
                b.name AS name, 
                b.description AS description, 
                b.brewery AS brewery, 
                b.type AS type,
                e.id AS event_beer_id,
                ROUND(AVG(r.score), 1) AS average_score,
                ROUND(AVG(r.smell), 1) AS average_smell,
                ROUND(AVG(r.aftertaste), 1) AS average_aftertaste,
                ROUND(AVG(r.taste), 1) AS average_taste,
                ROUND(AVG(r.design), 1) AS average_design
            FROM beer AS b
            INNER JOIN event_beer AS e ON b.id = e.beer_id
            LEFT JOIN rating AS r ON b.id = r.beer_id AND r.event_id = e.event_id
            WHERE e.event_id = :event_id
            GROUP BY b.id, e.id
            ORDER BY {sortby} {order}
        """
        )

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

    @staticmethod
    def deleteAllRatingsForBeerInEvent(event_id: int, beer_id: int) -> None:
        if not event_id or not beer_id:
            raise ValueError("event id and beer id should be passed")

        RatingORM.query.filter_by(event_id=event_id, beer_id=beer_id).delete()
        db.session.commit()

    @staticmethod
    def deleteAllRatingsForEvent(event_id: int) -> None:
        if not event_id:
            raise ValueError("event id should be passed")

        RatingORM.query.filter_by(event_id=event_id).delete()
        db.session.commit()

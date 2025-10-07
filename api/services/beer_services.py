from models.beer import Beer as BeerORM
from db import db
from typing import List
from pydantic import ValidationError
from schemas.beer import BeerSchema
from typing import List
from utils.utils import get_logger
logging = get_logger(__name__)

class BeerService:

    @staticmethod
    def beer_created():
        from app import socketio
        socketio.emit("beer_created")
        logging.info("Socket event 'beer_created' emitted.")

    @staticmethod
    def beer_updated(beer: BeerORM):
        from app import socketio
        socketio.emit("beer_updated", {"beer": beer.to_dict()})
        logging.info("Socket event 'beer_updated' emitted.")

    @staticmethod
    def create(name: str, description: str, brewery: str, type: str) -> BeerORM:
        existing_beer = BeerORM.query.filter_by(name=name).first()
        if existing_beer:
            raise ValueError(f"Beer with name '{name}' already exists.")
        try:
            validated_beer = BeerSchema(
                name=name, description=description, brewery=brewery, type=type
            )
        except ValidationError as e:
            raise ValueError(f"Invalid data: {e}")

        beer = BeerORM(
            name=validated_beer.name,
            description=validated_beer.description,
            brewery=validated_beer.brewery,
            type=validated_beer.type,
        )
        db.session.add(beer)
        db.session.commit()
        BeerService.beer_created()
        return beer


    @staticmethod
    def update(
        beer_id: int, name: str, description: str, brewery: str, type: str
    ) -> BeerORM:
        beer = BeerORM.query.get(beer_id)
        if not beer:
            raise ValueError("Beer not found")
        try:
            validated_beer = BeerSchema(
                id=beer_id,
                name=name,
                description=description,
                brewery=brewery,
                type=type,
            )
        except ValidationError as e:
            raise ValueError(f"Invalid data: {e}")

        beer.name = validated_beer.name
        beer.description = validated_beer.description
        beer.brewery = validated_beer.brewery
        beer.type = validated_beer.type
        db.session.commit()
        BeerService.beer_updated(beer)
        return beer


    @staticmethod
    def search_by_name(name: str) -> List[dict]:
        if not name or len(name) < 3:
            raise ValueError("Search term must be at least 3 characters long")
        beers = BeerORM.query.filter(BeerORM.name.ilike(f"%{name}%")).all()
        return [beer.to_dict() for beer in beers]


    @staticmethod
    def get_all() -> List[dict]:
        beers = BeerORM.query.all()
        return [beer.to_dict() for beer in beers]

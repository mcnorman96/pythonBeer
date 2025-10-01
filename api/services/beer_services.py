from flask import jsonify
from models.beer import Beer as BeerORM
from db import db
from typing import List
from pydantic import ValidationError
from schemas.beer import BeerSchema
from typing import List,  Dict, Any


class BeerService:
  @staticmethod
  def create(name: str, description: str, brewery: str, type: str) -> None:
      # Check if beer name already exists
      existing_beer = BeerORM.query.filter_by(name=name).first()
      if existing_beer:
          raise ValueError(f"Beer with name '{name}' already exists.")
      try:
        validated_beer = BeerSchema(name=name, description=description, brewery=brewery, type=type)
      except ValidationError as e:
          raise ValueError(f"Invalid data: {e}")

      beer = BeerORM(
          name=validated_beer.name,
          description=validated_beer.description,
          brewery=validated_beer.brewery,
          type=validated_beer.type
      )

      db.session.add(beer)
      db.session.commit()
      return beer; 

  @staticmethod
  def search_by_name(name: str) -> List[dict]:
    if not name:
        return []
    if len(name) < 3:
        raise ValueError("Search term must be at least 3 characters long")
    beers = BeerORM.query.filter(BeerORM.name.ilike(f"%{name}%")).all()
    return [beer.to_dict() for beer in beers]
    
  @staticmethod
  def get_all() -> List[Dict[str, Any]]:
      return BeerORM.query.all()

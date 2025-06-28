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

  @staticmethod
  def delete(id: int) -> None:
      if not id:
          raise ValueError("ID must be provided")
      if id < 0:
          raise ValueError("ID must be a positive integer")
      
      beer = BeerORM.query.filter_by(id=id).first()
      if not beer:
          raise ValueError(f"No beer found with ID {id}")

      if beer:
          db.session.delete(beer)
          db.session.commit()
          return jsonify({'message': 'Beer deleted successfully'}), 200
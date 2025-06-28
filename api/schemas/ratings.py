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


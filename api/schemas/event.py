from app import db
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ValidationError, validator

class EventsModel(BaseModel):
    id: Optional[int] = None
    name: str
    description: str

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
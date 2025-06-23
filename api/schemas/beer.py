from typing import Optional
from pydantic import BaseModel, validator
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
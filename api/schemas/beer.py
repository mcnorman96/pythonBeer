from typing import Optional
from pydantic import BaseModel, field_validator


class BeerSchema(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    brewery: Optional[str]
    type: Optional[str]

    @field_validator("name")
    def name_must_be_non_empty(cls, v: str) -> str:
        if not v:
            raise ValueError("name cannot be empty")
        return v

    @field_validator("description")
    def description_must_be_non_empty(cls, v: str) -> str:
        if not v:
            raise ValueError("description cannot be empty")
        return v

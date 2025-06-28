from pydantic import BaseModel, validator
from typing import Optional
import re

class UserModel(BaseModel):
    id: Optional[int]
    username: str
    password: str
    email: str

    @validator('username')
    def validate_username(cls, v):
        if not v or not re.match(r'^[A-Za-z0-9]+$', v):
            raise ValueError("Username must be alphanumeric and non-empty.")
        return v

    @validator('password')
    def validate_password(cls, v):
        if not v:
            raise ValueError("Password cannot be empty.")
        return v

    @validator('email')
    def validate_email(cls, v):
        if not re.match(r'[^@]+@[^@]+\.[^@]+', v):
            raise ValueError("Invalid email address.")
        return v

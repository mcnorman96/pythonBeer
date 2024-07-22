from app import db
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ValidationError, validator
import re

class UserModel(BaseModel):
    id: Optional[int] = None
    username: str
    password: str
    email: str

    @validator('username')
    def username_must_be_non_empty(cls, v: str) -> str:
        if not v:
            raise ValueError('Username cannot be empty')
        elif not re.match(r'[A-Za-z0-9]+', v):
            raise ValueError('Username must contain only characters and numbers !')
        return v

    @validator('password')
    def password_must_be_non_empty(cls, v: str) -> str:
        if not v:
            raise ValueError('Password cannot be empty')
        return v
    
    @validator('email')
    def email_must_be_non_empty(cls, v: str) -> str:
        if not v:
            raise ValueError('Email cannot be empty')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', v):
            raise ValueError('Invalid email address !')
        return v

class User:
    @staticmethod
    def create(username: str, password: str, email: str) -> None:
        try:
            user = UserModel(username=username, password=password, email=email)
        except ValidationError as e:
            raise ValueError(f"Invalid data: {e}")

        cur = db.connection.cursor()
        cur.execute("INSERT INTO user (username, password, email) VALUES (%s, %s, %s)", (user.username, user.password, user.email))
        db.connection.commit()
        cur.close()

    @staticmethod
    def get_by_username(username: str) -> Optional[Dict[str, Any]]:
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM user WHERE username = %s", [username])
        user = cur.fetchone()
        cur.close()
        if user:
            return user
        return None

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM user")
        users = cur.fetchall()
        cur.close()
        return [dict(user) for user in users]

    @staticmethod
    def delete(username: str) -> None:
        cur = db.connection.cursor()
        cur.execute("DELETE FROM user WHERE username = %s", [username])
        db.connection.commit()
        cur.close()

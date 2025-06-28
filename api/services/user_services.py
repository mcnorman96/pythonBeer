from models.user import User as UserORM
from schemas.auth import UserSchema
from db import db
from typing import Optional, List
from pydantic import ValidationError
from werkzeug.security import generate_password_hash

class UserService:
    @staticmethod
    def create(username: str, password: str, email: str) -> UserORM:
        try:
            validated_user = UserSchema(username=username, password=password, email=email)
        except ValidationError as e:
            raise ValueError(f"Invalid input: {e}")

        hashed_pw = generate_password_hash(validated_user.password)

        user = UserORM(username=validated_user.username, password=hashed_pw, email=validated_user.email)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_by_username(username: str) -> Optional[UserORM]:
        if not username:
            raise ValueError("Username must be provided")
        
        return UserORM.query.filter_by(username=username).first()

    @staticmethod
    def get_all() -> List[UserORM]:
        return UserORM.query.all()

    @staticmethod
    def delete(username: str) -> None:
        if not username:
            raise ValueError("Username must be provided")
        
        user = UserORM.query.filter_by(username=username).first()
        if user:
            db.session.delete(user)
            db.session.commit()


from models.user import User as UserORM
from schemas.auth import UserSchema
from db import db
from typing import Optional, List
from pydantic import ValidationError
from werkzeug.security import generate_password_hash
from utils.utils import get_logger
logging = get_logger(__name__)


class UserService:
    @staticmethod
    def create(username: str, password: str, email: str) -> Optional[UserORM]:
        # Validate input
        if not all([username, password, email]):
            logging.error("Username, password, and email must be provided")
            raise ValueError("Username, password, and email must be provided")

        try:
            validated_user = UserSchema(
                username=username, password=password, email=email
            )
        except ValidationError as e:
            logging.error(f"Invalid input: {e}")
            raise ValueError(f"Invalid input: {e}")

        hashed_pw = generate_password_hash(validated_user.password)

        user = UserORM(
            username=validated_user.username,
            password=hashed_pw,
            email=validated_user.email,
        )
        db.session.add(user)
        db.session.commit()
        logging.info(f"Created user '{username}' with email '{email}'")
        return user

    @staticmethod
    def get_by_username(username: str) -> Optional[UserORM]:
        if not username:
            logging.error("Username must be provided")
            raise ValueError("Username must be provided")

        user = UserORM.query.filter_by(username=username).first()
        if user:
            logging.info(f"Fetched user '{username}'")
        else:
            logging.warning(f"User '{username}' not found")
        return user

    @staticmethod
    def get_all() -> List[UserORM]:
        users = UserORM.query.all()
        logging.info(f"Fetched {len(users)} users")
        return users

    @staticmethod
    def delete(user_id: int) -> bool:
        if not user_id:
            logging.error("id must be provided")
            raise ValueError("id must be provided")

        user = UserORM.query.filter_by(id=user_id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            logging.info(f"Deleted user '{user_id}'")
            return True
        logging.warning(f"User '{user_id}' not found for deletion")
        return False

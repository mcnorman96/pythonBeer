from flask import Blueprint, session, jsonify
from db import db
from werkzeug.security import check_password_hash
from models.user import User
from services.user_services import UserService
from utils.utils import get_json_data, get_logger, validate_fields, handle_exceptions
import jwt
import datetime
import os

logger = get_logger(__name__)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register_user():
    try:
        data = get_json_data()
        valid, msg = validate_fields(data, ["username", "password", "email"])
        if not valid:
            return jsonify({"error": msg}), 400

        user = UserService.create(
            username=data.get("username"),
            password=data.get("password"),
            email=data.get("email"),
        )
        return jsonify({"message": "User registered", "user_id": user.id}), 201

    except Exception as e:
        return handle_exceptions(e)


# LOGOUT
@auth_bp.route("/logout", methods=["POST"])
def logout_user():
    session.clear()  # Clears all session data
    return jsonify({"message": "Logged out successfully!"}), 200


# LOGIN
@auth_bp.route("/login", methods=["POST"])
def login_user():
    try:
        data = get_json_data()
        valid, msg = validate_fields(data, ["username", "password"])
        if not valid:
            return jsonify({"error": msg}), 400

        username = data.get("username")
        password = data.get("password")

        user = db.session.query(User).filter_by(username=username).first()

        # wrong user or password
        if not user or not check_password_hash(user.password, password):
            return jsonify({"error": "Incorrect username or password"}), 401

        # Login logic
        session["loggedin"] = True
        session["id"] = user.id
        session["username"] = user.username
        token = jwt.encode(
            {
                "user_id": user.id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
            },
            os.getenv("SECRET_KEY_AUTH", ""),
            algorithm="HS256",
        )
        return jsonify({"token": token}), 200

    except Exception as e:
        return handle_exceptions(e)

from flask import Blueprint, session, jsonify
from db import db
from werkzeug.security import check_password_hash
from models.user import User
from services.user_services import UserService
from utils.utils import get_json_data, get_logger, validate_fields, handle_exceptions, get_valid_user_id
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
        return jsonify({"message": "user.registered", "user_id": user.id}), 201

    except Exception as e:
        return handle_exceptions(e)


# LOGOUT
@auth_bp.route("/logout", methods=["POST"])
def logout_user():
    session.clear()  # Clears all session data
    return jsonify({"message": "logged.out"}), 200


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
            return jsonify({"error": "incorrect.login"}), 401

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


@auth_bp.route("/user", methods=["GET"])
def get_user():
    try:
        user_id = get_valid_user_id()
        user = db.session.query(User).filter_by(id=user_id).first()

        if not user:
            return jsonify({"error": "error.fetching.user"});
        return jsonify({"response": user.to_dict()})

    except Exception as e:
        return handle_exceptions(e)
    
@auth_bp.route("/user", methods=["PUT"])
def update_user():
    try:
        user_id = get_valid_user_id()  # Ensure user is authenticated
        data = get_json_data()
        valid, msg = validate_fields(data, ["username", "email"])
        if not valid:
            return jsonify({"error": msg}), 400

        updated_user = UserService.update(
            id=user_id,
            username=data.get("username"),
            email=data.get("email"),
        )

        if not updated_user:
            return jsonify({"error": "error.updating.user"});

        return (
            jsonify(
                {
                    "message": "user.updated",
                    "response": updated_user,
                }
            ),
            200,
        )

    except Exception as e:
        return handle_exceptions(e)
from flask import Blueprint, request, session, jsonify
from db import db
from werkzeug.security import check_password_hash
from models.user import User
from services.user_services import UserService
from utils.utils import get_json_data, get_valid_user_id
import jwt
import datetime
import os

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


register = Blueprint("register", __name__)


@register.route("/register", methods=["POST"])
def register_user():
    try:
        data = get_json_data()
        user = UserService.create(
            username=data.get("username"),
            password=data.get("password"),
            email=data.get("email"),
        )
        return jsonify({"message": "User registered", "user_id": user.id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


# LOGOUT
logout = Blueprint("logout", __name__)


@logout.route("/logout", methods=["POST"])
def logout_user():
    session.clear()  # Clears all session data
    return jsonify({"message": "Logged out successfully!"}), 200


# LOGIN
login = Blueprint("login", __name__)


@login.route("/login", methods=["POST"])
def login_user():
    try:
        data = get_json_data()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password required"}), 400

        user = db.session.query(User).filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
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
        else:
            return jsonify({"error": "Incorrect username or password"}), 401
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

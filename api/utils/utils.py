from flask import request, abort, jsonify, make_response
import jwt
import os
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_json_data():
    data = request.get_json()
    if not data:
        data = request.form.to_dict()
    return data


def get_user_id_from_token():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        logger.warning("Authorization header missing or invalid")
        return None

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(
            token, os.getenv("SECRET_KEY_AUTH", ""), algorithms=["HS256"]
        )
        user_id = payload.get("user_id")
        user_id = int(user_id)
        return user_id
    except jwt.ExpiredSignatureError:
        logger.warning("Token has expired")
        return None
    except jwt.InvalidTokenError:
        logger.warning("Invalid token")
        return None


def get_valid_user_id():
    user_id = get_user_id_from_token()
    if not isinstance(user_id, int):
        logger.error(f"Invalid user_id extracted: {user_id} (type: {type(user_id)})")
        response = make_response(jsonify({"error": "Unauthorized"}), 401)
        abort(response)
    return user_id

from flask import request, abort, jsonify, make_response
from werkzeug.exceptions import HTTPException
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

def validate_fields(data, fields):
    missing = [f for f in fields if not data.get(f)]
    if missing:
        return False, f"Missing fields: {', '.join(missing)}"
    return True, None

def get_user_id_from_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        logger.warning("Authorization header missing or invalid")
        return None

    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY_AUTH', ''), algorithms=['HS256'])
        user_id = payload.get('user_id')
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

def handle_exceptions(e):
    if isinstance(e, HTTPException):
        logger.error(f"HTTPException: {e}")
        return jsonify({'error': e.description}), e.code
    elif isinstance(e, ValueError):
        logger.error(f"ValueError: {e}")
        return jsonify({'error': str(e)}), 400
    else:
        logger.error(f"Exception: {e}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
    

def get_logger(name=None, level=logging.DEBUG):
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    return logging.getLogger(name)
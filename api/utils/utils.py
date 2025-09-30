from flask import request, abort
import jwt

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_json_data():
    data = request.get_json()
    if not data:
        data = request.form.to_dict()
    return data


def get_user_id_from_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        logger.warning("Authorization header missing or invalid")
        return None  # Or raise an error

    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
        user_id = payload.get('user_id')
        user_id = int(user_id)
        return user_id
    except jwt.ExpiredSignatureError:
        logger.warning("Token has expired")
        return None  # Or handle expired token
    except jwt.InvalidTokenError:
        logger.warning("Invalid token")
        return None  # Or handle invalid token


def get_valid_user_id():
    user_id = get_user_id_from_token()
    if not isinstance(user_id, int):
        logger.error(f"Invalid user_id extracted: {user_id} (type: {type(user_id)})")
        abort(401, description="Unauthorized")
    return user_id
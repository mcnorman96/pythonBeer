from flask import Blueprint, request, session, jsonify
from db import db
from werkzeug.security import check_password_hash
from models.user import User
from services.user_services import UserService
import jwt
import datetime
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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

register = Blueprint('register', __name__)
@register.route('/register', methods=['GET', 'POST'])
def register_user():
    data = request.get_json(silent=True)
    if not data: 
        data = request.form.to_dict()

    try:
        user = UserService.create(
            username=data.get('username'),
            password=data.get('password'),
            email=data.get('email')
        )
        return jsonify({"message": "User registered", "user_id": user.id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# LOGOUT
logout = Blueprint('logout', __name__)
@logout.route('/logout', methods=['POST'])
def logout_user():
    session.clear()  # Clears all session data
    return jsonify({'message': 'Logged out successfully!'}), 200

#LOGIN
login = Blueprint('login', __name__)
@login.route('/login', methods=['POST'])
def login_user():

    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    user = db.session.query(User).filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        session['loggedin'] = True
        session['id'] = user.id
        session['username'] = user.username
        # Generate JWT token
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, 'your_secret_key', algorithm='HS256')
        return jsonify({'token': token}), 200
    else:
        return jsonify({'error': 'Incorrect username or password'}), 401
from flask import Blueprint, request, session, jsonify
from app import db
from werkzeug.security import check_password_hash
from models.user import User
from services.user_services import UserService

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
        return jsonify({'message': 'Logged in successfully!'}), 200
    else:
        return jsonify({'error': 'Incorrect username or password'}), 401
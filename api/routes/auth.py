from flask import Blueprint, request, redirect, url_for, session, flash, jsonify
from app import db
import MySQLdb.cursors
import re
from schemas.auth import User

register = Blueprint('register', __name__)
@register.route('/register', methods=['GET', 'POST'])
def register_user():
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']

		try:
			if username and password:
					existing_user = User.get_by_username(username)
					if existing_user:
						return jsonify({'error': 'Username already exists!'}), 400
					else:
						User.create(username, password, email)
						return jsonify({'message': 'User created successfully'}), 201
			else:
				return jsonify({'error':'Please fill out all fields.'}), 400
		except ValueError as e:
			return jsonify({'error': str(e)}), 400


# LOGOUT
logout = Blueprint('logout', __name__)
@logout.route('/logout', methods=['GET', 'POST'])
def logout_user():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return jsonify({'message': 'Logged out!'}), 201 # Refactor so this is in the login page

#LOGIN
login = Blueprint('login', __name__)
@login.route('/login', methods=['GET', 'POST'])
def login_user():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']

		cursor = db.engine.connect(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM user WHERE username = % s AND password = % s', (username, password))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			msg = jsonify({'message': 'Logged in successfully !'})
		else:
			msg = jsonify({'error': 'Incorrect username / password !'}), 400
	return msg
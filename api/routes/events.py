from flask import Blueprint, request, redirect, url_for, session, flash, jsonify
from app import db
from models.events import Events

newEvents = Blueprint('new_events', __name__)
@newEvents.route('/new', methods=['GET', 'POST'])
def new_events():
  if request.method == 'POST' and all(k in request.form for k in ('name',)):
    name = request.form['name']

    try:
      if name:
        Events.create(name)
        return jsonify({'message': 'Events created succesfully'}), 201
      else:
        return jsonify({'error': 'Please fill out all fields.'}), 400
    except ValueError as e:
      return jsonify({'error': str(e)}), 400
  else:
    return jsonify({'error': 'Please fill out all fields.'}), 400


allEvents = Blueprint('all_events', __name__)
@allEvents.route('/', methods=['GET', 'POST'])
def all_events():
  if request.method == 'GET':
    try:
      events = Events.get_all()
      if (events):
        return jsonify({'response': events}), 200
      else: 
        return jsonify({'error': 'No events found'}), 400
    except ValueError as e:
      return jsonify({'error': str(e)}), 400
from flask import Blueprint, request, redirect, url_for, session, flash, jsonify
from app import db
from models.event_participants import EventParticipant

# TODO: Check for participant already registred
newEventParticipant = Blueprint('new_event_participant', __name__)
@newEventParticipant.route('/<int:event_id>/participants/new', methods=['GET', 'POST'])
def new_event_participant(event_id):
  if request.method == 'POST' and all(k in request.form for k in ( 'user_id', )):
    user_id = request.form['user_id']

    try:
      if event_id and user_id :
        EventParticipant.create(event_id, user_id)
        return jsonify({'message': 'Event participant created succesfully'}), 201
      else:
        return jsonify({'error': 'Please fill out all fieldsss.'}), 400
    except ValueError as e:
      return jsonify({'error': str(e)}), 400
  else:
    return jsonify({'error': 'Please fill out all fields.'}), 400


allEventParticipant = Blueprint('all_event_participant', __name__)
@allEventParticipant.route('/<int:event_id>/participants/', methods=['GET', 'POST'])
def all_event_participant(event_id):
  if request.method == 'GET':
    try:
      events = EventParticipant.get_all_users_in_event(event_id)
      if (events):
        return jsonify({'response': events}), 200
      else: 
        return jsonify({'error': 'No event participant found'}), 400
    except ValueError as e:
      return jsonify({'error': str(e)}), 400
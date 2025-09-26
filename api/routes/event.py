from flask import Blueprint, request, jsonify
from services.event_services import EventService

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

newEvents = Blueprint('new_events', __name__)
@newEvents.route('/new', methods=['POST'])
def new_events():
  data = request.get_json()
  if not data:
      data = request.form.to_dict()
  name = data.get('name')
  description = data.get('description')

  try:
    if name and description:
      EventService.create(name, description)
      return jsonify({'message': 'Events created successfully'}), 201
    else:
      return jsonify({'error': 'Please fill out all fields.'}), 400
  except ValueError as e:
    return jsonify({'error': str(e)}), 400


allEvents = Blueprint('all_events', __name__)
@allEvents.route('/', methods=['GET', 'POST'])
def all_events():
  if request.method == 'GET':
    try:
      events = EventService.get_all()
      if (events):
        return jsonify({'response': events}), 200
      else: 
        return jsonify({'error': 'No events found'}), 400
    except ValueError as e:
      return jsonify({'error': str(e)}), 400

getEventById = Blueprint('get_event_by_id', __name__)
@getEventById.route('/<int:event_id>', methods=['GET'])
def get_event_by_id(event_id):
  try:
    event = EventService.get_by_id(event_id)
    if event:
      return jsonify({'response': event}), 200
    else:
      return jsonify({'error': 'Event not found'}), 404
  except ValueError as e:
    return jsonify({'error': str(e)}), 400
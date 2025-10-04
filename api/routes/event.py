from flask import Blueprint, request, jsonify
from utils.utils import get_json_data, get_valid_user_id
from services.event_services import EventService
from werkzeug.exceptions import HTTPException
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

newEvents = Blueprint('new_events', __name__)
@newEvents.route('/new', methods=['POST'])
def new_events():
  try:
    get_valid_user_id()  # Ensure user is authenticated
    data = get_json_data()
    name = data.get('name')
    description = data.get('description')

    if name and description:
      EventService.create(name, description)
      return jsonify({'message': 'Events created successfully'}), 201
    else:
      return jsonify({'error': 'Please fill out all fields.'}), 400
    
  except HTTPException as http_exc:
    raise http_exc
  except ValueError as e:
    return jsonify({'error': str(e)}), 400
  except Exception as e:
    return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
  


allEvents = Blueprint('all_events', __name__)
@allEvents.route('/', methods=['GET', 'POST'])
def all_events():
  try:
    events = EventService.get_all()
    if (events):
      return jsonify({'response': events}), 200
    else: 
      return jsonify({'error': 'No events found'}), 400
    
  except ValueError as e:
    return jsonify({'error': str(e)}), 400
  except Exception as e:
    return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


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
  except Exception as e:
    return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
  
updateEvent = Blueprint('update_event', __name__)
@updateEvent.route('/<int:event_id>', methods=['PUT'])
def update_event(event_id):
  try:
    get_valid_user_id()  # Ensure user is authenticated
    data = get_json_data()
    name = data.get('name')
    description = data.get('description')

    if name and description:
      updated_event = EventService.update(event_id, name, description)
      if updated_event:
        return jsonify({'message': 'Event updated successfully', 'response': updated_event}), 200
      else:
        return jsonify({'error': 'Event not found'}), 404
    else:
      return jsonify({'error': 'Please fill out all fields.'}), 400
    
  except HTTPException as http_exc:
    raise http_exc
  except ValueError as e:
    return jsonify({'error': str(e)}), 400
  except Exception as e:
    return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
  
deleteEvent = Blueprint('delete_event', __name__)
@deleteEvent.route('/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
  try:
    get_valid_user_id()  # Ensure user is authenticated
    deleted = EventService.delete(event_id)
    if deleted:
      return jsonify({'message': 'Event deleted successfully'}), 200
    else:
      return jsonify({'error': 'Event not found'}), 404
    
  except HTTPException as http_exc:
    raise http_exc
  except ValueError as e:
    return jsonify({'error': str(e)}), 400
  except Exception as e:
    return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
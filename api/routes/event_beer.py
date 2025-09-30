from flask import Blueprint, request, jsonify
from utils.utils import get_json_data, get_valid_user_id
from services.event_beer_services import EventBeersService

newEventBeer = Blueprint('new_event_beer', __name__)
@newEventBeer.route('/<int:event_id>/beers', methods=['POST'])
def new_event_beer(event_id):
  try:
      get_valid_user_id()  # Ensure user is authenticated
      data = get_json_data()
      beer_id = data.get('beer_id')
      if event_id and beer_id:
        EventBeersService.create(event_id, beer_id)
        return jsonify({'message': 'Event beer created successfully'}), 201
      else:
        return jsonify({'error': 'Please fill out all fields.'}), 400
      
  except ValueError as e:
    return jsonify({'error': str(e)}), 400
  except Exception as e:
    return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

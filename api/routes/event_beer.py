from flask import Blueprint, request, jsonify
from services.event_beer_services import EventBeersService

newEventBeer = Blueprint('new_event_beer', __name__)
@newEventBeer.route('/<int:event_id>/beers', methods=['POST'])
def new_event_beer(event_id):
  data = request.get_json()
  if not data:
      data = request.form.to_dict()

  beer_id = data.get('beer_id')

  try:
    if event_id and beer_id:
      EventBeersService.create(event_id, beer_id)
      return jsonify({'message': 'Event beer created successfully'}), 201
    else:
      return jsonify({'error': 'Please fill out all fields.'}), 400
  except ValueError as e:
    return jsonify({'error': str(e)}), 400
 
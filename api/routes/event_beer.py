from flask import Blueprint, request, jsonify
from services.event_beer_services import EventBeersService

newEventBeer = Blueprint('new_event_beer', __name__)
@newEventBeer.route('/<int:event_id>/beers', methods=['GET', 'POST'])
def new_event_beer(event_id):
  if request.method == 'POST' and all(k in request.form for k in ('beer_id', )):
    beer_id = request.form['beer_id']
  
    try:
      if event_id and beer_id:
        EventBeersService.create(event_id, beer_id)
        return jsonify({'message': 'Event beer created successfully'}), 201
      else:
        return jsonify({'error': 'Please fill out all fields.'}), 400
    except ValueError as e:
      return jsonify({'error': str(e)}), 400
  else:
    return jsonify({'error': 'Please fill out all fields.'}), 400

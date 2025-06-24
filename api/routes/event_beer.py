from flask import Blueprint, request, jsonify
from services.event_beer_services import EventBeersService
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

newEventBeer = Blueprint('new_event_beer', __name__)
@newEventBeer.route('/<int:event_id>/beers/add', methods=['GET', 'POST'])
def new_event_beer(event_id):
  if request.method == 'POST' and all(k in request.form for k in ('beer_id', )):
    beer_id = request.form['beer_id']

    try:
      if event_id and beer_id :
        EventBeersService.create(event_id, beer_id)
        return jsonify({'message': 'Event beer created succesfully'}), 201
      else:
        return jsonify({'error': 'Please fill out all fieldsss.'}), 400
    except ValueError as e:
      logger.error(f"Error creating event beer: {e}")
      return jsonify({'error': str(e)}), 400
  else:
    return jsonify({'error': 'Please fill out all fields.'}), 400


allEventBeer = Blueprint('all_event_beer', __name__)
@allEventBeer.route('/<int:event_id>/beers', methods=['GET', 'POST'])
def all_event_beer(event_id):
  if request.method == 'GET':
    try:
      event_beers = EventBeersService.get_all_beers_in_event(event_id)
      if (event_beers):
        return jsonify({'response': event_beers}), 200
      else: 
        return jsonify({'error': 'No event beer found'}), 400
    except ValueError as e:
      return jsonify({'error': str(e)}), 400
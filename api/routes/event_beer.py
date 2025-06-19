from flask import Blueprint, request, redirect, url_for, session, flash, jsonify
from app import db
from schemas.event_beer import EventBeers

newEventBeer = Blueprint('new_event_beer', __name__)
@newEventBeer.route('/<int:event_id>/beers/add', methods=['GET', 'POST'])
def new_event_beer(event_id):
  if request.method == 'POST' and all(k in request.form for k in ('beer_id', )):
    beer_id = request.form['beer_id']

    try:
      if event_id and beer_id :
        EventBeers.create(event_id, beer_id)
        return jsonify({'message': 'Event beer created succesfully'}), 201
      else:
        return jsonify({'error': 'Please fill out all fieldsss.'}), 400
    except ValueError as e:
      return jsonify({'error': str(e)}), 400
  else:
    return jsonify({'error': 'Please fill out all fields.'}), 400


allEventBeer = Blueprint('all_event_beer', __name__)
@allEventBeer.route('/<int:event_id>/beers', methods=['GET', 'POST'])
def all_event_beer(event_id):
  if request.method == 'GET':
    try:
      events = EventBeers.get_all_beers_in_event(event_id)
      if (events):
        return jsonify({'response': events}), 200
      else: 
        return jsonify({'error': 'No event beer found'}), 400
    except ValueError as e:
      return jsonify({'error': str(e)}), 400
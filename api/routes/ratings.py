from flask import Blueprint, request, jsonify
from services.ratings_service import RatingsService
from routes.auth import get_user_id_from_token

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

newRatings = Blueprint('new_ratings', __name__)
@newRatings.route('/new', methods=['GET', 'POST'])
def new_ratings():
  if request.method == 'POST' and all(k in request.form for k in ('event_id', 'beer_id', 'taste', 'aftertaste', 'smell', 'design', 'score')):
    user_id = get_user_id_from_token()
    # Ensure user_id is an integer and not a tuple or None
    if not isinstance(user_id, int):
        logger.error(f"Invalid user_id extracted: {user_id} (type: {type(user_id)})")
        return jsonify({'error': 'Unauthorized'}), 401

    event_id = request.form['event_id']
    beer_id = request.form['beer_id']
    taste = request.form['taste']
    aftertaste = request.form['aftertaste']
    smell = request.form['smell']
    design = request.form['design']
    score = request.form['score']

    try:
      if event_id and user_id and beer_id and taste and aftertaste and smell and design and score:
        RatingsService.create(event_id, user_id, beer_id, taste, aftertaste, smell, design, score)
        return jsonify({'message': 'Ratings created succesfully'}), 201
      else:
        return jsonify({'error': 'Please fill out all fields.'}), 400
    except ValueError as e:
      return jsonify({'error': str(e), 'user_id': user_id}), 400
  else:
    return jsonify({'error': 'Please fill out all fields.'}), 400

getRating = Blueprint('get_ratings', __name__)
@getRating.route('/getRating', methods=['GET'])
def get_ratings():
    if request.method == 'GET' and all(request.args.get(k) for k in ('event_id', 'beer_id')):
        user_id = get_user_id_from_token()
        if not isinstance(user_id, int):
            logger.error(f"Invalid user_id extracted: {user_id} (type: {type(user_id)})")
            return jsonify({'error': 'Unauthorized'}), 401

        event_id = request.args.get('event_id')
        beer_id = request.args.get('beer_id')

        try:
            if event_id and user_id and beer_id:
                getRating = RatingsService.getRating(event_id, user_id, beer_id)
                return jsonify({'response': getRating}), 200
            else:
                return jsonify({'error': 'Please fill out all fields.'}), 400
        except ValueError as e:
            return jsonify({'error': str(e), 'user_id': user_id}), 400
    else:
        return jsonify({'error': 'Please fill out all fields.'}), 400


allRatings = Blueprint('all_ratings', __name__)
@allRatings.route('/', methods=['GET', 'POST'])
def all_ratings():
  if request.method == 'GET':
    try:
      ratings = RatingsService.get_all()
      if (ratings):
        return jsonify({'response': ratings}), 200
      else: 
        return jsonify({'error': 'No ratings found'}), 400
    except ValueError as e:
      return jsonify({'error': str(e)}), 400
    
toplistRatings = Blueprint('toplist', __name__)
@toplistRatings.route('/toplist', methods=['GET', 'POST'])
def toplist():
  if request.method == 'GET':
    try:
      ratings = RatingsService.get_toplist()
      if (ratings):
        return jsonify({'response': ratings}), 200
      else: 
        return jsonify({'error': 'No ratings found'}), 400
    except ValueError as e:
      return jsonify({'error': str(e)}), 400
    
toplistRatingsByEvent = Blueprint('toplist_by_event', __name__)
@toplistRatingsByEvent.route('/toplist/<int:event_id>', methods=['GET', 'POST'])
def toplist_by_event(event_id):
  if request.method == 'GET':
    try:
      if event_id:
        ratings = RatingsService.get_toplist_by_event(event_id)
        if (ratings):
          return jsonify({'response': ratings}), 200
        else: 
          return jsonify({'error': 'No ratings found'}), 400
    except ValueError as e:
      return jsonify({'error': str(e)}), 400
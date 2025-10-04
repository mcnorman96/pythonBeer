from flask import Blueprint, request, jsonify
from services.ratings_service import RatingsService
from routes.auth import get_valid_user_id
from utils.utils import get_json_data
from werkzeug.exceptions import HTTPException
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

newRatings = Blueprint('new_ratings', __name__)
@newRatings.route('/new', methods=['POST'])
def new_ratings():
  try:
    user_id = get_valid_user_id()
    data = get_json_data()
    event_id = data.get('event_id')
    beer_id = data.get('beer_id')
    taste = data.get('taste')
    aftertaste = data.get('aftertaste')
    smell = data.get('smell')
    design = data.get('design')
    score = data.get('score')

    if event_id and user_id and beer_id and taste and aftertaste and smell and design and score:
      RatingsService.create(event_id, user_id, beer_id, taste, aftertaste, smell, design, score)
      return jsonify({'message': 'Rating created successfully'}), 201
    else:
      return jsonify({'error': 'Please fill out all fields.'}), 400
    
  except HTTPException as http_exc:
    raise http_exc
  except ValueError as e:
    return jsonify({'error': str(e), 'user_id': user_id}), 400
  except Exception as e:
    return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


getRating = Blueprint('get_ratings', __name__)
@getRating.route('/getRating', methods=['GET'])
def get_ratings():
  try:
      user_id = get_valid_user_id()
      event_id = request.args.get('event_id')
      beer_id = request.args.get('beer_id')

      if event_id and user_id and beer_id:
          getRating = RatingsService.getRating(event_id, user_id, beer_id)
          if not getRating:
              return jsonify({'error': 'No rating found'}), 400
          return jsonify({'response': getRating}), 200
      else:
          return jsonify({'error': 'Please fill out all fields.'}), 400
      
  except HTTPException as http_exc:
      raise http_exc
  except ValueError as e:
      return jsonify({'error': str(e), 'user_id': user_id}), 400
  except Exception as e:
      return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

getAllRatingsForBeer = Blueprint('get_all_ratings_for_beer', __name__)
@getAllRatingsForBeer.route('/all', methods=['GET'])
def get_all_ratings_for_beer():
  try:
    event_id = request.args.get('event_id')
    beer_id = request.args.get('beer_id')

    if event_id and beer_id:
        getRating = RatingsService.getAllRatingsForBeer(event_id, beer_id)
        if not getRating:
            return jsonify({'error': 'No ratings found for this beer in the event'}), 204
        return jsonify({'response': getRating}), 200
    else:
        return jsonify({'error': 'Please fill out all fields.'}), 400
    
  except ValueError as e:
      return jsonify({'error': str(e)}), 400
  except Exception as e:
      return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

allRatings = Blueprint('all_ratings', __name__)
@allRatings.route('/', methods=['GET', 'POST'])
def all_ratings():
  try:
    ratings = RatingsService.get_all()
    if (ratings):
      return jsonify({'response': ratings}), 200
    else: 
      return jsonify({'error': 'No ratings found'}), 400
  except ValueError as e:
    return jsonify({'error': str(e)}), 400
  except Exception as e:
    return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
    

toplistRatings = Blueprint('toplist', __name__)
@toplistRatings.route('/toplist', methods=['GET', 'POST'])
def toplist():
  try:
    ratings = RatingsService.get_toplist()
    if (ratings):
      return jsonify({'response': ratings}), 200
    else:
      return jsonify({'error': 'No ratings found'}), 400
  except ValueError as e:
    return jsonify({'error': str(e)}), 400
  except Exception as e:
    return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
    

toplistRatingsByEvent = Blueprint('toplist_by_event', __name__)
@toplistRatingsByEvent.route('/toplist/<int:event_id>', methods=['GET', 'POST'])
def toplist_by_event(event_id):
  try:
    sortby = request.args.get('sortby', 'event_beer_id').lower()
    order = request.args.get('order', 'asc').lower()
    if event_id:
      ratings = RatingsService.get_toplist_by_event(event_id, sortby=sortby, order=order)
      if ratings:
        return jsonify({'response': ratings}), 200
      else:
        return jsonify({'error': 'No ratings found for this event'}), 204
        
  except ValueError as e:
    return jsonify({'error': str(e)}), 400
  except Exception as e:
    return jsonify({'error': 'Internal server error', 'details': str(e)}), 500
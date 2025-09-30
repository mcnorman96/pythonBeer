from flask import Blueprint, request, jsonify
from services.beer_services import BeerService
from utils.utils import get_json_data, get_valid_user_id

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

newBeer = Blueprint('new_beer', __name__)
@newBeer.route('/new', methods=['POST'])
def new_beer():
    try:
      get_valid_user_id()  # Ensure user is authenticated
      data = get_json_data()
      name = data.get('name')
      description = data.get('description')
      brewery = data.get('brewery')
      beer_type = data.get('type')

      if name and description and brewery and beer_type:
          beer = BeerService.create(
              name, 
              description, 
              brewery, 
              beer_type
          )

          return jsonify({
              'message': 'Beer created successfully', 
              'response': beer.to_dict()
              }), 201
      else:
          return jsonify({'error': 'Please fill out all fields.'}), 400
    except ValueError as e:
      return jsonify({'error': str(e)}), 400
    except Exception as e:
      return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


allBeers = Blueprint('all_beers', __name__)
@allBeers.route('/', methods=['GET'])
def all_beers():
    try:
        beers = BeerService.get_all()
        if beers:
            beers_list = [beer.to_dict() for beer in beers]
            return jsonify({'response': beers_list}), 200
        else:
            return jsonify({'response': []}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
          

searchBeers = Blueprint('search_beers', __name__)
@searchBeers.route('/search', methods=['GET', 'POST'])
def search_beers():
  try: 
    search_query = request.args.get('s', '')
    if search_query:
      beers = BeerService.search_by_name(search_query)
      logger.debug(f"Search query: {search_query}, Result: {beers}")
      if beers:
        return jsonify({'response': beers}), 200
      else:
        return jsonify({'message': 'No beers found'}), 204
    else:
      return jsonify({'message': 'No search query provided'}), 400
     
  except ValueError as e:
      return jsonify({'error': str(e)}), 400
  except Exception as e:
      return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

  


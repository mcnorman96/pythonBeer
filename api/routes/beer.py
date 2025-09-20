from flask import Blueprint, request, jsonify
from services.beer_services import BeerService
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

newBeer = Blueprint('new_beer', __name__)
@newBeer.route('/new', methods=['GET', 'POST'])
def new_beer():
	if request.method == 'POST' and all(k in request.form for k in ('name', 'description', 'brewery', 'type')):
          name = request.form['name']
          description = request.form['description']
          brewery = request.form['brewery']
          beer_type = request.form['type']

          try:
            if name and description:
                beer = BeerService.create(
                   name, 
                   description, 
                   brewery, 
                   beer_type
                )

                return jsonify({
                   'message': 'Beer created successfully', 
                   'beer': beer.to_dict()
                   }), 201
            else:
                return jsonify({'error': 'Please fill out all fields.'}), 400
          except ValueError as e:
            return jsonify({'error': str(e)}), 400


allBeers = Blueprint('all_beers', __name__)
@allBeers.route('/', methods=['GET', 'POST'])
def all_beers():
    if request.method == 'GET':
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
  search_query = request.args.get('s', '')
  if search_query:
    beers = BeerService.search_by_name(search_query)
    logger.debug(f"Search query: {search_query}, Result: {beers}")
    if beers:
      return jsonify(beers), 200
    else:
      return jsonify({'message': 'No beers found'}), 404
  else:
    return jsonify({'message': 'No search query provided'}), 400


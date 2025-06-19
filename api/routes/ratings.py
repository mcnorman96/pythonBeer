from flask import Blueprint, request, redirect, url_for, session, flash, jsonify
from app import db
from schemas.ratings import Ratings

newRatings = Blueprint('new_ratings', __name__)
@newRatings.route('/new', methods=['GET', 'POST'])
def new_ratings():
  if request.method == 'POST' and all(k in request.form for k in ('event_id', 'user_id', 'beer_id', 'taste', 'aftertaste', 'smell', 'design', 'score')):
    event_id = request.form['event_id']
    user_id = request.form['user_id']
    beer_id = request.form['beer_id']
    taste = request.form['taste']
    aftertaste = request.form['aftertaste']
    smell = request.form['smell']
    design = request.form['design']
    score = request.form['score']
    
    try:
      if event_id and user_id and beer_id and taste and aftertaste and smell and design and score:
        Ratings.create(event_id, user_id, beer_id, taste, aftertaste, smell, design, score)
        return jsonify({'message': 'Ratings created succesfully'}), 201
      else:
        return jsonify({'error': 'Please fill out all fields.'}), 400
    except ValueError as e:
      return jsonify({'error': str(e)}), 400
  else:
    return jsonify({'error': 'Please fill out all fields.'}), 400


allRatings = Blueprint('all_ratings', __name__)
@allRatings.route('/', methods=['GET', 'POST'])
def all_ratings():
  if request.method == 'GET':
    try:
      ratings = Ratings.get_all()
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
      ratings = Ratings.get_toplist()
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
        ratings = Ratings.get_toplist_by_event(event_id)
        if (ratings):
          return jsonify({'response': ratings}), 200
        else: 
          return jsonify({'error': 'No ratings found'}), 400
    except ValueError as e:
      return jsonify({'error': str(e)}), 400
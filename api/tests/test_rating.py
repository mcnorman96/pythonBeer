from models.rating import Rating
from datetime import datetime
from app import app
from werkzeug.exceptions import Unauthorized
import pytest

def test_create_rating():
    rating = Rating(id=1, event_id=2, beer_id=3, user_id=4, taste=5, aftertaste=6, smell=7, design=8, score=9)
    expected = {
        'id': 1,
        'event_id': 2,
        'beer_id': 3,
        'user_id': 4,
        'taste': 5,
        'aftertaste': 6,
        'smell': 7,
        'design': 8,
        'score': 9
    }
    assert rating.to_dict() == expected

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

## New Rating Tests
def test_new_rating_success(client, mocker):
    # Mock authentication and RatingService.create
    mocker.patch('routes.ratings.get_valid_user_id', return_value=1)
    mock_rating = mocker.Mock()
    mock_rating.to_dict.return_value = {'id': 1, 'event_id': 2, 'beer_id': 3, 'user_id': 4, 'taste': 5, 'aftertaste': 6, 'smell': 7, 'design': 8, 'score': 9}
    mocker.patch('services.ratings_service.RatingsService.create', return_value=mock_rating)

    response = client.post('/ratings/new', json={
        'event_id': 2,
        'beer_id': 3,
        'user_id': 4,
        'taste': 5,
        'aftertaste': 6,
        'smell': 7,
        'design': 8,
        'score': 9
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'Rating created successfully'

def test_new_rating_missing_fields(client, mocker):
    mocker.patch('routes.ratings.get_valid_user_id', return_value=1)
    response = client.post('/ratings/new', json={
        'event_id': 2,
        # Missing beer_id, user_id, taste, aftertaste, smell, design, score
    })
    assert response.status_code == 400

def test_new_rating_unauthorized(client, mocker):
    mocker.patch('routes.ratings.get_valid_user_id', side_effect=Unauthorized())
    response = client.post('/ratings/new', json={
        'event_id': 2,
        'beer_id': 3,
        'user_id': 4,
        'taste': 5,
        'aftertaste': 6,
        'smell': 7,
        'design': 8,
        'score': 9
    })
    assert response.status_code == 401

## Get Rating by ID Tests
def test_get_rating_by_id_success(client, mocker):
    mock_rating = {'id': 1, 'event_id': 2, 'beer_id': 3, 'user_id': 4, 'taste': 5, 'aftertaste': 6, 'smell': 7, 'design': 8, 'score': 9}
    mocker.patch('services.ratings_service.RatingsService.getRating', return_value=mock_rating)
    mocker.patch('routes.ratings.get_valid_user_id', return_value=4)
    response = client.get('/ratings/getRating', query_string={'event_id': 1, 'beer_id': 2})

    assert response.status_code == 200
    assert response.get_json()['response'] == mock_rating

def test_get_rating_by_id_not_found(client, mocker):
    mocker.patch('services.ratings_service.RatingsService.getRating', return_value=None)
    mocker.patch('routes.ratings.get_valid_user_id', return_value=4)
    response = client.get('/ratings/getRating', query_string={'event_id': 1, 'beer_id': 2})

    assert response.status_code == 400
    assert response.get_json()['error'] == 'No rating found'

def test_get_rating_by_id_unauthorized(client, mocker):
    mocker.patch('routes.ratings.get_valid_user_id', side_effect=Unauthorized())
    response = client.get('/ratings/getRating', query_string={'event_id': 1, 'beer_id': 2})

    assert response.status_code == 401

## Get All Ratings for beer Tests
def test_get_all_ratings_for_beer_success(client, mocker):
    mock_ratings = [
        {'id': 1, 'event_id': 2, 'beer_id': 3, 'user_id': 4, 'taste': 5, 'aftertaste': 6, 'smell': 7, 'design': 8, 'score': 9},
        {'id': 2, 'event_id': 2, 'beer_id': 3, 'user_id': 5, 'taste': 6, 'aftertaste': 7, 'smell': 8, 'design': 9, 'score': 10}
    ]
    mocker.patch('services.ratings_service.RatingsService.getAllRatingsForBeer', return_value=mock_ratings)
    response = client.get('/ratings/all', query_string={'beer_id': 3, 'event_id': 2})

    assert response.status_code == 200
    assert response.get_json()['response'] == mock_ratings

def test_get_all_ratings_for_beer_no_ratings(client, mocker):
    mocker.patch('services.ratings_service.RatingsService.getAllRatingsForBeer', return_value=[])
    response = client.get('/ratings/all', query_string={'beer_id': 3, 'event_id': 2})

    assert response.status_code == 200
    assert response.get_json()['response'] == []

def test_get_all_ratings_for_beer_error(client, mocker):
    mocker.patch('services.ratings_service.RatingsService.getAllRatingsForBeer', side_effect=ValueError('DB error'))
    response = client.get('/ratings/all', query_string={'beer_id': 3, 'event_id': 2})

    assert response.status_code == 400
    assert 'DB error' in response.get_json()['error']

## Toplist Tests
def test_toplist_success(client, mocker):
    mock_toplist = [
        {'beer_id': 1, 'average_score': 9.5},
        {'beer_id': 2, 'average_score': 9.0}
    ]
    mocker.patch('services.ratings_service.RatingsService.get_toplist', return_value=mock_toplist)
    response = client.get('/ratings/toplist')

    assert response.status_code == 200
    assert response.get_json()['response'] == mock_toplist

def test_toplist_no_ratings(client, mocker):
    mocker.patch('services.ratings_service.RatingsService.get_toplist', return_value=[])
    response = client.get('/ratings/toplist')

    assert response.status_code == 400
    assert response.get_json()['error'] == 'No ratings found'

def test_toplist_error(client, mocker):
    mocker.patch('services.ratings_service.RatingsService.get_toplist', side_effect=ValueError('DB error'))
    response = client.get('/ratings/toplist', query_string={'event_id': 2})

    assert response.status_code == 400
    assert 'DB error' in response.get_json()['error']


## Toplist by Event ID Tests
def test_toplist_by_event_id_success(client, mocker):
    mock_toplist = [
        {'beer_id': 1, 'average_score': 9.5},
        {'beer_id': 2, 'average_score': 9.0}
    ]
    mocker.patch('services.ratings_service.RatingsService.get_toplist_by_event', return_value=mock_toplist)
    response = client.get('/ratings/toplist/1')

    assert response.status_code == 200
    assert response.get_json()['response'] == mock_toplist

def test_toplist_by_event_id_no_ratings(client, mocker):
    mocker.patch('services.ratings_service.RatingsService.get_toplist_by_event', return_value=[])
    response = client.get('/ratings/toplist/4')

    assert response.status_code == 200
    assert response.get_json()['response'] == []

def test_toplist_by_event_id_error(client, mocker):
    mocker.patch('services.ratings_service.RatingsService.get_toplist_by_event', side_effect=ValueError('DB error'))
    response = client.get('/ratings/toplist/1')

    assert response.status_code == 400
    assert 'DB error' in response.get_json()['error']

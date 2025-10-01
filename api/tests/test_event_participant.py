from models.event_participant import EventParticipant
from datetime import datetime
from app import app
from werkzeug.exceptions import Unauthorized
import pytest

def test_create_event_participant():
    ep = EventParticipant(id=1, event_id=2, user_id=3)
    assert ep.id == 1
    assert ep.event_id == 2
    assert ep.user_id == 3


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_new_event_participant_success(client, mocker):
    # Mock authentication and EventParticipantService.create
    mocker.patch('routes.event_participant.get_valid_user_id', return_value=1)
    mock_event_participant = mocker.Mock()
    mock_event_participant.to_dict.return_value = {'id': 1, 'event_id': 2, 'user_id': 3}
    mocker.patch('services.event_participant_service.EventParticipantService.create', return_value=mock_event_participant)

    response = client.post('/events/2/participants/new')

    assert response.status_code == 201
    assert response.get_json()['message'] == 'Event participant created successfully'


def test_new_event_participant_unauthorized(client, mocker):
    mocker.patch('routes.event_participant.get_valid_user_id', side_effect=Unauthorized())
    response = client.post('/events/2/participants/new')

    assert response.status_code == 401


def test_all_event_participant_success(client, mocker):
    mock_event_participants = [
        {'id': 1, 'event_id': 2, 'user_id': 3},
        {'id': 2, 'event_id': 2, 'user_id': 4}
    ]
    mocker.patch('services.event_participant_service.EventParticipantService.get_all_users_in_event', return_value=mock_event_participants)

    response = client.get('/events/2/participants/')

    assert response.status_code == 200
    assert response.get_json()['response'] == mock_event_participants


def test_all_event_participant_no_participants(client, mocker):
    mocker.patch('services.event_participant_service.EventParticipantService.get_all_users_in_event', return_value=[])

    response = client.get('/events/2/participants/')

    assert response.status_code == 400
    assert response.get_json()['error'] == 'No event participant found'
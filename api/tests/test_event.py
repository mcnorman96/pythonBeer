from models.event import Event
from datetime import datetime
from app import app
from werkzeug.exceptions import Unauthorized
import pytest


def test_create_event():
    start = datetime(2024, 1, 1, 12, 0)
    end = datetime(2024, 1, 2, 12, 0)
    event = Event(id=1, name="Party", start_date=start, end_date=end, description="Fun")
    expected = {
        "id": 1,
        "name": "Party",
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "description": "Fun",
    }
    assert event.to_dict() == expected


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_new_event_success(client, mocker):
    # Mock authentication and EventService.create
    mocker.patch("routes.event.get_valid_user_id", return_value=1)
    mock_event = mocker.Mock()
    mock_event.to_dict.return_value = {"id": 1, "name": "Test Event"}
    mocker.patch("services.event_services.EventService.create", return_value=mock_event)

    response = client.post(
        "/events/new", json={"name": "Test Event", "description": "A test event"}
    )
    assert response.status_code == 201
    assert response.get_json()["message"] == "Events created successfully"


def test_new_event_missing_fields(client, mocker):
    mocker.patch("routes.event.get_valid_user_id", return_value=1)
    response = client.post(
        "/events/new",
        json={
            "name": "Test Event",
            # Missing description
        },
    )
    assert response.status_code == 400


def test_new_event_unauthorized(client, mocker):
    mocker.patch("routes.event.get_valid_user_id", side_effect=Unauthorized())
    response = client.post(
        "/events/new", json={"name": "Test Event", "description": "A test event"}
    )
    assert response.status_code == 401


def test_all_events_success(client, mocker):
    mock_events = [{"id": 1, "name": "Event 1"}, {"id": 2, "name": "Event 2"}]
    mocker.patch(
        "services.event_services.EventService.get_all", return_value=mock_events
    )

    response = client.get("/events/")

    assert response.status_code == 200
    assert response.get_json()["response"] == mock_events


def test_all_events_no_events(client, mocker):
    mocker.patch("services.event_services.EventService.get_all", return_value=[])

    response = client.get("/events/")

    assert response.status_code == 400
    assert response.get_json()["error"] == "No events found"


def test_get_event_by_id_success(client, mocker):
    mock_event = {"id": 1, "name": "Event 1"}
    mocker.patch(
        "services.event_services.EventService.get_by_id", return_value=mock_event
    )

    response = client.get("/events/1")

    assert response.status_code == 200
    assert response.get_json()["response"] == mock_event


def test_get_event_by_id_not_found(client, mocker):
    mocker.patch("services.event_services.EventService.get_by_id", return_value=None)

    response = client.get("/events/999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Event not found"


def test_get_event_by_id_error(client, mocker):
    mocker.patch(
        "services.event_services.EventService.get_by_id",
        side_effect=ValueError("DB error"),
    )

    response = client.get("/events/1")

    assert response.status_code == 400
    assert response.get_json()["error"] == "DB error"

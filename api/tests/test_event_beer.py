from models.event_beer import EventBeer
from datetime import datetime
from app import app
from werkzeug.exceptions import Unauthorized
import pytest


def test_create_event_beer():
    added_at = datetime(2024, 1, 1, 12, 0)
    eb = EventBeer(id=1, event_id=2, beer_id=3, added_at=added_at)
    expected = {
        "id": 1,
        "event_id": 2,
        "beer_id": 3,
        "added_at": added_at,
    }
    assert eb.to_dict() == expected


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_new_event_beer_success(client, mocker):
    # Mock authentication and EventBeerService.create
    mocker.patch("routes.event_beer.get_valid_user_id", return_value=1)
    mock_event_beer = mocker.Mock()
    mock_event_beer.to_dict.return_value = {"id": 1, "event_id": 2, "beer_id": 3}
    mocker.patch(
        "services.event_beer_services.EventBeersService.create",
        return_value=mock_event_beer,
    )

    response = client.post("/events/2/beers", json={"beer_id": 3})
    assert response.status_code == 201
    assert response.get_json()["message"] == "Event beer created successfully"


def test_new_event_beer_missing_fields(client, mocker):
    mocker.patch("routes.event_beer.get_valid_user_id", return_value=1)
    response = client.post(
        "/events/2/beers",
        json={
            # Missing beer_id
        },
    )
    assert response.status_code == 400


def test_new_event_beer_unauthorized(client, mocker):
    mocker.patch("routes.event_beer.get_valid_user_id", side_effect=Unauthorized())
    response = client.post("/events/2/beers", json={"beer_id": 3})

    assert response.status_code == 401

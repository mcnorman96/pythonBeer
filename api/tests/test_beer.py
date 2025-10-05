from models.beer import Beer
from app import app
from werkzeug.exceptions import Unauthorized
import pytest


def test_create_beer():
    beer = Beer(id=1, name="Test", description="Desc", brewery="Brew", type="Lager")
    expected = {
        "id": 1,
        "name": "Test",
        "description": "Desc",
        "brewery": "Brew",
        "type": "Lager",
    }
    assert beer.to_dict() == expected


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_new_beer_success(client, mocker):
    # Mock authentication and BeerService.create
    mocker.patch("routes.beer.get_valid_user_id", return_value=1)
    mock_beer = mocker.Mock()
    mock_beer.to_dict.return_value = {"id": 1, "name": "Test Beer"}
    mocker.patch("services.beer_services.BeerService.create", return_value=mock_beer)

    response = client.post(
        "/beer/new",
        json={
            "name": "Test Beer",
            "description": "A test beer",
            "brewery": "Test Brewery",
            "type": "Ale",
        },
    )
    assert response.status_code == 201
    assert response.get_json()["message"] == "Beer created successfully"


def test_new_beer_missing_fields(client, mocker):
    mocker.patch("routes.beer.get_valid_user_id", return_value=1)
    response = client.post(
        "/beer/new",
        json={
            "name": "Test Beer",
            # Missing description, brewery, type
        },
    )
    assert response.status_code == 400


def test_new_beer_unauthorized(client, mocker):
    mocker.patch("routes.beer.get_valid_user_id", side_effect=Unauthorized())
    response = client.post(
        "/beer/new",
        json={
            "name": "Test Beer",
            "description": "A test beer",
            "brewery": "Test Brewery",
            "type": "Ale",
        },
    )
    assert response.status_code == 401


def test_all_beers(client, mocker):
    mock_beer1 = mocker.Mock()
    mock_beer1.to_dict.return_value = {"id": 1, "name": "Beer1"}
    mock_beer2 = mocker.Mock()
    mock_beer2.to_dict.return_value = {"id": 2, "name": "Beer2"}
    mocker.patch(
        "services.beer_services.BeerService.get_all",
        return_value=[mock_beer1, mock_beer2],
    )

    response = client.get("/beer/")
    assert response.status_code == 200
    assert len(response.get_json()["response"]) == 2


def test_all_beers_empty(client, mocker):
    mocker.patch("services.beer_services.BeerService.get_all", return_value=[])

    response = client.get("/beer/")
    assert response.status_code == 200
    assert response.get_json()["response"] == []


def test_all_beers_error(client, mocker):
    mocker.patch(
        "services.beer_services.BeerService.get_all", side_effect=ValueError("DB error")
    )

    response = client.get("/beer/")
    assert response.status_code == 400
    assert "DB error" in response.get_json()["error"]


def test_search_beers(client, mocker):
    # Mock the service to return a list of dictionaries (as it actually does)
    mock_beer_list = [{"id": 1, "name": "Searched Beer"}]
    mocker.patch(
        "services.beer_services.BeerService.search_by_name", return_value=mock_beer_list
    )

    response = client.get("/beer/search", query_string={"s": "Searched"})
    assert response.status_code == 200
    assert len(response.get_json()["response"]) == 1


def test_search_beers_no_results(client, mocker):
    # Mock the service to return an empty list (as it actually does)
    mocker.patch("services.beer_services.BeerService.search_by_name", return_value=[])

    response = client.get("/beer/search", query_string={"s": "NoMatch"})
    assert response.status_code == 200


def test_search_beers_error(client, mocker):
    mocker.patch(
        "services.beer_services.BeerService.search_by_name",
        side_effect=ValueError("Search error"),
    )

    response = client.get("/beer/search", query_string={"s": "Error"})
    assert response.status_code == 400
    assert "Search error" in response.get_json()["error"]

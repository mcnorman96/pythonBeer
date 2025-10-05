from flask import Blueprint, request, jsonify
from services.beer_services import BeerService
from utils.utils import (
    get_json_data,
    get_valid_user_id,
    validate_fields,
    handle_exceptions,
    get_logger,
)

logger = get_logger(__name__)

beer_bp = Blueprint("beer", __name__)


@beer_bp.route("/new", methods=["POST"])
def new_beer():
    try:
        get_valid_user_id()  # Ensure user is authenticated
        data = get_json_data()
        valid, msg = validate_fields(data, ["name", "description", "brewery", "type"])
        if not valid:
            return jsonify({"error": msg}), 400

        beer = BeerService.create(
            data["name"], data["description"], data["brewery"], data["type"]
        )

        return (
            jsonify(
                {"message": "Beer created successfully", "response": beer.to_dict()}
            ),
            201,
        )

    except Exception as e:
        return handle_exceptions(e)


@beer_bp.route("/update", methods=["PUT"])
def update_beer():
    try:
        get_valid_user_id()  # Ensure user is authenticated
        data = get_json_data()
        valid, msg = validate_fields(
            data, ["id", "name", "description", "brewery", "type"]
        )
        if not valid:
            return jsonify({"error": msg}), 400

        beer = BeerService.update(
            data["id"], data["name"], data["description"], data["brewery"], data["type"]
        )

        return (
            jsonify(
                {"message": "Beer updated successfully", "response": beer.to_dict()}
            ),
            200,
        )

    except Exception as e:
        return handle_exceptions(e)


@beer_bp.route("/", methods=["GET"])
def all_beers():
    try:
        beers = BeerService.get_all()
        if not beers:
            return jsonify({"response": []}), 200

        beers_list = [beer.to_dict() for beer in beers]
        return jsonify({"response": beers_list}), 200

    except Exception as e:
        return handle_exceptions(e)


@beer_bp.route("/search", methods=["GET"])
def search_beers():
    try:
        search_query = request.args.get("s", "")

        if not search_query:
            return jsonify({"message": "No search query provided"}), 400

        beers = BeerService.search_by_name(search_query)
        if not beers:
            return jsonify({"response": []}), 200

        return jsonify({"response": beers}), 200

    except Exception as e:
        return handle_exceptions(e)

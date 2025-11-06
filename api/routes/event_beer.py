from flask import Blueprint, jsonify
from services.event_beer_services import EventBeersService
from utils.utils import (
    get_json_data,
    get_valid_user_id,
    validate_fields,
    get_logger,
    handle_exceptions,
)

logging = get_logger(__name__)

event_beer_bp = Blueprint("event_beer", __name__)


@event_beer_bp.route("/<int:event_id>/beers", methods=["POST"])
def new_event_beer(event_id):
    try:
        get_valid_user_id()  # Ensure user is authenticated
        data = get_json_data()
        valid, msg = validate_fields(data, ["beer_id"])
        if not valid:
            return jsonify({"error": msg}), 400

        beer_id = data.get("beer_id")
        if not event_id or not beer_id:
            return jsonify({"error": "unfulfilled.fields"}), 400

        EventBeersService.create(event_id, beer_id)
        return jsonify({"message": "beer.added.to.event"}), 201

    except Exception as e:
        return handle_exceptions(e)


@event_beer_bp.route("/<int:event_id>/beers/<int:beer_id>", methods=["DELETE"])
def delete_event_beer(event_id, beer_id):
    try:
        get_valid_user_id()  # Ensure user is authenticated
        if not event_id or not beer_id:
            return jsonify({"error": "unfulfilled.fields"}), 400

        EventBeersService.deleteSingleEventBeerForEvent(event_id, beer_id)
        return jsonify({"message": "beer.deleted.from.event"}), 201

    except Exception as e:
        return handle_exceptions(e)

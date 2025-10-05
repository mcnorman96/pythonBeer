from flask import Blueprint, request, jsonify
from services.ratings_service import RatingsService
from routes.auth import get_valid_user_id
from utils.utils import (
    get_json_data,
    get_valid_user_id,
    validate_fields,
    handle_exceptions,
    get_logger,
)

logger = get_logger(__name__)

ratings_bp = Blueprint("ratings", __name__)


@ratings_bp.route("/new", methods=["POST"])
def new_ratings():
    try:
        user_id = get_valid_user_id()
        data = get_json_data()
        valid, msg = validate_fields(
            data,
            ["event_id", "beer_id", "taste", "aftertaste", "smell", "design", "score"],
        )
        if not valid:
            return jsonify({"error": msg}), 400

        event_id = data.get("event_id")
        beer_id = data.get("beer_id")
        taste = data.get("taste")
        aftertaste = data.get("aftertaste")
        smell = data.get("smell")
        design = data.get("design")
        score = data.get("score")

        RatingsService.create(
            event_id, user_id, beer_id, taste, aftertaste, smell, design, score
        )
        return jsonify({"message": "Rating created successfully"}), 201

    except Exception as e:
        return handle_exceptions(e)


@ratings_bp.route("/getRating", methods=["GET"])
def get_ratings():
    try:
        user_id = get_valid_user_id()
        valid, msg = validate_fields(request.args, ["event_id", "beer_id"])
        if not valid:
            return jsonify({"error": msg}), 400

        event_id = request.args.get("event_id")
        beer_id = request.args.get("beer_id")

        getRating = RatingsService.getRating(event_id, user_id, beer_id)
        if not getRating:
            return jsonify({"error": "No rating found"}), 400

        return jsonify({"response": getRating}), 200

    except Exception as e:
        return handle_exceptions(e)


@ratings_bp.route("/all", methods=["GET"])
def get_all_ratings_for_beer():
    try:
        valid, msg = validate_fields(request.args, ["event_id", "beer_id"])
        if not valid:
            return jsonify({"error": msg}), 400

        event_id = request.args.get("event_id")
        beer_id = request.args.get("beer_id")

        getRating = RatingsService.getAllRatingsForBeer(event_id, beer_id)
        if not getRating:
            return jsonify({"response": []}), 200
        return jsonify({"response": getRating}), 200

    except Exception as e:
        return handle_exceptions(e)


@ratings_bp.route("/", methods=["GET", "POST"])
def all_ratings():
    try:
        ratings = RatingsService.get_all()
        if not ratings:
            return jsonify({"error": "No ratings found"}), 400

        return jsonify({"response": ratings}), 200

    except Exception as e:
        return handle_exceptions(e)


@ratings_bp.route("/toplist", methods=["GET", "POST"])
def toplist():
    try:
        ratings = RatingsService.get_toplist()
        if not ratings:
            return jsonify({"error": "No ratings found"}), 400

        return jsonify({"response": ratings}), 200

    except Exception as e:
        return handle_exceptions(e)


@ratings_bp.route("/toplist/<int:event_id>", methods=["GET", "POST"])
def toplist_by_event(event_id):
    try:
        sortby = request.args.get("sortby", "event_beer_id").lower()
        order = request.args.get("order", "asc").lower()

        ratings = RatingsService.get_toplist_by_event(
            event_id, sortby=sortby, order=order
        )
        if not ratings:
            return jsonify({"response": []}), 200

        return jsonify({"response": ratings}), 200

    except Exception as e:
        return handle_exceptions(e)

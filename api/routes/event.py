from flask import Blueprint, jsonify
from services.event_services import EventService
from utils.utils import (
    get_json_data,
    get_valid_user_id,
    validate_fields,
    handle_exceptions,
    get_logger,
)

logging = get_logger(__name__)

event_bp = Blueprint("events", __name__)


@event_bp.route("/new", methods=["POST"])
def new_events():
    try:
        get_valid_user_id()  # Ensure user is authenticated
        data = get_json_data()
        valid, msg = validate_fields(data, ["name", "description"])
        if not valid:
            return jsonify({"error": msg}), 400

        name = data.get("name")
        description = data.get("description")
        EventService.create(name, description)
        return jsonify({"message": "Events created successfully"}), 201

    except Exception as e:
        return handle_exceptions(e)


@event_bp.route("/", methods=["GET", "POST"])
def all_events():
    try:
        events = EventService.get_all()
        if not events:
            return jsonify({"error": "No events found"}), 400

        return jsonify({"response": events}), 200

    except Exception as e:
        return handle_exceptions(e)


@event_bp.route("/<int:event_id>", methods=["GET"])
def get_event_by_id(event_id):
    try:
        event = EventService.get_by_id(event_id)
        if not event:
            return jsonify({"error": "Event not found"}), 404

        return jsonify({"response": event}), 200

    except Exception as e:
        return handle_exceptions(e)


@event_bp.route("/<int:event_id>", methods=["PUT"])
def update_event(event_id):
    try:
        get_valid_user_id()  # Ensure user is authenticated
        data = get_json_data()
        valid, msg = validate_fields(data, ["name", "description"])
        if not valid:
            return jsonify({"error": msg}), 400

        name = data.get("name")
        description = data.get("description")
        updated_event = EventService.update(event_id, name, description)

        if not updated_event:
            return jsonify({"error": "Event not found"}), 404

        return (
            jsonify(
                {
                    "message": "Event updated successfully",
                    "response": updated_event,
                }
            ),
            200,
        )

    except Exception as e:
        return handle_exceptions(e)


@event_bp.route("/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    try:
        get_valid_user_id()  # Ensure user is authenticated
        deleted = EventService.delete(event_id)
        if not deleted:
            return jsonify({"error": "Event not found"}), 404

        return jsonify({"message": "Event deleted successfully"}), 200

    except Exception as e:
        return handle_exceptions(e)

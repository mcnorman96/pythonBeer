from flask import Blueprint, request, jsonify
from utils.utils import get_json_data, get_valid_user_id
from services.event_participant_service import EventParticipantService
from werkzeug.exceptions import HTTPException

newEventParticipant = Blueprint("new_event_participant", __name__)


@newEventParticipant.route("/<int:event_id>/participants/new", methods=["POST"])
def new_event_participant(event_id):
    try:
        user_id = get_valid_user_id()  # Ensure user is authenticated

        if event_id and user_id:
            EventParticipantService.create(event_id, user_id)
            return jsonify({"message": "Event participant created successfully"}), 201
        else:
            return jsonify({"error": "Please fill out all fields."}), 400

    except HTTPException as http_exc:
        raise http_exc
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


allEventParticipant = Blueprint("all_event_participant", __name__)


@allEventParticipant.route("/<int:event_id>/participants/", methods=["GET", "POST"])
def all_event_participant(event_id):
    try:
        events = EventParticipantService.get_all_users_in_event(event_id)
        if events:
            return jsonify({"response": events}), 200
        else:
            return jsonify({"error": "No event participant found"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

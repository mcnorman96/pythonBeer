from flask import Blueprint, jsonify
from services.event_participant_service import EventParticipantService
from utils.utils import get_valid_user_id, handle_exceptions, get_logger

logging = get_logger(__name__)

event_participant_bp = Blueprint("event_participant", __name__)


@event_participant_bp.route("/<int:event_id>/participants/new", methods=["POST"])
def new_event_participant(event_id):
    try:
        user_id = get_valid_user_id()  # Ensure user is authenticated
        EventParticipantService.create(event_id, user_id)
        return jsonify({"message": "Event participant created successfully"}), 201

    except Exception as e:
        return handle_exceptions(e)


@event_participant_bp.route("/<int:event_id>/participants/", methods=["GET", "POST"])
def all_event_participant(event_id):
    try:
        eventParticipants = EventParticipantService.get_all_users_in_event(event_id)
        if not eventParticipants:
            return jsonify({"error": "No event participant found"}), 400

        return jsonify({"response": eventParticipants}), 200

    except Exception as e:
        return handle_exceptions(e)

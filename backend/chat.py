from flask import Blueprint, request, jsonify
from backend.models import mongo
from backend.auth import token_required
from datetime import datetime
from bson.objectid import ObjectId

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/<trip_id>/messages", methods=["POST"])
@token_required
def add_message(current_user, trip_id):
    data = request.get_json()
    message = data.get("message")
    if not message:
        return jsonify({"error": "Invalid input"}), 400
    mongo.db.itineraries.update_one(
        {"_id": ObjectId(trip_id)},
        {
            "$push": {
                "chat_logs": {
                    "user_id": current_user["_id"],
                    "message": message,
                    "timestamp": datetime.utcnow(),
                }
            }
        },
        upsert=True,
    )
    return jsonify({"message": "Message added"}), 201


@chat_bp.route("/<trip_id>/polls", methods=["POST"])
@token_required
def create_poll(current_user, trip_id):
    data = request.get_json()
    question = data.get("question")
    options = data.get("options")
    if not question or not options:
        return jsonify({"error": "Invalid input"}), 400
    poll = {"question": question, "options": options, "votes": []}
    mongo.db.itineraries.update_one(
        {"_id": ObjectId(trip_id)}, {"$push": {"polls": poll}}, upsert=True
    )
    return jsonify({"message": "Poll created"}), 201


@chat_bp.route("/<trip_id>/polls/<poll_id>/vote", methods=["POST"])
@token_required
def vote_poll(current_user, trip_id, poll_id):
    data = request.get_json()
    option = data.get("option")
    if not option:
        return jsonify({"error": "Invalid input"}), 400
    mongo.db.itineraries.update_one(
        {"_id": ObjectId(trip_id), "polls._id": ObjectId(poll_id)},
        {
            "$push": {
                "polls.$.votes": {"user_id": current_user["_id"], "option": option}
            }
        },
    )
    return jsonify({"message": "Vote added"}), 201

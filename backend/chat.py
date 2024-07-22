from flask import Blueprint, request, jsonify
from backend.models import mongo
from backend.auth import token_required
from datetime import datetime
from bson.objectid import ObjectId

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/<trip_id>/messages", methods=["POST"])
@token_required
def add_message(current_user, trip_id):
    data = request.form
    message = data.get("message")
    if not message:
        return jsonify({"error": "Invalid input"}), 400
    mongo.db.itineraries.update_one(
        {"_id": ObjectId(trip_id)},
        {
            "$push": {
                "chat_logs": {
                    "user_id": current_user["_id"],
                    "username": current_user["username"],  # Add username to chat log
                    "message": message,
                    "timestamp": datetime.utcnow(),
                }
            }
        },
        upsert=True,
    )
    return jsonify({"message": "Message added"}), 201


@chat_bp.route("/<trip_id>/messages", methods=["GET"])
@token_required
def get_messages(current_user, trip_id):
    itinerary = mongo.db.itineraries.find_one({"_id": ObjectId(trip_id)})
    if not itinerary:
        return jsonify({"error": "Trip not found"}), 404
    return jsonify(itinerary["chat_logs"]), 200

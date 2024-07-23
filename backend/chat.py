# Chat.py
import logging
from flask import Blueprint, request, jsonify
from backend.models import mongo
from backend.auth import token_required
from datetime import datetime
from bson.objectid import ObjectId

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

chat_bp = Blueprint("chat", __name__)


def serialize_chat_log(log):
    if "_id" in log:
        log["_id"] = str(log["_id"])
    log["user_id"] = str(log["user_id"])
    log["timestamp"] = log["timestamp"].isoformat()
    return log


@chat_bp.route("/<trip_id>/messages", methods=["POST"])
@token_required
def add_message(current_user, trip_id):
    data = request.form
    message = data.get("message")
    if not message:
        return jsonify({"error": "Invalid input"}), 400

    itinerary = mongo.db.itineraries.find_one({"_id": ObjectId(trip_id)})
    if not itinerary:
        return jsonify({"error": "Itinerary not found"}), 404

    chatroom_id = itinerary["chatroom_id"]

    # Log the message before adding it to the database
    logger.info(f"Adding message: {message} for chatroom_id: {chatroom_id}")

    mongo.db.chatrooms.update_one(
        {"_id": ObjectId(chatroom_id)},
        {
            "$push": {
                "chat_logs": {
                    "user_id": current_user["_id"],
                    "username": current_user["username"],
                    "message": message,
                    "timestamp": datetime.utcnow(),
                }
            }
        },
        upsert=True,
    )

    # Verify the update
    chatroom = mongo.db.chatrooms.find_one({"_id": ObjectId(chatroom_id)})
    logger.info(f"Chatroom after update: {chatroom}")

    return (
        jsonify({"message": "Message added", "username": current_user["username"]}),
        201,
    )


@chat_bp.route("/<trip_id>/messages", methods=["GET"])
@token_required
def get_messages(current_user, trip_id):
    itinerary = mongo.db.itineraries.find_one({"_id": ObjectId(trip_id)})
    if not itinerary:
        return jsonify({"error": "Itinerary not found"}), 404

    chatroom_id = itinerary["chatroom_id"]
    chatroom = mongo.db.chatrooms.find_one({"_id": ObjectId(chatroom_id)})
    if not chatroom:
        return jsonify({"error": "Chatroom not found"}), 404

    chat_logs = [serialize_chat_log(log) for log in chatroom["chat_logs"]]

    # Log the retrieved messages
    logger.info(f"Retrieved messages for chatroom_id: {chatroom_id} - {chat_logs}")

    return jsonify(chat_logs), 200

# Itinerary.py
from flask import Blueprint, request, jsonify, redirect, url_for
from backend.models import mongo
from backend.auth import token_required
from datetime import datetime
from bson.objectid import ObjectId

itinerary_bp = Blueprint("itinerary", __name__)


@itinerary_bp.route("/<trip_id>/items", methods=["POST"])
@token_required
def add_itinerary_item(current_user, trip_id):
    data = request.form
    activity = data.get("activity")
    location = data.get("location")
    time = data.get("time")
    notes = data.get("notes")
    if not activity or not location or not time:
        return jsonify({"error": "Invalid input"}), 400
    item = {
        "activity": activity,
        "location": location,
        "time": datetime.fromisoformat(time),
        "notes": notes,
    }
    itinerary = mongo.db.itineraries.find_one({"_id": ObjectId(trip_id)})
    if not itinerary:
        return jsonify({"error": "Trip not found"}), 404

    mongo.db.itineraries.update_one(
        {"_id": ObjectId(trip_id)}, {"$push": {"itinerary": item}}, upsert=True
    )
    return redirect(url_for("trip_detail", trip_id=trip_id))


@itinerary_bp.route("/new", methods=["POST"])
@token_required
def create_itinerary(current_user):
    data = request.form
    trip_name = data.get("trip_name")
    users = data.getlist("users")  # Assuming 'users' is a list of user IDs
    if not trip_name or not users:
        return jsonify({"error": "Invalid input"}), 400

    # Create chatroom
    chatroom_id = mongo.db.chatrooms.insert_one({"chat_logs": []}).inserted_id

    itinerary = {
        "trip_name": trip_name,
        "users": [ObjectId(user_id) for user_id in users],
        "chatroom_id": chatroom_id,
        "itinerary": [],
    }

    itinerary_id = mongo.db.itineraries.insert_one(itinerary).inserted_id

    # Update each user with the new itinerary
    for user_id in users:
        mongo.db.users.update_one(
            {"_id": ObjectId(user_id)}, {"$push": {"profile.past_trips": itinerary}}
        )

    return redirect(url_for("trip_detail", trip_id=itinerary_id))

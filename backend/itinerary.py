from flask import Blueprint, request, jsonify
from backend.models import mongo
from backend.auth import token_required
from datetime import datetime
from bson.objectid import ObjectId

itinerary_bp = Blueprint("itinerary", __name__)


@itinerary_bp.route("/<trip_id>/items", methods=["POST"])
@token_required
def add_itinerary_item(current_user, trip_id):
    data = request.get_json()
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
    mongo.db.itineraries.update_one(
        {"_id": ObjectId(trip_id)}, {"$push": {"itinerary": item}}, upsert=True
    )
    return jsonify({"message": "Itinerary item added"}), 201


@itinerary_bp.route("/<trip_id>/items", methods=["GET"])
@token_required
def get_itinerary(current_user, trip_id):
    itinerary = mongo.db.itineraries.find_one({"_id": ObjectId(trip_id)})
    if itinerary and current_user["_id"] in itinerary["users"]:
        return jsonify(itinerary["itinerary"]), 200
    return jsonify({"error": "Access denied"}), 403


@itinerary_bp.route("/<trip_id>/share", methods=["POST"])
@token_required
def share_itinerary(current_user, trip_id):
    data = request.get_json()
    email = data.get("email")
    if not email:
        return jsonify({"error": "Invalid input"}), 400
    user = mongo.db.users.find_one({"email": email})
    if not user:
        return jsonify({"error": "User not found"}), 404
    mongo.db.itineraries.update_one(
        {"_id": ObjectId(trip_id)}, {"$addToSet": {"users": user["_id"]}}
    )
    return jsonify({"message": "Itinerary shared"}), 200


@itinerary_bp.route("/create", methods=["POST"])
@token_required
def create_itinerary(current_user):
    data = request.get_json()
    trip_name = data.get("trip_name")
    if not trip_name:
        return jsonify({"error": "Trip name is required"}), 400
    itinerary = {
        "trip_name": trip_name,
        "users": [current_user["_id"]],
        "itinerary": [],
        "chat_logs": [],
    }
    result = mongo.db.itineraries.insert_one(itinerary)
    return (
        jsonify({"message": "Itinerary created", "trip_id": str(result.inserted_id)}),
        201,
    )

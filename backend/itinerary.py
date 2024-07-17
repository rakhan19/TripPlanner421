from flask import Blueprint, request, jsonify
from models import mongo
from auth import token_required
from datetime import datetime

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
        {"trip_id": trip_id}, {"$push": {"itinerary": item}}, upsert=True
    )
    return jsonify({"message": "Itinerary item added"}), 201


@itinerary_bp.route("/<trip_id>/items", methods=["GET"])
@token_required
def get_itinerary(current_user, trip_id):
    itinerary = mongo.db.itineraries.find_one({"trip_id": trip_id})
    return jsonify(itinerary["itinerary"]), 200

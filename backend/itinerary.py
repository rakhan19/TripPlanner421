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
    mongo.db.itineraries.update_one(
        {"_id": ObjectId(trip_id)}, {"$push": {"itinerary": item}}, upsert=True
    )
    return redirect(url_for("trip_detail", trip_id=trip_id))

# Itinerary.py
from flask import Blueprint, request, jsonify, redirect, url_for, flash
from backend.models import mongo
from backend.auth import token_required
from datetime import datetime
from bson.objectid import ObjectId
import uuid

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
    return redirect(url_for("itinerary", trip_id=trip_id))


@itinerary_bp.route("/new", methods=["POST"])
@token_required
def create_itinerary(current_user):
    trip_name = request.form.get("trip_name")
    temp_users=[current_user]

    user_ids = []

    for user in temp_users:
        existing_user = mongo.db.users.find_one({"username": user["username"]})
        user_ids.append(existing_user["_id"])

#    users = data.getlist("users")
    if not trip_name:
        return jsonify({"error": "Invalid input"}), 400
    
    existing_itinerary = mongo.db.itineraries.find_one({"trip_name": trip_name})
    if existing_itinerary:
        flash("Trip already exists!", "warning")
        return redirect(
         url_for("trip_detail", trip_id=existing_itinerary["_id"])
        )
    
    # Create chatroom
    chatroom_id = mongo.db.chatrooms.insert_one({"chat_logs": []}).inserted_id
    budget = [
    {
        "user_id": user_id,
        "flight": 0,
        "hotel": 0,
        "food": 0,
        "transport": 0,
        "activities": 0,
        "spending": 0
    } for user_id in user_ids
    ] 
    itinerary = {
        "trip_name": trip_name,
        "users": [ObjectId(user_id) for user_id in user_ids],
        "chatroom_id": chatroom_id,
        "itinerary": [],
        "budget" : budget
    }

    itinerary_id = mongo.db.itineraries.insert_one(itinerary).inserted_id

    # Update each user with the new itinerary
    for user_id in user_ids:
        mongo.db.users.update_one(
            {"_id": ObjectId(user_id)}, {"$push": {"profile.past_trips": itinerary}}
        )
    flash("Trip created successfully!", "success")
    return redirect(
         url_for("trip_detail", trip_id=itinerary_id)
    )


    # return redirect(
    #     url_for("trip_detail", trip_id=itinerary_id, invite_code=invite_code)
    # )


@itinerary_bp.route("/join/<chatroom_id>", methods=["GET"])
@token_required
def join_itinerary(current_user, chatroom_id):
    itinerary = mongo.db.itineraries.find_one({"chatroom_id": ObjectId(chatroom_id)})
    if not itinerary:
        return jsonify({"error": "Invalid chatroom ID"}), 405

    if ObjectId(current_user["_id"]) not in itinerary["users"]:
        mongo.db.itineraries.update_one(
            {"_id": itinerary["_id"]},
            {"$push": {"users": ObjectId(current_user["_id"])}},
        )
        return jsonify({"message": "You have been added to the itinerary"}), 200
    else:
        return jsonify({"message": "You are already part of this itinerary"}), 400


def get_invite_link(chatroom_id):
    base_url = "http://127.0.0.1:5000/itinerary/join/"
    return f"{base_url}{chatroom_id}"

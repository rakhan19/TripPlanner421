from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from werkzeug.security import generate_password_hash
from flask_cors import CORS
from dotenv import load_dotenv
import os
from datetime import datetime
from bson.objectid import ObjectId
import jwt
from backend.itinerary import generate_invite_code

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

from backend.models import mongo

mongo.init_app(app)

from backend.auth import auth_bp, token_required
from backend.chat import chat_bp
from backend.itinerary import itinerary_bp
from backend.budget import budget_bp
from jwt.exceptions import ExpiredSignatureError

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(chat_bp, url_prefix="/chat")
app.register_blueprint(itinerary_bp, url_prefix="/itinerary")
app.register_blueprint(budget_bp, url_prefix="/budget")


@app.route("/")
def welcome():
    print("Welcome route accessed")  # Debugging print statement
    token = request.cookies.get("x-access-token")
    if token:
        try:
            print("User already logged in")
            data = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
            username = data["username"]
            print(f"Token username: {username}")  # Debugging print statement
            return redirect(url_for("mainpage", username=username))
        except ExpiredSignatureError:
            print("Token has expired")  # Debugging print statement
            return redirect(
                url_for("auth.login")
            )  # Redirect to login page or handle accordingly

    return render_template(
        "welcome.html", google_maps_api_key=os.getenv("GOOGLEMAPS_API_KEY")
    )


@app.route("/admit")
def admit():
    return render_template(
        "admit.html", google_maps_api_key=os.getenv("GOOGLEMAPS_API_KEY")
    )


@app.route("/signup")
def signup():
    return render_template(
        "signup.html", google_maps_api_key=os.getenv("GOOGLEMAPS_API_KEY")
    )


@app.route("/main")
def main():
    print("Main route accessed")  # Debugging print statement
    return render_template(
        "mainpage.html", google_maps_api_key=os.getenv("GOOGLEMAPS_API_KEY")
    )


@app.route("/trip")
def trip(username, trip_name):
    return render_template(
        "trip.html", google_maps_api_key=os.getenv("GOOGLEMAPS_API_KEY")
    )


@app.route("/trip/<trip_id>/chat")
@token_required
def trip_chat(current_user, trip_id):
    trip = mongo.db.itineraries.find_one({"_id": ObjectId(trip_id)})
    if not trip:
        return jsonify({"error": "Trip not found"}), 404
    return render_template(
        "trip_chat.html",
        trip=trip,
        user=current_user,
        google_maps_api_key=os.getenv("GOOGLEMAPS_API_KEY"),
    )


@app.route("/trip/<trip_id>/budget")
@token_required
def budget(current_user, trip_id):
    trip = mongo.db.itineraries.find_one({"_id": ObjectId(trip_id)})
    user_ids = trip["users"]
    user_budgets = []
    for budget in trip["budget"]:
        user = mongo.db.users.find_one({"_id": budget["user_id"]})
        if user:
            user_budget = {"username": user["username"], "budget": budget}
            user_budgets.append(user_budget)

    return render_template(
        "budget.html",
        trip=trip,
        user_budgets=user_budgets,
        user=current_user,
        google_maps_api_key=os.getenv("GOOGLEMAPS_API_KEY"),
    )


@app.route("/trip/<trip_id>/itinerary")
@token_required
def itinerary(current_user, trip_id):
    trip = mongo.db.itineraries.find_one({"_id": ObjectId(trip_id)})
    if not trip:
        return jsonify({"error": "Trip not found"}), 404
    return render_template(
        "itinerary.html",
        trip=trip,
        user=current_user,
        google_maps_api_key=os.getenv("GOOGLEMAPS_API_KEY"),
    )


@app.route("/mainpage/<username>")
@token_required
def mainpage(current_user, username):
    print(f"Mainpage route accessed for user: {username}")  # Debugging print statement
    user = mongo.db.users.find_one({"username": username})
    if not user:
        return jsonify({"error": "User not found"}), 404

    for trip in user["profile"]["past_trips"]:
        user_names = []
        for user_id in trip["users"]:
            trip_user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
            if trip_user:
                user_names.append(trip_user["username"])
        trip["user_names"] = user_names

    return render_template(
        "mainpage.html",
        user=user,
        trip=user["profile"]["past_trips"],
        google_maps_api_key=os.getenv("GOOGLEMAPS_API_KEY"),
    )


@app.route("/trip/<trip_id>")
@token_required
def trip_detail(current_user, trip_id):
    print(
        f"Trip detail route accessed for trip_id: {trip_id}"
    )  # Debugging print statement
    trip = mongo.db.itineraries.find_one({"_id": ObjectId(trip_id)})
    if not trip:
        return jsonify({"error": "Trip not found"}), 404
    users = []
    for user_id in trip["users"]:
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            users.append(user["username"])
    trip["user_names"] = users

    return render_template(
        "trip.html",
        trip=trip,
        user=current_user,
        rapidapi_key=os.getenv("RAPIDAPI_KEY"),
        google_maps_api_key=os.getenv("GOOGLEMAPS_API_KEY"),
    )


def initialize_database():
    test_users = [
        {
            "username": "testuser1",
            "password": "testpassword1",
            "email": "testuser1@example.com",
        },
        {
            "username": "testuser2",
            "password": "testpassword2",
            "email": "testuser2@example.com",
        },
    ]

    user_ids = []
    for user in test_users:
        existing_user = mongo.db.users.find_one({"username": user["username"]})
        if not existing_user:
            hashed_password = generate_password_hash(user["password"])
            user_id = mongo.db.users.insert_one(
                {
                    "username": user["username"],
                    "password": hashed_password,
                    "email": user["email"],
                    "profile": {
                        "name": f"Test User {user['username'][-1]}",
                        "past_trips": [],
                    },
                }
            ).inserted_id
            user_ids.append(user_id)
            print(f"Test user {user['username']} created with user_id: {user_id}")
        else:
            user_ids.append(existing_user["_id"])

    # check if the itinerary already exists
    existing_itinerary = mongo.db.itineraries.find_one({"trip_name": "Test Trip"})
    if not existing_itinerary:
        # create a dummy chatroom in the chatrooms collection
        chatroom_id = mongo.db.chatrooms.insert_one(
            {
                "chat_logs": [
                    {
                        "user_id": user_ids[0],
                        "username": "testuser1",
                        "message": "Looking forward to the trip!",
                        "timestamp": datetime.utcnow().strftime("%H:%M"),
                    },
                    {
                        "user_id": user_ids[1],
                        "username": "testuser2",
                        "message": "Don't forget to pack comfortable shoes.",
                        "timestamp": datetime.utcnow().strftime("%H:%M"),
                    },
                ],
            }
        ).inserted_id

        # create a dummy itinerary in the itineraries collection
        itinerary_id = mongo.db.itineraries.insert_one(
            {
                "trip_name": "Test Trip",
                "users": user_ids,
                "chatroom_id": chatroom_id,
                "itinerary": [
                    {
                        "activity": "Visit Eiffel Tower",
                        "location": "Paris",
                        "time": datetime(2022, 7, 15, 10, 0).isoformat(),
                        "notes": "Buy tickets online",
                    },
                    {
                        "activity": "Lunch at Le Jules Verne",
                        "location": "Paris",
                        "time": datetime(2022, 7, 15, 13, 0).isoformat(),
                        "notes": "Reservation at 1 PM",
                    },
                ],
                "budget": [
                    {
                        "user_id": user_ids[0],
                        "flight": 300,
                        "hotel": 400,
                        "food": 200,
                        "transport": 150,
                        "activities": 200,
                        "spending": 100,
                    },
                    {
                        "user_id": user_ids[1],
                        "flight": 200,
                        "hotel": 300,
                        "food": 100,
                        "transport": 50,
                        "activities": 100,
                        "spending": 80,
                    },
                ],
                "invite_code": generate_invite_code(),
            }
        ).inserted_id

        itinerary = mongo.db.itineraries.find_one({"_id": ObjectId(itinerary_id)})

        # add the itinerary to each user's past trips
        for user_id in user_ids:
            mongo.db.users.update_one(
                {"_id": ObjectId(user_id)}, {"$push": {"profile.past_trips": itinerary}}
            )

        print(
            f"Dummy itinerary added to past trips for both test users with itinerary_id: {itinerary_id}"
        )
    else:
        # chatroom_id = existing_itinerary["chatroom_id"]
        print("Dummy itinerary already exists with chatroom_id")


# def initialize_database():
#     test_users = [
#         {
#             "username": "testuser1",
#             "password": "testpassword1",
#             "email": "testuser1@example.com",
#         },
#         {
#             "username": "testuser2",
#             "password": "testpassword2",
#             "email": "testuser2@example.com",
#         },
#     ]

#     user_ids = []
#     for user in test_users:
#         existing_user = mongo.db.users.find_one({"username": user["username"]})
#         if not existing_user:
#             hashed_password = generate_password_hash(user["password"])
#             user_id = mongo.db.users.insert_one(
#                 {
#                     "username": user["username"],
#                     "password": hashed_password,
#                     "email": user["email"],
#                     "profile": {
#                         "name": f"Test User {user['username'][-1]}",
#                         "past_trips": [],
#                     },
#                 }
#             ).inserted_id
#             user_ids.append(user_id)
#             print(f"Test user {user['username']} created with user_id: {user_id}")
#         else:
#             user_ids.append(existing_user["_id"])

#     # check if the itinerary already exists
#     existing_itinerary = mongo.db.itineraries.find_one({"trip_name": "Test Trip"})
#     if not existing_itinerary:
#         # create a dummy chatroom in the chatrooms collection
#         chatroom_id = mongo.db.chatrooms.insert_one(
#             {
#             "chat_logs": [
#                 {
#                 "user_id": user_ids[0],
#                 "username": "testuser1",
#                 "message": "Looking forward to the trip!",
#                 "timestamp": datetime.utcnow().strftime("%H:%M"),
#                 },
#                 {
#                 "user_id": user_ids[1],
#                 "username": "testuser2",
#                 "message": "Don't forget to pack comfortable shoes.",
#                 "timestamp": datetime.utcnow().strftime("%H:%M"),
#                 },
#             ],
#             }
#         ).inserted_id

#         # create a dummy itinerary in the itineraries collection
#         itinerary_id = mongo.db.itineraries.insert_one(
#             {
#                 "trip_name": "Test Trip",
#                 "users": user_ids,
#                 "chatroom_id": chatroom_id,
#                 "itinerary": [
#                     {
#                         "activity": "Visit Eiffel Tower",
#                         "location": "Paris",
#                         "time": datetime(2022, 7, 15, 10, 0).isoformat(),
#                         "notes": "Buy tickets online",
#                     },
#                     {
#                         "activity": "Lunch at Le Jules Verne",
#                         "location": "Paris",
#                         "time": datetime(2022, 7, 15, 13, 0).isoformat(),
#                         "notes": "Reservation at 1 PM",
#                     },

#                 ],
#                 "budget" :  [
#                     {
#                     "user_id": user_ids[0],
#                     "flight": 300,
#                     "hotel": 400,
#                     "food": 200,
#                     "transport": 150,
#                     "activities": 200,
#                     "spending": 100,
#                     },
#                     {
#                     "user_id": user_ids[1],
#                     "flight": 200,
#                     "hotel": 300,
#                     "food": 100,
#                     "transport": 50,
#                     "activities": 100,
#                     "spending": 80,
#                     },
#                 ],
#             }
#         ).inserted_id

#         itinerary = mongo.db.itineraries.find_one({"_id": ObjectId(itinerary_id)})

#         # add the itinerary to each user's past trips
#         for user_id in user_ids:
#             mongo.db.users.update_one(
#                 {"_id": ObjectId(user_id)}, {"$push": {"profile.past_trips": itinerary}}
#             )

#         print(
#             f"Dummy itinerary added to past trips for both test users with itinerary_id: {itinerary_id}"
#         )
#     else:
#         if "chatroom_id" not in existing_itinerary:
#             chatroom_id = mongo.db.chatrooms.insert_one({"chat_logs": []}).inserted_id
#             mongo.db.itineraries.update_one(
#                 {"_id": existing_itinerary["_id"]},
#                 {"$set": {"chatroom_id": chatroom_id}},
#             )
#             print(
#                 f"Chatroom added to existing itinerary with id: {existing_itinerary['_id']}"
#             )
#         else:
#             print("Dummy itinerary already exists with chatroom_id")


initialize_database()

if __name__ == "__main__":
    app.run(debug=True)

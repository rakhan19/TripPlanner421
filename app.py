from flask import Flask, render_template, request, jsonify
from werkzeug.security import generate_password_hash
from flask_cors import CORS
from dotenv import load_dotenv
import os
from datetime import datetime
from bson.objectid import ObjectId

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

from backend.models import mongo

mongo.init_app(app)

from backend.auth import auth_bp
from backend.chat import chat_bp
from backend.itinerary import itinerary_bp
from backend.budget import budget_bp

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(chat_bp, url_prefix="/chat")
app.register_blueprint(itinerary_bp, url_prefix="/itinerary")
app.register_blueprint(budget_bp, url_prefix="/budget")


@app.route("/")
def welcome():
    return render_template("welcome.html")


@app.route("/admit")
def admit():
    return render_template("admit.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/main")
def main():
    return render_template("mainpage.html")


@app.route("/trip")
def trip():
    return render_template("trip.html")


@app.route("/chat")
def chat():
    return render_template("chat.html")


@app.route("/budget")
def budget():
    return render_template("budget.html")


@app.route("/mainpage/<username>")
def mainpage(username):
    user = mongo.db.users.find_one({"username": username})
    if not user:
        return jsonify({"error": "user not found"}), 404

    for trip in user["profile"]["past_trips"]:
        user_names = []
        for user_id in trip["users"]:
            trip_user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
            if trip_user:
                user_names.append(trip_user["username"])
        trip["user_names"] = user_names

    return render_template("mainpage.html", user=user)


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
        # create a dummy itinerary in the itineraries collection
        itinerary_id = mongo.db.itineraries.insert_one(
            {
                "trip_name": "Test Trip",
                "users": user_ids,
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
                "chat_logs": [
                    {
                        "user_id": user_ids[0],
                        "message": "Looking forward to the trip!",
                        "timestamp": datetime.utcnow().isoformat(),
                    },
                    {
                        "user_id": user_ids[1],
                        "message": "Don't forget to pack comfortable shoes.",
                        "timestamp": datetime.utcnow().isoformat(),
                    },
                ],
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
        print("Dummy itinerary already exists")

initialize_database()


if __name__ == "__main__":
    app.run(debug=True)

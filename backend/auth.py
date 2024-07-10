# app.py
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
import jwt
import datetime
from functools import wraps
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

CORS(
    app,
    resources={r"/*": {"origins": ["http://localhost:3000", "http://127.0.0.1:3000"]}},
    supports_credentials=True,
)



# Get MongoDB URI and Secret Key from environment variables
MONGO_URI = os.getenv("MONGO_URI")
SECRET_KEY = os.getenv("SECRET_KEY")

if not MONGO_URI:
    raise ValueError("MONGO_URI is not set in the environment variables")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set in the environment variables")

app.config["MONGO_URI"] = MONGO_URI
app.config["SECRET_KEY"] = SECRET_KEY

# Create a new client and connect to the server
client = MongoClient(MONGO_URI, server_api=ServerApi("1"))

# Send a ping to confirm a successful connection
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
    mongo = client
    users_collection = mongo.db.users
except Exception as e:
    print("Failed to connect to MongoDB.")
    print(e)
    mongo = None
    users_collection = None


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("x-access-token")
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = users_collection.find_one({"username": data["username"]})
        except Exception as e:
            print("Token validation failed.")
            print(e)
            return jsonify({"error": "Token is invalid"}), 401
        return f(current_user, *args, **kwargs)

    return decorated


@app.route("/register", methods=["POST"])
def register():
    if users_collection is None:
        return jsonify({"error": "Database connection failed"}), 500

    data = request.get_json()
    username = data["username"]
    password = data["password"]

    if users_collection.find_one({"username": username}):
        return jsonify({"error": "User already exists"}), 400

    hashed_password = generate_password_hash(password)
    user_id = users_collection.insert_one(
        {
            "username": username,
            "password": hashed_password,
            "email": data["email"],
            "trips": [],
        }
    ).inserted_id

    return (
        jsonify({"message": "User registered successfully", "user_id": str(user_id)}),
        201,
    )


@app.route("/login", methods=["POST"])
def login():
    if users_collection is None:
        return jsonify({"error": "Database connection failed"}), 500

    data = request.get_json()
    username = data["username"]
    password = data["password"]

    user = users_collection.find_one({"username": username})

    if user and check_password_hash(user["password"], password):
        token = jwt.encode(
            {
                "username": user["username"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
            },
            app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        return jsonify({"token": token}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401


@app.route("/protected", methods=["GET"])
@token_required
def protected(current_user):
    return jsonify({"message": f'Welcome {current_user["username"]}'})


if __name__ == "__main__":
    app.run(debug=True)

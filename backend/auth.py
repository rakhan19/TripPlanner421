from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models import mongo
import jwt
import datetime
from functools import wraps
import os

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/admit", methods=["GET"])
def templ():
    return render_template('admit.html')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("x-access-token")
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        try:
            data = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
            current_user = mongo.db.users.find_one({"username": data["username"]})
        except Exception as e:
            return jsonify({"error": "Token is invalid"}), 401
        return f(current_user, *args, **kwargs)

    return decorated

def register_test(db, data):
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")

    if not username or not password or not email:
        return {'status_code': 400, 'json': {"error": "Invalid input"}}

    if db.users.find_one({"username": username}):
        return {'status_code': 400, 'json': {"error": "User already exists"}}

    hashed_password = generate_password_hash(password)
    user_id = db.users.insert_one(
        {
            "username": username,
            "password": hashed_password,
            "email": email,
            "profile": {"name": "", "age": 0, "gender": "", "past_trips": []},
        }
    ).inserted_id

    return {'status_code': 201, 'json': {"message": "User registered successfully", "user_id": str(user_id)}}

@auth_bp.route("/signup", methods=["GET", "POST"])
def register():
    #Request Form instead of using get_json()
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")
    if request.method == "POST":
        if not username or not password or not email:
            return jsonify({"error": "Invalid input"}), 400

        if mongo.db.users.find_one({"username": username}):
            return jsonify({"error": "User already exists"}), 400

        hashed_password = generate_password_hash(password)
        user_id = mongo.db.users.insert_one(
            {
                "username": username,
                "password": hashed_password,
                "email": email,
                "profile": {"name": "", "past_trips": []},
            }
        ).inserted_id
        #return jsonify({"message": "User registered successfully", "user_id": str(user_id)}), 201, 
        return redirect(url_for('mainpage', username=username))
    
    return render_template('signup.html') 
    #return jsonify({"message": "User registered successfully", "user_id": str(user_id)}), 201
    

def login_test(db, data):
    username = data.get("username")
    password = data.get("password")
    
    user = db.users.find_one({"username": username})
    
    if user and check_password_hash(user["password"], password):
        token = jwt.encode(
            {
                "username": user["username"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
            },
            os.getenv("SECRET_KEY"),
            algorithm="HS256",
        )
        return {"status_code": 200, "json": {"token": token}}
    return {"status_code": 401, "json": {"error": "Invalid username or password"}}

@auth_bp.route("/admit", methods=["GET","POST"])
def login():
    #data = request.get_json()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = mongo.db.users.find_one({"username": username})
        if user and check_password_hash(user["password"], password):
            token = jwt.encode(
                {
                    "username": user["username"],
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
                },
                os.getenv("SECRET_KEY"),
                algorithm="HS256",
            )
            return redirect(url_for('mainpage', username=username))
            #return jsonify({"token": token}), 200
        return jsonify({"error": "Invalid username or password"}), 401
        #return render_template('login.html', error="Incorrect username or password")
    return render_template('login.html')
    #return jsonify({"error": "Invalid username or password"}), 401
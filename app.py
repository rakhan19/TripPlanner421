from flask import Flask, render_template, request, jsonify
from werkzeug.security import generate_password_hash
from flask_cors import CORS
from dotenv import load_dotenv
import os

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
        return jsonify({"error:": "user not found"}), 404
    return render_template("mainpage.html", user=user)


if __name__ == "__main__":
    app.run(debug=True)


# from flask import Flask, render_template, request

# app = Flask(__name__)

# @app.route('/')
# def welcome():
#     return render_template('welcome.html')

# @app.route('/admit')
# def admit():
#     return render_template('admit.html')

# @app.route('/signup')
# def signup():
#     return render_template('signup.html')

# @app.route('/main')
# def mainpage():
#     return render_template('mainpage.html')

# @app.route('/trip')
# def trip():
#     return render_template('trip.html')

# @app.route('/chat')
# def chat():
#     return render_template('chat.html')

# @app.route('/budget')
# def budget():
#     return render_template('budget.html')

# if __name__=='__main__':
#     app.run(debug="True")

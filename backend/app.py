from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

from models import mongo

mongo.init_app(app)

from auth import auth_bp
from chat import chat_bp
from itinerary import itinerary_bp
from budget import budget_bp

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(chat_bp, url_prefix="/chat")
app.register_blueprint(itinerary_bp, url_prefix="/itinerary")
app.register_blueprint(budget_bp, url_prefix="/budget")

if __name__ == "__main__":
    app.run(debug=True)

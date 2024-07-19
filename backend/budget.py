from flask import Blueprint, request, jsonify
from backend.models import mongo
from backend.auth import token_required

budget_bp = Blueprint("budget", __name__)


@budget_bp.route("/<trip_id>/expenses", methods=["POST"])
@token_required
def add_expense(current_user, trip_id):
    data = request.get_json()
    category = data.get("category")
    amount = data.get("amount")
    description = data.get("description")
    if not category or not amount or not description:
        return jsonify({"error": "Invalid input"}), 400
    expense = {"category": category, "amount": amount, "description": description}
    mongo.db.trips.update_one({"_id": trip_id}, {"$push": {"budget.expenses": expense}})
    return jsonify({"message": "Expense added"}), 201


@budget_bp.route("/<trip_id>/expenses", methods=["GET"])
@token_required
def get_expenses(current_user, trip_id):
    trip = mongo.db.trips.find_one({"_id": trip_id})
    return jsonify(trip["budget"]["expenses"]), 200

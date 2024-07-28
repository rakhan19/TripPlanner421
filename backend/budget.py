from flask import Blueprint, request, jsonify, redirect, url_for
from backend.models import mongo
from backend.auth import token_required
from bson import ObjectId


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


@budget_bp.route("/<trip_id>/updated", methods=["POST"])
@token_required
def update_expenses(current_user, trip_id):
    user_id = ObjectId(request.form.get("user_id"))

    budget_items = []
    for field in ["flight", "hotel", "food", "transport", "activities", "spending"]:
        value = request.form.get(field)
        try:
            # Convert to float and ensure two decimal precision
            budget_items.append(float(value))
        except ValueError:
            # Default to 0 if conversion fails
            budget_items.append(0)

    # Assign budget items to variables
    flight = budget_items[0]
    hotel = budget_items[1]
    food = budget_items[2]
    transport = budget_items[3]
    activities = budget_items[4]
    spending = budget_items[5]

    updated_budget = {
        "flight": flight,
        "hotel": hotel,
        "food": food,
        "transport": transport,
        "activities": activities,
        "spending": spending,
    }
    result = mongo.db.itineraries.update_one(
        {"_id": ObjectId(trip_id), "budget.user_id": user_id},
        {
            "$set": {
                "budget.$.flight": updated_budget["flight"],
                "budget.$.hotel": updated_budget["hotel"],
                "budget.$.food": updated_budget["food"],
                "budget.$.transport": updated_budget["transport"],
                "budget.$.activities": updated_budget["activities"],
                "budget.$.spending": updated_budget["spending"],
            }
        },
    )

    return redirect(url_for("budget", trip_id=trip_id))

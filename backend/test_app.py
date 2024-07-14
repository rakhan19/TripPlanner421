import pytest
from flask import json
from app import app as flask_app
from models import mongo


@pytest.fixture
def app():
    flask_app.config["TESTING"] = True
    flask_app.config["MONGO_URI"] = "mongodb://localhost:27017/testdb"
    mongo.init_app(flask_app)

    with flask_app.app_context():
        # Setup database
        mongo.db.users.drop()
        mongo.db.trips.drop()
        mongo.db.itineraries.drop()
        mongo.db.chatrooms.drop()
        mongo.db.budgets.drop()

    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


def register_user(client, username, password, email):
    return client.post(
        "/auth/register",
        data=json.dumps({"username": username, "password": password, "email": email}),
        content_type="application/json",
    )


def login_user(client, username, password):
    return client.post(
        "/auth/login",
        data=json.dumps({"username": username, "password": password}),
        content_type="application/json",
    )


def test_register(client):
    rv = register_user(client, "testuser", "testpassword", "test@example.com")
    assert rv.status_code == 201
    json_data = rv.get_json()
    assert "user_id" in json_data


def test_login(client):
    register_user(client, "testuser", "testpassword", "test@example.com")
    rv = login_user(client, "testuser", "testpassword")
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert "token" in json_data


def test_add_message(client):
    register_user(client, "testuser", "testpassword", "test@example.com")
    login_response = login_user(client, "testuser", "testpassword")
    token = login_response.get_json()["token"]
    trip_id = mongo.db.trips.insert_one(
        {
            "trip_name": "Test Trip",
            "trip_owner": mongo.db.users.find_one({"username": "testuser"})["_id"],
            "members": [],
            "itinerary_id": None,
            "chatroom_id": None,
            "budget_id": None,
        }
    ).inserted_id

    rv = client.post(
        f"/chat/{trip_id}/messages",
        headers={"x-access-token": token},
        data=json.dumps({"message": "Hello, this is a test message."}),
        content_type="application/json",
    )

    assert rv.status_code == 201
    json_data = rv.get_json()
    assert json_data["message"] == "Message added"


def test_create_poll(client):
    register_user(client, "testuser", "testpassword", "test@example.com")
    login_response = login_user(client, "testuser", "testpassword")
    token = login_response.get_json()["token"]
    trip_id = mongo.db.trips.insert_one(
        {
            "trip_name": "Test Trip",
            "trip_owner": mongo.db.users.find_one({"username": "testuser"})["_id"],
            "members": [],
            "itinerary_id": None,
            "chatroom_id": None,
            "budget_id": None,
        }
    ).inserted_id

    rv = client.post(
        f"/chat/{trip_id}/polls",
        headers={"x-access-token": token},
        data=json.dumps({"question": "Test poll?", "options": ["Yes", "No"]}),
        content_type="application/json",
    )

    assert rv.status_code == 201
    json_data = rv.get_json()
    assert json_data["message"] == "Poll created"


def test_add_itinerary_item(client):
    register_user(client, "testuser", "testpassword", "test@example.com")
    login_response = login_user(client, "testuser", "testpassword")
    token = login_response.get_json()["token"]
    trip_id = mongo.db.trips.insert_one(
        {
            "trip_name": "Test Trip",
            "trip_owner": mongo.db.users.find_one({"username": "testuser"})["_id"],
            "members": [],
            "itinerary_id": None,
            "chatroom_id": None,
            "budget_id": None,
        }
    ).inserted_id

    rv = client.post(
        f"/itinerary/{trip_id}/items",
        headers={"x-access-token": token},
        data=json.dumps(
            {
                "activity": "Test activity",
                "location": "Test location",
                "time": "2024-07-12T12:00:00",
                "notes": "Test notes",
            }
        ),
        content_type="application/json",
    )

    assert rv.status_code == 201
    json_data = rv.get_json()
    assert json_data["message"] == "Itinerary item added"


def test_add_expense(client):
    register_user(client, "testuser", "testpassword", "test@example.com")
    login_response = login_user(client, "testuser", "testpassword")
    token = login_response.get_json()["token"]
    trip_id = mongo.db.trips.insert_one(
        {
            "trip_name": "Test Trip",
            "trip_owner": mongo.db.users.find_one({"username": "testuser"})["_id"],
            "members": [],
            "itinerary_id": None,
            "chatroom_id": None,
            "budget_id": None,
        }
    ).inserted_id

    rv = client.post(
        f"/budget/{trip_id}/expenses",
        headers={"x-access-token": token},
        data=json.dumps(
            {
                "category": "Test category",
                "amount": 100.0,
                "description": "Test description",
            }
        ),
        content_type="application/json",
    )

    assert rv.status_code == 201
    json_data = rv.get_json()
    assert json_data["message"] == "Expense added"


# import requests

# BASE_URL = "http://127.0.0.1:5000"


# def test_register():
#     url = f"{BASE_URL}/auth/register"
#     payload = {
#         "username": "testuser",
#         "password": "Test@1234",
#         "email": "testuser@example.com",
#     }
#     response = requests.post(url, json=payload)
#     print("Raw Register Response Content:", response.text)
#     try:
#         print("Register Response JSON:", response.json())
#     except requests.exceptions.JSONDecodeError as e:
#         print("Failed to decode JSON response:", e)


# def test_login():
#     url = f"{BASE_URL}/auth/login"
#     payload = {"username": "testuser", "password": "Test@1234"}
#     response = requests.post(url, json=payload)
#     print("Raw Login Response Content:", response.text)
#     try:
#         print("Login Response JSON:", response.json())
#     except requests.exceptions.JSONDecodeError as e:
#         print("Failed to decode JSON response:", e)
#     return response.json().get("token")


# def test_chat(token):
#     url = f"{BASE_URL}/chat/1/messages"
#     headers = {"x-access-token": token}
#     payload = {"message": "Hello, World!"}
#     response = requests.post(url, headers=headers, json=payload)
#     print("Raw Chat Response Content:", response.text)
#     try:
#         print("Chat Response JSON:", response.json())
#     except requests.exceptions.JSONDecodeError as e:
#         print("Failed to decode JSON response:", e)
#     return response.json().get("message")


# def test_poll(token):
#     url = f"{BASE_URL}/chat/1/polls"
#     headers = {"x-access-token": token}
#     payload = {
#         "question": "What is your favorite color?",
#         "options": ["Red", "Green", "Blue"],
#     }
#     response = requests.post(url, headers=headers, json=payload)
#     print("Raw Poll Response Content:", response.text)
#     try:
#         print("Poll Response JSON:", response.json())
#     except requests.exceptions.JSONDecodeError as e:
#         print("Failed to decode JSON response:", e)
#     return response.json().get("message")


# def test_protected(token):
#     url = f"{BASE_URL}/protected"
#     headers = {"x-access-token": token}
#     response = requests.get(url, headers=headers)
#     print("Raw Protected Response Content:", response.text)
#     try:
#         print("Protected Response JSON:", response.json())
#     except requests.exceptions.JSONDecodeError as e:
#         print("Failed to decode JSON response:", e)


# def test_itenerary(token):
#     url = f"{BASE_URL}/itinerary/1/items"
#     headers = {"x-access-token": token}
#     payload = {
#         "activity": "Hiking",
#         "location": "Mount Everest",
#         "time": "2021-12-31T23:59:59",
#         "notes": "Bring water and snacks",
#     }
#     response = requests.post(url, headers=headers, json=payload)
#     print("Raw Itinerary Response Content:", response.text)
#     try:
#         print("Itinerary Response JSON:", response.json())
#     except requests.exceptions.JSONDecodeError as e:
#         print("Failed to decode JSON response:", e)
#     return response.json().get("message")


# if __name__ == "__main__":
#     print("Testing User Registration:")
#     test_register()

#     print("\nTesting User Login:")
#     token = test_login()

#     # if token:
#     #     print("\nTesting Protected Route with Valid Token:")
#     #     test_protected(token)
#     # else:
#     #     print("\nLogin failed, cannot test protected route.")

#     print("\nTesting Chat:")
#     test_chat(token)

#     print("\nTesting Poll:")
#     test_poll(token)

#     print("\nTesting Itinerary:")
#     test_itenerary(token)

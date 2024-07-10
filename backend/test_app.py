import requests

BASE_URL = "http://127.0.0.1:5000"


def test_register():
    url = f"{BASE_URL}/register"
    payload = {
        "username": "testuser",
        "password": "Test@1234",
        "email": "testuser@example.com",
    }
    response = requests.post(url, json=payload)
    print("Raw Register Response Content:", response.text)
    try:
        print("Register Response JSON:", response.json())
    except requests.exceptions.JSONDecodeError as e:
        print("Failed to decode JSON response:", e)


def test_login():
    url = f"{BASE_URL}/login"
    payload = {"username": "testuser", "password": "Test@1234"}
    response = requests.post(url, json=payload)
    print("Raw Login Response Content:", response.text)
    try:
        print("Login Response JSON:", response.json())
    except requests.exceptions.JSONDecodeError as e:
        print("Failed to decode JSON response:", e)
    return response.json().get("token")


def test_protected(token):
    url = f"{BASE_URL}/protected"
    headers = {"x-access-token": token}
    response = requests.get(url, headers=headers)
    print("Raw Protected Response Content:", response.text)
    try:
        print("Protected Response JSON:", response.json())
    except requests.exceptions.JSONDecodeError as e:
        print("Failed to decode JSON response:", e)


if __name__ == "__main__":
    print("Testing User Registration:")
    test_register()

    print("\nTesting User Login:")
    token = test_login()

    if token:
        print("\nTesting Protected Route with Valid Token:")
        test_protected(token)
    else:
        print("\nLogin failed, cannot test protected route.")

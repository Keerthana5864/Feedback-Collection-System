import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_login():
    print("--- Testing Login ---")
    payload = {
        "email": "admin@demo.com",
        "password": "admin123",
        "institution_id": 1001
    }
    try:
        response = requests.post(f"{BASE_URL}/login", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error during login test: {e}")

def test_institution_register():
    print("\n--- Testing Institution Registration ---")
    payload = {
        "name": "Test University",
        "admin_email": "test_admin_new@example.com",
        "admin_password": "password123"
    }
    try:
        response = requests.post(f"{BASE_URL}/institutions/register", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error during registration test: {e}")

if __name__ == "__main__":
    test_login()
    test_institution_register()
